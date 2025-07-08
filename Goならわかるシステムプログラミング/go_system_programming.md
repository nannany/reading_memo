# 4. 低レベルアクセスへの入口3: チャネル

## 4.1 goroutine

## 4.2 チャネル

### 4.2.1 チャネルの使用方法

後半のクローズされているかを確認する方法がない、というところはよくわかってない。

### 4.2.2 チャネルの3つの状態

バッファなしチャネル、バッファ付きチャネル、閉じたチャネル

### 4.2.3 for文

forとくっつけて、channelを使うと、チャネルが閉じられるまでループすることができる。

### 4.2.4 チャネルとselect文

### 4.2.5 コンテキスト

## 4.3 システムからの通知

## 4.5 問題

# 5 システムコール

## 5.3 POSIXとC言語の標準規格

## 5.4 システムコールより内側の世界

## 5.5 Go言語のシステムコールとPOSIX

# 6 TCPソケットとHTTPの実装

## 6.1 プロトコルとレイヤー

## 6.2 HTTPとその上のプロトコルたち

## 6.3 ソケットとは

## 6.4 ソケット通信の基本構造

クライアント側はDial(), サーバ側はListen()を使う。
それぞれ net.Conn インターフェースが返ってくるので、以後はそれを用いて諸々する。

## 6.5 Go言語でHTTPサーバを実装する

## 6.6 速度改善(1): HTTP/1.1のKeep-Aliveに対応させる

tcpの接続を閉じないようにすることで、同じ接続を使いまわすことができる。 

Accept()メソッドは、3way handshakeが完了するまではブロックし、完了後は、接続を受け付ける。


---

3way handshakeについて、なぜ3wayなのか調べてみた。
主な理由は

https://www.ietf.org/rfc/rfc793.html

```
 The principle reason for the three-way handshake is to prevent old
  duplicate connection initiations from causing confusion.k
```

つまり、古いtcp接続の再利用を防ぐため、ということらしい。

## 6.7 速度改善(2): 圧縮

Accept-Encodingヘッダは、クライアント->サーバのリクエストヘッダに付与し、対応している圧縮方式を指定する。

Content-Encodingヘッダは、サーバ->クライアントのレスポンスヘッダに付与し、実際の圧縮方式を指定する。
クライアント->サーバのリクエストにおいても圧縮をしている場合は、Content-Encodingヘッダにその圧縮方式を指定する。

ヘッダの圧縮についてもあるようで、その際にはHPACKという方式を使う。

https://datatracker.ietf.org/doc/html/rfc7541

## 6.8 速度改善(3): チャンク形式のボディー送信

transfer-encoding: chunked ヘッダを使うことで、ボディーをチャンク形式で送信することができる。

最初にサイズがあり、その後にデータが続く。

## 6.9 速度改善(4): パイプライニング

# 7 UDPソケットを使ったマルチキャスト通信

## 7.1 UDPとTCPの用途の違い

UDPはDNSやNTP,WebRTCなどで使われている。

### 7.1.1 UDPが使われる場面は今と昔で変わってきている

[tcp輻輳制御のwiki](https://en.wikipedia.org/wiki/TCP_congestion_control).日本語版がない。。

[ネットゲームにおけるTCP/UDPの使い分け](https://www.slideshare.net/slideshow/tcpudp-81497235/81497235)


## 7.2 UDPとTCPの処理の流れの違い

## 7.3 UDPのマルチキャストの実装例

## 7.4 UDPを使った実世界のサンプル

### 7.4.1 NTP

### 7.4.2 同じネットワーク内部で仲間を探す

[peer discovery](https://github.com/schollz/peerdiscovery)

## 7.5 UDPとTCPの機能面の違い

# 8 高速なUNIXドメインソケット

## 8.1 UNIXドメインソケットの基本

UNIXドメインソケットによる通信は、TCPなどの外部ネットワークとの通信に用いられるものではなくて、カーネル内部の通信に用いられる。

ソケットファイルという特殊なファイルを作成して、それでやり取りをする。

同じホスト内のDBとWebサーバ間の通信などで使われる。

## 8.2 Unixドメインソケットの使い方

dockerクライアントとdockerd間の通信は、UNIXドメインソケットを使っている。
これは、`/var/run/docker.sock` というファイルを介して行われる。
なぜUNIXドメインソケットを使うのかというと、TCP/IPよりも高速で、セキュリティ的にも優れているから。

## 8.3 Windowsの名前付きパイプ

npipeは、WindowsのUNIXドメインソケットに相当するもの。



