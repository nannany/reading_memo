# Java Silver
Java SE 8 Programmer I を受けるにあたって得た知識を残す。
勉強に使用した本は「徹底攻略Java SE 8 Silver問題集［1Z0-808］対応」
https://www.amazon.co.jp/dp/B01ASGJYIE/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1
であったので、それに沿った構成で書いていく。

# 1. Javaの基本
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

# 2. Javaのデータ型の操作
* 数値を2進数、8進数、16進数のリテラルで表す場合、それぞれ先頭、0b、0、0xで始める。
* 整数リテラル表記`_` についての注意点は以下。
 * リテラルの先頭と末尾には記述できない
 * 記号の前後には記述できない**8進の先頭の`0` は記号にならないらしい。。**
 * プリミティブ型の変数に`null`は代入できない。`null`は、変数が何も参照しないことを表すデータであるため。
 * 識別子(メソッド、クラスなどを一意に識別するためのもの)に使える記号は、`_`と`通貨記号`。また、識別子の先頭は数字にしてはいけない。

# 3. 演算子と判定構造の使用
* 大きな範囲の値を小さな変数に代入するときは明示的なキャストが必要。
 * byte:8bit：-128~127
 * char:16bit：0~65535
 * short:16bit:-32768~32767
 * int:32bit:-2147483648~2147483647
 * long:64bit:-9223372036854775808~9223372036854775807
* 桁あふれを以下で試した。

```
package tryAny;

import java.nio.ByteBuffer;

public class Cast {
    public static void main(String[] args) {
	// short桁あふれ
	long a = 32768;
	int b = (int) a;
	short c = (short) b;
	byte[] byteShort = ByteBuffer.allocate(2).putShort(c).array();
	System.out.println("shortの桁あふれ");
	for (byte b1 : byteShort) {
	    System.out.printf("%x ", b1);
	}
	System.out.println();
	System.out.println("32768の時のint　" + b);
	System.out.println("32768の時のshort　" + c);

	// int桁あふれ
	long aa = 2147483648L;
	int bb = (int) aa;
	short cc = (short) bb;
	byte[] byteInt = ByteBuffer.allocate(4).putInt(bb).array();
	System.out.println("int,shortの桁あふれ");
	for (byte b2 : byteInt) {
	    System.out.printf("%x ", b2);
	}
	System.out.println();
	System.out.println("2147483648の時のint　" + bb);
	System.out.println("2147483648の時のshort　" + cc);
    }
}
```

標準出力
```
shortの桁あふれ
80 0 
32768の時のint　32768
32768の時のshort　-32768
int,shortの桁あふれ
80 0 0 0 
2147483648の時のint　-2147483648
2147483648の時のshort　0
```

* `int a = 1+1L;`のように、intで表現できる範囲を超えてなくても、`int a = 1+(int)1L;`とキャストが必要。
* 関係演算子`<` `<=` `>` `>=` は数値以外の比較はできない。`true<false` とかできそうだけどできない。
* 
