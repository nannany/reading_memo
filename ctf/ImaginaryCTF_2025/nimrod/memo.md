```text
And Cush begat Nimrod: he began to be a mighty one in the earth.
```

## Writeup (ImaginaryCTF 2025 – nimrod)

### 概要
- Nim で書かれた検証バイナリ。標準入力で受け取ったフラグを「同じ方式で暗号化」し、バイナリ内に埋め込まれた暗号文と一致すれば `Correct!`。
- 従って、埋め込み暗号文を同じキーストリームで XOR すれば平文（フラグ）が復元できる。

### 解析の要点
- 文字列に `Enter the flag: / Correct! / Incorrect.` があり、Nim ランタイム関数名も残存。
- `NimMainInner` 付近のフロー（逆アセンブル）:
  - `readLine` → `nsuStrip`（前後空白除去）
  - `xorEncrypt__nimrod_46(input, key=0x13371337)`
  - `eqeq___nimrod_69(result, encryptedFlag__nimrod_10)`（等価比較）
  - 一致なら `Correct!`、不一致なら `Incorrect.` を出力
- `keystream__nimrod_20`（キーストリーム生成）の中身:
  - 32bit LCG: `x = (x * 0x19660D + 0x3C6EF35F) & 0xffffffff`
  - キーストリーム1バイト: `(x >> 16) & 0xff`
  - 暗号化は `cipher[i] = plain[i] XOR keystream[i]`

### 埋め込み暗号文
- `.rodata` に Nim のシーケンスとして格納（長さとデータの2ワード）。
- VA 0x116e0 に長さ（`len=34`）、続く VA 0x116f0 から34バイトが暗号文。
- 暗号文（抜粋）: `28f83ee63e2f430cb996d15cd6bf36d820790e8e5221b250e398b5c9b8a08830d90a`

### 復号手順
1) シード `0x13371337` から LCG を回し、長さ分のキーストリームを生成。
2) 暗号文と XOR → 平文フラグ。

### ソルバ
- 追加済: `ctf/ImaginaryCTF_2025/nimrod/solve.py`
- 使い方:
  - `python3 ctf/ImaginaryCTF_2025/nimrod/solve.py ctf/ImaginaryCTF_2025/nimrod/nimrod`
- 出力:
```
ictf{a_mighty_hunter_bfc16cce9dc8}
```

### 小ネタ
- 問題名とメモの引用は聖書のニムロド（mighty hunter）由来。フラグ文言と対応している。
