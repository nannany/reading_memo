# パスキーのすべて

著者: えーじ, 倉林雅, 小岩井航介
リンク: https://www.amazon.co.jp/dp/B0D7RNFQD2
評価: ⭐️⭐️⭐️⭐️⭐️
ステータス: 読了
種別: 書籍
読了日: 2025年3月23日

<aside>
💡 **Notionヒント：**このページにメモやハイライトなどを記録しましょう。`[[` コマンドを使ってほかのNotionページへのリンクを追加することもできます。詳細は[こちら](https://www.notion.so/ja-jp/help/create-links-and-backlinks)。

</aside>

[](https://www.notion.so)

**目次**

## 1章

- １章はこれまでのパスワードの歴史とかをたどり、なぜpasskeyが求められているかを述べている

## 2章

パスキーはデバイス認証の延長線上にある。

デバイス認証との違いは、

- ディスカバラブルである
    - 従来はemailなどを入力したのちに、webauthn apiに対してcredentialIDと公開鍵を渡す、というような流れであったが、これはcredentialIDを渡す必要がない
- クラウド同期がなされる

という点。

パスキーでも解決できないことが書いてある。

- セッションとられる
    - 最近はdbscなる仕組みが策定中らしい。フロー長いな..
    - [https://zenn.dev/maronn/articles/about-dbsc-infomation#dbsc-のフロー](https://zenn.dev/maronn/articles/about-dbsc-infomation#dbsc-%E3%81%AE%E3%83%95%E3%83%AD%E3%83%BC)
- pin見られてデバイス盗まれたら詰む
    - まぁそれはそうだろう
- パスワードマネージャーのログインアカウントが乗っ取られたら？
- パスキーにアクセスできなくなったら？

## 3章passkeyのユーザー体験

### 3.2 既存アカウントへのパスキー登録

- ログイン直後にパスキー登録を促すプロモーションを行う
    - これはそう

- well known url for passkey endpoints
    - これがあれば、passkey providerによってはpasskey登録画面に遷移させてくれる
- Conditional Registration
  - 


### 3.6 パスキーの管理画面

認証のテストボタン、良さげ。自分だったら確認したい

## 4章サポート環境

各ブラウザでの対応状況。実装している時に見たかった

## 5章passkeyのux

### 5.6 再認証uxの実装

**allowCredentials**を使ってやる。

## 6章

getClientCapabilities、というメソッドでブラウザのpasskey関連の機能が使えるか否かを判定できるっぽい

### 6.5

authenticatorSelection.authenticatorAttachment

**allowCredentials**

これを使うと、特定のユーザーのみが対象となってpasskeyログインできる。

何に使うかというと、重要な処理を行う前に再認証を求めるなどをするときに、複数のpasskeyを持っている場合に意図せずアカウントが切り替わってしまう可能性がある。そうならないように、このオプションを使う。

## 7章

mobileにおけるpasskeyの話。ここは一旦飛ばす

## 8章

### 8.2

A well-known URL for Passkey Endpoint

### 8.4 パスキーの表示名変更や削除をパスキープロバイダに通知する

SignalAPIというやつ。

サーバーから削除済みであれば、認証器の方のも消す、ができる

### 8.7

↓otpの話

[https://web.dev/articles/sms-otp-form?hl=ja](https://web.dev/articles/sms-otp-form?hl=ja)

## 9章パスキー周辺のエコシステム

### 9.2パスキーの実装をサポートするエコシステム

下記、passkeyのデモサイト

[https://try-webauthn.appspot.com/](https://try-webauthn.appspot.com/)

実装もある。

[https://github.com/google/webauthndemo](https://github.com/google/webauthndemo)

discord

[https://discord.gg/](https://discord.gg/MvQmq4h6)