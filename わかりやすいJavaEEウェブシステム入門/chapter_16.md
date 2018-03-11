# マッピングアノテーション
* コンストラクタ→インジェクション→PostConstructの順で処理が行われる。
* @SecondaryTables と @SecondaryTable を用いることで、複数テーブルのカラムを1つのentityに含めることができる。
* @Embedded と @Embeddable でEntityに他のクラスを組み込むことができる。
* 複合キークラスでは、equalsメソッドとhashCodeメソッドをoverrideする必要がある。
Objects.equals(~~,~~)とか使う。
以下 Objects.javaの実装。

```
    public static boolean equals(Object a, Object b) {
        return (a == b) || (a != null && a.equals(b));
    }
```

```
    public static int hashCode(Object o) {
        return o != null ? o.hashCode() : 0;
    }
```

* @Basic(fatch=FetchType.LAZY)で遅延フェッチできる。
* DateやCalenderには必ず @Temporal をつける。
* @Transcient をつけると、DBに保存しないようになる。
* 