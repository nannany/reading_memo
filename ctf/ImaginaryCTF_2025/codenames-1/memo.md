# ImaginaryCTF 2025 – codenames-1 Writeup

- 種別: Web (Flask + Flask-SocketIO)
- 目標: `/flag.txt` の読み取り
- 結果: `language=/flag` でゲーム生成すると、盤面(`board`)経由で `/flag.txt` が漏洩し入手可能

## 脆弱性の概要（絶対パス合成の不備）
`challenge/app.py` のゲーム生成 `/create_game`:

```python
language = request.form.get('language', None)
if not language or '.' in language:
    language = LANGUAGES[0] if LANGUAGES else None
# 語彙リストの読み込み
wl_path = os.path.join(WORDS_DIR, f"{language}.txt")
with open(wl_path) as wf:
    word_list = [line.strip() for line in wf if line.strip()]
```

- `'.'` を含む値は却下されるが、`'/'`（絶対パス）のチェックがない。
- `language` に `'/flag'` を渡すと、`os.path.join('words', '/flag.txt')` は `'/flag.txt'` を返す（先頭が `/` のためベース無視）。
- その結果 `/flag.txt` が開かれ、ファイル内容が `word_list` として読み込まれる。
- 盤面生成は `words = random.sample(word_list, 25) if len(word_list) >= 25 else random.sample(word_list * 25, 25)` なので、1行しかない場合は同じ単語（= flag）が25マスに複製される。

さらに、ゲーム開始時（両者がWS接続すると）`start_game` イベントで以下が各プレイヤーに配布される:

```python
payload_common = {
    'board': game['board'],
    'revealed': game['revealed'],
    'clue_giver': game['clue_giver'],
    'team_color': game['team_color'],
    'score': game['score'],
    'clue': game['clue'],
    'guesses_remaining': game['guesses_remaining'],
    'hard_mode': game.get('hard_mode', False)
}
# colors はヒント役にのみ送付だが、board は両者に送られる
```

よって board に読み込んだ `/flag.txt` の内容がそのまま露出する。

## 取得手順（手動・プロキシ）
- Chrome を Burp/ZAP にプロキシ（HTTP/HTTPS）し、Intercept ON。
- ログイン後、Lobby の「Create Game」を送信する直前で `POST /create_game` を止める。
- リクエスト本文の `language=...` を `language=/flag` に書き換えて Forward。
- `/game/<CODE>` に遷移後、別セッションで同コードに Join（2人必須）。
- 両者が Socket.IO で参加した時点で `start_game` が飛び、画面の 25 マスが flag（またはそのコピー）で埋まる。

補足: DevTools でも可
- コンソールで `select[name="language"]` に `value="/flag"` の `<option>` を追加して選択→送信しても同様に通る。

## 取得手順（自動）
リポジトリにソルバを追加済み:
- `ctf/ImaginaryCTF_2025/codenames-1/solve.py`
- 依存: `pip install requests python-socketio websocket-client`
- 実行: `BASE_URL=http://<host>:<port> python3 ctf/ImaginaryCTF_2025/codenames-1/solve.py`
- 挙動: ユーザA/Bを登録→Aで `language=/flag` で作成→Bが参加→両WSで `start_game` を受け取り、board のユニーク語を列挙し先頭を flag 候補として表示。

## もう一つの flag について（設計上）
- Hard Mode 勝利時、ゲーム内に bot が参加していれば `update` payload に `flag: os.environ['FLAG_2']` が含まれる（`/add_bot` 経由で Selenium bot が起動）。
- 今回は `/flag.txt`（flag1）を board から読む方が容易。

## 修正案（防御）
- `language` は厳格ホワイトリスト（`LANGUAGES` に存在する名前のみ）で受け付ける。
- `'/'` やパス区切りを含む値は拒否。`os.path.isabs(language)` で弾く。
- `Path(WORDS_DIR, f"{language}.txt").resolve()` が `WORDS_DIR` 配下であることを検証（ディレクトリ外を拒否）。
- 可能ならフロントの `<select>` 値も固定（サーバ側の検証は必須）。

## まとめ
- 入力 `language` の絶対パスが `os.path.join` をバイパスし、`/flag.txt` が board に読み込まれたことが原因。
- 2プレイヤーが WebSocket 参加すると `board` が双方に配布されるため、画面上（またはソケット受信）で flag が取得できる。

