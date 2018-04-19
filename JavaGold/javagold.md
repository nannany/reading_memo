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
* 