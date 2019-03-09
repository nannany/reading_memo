# Amazon SESを使用してメールを送信する

https://docs.aws.amazon.com/ja_jp/ses/latest/DeveloperGuide/quick-start.html

## コンソールからメール送ってみる

* SES Management Consoleで送信元となるメールアドレスを登録する。
* 登録方法としては、メールアドレスをコンソール上で入力したら、そのアドレスにメールが送られてきて、そのメールのなかのリンク踏むというよくあるやつ。
* コンソールからメールを送れる。ただし、サンドボックス版においては、登録されたものに対してしか送信することができない。

## AWS SDK for Javaでメール送ってみる

https://docs.aws.amazon.com/ja_jp/ses/latest/DeveloperGuide/send-an-email-using-sdk.html

### 前準備

* とりあえずSDKを[ダウンロード](https://docs.aws.amazon.com/ja_jp/ses/latest/DeveloperGuide/download-aws-sdk.html)。
* awsの認証情報を取得、認証情報の共有ファイルを作成
* EclipseにAWS Toolkit for Eclipseをインストールする。
  * Help→Install new SoftwareのWork withの中に https://aws.amazon.com/eclipse を入れる。あとはぽちぽちやる。
* 
