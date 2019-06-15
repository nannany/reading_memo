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
Bearer Tokenは署名なしトークンといわれ、
RFC6750では、
* Authorizationリクエストヘッダフィールド
* Formエンコードされたボディパラメータ
* URIクエリパラメータ
のいずれかでリソースサーバに対してBearer Tokenを送信する方法が載っています。
ここでは1つ目のAuthorizationリクエストヘッダフィールド


### JWT

アクセストークンにはJWTを使用します。

#### RFC7519

[RFC7519](https://openid-foundation-japan.github.io/draft-ietf-oauth-json-web-token-11.ja.html) 
