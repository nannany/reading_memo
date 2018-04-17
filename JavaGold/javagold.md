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


