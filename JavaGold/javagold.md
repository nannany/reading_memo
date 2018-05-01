# 1章 Javaのクラス設計

* equalsメソッドはデフォでは以下のよう。
```java
    public static boolean equals(Object a, Object b) {
        return (a == b) || (a != null && a.equals(b));
    }
```

* ObjectsのhashCodeメソッドは、検索パフォーマンスの向上のためにある。
* セマンティクスとは何か？
* final 修飾子の持つ意味はクラス、変数、メソッドで異なる
  * クラス：継承不可
  * 変数：再代入不可。つまり定数
  * メソッド：オーバーライド不可

* **引数にfinalつけることができる** （知らなかった。。）
* static Initializer内のコードはクラスロード時に実行される
* Singletonなクラスの特徴
  * private static フィールドで自身のインスタンスを生成
  * コンストラクタをprivateで宣言
  * フィールドにセットしてあるインスタンスを返すメソッドをpublic staticで用意する
* 不変クラス＝immutable class
* ひし形継承について。インターフェースの多重継承によって、メソッドがかぶってしまった場合、距離が同じ場合はコンパイルエラーとなるが、一番距離が近いものが一意に決まるならば、その一番近いものが採用される。

```java
package tryAny.diamondExtends;

public interface A {
    default void x() {
	System.out.println("I am A.");
    }
}
```
```java
package tryAny.diamondExtends;

public interface B extends A {

}
```
```java
package tryAny.diamondExtends;

public interface C extends A {
    default void x() {
	System.out.println("I am C.");
    }
}
```
```java
package tryAny.diamondExtends;

public class DiamondExtends implements B, C {
    public static void main(String[] args) {
	DiamondExtends de = new DiamondExtends();
	de.x();// I am C.を出力
    }
}
```

* 入れ子クラスというものがある。（これとの対比で、普通のクラスのことをトップレベルクラスという）
  * staticメンバークラス、内部クラス
  * 外側のクラスのことをエンクロージングクラスという。エンクロージングクラスは必ずしもトップレベルクラスではない。

* 入れ子クラスの使い道は、パーフェクトJavaによると以下のよう
  * エンクロージングクラス内部だけでオブジェクトを使う場合
  * ネストしたクラスの実装をエンクロージングクラス内に隠ぺいしたい場合

```java
package tryAny.inner;

public class InnerTest {
    class InnerA {
	void innerMethod() {
	    System.out.println("I am inner.");
	}
    }

    private void execInner() {
	InnerA ia = new InnerA();
	ia.innerMethod();
    }

    public static void main(String[] args) {
	InnerTest it = new InnerTest();
	it.execInner();
    }
}
```

```java
package tryAny.inner;

public class Other {
    public static void main(String[] args) {
	InnerTest.InnerA ia = new InnerTest().new InnerA();
	ia.innerMethod();
    }
}
```

* 匿名クラスが使われる場面は、**インターフェース型の引数をとるように宣言された、他のクラスのメソッドを利用する**場合が多い

```java
package tryAny.anonymous;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class AnonymousTest {
    public static void main(String[] args) {
	Data d1 = new Data(3, "aaa");
	Data d2 = new Data(1, "bbb");
	Data d3 = new Data(2, "ccc");

	List<Data> list = new ArrayList<Data>();
	list.add(d1);
	list.add(d2);
	list.add(d3);

	list.stream().forEach(System.out::println);// 3,1,2の順で表示

	list.sort(new Comparator<Data>() {
	    public int compare(Data data1, Data data2) {
		if (data1.num > data2.num) {
		    return 1;
		} else {
		    return -1;
		}
	    }
	});

	list.stream().forEach(System.out::println);// 1,2,3の順で表示
    }

    static class Data {
	int num;
	String value;

	Data(int num, String value) {
	    this.num = num;
	    this.value = value;
	}

	@Override
	public String toString() {
	    return num + ":" + value;
	}
    }
}
```

* Enumは他のクラスを継承することはできないが、インターフェースを実装することはできる
* name(),toString()で列挙定数名と同じ文字列がとれる。
* values()でEnumの配列が取れる。

```java
package tryAny.enumTes;

public enum Gender {
    MAN, WOMAN, OTHER;
}

class Try {
    public static void main(String[] args) {
	System.out.println(Gender.MAN.toString());// MAN
	System.out.println(Gender.MAN.name());// MAN
	for (Gender g : Gender.values()) {
	    System.out.println(g.name() + ":" + g.ordinal());
	    /**
	     * MAN:0 </br>
	     * WOMAN:1 </br>
	     * OTHER:2
	     */
	}
	Gender g = Gender.MAN;

	trans(g);//男
    }

    public static void trans(Gender g) {
	switch (g) {
	case MAN:
	    System.out.println("男");
	    break;
	case WOMAN:
	    System.out.println("女");
	    break;
	case OTHER:
	    System.out.println("その他");
	    break;
	default:
	    assert (false);
	}
    }
}
```

* Enumはprivateコンストラクタしか宣言できない。

# 2章 コレクションとジェネリクス
* 型変数の命名指針
  * コレクションに格納される要素は**E**
  * マップに格納されるキーと値はそれぞれ、**K**と**V**
  * 上記以外の一般的な型は**T**
  * 戻り値用の型には**R**

* 型引数にプリミティブ型は指定できない
* 変数宣言、インスタンス生成の型引数を一致させなければならない。そのため、JavaSE7より、以下のようにインスタンス生成における型引数の省略ができるようなった。

```java
Foo<Integer> foo = new Foo<>();
```

* ジェネリッククラスは内部的には型変数の部分をObjectに置き換えたクラスが1つ生成されるのみ。そのため、型変数をクラスフィールドにはできないし、クラスメソッドの戻り値や引数にすることはできない。（いまいちこのロジックを理解しきれていない）


```java
package tryAny.Generic;

public class GenericTest<T> {
    /**
     * クラス宣言時のTと下のメソッドでのTは別物なのでこれはコンパイルできる。
     */
    static <T> T exec3(T t) {
	return t;
    }

    /** 以下はコンパイル通らない
    static T exec(T t) {
	return t;
    }
    **/
}
```

* 型境界なる制約を用いて、型変数に制限を加えることができる。

```java
// TはNumberのサブタイプに限定される。
class Foo<T extends Number> {}
```

```java
package tryAny.Generic;

public class BoundedType {
    public static void main(String[] args) {
	Hoge<Foo, Bar> h1 = new Hoge<Foo, Bar>();// コンパイル通る
	Hoge<Foo, Foo> h2 = new Hoge<Foo, Foo>();// コンパイル通る
	// Hoge<Bar, Foo> h3 = new Hoge<Bar, Foo>();//コンパイル通らない
    }
}

abstract class Foo {
}

class Bar extends Foo {
}

class Hoge<T, U extends T> {
}
```

* 型引数にはワイルドカード **?** が使える。
  * <? extends T\>:Tのサブクラス、またはT
  * <? super T>:Tのスーパークラス、またはT

* ジェネリッククラスを継承する場合、型変数が定まるようにせねばならない。

* ArrayListとLinkedListの比較
  * ArrayListは要素に対するランダムアクセスが早いが、リストへの要素の追加のコストは高い
  * LinkedListはランダムアクセスはArrayListより遅いが、要素の追加コストは低い

* TreeSetに格納される要素がComparable<T>型でない場合はClassCastExceptionがスローされる。

# 3章 ラムダ式と組み込み関数型インターフェース
* ラムダ式→匿名内部クラスの実装を簡潔に記述できる

```java
package tryAny.lambda;

public class LambdaTest {
    public static void main(String[] args) {
	Runnable r1 = new Runnable() {
	    public void run() {
		System.out.println("run1");
	    }
	};

	// 同じ
	Runnable r2 = () -> System.out.println("run2");

	Thread t1 = new Thread(r1);
	Thread t2 = new Thread(r2);
	t1.start();
	t2.start();
    }
}
```

* 第1級オブジェクト→リテラルと同様に扱うことができるオブジェクト
* 高階関数→関数の引数に関数を渡すことができ、関数の戻り値として関数を戻すこと、ができる関数
* ラムダ式では常に引数の型を省略できる。また、引数が1つだけの場合は()を省略できる。()を省略する場合は引数の型を記述できない。
* あらかじめ用意されている関数型インターフェースで代表的なのは以下の4つ
  * Supplier< T > : 引数を受け取らず、T型の値を返す。T get()メソッド
  * Predicate< T > : 引数として受け取ったT型の値を評価する。boolean test(T t)メソッド
  * Consumer< T > : 引数としてT型を受け取り、処理を実行する（戻り値なし）。void accept(T t)
  * Function< T,R > : 引数としてT型を受け取り、処理を実行し、R型の値返す。R apply(T t)

```java
package tryAny.lambda;

import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class LambdaTest2 {
    public static void main(String[] args) {
	Supplier<String> s = () -> "supplier";
	Predicate<String> p = str -> "supplier".equals(str);
	Consumer<String> c = str -> System.out.println(str);
	Function<String, Integer> f = str -> str.length();

	// "supplier" の文字数だす。
	if (p.test(s.get())) {
	    c.accept(f.apply(s.get()).toString());
	}
    }
}
```

* UnaryOperator<T> は、引数、戻り値ともにT型になる。つまり、Function<T,T>と考えられる。
* BinaryOperator<T>は上と同様に、BiFunction<T,T,T>とおなじ。

* メソッド参照→ラムダ式が何らかのメソッド呼び出しのみで完結し、SAMの抽象メソッドと、ラムダ式で呼び出しているメソッドのシグニチャが同一の場合に使える構文。

# 4章 Stream API
* StreamAPIのStreamはInputStreamやOutputStreamとは別の概念。
* 終端操作の実行時に中間操作が実行される。（**遅延評価**）
* 同一ストリームに対して、終端操作は一回しかできない。
* Arrays.stream(配列)でストリームを返す。

```java
package tryAny.stream;

import java.util.Arrays;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class StreamTest1 {
    public static void main(String[] args) {
	String[] strAry = { "a", "b", "c" };
	Stream<String> strStream = Arrays.stream(strAry);
	strStream.forEach(System.out::println);

	int[] intAry = { 1, 2, 3, 4, 5 };
	IntStream intStream = Arrays.stream(intAry);
	intStream.forEach(System.out::println);

	IntStream intStream2 = Arrays.stream(intAry, 2, 4);
	intStream2.forEach(System.out::println);
	/**
	 * 3</br>
	 * 4
	 */

	IntStream.range(0, 4).forEach(System.out::print);// 0123
	IntStream.rangeClosed(0, 4).forEach(System.out::print);// 01234

    }
}
```

* 任意の参照型オブジェクトのストリームを作るには、Stream.of()を使う。

```java
package tryAny.stream;

import java.util.stream.Stream;

public class StreamTest2 {
    public static void main(String[] args) {

	Stream<Data> s = Stream.of(new StreamTest2().new Data("a", 1), new StreamTest2().new Data("b", 2));
	// "a:1 b:2 "

	s.forEach(System.out::print);
    }

    class Data {
	String str;
	int i;

	public Data(String s, int i) {
	    this.str = s;
	    this.i = i;
	}

	@Override
	public String toString() {
	    return this.str + ":" + this.i + "  ";
	}
    }
}
```

* BufferedReaderのlinesメソッドとFilesクラスのlinesメソッドはストリームを返す。

```java
package tryAny.stream;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class StreamTest3 {
    public static void main(String[] args) {
	try (BufferedReader br = new BufferedReader(new FileReader("src/main/java/tryAny/stream/sample.txt"))) {
	    br.lines().forEach(System.out::println);

	    Files.lines(Paths.get("src/main/java/tryAny/stream/sample.txt")).forEach(System.out::println);
	} catch (IOException e) {
	    e.printStackTrace();
	}

    }
}
```

* flatMapを用いることで入れ子になったListを平たんにすることができる。
* distinct()で重複を削除できる。

```java
package tryAny.stream;

import java.util.Arrays;
import java.util.List;

public class StreamTest5 {
    public static void main(String[] args) {
	List<List<String>> l = Arrays.asList(Arrays.asList("banana", "apple"), Arrays.asList("banana", "orange"));

	l.stream().flatMap(li -> li.stream()).distinct().forEach(System.out::println);

	List<List<List<String>>> l2 = Arrays.asList(Arrays.asList(Arrays.asList("pineapple", "grape")));

	l2.stream().flatMap(li2 -> li2.stream()).flatMap(li3 -> li3.stream()).forEach(System.out::println);
    }
}
```

* Mapのmerge(K key, V value, BiFunction remappingFunction)では、keyが存在した場合には、valueを用いてremappingFunctionを行った結果が、keyに対応する値となる。keyが存在しない場合には、valueがそのままkeyの値になる。

```java
package tryAny.stream;

import java.util.HashMap;
import java.util.Map;

public class StreamTest6 {
    public static void main(String[] args) {
	Map<String, Integer> m = new HashMap<>();
	m.put("A", 1);
	m.merge("A", 2, (v1, v2) -> v1 * v2);
	m.merge("b", 1, (v1, v2) -> v1 * v2);

	System.out.println(m);
	// {A=2, b=1}

    }
}
```

* データの集合を1つに要約するような終端処理をリダクションと呼ぶ。
* Collectorインターフェースを実装したものをコレクタと呼ぶ。これは、どのような可変コンテナにどのような要素を収集するかを決めている。可変リダクション操作は以下の4つ。
  * 前処理
  * 蓄積
  * 結合
  * 後処理
* java.util.stream.Collectionsユーティリティを利用して、Collectorオブジェクトを生成することができる。

```java
package tryAny.stream;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StreamTest8 {
    public static void main(String[] args) {
	/**
	 * Collectors.toList()で生成されるCollectorオブジェクトは</br>
	 * 入力要素をListに蓄積する。
	 */
	List<String> l = Stream.of("paper", "book", "photo").collect(Collectors.toList());

	l.stream().forEach(System.out::println);

	// Collector<Integer,Map<String,Integer>,Map<String,List<Integer>>>
	// collector
	// = Collectors.groupingBy(Integer;]

	// 文字数毎にグルーピングする
	Map<Integer, List<String>> map = l.stream().collect(Collectors.groupingBy(e -> e.length()));
	map.forEach((v1, v2) -> System.out.println(v1 + ":" + v2));
	/**
	 * 4:[book]</br>
	 * 5:[paper, photo]
	 */

	// 頭文字後にグルーピングする
	Map<Character, List<String>> map2 = l.stream().collect(Collectors.groupingBy(e -> e.charAt(0)));
	map2.forEach((v1, v2) -> System.out.println(v1 + ":" + v2));
    }
}
```

# 5章 例外とアサーション
* catchした例外は、再スローする例外に格納することができる。
* 格納した例外はgetCause()で取得することができる。

```java
package tryAny.exception;

public class ExceptionTest1 {
    public static void main(String[] args) {
	try {
	    x();
	} catch (Throwable e) {
	    while (e != null) {
		System.out.println(e.getMessage());
		e = e.getCause();
	    }
	    /**
	     * from x</br>
	     * from y</br>
	     * from z
	     */
	}
    }

    static void x() throws Exception {
	try {
	    y();
	} catch (Exception e) {
	    throw new Exception("from x", e);
	}
    }

    static void y() throws Exception {
	try {
	    z();
	} catch (Exception e) {
	    throw new Exception("from y", e);
	}
    }

    static void z() throws Exception {
	throw new Exception("from z");
    }
}
```

* 複数の例外を1つのcatch節でとらえるときは、multi-catch文が使える。

```java
package tryAny.exception;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ExceptionTest2 {
    public static void main(String[] args) {
	try {
	    BufferedReader br = new BufferedReader(new FileReader("src/main/java/tryAny/stream/sample.txt"));
	    int a = Integer.parseInt("a");
	} catch (IOException | NumberFormatException e) {
	    System.out.println(e);
	}
    }
}
```

* 