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

2. 