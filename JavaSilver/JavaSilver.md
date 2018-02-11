# Java Silver
Java SE 8 Programmer I を受けるにあたって得た知識を残す。
勉強に使用した本は「徹底攻略Java SE 8 Silver問題集［1Z0-808］対応」
https://www.amazon.co.jp/dp/B01ASGJYIE/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1
であったので、それに沿った構成で書いていく。

1. Javaの基本
* クラスは必ず何らかのパッケージに属する。パッケージ宣言をしていない場合は、「無名パッケージ」なるものに属することとなる。
* java.lang パッケージのインポート宣言は省略することができる。
* staticインポートなるものがある。本来staticなフィールド、メソッドは、`クラス名.フィールド`や`クラス名.メソッド`で呼び出す。staticインポートを行えば、クラス内で定義されたフィールド、メソッドかのように扱うことができる。
**これを実際の開発でつかうことってあるのだろうか??**
書き方の注意としては、`static import`ではなく、`import static`の順。


```
package tryAny;

public class staticImport {
    public static int num = 0;

    public static void print() {
	System.out.println(num);
    }
}
```

```
package tryAny.test;

import static tryAny.staticImport.*;

public class Main {
    public static void main(String[] args) {
	num = 13;
	print();
    }
}
```

* 同名のフィールド、メソッドが存在した場合、そのインポートは無視される。

2. Javaのデータ型の操作
* 数値を2進数、8進数、16進数のリテラルで表す場合、それぞれ先頭、0b、0、0xで始める。
* 整数リテラル表記`_` についての注意点は以下。
 * リテラルの先頭と末尾には記述できない
 * 記号の前後には記述できない**8進の先頭の`0` は記号にならないらしい。。**
 * プリミティブ型の変数に`null`は代入できない。`null`は、変数が何も参照しないことを表すデータであるため。
 * 識別子(メソッド、クラスなどを一意に識別するためのもの)に使える記号は、`_`と`通貨記号`。また、識別子の先頭は数字にしてはいけない。
 * 