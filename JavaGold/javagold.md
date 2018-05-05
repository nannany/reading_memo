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

* try-with-resources文を用いることでオープンしたリソースを自動的にクローズすることができる。

```java
package tryAny.exception;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class ExceptionTest3 {
    public static void main(String[] args) {
	try (FileReader in = new FileReader("src/main/java/tryAny/stream/sample.txt");
		FileWriter out = new FileWriter("src/main/java/tryAny/exception/sample.txt");
		AutoCloseTest act = new AutoCloseTest();
		/** AutoCloseTest2 act2 = new AutoCloseTest2(); ←AutoClosableを実装していないのでダメ**/ ) {
	    // AutoCloseTest のcloseが実行される。
	} catch (IOException e) {

	}
    }
}

class AutoCloseTest implements AutoCloseable {
    @Override
    public void close() {
	System.out.println("AutoCloseTest is closed.");
    }
}

class AutoCloseTest2 {
    public void close() {
	System.out.println("AutoCloseTest is closed.");
    }
}
```

* assert文がfalseになると、AssertionErrorが発生する（コマンドライン引数に-eaを入れておく）。
* assert文は開発中のプログラムのための機能であり、実運用時は無効にすべきもの。

```java
package tryAny.exception;

public class ExceptionTest4 {
    public static void main(String[] args) {
	int x = 1;

	assert (x == 2) : "Error Message出すで！";
	/**
	 * VM引数に-eaを入れてやると、以下のエラーが出る。
	 *
	 * Exception in thread "main" java.lang.AssertionError: Error Message出すで！
	 * at tryAny.exception.ExceptionTest4.main(ExceptionTest4.java:7)
	 *
	 */
    }
}
```

# 6章 日付/時刻API
* now()メソッドで現在時が、ofメソッドで指定した時間を保持するクラスが取れる。

```java
package tryAny.dateTime;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.Month;

public class DateTest1 {
    public static void main(String[] args) {
	LocalDateTime now = LocalDateTime.now();
	LocalDate ld = LocalDate.of(2018, Month.JANUARY, 1);

	System.out.println(now + " " + ld);
    }
}
```

* TemporalUnitクラスのメソッドで、簡単な日付計算を施して、Temporalを実装したクラスや期間の長さを計算することができる。

```java
package tryAny.dateTime;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class DateTest2 {
    public static void main(String[] args) {
	LocalDate ld1 = LocalDate.now();
	LocalDate ld2 = ChronoUnit.YEARS.addTo(ld1, -1);
	long l = ChronoUnit.DAYS.between(ld1, ld2);

	System.out.println(ld1);// 今
	System.out.println(ld2);// 今から一年前
	System.out.println(l);// 閏年等考慮しなければ-365
    }
}
```

* 期間を表すクラスとして、DurationクラスとPeriodクラスがある。どちらもTemporalAmountインタフェースを実装している。
  * Durationは時間ベースの期間を表す。
  * Periodは日付ベースの期間を表す。

```java
package tryAny.dateTime;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.Period;
import java.time.temporal.ChronoUnit;

public class DateTest3 {
    public static void main(String[] args) {
	LocalDateTime ldt1 = LocalDateTime.now();
	LocalDateTime ldt2 = ChronoUnit.DAYS.addTo(ldt1, 31);

	Duration d = Duration.between(ldt1, ldt2);
	Period p = Period.between(ldt1.toLocalDate(), ldt2.toLocalDate());

	System.out.println(d + " " + p);// PT744H P1M
    }
}
```

* 日付、時刻の表示形式は定義済みのものを使うことも、自分で作成することもできる。

```java
package tryAny.dateTime;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;

public class DateTest4 {
    public static void main(String[] args) {
	DateTimeFormatter dtf1 = DateTimeFormatter.BASIC_ISO_DATE;
	DateTimeFormatter dtf2 = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM);

	System.out.println(dtf1.format(LocalDate.now()));
	System.out.println(dtf2.format(LocalDateTime.now()));

	// オリジナルなフォーマットを作成
	DateTimeFormatter dtf3 = DateTimeFormatter.ofPattern("yyyy★MM★dd");
	System.out.println(dtf3.format(LocalDate.now()));
    }
}
```

# 7章 Java/IO
* ファイルを扱うクラスとして、FileとPathがあるが、JavaSE7以降ではPathの使用が推奨されている。
* 入出力の流れは、入力or出力、テキストorバイナリ、を掛け合わせた4通りがあり、それぞれ以下のような抽象クラスがある。
  * 入力、テキスト：Reader
  * 入力、バイナリ：InputStream
  * 出力、テキスト：Writer
  * 出力、バイナリ：OutputStream
* java.ioパッケージ内のクラス設計は、Decoratorパターンで作りこまれている。
* PrintStreamとPrintWriterはほとんど一緒。これらはプリミティブ型の値をそのまま出力できるようになっている。

```java
package tryAny.io;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class IOTest1 {
    public static void main(String[] args) {
	try (PrintWriter pw = new PrintWriter("out.txt")) {
	    pw.println("Hello world");
	    // BufferedWriterではboolean、doubleといったプリミティブ型をそのまま出力させることはできない。
	    pw.println(true);
	    pw.println(0.4);
	} catch (FileNotFoundException e) {
	    System.out.println(e);
	}
    }
}
```

* Consoleクラスを用いることで標準入力の読み込みができる。Consoleインスタンスを取得するには、Systemクラスのconsole()メソッドを呼ぶ必要がある。
* 直列化が必要であるクラスはSerializableを実装している必要がある。Serializableインターフェース自体は何の機能もなく、これを実装したクラスは直列化が可能である、という責任を負うという理解。
<http://d.hatena.ne.jp/daisuke-m/20100414/1271228333>
* ObjectOutputStreamクラス、ObjectInputStreamクラスを用いて実際にシリアライズ、デシリアライズを行うことができる。

```java
package tryAny.io;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class IOTest3 {
    public static void main(String[] args) throws IOException {
	// シリアライズしたデータを格納。
	try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("iotest3.ser"))) {
	    String test = "iotest3";
	    oos.writeObject(test);// これでiotest3.serができる。
	    oos.writeInt(111);
	} catch (IOException e) {
	    throw new IOException(e);
	}

	// シリアライズしたデータを取得してメモリに展開。
	try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("iotest3.ser"))) {
	    System.out.println(ois.readObject());
	    System.out.println(ois.readInt());
	} catch (ClassNotFoundException | IOException e) {
	    throw new IOException(e);
	}
    }
}
```

* static変数、transient修飾子の付与された変数はシリアライズ対象外となる。

* JavaSE7でファイルを扱うクラスがFileからPathになったことにより、プラットフォームのファイルシステム固有の仕組みを透過的に使用できるようになった。
* Filesクラスのデフォルトの挙動は以下。これらの挙動は引数にオプションを指定することによって変更できる。
  * コピー先ファイルが存在する場合は例外がスローされる。
  * コピー元ファイルの属性は引き継がれない。
  * ディレクトリのコピーの場合、ディレクトリ内のファイルはコピーされない。
  * シンボリックリンクをコピーした場合、リンク先のみコピーされ、リンク自体はコピーされない。
* ファイル属性を扱うクラスはjava.nio.file.attributeパッケージにあり、以下の3つがある。
  * BasicFileAttributes:Windows,Linux問わず共通のファイル属性
  * DosFileAttributes:Windows系のファイル属性
  * PosixFileAttributes:Linux系のファイル属性
* ファイル属性のセットを表すインターフェースとしてAttributeViewがある。（**ファイル属性のセットってどういうこと??**）
* ファイルやディレクトリの単一の属性を得るときは、Files.getAttributeが使える。

```java
package tryAny.io;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.attribute.FileTime;

public class IOTest5 {
    public static void main(String[] args) throws IOException {
	Path p = Paths.get("out.txt");

	// 作成日時
	System.out.println((FileTime) Files.getAttribute(p, "creationTime"));

	// サイズ
	System.out.println((long) Files.getAttribute(p, "size"));

	// シンボリックリンクか否か
	System.out.println((boolean) Files.getAttribute(p, "isSymbolicLink"));
    }
}
```

* walkFileTreeメソッドを使うとディレクトリ階層の再帰的トラバース処理が比較的容易に行える。
* Files.walkメソッドの用いると深さ優先探索でトラバース処理が行える。

```java
package tryAny.io;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

public class IOTest6 {
    public static void main(String[] args) throws IOException {
	Path p = Paths.get("src");

	// ファイルが現れたら標準出力するようにする。
	Files.walkFileTree(p, new SimpleFileVisitor<Path>() {
	    @Override
	    public FileVisitResult visitFile(Path path, BasicFileAttributes bfa) throws IOException {
		System.out.println(path);
		return FileVisitResult.CONTINUE;
	    }
	});

	// ディレクトリのみ出力するようにする。
	Files.walk(p).filter(path -> {
	    try {
		return (boolean) Files.getAttribute(path, "isDirectory");
	    } catch (IOException e) {
		System.out.println(e);
		return false;
	    }
	}).forEach(System.out::println);
    }
}
```

# 8章 並行性
* 並行処理ユーティリティはjava.util.concurrent.atomicとjava.util.concurrent.locksで提供される。ここで提供される仕組み、機能は以下。
  * スレッドプール：あらかじめスレッドを生成してためておくことで、スレッド生成のオーバーヘッドをなくすための仕組み。Executorフレームワークがこの機能を提供
  * 並行コレクション：パフォーマンスと並行性にうまく折り合いをつけたコレクション
  * アトミック変数：処理の原子性を担保してくれる、つまり、とある機能を実行したか、しないかの二択以外の状況はあり得ないことを保障してくれる仕組みを持った変数のこと。インクリメント処理であれば、①値の読み込み→②値変更→③値書き込み、という処理であるが、①～③の流れについて、完了or手つかずのいずれかであるということが保証される。（①と②の間で他の処理が対象の変数に対して書き込みを行う、といったことを考慮している）
  * カウンティング・セマフォ：**セマフォ**とは、プロセスやスレッド間における同期や割込み制御に用いられる仕組みである。セマフォには**バイナリ・セマフォ**と**カウンティング・セマフォ**がある。バイナリ・セマフォはリソースに対するアクセス制御の種類が「可能」「不可能」のみであるのに対し、カウンティング・セマフォはアクセス可能なリソース数を任意に設定することができる。

* アトミック変数を使用するとアトミックな操作が保証される。

```java
package tryAny.concurrentUtility;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrentTest5 {
    public static void main(String[] args) throws InterruptedException, ExecutionException {

	ExecutorService es = Executors.newFixedThreadPool(8);
	MyAtomCounter mac = new MyAtomCounter();

	Future<?> ret1 = es.submit(new MyAtomWorker(mac));
	Future<?> ret2 = es.submit(new MyAtomWorker(mac));

	ret1.get();
	ret2.get();
	es.shutdown();

	// 確実に200000になる。
	mac.show();

    }
}

class MyAtomCounter {
    private AtomicInteger count = new AtomicInteger();

    public void increment() {
	count.incrementAndGet();
    }

    public void show() {
	System.out.println("AtomicIntegerの場合：" + count);
    }
}

class MyAtomWorker implements Runnable {
    private static final int NUM_LOOP = 100000;
    private final MyAtomCounter counter;

    MyAtomWorker(MyAtomCounter counter) {
	this.counter = counter;
    }

    @Override
    public void run() {
	for (int i = 0; i < NUM_LOOP; i++) {
	    counter.increment();
	}
    }
}
```

* **ConcurrentHashMap**クラスはMapがアトミック操作できるようになったもの。ロックする単位はマップ全体ではなくもっと細かいものとなっており、実行性能の劣化は小さいが、size()やisEmpty()が正確でないことがある。また、このクラスが返すIteratorの設計方針は**弱い整合性**であり、並行アクセス時の要素変更を許容しているため、ConcurrentModificationExceptionは発生しない。
* **CopyOnWriteArrayList**クラスは、リストの要素に変更がはいるようなメソッドが呼ばれる際には、元のリストのコピーが生成される。リスト要素変更中にほかのスレッドからリストの読み取り要求が来た場合には、作成したコピーの値を返すため、ConcurrentModificationExceptionは発生しない。コピーを作成するという仕組み上、リストのサイズが大きい場合は性能が悪くなる。
* CyclicBarrierクラスを用いることで複数スレッド間で協調を取ることができる。
* Threadクラスでは「タスクの実行をJVMに依頼する」部分と「タスクをどのように実行するか」という部分が蜜結合となっており、スレッドの生成と管理をプログラムで制御することが難しかった。JavaSE8からはExecutorクラスがそれらの問題を解決する形で登場した。
* Executorフレームワークによって、タスクのライフサイクルの管理、スレッドプール、タスクの遅延開始・周期的実行の機能等が提供されるようになった。
* ScheduledThreadPoolExecutor クラスを使用することで、タスクの遅延開始・周期的実行ができる。

```java
package tryAny.concurrentUtility;

import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

// １秒ごとにランダム値を生成し続ける。
public class ConcurrentTest6 {
    public static void main(String[] args) {
	ScheduledThreadPoolExecutor stpe = new ScheduledThreadPoolExecutor(1);

	ScheduledFuture<?> sf = stpe.scheduleAtFixedRate(new Runnable() {
	    @Override
	    public void run() {
		System.out.println(Math.random());
	    }
	}, 1000, 1000, TimeUnit.MILLISECONDS);

	while (true) {
	    if (sf.isCancelled() || sf.isDone()) {
		stpe.shutdown();
		break;
	    }
	}
    }
}
```

* Executorインターフェース導入の目的は**タスクの実行者**と**タスクの実行方法**の分離であり、タスクの実行者部分はExecutorインターフェースが受け持ち、タスクの実行方法部分はExecutorServiceとScheduledExecutorServiceが受け持つ（Executorを実装した具象クラス）。
* Futureオブジェクトは非同期タスクの実行結果を表すオブジェクト。
* Executorの状態は以下の3つがある。
  * Active：新規タスクの受付可能な状態。
  * ShuttingDown：新規タスクの受付はしないが、キューにたまったタスクの実行を行っている状態。
  * Shutdown：新規タスクの受付はせず、キューにもタスクがない状態。
* **Fork/Joinフレームワーク**なるものを用いて、タスクを細分化し、複数のスレッドで処理を効率的に行うことができる。そこで使用されているアルゴリズムは**Work-stealing**というもの。細分化されて振り分けられたタスクが早めに完了したスレッドは、まだタスクをすべて終えていないスレッドのキューの一番上にあるタスクをぶんどる、というようなアルゴリズム。
* Fork/JoinフレームワークにおけるタスクはForkJoinTask抽象クラスで表され、タスクの実行方法部分はForkJoinPool実装クラスが受け持つ。
* ForkJoinTaskを継承したクラスは**RecursiveAction**クラスと**RecursiveTask**があり、RecursiveActionのほうは戻り値がなく、RecursiveTaskのほうは戻り値がある。
* ForkJoinPoolのタスク実行メソッドは以下の3つ。
  * execute:非同期実行で戻り値なし
  * submit：非同期実行で戻り値あり
  * invoke:同期実行

```java
package tryAny.concurrentUtility;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class ConcurrentTest7 {
    public static void main(String[] args) throws InterruptedException {
	ForkJoinPool jfp = new ForkJoinPool();
	jfp.execute(new MyAction());
	System.out.println("①");
	Thread.sleep(3000);
	System.out.println("②");
	/**
	 * ①</br>
	 * ③</br>
	 * ②
	 */

	jfp.invoke(new MyAction());
	System.out.println("①");
	Thread.sleep(3000);
	System.out.println("②");
	/**
	 * ③</br>
	 * ①</br>
	 * ②
	 */
    }
}

class MyAction extends RecursiveAction {
    @Override
    protected void compute() {
	try {
	    Thread.sleep(2000);
	} catch (InterruptedException e) {
	    e.printStackTrace();
	}

	System.out.println("③");
    }
}
```

# 9章 JDBCによるデータベース・アプリケーション

* 


# 10章 ローカライズ
* java.util.Propertiesで許されているプロパティファイルの形式はテキストファイルかXMLファイル。
* プロパティファイルの読み込みそのものはFileInputSteamをつかい、読み込んだInputStreamをPropertiesオブジェクトのloadメソッドの引数に渡す。

```java
package tryAny.locale;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class LocaleTest1 {
    public static void main(String[] args) {

	try (InputStream is = new FileInputStream("test.properties");
		InputStream is2 = new FileInputStream("test2.properties")) {
	    Properties p = new Properties();
	    p.load(is);
	    p.list(System.out);
	    System.out.println("★" + p.getProperty("fruit") + "★");

	    // ここでのロードは上書きでなく、追記のよう。
	    p.loadFromXML(is2);
	    p.forEach((k, v) -> System.out.println(k + "=" + v));
	    System.out.println("★" + p.getProperty("hoge") + "★");

	    /**
	     * -- listing properties --</br>
	     * fruit=apple</br>
	     * vegitable=carot</br>
	     * ★apple★</br>
	     * vegitable=carot</br>
	     * hoge=ほげ</br>
	     * fuga=ふが</br>
	     * fruit=apple</br>
	     * piyo=ぴよ</br>
	     * ★ほげ★</br>
	     *
	     */
	} catch (IOException e) {
	    e.printStackTrace();
	}
    }
}
```


