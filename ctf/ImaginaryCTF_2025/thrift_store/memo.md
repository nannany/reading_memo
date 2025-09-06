
# ImaginaryCTF 2025 – thrift_store Writeup

## 問題文
The frontend has gone down but the store is still open, can you buy the flag?

フロントエンドは落ちているが、ストアのバックエンドは生きている。どうにかして flag を「購入」できないか？

## 与えられたもの
- `capture.pcap`（ローカルバックエンドの通信キャプチャ）
- 実際の接続先: `thrift-store.chal.imaginaryctf.org:9090`

## 概要
- バックエンドは Apache Thrift の Strict Binary + Framed Transport（TFramedTransport + TBinaryProtocolStrict）。
- メソッドは `getInventory`, `createBasket`, `addToBasket`, `getBasket`, `pay`。
- PCAPからIDL(Internet Definition Language)を再構築し、最小クライアントでサーバに接続。`getInventory` に「flag」という商品（価格 9999）があることを確認。
- `createBasket` → `addToBasket(bid, "flag")` → `pay(bid, 9999)` で支払い成功レスポンスにフラグが含まれていた。

フラグ:
- ictf{l1k3_gRPC_bUt_l3ss_g0ogly}

---

## 解析

### プロトコルとストリーム
- `tshark -r capture.pcap -q -z io,phs` より、`thrift` が主要プロトコル。
- 会話はすべて `127.0.0.1:9090` の TCP 上で、Thriftの CALL/REPLY を確認。

代表的な呼び出し
- `CALL createBasket` → `REPLY createBasket`（UUID付与）
- `CALL addToBasket` → `REPLY addToBasket`（void想定）
- `CALL getBasket` → `REPLY getBasket`（カゴの中身）
- `CALL getInventory` → `REPLY getInventory`（商品一覧）
- `CALL pay` → `REPLY pay`（成功: 空struct/文字列、失敗: “Total does not match basket total”）

### インベントリと価格（PCAPから）
PCAP内のローカル環境では少なくとも以下の価格が確認できた（抜粋）。
- banana: 90
- apple-red-delicious: 120
- whole-milk-1l: 250
- brown-eggs-dozen: 450
- bread-sourdough-loaf: 500
- carrots-1kg: 300
- chicken-breast-500g: 750
- rice-basmati-1kg: 600
- olive-oil-500ml: 1200
- cheddar-cheese-200g: 550
- tomatoes-500g: 280
- onions-1kg: 250
- orange-juice-1l: 400
- potatoes-2kg: 350
- yogurt-plain-500g: 320

PCAP上では `pay` の検証として「合計と請求額が一致しないと例外」が返ることが確認できる。

### 型の推定（IDL再構築）
- `getInventory() -> list<struct { 1:id:string, 2:name:string, 3:price:i64, 4:opt description:string }>`
- `createBasket() -> string`（UUID）
- `addToBasket(1:basketId:string, 2:itemId:string) -> void`
- `getBasket(1:basketId:string) -> list<struct { 1:id:string, 2:quantity:i8 }>`
- `pay(1:basketId:string, 2:total:i64) -> (成功: 空struct or 文字列, 失敗: 例外)`

再構築IDLはリポジトリに保存:
- `ctf/ImaginaryCTF_2025/thrift_store/store.thrift`

### 気づき（脆弱性の可能性）
- `getBasket` の `quantity` が `i8`（符号付き8bit）。大量に `addToBasket` すると数量がオーバーフローし、合計計算が負方向に崩れる可能性がある。
- ただし、この問題では実サーバに `flag` という特別商品が存在し、通常フローでの購入が可能だったため、オーバーフローは使わずに解ける。

---

## 攻略方針
- ThriftのStrict Binary + Framedに対応する最小クライアントを実装。
- 実サーバに接続して `getInventory` を確認 → `flag` 商品を特定。
- `createBasket` → `addToBasket` → 合計は `getInventory` の価格通り → `pay` 実行。
- `pay` の成功レスポンスから文字列を収集し、フラグを抽出。

---

## 実装

### 最小クライアント
- 自前で Strict Binary のエンコード/デコードを実装（version header 0x80010000、Framedの4バイト長）。
- ファイル: `ctf/ImaginaryCTF_2025/thrift_store/solve.py`

ポイント
- メッセージ先頭は `0x80010000 | msg_type`（Strict Binary）。
- Framed Transportのため、送受信ともに「4バイト長 + メッセージ本体」。
- `pay` 成功時に文字列を含む可能性があるため、汎用の文字列収集を追加。

---

## 実行手順

1) リポジトリのスクリプトを実行
```
python3 solve.py thrift-store.chal.imaginaryctf.org 9090
```

2) 実行ログ（要約）
- Inventory 取得 → items: 16
- Most expensive: flag = 9999
- Basket 取得 → UUID
- addToBasket(bid, "flag") → pay(bid, 9999)

3) サーバ応答
- `pay` 成功時レスポンス中にフラグ文字列を確認

取得フラグ
```
ictf{l1k3_gRPC_bUt_l3ss_g0ogly}
```

---

## 代替アプローチ（未使用だが有効そうな手）
- `quantity: i8` を利用したオーバーフロー（例：高額商品を128回追加して quantity=-128 にし、負の合計で `pay` を通す）。
- PCAP上でも `pay` ミスマッチ時の例外が読めるため、バックエンド側で合計計算をそのまま評価していることが推測できる。

---

## 学び
- ThriftのStrict Binary + Framedは、先頭4バイト長と `0x80010000` ヘッダさえ押さえれば自前実装でも解析可能。
- PCAPから型（IDL）を段階的に復元し、最小限のクライアントで攻撃が通る。
- バックエンドに隠し商品がある典型パターン。まずは `getInventory` 確認が大正解。

---

## Appendix: 解析に使ったコマンド
- プロトコル確認
```
tshark -r capture.pcap -q -z io,phs
```
- 会話一覧
```
tshark -r capture.pcap -q -z conv,tcp
```
- ストリーム追跡
```
tshark -r capture.pcap -q -z follow,tcp,ascii,<stream_id>
```
- Thrift詳細の確認
```
tshark -r capture.pcap -Y thrift
tshark -r capture.pcap -Y "frame.number==<N>" -V
```

---

## Appendix: 追加ファイル
- `ctf/ImaginaryCTF_2025/thrift_store/store.thrift`（IDL）
- `ctf/ImaginaryCTF_2025/thrift_store/solve.py`（最小クライアント）
- `ctf/ImaginaryCTF_2025/thrift_store/solve_notes.md`（解析メモ）

以上。