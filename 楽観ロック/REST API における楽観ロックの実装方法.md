# 概要

RESTful APIにおいて、更新時に

# 楽観ロックの実装方法について



## If-MatchヘッダとETagヘッダ

![If-Match-and-Etag.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/a5fb4b53-953b-c4e0-f7f0-5644976bd166.png)

## 結果エンティティにおけるETags

![結果エンティティにおけるETags.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/549066bb-8dc0-566f-7080-f8ff3e8ae191.png)


## バージョン番号

![バージョン番号.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/349c716d-4d2e-67ae-4dc8-8957bedb706d.png)

## Last-Modified / If-Unmodified-Since

![Last-Modified_If-Unmodified-Since.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/441085/8a44cb1f-8745-06fa-6b0d-2ff794d7800d.png)

# 各手法のPros/Cons

# ETagヘッダを利用した楽観ロックの具体例

# まとめ

# 参考

(Zalando)[https://restful-api-guidelines-ja.netlify.com/#optimistic-locking]
(理系学生日記)[https://kiririmode.hatenablog.jp/entry/20180917/1537148448]
(RFC7232)[https://tools.ietf.org/html/rfc7232]