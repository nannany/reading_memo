# effective java 3rd

# 2章.オブジェクトの生成、削除

# 1.コンストラクタの代わりにstaticなファクトリメソッドの作成を考慮すべし

# 2.コンストラクタの引数が膨大になるときはbuilderを使うべし

* telescoping constructor と JavaBeansパターンなるものと対比させている。
* インスタンス生成において、パラメータが片手で数えられるよりも多くなるような場合にはbuilderパターンでのインスタンス生成を考えたほうが良い。
* JavaBeansパターンとするときの欠点の説明がよく分からなかった。複数回の呼び出しがあるから不整合が起きうる、みたいな話だが具体的にどういうこと？

# 3.シングルトンなクラス設計をするにおいては、コンストラクタをprivateにするか、ENUMを用いる手法とせよ

* ENUM型使ったシングルトンみたことないが。。

# 4.インスタンス化を抑制したいクラスには、privateコンストラクタを作成せよ

* utilityクラス等はインスタンス生成を抑制したいので、その時に使う模様。

# 5.リソースのハードコーディングを行うより、Dependency Injectionを行うべし
* 大きな規模になった場合には、フレームワークのDIの仕組みを使うべき。
* Factoryパターンを使う。
* この項目は第2版にはなかったよう。

# 6.不必要なオブジェクト生成は避けるべし
* defensive copyが必要な場合はその限りでない。defensive copyってなんだ？

# 7.使わなくなった参照は廃棄すべし
* 廃棄しないとメモリリークが起きる。
* キャッシュやコールバックを持つクラスで起こりがちな問題らしい。
* 弱参照？→以下が分かりやすい。弱参照は他からの参照（弱参照以外の参照）がなくなると、GCの対象となる。
<http://www.ne.jp/asahi/hishidama/home/tech/java/weak.html>

# 8.finalizerとcleanerの使用は避けるべし
* これらの短所は、どのように動くかの予想がつきにくいことにある。
* finalizerはパフォーマンスに深刻な悪影響を与える。
* finalizerの使用はセキュリティに悪影響を与える。以下に詳しく乗っていたが、正直よくわからん。。
<https://www.ibm.com/developerworks/jp/java/library/j-fv/index.html>
* これらの使用の代わりに、AutoClosableの実装とtry-with-resourcesを用いていく。

# 9.try-finallyよりもtry-with-resourcesを使うべし
* try-finallyでtry句とfinally句で同時に例外発生した場合、try句のほうがかき消されてしまう。

# 3章.全オブジェクト共通のメソッド



* この章ではObjectsのメソッドオーバーライド方法を中心にまとめられている。







# 10.equalsのoverrideは一般契約（general contracts）に従うべし



* 一般契約とは、反射性（reflexive）,対照性（symmetric）,推移性（transitive）,整合性（consistent）,非 null 性（non-null）のこと。



* googleのAutoValueを使えば、うまくequalsのオーバーライドを行ってくれる。







# 11.equalsをオーバーライドする場合はhashcodeもオーバーライドせよ



* hashCodeの一般契約によると、等しい2つのオブジェクトは等しいhashCodeの値を返さねばならない。よって、equalsをオーバーライドして、論理的に等しいが同じ参照ではない場合も等しいとする場合には、hashCodeをオーバーライドしないままだと異なった値を返すことになってしまう。



* 性能を気にする場合は、hashCodeで計算された値をキャッシュしておく。

# 12.常にtoStringをオーバーライドせよ

* Thread.javaのtoStringは以下のよう。

```java
    public String toString() {
        ThreadGroup group = getThreadGroup();
        if (group != null) {
            return "Thread[" + getName() + "," + getPriority() + "," +
                           group.getName() + "]";
        } else {
            return "Thread[" + getName() + "," + getPriority() + "," +
                            "" + "]";
        }
    }
```

# 13.cloneをオーバーライドするときは注意せよ



* super.cloneを呼んでキャストをする。mutableな変数がある場合はdeepcopyして対応する。



* 大体の場合において、cloneメソッドでオブジェクトのコピーを作るよりも、コンストラクタやファクトリメソッドで作るほうが容易である。唯一、配列のコピーはcloneのほうがうまくやれる。


# 14.Comparableを実装することを考慮せよ
* Javaライブラリの値クラスは、enumも含めておおむねComparableを実装している。
* BigDecimalについて、equalsではBigDecimal("1.0")とBigDecimal("1.00")は異なる扱いになるが、compareToでは同じ扱いになる。そのため、HashSetにこれらの2つを入れたときには、2つの要素が残るが、TreeSetに入れた場合には、1つになる。
* compareToの中で、不等号を使って比較を行うことは冗長で、エラーの要因となりうるので、プリミティブ型のラッパークラスのcompareを使うべき。
* 複数キーでのソートを考える場合、Comparatorのコンストラクションメソッドを使うことを考慮に入れる。1つずつ比較して、if文で分けていくよりもこちらのほうが性能が良いらしい。


```java
package tryAny.effectiveJava;

import static java.util.Comparator.*;
import java.util.Comparator;
import java.util.stream.Stream;

public class CompareTest {
    public static void main(String[] args) {
	Stream<PhoneNum> s = Stream.of(new PhoneNum(111, 222, 333), new PhoneNum(111, 222, 222),
		new PhoneNum(111, 333, 111), new PhoneNum(000, 999, 1));
	s.sorted().forEach(System.out::println);
    }
}

class PhoneNum implements Comparable<PhoneNum> {
    int areaCode;
    int prefix;
    int lineNum;

    public PhoneNum(int areaCode, int prefix, int lineNum) {
	this.areaCode = areaCode;
	this.prefix = prefix;
	this.lineNum = lineNum;
    }

    private static final Comparator<PhoneNum> COMPARATOR = comparingInt((PhoneNum pn) -> pn.areaCode)
	    .thenComparingInt(pn -> pn.prefix).thenComparingInt(pn -> pn.lineNum);

    @Override
    public int compareTo(PhoneNum pn) {
	return COMPARATOR.compare(this, pn);
    }
    
    @Override
    public String toString() {
	StringBuilder sb = new StringBuilder();
	sb.append("areaCode:").append(areaCode).append(",prefix:").append(prefix).append(",lineNum:").append(lineNum);
	return sb.toString();
    }
}
```

# 4章.クラスとインターフェース



# 15.クラス、メンバ変数のアクセシビリティは最小限にせよ



* 情報を隠す第一の目的は、システム構成から独立したものに切り分けておき、独立に開発、テスト、最適化、理解、変更等ができるようにしておくことである。



* classのアクセシビリティには、publicかpackage-private（アクセス修飾子なし）しかない。



* package-privateなクラスが1つのクラスからのみ呼ばれているのであれば、private static な入れ子クラスにすることを検討して、アクセスされる可能性を低くするべき。



* Java9からは、アクセス制御の仕組みとして、module	systemが採用されている。



# 16.publicなクラスにおいては、アクセサメソッドを用い、フィールドをpublicにはしないようにせよ



* java.awtクラス内のPoint.javaなどはフィールド変数のアクセシビリティがpublicになっていたりするが、性能問題によりそうしているよう。

* immutableなフィールド変数であれば、publicであっても害は少ないが、やめておいたほうが良い。



# 17.可変性を最小限にせよ

* 不変クラスは設計、使用、実装が可変クラスよりもしやすい。

* 不変クラスを作るにあたって、以下の5つをルールを順守するべし。

  * オブジェクトの状態を変更させるようなメソッドを提供しない

  * 継承が不可能であるように作る

  * 全てのフィールドをfinalにする

  * 全てのフィールドをprivateにする

  * 可変クラスへのアクセスをさせないようにする

* 不変クラスは本質的にスレッドセーフであり、同期が必要ない。

* 不変クラスのデメリットは、異なる値に対して別々のオブジェクトを作成することとなり、コストが高くつく点にある。これの解決策として、コンパニオンクラスなるものがある。具体例としては、不変クラスであるStringに対応する可変クラスのStringBuilderである。

* 不変クラスを継承させない方法として、クラスにfinal修飾子をつける以外の方法として、コンストラクタをprivateとして、ファクトリメソッドをpublicで作成する方法がある。

* BigInteger,BigDecimalが実装された当時は、不変クラスは継承させないほうが良い、ということが分かっていなかったため、継承が可能。

* 可能な限り不変クラスに近づけるため、原則として、フィールドはprivate final にするべき。（CountDownLatchは好例）



# 18.継承よりコンポジションを選ぶべし

* 具象クラスをパッケージをまたいで継承するのは危険。起こりうる問題は以下のように2つある。

  * スーパークラスの実装はリリース毎に変わりうる。サブクラスはそれに合わせて変更を加えなければならないかもしれない。

  * スーパークラスに新しいメソッドが追加された場合にセキュリティホールとなる場合があるらしい。（**全然ピンと来ない**）

* 継承を回避するにあたっては、もともとスーパークラスになるはずだったクラスを private finalなフィールドとして取り込み（composition）、各メソッドでその取り込んだフィールドのメソッドを参照する（forwarding）ことによって実現できる。

* ↑の作りの欠点は、callback framework　には向いていないということ。ラップされたオブジェクトはどれがラップしたオブジェクトであるかを認識しないため、自身への参照でサブクラス呼び出しをすることができない。

* B is a A の関係が本当に成り立たない限り、B extends A はやめたほうが良い。これはJavaプラットフォームライブラリでも守れていなくて、Stack はVectorではないので、StackがVectorを継承するべきではないし、Properties と HashListの関係も同様である。



# 19.継承のための設計、ドキュメンテーションがをすべし。なければ継承を禁止すべし

* オーバーライド可能なメソッドに関しては、自身の利用方法を書く必要がある。そのためのJavadoc用のアノテーションが@implSpecである。

* 一般に良いAPIは、何をするかを記述し、どのようにするかを記述しないが、継承を安全に行うにあたっては詳細な仕様が必要であるため記述する。

* 継承元となるクラスの設計をテストするには、実際にサブクラスを作ってみてテストするほかない。広く使われるライブラリを目指すのであれば、一度リリースしたprotectedなメソッドはほぼ変更不可能なので、必ずリリース前にサブクラスを作ってみて確かめてみるべき。

* コンストラクタでオーラライドできるメソッドの呼び出しをしてはならない。なぜなら、サブクラスのコンストラクタの処理が走る前に、スーパークラスのコンストラクタの処理が必ず走るが、「サブクラスのコンストラクタ内で、サブクラスのフィールド初期化等の処理があり、オーバーライドしたメソッドがそのフィールドを用いた処理を行う」といった場合には、直感的でない挙動を示すため。

* 基本的に、継承元として設計するクラスには、Serializable,Clonableは実装させるべきではないが、やまれぬ事情でそうする場合には、readObjectメソッド、cloneメソッドの中で、オーバーライドされうるメソッドを呼んではならない。呼んでしまうと、クローンオブジェクトができていないのに、それに対して変更を加えようとする、みたいなことが起こり得るため。



# 20.抽象クラスよりインターフェースを優先せよ

* 現存しているクラスを、新しく誕生したインターフェースを実装するように改変するのは容易である。

* インターフェースはmixinsを定義するのに最適である。

  * mixinとは単独で動作することを意図しないコード（再利用したいコード）を予め定義しておき、必要に応じてクラスに混ぜ込む（Javaで言うとimplementsする）ことによって、処理の再利用を促す仕組みの事である。

<https://ja.wikipedia.org/wiki/Mixin>

<http://equj65.net/tech/java8mixin/>

* non-primitive interface method ってなんだ？

* interfaceの利点と抽象クラスの利点を伏せ持つ、骨格実装クラス（skeletal implementation class）がある。骨格実装クラスは、AbstractInterfaceと呼ばれているもので、CollectionsFWのAbstractCollectionやAbstractSetなどがそれにあたる。（本来ならこれらはSkeletalCollection,SkeletalSetと呼ばれるべきだが、慣習的にこう呼ばれている）

* 骨格実装クラスはimplementsしたインターフェースが提供しているメソッドの一部をオーバーライドし、残りのメソッドを骨格実装クラスを継承するクラスでのオーバーライドにゆだねるように作られる。この骨格実装クラスがないと、実装者は直接インターフェースをimplementsして、提供される全てのメソッドをオーバーライドしないといけないが、骨格実装クラスを挟むことによって、実装者がオーバーライドすべきメソッドが減る（誤ったオーバーライドがなされる危険性も減る）。**これが利点という理解でOKなのか？**



# 21.後々のことを考えてインターフェースは設計せよ

* 現存するインターフェースにメソッドを追加することにはリスクがある。

  * 例として、Collection に removeIf がデフォルトメソッドとして追加されたが、 Collection を implements している Apatche Commonsライブラリの SynchronizedCollection でこの removeIf を呼び出した際には、同期されないメソッドとして呼び出され、SynchronizedCollection 使用における約束事が破られてしまう。Javaライブラリではこれと同様のことを防ぐため、Collections.synchronizedCollection において removeIfメソッドをオーバーライドしている。



# 22.インターフェースは型定義のためだけに用いよ

* 定数定義だけするようなインターフェース（constant interface）を作るべきでない。java.io.ObjectStreamConstants がやっているがマネするべきでない。以下理由。

  * そのうち定数が必要なくなった時でも、バイナリ互換性の維持のために implements し続けなければならない。（**バイナリ互換性??**）

  * 定数インターフェースを implements したら名前空間が汚染される。

* 定数定義の別の合理的な方法は以下。

  * 定数定義する値が現存するクラスと密接に結びついているとしたら、そこに加える。

  * 定数定義する値が列挙するのがベストなものであればEnumを使う。

  * それ以外だと、ユーティリティクラスを使う。



```java

// Constant utility class

public interface PhysicalConstants {

    static final double AVOGADROS_NUMBER = 6.02214199e23;

    static final double BOLTZMANN_CONSTANT = 1.3806503e-23;

    static final double ELECTRON_MASS = 9.10938188e-31;

}

```

  *   * ユーティリティクラスからたくさん定数を利用する場合はstatic importを使う。

```java

// Use of static import to avoid qualifying constants

import static com.effectivejava.science.PhysicalConstants.*;

 public class Test {

    double  atoms(double mols) {

        return AVOGADROS_NUMBER * mols;

    }

    ...

    // Many more uses of PhysicalConstants justify static import

```


# 5章.ジェネリクス

# 26.raw タイプは使ってはならない

* rawタイプとは、型パラメータなしで宣言されたジェネリック型のことを指す。例えば、List< E > に対する、List のようなものをrawタイプと呼ぶ。
* rawタイプを用いると、型パラメータを明確にして宣言したジェネリクス型であればコンパイル時に検出できた誤りが、実行時まで検出されなくなる。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;

public class GenericsTest1 {

    public static void main(String[] args) {
        final Collection stamps = Arrays.asList(new Stamp(), new Stamp(), "");
        // 以下のコードだとコンパイルエラーとして検出してくれる。
        // final Collection<Stamp> stamps = Arrays.asList(new Stamp(), new Stamp(), "");
        for (Iterator i = stamps.iterator(); i.hasNext();) {
            Stamp stamp = (Stamp) i.next(); // 3つ目の要素をキャストするときにエラー送出。実行時に初めてわかる。
            System.out.println("cast success");
        }
    }

    static class Stamp {

    }
}
```

* Listのようなrawタイプを使うべきではないが、任意の型を許容する、List< Object > のようなジェネリック型は使用してもよい。
大まかに、この2つの違いは、前者はジェネリックに適応していないが、後者はコンパイラに明確にどのような型も許容すると明確に示している。
例えば、List< String >をList型に入れることはできるが、List< Object >に入れることはできない。

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.List;

public class GenericsTest2 {
    public static void main(String[] args) {
        List<String> strings = new ArrayList<>();
        unsafeAdd(strings, Integer.valueOf(42));
        String s = strings.get(0); // Has compiler-generated cast
    }

    private static void unsafeAdd(List list, Object o) {
        // 以下のコードにするとコンパイルエラーにしてくれる。
        // private static void unsafeAdd(List<Object> list, Object o) {
        list.add(o);
    }

}
```

* 要素となる型が何であれ構わない場合にはrawタイプを使いたくなるかもしれないが、**?**のワイルドカードを使うべきである。
これらの違いも型安全性にある。

```java
package tryAny.effectiveJava;

import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class GenericsTest3 {

    public static void main(String[] args) {
        Set<?> s1 = Stream.of("2", "b", 1).collect(Collectors.toSet());
        Set s2 = Stream.of("2", "c", 1).collect(Collectors.toSet());

        // s1.add("c"); // このコードはコンパイルエラーとなる
        s2.add("b");

        System.out.println(numElementsInCommon(s1, s2));
    }

    // Use of raw type for unknown element type - don't do this!
    static int numElementsInCommon(Set<?> s1, Set<?> s2) {
        int result = 0;
        for (Object o1 : s1)
            if (s2.contains(o1))
                result++;
        return result;
    }
}
```

* rawタイプを使うべきでないという規則の例外が少数ある。
  * クラスのリテラルに型パラメータを使ったジェネリック型を指定することはできない。つまり、List.classやString[].classは許されるが、List< String >やList< ? > は許されない。
  * instanceof を型パラメータを使ったジェネリック型に対して使うことはできないので（Unbounded wildcard type除く）、その時はrawタイプで検査する。

```java
// Legitimate use of raw type - instanceof operator
if (o instanceof Set) {       // Raw type
    Set<?> s = (Set<?>) o;    // Wildcard type
    ...
}
```

# 27.unchecked warnings は削除せよ

* コンパイラが出すunchecked warningsを全部消すことができれば、そのコードはタイプセーフ、つまり、実行時にClassCastExceptionを発生させることがなくなる。よって、unchecked warningsは全て消すようにするべきである。
* すべてのwarningは消すことができないが、タイプセーフであることを証明できた場合は```@SuppressWarnings("unchecked")```アノテーションを付与する。
タイプセーフであることを証明する前にこのアノテーションを付与してしまうと、コンパイル時にunchecked warnings はでないのに、ClassCastExceptionは出ることとなり、エラー解消を困難にしてしまう。
* ```@SuppressWarnings("unchecked")```の付与はできるだけ小さいスコープにするべきである。

```java
package tryAny.effectiveJava;

import java.util.Arrays;

public class GenericsTest4 {

    private int size;
    transient Object[] elementData; // non-private to simplify nested class access

    public <T> T[] toArray(T[] a) {
        if (a.length < size) {
            @SuppressWarnings("unchecked")
            T[] result = (T[]) Arrays.copyOf(elementData, size, a.getClass());
            return result;
        }
        System.arraycopy(elementData, 0, a, 0, size);
        if (a.length > size)
            a[size] = null;
        return a;
    }
}
```

* ```@SuppressWarnings("unchecked")```を使用するときは、なぜそれが安全なのか理由を記載すべき。
記載することによって、コードの理解の助けになるし、誰かが安全でない演算となるような変更を加える機会は減る。

# 28.配列よりもリストを使うべし

* 配列はジェネリック型と比べて2つの重要な点で異なる。
  * 配列は共辺（covariant）である。例えば、SubクラスはSuperクラスのサブクラスであるとして、Sub[]クラスはSuper[]クラスのサブクラスである。
  一方で、ジェネリックスは共辺ではない。どのような2つのType1、Type2クラスであっても、List< Type1 > 、List< Type2 >は親子関係になりえない。
  この性質から、以下のようなコードでは、配列は実行するまで結果が分からないがListはコンパイル時にわかる。
  
```java
package tryAny.effectiveJava;

public class GenericsTest5 {
    public static void main(String[] args) {

        Object[] objAry = new Long[1];
        objAry[0] = "aa";

        // Won't compile!
        // List<Object> ol = new ArrayList<Long>(); // Incompatible

    }
}
```
  * 配列は物象化（reified）される。配列は実行時に要素を知り、要素を処理する。
  一方で、ジェネリクスはイレイジャー（erasure）によって実装される。ジェネリクスはコンパイル時にのみ型制限が効き、実行時には要素の型情報は捨てられる。
  
* 上記のような根本的な違いにより、配列とジェネリクスはうまく混ぜて使うことができない。例えば、```new List< E >[]```といったコードはコンパイル時にはじかれる。
ジェネリクスの配列が作れない理由を、以下のコードの1行目がコンパイルエラーにならないと仮定して説明していく(本当は1行目でコンパイルエラー)。
2行目で要素を一つ持つList<Integer>が作られる。
3行目でList< String > の配列を Objectの配列に格納している。これは配列はcovariantであるので成立する。
4行目でObject配列にList< Integer > を格納している。これは実行にはList< Integer >は単にListで、List< String >[]は単にList[]となるため、ArrayStoreExceptionは発生しない。
そうすると、5行目でList< String >の中から取り出した要素がIntegerであり、ClassCastExceptionが発生する。
このようなことを防ぐために、ジェネリック型の配列はコンパイルエラーにしている。


```java
// Why generic array creation is illegal - won't compile!
List<String>[] stringLists = new List<String>[1];  // (1)
List<Integer> intList = List.of(42);               // (2)
Object[] objects = stringLists;                    // (3)
objects[0] = intList;                              // (4)
String s = stringLists[0].get(0);                  // (5)
```

* EやList< E >といった型は**non-reifiable**と呼ばれる。この言葉の直感的な意味は、コンパイル時よりも実行時の時の方が持っている情報が少ない、という意味である。?のワイルドカードを使ったジェネリック型のみreifiableであるが、ワイルドカードを使ったジェネリクスの配列に実用的な価値はない。
* ジェネリック型の配列が作れないことによって、可変長引数を持つメソッドを利用する時などの対応が面倒となる。可変長引数のメソッドを利用するときは、可変長引数を保持するために配列が作られる。これらの要素型がnon-reifiableだった場合には、ワーニングが出る。これの対処のためには```SafeVarargs```アノテーションを使用する（Item32）。
* ジェネリック型の配列が作れなかったり、配列へのキャストができない状況に直面した場合には、要素型の配列**E[]**よりも、コレクション型**List< E >**を利用するべき。こうすることで、簡潔さやパフォーマンスを犠牲にして型安全性と相互運用性を担保できる。
* 例として、コンストラクタにcollectionをとり、唯一のメソッドでそのcollectionの中にある要素をランダムで取り出す、Chooserクラスを書くとする。
ジェネリックスを使わずに書くと以下のようになる。このクラスを使う場合だと、メソッドを使うとき常に望む型であるかキャストせねばならないし、キャストに失敗したときには実行時にエラーが出てしまう。

```java
package tryAny.effectiveJava;

import java.util.Collection;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

public class Chooser1 {
    private final Object[] choiceArray;

    public Chooser1(Collection choices) {
        choiceArray = choices.toArray();
    }

    public Object choose() {
        Random rnd = ThreadLocalRandom.current();
        return choiceArray[rnd.nextInt(choiceArray.length)];
    }

}
```

Item29に従い、ジェネリックスで書いたのが以下。少し冗長で、性能劣化するが、実行時にClassCastExceptionを出さない。

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

//List-based Chooser - typesafe
public class Chooser2<T> {
    private final List<T> choiceList;

    public Chooser2(Collection<T> choices) {
        choiceList = new ArrayList<>(choices);
    }

    public T choose() {
        Random rnd = ThreadLocalRandom.current();
        return choiceList.get(rnd.nextInt(choiceList.size()));
    }
}
```

# 29.ジェネリック型を使用すべし

* Item7で扱った、簡単なスタックの実装について考えてみる。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.EmptyStackException;

//Object-based collection - a prime candidate for generics
public class Stack1 {
    private Object[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    public Stack1() {
        elements = new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(Object e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public Object pop() {
        if (size == 0)
            throw new EmptyStackException();
        Object result = elements[--size];
        elements[size] = null; // Eliminate obsolete reference
        return result;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }

}
```

* クラスをジェネリック化するにあたっては、まず型パラメータをクラスに加える。上記のスタックの場合は1つ型パラメータが必要で、それはスタックの要素であるので、慣習に従って名前は E とする（Item68）。
* その次に、全てのObject型を適切な型パラメータに置換し、コンパイルできるようにする。
* non-reifiableな型の配列ができてしまった場合の対処法の1つは、Objectで配列をnewしてやり、それをキャストしてやる方法があるが、一般にはこれはタイプセーフではない。
今回の場合、問題となるのはコンストラクタの中のソースだが、elementsフィールドはprivateであり、pushメソッド以外から値を入れることはないので、実態がEであることは保証されている。よって```@SuppressWarning("unchecked")```の付与を最小の範囲で、かつ、コメント付きで付与してやることでwarningを消してやるべき。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.EmptyStackException;

//Initial attempt to generify Stack - won't compile!
public class Stack2<E> {
    private E[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    // The elements array will contain only E instances from push(E).
    // This is sufficient to ensure type safety, but the runtime
    // type of the array won't be E[]; it will always be Object[]!
    @SuppressWarnings("unchecked")
    public Stack2() {
        elements = (E[]) new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(E e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public E pop() {
        if (size == 0)
            throw new EmptyStackException();
        E result = elements[--size];
        elements[size] = null; // Eliminate obsolete reference
        return result;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }

}
```

* non-reifiableな型の配列ができてしまった場合の対処法のもう1つは、配列の宣言はObjectで行うようにすることが考えられる。
この場合でも、そのままではpopメソッドにてエラーが発生してしまうので、キャストをする。キャストするとwarningがでてしまうが、上と同じ理由で今回も E にキャストできることは自明なので、```@SuppressWarning("unchecked")```を最小の範囲で付与する（Item27）。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.EmptyStackException;

public class Stack3<E> {
    private Object[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    public Stack3() {
        elements = new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(E e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public E pop() {
        if (size == 0)
            throw new EmptyStackException();
        // push requires elements to be of type E, so cast is correct
        @SuppressWarnings("unchecked")
        E result = (E) elements[--size];
        elements[size] = null; // Eliminate obsolete reference
        return result;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }

}
```

* 上記2つの方法に関して、前者の方が読みやすく、キャストもインスタンス生成時の一回で済むので、一般的には前者が多く使われる。しかし、heap pollution（Item32）、つまり、実行時の配列の型とコンパイル時の型が異なるので、それにいらだって後者を選択するプログラマーもいる。
* 上記の例はItem28の、配列よりもlistを使うべしという助言に矛盾しているが、Javaは本来listをサポートしておらず、ジェネリック型のどこかでは配列を使用しなければならない。例えば、ArrayListなどでは配列を使っている。また、HashMapなどではパフォーマンスのために配列を用いている。
* 上記の例の型パラメータには基本的に何でも指定できるが、Stack< int > や Stack< double >などプリミティブ型を指定するとコンパイルエラーとなる。プリミティブ型を使いたいような場合はボックス化されたものを型パラメータに指定する（Item61）。
* ジェネリック型の中には、型パラメータに制限を課しているものもある。例えば、DelayQueueクラスは以下のように境界のあるパラメータを使用している。

```java
class DelayQueue<E extends Delayed> implements BlockingQueue<E>
```

# 30.ジェネリックメソッドを選択すべし
* Collectionsの中のアルゴリズム系のメソッド（バイナリサーチやソート）はジェネリックメソッドである。
* ジェネリックメソッドを書くことはジェネリック型を書くのと似ている。以下のようにrawタイプで書くとwarningが現れる。

```java
// Uses raw types - unacceptable! (Item 26)
public static Set union(Set s1, Set s2) {
    Set result = new HashSet(s1);
    result.addAll(s2);
    return result;
}
```

warningを消して、タイプセーフにするにおいては、メソッド修飾子とメソッドの返り値の間に型パラメータを書いて以下のようにする。

```java
// Generic method
public static <E> Set<E> union(Set<E> s1, Set<E> s2) {
    Set<E> result = new HashSet<>(s1);
    result.addAll(s2);
    return result;
}
```

* immutableであるけれど、たくさんの異なる型に適応できるオブジェクトが必要となる場合があるかもしれない。
ジェネリックスはerasureによって実装されているので、求められるすべての型パラメータに対して、1つのオブジェクトで対応できるが、繰り返し、求められる型のオブジェクトを生成するstaticなファクトリメソッドを書く必要がある。このパターンは、generic singleton factoryと呼ばれ、関数オブジェクト（Item42）生成などに用いられる。
* 自分自身を返す関数が必要だとすると、Fuction.identityメソッドを用いれば事足りるが、説明にはもってこいなので下記に記す。
```IDENTITY_FN```を```UnaryOperator<T>```にキャストするときにwarningがでるが、```identity```関数は引数を変更せずに返却するので、warningを抑制することができる。

```java
package tryAny.effectiveJava;

import java.util.function.UnaryOperator;

public class GenericsTest7 {
    public static void main(String[] args) {
        String[] strings = { "jute", "hemp", "nylon" };
        UnaryOperator<String> sameString = identityFunction();
        for (String s : strings)
            System.out.println(sameString.apply(s));
        Number[] numbers = { 1, 2.0, 3L };
        UnaryOperator<Number> sameNumber = identityFunction();
        for (Number n : numbers)
            System.out.println(sameNumber.apply(n));

    }

    // Generic singleton factory pattern
    private static UnaryOperator<Object> IDENTITY_FN = (t) -> t;

    @SuppressWarnings("unchecked")
    public static <T> UnaryOperator<T> identityFunction() {
        return (UnaryOperator<T>) IDENTITY_FN;
    }

}
```

* 型パラメータが自身の型変数を含んだ表現で定義されている場合を、再帰型境界という。再帰型境界は```Comparable```インターフェースと関係がある。

```java
public interface Comparable<T> {
    int compareTo(T o);
}
```

* ```Collection```の並べかえ、ソート、最大最小導出のメソッドでは、```Comparable```を実装した要素を使っている。これらのメソッドでは互いに比較可能な要素が必要となるが、それを以下のように表現してる。

```java
// Using a recursive type bound to express mutual comparability
public static <E extends Comparable<E>> E max(Collection<E> c);
```
```<E extends Comparable<E>>```の表すところは、「自身と比較可能なあらゆる要素E」である。
以下が再帰型境界を使ったmaxメソッドとなる。

```java
package tryAny.effectiveJava;

import java.util.Collection;
import java.util.Objects;

public class GenericsTest8 {
    // Returns max value in a collection - uses recursive type bound
    public static <E extends Comparable<E>> E max(Collection<E> c) {
        if (c.isEmpty())
            throw new IllegalArgumentException("Empty collection");
        E result = null;
        for (E e : c)
            if (result == null || e.compareTo(result) > 0)
                result = Objects.requireNonNull(e);
        return result;
    }

}
```

上記のメソッドはlistが空の時にIllegalArgumentExceptionを発生させる。良い代替案としては、戻り値を```Optional<E>```とすることがあげられる。

* 再帰型境界はもっと複雑になりえるが、まれである。本章で扱ったイディオムと、ワイルドカードを用いる場合（Item31）と、simulated self-type（Item2）を理解すれば、実際に直面する大体の再帰型境界は扱うことができる。

# 31.APIの柔軟性のために境界ワイルドカードを使用すべし

Item28でもあったように、型パラメータはinvariantである。よって、例えば、```List<String>```は```List<Object>```のサブタイプではない。```List<Object>```のできることすべてが、```List<String>```にできるわけではないので、リスコフの置換原則にも符合する。（Item10）
時には、もっと柔軟性が必要となることがある。Item29で使用したStackクラスを例に考えてみる。StackクラスのAPIは以下のよう。

```java
public class Stack<E> {
    public Stack();
    public void push(E e);
    public E pop();
    public boolean isEmpty();
}
```
ここに要素のシーケンスを引数にとり、それらをすべてStackにのせるメソッドを追加することを考える。最初に考えるのは以下のようなものだろう。

```java
// pushAll method without wildcard type - deficient!
public void pushAll(Iterable<E> src) {
    for (E e : src)
        push(e);
}
```

このメソッドはコンパイルできるが、満足いくものではない。```Iterable<E> src```の要素がStackの要素と一致すればうまく動くが、例えば、以下のようなコードはエラーとなる。エラーの理由は、型パラメータはinvariantだからである。

```java
Stack<Number> numberStack = new Stack<>();
Iterable<Integer> integers = ... ;
numberStack.pushAll(integers);
```

ここで出てくるエラーに対処するためには、型引数にワイルドカードを用いる。

```java
// Wildcard type for a parameter that serves as an E producer
public void pushAll(Iterable<? extends E> src) {
    for (E e : src)
        push(e);
}
```
この対応によって、コンパイルできるようになり、タイプセーフにもなる。

次に、collectionを引数にとり、Stackにたまっている要素をすべてそれに移す、```popAll```メソッドを考えてみる。素案は以下のよう。

```java
// popAll method without wildcard type - deficient!
public void popAll(Collection<E> dst) {
    while (!isEmpty())
        dst.add(pop());
}
```
これは要素EがStackのそれと完全に一致した場合にはうまく動くが、そうでない場合は動かない。つまり、以下のコードはコンパイルエラーとなる。

```java
Stack<Number> numberStack = new Stack<Number>();
Collection<Object> objects = ... ;
numberStack.popAll(objects);
```
対処するためには、以下のようにここでも型引数にワイルドカードを用いる。

```java
// Wildcard type for parameter that serves as an E consumer
public void popAll(Collection<? super E> dst) {
    while (!isEmpty())
        dst.add(pop());
}
```

ここでの教訓は明確で、**インプットされる引数が、producerまたは、consumerのどちらかの役割を果たすときワイルドカードを使う**、ということである。
インプットされる引数がproducer、consumerのどちらの役割も果たす場合には、ワイルドカードを使う必要はない。
使いどころは以下のように記憶する。

```
PECS stands for producer-extends, consumer-super.
```
これはつまり、型変数Tがproducerである場合には、```<? extends T>```を用い、consumerである場合には```<? super T>```を用いるということを表している。上のStackの例もそのようになっている。

このPECSの具体例を本章の例に適用していく。
Item28の以下のコンストラクタについて考える。

```java
public Chooser(Collection<T> choices)
```
この引数はproducerの役割を果たすので、PECSに従い、以下のようになる。

```java
// Wildcard type for parameter that serves as an T producer
public Chooser(Collection<? extends T> choices)
```

次に、Item30の以下のunionメソッドについて考える。

```java
public static <E> Set<E> union(Set<E> s1, Set<E> s2)
```
引数はどちらもproducerの役割を担うため、以下のようになる。

```java
public static <E> Set<E> union(Set<? extends E> s1,
                               Set<? extends E> s2)
```
ここでの注意点は、**戻り値の型には境界ワイルドカードを使ってはならない**ということだ。
そのような対応は、ユーザにとって柔軟性が増すというより、クライアントのコードの中でワイルドカードを使うことを強いることになる。
**クラスの使用に当たって、ユーザが境界ワイルドカードのことを考えないといけないのは、そのAPIに問題があると考えられる。**

Java8より前だと以下のように型を明示してやらねばならない。

```java
// Explicit type parameter - required prior to Java 8
Set<Number> numbers = Union.<Number>union(integers, doubles);
```

次に、Item30のmaxメソッドについて考える。

```java
public static <T extends Comparable<T>> T max(List<T> list)
```
これをPECSに当てはめると、以下のようになる。

```java
public static <T extends Comparable<? super T>> T max(
        List<? extends T> list)
```
ここでは2回PECSを当てはめている。
**Comparableは常にconsumerなので、```Comparable<T>```より```Comparable<? super T>```を選択するべき**。
**Comparatorも同様なので、```Comparator<T>```より```Comparator<? super T>```を選択するべき**。

そのほかに、ワイルドカード関連で議論すべきは、型パラメータを使うべきか、ワイルドカードを使うべきかの問題がある。
例えば、listのスワップを行うメソッドは、型パラメータを使用した場合と、ワイルドカードを使用した場合の2通りが考えられる。

```java
// Two possible declarations for the swap method
public static <E> void swap(List<E> list, int i, int j);
public static void swap(List<?> list, int i, int j);
```
どちらが好まれるかというと、2つ目のワイルドカードを使用したメソッドの方がシンプルであるので好まれる。
一般に**型変数がメソッド内の一か所にしか現れない場合には、ワイルドカードに置き換えるべきである。**
2つ目のメソッドは以下のように、それだけを書くとコンパイルエラーとなる。

```java
public static void swap(List<?> list, int i, int j) {
    list.set(i, list.set(j, list.get(i)));
}
```

```
型 List<capture#2-of ?> のメソッド set(int, capture#2-of ?) は引数 (int, capture#3-of ?) に適用できません
```
これを解消するためには、ワイルドカードを型にはめるヘルパークラスを作成する。

```java
package tryAny.effectiveJava;

import java.util.List;

public class GenericesTest9 {
    public static void swap(List<?> list, int i, int j) {
        swapHelper(list, i, j);
    }

    // Private helper method for wildcard capture
    private static <E> void swapHelper(List<E> list, int i, int j) {
        list.set(i, list.set(j, list.get(i)));
    }

}
```
こうすることによって、実装が多少複雑になるが、ユーザにはシンプルなswapメソッドを見せることができる。

# 32.ジェネリクスと可変長引数を結び付ける際は慎重にせよ

可変長引数を持つメソッドとジェネリクスは、Java5で同時にリリースされたが、相性はよくない。
可変長引数はleaky abstraction である。
<https://euske.github.io/slides/sem20170627/index.html>
可変長引数を持つメソッドを呼び出すときには、可変長引数を保持するために配列が作成され、この配列は見えてしまう。（抽象化された場合、本来はユーザから意識させてはならないということを指して、leaky abstractionといっているのだと思われる）
結果として、ジェネリック型やパラメータ化された型を可変長引数に渡した場合には、コンパイラーは混乱してしまう。
non-reifiableな型を可変長引数としたメソッドを宣言した場合には、コンパイラがワーニングを上げる。また、non-reifiableと推論される型をもつ可変長引数が渡されるメソッドが呼び出される時もワーニングが上がる。そのワーニングは以下のよう。

```
warning: [unchecked] Possible heap pollution from
    parameterized vararg type List<String>
```
Heap pollution は、様々なパラメータ化された型が、その型とは違う方を参照するときにおこる。Heap pollutionによってコンパイラによって自動的に起こるキャストが失敗し、ジェネリック型が保証する型安全の基盤が侵されてしまう。

例として、以下のメソッドについて考える。

```java
// Mixing generics and varargs can violate type safety!
static void dangerous(List<String>... stringLists) {
    List<Integer> intList = List.of(42);
    Object[] objects = stringLists;
    objects[0] = intList;             // Heap pollution
    String s = stringLists[0].get(0); // ClassCastException
}
```
このメソッドは明確なキャストをしていないにも関わらず、```ClassCastException```が発生する。最終行でコンパイラによる暗黙のキャストが実行され、失敗している。
このことは、**ジェネリック型の可変長引数に値を格納するのは安全でない**ことを示している。
なぜ、ジェネリック型の可変長引数を持つメソッドが宣言された時点でコンパイルエラーが出ないかというと、ジェネリック型やパラメータ化された型の可変長引数がとても便利だからである。
例として、```Arrays.asList(T... a)```, ```Collections.addAll(Collection<? super T> c, T... elements)```,```EnumSet.of(E first, E... rest)```などのメソッドがJava標準ライブラリにあり、これらはタイプセーフである。
Java6以前では、ジェネリック型の可変長引数を持ったメソッドの呼び出し箇所で現れるワーニングを、メソッドの作者が対処する方法はなかった。これにより、呼び出し側でいちいち、```@SuppressWarnings("unchecked")```を書かねばならなかった。
Java7においては、```SafeVarargs```アノテーションなるものが追加された。これをジェネリック型の可変長引数を持ったメソッドに付与することで、呼び出し側でワーニングが出ることはなくなる。**```SafeVarargs```アノテーションは、メソッドの作者が、そのメソッドはタイプセーフであると約束していることを表している。**
```SafeVarargs``` アノテーションでは、本当にタイプセーフであるかが重要となるが、どのようにタイプセーフであるかを確かめるべきか？
ジェネリック型の配列は、可変長配列を保持するために、メソッドが呼び出されたときに生成される。メソッドの処理において、該当の配列への格納を行わず、該当の配列への信用できないコードからの参照を許していない場合には、安全といえる（つまり、引数からメソッドへの単純な移送のみが安全といえる）。
可変長引数配列に対して、何も格納しなかったとしても、タイプセーフを脅かし得ることはしっておくべき。以下の例は一見問題がなさそうだが、危険がはらんでいる。

```java
// UNSAFE - Exposes a reference to its generic parameter array!
static <T> T[] toArray(T... args) {
    return args;
}
```
この配列の型は、メソッドの引数に渡された型のコンパイル時の型、で決まるが、コンパイラは正確な判断の下すための十分な情報を与えられない。このメソッドは可変長引数の配列を返すので、heap pollutionが呼び出しスタックにおいて起きる。
具体的に考えるために、以下のようなメソッドを考えてみる。

```java
static <T> T[] pickTwo(T a, T b, T c) {
    switch(ThreadLocalRandom.current().nextInt(3)) {
      case 0: return toArray(a, b);
      case 1: return toArray(a, c);
      case 2: return toArray(b, c);
    }
    throw new AssertionError(); // Can't get here
}
```
このメソッドをコンパイルするにあたり、コンパイラは2つの```T```インスタンスを```toArray```メソッドに渡すための可変長引数配列を生成するコード生み出す。そのコードは、呼び出し元でどのようなオブジェクトが渡されてもよいように、```Object[]```の配列を配置する。```toArray```メソッドは単にこの配列を```pickTwo```メソッドに返し、```pickTwo```メソッドが呼び出し元にこの配列を返す。よって、```pickTwo```メソッドは常に```Object[]```型の配列を返す。
以下のメインコードから、```pickTwo```を呼び出すことを考える。

```java
public static void main(String[] args) {
    String[] attributes = pickTwo("Good", "Fast", "Cheap");
}
```
このコードに関しては、コンパイルエラー、ワーニングともに出ないが、実行すると明示的にキャストしていないのに、```ClassCastException```が発生する。これは、```pickTwo```メソッドの戻り値の型が```Object[]```であるので、それを```String[]```にしようとしているところで発生している。
この例は、**ほかのメソッドにジェネリック型の可変長引数配列にアクセスをゆるすのは安全でない**、ということを再認識させる。これには以下2つの例外がある。
  * 正しく@SafeVarargsが付与されているメソッドにその配列を渡すのは安全
  * その配列を可変長でない引数のメソッドに、単に配列の内容の演算をかける場合は安全

典型的な安全なジェネリック型の可変長引数の使い方は以下のよう。

```java
// Safe method with a generic varargs parameter
@SafeVarargs
static <T> List<T> flatten(List<? extends T>... lists) {
    List<T> result = new ArrayList<>();
    for (List<? extends T> list : lists)
        result.addAll(list);
    return result;
}
```
```SafeVarargs``` アノテーションをつけるか否かの判断はシンプルで、**ジェネリック型やパラメータ化された型の可変長引数を持つ全メソッドに```SafeVarargs``` アノテーションをつけるべき**。これはつまり、上述の```toArray```メソッドのような安全でない可変長引数メソッドは書くな、ということである。安全な可変長引数メソッドは以下を満たしている。
1. 可変長引数に何かを格納していない
2. 可変長引数を信頼ならないコードから視えるようにしていない

また、```SafeVarargs``` アノテーションはオーバーライドされないメソッドでのみ有効である。

```SafeVarargs``` アノテーションを使う以外の対応としては、Item28より、可変長引数を```List```に替えることが考えられる。そうすると、```flatten```メソッドは以下のように変わる。

```java
// List as a typesafe alternative to a generic varargs parameter
static <T> List<T> flatten(List<List<? extends T>> lists) {
    List<T> result = new ArrayList<>();
    for (List<? extends T> list : lists)
        result.addAll(list);
    return result;
}
```
こちらのいいところは、タイプセーフであることを保証し、```SafeVarargs``` アノテーションを自身で付与しなくていいところだ。悪いところは、クライアント側のコードが少し冗長になり、少し遅くなるかもしれないところだ。

# 33.型安全な異種コンテナーを検討する

  ```Set<E>``` や```Map<K,V>``` といったcollections、また、```ThreadLocal<T>``` や```AtomicReference<T>``` といった要素を格納するコンテナでは、型パラメータの数が固定されている（Setだと1つ、Mapだと2つ）。
  型パラメータの数が固定されていることは、大概の場合において、ユーザが望んでいることだが、時にはもっと柔軟性が必要となるときがある。こういった時の対応方法としては、コンテナをパラメータ化するのではなく、キーをパラメータ化する。
  このアプローチのシンプルな例として、クライアントに任意で複数の型のインスタンスを格納、検索をさせる```Favorites``` クラスを考える。
  ```Favorites``` クラスのAPIは以下のよう。Mapのキーが```Class<T>``` になっている。
  
```java
// Typesafe heterogeneous container pattern - API
public class Favorites {
    public <T> void putFavorite(Class<T> type, T instance);
    public <T> T getFavorite(Class<T> type);
}
```
以下のコードを実行すると、

```java
// Typesafe heterogeneous container pattern - client
public static void main(String[] args) {
    Favorites f = new Favorites();
    f.putFavorite(String.class, "Java");
    f.putFavorite(Integer.class, 0xcafebabe);
    f.putFavorite(Class.class, Favorites.class);
    String favoriteString = f.getFavorite(String.class);
    int favoriteInteger = f.getFavorite(Integer.class);
    Class<?> favoriteClass = f.getFavorite(Class.class);
    System.out.printf("%s %x %s%n", favoriteString,
        favoriteInteger, favoriteClass.getName());
}
```
予想通り、Java cafebabe パッケージ名$Favorites と出る。
```Favorites```インスタンスはタイプセーフであり、異種（heterogeneous：普通のMapと異なり、全てのキーの型が異なる)であるため、```Favorites```のようなクラスは、typesafe heterogeneous container と呼ばれる。
  実装は以下のよう。

```java
// Typesafe heterogeneous container pattern - implementation
public class Favorites {
    private Map<Class<?>, Object> favorites = new HashMap<>();

    public <T> void putFavorite(Class<T> type, T instance) {
        favorites.put(Objects.requireNonNull(type), instance);
    }

    public <T> T getFavorite(Class<T> type) {
        return type.cast(favorites.get(type));
    }
}
```
  Mapのキーが```Class<?>``` となっており、どんな型でもキーに取ることができる。
  また、Mapのバリューは```Object```である。つまり、Mapにおいてはキーとバリューの型の結びつきは保証されていない。
  ```putFavorites``` メソッドにおいては、単純にClassオブジェクトとインスタンスをMapに入れ込むのみ。
  ```getFavorites``` メソッドは技巧的で、Classオブジェクトをキーに、Mapから取ってきたバリューを、Classの```cast``` メソッドで動的に```T```を返すようにキャストしている。
  ```cast``` メソッドは、引数に取ったインスタンスが自身と同じ型なら、自身の型にキャストして戻す、ということをしている。

  ```Favorites``` クラスには2つ気を付けるべきことがある。
  1つ目は、悪意のあるクライアントは、rawタイプなClassオブジェクトを使って```Favorites``` クラスのタイプセーフを破ってくるということだ。これを防ぐためには、```putFavorite``` メソッドにおいて、格納するインスタンスが本当にキーと同じ型であるかを、```cast``` メソッドを使って確かめればよい。

```java
// Achieving runtime type safety with a dynamic cast
public <T> void putFavorite(Class<T> type, T instance) {
    favorites.put(type, type.cast(instance));
}
```
これについては、checkedSet, checkedList, checkedMap などでも同じ技術が使われている。これらのラッパークラスは、ジェネリックスとrawタイプが混在したアプリケーションにおいて、クライアントコードから不正な要素の追加をしているところを見つけ出すのに有用である。
  2つ目は、```Favorites``` クラスはnon-reifiableな型（Item28）を利用できない。つまり、```String``` や、```String[]``` を格納することはできるが、```List<String>``` を格納することはできない。これに関しては、満足いく回避策はない。

  上述の```Favorites``` クラスでは型に境界はなく、```getFavorite``` も```putFavorite``` もあらゆる型を受け入れていた。もし、受け入れる型に制限を加えたいのであれば、境界のある型パラメータ（Item30）や境界ワイルドカード（Item31）を使える。

  アノテーションAPI（Item39）では境界のある型パラメータの拡張的な使い方をしている。例として、実行時にアノテーションを読むメソッドを考える。このメソッドは```AnnotatedElement``` インターフェースにあり、クラス、メソッド、フィールドなどの要素を代表した、リフレクティブ型（reflective types）に実装される。（**リフレクティブ型？？**）

```java
public <T extends Annotation>
    T getAnnotation(Class<T> annotationType);
```
  引数である```annotationType``` はアノテーションの型を表すが、境界のある型変数が使われている。このメソッドは、引数で受け取った型のアノテーションがあればそれを返し、なければnullを返す。重要なのは、アノテーションを付与された要素は、キーがアノテーション型である、typesafe heterogeneous container であるということである。
  仮に```Class<?>```という型のオブジェクトを持っていたとして、引数に境界のある型パラメータを求めるようなメソッド、つまり、今回の```getAnnotation``` に渡すとする。その場合には、```Class<T extends Annotation>``` へのキャストをすると思うが、このキャストはコンパイル時にワーニングが出る（Item27）。
  このような時には、```asSubclass``` メソッドを用いる。このメソッドは、自身が引数に取った```Class``` オブジェクトのサブクラスであれば、自身の```Class``` オブジェクトを戻し、そうでなければ```ClassCastException``` をスローするというものである。
  結果、以下の実装となる。

```java
// Use of asSubclass to safely cast to a bounded type token
static Annotation getAnnotation(AnnotatedElement element, String annotationTypeName) {
    Class<?> annotationType = null; // Unbounded type token
    try {
        annotationType = Class.forName(annotationTypeName);
    } catch (Exception ex) {
        throw new IllegalArgumentException(ex);
    }
    return element.getAnnotation(annotationType.asSubclass(Annotation.class));
}
```

# 6章.ENUMとアノテーション

# 34.intの定数の代わりにenumを使うべし

* enumをいつ使えばよいか？→コンパイル時に明らかになっている定数のセットが必要な時はいつでも！
* constant-specific methodは馴染みがなくてしっくりこなかった。。以下の説明が分かりやすかった。

<http://d.hatena.ne.jp/hageyahhoo/20091115/1258258461>

# 35.ordinalよりもインスタンスフィールドの値を使うべし
* そもそもordinalメソッドはEnumSetやEnumMap用に使われるものであって、大半のプログラマは使わないものである。

# 36.bitフィールドの替わりにEnumSetを用いるべし
  enum型の要素が集合に適用される場合、昔はint enumパターン（Item34）を用いて、各定数に2の何乗かを振り分けていた。

```java
// Bit field enumeration constants - OBSOLETE!
public class Text {
    public static final int STYLE_BOLD          = 1 << 0;  // 1
    public static final int STYLE_ITALIC        = 1 << 1;  // 2
    public static final int STYLE_UNDERLINE     = 1 << 2;  // 4
    public static final int STYLE_STRIKETHROUGH = 1 << 3;  // 8
 // Parameter is bitwise OR of zero or more STYLE_ constants
    public void applyStyles(int styles) { ... }
}
```
これらにOR演算をかけることによって、いくつかの要素を集合にまとめていた。（bit field）

```java
text.applyStyles(STYLE_BOLD | STYLE_ITALIC);
```
bit演算によって、結合や交差も実現できるが、この方法はint enum　の悪い点をすべて引き継いでいる。

  定数の集合を作るにおいては、```EnumSet``` クラスを使うべき。性能はbit fieldで処理する場合と遜色ない。
  上記の例をenum、EnumSetを用いたのが以下。

```java
// EnumSet - a modern replacement for bit fields
public class Text {
    public enum Style { BOLD, ITALIC, UNDERLINE, STRIKETHROUGH }
 // Any Set could be passed in, but EnumSet is clearly best
    public void applyStyles(Set<Style> styles) { ... }
}
```
```EnumSet``` インスタンスを渡す、クライアント側のコードは以下のよう。

```java
text.applyStyles(EnumSet.of(Style.BOLD, Style.ITALIC));
```
  上記の```applyStyles``` メソッドでは、```EnumSet``` ではなく、```Set``` を引数に取っている。たいていのユーザは```EnumSet``` を渡すであろうが、引数として実装クラスを受け付けるのではなく、インターフェースを受け付けるべき（Item64）という原則にしたがってこうしている。

# 37. ordinalのかわりにEnumMapを使うべし

  ordinalメソッドをつかう（Item35）例として、以下のPlantクラスをもとに考えていく。

```java
class Plant {
    enum LifeCycle { ANNUAL, PERENNIAL, BIENNIAL }
 final String name;
    final LifeCycle lifeCycle;
     Plant(String name, LifeCycle lifeCycle) {
        this.name = name;
        this.lifeCycle = lifeCycle;
    }
 @Override public String toString() {
        return name;
    }
}
```
ここで、各ライフサイクルごとのPlantの配列を作成したいとする。そのために、ordinalを使って以下のようにやってしまうかもしれない。

```java
// Using ordinal() to index into an array - DON'T DO THIS!
Set<Plant>[] plantsByLifeCycle =
    (Set<Plant>[]) new Set[Plant.LifeCycle.values().length];
for (int i = 0; i < plantsByLifeCycle.length; i++)
    plantsByLifeCycle[i] = new HashSet<>();
 for (Plant p : garden)
    plantsByLifeCycle[p.lifeCycle.ordinal()].add(p);
 // Print the results
for (int i = 0; i < plantsByLifeCycle.length; i++) {
    System.out.printf("%s: %s%n",
        Plant.LifeCycle.values()[i], plantsByLifeCycle[i]);
}
```
ここでの一番の問題は、配列にアクセスしようとしたときに、enumのordinalで位置を決められた配列に対して、正しい整数値の選択をする必要があることである。もし間違った数字を選んだ場合には、運が良ければArrayIndexOutOfBoundsExceptionが起こるが、そうでない場合には、間違った選択をしたまま処理が進んでしまう。
  同じことを実現するのにもっと良い方法がある。ここでの配列はenumをキーにバリューを得るMapのような役割をしているので、実装もMapを使用したほうが良い。さらに、enumをキーにするMapとしての効率的な実装が、```EnumMap``` ではなされているので、これを使った例を以下で見ていく。

```java
// Using an EnumMap to associate data with an enum
Map<Plant.LifeCycle, Set<Plant>>  plantsByLifeCycle =
    new EnumMap<>(Plant.LifeCycle.class);
for (Plant.LifeCycle lc : Plant.LifeCycle.values())
    plantsByLifeCycle.put(lc, new HashSet<>());
for (Plant p : garden)
    plantsByLifeCycle.get(p.lifeCycle).add(p);
System.out.println(plantsByLifeCycle);
```
こちらの実装のほうが短く、見やすく、安全である。具体的には以下のメリットがある。
  * 型安全でないキャストがない
  * アウトプットの際にキーにラベルを付ける必要がない
  * 配列のインデックス計算由来のエラーがあり得ない
  * 内部で配列を使っているので、性能的にも遜色ない

また、EnumMapのコンストラクタではClassオブジェクトを引数に取っているが、これは境界付きの型であり、実行時のジェネリック型の情報を提供する（Item33）。
  前の例はストリーム（Item45）を使うとさらに短く、以下のようになる。

```java
// Naive stream-based approach - unlikely to produce an EnumMap!
System.out.println(Arrays.stream(garden)
        .collect(groupingBy(p -> p.lifeCycle)));
```
この実装の問題点は、EnumMapが使われておらず、パフォーマンスが使った場合より劣ってしまう。これを修正するためには、以下のように明示的に使うMapを示す。

```java
// Using a stream and an EnumMap to associate data with an enum
System.out.println(Arrays.stream(garden)
        .collect(groupingBy(p -> p.lifeCycle,
            () -> new EnumMap<>(LifeCycle.class), toSet())));
```
この最適化はMapを多用するときには重要になってくる。  

2つのenumを、ordinalの値を用いた配列の配列を用いた形で表すことがある。以下のソースコードはその例で、2つの状態間の変化について扱っている。

```java
public enum Phase {
    SOLID, LIQUID, GAS;
    public enum Transition {
        MELT, FREEZE, BOIL, CONDENSE, SUBLIME, DEPOSIT;
        // Rows indexed by from-ordinal, cols by to-ordinal
        private static final Transition[][] TRANSITIONS = { { null, MELT, SUBLIME }, { FREEZE, null, BOIL },
                { DEPOSIT, CONDENSE, null } };

        // Returns the phase transition from one phase to another
        public static Transition from(Phase from, Phase to) {
            return TRANSITIONS[from.ordinal()][to.ordinal()];
        }

    }
}
```
このプログラムには問題がある。コンパイラはordinal値と配列のインデックスの関係を知る由もなく、もし配列の作成に失敗したり、情報更新にともなう配列の更新を忘れていたら、実行時に失敗するか、```ArrayIndexOutOfBoundsException``` または、```NullPointerException``` が発生するか、誤った挙動をしたまま処理が進んでしまう。  
  上記のenumは、```EnumMap``` を使うことでもっとうまく書ける。

```java
// Using a nested EnumMap to associate data with enum pairs
public enum Phase {
    SOLID, LIQUID, GAS;
    public enum Transition {
        MELT(SOLID, LIQUID), FREEZE(LIQUID, SOLID), BOIL(LIQUID, GAS), CONDENSE(GAS, LIQUID), SUBLIME(SOLID,
                GAS), DEPOSIT(GAS, SOLID);
        private final Phase from;
        private final Phase to;

        Transition(Phase from, Phase to) {
            this.from = from;
            this.to = to;
        }

        // Initialize the phase transition map
        private static final Map<Phase, Map<Phase, Transition>> m = Stream.of(values())
                .collect(groupingBy(t -> t.from, () -> new EnumMap<>(Phase.class),
                        toMap(t -> t.to, t -> t, (x, y) -> y, () -> new EnumMap<>(Phase.class))));

        public static Transition from(Phase from, Phase to) {
            return m.get(from).get(to);
        }
    }
}
```
このコードは初期化部分が少し複雑である。toMap内の第三引数である```(x, y) -> y``` は使用されておらず、EnumMapを得るためだけに必要となっているものである。  
  いまここで、新たな状態である、plasma を定義したいとする。ここで追加される状態遷移の定義は、ionization と deionization である。配列ベースのenumで、この変更を取り入れようとしたら、新しく1つの定数を```Phase``` に追加し、2つの定数を```Phase.Transition``` に追加し、9つの要素があった2次元配列を16個の要素を持つように書き換える必要がある。一方、```EnumMap``` ベースのenumであれば、以下のように、新しく1つの定数を```Phase``` に追加し、2つの定数を```Phase.Transition``` に追加するのみでよい。

```java
// Adding a new phase using the nested EnumMap implementation
public enum Phase {
    SOLID, LIQUID, GAS, PLASMA;
     public enum Transition {
        MELT(SOLID, LIQUID), FREEZE(LIQUID, SOLID),
        BOIL(LIQUID, GAS),   CONDENSE(GAS, LIQUID),
        SUBLIME(SOLID, GAS), DEPOSIT(GAS, SOLID),
        IONIZE(GAS, PLASMA), DEIONIZE(PLASMA, GAS);
        ... // Remainder unchanged
    }
}
```
こちらのコードは人為的エラーが起こりえないし、EnumMapの内部では配列の配列を用いているので、性能的にも劣っているところはない。

# 38.拡張可能なenumをインターフェースで模倣すべし

  たいていの場合、列挙型を拡張するような考えはよくないことであるが、```operation code``` を書くときだけは切実に必要となる。  
  これをenumを使って実現する良い方法がある。enumはインターフェースを実装できるので、例えば以下のようにできる。

```java
// Emulated extensible enum using an interface
public interface Operation {
    double apply(double x, double y);
}

public enum BasicOperation implements Operation {
    PLUS("+") {
        public double apply(double x, double y) {
            return x + y;
        }
    },
    MINUS("-") {
        public double apply(double x, double y) {
            return x - y;
        }
    },
    TIMES("*") {
        public double apply(double x, double y) {
            return x * y;
        }
    },
    DIVIDE("/") {
        public double apply(double x, double y) {
            return x / y;
        }
    };
    private final String symbol;

    BasicOperation(String symbol) {
        this.symbol = symbol;
    }

    @Override
    public String toString() {
        return symbol;
    }
}
```
enum型は拡張不可であるが、インターフェースは拡張可能であり、オペレーションのAPIとして使われるのはインターフェースである。このインターフェースを使用して、以下のように新しくoperation codeを定義することもできる。

```java
// Emulated extension enum
public enum ExtendedOperation implements Operation {
    EXP("^") {
        public double apply(double x, double y) {
            return Math.pow(x, y);
        }
    },
    REMAINDER("%") {
        public double apply(double x, double y) {
            return x % y;
        }
    };
    private final String symbol;

    ExtendedOperation(String symbol) {

        this.symbol = symbol;
    }

    @Override
    public String toString() {
        return symbol;
    }
}
```
  基盤となるenumのインスタンスが期待されている場所であれば、拡張enumのインスタンスは使用できる。それだけでなく、基盤enumの全要素を渡すような場面でも、代わりに拡張enumの全要素を渡すことができる。以下のソースコードでは、引数に取った2つの値の```ExtendedOperation``` による全演算の結果を表示する。  

```java
public static void main(String[] args) {
    double x = Double.parseDouble(args[0]);
    double y = Double.parseDouble(args[1]);
    test(ExtendedOperation.class, x, y);
}

private static <T extends Enum<T> & Operation> void test(Class<T> opEnumType, double x, double y) {
    for (Operation op : opEnumType.getEnumConstants())
        System.out.printf("%f %s %f = %f%n", x, op, y, op.apply(x, y));

}
```
このコードにおいては、testメソッドの第一引数に```ExtendedOperation.class``` が取られている。これは境界付きの型トークン（Item33）である。
```<T extends Enum<T> & Operation>``` とあるが、これによってtestの第一引数に与えられるクラスは、enumであり、かつ、```Operation``` のサブクラスであることが保証される。
  境界付きワイルドカード型(Item31)を使って、以下のように記述することもできる。

```java
public static void main(String[] args) {
    double x = Double.parseDouble(args[0]);
    double y = Double.parseDouble(args[1]);
    test(Arrays.asList(ExtendedOperation.values()), x, y);
}
private static void test(Collection<? extends Operation> opSet, double x, double y) {
    for (Operation op : opSet) {
        System.out.printf("%f%s%f=%f%s", x, op, y, op.apply(x, y));
    }
}
```
このコードは少し簡潔で柔軟性が増しているが、```EnumSet``` （Item36）と```EnumMap``` （Item37）の使用はあきらめなければならない。
  上記2つのコードは、引数に4 2 を与えたら、以下のように出力する。

```
4.000000 ^ 2.000000 = 16.000000
4.000000 % 2.000000 = 0.000000
```
  
この拡張enumのマイナーな欠点は、オペレーションに紐づくシンボルを保存するコードと、検索するコードは```BasicOperation``` と```ExtendedOperation``` の双方で保持しなければならない点である。あまりに多くの共通機能が出てきた場合には、ヘルパークラスなどを用意して、コードの重複を除く必要がある。  
  この章で語られたパターンは```java.nio.file.LinkOption``` でも使われている。

# 39. 命名パターンよりアノテーションを選ぶべし

ツールやフレームワークが、**命名パターン**に応じて扱いを変えることが過去よくあった。例えば、バージョン4より前のJUnitでは、テストメソッドの名前は、testが先頭にくるようにせねばならない。この方法にはいくつか欠点がある。  
タイポをしてしまった場合には、暗黙のうちに失敗してしまう。例えば、testSafetyOverrideの代わりにtsetSafetyOverrideと打ってしまったとすると、JUnit3では、失敗とならないが、テストは実行されない。  
また、命名パターンが適切なプログラムの要素にのみ使用されているか保証するすべがない。
他にも、引数の値とプログラム要素を紐づける良い方法がないことが欠点である。  

アノテーションによってこれらの欠点は解消されている（JUnit4からはアノテーションが導入されている）。この章では、簡単なテスティングフレームワークを作って、どのようにアノテーションが動作するかを見ていく。
まず、自動で動き、エラーが送出されたら失敗とするアノテーションを見ていく。

```java
/**
 * Indicates that the annotated method is a test method.
 * Use only on parameterless static methods.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Test {
}
```
Testアノテーションの定義において、```@Retention``` と```@Target``` が付与されているが、これらはメタアノテーションと呼ばれる。
```@Retention(RetentionPolicy.RUNTIME)``` は、Testアノテーションは実行時に保持されるということを示している。
```@Target(ElementType.METHOD)``` は、Testアノテーションはメソッド宣言においてのみ有効（フィールドやクラスに適用できない）であるということを示している。
Testアノテーションの宣言のコメントに、「Use only on parameterless static methods」とあるが、これはアノテーションプロセッサーを書かない限りはコンパイラでは検知できない。さらに知りたい場合には```javax.annotation.processing``` のドキュメントを見るべし。
以下にTestアノテーションが実際どのように使われるのかを示した。

```java
// Program containing marker annotations
public class Sample {
    @Test public static void m1() { }  // Test should pass
    public static void m2() { }
    @Test public static void m3() {     // Test should fail
        throw new RuntimeException("Boom");
    }
    public static void m4() { }
    @Test public void m5() { } // INVALID USE: nonstatic method
    public static void m6() { }
    @Test public static void m7() {    // Test should fail
        throw new RuntimeException("Crash");
    }
    public static void m8() { }
}
```
Testアノテーションは、引数がなく、単に要素にマークを付けるだけであるので、**マーカーアノテーション**と呼ばれる。もし、Testのタイポをしたり、Testアノテーションをメソッド宣言以外に使用したら、コンパイルエラーが発生する。
```Sample``` クラスのうち、m1は成功、m3、m7は失敗、m5はstaticなメソッドでないので不正、そのほか4つのメソッドはTestアノテーションが付与されていないので、テスティングフレームワークからは無視される。
Testアノテーションは```Sample```クラスのsemanticsに直接影響を与えず、Testアノテーションを利用するプログラムにのみ情報を与える。
つまり、アノテーションは付与されたコードのsemanticsには影響を与えず、以下のサンプルテストランナーのようなツールの処理に影響を与える。

```java
package tryAny.effectiveJava;

//Program to process marker annotations
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class RunTests {
    public static void main(String[] args) throws Exception {
        int tests = 0;
        int passed = 0;
        Class<?> testClass = Class.forName(args[0]);
        for (Method m : testClass.getDeclaredMethods()) {
            if (m.isAnnotationPresent(Test.class)) {
                tests++;
                try {
                    m.invoke(null);
                    passed++;
                } catch (InvocationTargetException wrappedExc) {
                    Throwable exc = wrappedExc.getCause();
                    System.out.println(m + " failed: " + exc);
                } catch (Exception exc) {
                    System.out.println("Invalid @Test: " + m);
                }
            }
        }
        System.out.printf("Passed: %d, Failed: %d%n", passed, tests - passed);
    }

}
```
テストランナーツールはFQDNを引数に取り、```Method.invoke``` の呼び出しでTestアノテーションが付与されたメソッドを実行する。testメソッドが例外を投げた場合、リフレクションファシリティがその例外をラップして、```InvocationTargetException``` を投げる。本ツールではこの例外をキャッチして、原因となる例外を```getCause```メソッドで得ている。
2番目のcatch節ではTestアノテーションの不正使用による例外を捕捉し、適切なメッセージをプリントアウトしている。```Sample``` クラスをテストツールにかけた時のアウトプットは以下のよう。

```
public static void tryAny.effectiveJava.Sample.m3() failed: java.lang.RuntimeException: Boom
Invalid @Test: public void tryAny.effectiveJava.Sample.m5()
public static void tryAny.effectiveJava.Sample.m7() failed: java.lang.RuntimeException: Crash
Passed: 1, Failed: 3
```
ここで、特定の例外がスローされた場合には成功とする新しいアノテーションを作成してみる。

```java
package tryAny.effectiveJava;

//Annotation type with a parameter
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 *  * Indicates that the annotated method is a test method that  * must throw
 * the designated exception to succeed.  
 */

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface ExceptionTest {
    Class<? extends Throwable> value();
}
```
このアノテーションの引数には```Class<? extends Throwable>```という境界付き型トークン（Item33）が用いられており、```Throwable```を継承したクラスが引数に取れる、ということを意味する。以下が使用の具体例となる。

```java
package tryAny.effectiveJava;

//Program containing annotations with a parameter
public class Sample2 {
    @ExceptionTest(ArithmeticException.class)
    public static void m1() { // Test should pass
        int i = 0;

        i = i / i;
    }

    @ExceptionTest(ArithmeticException.class)
    public static void m2() { // Should fail (wrong exception)
        int[] a = new int[0];
        int i = a[1];
    }

    @ExceptionTest(ArithmeticException.class)
    public static void m3() {
    } // Should fail (no exception)
}
```
また、テストランナーツールをこれに合わせて、以下のように改修する。

```java
package tryAny.effectiveJava;

//Program to process marker annotations
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class RunTests {
    public static void main(String[] args) throws Exception {
        int tests = 0;
        int passed = 0;
        Class<?> testClass = Class.forName(args[0]);
        for (Method m : testClass.getDeclaredMethods()) {
            if (m.isAnnotationPresent(Test.class)) {
                tests++;
                try {
                    m.invoke(null);
                    passed++;
                } catch (InvocationTargetException wrappedExc) {
                    Throwable exc = wrappedExc.getCause();
                    System.out.println(m + " failed: " + exc);
                } catch (Exception exc) {
                    System.out.println("Invalid @Test: " + m);
                }
            }

            if (m.isAnnotationPresent(ExceptionTest.class)) {
                tests++;
                try {
                    m.invoke(null);
                    System.out.printf("Test %s failed: no exception%n", m);
                } catch (InvocationTargetException wrappedEx) {
                    Throwable exc = wrappedEx.getCause();
                    Class<? extends Throwable> excType = m.getAnnotation(ExceptionTest.class).value();
                    if (excType.isInstance(exc)) {
                        passed++;
                    } else {
                        System.out.printf("Test %s failed: expected %s, got %s%n", m, excType.getName(), exc);
                    }
                } catch (Exception exc) {
                    System.out.println("Invalid @Test: " + m);
                }
            }

        }

        System.out.printf("Passed: %d, Failed: %d%n", passed, tests - passed);
    }

}
```
このコードでは```ExceptionTest```アノテーションの引数を抽出し、発生した例外がその型と同じかをチェックしている。
テストプログラムがコンパイルされるということは、アノテーションの引数として指定された例外の型が有効なものであると示している。ただし、コンパイル時にはあった特定の例外の型が実行時にはない場合、テストランナーは```TypeNotPresentException```をスローする。

この例外テストのコードをさらに改良し、指定した複数の例外のうちのいずれかがスローされるかをテストできるようにする。
この改良は容易に行うことができて、```ExceptionTest```の引数の型を配列にすればよい。

```java
// Annotation type with an array parameter
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface ExceptionTest {
    Class<? extends Exception>[] value();
}
```
これでExceptionTestアノテーションには1つの引数でも複数の引数でも取れるようになる。
複数例外を記述する場合は以下のようになる。

```java
// Code containing an annotation with an array parameter
@ExceptionTest({ IndexOutOfBoundsException.class,
                 NullPointerException.class })
public static void doublyBad() {
    List<String> list = new ArrayList<>();
 // The spec permits this method to throw either
    // IndexOutOfBoundsException or NullPointerException
    list.addAll(5, null);
}
```
```ExceptionTest``` を新しくしたことによって、テストランナーツールは以下のようになる。

```java
package tryAny.effectiveJava;

//Program to process marker annotations
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class RunTests {
    public static void main(String[] args) throws Exception {
        int tests = 0;
        int passed = 0;
        Class<?> testClass = Class.forName(args[0]);
        for (Method m : testClass.getDeclaredMethods()) {
            if (m.isAnnotationPresent(Test.class)) {
                tests++;
                try {
                    m.invoke(null);
                    passed++;
                } catch (InvocationTargetException wrappedExc) {
                    Throwable exc = wrappedExc.getCause();
                    System.out.println(m + " failed: " + exc);
                } catch (Exception exc) {
                    System.out.println("Invalid @Test: " + m);
                }
            }

            if (m.isAnnotationPresent(ExceptionTest.class)) {
                tests++;
                try {
                    m.invoke(null);
                    System.out.printf("Test %s failed: no exception%n", m);
                } catch (InvocationTargetException wrappedEx) {
                    Throwable exc = wrappedEx.getCause();
                    int oldPasses = passed;
                    Class<? extends Throwable>[] excTypes = m.getAnnotation(ExceptionTest.class).value();
                    for (Class<? extends Throwable> excType : excTypes) {
                        if (excType.isInstance(exc)) {
                            passed++;
                            break;
                        }
                    }
                    if (passed == oldPasses) {
                        System.out.printf("Test %s failed: %s%n", m, exc);
                    }
                } catch (Exception exc) {
                    System.out.println("Invalid @Test: " + m);
                }
            }

        }

        System.out.printf("Passed: %d, Failed: %d%n", passed, tests - passed);
    }

}
```

Java8では、複数の引数をとるアノテーションを別の方法で実現できる。アノテーションを配列引数で宣言する代わりに、```@Repeatable```メタアノテーションを使って、一つの要素に対して複数回アノテーション付与ができるようにする。
この```@Repeatable```メタアノテーションは、1つの引数をとる。その引数は、containing anotation typeと呼ばれる1つの配列を引数に持つクラスオブジェクトである。




# 7章.ラムダとストリーム

# 42.匿名クラスより、ラムダ式を選択すべし

* より簡潔明瞭に書けるという理由から、匿名クラスよりもラムダ式を用いるべき。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class AnonymouseVsLambda {
    public static void main(String[] args) {
        List<String> words1 = Arrays.asList("apple", "pen", "pineapple");
        // 匿名クラスで書く。
        Collections.sort(words1, new Comparator<String>() {
            public int compare(String s1, String s2) {
                return Integer.compare(s1.length(), s2.length());
            }
        });
        System.out.println(words1);

        // 型をRawにするとコンパイルエラーとなる。
        List<String> words2 = Arrays.asList("banana", "grape", "melon");
        // ラムダ式で書く。
        Collections.sort(words2, (s1, s2) -> Integer.compare(s1.length(), s2.length()));
        System.out.println(words2);
    }
}
```

* ラムダ式での型は、書くことによってコードが綺麗にならない限り、省略してよい。
* クラスやメソッドと違って、ラムダ式には名前もドキュメントもないので、自明な処理でなかったり、4行以上となる処理はラムダ式で記述すべきでない。
* 匿名クラスが必要となる場面は以下。
  * ラムダ式は関数型インターフェースのインスタンスにしか代入できないので、複数のメソッドを持つインターフェースや、抽象クラスのインスタンスが必要となる場合は匿名クラスを使う
  * ラムダ式でのthisはエンクロージングクラス（外側のクラス）を指すが、匿名クラスでは匿名クラス自身を指すので、関数オブジェクト自身へのアクセスが必要な場合には、匿名クラスを使う

# 43.ラムダ式よりメソッド参照を使うべし

* 基本的にラムダ式よりメソッド参照の方が簡潔に書けるため、メソッド参照を選択するべき。
* ラムダ式の方が簡潔に書ける場合もある。よくあるのは、同クラスにあるメソッドを用いる場合。

```java
// メソッド参照
service.execute(GoshThisClassNameIsHumongous::action);
// ラムダ式
service.execute(() -> action());
```

* 多くのメソッド参照はstaticメソッドの参照であるが、他にも4つのパターンがある。
  * Bound 参照（訳が分からない。。）はメソッド参照において、受け取るオブジェクトが特定される。
  * UnBound 参照（訳が分からない。。）は関数オブジェクトを適用するときに、受け取るオブジェクトが特定される（**意味がよくわからない**）。streamのmapやfilterでよく使われる。
  * クラス、配列のコンストラクタについては以下の表のようにできる。


| Method Ref Type | Example | Lambda Equivalent |
|:-------|:-------|:-------|
| Static       | Integer::parseInt | str -> Integer.parseInt(str)
| Bound |Instant.now()::isAfter | Instant then = Instant.now(); t -> then.isAfter(t) |
| Unbound | String::toLowerCase | str -> str.toLowerCase() |
| Class Constructor | TreeMap<K,V>::new | () -> new TreeMap<K,V> |
| Array Constructor | int[]::new | len -> new int[len]

# 44.標準の関数型インターフェースを使うべし
* 標準で用意されているものを使うことによって、使いやすさが増し、すでに組み込まれている様々なメソッドの恩恵にあずかれる。
* java.util.functionに含まれる関数型インターフェースは43個ある。
  * 中心的なのはUnaryOperator< T >、BinaryOperator< T >、Predicate< T >,Function< T >,Consumer< T >,Supplier< T >の6つ。(6)
  * 上の6つそれぞれにint、long、doubleのプリミティブ型を扱うための関数型インターフェースがある。（18）
  * Functionには*Src*To*Result*Functionで6つ。*Src*ToObjFucntionで3つある。(9)
  * 引数を2つ取るものが9つある。(9)
  * BooleanSupplierなるものがある。(1)
* プリミティブ型に対応していない関数型インターフェースでプリミティブ型をボクシングしたオブジェクトを使ってはならない。性能が悪くなる。
* 自身で関数型インターフェースを書く必要があるのは以下の場合。
  * 引数を3つ取る関数型インターフェースなど標準で用意されていないものが必要となる場合。
  * 一般的に使われていて記述から恩恵を受けれらる、強い関連性をもった契約がある（**よくわからん**）、defaultメソッドから恩恵が受けられる、といった特徴がある場合。
* 関数型インターフェースを書く際には、必ず@FunctionalInterfaceをつける。これがあれば、誤った書き方をしていた場合にコンパイルエラーにしてくれる。
* 関数型インターフェースを引数に取るメソッドはオーバーライドすべきでない。（Item52）

# 45.Streamは気を付けて使うべし
* Streamパイプラインの処理は終端処理が呼ばれて初めて実行される。
* 簡単に並列Streamにすることができるが、おおむね並列にするのは適切でない。（Item48）
* いつStreamを使うべきかにかっちりしたルールはない。ヒューリスティックな解があるのみ。
* 指定したファイルに含まれる単語（例1）、行（例2,3）について、アナグラム毎にまとめ、指定した数以上の単語があるアナグラムを表示するプログラムが以下。
例2はstream処理を使いすぎて読みづらくなっている。例3が適切な使い方。
下の例のラムダ式内のgなどは本当はgroupとして、読みやすさを向上させるべき。
alphabetize のようなヘルパーメソッドを作ることは、ストリーム処理を書くにおいて、読みやすさを向上させるために重要なことである。

```java
package tryAny.effectiveJava;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Anagrams {
    public static void main(String[] args) throws IOException {
        File dictionary = new File("/application/gradle/getting-started.html");
        int minGroupSize = 2;

        Map<String, Set<String>> groups = new HashMap<>();

        // 例1 start
        try (Scanner s = new Scanner(dictionary)) {
            while (s.hasNext()) {
                String word = s.next();
                groups.computeIfAbsent(alphabetize(word), (unused) -> new TreeSet<>()).add(word);
            }
        }
        for (Set<String> group : groups.values()) {
            if (group.size() >= minGroupSize) {
                System.out.println(group.size() + ":" + group);
            }
        }
        // 例1 end

        // 例2 start(こっちは一行毎でアナグラム取っているから例1と結果違う)
        Path dictionary2 = Paths.get("/application/gradle/getting-started.html");
        try (Stream<String> words = Files.lines(dictionary2)) {
            words.collect(Collectors.groupingBy(word -> word.chars().sorted()
                    .collect(StringBuilder::new, (sb, c) -> sb.append((char) c), StringBuilder::append).toString()))
                    .values().stream().filter(group -> group.size() >= minGroupSize)
                    .map(group -> group.size() + ":" + group).forEach(System.out::println);
        }
        // 例2 end

        // 例3 start（例2と同じ結果）
        try (Stream<String> words = Files.lines(dictionary2)) {
            words.collect(Collectors.groupingBy(word -> alphabetize(word)))
            .values().stream()
                    .filter(group -> group.size() >= minGroupSize)
                    .forEach(g -> System.out.println(g.size() + ":" + g));
        }
        // 例3 end
    }

    private static String alphabetize(String s) {
        char[] a = s.toCharArray();
        Arrays.sort(a);
        return new String(a);
    }
}
```

* 以下の例のように、char型のstream処理は直感的でない動きをしうるので、原則としてchar型の値をstream処理で扱うべきでない。

```java
package tryAny.effectiveJava;

public class CharStream {
    public static void main(String[] args) {
        "Hello, world!".chars().forEach(System.out::print);
        // 72101108108111443211911111410810033 が表示

        System.out.println();

        "Hello, world!".chars().forEach(x -> System.out.print((char) x));
        // Hello, world! が表示
    }
}
```

* 既存のforループをstreamに置き換えるにおいては、やる意味があるときのみやるべき。
* 関数型オブジェクトを使用したstream処理ではできないが、code block（**普通の繰り返し文のこと?**）ではできることが以下。
  * ラムダ式ではローカル変数について、実質finalなものしか読み取れないが、code blockでは、どんなものでも読めるし変更もできる。
  * code block では enclosing methodからリターンすることができ（**どういうこと？**）、ループからbreakやcontinueの操作ができ、宣言している検査例外をスローすることができるが、ラムダ式では以上のことはできない。

* streamで簡単にできるようになることは以下。
  * 画一的な要素の変換
  * 要素のフィルタリング処理
  * 単一のオペレーションで要素を結びつける処理（加えたり、最小値を出したり）
  * 要素をcollectionに集約する処理（ある属性でグルーピングするなど）
  * 特定の基準を満たす要素を探す処理
* パイプライン上の別のステージにある要素を同時に扱うような処理は、streamでは困難。
以下の例では、Mersenne素数というものを出力している。
Mersenne素数はpが素数であったときに、2^p-1で表される数で、必ず素数になるものである。
stream処理で、
素数→Mersenne素数→20個で区切る→表示
としているが、表示する部分では、元となった素数にアクセスすることはできない（今回は結果から逆算することができたが）。

```java
package tryAny.effectiveJava;

import static java.math.BigInteger.*;

import java.math.BigInteger;
import java.util.stream.Stream;

public class MersennePrimes {
    public static void main(String[] args) {
        primes().map(p -> TWO.pow(p.intValueExact()).subtract(ONE)).filter(mersenne -> mersenne.isProbablePrime(50))
                .limit(20)
                // .forEach(System.out::println);
                .forEach(mp -> System.out.println(mp.bitLength() + ":" + mp));
    }

    static Stream<BigInteger> primes() {
        return Stream.iterate(TWO, BigInteger::nextProbablePrime);
    }
}
```

* streamを使うべきか、繰り返し処理をすべきか迷う処理はたくさんある。迷った場合には、両方試してみてどちらが良いか判断してみるべき。

# 8章.メソッド

# 49.引数のバリデーションチェックをすべし
* 引数のバリデーションチェックをすることなく、誤った引数の値が先の処理にわたった場合、直接的な原因が分かりにくいエラーが出たり、最悪の場合、エラーにはならないが、誤った処理がなされることがある。
* 引数の制限はJavadocに書くべき。
* Nullチェックに際して、Java7からは Objects.requireNonNull でできるようになった。
* rangeのチェックに際しては、Java9からは Objects の checkFromIndexSize, checkFromToIndex, checkIndex が使えるようになった。（closed rangeには使えない）
* 外に公開しない、ヘルパーメソッドにおける引数チェックではアサーションを用いるべき。通常のバリデーションと異なり、影響がなく、javaコマンドに-aeをつけない限りコストもかからない。（**理由がピンとこない**）

```java
// Private helper function for a recursive sort
private static void sort(long a[], int offset, int length) {
    assert a != null;
    assert offset >= 0 && offset <= a.length;
    assert length >= 0 && length <= a.length - offset;
    ... // Do the computation
}
```

* メソッドで使う引数でなく、後々の利用のために溜めておく引数は特にバリデーションチェックすることが重要（コンストラクタとかの話）。そこで誤った値を落としておかないと、後の処理でエラーになったときにデバッグが難しいため。
* バリデーションチェックを明示的にすべきでないときもあって、それは、バリデーションチェックのコストが高く、非現実的で、かつ、チェックが処理の中に内包されているとき。例えば、Collections.sort(List)において、Listに内包される値は互いに比較可能なものでなければならないが、それはキャストするときにチェックされる。
* 内包的チェックがなされた時に、出力されたエラーが適切なものでない場合には、適切なエラーへの変換処理を行う。
* ここでの指南は、引数の恣意的な制限が良いというわけではなく、メソッドの設計をより汎用的なものに対応できるようにすることを目指すべきであり、制限は少ないほうがよい。

# 50.必要に応じて防御的コピー（defensive copies）を作るべし
* JavaはCやC++のようなメモリに手を加えて起こる脆弱性（バッファオーバラン等）がない、という意味で安全な言語であるが、自分でクラスを実装するにあたっては、攻撃者が不変条件（invariant）を破ってくる、というつもりで実装をすべき。
* 以下のクラスは一見immutableに見える。

```java
// Broken "immutable" time period class
public final class Period {
    private final Date start;
    private final Date end;
 /**
     * @param  start the beginning of the period
     * @param  end the end of the period; must not precede start
     * @throws IllegalArgumentException if start is after end
     * @throws NullPointerException if start or end is null
     */
    public Period(Date start, Date end) {
        if (start.compareTo(end) > 0)
            throw new IllegalArgumentException(
                start + " after " + end);
        this.start = start;
        this.end   = end;
    }
    public Date start() {
        return start;
    }
    public Date end() {
        return end;
    }
 ...    // Remainder omitted
}
```
* しかし、Dateクラスはmutableなので、以下のように簡単に、「startはend以後にはならない」という条件を破れる。

```java
// Attack the internals of a Period instance
Date start = new Date();
Date end = new Date();
Period p = new Period(start, end);
end.setYear(78);  // Modifies internals of p!
```

* 日付のクラスに関しては、Dateはもはや時代遅れであり、Java8以降は Instant クラス等を使うべきである。
* mutable な引数を持つコンストラクタに defensive　copy を使用して、脆弱性をなくす。defensive copyを使って上のコードのコンストラクタを書き直すと以下のようになる。

```java
// Repaired constructor - makes defensive copies of parameters
public Period(Date start, Date end) {
    this.start = new Date(start.getTime());
    this.end   = new Date(end.getTime());
 if (this.start.compareTo(this.end) > 0)
      throw new IllegalArgumentException(
        this.start + " after " + this.end);
}
```
* defensive copy を採用した際の引数のバリデーションチェックは、引数で渡ってきたオリジナルのものではなく、コピー側に対して行う。これは、バリデーションチェックを行ってから、コピーを行うまでの間に、別スレッドから攻撃を受ける可能性（TOCTOUというらしい）を考慮してのことである。
* 引数で受けるオブジェクトがfinalでない、つまり、継承が可能であるクラスである場合は、defensive copy の作成に当たって、cloneを用いてはならない。なぜなら、受け取った引数が悪意のあるサブクラスである可能性があるため。
* アクセサを用いて、不変条件を壊すことも可能。

```java
// Second attack on the internals of a Period instance
Date start = new Date();
Date end = new Date();
Period p = new Period(start, end);
p.end().setYear(78);  // Modifies internals of p!
```
* 上の攻撃を防ぐため、アクセサにおいてもdefensive copyを作って対応する。

```java
// Repaired accessors - make defensive copies of internal fields
public Date start() {
    return new Date(start.getTime());
}
 public Date end() {
    return new Date(end.getTime());
}
```
* その他のdefensive copyの用途として、フィールドの配列変数をクライアントに返す際に用いる。配列は必ず mutable なので、このような対応を取る必要がある。（Item15でも言及）
* そもそもmutableなものをクライアントに返す設計にしないようにすべきである。
* defensive copyのコストがとても高く、かつ、クラスの利用者が不適切にmutableなフィールドを変更ないと確信できる場合は、defensive copyの代わりに、ドキュメントで注意を書く。

# 51.メソッドのシグニチャは注意深く設計せよ
* メソッドの名前は注意深く決めるべき。理解しやすく、同パッケージ内の他の名前と矛盾しないようにする。また、広く一般的に合意を得ている名前を付ける。迷ったらガイダンスとして、JavaライブラリAPIを見てみる（良くないのもあるが、良いのがたくさんある）。
* 便利なメソッドを過度に提供すべきでない。あまりに多いメソッドがあると、学習、利用、ドキュメント作成、テスト、保守が大変になる。頻繁に使われる場合にのみ、記述の省略化ができるようなメソッドの提供を考慮すべき。迷ったら作らないほうが良い。
* 引数の数を多くとるべきでない。引数の数は4つ以下に抑えるべきである。利用者は多くの引数を覚えることができないので、リファレンスをみながら使用しなければならない。特に、同じ型で多くの引数がある場合は避けたい。なぜなら、引数の順番を間違えたとしても、コンパイルエラーとならず、意図したものと違う処理がなされる可能性があるから。引数の数を減らすテクニックは以下の3つ。
   * 1つのメソッドを複数のメソッドに分割する。（**Listのsublist、indexOf、lastIndexOfの例をあげていたがいまいちわからず**）
   * ヘルパークラスを作る。例えば、トランプの柄と数を引数に取るものがあるならば、柄と数をまとめたEntityを作成し、それを引数に取るようにする。
   * ビルダーパターンを使う。（Item2）
* 引数の型は具象クラスよりもインターフェースに優先すべき。具象クラスにした場合には、メソッドの使用者に特定の実装を強いることになり、時にはコストの高いコピーを強いるときがある。
* boolean 引数よりも、2値のenumとすべき。なぜなら、enumの方は後に拡張することが容易であるから（要素を2つから3つにする）。また、enumはその中にメソッドを持つこともできる。（Item34）

# 52.オーバーロードは気を付けて使うべし
* オーバーロードはコンパイル時に呼び出すメソッドが決められる。

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class OverloadTest {
    public static String classify(Set<?> s) {
        return "Set";
    }

    public static String classify(List<?> s) {
        return "List";
    }

    public static String classify(Collection<?> s) {
        return "Collection";
    }

    public static void main(String[] args) {
        Collection<?>[] collections = { new HashSet<String>(), new ArrayList<String>(),
                new HashMap<String, String>().values() };

        for (Collection<?> c : collections) {
            System.out.println(classify(c));
        }
        /**
         * Collection <br>
         * Collection <br>
         * Collection
         */
    }
}
```

* 一方、オーバーライドはコンパイル時ではなく、実行時に決められる。

```java
package tryAny.effectiveJava;

import java.util.List;

public class OverrideTest {
    public static void main(String[] args) {
        List<Wine> l = List.of(new Wine(), new SparklingWine(), new Champagne());

        for (Wine w : l) {
            System.out.println(w.name());
            /**
             * wine<br>
             * sparkling wine<br>
             * champagne
             */
        }
    }
}

class Wine {
    String name() {
        return "wine";
    }
}

class SparklingWine extends Wine {
    @Override
    String name() {
        return "sparkling wine";
    }
}

class Champagne extends SparklingWine {
    @Override
    String name() {
        return "champagne";
    }
}
```

* 混乱を招くようなオーバーロードの使用は避ける。混乱を招くオーバーロードとは何か、ということについては議論の余地があるが、同じ引数の数で、オーバーロードさせるメソッドは作るべきでない、という意見は受け入れられている。
* 同じ引数の数でオーバーロードしたくなったら、違うメソッド名でメソッドを作るべきである。ObjectOutputStream は全てのprimitive型の書き込みメソッドを持っているが、それぞれ writeBoolean、writeInt等、writeをオーバーライドしたりせず、別のメソッドを作っている。
* コンストラクタの場合は、別の名称にすることはできないので、同じ数の引数で複数のコンストラクタを用意することがあるかもしれない。そういった場合に取る引数は、互いに根本的に異なる（radically different）のであれば比較的安全である（キャストできないような関係）。
* Java5になる前は、primitive型と全ての参照型は根本的に異なるものであったが、autoboxingが出現したことによってその前提が覆された。以下のコードでは、直感的には、 [-3, -2, -1] [-3, -2, -1]が表示されそうだが、Listのremoveには、int を引数に取るremoveメソッドがオーバライドされているため、実際には、[-3, -2, -1] [-2, 0, 2]となる。

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class SetList {
    public static void main(String[] args) {
        Set<Integer> s = new TreeSet<>();
        List<Integer> l = new ArrayList<>();

        for (int i = -3; i < 3; i++) {
            s.add(i);
            l.add(i);
        }

        for (int i = 0; i < 3; i++) {
            s.remove(i);
            l.remove(i);
        }

        System.out.println(s + "" + l);// [-3, -2, -1] [-2, 0, 2]
    }
}
```

* 以下のコードは、```exec.submit(System.out::println);```の部分でコンパイルエラーになる。このsubmitメソッドは、```submit(Runnable task);```と```submit(Callable<T> task);```でオーバーロードされており、コンパイラがどちらを使うか判断できないようになる（**判断できない理屈は難しくてわからず。```System.out::println```は inexact method referenceであるとかなんとか**）。とにかく、混乱を避けるためにも、同じ引数の位置で異なるfunctional interface でオーバーロードするのは避けるようにするべき。

```java
package tryAny.effectiveJava;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Snippet {
    public static void main(String[] args) {
        new Thread(System.out::println).start();
        ExecutorService exec = Executors.newCachedThreadPool();
        exec.submit(System.out::println); //コンパイルエラー

    }
}
```

* 以前作成したコードの修正等でやむを得ずオーバーロードせねばならない場合には、同じ動作をするよう保証して作る。

```java
// Ensuring that 2 methods have identical behavior by forwarding
public boolean contentEquals(StringBuffer sb) {
    return contentEquals((CharSequence) sb);
}
```

# 53.可変長引数は気を付けて使うべし
* 0個以上の引数を取る場合に、個数のチェック等が入って美しくない作りになるときがある。そういった場合は、取るべき引数を、以下のように2つに分解してやる。

```java
package tryAny.effectiveJava;

public class Varargs {
    public static void main(String[] args) {
        System.out.println(min1(99));
        System.out.println(min2(1, 2, 3));

    }

    // ugly
    static int min1(int... args) {
        if (args.length == 0)
            throw new IllegalArgumentException("Too few arguments");
        int min = args[0];
        for (int i = 1; i < args.length; i++)
            if (args[i] < min)
                min = args[i];
        return min;
    }

    // better
    static int min2(int firstArg, int... remainingArgs) {
        int min = firstArg;
        for (int arg : remainingArgs) {
            if (arg < min) {
                min = arg;
            }
        }
        return min;
    }
}
```

* 可変長引数を用いる場合には、配列のメモリ割り当てと初期化が必要となり、コストがかかる。もし、コストを減らす必要があり、引数の個数が3つ以下の場合が大多数であるとわかっている場合には、あらかじめ引数が0,1,2,3個の場合を作って対応するのがよい。

```java
public void foo() { }
public void foo(int a1) { }
public void foo(int a1, int a2) { }
public void foo(int a1, int a2, int a3) { }
public void foo(int a1, int a2, int a3, int... rest) { }
```

# 54.nullではなく、空のコレクション、配列を返すべし
* nullを返すとなると、呼び出し側でnullをチェックするためのコードが必要となり、煩わしい。空のコレクション、配列を返すべきである。

```java
//The right way to return a possibly empty collection
public List<Cheese> getCheeses() {
    return new ArrayList<>(cheesesInStock);
}
```

```java
//The right way to return a possibly empty array
public Cheese[] getCheeses() {
    return cheesesInStock.toArray(new Cheese[0]);
}
```

* 空のコレクション、配列を返すよりnullを返すほうが、メモリ割り当てがない分性能が良くなるという意見がある。これは以下2点で誤っている。
  * このレベルで性能が良くなるかは疑わしい。証明できている場合を除いたら、心配する必要はない。
  * メモリ割り当てをすることなく空のコレクション、配列を返すことは可能である。

```java
// Optimization - avoids allocating empty collections
public List<Cheese> getCheeses() {
    return cheesesInStock.isEmpty() ? Collections.emptyList()
        : new ArrayList<>(cheesesInStock);
}
```

```java
// Optimization - avoids allocating empty arrays
private static final Cheese[] EMPTY_CHEESE_ARRAY = new Cheese[0];
public Cheese[] getCheeses() {
    return cheesesInStock.toArray(EMPTY_CHEESE_ARRAY);
}
```

# 55.Optional を返す時は気を付けるべし
* 特定の条件下では値を返せないメソッドを考慮する際に、Java7以前では、exceptionをスローするか、nullを返すしかなかった。Java8からは、Optionalを返すという選択肢が生まれた。

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Optional;

public class OptionalTest {
    public static void main(String[] args) {
        List<String> l1 = Arrays.asList("paper", "strong", "java", "pepper");
        List<String> l2 = new ArrayList<>();

        System.out.println(max(l1).get());
        System.out.println(max(l2).orElse("no words"));
        try {
            max(l2).orElseThrow();
        } catch (NoSuchElementException e) {
            System.out.println(e.getMessage());
        }

        System.out.println(max(l1).filter(str -> str.length() == 6).map(str -> str.toUpperCase()).get());
    }

    public static <E extends Comparable<E>> Optional<E> max(Collection<E> c) {
        if (c.isEmpty()) {
            return Optional.empty();
        }

        E result = null;
        for (E ele : c) {
            if (result == null || ele.compareTo(result) > 0) {
                result = Objects.requireNonNull(ele);
            }
        }

        return Optional.of(result);
    }
}
```

* Optionalが戻り値であるメソッドからnullを返してはならない。これを行うと、Optionalを導入した意味がなくなる。
* nullを返したり、例外をスローする代わりに、Optionalを返すかを選択するにあたっては、検査例外をスローするか否かを決めるのと同じ考え（Item71）で選択する。
* コレクション、マップ、ストリーム、配列、Optionalといった何かを格納するものに対して、Optionalでラップすべきではない。例えば、Optional<List<T>>を返すよりは、空のList<T>を返すほうが良い。空のList<T>を返せるのであれば、そもそもOptionalを返す必要がないからである。
* メソッドの戻り値として、Optionalでラップした値を選択すべき時は、結果を返すことができない可能性があり、かつ、結果がnullである場合にメソッド呼び出し側で特別な考慮が必要な場合である。
* int,double,longのラッパークラスのOptionalを返してはならない。OptionalInt,OptionalDouble,OptionalLongが用意されているのでそちらを使う。
* コレクション、配列のキー、バリュー、要素としてOptionalを使ってはならない。
* インスタンスの必須ではないフィールド値として、Optionalを使用することはあり得る。（Item2で扱ったクラス参照）

# 56.公開するAPIの全ての要素にJavadocコメントを書くべし
* Javadocの書き方については、How to Write Doc CommentsというJava4がリリースされて以来更新されていないWebページで、いまだに価値のある情報が提供されている。Java9で```@index```、Java8では```@implSpec```、Java5では```@literal```と```@code```、という重要なタグが追加された。
<http://www.oracle.com/technetwork/java/javase/tech/index-137868.html>
* 公開する全てのクラス、インターフェース、コンストラクタ、メソッド、フィールドにJavadocコメントを書く必要がある（公開しないものについても書くべきであるが、公開するものはマスト）。publicなクラスでは、コメントが書けないのを避けるため、デフォルトコンストラクタの使用は避けるべき。
* メソッドのJavadocコメントには、メソッドと使用者の間の決まり事を簡潔に記すべき。継承を見越した設計は別として（Item19）、一般に、Javadocコメントにはどのように役割を果たすかではなく、どんな役割を果たすかを書く。
また、コメントには、利用前の条件、利用後の状態を書く。```@throws```タグで、前提条件を破るとこの例外が出る、と示すことで利用前の条件を暗に示し、```@tag```タグで、メソッド呼び出し後の引数の状態を示すことで利用後の状況を書くのが典型的なパターンである。
加えて、メソッド呼び出しで起こる副作用も記述する。例えば、メソッド呼び出しをするとバックグラウンドでスレッドが立ち、処理が流れる、など。
メソッドの決まりごとを十分に記述するために、@param、@return、@throwsを書くようにする。
慣例として、@param、@returnには名詞句を記述する。@throwsはifから始まるような言葉で構成する。

```java
/**
 * Returns the element at the specified position in this list.
 *
 * <p>This method is <i>not</i> guaranteed to run in constant
 * time. In some implementations it may run in time proportional
 * to the element position.
 *
 * @param  index index of element to return; must be
 *         non-negative and less than the size of this list
 * @return the element at the specified position in this list
 * @throws IndexOutOfBoundsException if the index is out of range
 *         ({@code index < 0 || index >= this.size()})
 */
E get(int index);
```

* Javadoc内ではHTMLのタグが使える。
* ```@code```を使うことで、囲んだ部分をHTMLマークアップJavadocタグがないものとみなす。
* 継承元となる設計をされたクラスは```@implSpec```タグでメソッドとサブクラスとの決まり事を記述する。

```java
/**
 * Returns true if this collection is empty.
 *
 * @implSpec
 * This implementation returns {@code this.size() == 0}.
 *
 * @return true if this collection is empty
 */
public boolean isEmpty() { ... }
```

* Java9からできた```@literal```で囲むと、その中身はHTMLマークアップの処理がされない。また、```@code```と違い、コードのフォントにレンダリングされない。
* Javadocコメントの一文目には、その要素の要約を記す。混乱を避けるために、クラス内で異なるメンバ、コンストラクタに同じ要約をつけないようにする（オーバーロードする時など特にやりがちなので注意する）。
* メソッドとコンストラクタの要約文は慣例として、完全な文でなく、動詞句の文となっている。Collection.size()の例は以下のよう。

```
Returns the number of elements in this collection.
```

* クラス、インターフェース、フィールドの要約文は慣例として、名詞句の文となっている。Instantクラスの例は以下のよう。

```
An instantaneous point on the time-line.
```

* Java9以降で、Javadocにインデックスを張り、検索ができるようになった。クラス、メソッド、フィールド等は自動的にインデックスが張られるのだが、任意の文字列に対してもインデックスを張りたい場合には、```@index```を用いる。

```
This method complies with the {@index IEEE 754} standard.
```

* ジェネリック型に対しては、すべての型にドキュメントを書く必要がある。

```java
/**
 * An object that maps keys to values.  A map cannot contain duplicate keys;
 * each key can map to at most one value.
 *
 *
 * @param <K> the type of keys maintained by this map
 * @param <V> the type of mapped values
 *
 * @since 1.2
 */
public interface Map<K, V> {
```

* Enumに対しては、enum定数の全てにドキュメントを書く必要がある。

```java
/**
 * An instrument section of a symphony orchestra.
 */
public enum OrchestraSection {
    /** Woodwinds, such as flute, clarinet, and oboe. */
    WOODWIND,
    /** Brass instruments, such as french horn and trumpet. */
    BRASS,
     /** Percussion instruments, such as timpani and cymbals. */
    PERCUSSION,
     /** Stringed instruments, such as violin and cello. */
    STRING;
}
```

* アノテーション型については、アノテーション型そのものに加え、メンバにもドキュメントを書く。

```java
/**
 * Indicates that the named compiler warnings should be suppressed in the
 * annotated element (and in all program elements contained in the annotated
 * element).  Note that the set of warnings suppressed in a given element is
 * a superset of the warnings suppressed in all containing elements.  For
 * example, if you annotate a class to suppress one warning and annotate a
 * method to suppress another, both warnings will be suppressed in the method.
 * However, note that if a warning is suppressed in a {@code
 * module-info} file, the suppression applies to elements within the
 * file and <em>not</em> to types contained within the module.
 *
 * <p>As a matter of style, programmers should always use this annotation
 * on the most deeply nested element where it is effective.  If you want to
 * suppress a warning in a particular method, you should annotate that
 * method rather than its class.
 *
 * @author Josh Bloch
 * @since 1.5
 * @jls 4.8 Raw Types
 * @jls 4.12.2 Variables of Reference Type
 * @jls 5.1.9 Unchecked Conversion
 * @jls 5.5.2 Checked Casts and Unchecked Casts
 * @jls 9.6.4.5 @SuppressWarnings
 */
@Target({TYPE, FIELD, METHOD, PARAMETER, CONSTRUCTOR, LOCAL_VARIABLE, MODULE})
@Retention(RetentionPolicy.SOURCE)
public @interface SuppressWarnings {
    /**
     * The set of warnings that are to be suppressed by the compiler in the
     * annotated element.  Duplicate names are permitted.  The second and
     * successive occurrences of a name are ignored.  The presence of
     * unrecognized warning names is <i>not</i> an error: Compilers must
     * ignore any warning names they do not recognize.  They are, however,
     * free to emit a warning if an annotation contains an unrecognized
     * warning name.
     *
     * <p> The string {@code "unchecked"} is used to suppress
     * unchecked warnings. Compiler vendors should document the
     * additional warning names they support in conjunction with this
     * annotation type. They are encouraged to cooperate to ensure
     * that the same names work across multiple compilers.
     * @return the set of warnings to be suppressed
     */
    String[] value();
}
```

* クラス、メソッドのスレッド安全例のレベル（Item82）と直列化可否、直列化されたときの形式（Item87）を書くべき。
* クラス同士が複雑に連携しているなど、APIの全体観を示す補助資料が必要な場合で、資料がある場合にはJavadocにリンクを載せておく。

# 9章.プログラミング一般

# 57.ローカル変数のスコープは最小にせよ
* ローカル変数のスコープを最小にする最も効果的なテクニックは、その変数を最初に用いる直前に宣言することである。
* ローカル変数は基本的に宣言時に初期化しておくべきである。
* ループ文においては、while文よりfor文を選択すべき。
  * なぜなら、for文は繰り返しに用いるその場限りの変数を定義できるのに対して、while文ではそれができないから。
  * for文のほうがコピペによるミスが起きにくい。（構文が割と定まっている）
* ローカル変数のスコープを最小にするためにメソッドを単位を小さくすべき。

# 58.従来のforループより、for-eachのループを選択すべき

* 従来のfor文のほうが記述すべきことが多くて、ミスが発生する確率が上がる。
* 入れ子のイテレーションがあるときもfor-eachが使える。



```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.Collection;

public class NestedFor {
    enum Suit {
        CLUB, DIAMOND, HEART, SPADE
    };

    enum Rank {
        ACE, DEUCE, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING
    };

    public static void main(String[] args) {
        Collection<Suit> suits = Arrays.asList(Suit.values());
        Collection<Rank> ranks = Arrays.asList(Rank.values());

        for (Suit suit : suits) {
            for (Rank rank : ranks) {
                System.out.println("柄" + suit + "：数" + rank);
            }
        }
    }
}
```



* 一般的にfor-eachが使えない場面が3つある。

  * フィルタリングして特定の要素を削除する場合

  * 要素の値を変換する場合

  * 複数の要素集合を、並列で走査する場合

* Iterableをimplementsしているオブジェクトに対してfor-eachで要素を取り出すことができる。



# 59.ライブラリを知り、利用する
* ランダムな値を作るにおいて、下記の1番目のような実装では値の平均値がおかしくなる。ライブラリを使用することで正しくランダム値生成ができる。


```java
package tryAny.effectiveJava;

import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

import org.apache.commons.lang3.time.StopWatch;

public class RandomTest {
    public static void main(String[] args) {
        int n = 2 * (Integer.MAX_VALUE / 3);
        int low1 = 0;
        StopWatch sw1 = new StopWatch();
        sw1.start();
        for (int i = 0; i < 1000000; i++) {
            if (random(n) < n / 2) {
                low1++;
            }
        }
        sw1.stop();

        System.out.println(low1); // 500000位になると思いきやならない。666666位になる。
        System.out.println(sw1.getTime());

        int low2 = 0;
        StopWatch sw2 = new StopWatch();
        sw2.start();
        for (int i = 0; i < 1000000; i++) {
            if (tlr.nextInt(n) < n / 2) {
                low2++;
            }
        }
        sw2.stop();
        System.out.println(low2);// 500000位になる。
        System.out.println(sw2.getTime());// 速度はあまり変わらない
    }

    static Random rnd = new Random();

    static int random(int n) {
        return Math.abs(rnd.nextInt()) % n;
    }

    static ThreadLocalRandom tlr = ThreadLocalRandom.current();

}

```



* 自分で処理を書くのではなく、ライブラリを使用することで得られる利点は以下の5つ。

  * エキスパートが練りに練った実装を使える。

  * 時間を節約できる。

  * ライブラリ自体が進化していくので、恩恵にあずかれる。

  * ライブラリの機能がリリース事に増えるので、その恩恵にあずかれる。

  * 標準的なライブラリを使うことで、自身のコードが主流に則ったものとなり、読みやすく、つかいやすいものとなる。

* すべてのプログラマが、java.lang,java.util,java.ioとそれらのサブパッケージには親しくなっておくべき。



# 60.正確な値を求める場合はfloatとdoubleの使用を控えるべし

* 特に金の計算には使わないほうが良い。floatとdoubleでは0.1を表現できない。代わりにBigDecimal、int、longを用いる。

* BigDecimalのデメリットは、使いづらく、遅いところ。

* 9桁以下の計算にはintを、18桁以下ならlongを、19桁以上ならBigDecimalを使うべき。



# 10章.例外



# 69.例外的な状況にのみ、例外は用いるべし

* パフォーマンスを上げる目的で、通常のフローにもかかわらず、例外を用いたコードを書いてはならない。

* APIを作成するにあたっては、通常のフローで例外を使うようにさせない工夫がいる。以下のようなコードを生まないようにするには、hasNext 的なメソッドを用意するか、状態に応じて空のOptionalやnullを返すメソッドを用意するかのいずれかが考えられる。並列でアクセスされる可能性がある場合は後者を選ぶべき。性能的には後者のほうが良い。可読性と誤り検知のしやすさの観点では前者が勝る。



```java

// Do not use this hideous code for iteration over a collection!

try {

    Iterator<Foo> i = collection.iterator();

    while(true) {

        Foo foo = i.next();

        ...

    }

} catch (NoSuchElementException e) {

```



# 70.復帰可能な状況では検査例外を用い、プログラミングエラー？に対しては実行時例外を用いる

* 指針としては、呼び出し側が復帰できるような状況で出力される例外は、検査例外とする。復帰できないものは非検査例外。

* 復帰可能か否か判別がつかない場合は非検査例外とすべき。（item71で説明）

* Error クラスは慣習的にリソース欠乏時などにJVMによって出力されるものであり、Errorのサブクラスをプログラマーが作ることはまずない。そのため、非検査例外のうちでimplementsしうるのはRuntimeExceptionのみである。

* Throwablesを直接継承した例外を定義してはならない。検査例外を継承しないことによるメリットがないし、ユーザを混乱させてしまうため。



# 71.不必要な検査例外の使用はさけるべし

* APIを適切に使用しても該当の例外的状況を避けられず、かつ、その例外が発生したときにAPI利用ユーザが何らかの有益なアクションを取れる場合にのみ検査例外の使用するべき。

* メソッドによってスローされる検査例外がただ一つである場合、実質的に実装者の負担は増える？。（**どういう理屈か理解できなかった**）

* 検査例外をスローする代わりに、空のOptionalを返す方法がある。このOptionalを返す方法のデメリットは望み通りの演算ができなかったことについての情報を呼び出し元に届けられない点にある。

* 検査例外スローを避ける手段として、常に成り立つわけではないが、状態を確かめる boolean を返すメソッドと、非検査例外を返すメソッドに分ける方法がある。



```java

// Invocation with state-testing method and unchecked exception

if (obj.actionPermitted(args)) {

    obj.action(args);

} else {

    ... // Handle exceptional condition

}

```



# 72.標準例外の使用を心掛けるべし

* Javaライブラリが提供している標準例外を用いることによるメリットは以下。

  * 慣習に従っているので、学びやすく理解しやすい

  * 見慣れない例外を使用していないので、読みやすい

* 以下、Javaライブラリにある例外をしるす。

  * IllegalArgumentException：nullでない、不適鉄な引数を受け取ったときスローされる

  * IllegalStateException：受け取るオブジェクトの状態が不適切な時スローされる。例えば、あるオブジェクトを適切に初期化する前に使用してしまった場合などにスローされる

  * NullPointerException：nullが禁止されているところでパラメータがnullとなる場合にスロー

  * IndexOutOfBoundsException：リスト等のパラメータの範囲外にアクセスした場合にスロー

  * ConcurrentModificationException：シングルスレッドで利用される前提で作られたオブジェクトが、並列実行を検知したときにスローされる

  * UnsupportedOperationException：該当オブジェクトがサポートしていないメソッドを使用した場合にスロー

* 例外を再利用するときは、その例外のドキュメントをみて、意図に沿っているか確認せねばならない



# 73.抽象概念に適した例外をスローすべし

* 低層で送出された例外は、高層で具体的に行われているタスクとあまり関係がないように見えて困ることがある。また、低層で創出された例外は、高層のAPI実装に影響を与えうる（**あまりピンとこない**）。この問題を避けるために、低層で送出された例外をcatchし、高層の例外に翻訳する処理を加えることがある。



```java

// Exception Translation

try {

    ... // Use lower-level abstraction to do our bidding

} catch (LowerLevelException e) {

    throw new HigherLevelException(...);

}

```



* 低層から高層に例外翻訳する際に、低層での例外情報を保持するために、以下のようにchaining-aware constructor を書くことべき。



```java

// Exception Chaining

try {

    ... // Use lower-level abstraction to do our bidding

} catch (LowerLevelException cause) {

    throw new HigherLevelException(cause);

}

```



* 一番良いのは、そもそも低層で例外が起こらないようにすることであり、そのために渡すパラメータの値をバリデーションしたりすることを考える。

# 74.各メソッドからスローされる例外は全てドキュメントに残すべし
* 検査例外をスローするメソッドには、Javadoc内で@throwsタグを使って、どのような状況でスローされるのか書く。
* 非検査例外に関しても、Javadoc内で@throwsタグでどのような場合にスローされるのか書くべき。こうすることによって、API使用者は@throwsがあるのにthrows句がないことから、該当の例外が非検査例外であることを知る手掛かりとなる。
* 各メソッドがスローしうる非検査例外全てをドキュメントとして残すのが理想。（現実はそうもいかない）
* クラス内の多くのメソッドで、同じ理由でスローされる例外は、クラスのドキュメントに記すべきである。

# 75.詳細メッセージにエラー記録情報を含めるべし
* 例外の詳細メッセージ（スタックトレースに出てくるやつ）にはエラー解析に役立つ情報を含める。例えば、IndexOutOfBoundsException であれば、下限値、上限値、indexの値を含めるようにすべき。（実際にはJava9時点で以下のようにindexの値だけ出すコンストラクタがある）

```java
    /**
     * Constructs a new {@code IndexOutOfBoundsException} class with an
     * argument indicating the illegal index.
     *
     * <p>The index is included in this exception's detail message.  The
     * exact presentation format of the detail message is unspecified.
     *
     * @param index the illegal index.
     * @since 9
     */
    public IndexOutOfBoundsException(int index) {
        super("Index out of range: " + index);
    }
```

* スタックトレースは多くの人目に触れるため、詳細メッセージにパスワードや暗号化キー等を含めてはいけない。

# 76.障害原子性（failure atomicity）が達成できるよう努めるべし
* オブジェクトに対してメソッド呼び出しをして、エラーを出力した後でも、そのオブジェクトがメソッド呼び出し前と同じ状態にある。このような特性をfailure atomicという。
* immutableオブジェクトのメソッド呼び出しであれば、自ずとfailure atomicityが実現できる。
* mutableオブジェクトのメソッド呼び出しにおいて、極力failure atomicity とするための方法は以下。
  * オペレーション実行前にバリデーションチェックを入れる。（状態が変わる前にエラーにさせる）
  * 状態を変えるオペレーションの実行前に演算を行う。例えば、TreeMap の put であれば、実際にMapに加える前にソート処理が走り、そこでComparableでないものだったら落とされる。
  * 一時的なコピーを作成して、そのコピーに対して処理をしていき、最後に該当のコンテンツに代入するようにする。これは性能面でも有効。
  * 処理の最中で失敗するようなことがあれば、ロールバックするようにして、オペレーション開始前の状態に戻す。
* failure atomicityを満たせない場合は、エラーが起きた場合にどのような状態が残るのか、ドキュメントに残しておくことが理想。

# 77.例外を無視してはならない
* エラーを無視するのが適切な場合もありうるが、その場合はcatchブロックの中でなぜエラーを無視するかのコメントを入れ、catchするエラーの変数名を**ignored**にするべきである。
* 検査例外も非検査例外も等しくこのItem77を守るべき。

# 11章.並列性

# 78.共有されるmutableなデータには、同期したアクセスをすべし
* 同期化の一つの役割は、排他制御であり、変数を矛盾した状態で読み取らせないようにすることにある。また、他スレッドが行った変更を見ることができるようにするのも同期化の役割である（**後半いまいちわからん**）。
* 排他制御だけでなく、スレッド間の信頼ある通信のためにも同期化は必要である。
* Thread#stop()は使ってはいけない。使うとデータが壊れてしまう。
* 以下のコードは一見、1秒で止まるように見えるが、実際には止まらない。バックグラウンドで動作するスレッドがいつstopRequestedを見に行くか、同期が保証されていないので、JVMは

```java
    while (!stopRequested)
        i++;
```
を

```java
if (!stopRequested)
    while (true)
        i++;
```
のように変換する。この最適化はhoistingと呼ばれる。（「**liveness failure**:プログラムがそれ以上先に進めなくなるエラー」の例）


```java
package tryAny.effectiveJava;

import java.util.concurrent.TimeUnit;

public class StopThread {
    private static boolean stopRequested;

    public static void main(String[] args) throws InterruptedException {
        Thread backgroundThead = new Thread(() -> {
            int i = 0;
            while (!stopRequested) {
                i++;
            }
        });

        backgroundThead.start();

        TimeUnit.SECONDS.sleep(1);

        stopRequested = true;
    }
}
```

* 以下のように、stopRequested の読み込み、書き込みともに同期化してやれば期待通りに1秒で止まる。

```java
package tryAny.effectiveJava;

import java.util.concurrent.TimeUnit;

public class StopThread2 {
    private static boolean stopRequested;

    private static synchronized void requestStop() {
        stopRequested = true;
    }

    private static synchronized boolean stopRequested() {
        return stopRequested;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread backgroundThead = new Thread(() -> {
            int i = 0;
            while (!stopRequested()) {
                i++;
            }
        });

        backgroundThead.start();

        TimeUnit.SECONDS.sleep(1);

        requestStop();
    }
}
```

* 以下のように、stopRequestedにvolatile修飾子をつけてやれば、一番新しく書き込まれた値を読むことを保証できるので、期待通りに1秒で止まる。

```java
package tryAny.effectiveJava;

import java.util.concurrent.TimeUnit;

public class StopThread3 {
    private static volatile boolean stopRequested;

    public static void main(String[] args) throws InterruptedException {
        Thread backgroundThead = new Thread(() -> {
            int i = 0;
            while (!stopRequested) {
                i++;
            }
        });

        backgroundThead.start();

        TimeUnit.SECONDS.sleep(1);

        stopRequested = true;
    }
}
```

* ++のインクリメント処理はアトミックなものではないので、以下のコードが1ずつ上昇していくユニークな値を返す保証はない。解消する場合には、AtomicLongを使うべき。（「**safety failure**：プログラムが誤った結果を返すエラー」の例）

```java
// safety failure
private static volatile int nextSerialNumber = 0;
public static int generateSerialNumber() {
    return nextSerialNumber++;
}
```

```java
private static final AtomicLong nextSerialNum = new AtomicLong();
 public static long generateSerialNumber() {
    return nextSerialNum.getAndIncrement();
}
```

* 本章で扱われている問題を避けるには、mutableなデータの処理は1つのスレッドに限定させておくようにする。

# 79.過度な同期は避ける

* 過度な同期は、性能の劣化、デッドロック、非決定的な挙動を招く。
* 活性エラー（liveness failure）、安全性エラー（safety failure）を避けるためには、同期をとった処理の中でクライアントに処理させる権限を与えないようにするべき。
* 以下のプログラムは```ConcurrentModificationException```を出力する。
notifyElementAdded メソッドではobservers のイテレート処理を行い、その中で、SetObserverのaddedメソッドを実行し、observersに変更をかけようとしている。イテレート処理の最中のリストから要素を取り除くことはできないので、エラーが発生した。

```java
package tryAny.effectiveJava;

import java.util.HashSet;

public class SynchroTest {
    public static void main(String[] args) {
        ObservableSet<Integer> set = new ObservableSet<>(new HashSet<>());
        set.addObserver(new SetObserver<>() {
            public void added(ObservableSet<Integer> s, Integer e) {
                System.out.println(e);
                if (e == 23) {
                    s.removeObserver(this);
                }
            }
        });
        for (int i = 0; i < 100; i++) {
            set.add(i);
        }
    }
}
```

```java
package tryAny.effectiveJava;

import java.util.Collection;
import java.util.Iterator;
import java.util.Set;

public class ForwardingSet<E> implements Set<E> {
    private final Set<E> s;

    public ForwardingSet(Set<E> s) {
        this.s = s;
    }

    public void clear() {
        s.clear();
    }

    public boolean contains(Object o) {
        return s.contains(o);
    }

    public boolean isEmpty() {
        return s.isEmpty();
    }

    public int size() {
        return s.size();
    }

    public Iterator<E> iterator() {
        return s.iterator();
    }

    public boolean add(E e) {
        return s.add(e);
    }

    public boolean remove(Object o) {
        return s.remove(o);
    }

    public boolean containsAll(Collection<?> c) {
        return s.containsAll(c);
    }

    public boolean addAll(Collection<? extends E> c) {
        return s.addAll(c);
    }

    public boolean removeAll(Collection<?> c) {
        return s.removeAll(c);
    }

    public boolean retainAll(Collection<?> c) {
        return s.retainAll(c);
    }

    public Object[] toArray() {
        return s.toArray();
    }

    public <T> T[] toArray(T[] a) {
        return s.toArray(a);
    }

    @Override
    public boolean equals(Object o) {
        return s.equals(o);
    }

    @Override
    public int hashCode() {
        return s.hashCode();
    }

    @Override
    public String toString() {
        return s.toString();
    }

}
```

```java
package tryAny.effectiveJava;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Set;

public class ObservableSet<E> extends ForwardingSet<E> {
    public ObservableSet(Set<E> set) {
        super(set);
    }

    private final List<SetObserver<E>> observers = new ArrayList<>();

    public void addObserver(SetObserver<E> observer) {
        synchronized (observers) {
            observers.add(observer);
        }
    }

    public boolean removeObserver(SetObserver<E> observer) {
        synchronized (observers) {
            return observers.remove(observer);
        }
    }

    private void notifyElementAdded(E element) {

        synchronized (observers) {
            for (SetObserver<E> observer : observers)
                observer.added(this, element);
        }
    }

    @Override
    public boolean add(E element) {
        boolean added = super.add(element);
        if (added)
            notifyElementAdded(element);
        return added;
    }

    @Override
    public boolean addAll(Collection<? extends E> c) {
        boolean result = false;
        for (E element : c)
            result |= add(element); // Calls notifyElementAdded
        return result;
    }
}
```

```java
package tryAny.effectiveJava;

@FunctionalInterface
public interface SetObserver<E> {
    // Invoked when an element is added to the observable set
    void added(ObservableSet<E> set, E element);
}
```

* 以下のコードを実行するとデッドロックが発生する。バックグラウンドで走るスレッドは```s.removeObserver```において```observers```のロックを取ろうとするが、メインスレッドがすでに```observers```のロックを取っているため、ロックが取れない。一方、メインスレッドバックグラウンドのスレッドの処理待ちとなるのでデッドロックとなる。

```java
package tryAny.effectiveJava;

import java.util.HashSet;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SynchroTest2 {
    public static void main(String[] args) {
        ObservableSet<Integer> set = new ObservableSet<>(new HashSet<>());
        set.addObserver(new SetObserver<>() {
            public void added(ObservableSet<Integer> s, Integer e) {
                System.out.println(e);
                if (e == 23) {
                    ExecutorService exec = Executors.newSingleThreadExecutor();
                    try {
                        exec.submit(() -> (s.removeObserver(this))).get();
                    } catch (ExecutionException | InterruptedException ex) {
                        throw new AssertionError(ex);
                    } finally {
                        exec.shutdown();
                    }
                }
            }
        });
        for (int i = 0; i < 100; i++) {
            set.add(i);
        }

        // エラーは出ないがここには到達しない
        System.out.println("finish");
    }
}
```

* 上の```ConcurrentModificationException```が発生する例では、デッドロックは発生していない。これは、Java言語のロックは```reentrant```なものだからである。reentrantなロックはマルチスレッドプログラミングをシンプルなものにするが、liveness failureをsafety failureにしうる。（**？**）
* これらの問題への対処法としては、synchronizedブロックから未知のメソッドを取り除く方法がある。

```java
// Alien method moved outside of synchronized block - open calls
private void notifyElementAdded(E element) {
    List<SetObserver<E>> snapshot = null;
    synchronized(observers) {
        snapshot = new ArrayList<>(observers);
    }
    for (SetObserver<E> observer : snapshot)
        observer.added(this, element);
}
```
また、さらに良い方法としては、synchronizedブロックを使わずに ```CopyOnWriteArrayList```を使う方法がある。

```java
// Thread-safe observable set with CopyOnWriteArrayList
private final List<SetObserver<E>> observers =
        new CopyOnWriteArrayList<>();
 public void addObserver(SetObserver<E> observer) {
    observers.add(observer);
}
 public boolean removeObserver(SetObserver<E> observer)
{
    return observers.remove(observer);
}
 private void notifyElementAdded(E element) {
    for (SetObserver<E> observer : observers)
        observer.added(this, element);
}
```

* synchronizedブロックの中での処理はできるだけ少なくするべき。長い時間がかかる処理が必要な場合は、Item78のガイドを破らずに、処理をsynchronizedブロックの外側に出すようにするべき。
* 過度な同期のコストは、ロックを取るためのCPU時間ではなく、並列化する機会を失うことや、全coreでのメモリに対する一貫性を担保するために課される処理が問題となる。また、過度な同期によってVMによるコード実行の最適化が行われないことも問題である。
* mutableなクラスを書くにあたっては、2つの選択肢がある。
  * 同期に関するコードは書かず、利用者に同期を任せる。
  * スレッドセーフ（Item82）なクラスを書き、内部で同期を保つ。

* ```StringBuffer``` はほとんどシングルスレッドでしか使われないのに、内部で同期する仕組みになっている。そのため、同期をしない仕組みの```StringBuilder```に取って代わられた。ランダムな数値を作成する ```java.util.Random``` も同様の理由で```java.util.concurrent.ThreadLocalRandom```に取って代わられた。
* 内部で同期するクラスをうまく作る技法は様々あるが、この本では述べられていない。
* メソッドがstaticフィールドを変更し、複数のスレッドから呼ばれることがあるとすれば、そのstaticフィールドへのアクセスは内部で同期しておかなければならない。なぜなら、外部で同期をとることはできないからである。

# 80.スレッドよりエグゼキュータ、タスク、ストリームを選択すべし

* Executor Frameworkを用いて簡単にバックグラウンドで処理を実行させることができる。
* Executor Frameworkを用いることで、全てのタスクが終了する、またはどれか一つのタスクが終了するまで待つことや、周期的にタスクを実行するなどといったことができるようになった。

```java
package tryAny.effectiveJava;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorTest {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        List<Callable<String>> tasks = Arrays.asList(() -> "first", () -> "second");

        ExecutorService es = Executors.newFixedThreadPool(2);
        List<Future<String>> rets = es.invokeAll(tasks);

        for (Future<String> r : rets) {
            System.out.println(r.get());
        }

        System.out.println(es.invokeAny(tasks));// first か second ランダムで

    }
}
```

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

* 複数のスレッドを利用した処理がしたい場合には、java.util.concurrent.Executors に様々なスレッドプールを作成するファクトリメソッドがあるので、それを使う。それらの使用では用途に合わない場合、ThreadPoolExecutorを直接使用する。
* 比較的処理の軽いサーバにおいては、newCachedThreadPool を使いうるが、cached thread pool はサブミットされたタスクをすぐに実行に移し、スレッドがなければ新しいスレッドを作る、という挙動を取るため処理が重いサーバでは newFixedThreadPool を使うべき。
* Threadsを直接使用するのは避けるべき。ExecutorFramework　では、処理の単位と実行のメカニズムが分離されており、柔軟性がある。
* Java7以降、fork-join という仕組みで効率的に処理を実行できるようになった。

```java
package tryAny.concurrentUtility;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class ConcurrentTest8 {
    public static void main(String[] args) {
        int data[] = { 1, 2, 3, 4, 5, 6, 7 };
        ForkJoinPool service = new ForkJoinPool();
        service.invoke(new AddAction(data, 0, data.length));
    }
}

class AddAction extends RecursiveAction {
    private static final int THRESHOLD_SIZE = 3;
    private int start;
    private int end;
    private int[] numbers;

    public AddAction(int[] numbers, int start, int end) {
        this.start = start;
        this.end = end;
        this.numbers = numbers;
    }

    protected void compute() {
        int total = 0;
        if (end - start <= THRESHOLD_SIZE) {
            for (int i = start; i < end; i++) {
                total += numbers[i];
            }
            System.out.println(total + " ");
        } else {
            new AddAction(numbers, start + THRESHOLD_SIZE, end).fork();
            new AddAction(numbers, start, Math.min(end, start + THRESHOLD_SIZE)).compute();
        }
    }
}
```

#81 wait と notify よりコンカレンシーユティリティを選ぶべし

* Java5以降、以前はwaitやnotifyで行っていた処理が高レベルなコンカレンシーユーティリティでできるようになった。これらを代わりに使うべきである。
* 高レベルなコンカレンシーユーティリティは3つに分けられる。
  * Executor フレームワーク（Item80）
  * concurrent collection。List、Map、Queueに並列処理がうまくできるように実装されたものがこれに当たる。これらは内部で同期がなされるため、ロックしても単に処理が遅くなるだけである。この部品は状態に依存する変更処理（state-dependent modify operations）に適している。concurrent collections の登場によって、synchronized collections はお払い箱となった。
  * synchronizers。synchronizers は他のスレッドの処理完了を待つなど、他と強調した動きを可能にする。有名なのは、CountDownLatch、Semaphore、CyclicBarrier、Exchanger、Phaserなど。
* CountDownLatch を使用したコードは以下のようになる。timeメソッドについて説明すると、ready が3回 countDown されると、ready のawait が解けて、startNanosが計測されて、start の countDown が1回なされて actionが走り、そして、各スレッドで done の countDown がなされて、3つすべてでcountDownされたらdoneのawaitが解けて、かかった時間が返される仕組み。このメソッドはスレッド数が第2引数で指定されていた数より少ない場合は処理が終わらない（thread starvation deadlock）。	

```java
package tryAny.effectiveJava;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class CountDownLatchTest {
    public static void main(String[] args) throws InterruptedException {
        Executor e = Executors.newFixedThreadPool(3); // ここの引数をtimeの第2引数の値未満にすると処理が終わらない。

        System.out.println(time(e, 3, () -> System.out.println("a")));

    }

    // Simple framework for timing concurrent execution
    public static long time(Executor executor, int concurrency, Runnable action) throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(concurrency);
        CountDownLatch start = new CountDownLatch(1);
        CountDownLatch done = new CountDownLatch(concurrency);
        for (int i = 0; i < concurrency; i++) {
            executor.execute(() -> {
                ready.countDown(); // Tell timer we're ready
                try {
                    start.await(); // Wait till peers are ready
                    action.run();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    done.countDown(); // Tell timer we're done
                }
            });
        }
        ready.await(); // Wait for all workers to be ready
        long startNanos = System.nanoTime();
        start.countDown(); // And they're off!
        done.await(); // Wait for all workers to finish
        return System.nanoTime() - startNanos;

    }
}
```

* wait と notify についてはもはや新しく書かれたコードで見ることはない。レガシーなコードの保守で見ることはあるかもしれない。
* wait と notify についての要約だけ書くと、
  * waitはwhile ループの中で使うこと。
  * notifyよりnotifyAllを使うべき。notifyを使うときは、スレッドの生存に気を付けて使用せねばならない。

# 82.スレッドセーフティについてドキュメントすべし

* 提供するメソッドを並列実行させた時の挙動は、クライアントとの重要な約束事であり、ドキュメントとして明記しないとエラーを招くこととなる。
* sychronized句の有無でスレッドセーフであるかを見分けることはできない。
* スレッドセーフという性質はオールオアナッシングなものではなく、数段階のレベルがあるものである。以下、スレッドセーフの各レベルを要約する。
  * Immutable：状態は常に一貫しており、外部での同期は必要ない。
ex)String,Long,BigInteger
  * Unconditionally thread-safe：mutableなインスタンスであるが、内部で十分に同期がとれているので、外部での同期は必要ない。
ex)AtomicLong,ConcurrentHashMap
  * Conditionally thread-safe：Unconditionally thread-safeに似ているが、一部のメソッドでは外部での同期が必要となる。
ex)Collections.synchronized のラッパークラス。これらのiterators は外部の同期が必要となる。
  * Not thread-safe：並列処理をしようと思ったら必ず外部で同期が必要となる。
ex)ArrayList,HashMap
  * Thread-hostile：外部で同期をかけてもスレッドセーフにならない。たいていはstaticなデータを同期なしで変更していることによる。
ex)Item78のgeneralSerialNumber メソッド

* クラスのスレッドセーフティについてはクラスのJavadocに書くべきで、スレッドセーフティに関して特別な考慮が必要なメソッドには、そのJavadocに記述する。以下の```Collections.synchronizedMap```が好例。

```java
    /**
     * It is imperative that the user manually synchronize on the returned
     * map when traversing any of its collection views via {@link Iterator},
     * {@link Spliterator} or {@link Stream}:
     * <pre>
     *  Map m = Collections.synchronizedMap(new HashMap());
     *      ...
     *  Set s = m.keySet();  // Needn't be in synchronized block
     *      ...
     *  synchronized (m) {  // Synchronizing on m, not s!
     *      Iterator i = s.iterator(); // Must be in synchronized block
     *      while (i.hasNext())
     *          foo(i.next());
     *  }
     * </pre>
     */
    public static <K,V> Map<K,V> synchronizedMap(Map<K,V> m) {
        return new SynchronizedMap<>(m);
    }
```

* Unconditionally thread-safe なクラスを書くにあたっては、synchronized なメソッドの代わりにprivate lockを使う手法がある。これによって、クライアント、サブクラスからの悪意ある同期から守ることができる。（**DOSの例を挙げていたが、どうやって起こすのかいまいちわからない**）

# 83.遅延初期化は注意して使うべし

* 遅延初期化とは、値が必要となった時に初めて初期化させる動作のことをいう。遅延初期化は主に処理性能を上げるために行われるが、害をもたらすこともある。
* 遅延初期化はクラスの初期化やインスタンス生成のコストを省いてくれるが、遅延初期化を行うフィールドへのアクセスコストは増加する。
* 遅延初期化を行う該当のフィールドが、該当クラスのインスタンスのたった一部のフィールドであり、かつ、そのフィールドの初期化コストが高い場合には、遅延初期化の効果があるかもしれない。効果を確かめる唯一の方法は遅延初期化しない場合と性能差を比べるしかない。
* マルチスレッド環境下での遅延初期化はトリッキーなものとなる。本章で述べられる初期化テクニックはスレッドセーフなものである。
* たいていの状況では、普通の初期化の方が遅延初期化よりも好ましい。以下通常の初期化例。

```java
// Normal initialization of an instance field
private final FieldType field = computeFieldValue();
```

* 遅延初期化を使って、初期化循環を防ぐにあたっては、シンプルで明確であるという理由から、synchronizedアクセサを使用するべきである。

```java
// Lazy initialization of instance field - synchronized accessor
private FieldType field;
 private synchronized FieldType getField() {
    if (field == null)
        field = computeFieldValue();
    return field;
}
```

* 上記2つの書き方は、フィールドがstaticであっても変わらない（フィールドとアクセサメソッド両方がstaticである場合は除く）。
* 遅延初期化をstaticフィールドに対して、パフォーマンス向上のために使用するのであれば、以下のような書き方があり得る（lazy initialization holder class idiom）。


```java
// Lazy initialization holder class idiom for static fields
private static class FieldHolder {
  static final FieldType field = computeFieldValue();
}
private static FieldType getField() { return FieldHolder.field; }
```

* 遅延初期化をインスタンスフィールドに対して、パフォーマンス向上のためにやるのであれば、以下のような書き方がある（double-check idiom）。
この書き方では、初期化済みであった場合には、ロックを取らないようにしている。
書き方の説明をすると、ここではフィールド変数に対して2回のチェックロジックがはしっている。1回目はロックせずにチェックをし、チェックの結果として初期化がまだであれば、ロックをしてもう一度チェックをする。2度目のチェックでも初期化がまだだったら初期化のメソッドを走らせる。
一度初期化されるとロックを用いた処理ではなくなるので、フィールドはvolatileで宣言しておかねばならない。

```java
// Double-check idiom for lazy initialization of instance fields
private volatile FieldType field;
 private FieldType getField() {
    FieldType result = field;
    if (result == null) {  // First check (no locking)
        synchronized(this) {
            if (field == null)  // Second check (with locking)
                field = result = computeFieldValue();
        }
    }
    return result;
}
```

* 上記のコードのresultはいらないように見えるが、これがあるとない場合より1.4倍くらい速くなるらしい（**速くなる理屈はよくわからず**）。
* double-check idiomはstatic フィールドにも適用できるが、lazy initialization holder class idiom の方がベターである。
* double-check idiom に関して、複数回の初期化にも耐えられるようにするには2つ目のチェックを除けばよい（single-check idiom）。
（**複数回の初期化に耐えられるようにするのに、なぜsingle-check idiomが適しているのかわからない。。**）

```java
// Single-check idiom - can cause repeated initialization!
private volatile FieldType field;
 private FieldType getField() {
    FieldType result = field;
    if (result == null)
        field = result = computeFieldValue();
    return result;
}
```

# 84.スレッドスケジューラに依存してはならない

* スレッドスケジューラに正確性、パフォーマンスを依存したプログラムには移植性がない。スレッドをどのように実行するかはOS依存するからである。
* 信頼のおけるプログラムにするためには、処理実行平均スレッド数がプロセッサの数を大きく上回らないようにすべきである。
* runnableなスレッドの数を低く抑えるためには、効果のある処理をしないときには、スレッドを走らせないようにすべきである。ExecutorFrameworkの観点からは、スレッドプールのサイズを適切にし、タスクを短く抑えるようにすべき（短すぎると割り当てのためのオーバーヘッドが大きいのでダメ）。
* スレッドはbusy-wait状態、つまり、共有オブジェクトの状態が変化したか否かを繰り返しチェックしに行く状態、を避けるべきである。busy-waitはプロセッサに大きな負荷を与え、他のスレッドが効果のある処理を行うことを妨げてしまう。
以下の実装（SlowCountDownLatch）のようなCountDownLatchを使うとbusy-wait状態となり、普通のCountDownLatchを使うよりも遅くなる。

```java
package tryAny.effectiveJava;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class CountDownLatchTest {
    public static void main(String[] args) throws InterruptedException {
        Executor e = Executors.newFixedThreadPool(1000); // ここの引数をtimeの第2引数の値未満にすると処理が終わらない。

        System.out.println("time :" + time(e, 1000, () -> System.out.print("")));
        System.out.println("time2:" + time2(e, 1000, () -> System.out.print("")));
    }

    // Simple framework for timing concurrent execution
    public static long time(Executor executor, int concurrency, Runnable action) throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(concurrency);
        CountDownLatch start = new CountDownLatch(1);
        CountDownLatch done = new CountDownLatch(concurrency);
        for (int i = 0; i < concurrency; i++) {
            executor.execute(() -> {
                ready.countDown(); // Tell timer we're ready
                try {
                    start.await(); // Wait till peers are ready
                    action.run();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    done.countDown(); // Tell timer we're done
                }
            });
        }
        ready.await(); // Wait for all workers to be ready
        long startNanos = System.nanoTime();
        start.countDown(); // And they're off!
        done.await(); // Wait for all workers to finish
        return System.nanoTime() - startNanos;

    }

    public static long time2(Executor executor, int concurrency, Runnable action) throws InterruptedException {
        SlowCountDownLatch ready = new SlowCountDownLatch(concurrency);
        SlowCountDownLatch start = new SlowCountDownLatch(1);
        SlowCountDownLatch done = new SlowCountDownLatch(concurrency);
        for (int i = 0; i < concurrency; i++) {
            executor.execute(() -> {
                ready.countDown(); // Tell timer we're ready
                try {
                    start.await(); // Wait till peers are ready
                    action.run();
                } finally {
                    done.countDown(); // Tell timer we're done
                }
            });
        }
        ready.await(); // Wait for all workers to be ready
        long startNanos = System.nanoTime();
        start.countDown(); // And they're off!
        done.await(); // Wait for all workers to finish
        return System.nanoTime() - startNanos;

    }

    static class SlowCountDownLatch {
        private int count;

        public SlowCountDownLatch(int count) {
            if (count < 0)
                throw new IllegalArgumentException(count + " < 0");
            this.count = count;
        }

        // ここの実装がめっちゃbusy-wait
        public void await() {
            while (true) {
                synchronized (this) {
                    if (count == 0)
                        return;
                }
            }
        }

        public synchronized void countDown() {
            if (count != 0)
                count--;
        }
    }

}
```

* 対象のスレッドが十分なCPU時間を確保できないからといって、Thread.yieldを用いてはならない。一時的に事態が好転するかもしれないが、移植性のあるものではない。そうするよりも、アプリケーションの構成を見直し、並列実行されるスレッド数を減らすようにするべきである。
* Threadのpriorityも同様に移植性がなくあてにはならない。

# 12章．シリアライゼーション

