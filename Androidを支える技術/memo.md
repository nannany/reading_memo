# 20210314

## androidのセキュリティについて

* デバイスを特定するのに一番いい方法はなにか？
  * random guid generated at install time 
* sticky broadcast?
  * →とりあえず使うな
* certificate pinning?
  * →クライアントで許容するTLS証明書をあらかじめ規定しておく

## JavaScriptのセキュリティについて

* strict modeを確実に効かせるためには、IIFEを使う
* document.domainは使うな
  * `window.postMessage`なるものがあるのでそれを使う
    
