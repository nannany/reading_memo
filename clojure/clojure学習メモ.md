# プログラミングclojure

* defnは関数を定義する。

```clojure
(defn hello [name] (str "hello, " name))
```

* *1でひとつ前の結果
* *e で最後に出た例外
* use をうまく使えない..
* find-reduceでドキュメントを探せる。

# 2章 Clojureひとめぐり

* フォームとは？
  * シンボルとキーワードは異なるものである。

* リーダマクロとは？
  * clojureではリーダマクロを定義することはできない。

* 関数とは？
  * 

* 無名関数とは？

* 束縛と名前空間

* フロー制御
  * if は最初の引数を評価し、trueなら2つ目の、falseなら3つ目の引数を評価したものが返る。
```clojure
(defn is-small? [number]
  (if (< number 100) "yes" "no"))
```
  * 副作用ってどういうこと？