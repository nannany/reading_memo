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

# 20210321 

### XSS

XSSを防ぐためには、データフローを理解することが大切。

マクドナルドでもXSSの脆弱性を突かれたらしい。  
https://tij.me/blog/stealing-passwords-from-mcdonalds-users/#void


# 20210328

* デスクトップアプリをモバイルに移植するとなった場合に考慮するべきことは、画面サイズ以外にもいろいろある。
  * 回線の問題。モバイルは極端に遅くなったり、つながらなくなったりすることがよくある。その問題への対応
  * モバイルを紛失した場合にデータを守れるか

## iOS

* iOSアプリにおいて、ユーザーが意識せずともなされているセキュリティ対策がある
  * DEP(Data execution prevention)
    * メモリの上書を防いでくれる
  * ASLR(Address space layout randomization)
    * メモリ位置のランダム化を図ってくれる
  * Stack canaries
    * バッファオーバーフローの検出
* mach-Oファイル？
* apns? ats? ipc?

