https://chatgpt.com/c/68b989f2-3fc8-8331-b190-488bb44cde39

ログイン画面が提供されていて、username/passwordを入れるのだが、passwordが誤っている場合にどれだけの文字があっているかを出してくれるサイトになっている。

adminがユーザーネームであると仮定して、curlを打ちまくって狭めていけばできそうな気がする。

下記のようなcurlでパスワードが何文字合ってるかの文言が含まれるレスポンスが返ってくるのを確認した。

```shell
curl -sS -L \
  -b 'PHPSESSID=7b598ad71b99eb80708d4cdec7c2437f; webpy_session_id=2f8752c17fb5b63ae949a6e94e3f13b7756d3cd6' \
  -e 'http://52.59.124.14:5015/index.php' \
  --data-urlencode 'username=admin' \
  --data-urlencode 'password=a' \
  'http://52.59.124.14:5015/login.php'
```

これを繰り返してやっていけばadminでログインできてflagが取れる。

(adminというユーザーネームできめうちでいいんか、、と思ったがそれは良かったらしい。)

