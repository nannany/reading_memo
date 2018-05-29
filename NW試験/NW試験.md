# NW試験メモ

# h25_午後1_1
* ローカルのhostsファイルにドメイン名とIPアドレスを記述しておくと、DNSサーバに問い合わせに行く前にそこで名前解決しに行く。
* SSLについて問われている。以下参考記事。食べるSSLは読んでみたい。
<https://qiita.com/toshihirock/items/acbf9800f7e784118e46>
* ホスト名、ドメイン名、FQDNについて
  * RFC3986によるとこれらはURL内のauthority に当たる部分で、www.example.com というauthorityであった場合には、
    * example.com：ドメイン名にあたる。インターネット上のネットワークを特定する情報。
    * www：ホスト名にあたる。↑で特定されたネットワーク上のどのサーバに当たるかを特定する情報。wwwの場合は一般的にはwebサーバ。
    * www.example.com：FQDN
  * Qiitaとかのauthority部分はqiita.comだけどこれはホスト名がないという理解であっているのか？→qiita.comというネットワークにはwwwの1台のマシンしか存在しないため。おそらく。
<http://www.gabacho-net.jp/whims/whim0100.html>
* FTP,SIP,H.323などは制御用セッションとデータ用セッションが別であり、データ用セッションは動的にポート番号が変化する。
* nslookupしたときにあらわれる項目の意味は以下のよう。

```
C:\Users\nannany>nslookup qiita.com
サーバー:  UnKnown   ←DNSサーバの名前
Address:  192.168.2.1  ←DNSサーバのIP

権限のない回答:
名前:    qiita.com ←問い合わせ内容
Addresses:  2406:da14:add:901:60d8:5158:9752:4268  ←結果
          2406:da14:add:902:f3b0:3362:121d:81e
          2406:da14:add:900:d513:2c97:e2fe:dba9
          13.113.218.131
          52.197.145.144
          54.64.239.23
```
