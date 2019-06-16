# Cognitoを使用した認証・認可について

## Cognitoの概要

大きな機能のとしては2つあり、ユーザープールとIDプールがあります。
この2つは別々に使うこともできるし、一緒に使うこともできます。
ユーザープールでは認証ができ、IDプールでは認可ができます。

### 認証・認可

認証(Authentication:AuthN)は通信相手を確認する行為を指します。

認可(Authorization:AuthZ)はリソースへのアクセス権限を与える行為を指します。



## Cognitoを利用した認証

## Cognitoを利用した認可

### Bearer Token

アクセストークンにはBearer Tokenを使用します。
Bearer Tokenについては、[RFC6750](https://openid-foundation-japan.github.io/rfc6750.ja.html) で定義されています。  
Bearer Tokenという言葉はRFC6750においては以下のように定義されています。
```
署名なしトークン (Bearer Token)
セキュリティトークン. トークンを所有する任意のパーティ (持参人 = bearer) は, 「トークンを所有している」という条件を満たしさえすればそのトークンを利用することができる. 署名無しトークンを利用する際, 持参人は, 暗号鍵の所持を証明 (proof-of-posession) するよう要求されない.
```

若干ピンと来なかったので、bearerという言葉の意味は英和辞典で調べると
```
運ぶ人、運搬人、かごかき、(小切手・手形の)持参人、(手紙の)使者、実のなる草木
```

といった意味があるそうです。
英英でも調べてみると、
```
someone who brings you information, a letter etc
```

という意味があるそうです。
つまり、bearerという単語の意味としては、何かを持ってきたその人本人、という意味があるようです。
認可の文脈では、Bearer Tokenを持って通信してきたその人に権限を与えるという意味になるのだと思います。

RFC6750では、以下の3つがBearer Tokenをリソースサーバへ送信する方法として定義されています。
* Authorizationリクエストヘッダフィールド
* Formエンコードされたボディパラメータ
* URIクエリパラメータ
ここでは1つ目のAuthorizationリクエストヘッダフィールドに含める方法


### JWT

アクセストークンにはJWTを使用します。

#### RFC7519

[RFC7519](https://openid-foundation-japan.github.io/draft-ietf-oauth-json-web-token-11.ja.html) 

---
### JWS
OpenId Connect において発行されるIDトークンの1形式としてJWSがあります。

JWSは`ヘッダー.ペイロード.署名`という形式からなります。
JWEは`ヘッダー.キー.初期ベクター.暗号文.認証タグ`という形式からなります。この形式はIDトークンを暗号化したいときに用いられます。

JWTとは、「JSON 形式で表現されたクレーム (claim) の集合を、JWS もしくは JWE に埋め込んだもの」である。
IDトークンはJWT形式で表現されます。つまり、IDトークンはJWTの一種といえます。

IDトークンの仕様では必須のクレームが複数あり、`iss`、`sub`、`aud`、`exp`、`iat`の5つは必須のクレームとされています。

#### issクレーム
iss(issuer)クレームはJWTの発行者を識別するための識別子です。

#### subクレーム
sub(subject)クレームはユーザーの一意識別子となります。

#### audクレーム
aud(audience)クレームは発行されたJWTが誰に対して発行されたのかを示すものとなります。

#### expクレーム
exp(expiration time)クレームはJWTの有効期限を示しています。

#### iatクレーム
iat(issued at)クレームはJWTが発行された日時を示しています。

---

### Cognitoにユーザーを作成
以下のようなコマンドを実行してCognitoにユーザーを登録することができます。
```
aws cognito-idp sign-up --client-id xxxxxxxxxxxxx --username nannany --password xxxxxxxxx
aws cognito-idp admin-confirm-sign-up --user-pool-id ap-northeast-1_xxxxxxxx --username nannany
```