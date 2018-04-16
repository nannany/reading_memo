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
* 
