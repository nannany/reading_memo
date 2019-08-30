# 概要

RESTful APIにおいて、更新時に

# 楽観ロックの実装方法について

[ZalandoのRESTful APIに関するガイド](https://restful-api-guidelines-ja.netlify.com/#optimistic-locking)では、楽観ロックの実現方法について、以下の4つが紹介されています。

* If-MatchヘッダとETagヘッダ
* 結果エンティティにおけるETags
* バージョン番号
* Last-Modified / If-Unmodified-Since

API経由で一覧情報を取得し、その中の1件を更新する、というケースでこれら4つがどのように楽観ロックを実現するか見ていきます。

## If-MatchヘッダとETagヘッダ


![If-Match-and-Etag.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/a5fb4b53-953b-c4e0-f7f0-5644976bd166.png)

## 結果エンティティにおけるETags


![結果エンティティにおけるETags.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/549066bb-8dc0-566f-7080-f8ff3e8ae191.png)


## バージョン番号


![バージョン番号.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/349c716d-4d2e-67ae-4dc8-8957bedb706d.png)

## Last-Modified / If-Unmodified-Since


![Last-Modified_If-Unmodified-Since.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/8a44cb1f-8745-06fa-6b0d-2ff794d7800d.png)

# 各手法のPros/Cons

| 楽観ロック実現方法 | メリット | デメリット | 
| :---              | :---    | :---      |
| If-MatchヘッダとETagヘッダ | ・業務オブジェクトに干渉しない | ・リクエスト数が多くなる |
| 結果エンティティにおけるETags | ・更新リクエスト以外の追加リクエストが不要 | ・HTTPヘッダに付与すべき情報が、業務オブジェクトに入り込んでしまう |
| バージョン番号 | ・更新リクエスト以外の追加リクエストが不要 | ・HTTPヘッダに付与すべき情報が、業務オブジェクトに入り込んでしまう |
| Last-Modified / If-Unmodified-Since | ・昔から使用されているので実績がある<br>・業務オブジェクトに干渉しない<br>・実装が容易<br>・更新リクエスト以外の追加リクエストが不要 | ・API側が複数インスタンスから構成されている場合、厳密な時刻同期が必要となる |



# ETagヘッダを利用した楽観ロックの具体例

# Last-Modified / If-Unmodified-Sinceを利用した楽観ロックの具体例

# まとめ

# 参考

[Zalando](https://restful-api-guidelines-ja.netlify.com/#optimistic-locking)
[理系学生日記](https://kiririmode.hatenablog.jp/entry/20180917/1537148448)
[RFC7232](https://tools.ietf.org/html/rfc7232)