* Cognitoで認証処理をやらせたいのだが、ユーザーの登録はどうやってやればよいのか？
  * ユーザーは名前とパスワードを持つイメージなのだが、どこで登録できるのか。。。 → cognitoのホストしているUIからできるし、コマンドからもできる
* Cognitoのライブラリを使用した場合はどのようにしてCognitoまで情報を送るのだろうか 
  * もし、実態はcurlだとしたら、https通信が発生するはずなので、Cognitoに証明書を持たせなければならない。  → 実態はhttpsっぽい。証明書系の話はよく分からん
  * awscliによる通信だとしたら、credentialをクライアントアプリケーションで持たなければならないのでは。
* cognitoでいうところの、アプリクライアントとはいったい → RFC6749でいうところのClient
* RFC6749のUser-Agent はだいたいブラウザの理解でOK？ → たぶんおけー

* 

# Spring Securityとcognito

https://www.baeldung.com/spring-security-oauth-cognito


# cognitoのログインページ


