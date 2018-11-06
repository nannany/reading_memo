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

* ユーティリティクラスからたくさん定数を利用する場合はstatic importを使う。

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

# 23.タグ付きクラスよりクラス階層を選ぶ

## タグ付きクラス
2種類以上の特性を示し、その特性をフィールドに有しているタグで切り替えるクラスをタグ付きクラスと呼ぶ。
以下のクラスはその実例で、円と長方形を表現することが可能である。

```java
package tryAny.effectiveJava;

class Figure {
    enum Shape {
        RECTANGLE, CIRCLE
    }

    // 図形タイプを保持する
    final Shape shape;

    // shape が RECTANGLE の場合だけ利用する
    double length;
    double width;

    // shape が CIRCLE の場合だけ利用する
    double radius;

    // 円のためのコンストラクタ
    Figure(double radius) {
        shape = Shape.CIRCLE;
        this.radius = radius;
    }

    // 長方形のためのコンストラクタ
    Figure(double length, double width) {
        shape = Shape.RECTANGLE;
        this.length = length;
        this.width = width;
    }

    double area() {
        switch (shape) {
        case RECTANGLE:
            return length * width;
        case CIRCLE:
            return Math.PI * (radius * radius);
        default:
            throw new AssertionError();
        }
    }
}
```

このようなタグ付きクラスは欠点がたくさんある。
以下、欠点一覧。

* タグ付きクラスの定型文には、enum、タグフィールド、switchさせる文があり、たくさんの実装が1つのクラスに混ざるので、可読性が落ちる
* 利用している特性に関係ないフィールドも保持せねばならず、メモリ使用量が大きくなる
* コンストラクタが無関係なフィールドも初期化しない限りは、フィールドをfinalとして生成することができない（？）
* コンストラクタでタグフィールドを初期化し、コンパイラの補助なしで正しくフィールドを初期化する必要がある。できないとプログラムは実行時に落ちる
* ソースをいじらない限り、タグクラスに新しい特性を追加することはできない。また、追加したときに、switch文にケースを追加しないと実行時に失敗する
* インスタンスのデータ型がその特性に関して手掛かりを与えてくれない

## タグ付きクラスの代替法：クラス階層
オブジェクト指向言語であれば、クラス階層を用いることで改良できる。

タグ付きクラスからクラス階層に修正する手順としては、

1. abstract なクラスを作成し、その中にタグの値で動作を切り替えていたメソッド(上の例だとareaメソッド)を、abstract メソッドとして定義する
2. タグの値に依存しないメソッド、フィールド値は abstract クラスに入れる（上の例だとそのようなものは無い）
3. タグ付きクラスの特性に当たる部分について、サブクラスを作成する。（上記例だとcircle,rectangle）
4. 特性独自のフィールドを各サブクラスに入れる。（circleならradius、rectangleならlength,width）

上記の修正結果は以下のようになる。

```java
package tryAny.effectiveJava;

abstract class Figure {
    abstract double area();
}

class Circle extends Figure {
    final double radius;

    Circle(double radius) {
        this.radius = radius;
    }

    @Override
    double area() {
        return Math.PI * (radius * radius);
    }
}

class Rectangle extends Figure {
    final double length;
    final double width;

    Rectangle(double length, double width) {
        this.length = length;
        this.width = width;
    }

    @Override
    double area() {
        return length * width;
    }
}
```

こうすることによって上記であげたタグ付きクラスの欠点は解消されている。

### その他クラス階層の良い点
クラス階層は、型の間の本来の階層関係について反映できるため、柔軟性を改良したり（？）、コンパイル時のエラーチェックをより良いものにすることができる。

上記例で正方形の型について追加することになったときは、クラス階層の特性を使って以下のように記述することができる。

```java
class Square extends Rectangle {

    Square(double side) {
        super(side, side);
    }
}
```


# 24.staticでないメンバクラスより、staticメンバクラスを選択すべし
ネストしたクラスはエンクロージングクラスを補助する目的のために存在すべきである。
もしネストしたクラスをそれ以外の文脈で使用したいなら、トップレベルクラスとして定義するべき。

## ネストしたクラスの種類
ネストしたクラスには4種類あって、
* staticメンバクラス
* 非staticなメンバクラス
* 匿名クラス
* ローカルクラス

がある。staticメンバクラス以外は、内部クラスと呼ばれるものである。
 
本章ではどの場面でどのような理由からどのネストしたクラスを使用すべきか述べる。

### staticメンバクラス
staticメンバクラスはエンクロージングクラスのstaticなメンバの一つで、そのほかのstaticなメンバと同じアクセシビリティのルールに従う。
 
よくあるstaticメンバクラスの使い方の1つは、アウタークラスと伏せて使用した場合にのみ有効なpublic なヘルパークラスとしてである。
例として、計算機のオペレーションを表すenumを考える（Item34）。
オペレーションenumはCalculatorクラスのpublic staticなメンバークラスであるべき。
Calcuratorの利用者は、オペレーションを Calculator.Operation.PLUSや Calculator.Operation.PLUS のように参照できる。

### 非staticメンバクラス
非staticなメンバクラスのインスタンスは、暗黙的にエンクロージングインスタンスへの参照を持つ。
非staticなメンバクラスの中のインスタンスメソッドにおいて、エンクロージングインスタンスのメソッドを呼ぶことができ、qualified thisを使用してエンクロージングインスタンスへの参照を得ることができる。
（qualified thisはエンクロージングクラス.thisのことを指している）
エンクロージングインスタンス抜きで非staticなメンバクラスのインスタンスを生成することは不可能、つまり、独立にさせたいのならstaticメンバクラスを選択する必要がある。
 
非staticメンバクラスのインスタンスと、エンクロージングインスタンスの参照が形成されるのは、メンバクラスのインスタンスが生成されたときであり、そのあとに変更されることはない。
通常、エンクロージングクラスのインスタンスメソッドから、非staticなメンバクラスのコンストラクタが呼ばれることによって、参照が形成される。

非staticメンバクラスのよくある使い方は、Adapterである。
Adapterを用いると、エンクロージングクラスのインスタンスが別のクラスのインスタンスであるかのように見せることができる。
具体的には、MapのkeySetやvaluesメソッドで返されるcollection的な見た目のものは、非staticメンバクラスを使用している。
ListのIteratorなんかもそう。

```java
    public Iterator<E> iterator() {
        return new Itr();
    }

    /**
     * An optimized version of AbstractList.Itr
     */
    private class Itr implements Iterator<E> {
    ...
    }
```


もし、メンバクラスがエンクロージングインスタンスにアクセスする必要がないのであれば、常にstaticとして宣言しておくべきである。
なぜなら、この間の参照を生成するのに時間とメモリが食われるということと、この参照がなければガベージコレクションの対象となっているかもしれないからである（Item7)

private static なメンバークラスは、エンクロージングクラスのコンポーネントの一部として表される。
例えば、Mapインスタンスを考えてみると、多くのMapの実装では、Mapのなかのkey-valueのペアとしてEntryオブジェクトを保有する。
Entryのメソッド（getKey、getValue、setValue）はmapのメソッドにアクセスする必要がないので、entryを非staticなクラスにするのは無駄である。
非staticにしても動くが、mapへの余計な参照が増えるだけでメモリの無駄使いである。

ネストクラスについて、外部公開するか迷っている場合も、staticにするか非staticにするかの選択は重要である。
ネストクラスを外部公開した場合、非staticからstaticに変えることはできない。（後方互換性を犯すことになる）

### 匿名クラス
匿名クラスは他のクラスに属するというよりは、使用される時に宣言、インスタンス化が同時に行われるといえる。
匿名クラスは非staticな文脈であれば、エンクロージングクラスのインスタンスを保有することができる。
しかし、staticな文脈で匿名クラスが書かれていたとしても、constant variable(finalが付与されたprimitiveかStringの変数)でない限りはstaticメンバをもつことはできない。

#### 匿名クラスの制限
* 匿名クラスには以下のような制限がある。
* 宣言された箇所以外でインスタンス化することはできない
* instanceofでテストできないなど、クラスの名前が必要となる処理はできない
* 複数インターフェースを実装したり、クラスを継承してインターフェースを実装したりすることができない
* 匿名クラスの利用者は、匿名クラスのスーパークラスのから継承したものしか呼び出せない

lambdaが導入されるまでは、小さな関数オブジェクトやプロセスオブジェクト（？）を生成する手段として匿名クラスが用いられてきたが、現在はlambdaのほうが好まれる。
その他、匿名クラスのおもな使用例としては、staticなファクトリメソッドの実装で用いられる。（Item20）

### ローカル内部クラス
ローカル内部クラスは、ローカル変数と同様のかたちで宣言され、スコープも同じかんじ。
可読性のために短く保つべき。

## まとめ
ネストクラスは4つあり、それぞれ使い道が違う。
メソッドの外側でvisibleである必要があったり、メソッドの内部に置くには長すぎる時にはメンバクラスを用意する。
メンバクラスのそれぞれのインスタンスがエンクロージングクラスのインスタンスにアクセスする必要があるのならば、非staticにすべき。それ以外はstaticにすべき。

メソッド内のクラスに関して、1か所のみで使い、動きを規定してくれるような既存のクラスがある場合は匿名クラスを使う。それ以外はローカル内部クラスを使う。

# 25.1ファイルあたり1つのトップレベルクラスに制限せよ

1ファイルに複数のトップレベルクラスを定義することは可能だが、メリットは何もなく、リスクは存在する。

## 1ファイルに複数のトップレベルクラスを定義することの問題点

リスクとは、1つのクラス定義を複数してしまうというものである。複数定義されたうちのどれが使われるかは、ソースファイルがコンパイラーに渡された順に影響を受ける。
以下のような、2つのトップレベルクラスを参照するMainクラスを考える。

```java
public class Main {
    public static void main(String[] args) {
        System.out.println(Utensil.NAME + Dessert.NAME);
    }
}
```

Utensil.java という1つのファイルの中にUtensilクラスとDessertクラスを作る。

```java
class Utensil {
    static final String NAME = "pan";
}

class Dessert {
    static final String NAME = "cake";
}
```
この時Mainを実行すると、pancakeと表示が出る。

ここで、Dessert.java に以下のようなクラスを定義したとする。

```java
class Utensil {
    static final String NAME = "pot";
}

class Dessert {
    static final String NAME = "pie";
}
```

ここで、javac Main.java Dessert.java というコマンドでコンパイルを実行した場合、コンパイルは失敗し、UtensilとDessertというクラスが重複していることを教えてくれる。
この時、コンパイラはMain.javaをまず見に行き、Utensilへの参照を見たときに、Utensil.javaを見に行き、UtensilとDessertクラスを見つける。コンパイラーがDessert.javaを見に行くときには、再びUtensilとDessertの定義を見つける。
もし、javac Main.java または、javac Main.java Utensil.javaとした場合には、Dessert.javaを書く前と同様の結果（pancake表示）になる。
しかし、javac Dessert.java Main.javaとした場合には、potpieと表示される。

このように、プログラムの挙動はコンパイルされる順番に影響されてしまうようになる。

## 解決法
解決策としては、シンプルに1つのソースファイルには1つのトップレベルクラスしか定義しないようにすることである。

もしくは、staticなメンバクラス（Item24）として定義してやる。
そのクラスが他の1つのクラスへの補助的な役割をするものであるなら、staticなメンバークラスにすることによって、可読性が向上し、無駄なアクセスを抑制することができる（staticメンバクラスをprivateにする）。
以下がその具体例である。

```java
public class TestStaticMember {

    public static void main(String[] args) {
        System.out.println(Utensil.NAME + Dessert.NAME);
    }

    private static class Utensil {
        static final String NAME = "pan";
    }

    private static class Dessert {
        static final String NAME = "cake";
    }
}
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
以下が例となる。

```java
package tryAny.effectiveJava;

//Annotation type with a parameter
import java.lang.annotation.ElementType;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 *  * Indicates that the annotated method is a test method that  * must throw
 * the designated exception to succeed.  
 */

// Repeatable annotation type
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Repeatable(ExceptionTestContainer.class)
public @interface ExceptionTest {
    Class<? extends Exception> value();

}
```

```java
package tryAny.effectiveJava;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface ExceptionTestContainer {
    ExceptionTest[] value();
}
```
アノテーションの付与の仕方は以下のよう。

```java
// Code containing a repeated annotation
@ExceptionTest(IndexOutOfBoundsException.class)
@ExceptionTest(NullPointerException.class)
public static void doublyBad() { ... }
```

```@Repeatable``` を処理する際には注意が必要である。繰り返し使用されるアノテーションは、それを格納するアノテーションと組み合わせて作成される。
```getAnnotationsByType``` メソッドはこのことを隠ぺいし、繰り返し使用されるアノテーションとそうではないアノテーションの場合の両方にアクセスが可能である。一方で、```isAnnotationsPresent``` メソッドは繰り返し使用されるアノテーションに対して、それを格納するアノテーションであると判断してしまう。つまり、繰り返し使用されているアノテーションの型を```isAnnotationsPresent``` メソッドで、その繰り返し使用されている型であると判断することはできないということだ。
繰り返し使用されるアノテーションと、そうでないアノテーションのどちらも検知するためには、格納しているアノテーションと要素のアノテーションどちらもチェックする必要がある。
以下がアノテーション繰り返し使用に耐えうるよう書き直したものとなる。

```java
// Processing repeatable annotations
if (m.isAnnotationPresent(ExceptionTest.class) || m.isAnnotationPresent(ExceptionTestContainer.class)) {
    tests++;
    try {
        m.invoke(null);
        System.out.printf("Test %s failed: no exception%n", m);
    } catch (Throwable wrappedExc) {
        Throwable exc = wrappedExc.getCause();
        int oldPassed = passed;
        ExceptionTest[] excTests = m.getAnnotationsByType(ExceptionTest.class);
        for (ExceptionTest excTest : excTests) {
            if (excTest.value().isInstance(exc)) {
                passed++;
                break;
            }
        }
        if (passed == oldPassed)
            System.out.printf("Test %s failed: %s %n", m, exc);
    }
}
```

```@Repeatable``` の使用が可読性を高めると感じるのであれば使うべきであるが、これを使用した場合には繰り返し使用したアノテーションの処理が煩雑になることを覚えておくべきである。

本章のテスティングフレームワークは簡単なものであるが、アノテーション使用のネーミングパターンに対する優位性を示した。

たいていのプログラマは自身でアノテーションを定義することはない。Java標準のアノテーションやIDEやツールが提供してくれるアノテーションを使うべきである。

# 40.一貫してOverrideアノテーションを使うべし

Javaライブラリはいくつかのアノテーションを提供してるが、多くのプログラマにとって、```@Override``` が一番重要だろう。
一貫して```@Override``` を使用していれば、バグが起こりにくくなる。
以下の[bigram](https://www.weblio.jp/content/bigram)を模したクラスを例に見ていく（バグあり）。

```java
package tryAny.effectiveJava;

import java.util.HashSet;
import java.util.Set;

//Can you spot the bug?
public class Bigram {
    private final char first;
    private final char second;

    public Bigram(char first, char second) {
        this.first = first;
        this.second = second;
    }

    public boolean equals(Bigram b) {
        return b.first == first && b.second == second;
    }

    public int hashCode() {
        return 31 * first + second;
    }

    public static void main(String[] args) {
        Set<Bigram> s = new HashSet<>();
        for (int i = 0; i < 10; i++)
            for (char ch = 'a'; ch <= 'z'; ch++)
                s.add(new Bigram(ch, ch));
        System.out.println(s.size());
    }
}
```
このプログラムは26を出力すると思いきや、260を出力する。
原因はequalsをOverrideするつもりがOverloadしてしまっていることにある。```Object.equals```の引数はObject型であり、シグニチャが違う。
こういった誤りを防ぐために、Overrideするメソッドには```@Override```をつける。そうすると以下のコードはコンパイルエラーとなる。

```java
@Override public boolean equals(Bigram b) {
    return b.first == first && b.second == second;
}
```
正しくは以下のようになる。

```java
@Override
public boolean equals(Object o) {
    if (!(o instanceof Bigram))
        return false;
    Bigram b = (Bigram) o;
    return b.first == first && b.second == second;
}
```

このようなことから、**親クラスのメソッドをOverrideするときは@Overrideをつけるべきである**。
これには一つ例外があって、具象クラスにおいて、親の抽象メソッドをOverrideするときは、そもそもOverrideしないとコンパイルエラーが出るので、```@Override```の記述の必要はない（記述による害もない）。


# 41.型定義のためにマーカーインターフェースを使うべし

[マーカーインターフェース](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%BC%E3%82%AB%E3%83%BC%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%95%E3%82%A7%E3%83%BC%E3%82%B9)とは、メソッド定義を含まず、単にそのインターフェースを実装したクラスが特定の属性を持っていることを示すためのものである。
例として、```Serializable```インターフェースがあげられる（12章）。このインターフェースを実装することで、そのクラスのインスタンスは```ObjectOutputStream```に書き込み可能であることが示される。

マーカーアノテーション（Item39）の登場で、マーカーインターフェースは時代遅れになったように思えるかもしれないが、それは誤りである。
マーカーインターフェースはマーカーアノテーションに比べて、2つの点でアドバンテージがある。
1つ目は**マーカーインターフェースは型を定義するが、マーカーアノテーションはしない**ことである。これによって、マーカーアノテーションでは実行時まで捕捉できないエラーがコンパイル時に捕捉できることとなる。
Javaのシリアライゼーション機能では、型がシリアライザブルであることを示すために、```Serializable```マーカーインターフェースを使用している。```ObjectOutputStream.writeObject```メソッドでは、渡されたオブジェクトをシリアライズするが、その引数はシリアライザブルであることを求める。このメソッドの引数が```Serializable```であれば（実際にはObjectをとる）、不適切な型の引数が来た場合にコンパイルで検知できる。
2つ目は**マーカーインターフェースの方がより簡潔に対象を絞れる**ことにある。
マーカーアノテーションのターゲットが```ElementType.TYPE```である場合は全てのクラスとインターフェースが対象となるが、マーカーインターフェースの場合はそれを実装しているクラスに限られる。
```Set``` インターフェースは、そのような制限するマーカーインターフェースである。
SetはCollectionのサブタイプにのみ実装されるが、Collectionで定義されたメソッドに何も付け加えていない。SetはCollectionのメソッドの一部を再定義しているので、一般にマーカーインターフェースとはみなされていない。
しかし、特定のインターフェースのサブタイプにのみ適用され、インターフェースのメソッドを再定義しないマーカーインターフェースは想像しやすい。そのようなマーカーインターフェースは、オブジェクト全体のある不変値（?）を記述したり、そのインスタンスは他の特定のクラスのメソッドによって処理されるように適合していることを指し示す（この意味では、```Serializable```インターフェースは、そのインスタンスが```ObjectOutputStream```に処理されることに適合していることを指し示している）。

**マーカーアノテーションの利点は、大きなアノテーション機能の一部であるという点にある。**それゆえ、マーカーアノテーションはアノテーションベースのフレームワークで一貫性が考慮されている。

## マーカーアノテーション、マーカーインターフェースをどう使い分けるか？
まず、クラスとインターフェース以外の要素にマーカーをつけるには、マーカーアノテーションを使用するしかない。
クラス、インターフェースへのマーカーに関しては、
***このマーキングをしたオブジェクトのみを対象としたメソッドを1つ以上書くことがあるか？***
を考えてみる。
もし書くことがあるなら、マーカーインターフェースを利用するべき。これによって、メソッドの引数の型チェックをコンパイル時に行うことができる。
もし書かないのであれば、マーカーアノテーションを利用すべき。
アノテーションをたくさん使うフレームワークにおけるマーキングであれば、マーカーアノテーションを選ぶべき。


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
  * ラムダ式は関数型インターフェースの型にしか代入できないので、複数のメソッドを持つインターフェースや、抽象クラスのインスタンスが必要となる場合は匿名クラスを使う
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
  * 中心的なのは```UnaryOperator<T>```、```BinaryOperator<T>```、```Predicate<T>```,```Function<T>```,```Consumer<T>```,```Supplier<T>```の6つ。(6)
  * 上の6つそれぞれに```int```、```long```、```double```のプリミティブ型を扱うための関数型インターフェースがある。（18）
  * Functionには*Src*To*Result*Functionで6つ。*Src*ToObjFucntionで3つある。(9)
  * 引数を2つ取るものが9つある。(9)
  * BooleanSupplierなるものがある。(1)
* プリミティブ型に対応していない関数型インターフェースでプリミティブ型をボクシングしたオブジェクトを使ってはならない。性能が悪くなる。
* 自身で関数型インターフェースを書く必要があるのは以下の場合。
  * 引数を3つ取る関数型インターフェースなど標準で用意されていないものが必要となる場合。
  * 一般的に使われていて記述から恩恵を受けれらる、強い関連性をもった契約がある（**よくわからん**）、defaultメソッドから恩恵が受けられる、といった特徴がある場合。(```Comparator<T>```が例に挙げられている)
* 関数型インターフェースを書く際には、必ず@FunctionalInterfaceをつける。これがあれば、誤った書き方をしていた場合にコンパイルエラーにしてくれる。
* 関数型インターフェースを引数に取るメソッドはオーバーライドすべきでない。（Item52）

# 45.Streamは気を付けて使うべし
* Streamパイプラインの処理は終端処理が呼ばれて初めて実行される。
* 簡単に並列Streamにすることができるが、たいていの場合、並列にするのは適切でない。（Item48）
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

# 46.副作用のないストリーム処理を選択すべし

## ストリームによるパラダイムの変化
ストリームは単なるAPIでなく、関数型プログラミングに根ざしたパラダイム（ものの見方？）の変化であり、そのパラダイムに適応しなければならない。
ストリームのパラダイムで最も重要な部分は、演算を純粋関数による変換の連続の結果、という構造にするところにある。純粋関数とは、結果がそのインプットにのみ依存し、mutableな状態には依存せず、他の状態を変更しないものを指す。
このパラダイムを達成するために、ストリームにおける中間操作、終端操作は副作用と無縁のものにせねばならない。

以下、ファイルに含まれる単語の頻度を求めるプログラムをみていく。

```java
// Uses the streams API but not the paradigm--Don't do this!
Map<String, Long> freq = new HashMap<>();
try (Stream<String> words = new Scanner(file).tokens()) {
    words.forEach(word -> {
        freq.merge(word.toLowerCase(), 1L, Long::sum);
    });
}
```
ストリーム、ラムダ式、メソッド参照を使い、結果も正しいが、これはストリームAPIの利点を引き出せていない。
問題は、forEachの中で外部の状態（freq変数）を変更していることにある。一般に、ストリームのforEachで結果の表示以外をしているコードは、状態を変化させているコードなので、悪いコードである可能性がある。

以下が本来あるべき姿。

```java
// Proper use of streams to initialize a frequency table
Map<String, Long> freq;
try (Stream<String> words = new Scanner(file).tokens()) {
    freq = words
        .collect(groupingBy(String::toLowerCase, counting()));
}
```
**forEachは、ストリームの演算の結果を示すために使うべきで、演算そのものに使うべきではない。**

## collectorの利用
上記の改良コードでは、collectorを利用しており、ストリームを使うには欠かせない。
Collectors APIは39個のメソッドがあり、また、最大で5つの引数をとるメソッドがあり、恐ろしげに見える。しかし、深く入り込まずともこのAPIを利用することはできる。最初はCollectorのインターフェースは無視して、リダクション（ストリームの要素を一つのオブジェクトにまとめる）を行うものと考える。

ストリームの要素をcollectionにするメソッドとして、```toList()```, ```toSet()```, ```toCollection()```がある。これらはそれぞれ、list、set、任意のcollectionを返す。これらを使って頻度表のトップ10を抽出したのが以下になる。

```java
// Pipeline to get a top-ten list of words from a frequency table
List<String> topTen = freq.keySet().stream()
    .sorted(comparing(freq::get).reversed())
    .limit(10)
    .collect(toList());
```
上記コードでは前提となっているが、ストリームパイプラインの可読性のために、Collectorsのメンバーはstaticインポートしておくべきである。

### toMapメソッド
上の3つを除いた残りの36メソッドは、ほとんどストリームをMapにするためのものである。
最もシンプルなのは、```toMap(keyMapper, valueMapper)```で、ストリームをキーにする関数とストリームをバリューにする関数を引数にとる。例は以下のよう。

```java
// Using a toMap collector to make a map from string to enum
private static final Map<String, Operation> stringToEnum =
    Stream.of(values()).collect(
        toMap(Object::toString, e -> e));
```
上記のコードは、同じキーが複数あった場合には```IllegalStateException```をスローする。
このような衝突を防ぐための方法の1つとして、引数にマージ関数（```BinaryOperator<V>```でVはMapのバリューの型）を持たせることがある。
以下の例は、Albumオブジェクトのストリームからartist毎に最も売れたAlbumのMapを作成している。

```java
// Collector to generate a map from key to chosen element for key
Map<Artist, Album> topHits = albums.collect(
   toMap(Album::artist, a->a, maxBy(comparing(Album::sales))));
```

3つの引数を取る```toMap```メソッドのそのほかの使用法は、キーが衝突したときに、最後に書き込まれたものが正となるような使い方である。この時のコード例は以下のようである。

```java
// Collector to impose last-write-wins policy
toMap(keyMapper, valueMapper, (oldVal, newVal) -> newVal)
```

4つの引数を取る```toMap```メソッドもあり、4つ目の引数には返り値の実装となるMapを指定する。

### groupingByメソッド
Collectors APIには```toMap```メソッドの他にも、```groupingBy```メソッドなるものがある。
```groupingBy``` メソッドはclassifier関数をもとに要素をカテゴリー分けしたMapを生成する。
classifier関数とは、要素を受けて、その要素のカテゴリー（Mapのキー）を返す関数である。
Item45で例示したアナグラムプログラムの中で使われていたものがそれにあたる。

```java
words.collect(groupingBy(word -> alphabetize(word)))
```

groupingByメソッドで、バリューがList以外のMapを生成するcollectorを返すには、classifier関数に加えて、downstream collectorを特定してやる必要がある。
最もシンプルな例では、このパラメータにtoSetを渡してやるとMapのバリューはListでなく、Setになる。
そのほかのgroupingByメソッドの2つ引数を取るシンプルな例としては、downstream collectorにcounting()を渡すことがある。
counting()では各カテゴリー内の要素数を集約できる。その実例が本章の最初で提示した頻度テーブルの例である。

```java
Map<String, Long> freq = words
        .collect(groupingBy(String::toLowerCase, counting()));
```

3つ引数を取るgroupingByメソッドでは、生成するMapの型を特定することができる。（ただし、2番目の引数にMapのファクトリが来て、3番目にdownstream collectorが来るようになる）

### その他のメソッド
countingメソッドはdownstream collectorとしての利用に特化したものであり、同様の機能はStreamから直接得られるので、```collect(counting())```のような呼び出しはしてはならない。
このような特性のメソッドはCollectorsの中にあと15個あり、それらの内9つはsumming,averaging,summarizingから始まるメソッド名である。
そのほかに、Streamのメソッドと似た、reducing、filtering, mapping, flatMapping、collectingAndThen メソッドがある。

Collectorsのメソッドでまだ言及していないものが3つあるが、それらはcollectorsとあまり関わりがない。
最初の2つは```minBy```と```maxBy```メソッドである。これらは引数にComparatorをとり、ストリームの要素から最小、最大の要素を返す。

最後のCollectorsのメソッドは```joining```で、これは```CharSequence```インスタンス（Stringとか）のストリームの操作のみを行う。
引数なしのjoiningは要素を結合するのみのcollectorを返す。
引数が1つのjoiningはdelimiterを引数に取り、要素間にdelimiterを挟みこむcollectorを返す。
引数が3つのjoiningはdelimiterに加え、prefixとsuffixを引数に取る。delimiterがコンマで、prefixが[で、suffixが]だと、
```
[came, saw, conquered].
```
のようになる。

# 47.戻り値の型としてストリームよりCollectionを選択すべし
## 連続した要素をどの型で返すべきか？
連続した要素の戻り値型としてあり得るのは、collectionインターフェース、Iterable、配列、ストリームである。

### ストリームで返す
ストリームで返すのが善であると聞くかもしれないが、Item45で述べたように、ストリームとイテレーションをうまくすみ分けることが重要である。

StreamはIterableを継承していないため、ストリームとして返ってきた値をfor-each文でまわすのには、Streamのiteratorメソッドを使うしかない。
ぱっとみ以下のコードようにiteratorメソッド使ってうまくいくように思える。

```java
// Won't compile, due to limitations on Java's type inference
for (ProcessHandle ph : ProcessHandle.allProcesses()::iterator) {
    // Process the process
}
```
しかし、このコードはコンパイルできず、以下のようにキャストをしてやる必要がある。

```java
// Hideous workaround to iterate over a stream
for  (ProcessHandle ph : (Iterable<ProcessHandle>)
                        ProcessHandle.allProcesses()::iterator)
```
このコードは動くものの、乱雑で分かりにくい。
代替方法としては、アダプターメソッドを使う方法がある。JDKではそのようなメソッドは提供されていないが、以下のように簡単に書ける。

```java
// Adapter from  Stream<E> to Iterable<E>
public static <E> Iterable<E> iterableOf(Stream<E> stream) {
    return stream::iterator;
}
```
このアダプターメソッドを使うことによって、ストリームに対して以下のようにfor-eachを回すことが可能となる。

```java
for (ProcessHandle p : iterableOf(ProcessHandle.allProcesses())) {
    // Process the process
}
```

### Iterableで返す
逆に、クライアント側でストリームとして処理しようとしているのに、戻り値はIterableにのみ対応したものであるときも対応が必要である。
この対応もJDKでは用意されていないが、以下のようなに簡単に対応メソッドを書ける。

```java
// Adapter from Iterable<E> to Stream<E>
public static <E> Stream<E> streamOf(Iterable<E> iterable) {
    return StreamSupport.stream(iterable.spliterator(), false);
}
```

### Collectionで返す
CollectionインターフェースはIterableのサブタイプであり、ストリームのメソッドも持っているので、イテレーション処理でもストリーム処理でも対応できる。
そのため、**連続した要素を返すメソッドの最適な戻り値型は、たいていの場合、Collectionか適切なCollectionのサブタイプである**と言える。
もし返却する連続要素が十分小さければ、ArrayListやHashSetなどのCollectionを実装したものを返せばいいのだが、**Collectionとして返却するために、大きな連続要素をメモリに蓄えることはすべきでない。**

返却する連続要素が、大きいけれど簡潔に表現できるものであれば、特別にcollectionを実装してやることを考える。
例えば、与えられた集合のべき集合を返すような実装を考える。
べき集合とは、例えば、{a,b,c}のべき集合は、{{}, {a}, {b}, {c}, {a, b}, {a, c}, {b, c}, {a, b, c}}のようであり、n個の要素の集合があれば、２のn乗個のべき集合ができる。
とても大きな数の集合になるため、べき集合をスタンダードなcollectionの中に入れようと考えてはならない。
これを実現するカスタムcollectionは、AbstractListを使って簡単に実装することができる。
仕組みとしては、集合の各要素にインデックスを付して、それらが存在するかしないかをbitで判断する、というものである。コードは以下のようになる。

```java
package tryAny.effectiveJava;

import java.util.AbstractList;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

//Returns the power set of an input set as custom collection
public class PowerSet {
    public static final <E> Collection<Set<E>> of(Set<E> s) {
        List<E> src = new ArrayList<>(s);
        if (src.size() > 30)
            throw new IllegalArgumentException("Set too big " + s);
        return new AbstractList<Set<E>>() {
            @Override
            public int size() {
                return 1 << src.size(); // 2 to the power srcSize
            }

            @Override
            public boolean contains(Object o) {
                return o instanceof Set && src.containsAll((Set) o);
            }

            @Override
            public Set<E> get(int index) {
                Set<E> result = new HashSet<>();
                for (int i = 0; index != 0; i++, index >>= 1)
                    if ((index & 1) == 1)
                        result.add(src.get(i));
                return result;
            }
        };
    }
}
```
上記のコードでは、集合が30以上の要素を持っている場合には例外をスローさせるようにしている。
これはCollectionのsizeメソッドで返せる最大値が2の31乗-1であることによる。


どの型で返すかを、実装の難易度だけで決めることもある。
例えば、インプットのlistの全てのサブリストを返却するようなメソッドを書くような場合を考える。
サブリストを作り出して、それらを標準のcollectionに入れるコードは3行で書けるが、メモリが2次元構造のcollectionを保持しなくてはならない。
これは指数関数的に増えるべき集合に比べれば悪くないが、受け入れられない。
べき集合の時のようにカスタムcollectionを実装するのは面倒である。

しかし、リストの全サブリストをストリームで返すのは、少し工夫をすれば直接的に実装できる。
リストの最初の文字を保持しているサブリスト群をprefixesと呼ぶ。つまり、(a, b, c)のprefixesは(a), (a, b), (a, b, c)になる。
リストの最後の文字を保持しているサブリスト群をsuffixesと呼ぶ。つまり、(a, b, c)のsuffixesは(a, b, c), (b, c), (c)になる。
このとき、リストの全サブリストは、リストのprefixesのsuffixesと、空のリストである。実装は以下のようになる。

```java
package tryAny.effectiveJava;

import java.util.Collections;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

//Returns a stream of all the sublists of its input list
public class SubLists {
    public static <E> Stream<List<E>> of(List<E> list) {
        return Stream.concat(Stream.of(Collections.emptyList()), prefixes(list).flatMap(SubLists::suffixes));
    }

    private static <E> Stream<List<E>> prefixes(List<E> list) {
        return IntStream.rangeClosed(1, list.size()).mapToObj(end -> list.subList(0, end));
    }

    private static <E> Stream<List<E>> suffixes(List<E> list) {
        return IntStream.range(0, list.size()).mapToObj(start -> list.subList(start, list.size()));
    }
}
```
このコードは以下のような通常のforループのネストしたものと同様の考え方をしている。

```java
for (int start = 0; start < src.size(); start++)
    for (int end = start + 1; end <= src.size(); end++)
        System.out.println(src.subList(start, end));
```
このforループをストリーム処理に直訳した形で表すと、簡潔にはなるが、可読性は落ちる。具体的には以下のようになる。

```java
// Returns a stream of all the sublists of its input list
public static <E> Stream<List<E>> of(List<E> list) {
   return IntStream.range(0, list.size())
      .mapToObj(start ->
         IntStream.rangeClosed(start + 1, list.size())
            .mapToObj(end -> list.subList(start, end)))
      .flatMap(x -> x);
}
```
どちらの実装も悪くないが、使用するユーザーによってはストリームからイテレートできるように変換するコードが必用となる、または、イテレート処理が自然なところでストリーム処理を行わなければならないかもしれない。
ストリームからイテレートできるように変換するコードは、クライアントコードが乱雑になるだけでなく、Collectionでの実装に比べて、性能的にも問題がある。

# 48.ストリーム処理を並列で行う際は注意せよ

## 並列処理は依然として困難
Javaの進化に伴い、並列プログラミングは書きやすくなったものの、正しく、速い並列処理の実装を書くことは依然として難しい。これはストリームのparallelストリームでの処理も例外でない。
Item45の例をみてみる。

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
このプログラムのストリーム処理にparallel()を入れても、処理が速くなるどころか、処理は完了せず、CPUが高止まりし続ける。

ここでは何が起こっているのか？
簡単には、ストリームのライブラリがこのパイプラインをどのように並列化するか分からず、ヒューリスティックな解が失敗したということが原因である。
**もともとStream.iterateから来ていたり、limit中間操作が行われる場合は、パイプラインの並列化は性能を上げにくい。**上記のプログラムはこのどちらの要素も持ってしまっている。
ここでの教訓は、**見境なく並列ストリームを使ってはならない**ということだ。

概して、**並列化でパフォーマンス向上が見込めるのは、ArrayList、HashMap、HashSet、ConcurrentHashMap、配列、intの範囲をもったもの、longの範囲を持ったもののストリームに対しての並列化である。**
これらの共通点は、サブレンジへの分割が容易であることである。
これらのデータ構造が持つもう一つの重要な共通点は、逐次処理される時の**[参照の局所性](https://ja.wikipedia.org/wiki/%E5%8F%82%E7%85%A7%E3%81%AE%E5%B1%80%E6%89%80%E6%80%A7)**である。

終端操作も並列処理の性能に響いてくる。
パイプラインの全体に比して、大量の処理を終端処理で行い、かつ、その終端処理が内部的に逐次処理を行うものであったら、パイプラインの並列化はあまり効果を得られない。
一番効果を得られる終端処理は、min、max、count、sumといったリダクション処理である。
また、anyMatch、allMatch、noneMatchといった[短絡評価](https://ja.wikipedia.org/wiki/%E7%9F%AD%E7%B5%A1%E8%A9%95%E4%BE%A1)は並列化の効果を得やすい。
ストリームのcollectメソッドによって行われる可変リダクション操作は、並列化の恩恵を受けにくい。なぜなら、コレクションを結びつける処理のオーバーヘッドがコストとなるからだ。

### Safety failure 
**ストリームの並列化によって、liveness failureを含む性能面の問題が起こるだけでなく、間違った結果や予期しない動作を招くこともある。（safety failure）**
safety failureはストリームの厳しい仕様にのっとっていない関数を使用した場合に発生する。
例えば、ストリームに渡されるaccumulate（蓄積させる）する関数とコンバインする関数は、[結合的](https://docs.oracle.com/javase/jp/8/docs/api/java/util/stream/package-summary.html#Associativity)で、[非干渉](https://docs.oracle.com/javase/jp/8/docs/api/java/util/stream/package-summary.html#NonInterference)で、[ステートレス](https://docs.oracle.com/javase/jp/8/docs/api/java/util/stream/package-summary.html#Statelessness)な関数でなければならない。
これを守れずとも、直線的なパイプラインであれば問題は起きないが、並列化されたパイプラインだと悲惨な結果になりうる。

### 並列化して効果があるのか？
とても良い条件で並列処理ができたとしても、並列化したコストを相殺するような性能を見せなければ意味がない。
荒く見積もって、(ストリームの要素の数)*(1要素に実行されるコード行数) > 100000 を満たすべきである（リンク元見ると10000のような。。（http://gee.cs.oswego.edu/dl/html/StreamParallelGuidance.html））。

ストリームの並列化はパフォーマンス最適化である、ということは認識しておくべき。
どのような最適化でも、その変更前後でテストをしてやる価値があるか確かめねばならない。理想的には、テストは本番環境で行うべきである。

### 並列化は正しい状況下で使えばとても有用
**正しい状況下で並列化を行えば、プロセッサ数と比例するような性能向上が見込める。**
機械学習やデータ処理の分野ではこれらの性能向上がしやすい。

並列化が効率的に行える、[素数計数関数](https://ja.wikipedia.org/wiki/%E7%B4%A0%E6%95%B0%E8%A8%88%E6%95%B0%E9%96%A2%E6%95%B0)の例を見ていく。

```java
package tryAny.effectiveJava;

import java.math.BigInteger;
import java.util.stream.LongStream;

public class ParallelTest1 {
    // Prime-counting stream pipeline - benefits from parallelization
    static long pi(long n) {
        return LongStream.rangeClosed(2, n).mapToObj(BigInteger::valueOf).filter(i -> i.isProbablePrime(50)).count();
    }

    public static void main(String[] args) {
        StopWatch sw = new StopWatch();
        sw.start();
        System.out.println(pi(10000000));
        sw.stop();
        System.out.println(sw.getTime());
    }
}
```
上記のコードを処理するのに42秒くらいかかった。これを並列化する。

```java
package tryAny.effectiveJava;

import java.math.BigInteger;
import java.util.stream.LongStream;

import org.apache.commons.lang3.time.StopWatch;

public class ParallelTest1 {
    // Prime-counting stream pipeline - benefits from parallelization
    static long pi(long n) {
        return LongStream.rangeClosed(2, n).parallel().mapToObj(BigInteger::valueOf).filter(i -> i.isProbablePrime(50))
                .count();
    }

    public static void main(String[] args) {
        StopWatch sw = new StopWatch();
        sw.start();
        System.out.println(pi(10000000));
        sw.stop();
        System.out.println(sw.getTime());
    }
}
```
こうすると23秒くらいで終了した。（2コアのマシンで実行）

### ランダム値のストリームを並列化する場合
ランダム値の生成を並列で行うのならば、ThreadLocalRandomよりもSplittableRandomを使うべき。



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


# 61.ボクシングされたプリミティブ型（boxed primitive）より、プリミティブ型（primitive）を選択すべし
## ボクシングされたプリミティブ型とプリミティブ型の違い
Item6でも述べられれているように、オートボクシングとオートアンボクシングにより、ボクシングされたプリミティブ型（以下boxed primitive）とプリミティブ型（以下primitive）の違いはあいまいになっている。
しかし、これらの2つには違いがあり、使用時にはその差異に気を付けながら使わなければならない。その違いは3つで、
* primitiveは値のみを持つが、boxed primitiveは値とは異なる形で参照を持つ。
* primitiveは機能する値しか持ちえないが、boxed primitiveはnull（nonfunctional value）があり得る。
* primitiveのほうが、時間的にも省メモリスペース的にも優れている。

## boxed primitiveを使用した場合の誤り例

### primitiveは値のみを持つが、boxed primitiveは値とは異なる形で参照を持つ
以下のコードは一見うまく比較をしてくれるメソッドにみえる。

```java
// Broken comparator - can you spot the flaw?
Comparator<Integer> naturalOrder =
    (i, j) -> (i < j) ? -1 : (i == j ? 0 : 1);
```
しかし、このメソッドを```naturalOrder.compare(new Integer(42), new Integer(42))```のように用いると、想定としては等しいので0を返すはずだが、実際には1を返す。
1つ目の判定（i < j）は、auto-unboxedされて正しく動作する。
一方、2つ目の判定（i == j）は、同値であることをみる、つまり、参照が同じであるかをみている。よって、この比較はtrueにはならず、結果として1が返却される。 boxed primitiveに対して==演算子を用いることはたいてい間違っている。

上記の誤りを防ぐためには、```Comparator.naturalOrder()```を用いるか、自身でcomparatorを書くのであれば、以下のようにprimitiveでの比較を行うようにする。

```java
Comparator<Integer> naturalOrder = (iBoxed, jBoxed) -> {
    int i = iBoxed, j = jBoxed; // Auto-unboxing
    return i < j ? -1 : (i == j ? 0 : 1);
};
```

### primitiveは機能する値しか持ちえないが、boxed primitiveはnull（nonfunctional value）があり得る

以下のプログラムでは、ヌルポが発生する。

```java
package tryAny.effectiveJava;

public class BoxedPrimitive {
    static Integer i;

    public static void main(String[] args) {
        if (i == 42)
            System.out.println("Unbelievable");
    }

}
```
i==47のところで、Integerとintを比較している。
boxed primitiveとprimitiveが混じった処理においては、**たいていの場合boxed primitiveがauto-unboxされる。**
nullを参照しているオブジェクトをunboxするとヌルポが生じるが、それがここでは起きている。

### primitiveのほうが、時間的にも省メモリスペース的にも優れている
以下は、Item6で扱ったプログラムである。

```java
package tryAny.effectiveJava;

public class BoxedPrimitive2 {
    // Hideously slow program! Can you spot the object creation?
    public static void main(String[] args) {
        Long sum = 0L;
        for (long i = 0; i < Integer.MAX_VALUE; i++) {
            sum += i;
        }
        System.out.println(sum);
    }

}
```
box化、unbox化が繰り返し起こるため、これはローカル変数の型をlongにした場合よりも格段に遅い。

## 総括
3つの問題点があったが、最初の2つは結果がおかしくなり、最後の1つは性能が悪くなる。

boxed primitiveの使い時としては以下の場合がある。
* collectionの要素、キー、バリューとして使うとき。primitiveをcollectionに入れることはできないので使わざるを得ない。
* パラメータ化された型に用いるとき。例えば、```ThreadLocal<int>```という型は宣言できないが、```ThreadLocal<Integer>```は宣言できる。
* リフレクションでメソッドを参照するときはboxed primitiveを使う（？）。（Item65）

# 62.他の型が適している場合にはStringを避けるべし
## Stringが適していない場面でもStringが使われがち
本章では、Stringを使うべきではない場面について述べる。

### 他の型の代替として使うべきでない
ファイル、ネットワーク、キーボードからくるデータをStringとして扱うことが多いが、本当にStringとして扱う場合のみにとどめるべきである。
入ってくるデータが数字なのであれば、int、float、BigIntegerなどが、真偽値であればenumやbooleanが適切である。
より一般的には、値の適切な型があるのであれば、それを使うべきで、適切な型がないのであれば、作成すべきである。
このアドバイスは当たり前のようであるが、よくおこるミスである。

### enumの代替として使うべきでない
Item34で述べられているが、Stringで定数の列挙を行うべきでない。enumを使うべし。

### 要素を集結させるもの（aggregate type）として使うべきでない
複数の要素を持つものがあったとして、それをStringで表現するのはbadアイデアだ。以下がそれにあたる。

```java
// Inappropriate use of string as aggregate type
String compoundKey = className + "#" + i.next();
```
この方法には複数の悪い点がある。
* 区切り文字として使われている文字が要素に入ってくると面倒なことになる。
* 個々の要素を取り出すために、パースをしなければならないため、遅く、エラーを生み出しやすい。
* equals、toString、compareToといったメソッドを提供できないが、Stringが提供するメソッドは受け入れることを強制される。（？）

ベターな方法としては、単純に、要素をまとめるクラスを書くことだ。よくprivate staticなメンバークラスが作られる（Item24）。

### 偽造不可能なキー（capability）として使うべきでない
Stringは何らかの機能へのアクセス手段として使われることがある。
例として、ThreadLocalの変数格納機能を考えてみる。
ThreadLocalはそれぞれのスレッドの固有の値を格納できるものとして機能する。この機能は、Java1.2以降にJavaライブラリに現れたが、それ以前にこういった機能を設計しようとしたら、以下のようにStringを使って実現してしまうかもしれない。

```java
// Broken - inappropriate use of string as capability!
public class ThreadLocal {
    private ThreadLocal() { } // Noninstantiable
 // Sets the current thread's value for the named variable.
    public static void set(String key, Object value);
 // Returns the current thread's value for the named variable.
    public static Object get(String key);
}
```
上記のようにしたときの問題点は、Stringのキーがグローバルな名前空間として共有されてしまうことにある。
そのため、意図せず別々のユーザーが1つの変数を共有してしまうかもしれず、エラーを生むことになる。

また、セキュリティの観点からも良くない。
悪意のあるユーザーがわざと他のユーザーのキーと同じ値でThreadLocalから値を取得する可能性があるからだ。

上記を代替不可能なキー（unforgeable key または、capability）を使って書き換えると以下のようになる。

```java
public class ThreadLocal {
    private ThreadLocal() { }    // Noninstantiable
 public static class Key {    // (Capability)
        Key() { }
    }
 // Generates a unique, unforgeable key
    public static Key getKey() {
        return new Key();
    }
 public static void set(Key key, Object value);
    public static Object get(Key key);
}
```
上記でStringのキーを使った場合の問題は解消されているが、さらに良い方法がある。
staticなメソッドはもう必要なく、インスタンスメソッドがキーとなる（？）。
その時点でキーはスレッドローカルな変数を指し示すキーではなく、キー自体がスレッドローカルな変数となっている（？）。
APIとしては以下のよう。

```java
public final class ThreadLocal {
    public ThreadLocal();
    public void set(Object value);
    public Object get();
}
```
上記のAPIから値を取り出すときはキャストをしなければならないので、このAPIはタイプセーフではない。
元のStringをキーとしたAPIや、Keyを使ったAPIでもタイプセーフにするのは難しいが、上記のAPIは以下のように、容易にタイプセーフにできる。

```java
public final class ThreadLocal<T> {
    public ThreadLocal();
    public void set(T value);
    public T get();
}
```
javaライブラリのThreadLocalもざっくりいうと上のようになっている。


# 63.文字結合のパフォーマンスに気を付けよ
文字結合を数多く行う場合には、+演算子による結合ではなく、StringBuilderを使うべし。
Stringはimmutableなので、文字結合するごとに新しいオブジェクトが作成されてしまう。

Stringを使った文字結合の例が以下。

```java
// Inappropriate use of string concatenation - Performs poorly!
public String statement() {
    String result = "";
    for (int i = 0; i < numItems(); i++)
        result += lineForItem(i);  // String concatenation
    return result;
}
```

StringBuilderを使った場合が以下。

```java
public String statement() {
    StringBuilder b = new StringBuilder(numItems() * LINE_WIDTH);
    for (int i = 0; i < numItems(); i++)
        b.append(lineForItem(i));
    return b.toString();
}
```

# 64.インターフェースを参照するようにせよ
## インターフェースで型を宣言しといた方が柔軟な設計になる
**適切なインターフェース型あるならば、引数、戻り値、変数、フィールド全てがインターフェース型で宣言されるべきである。**
オブジェクトクラスを参照するのはコンストラクタにおいてのみである。

以下、Setインターフェースの実装クラスである、LinkedHashSetを例に見ていく。

```java
// Good - uses interface as type
Set<Son> sonSet = new LinkedHashSet<>();
```
上記はいい例。

```java
// Bad - uses class as type!
LinkedHashSet<Son> sonSet = new LinkedHashSet<>();
```
上記は悪い例。

インターフェースで宣言した例だと、以下のように変えるだけで、実装クラスが基本的にエラーなく変えられる（インターフェースで宣言しているメソッドのみ使用しているため）。

```java
Set<Son> sonSet = new HashSet<>();
```
ただし、気を付けなくてはいけないのは、インターフェースでは規定されていない機能に依存したコードである場合には、実装クラスを変える影響があり得るということだ。
例えば、LinkedHashSetの並び変えのポリシーに依存していた場合には、HashSetに実装を変えた時に影響が出るだろう。

## 適切なインターフェースがない時
適切なインターフェースがない時は、クラスの型で宣言を行うのが正しい。

### value class
例えば、StringやBigIntegerなどの値を表すクラス（value class）を考えてみる。
value classは複数の実装があることがまずない。また、おおむねfinalなクラスであり、対応するインターフェースがない。
value classは引数、変数、フィールド、戻り値の型として適している。

### クラスベースのフレームワークを使っているとき
クラスベースのフレームワークを使用しており、適切な基盤の型がインターフェースでなくて、クラスであるときがある。
そういった場合も適したクラス（だいたいabstract）を継承するのが良い。
java.ioのOutputStreamなどはこれに当たる。

### 適したインターフェースはないが、実装クラスに適したメソッドが実装されているケース
例えば、PriorityQueueにはcomparatorメソッドがあるが、Queueインターフェースにはない。もしcomparatorメソッドに依存するプログラムを書くのであれば、PriorityQueueを参照する。ただし、このようなケースはレアである。


上記3つのケースは網羅的なものではなく、クラスで参照するなんとなくの場面について伝えたものである。

**もし適したインターフェースがない場合は、目的の機能を持っている一番抽象度の高いクラスを参照すべき。**

# 65.リフレクションよりインターフェースを選択すべき
## リフレクションはパワフルな機能だが、欠点もある

リフレクションの欠点は以下。
* コンパイル時の型チェックで受ける恩恵を失う
* リフレクティブなアクセスをするコードは洗練されておらず、冗長である
* 通常のメソッド呼び出しに比べて、リフレクションでのメソッド呼び出しは遅い

分析ツールや依存性注入フレームワーク等のリフレクションを利用した洗練されたアプリケーションはあるが、それらでもリフレクションの欠点がみえるにつれ、リフレクションから離れていってる。もし、リフレクションを使うべきか迷ったとしたら、おそらく使わないのが正しい。

## リフレクションを使うケース
リフレクションはとても限られたケースで使う。
コンパイル時には得られないクラスを利用せねばならない多くのプログラムでは、コンパイル時に、そのクラスを入れる型として、適切な型、スーパークラスが存在している（Item64）。
このケースでは、リフレクティブにインスタンスを作成し、インターフェースやスーパークラス経由でそれら生成されたインスタンスにアクセスする。
例として、以下のプログラムでは、第一引数で特定される、```Set<String>```のサブクラスのインスタンスを作り、他のコマンドライン引数をそのSetの中に詰め込んで標準出力する。
HashSetを第一引数にとるとランダムで表示されるが、TreeSetを第一引数にとるとアルファベット順で表示される。

```java
package tryAny.effectiveJava;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.Arrays;
import java.util.Set;

public class Reflection {
    // Reflective instantiation with interface access
    public static void main(String[] args) {
        // Translate the class name into a Class object
        Class<? extends Set<String>> cl = null;
        try {
            cl = (Class<? extends Set<String>>) // Unchecked cast!
            Class.forName(args[0]);
        } catch (ClassNotFoundException e) {

            fatalError("Class not found.");
        }
        // Get the constructor
        Constructor<? extends Set<String>> cons = null;
        try {
            cons = cl.getDeclaredConstructor();
        } catch (NoSuchMethodException e) {
            fatalError("No parameterless constructor");
        }
        // Instantiate the set
        Set<String> s = null;
        try {
            s = cons.newInstance();
        } catch (IllegalAccessException e) {
            fatalError("Constructor not accessible");
        } catch (InstantiationException e) {
            fatalError("Class not instantiable.");
        } catch (InvocationTargetException e) {
            fatalError("Constructor threw " + e.getCause());
        } catch (ClassCastException e) {
            fatalError("Class doesn't implement Set");
        }
        // Exercise the set
        s.addAll(Arrays.asList(args).subList(1, args.length));
        System.out.println(s);
    }

    private static void fatalError(String msg) {
        System.err.println(msg);
        System.exit(1);
    }

}
```
上記で使われるテクニックは本格的なservice provider framework（？Item1）で使われるくらい強力なものである。
だいたいこのテクニックがリフレクションで必要なすべてである。

上記には2つ欠点がある。
* 6つの実行時エラーが出うる。これらはリフレクションを使わなければコンパイル時に検出できるエラーである。
* 名称からインスタンスを生成するのに25行もかかってしまっている。通常のコンストラクタなら1行ですむのに。

上記のコードではキャスト時にwarningが出ている。
仮に第一引数に取る名称がSetの実装クラスでなくとも、```Class<? extends Set<String>>```へのキャストは成功するので、この警告は正当なものである。
warningの抑制についてはItem27をみるべし。

リフレクションを使う非常にレアなケースとして、パッケージの複数のバージョンを動的に使う場合がある。
一番古いバージョンをコンパイルしておいて、動的に新しいクラスのメソッドを呼び出すなどを行う。（全然ぴんと来ない）

# 66.nativeメソッドは気を付けて使うべし
## native メソッド
Java Native Interface（JNI）を使って、CやC++で書かれたメソッドを呼べる。

歴史的に、nativeメソッドには3つの用途がある。
* windowsのレジストリなど、プラットフォーム特有の機能へアクセスするため
* レガシーなデータにアクセスするライブラリを含む、nativeコードのライブラリを使うため
* パフォーマンス向上のため
プラットフォーム特有の機能にアクセスするためにnativeメソッドを使うことは正当である。
とはいえ、Javaは成熟してきたので、だいたいの機能はある。例えば、Java9ではOSのプロセスにアクセスできたりする。
また、Javaにはないライブラリがnativeライブラリにある場合も、nativeメソッドを使ってよい。

性能のためにnativeメソッドを使うことはあまりない。
初期のJavaではそのようなことがあったらしいが、JVMの進化によりそんなに性能は変わらなくなっている。

## nativeメソッドの欠点
nativeメソッドには大きな欠点がある。
* nativeメソッドはsafe（BOFとかが起きないという意味の、メモリ管理的な安全のことだと思う）でないので（Item50）、nativeメソッドを使っているアプリケーションは、Javaとは言え、メモリ破損のエラーに対して免疫があるとは言えなくなる。
* nativeメソッドはプラットフォームに大きく依存するので、移植性がなくなる。
* デバッグがむずい
* 下手すると性能劣化する。ガベージコレクターがうまく働かないことがあり得るし、nativeコードを行き来するコストがかさむためだ。
* 可読性が低く、冗長な記述が必要なグルーコードが必用。

つまり、よく考えてnativeメソッドを使えということ。

# 67.最適化は気を付けて行うべし
## 速いプログラムよりも良いプログラムを目指す
プログラムの最適化を安易に行わないように促す格言は、昔からある。

最適化のために健全なアーキテクチャを破壊してはならない。
健全なアーキテクチャが保てているのであれば、個々のコンポーネントは疎な関係を保てているはずなので、それらは後から他には影響を与えずに変更することができる。

かといって、プログラムが完成するまで性能のことを考えなくてよいわけではない。
普及したアーキテクチャの欠陥を修正することはほぼ無理である。
そのため、設計の段階で性能に関する考慮は十分にしておかなければならない。

## 性能を制限してしまう設計は避ける
コンポーネントの設計で、一度決まった後に変更するが一番困難なのは、外界とコンポーネントの境界部分である。
主な例としては、
* API
* wire-levelのプロトコル（SOAPとかCORBAとか）
* 永続化データの形式
などである。

## API設計での性能について考える
API設計において、パフォーマンスについて考えねばならない。
* publicな型をmutableにすると、不必要なdefensive copyがたくさん必要になるかもしれない（Item50）。
* publicクラスに継承を用いるとスーパークラスによって性能制限を受け続けるかもしれない（Item18）（いまいちよくわからない）。
* APIにインターフェースでなく、実装型を用意した場合には、より良い実装が未来になされた場合に変更しにくい（Item64）。

実例として、java.awt.Component クラスのgetSizeメソッドは呼び出すたびにmutableな Dimension インターフェースを生成することになっており、性能影響が出てしまう。

本来的には、Dimensionはimmutable（Item17）であるべきであった。また、getSizeメソッドは個々のDimensionオブジェクトのコンポーネントを返す2つのメソッドに置き換えられるべきであった（ぴんと来ない）。
実際、Componentクラスに、そのようなメソッドがJava2では用意されたが、以前からgetSizeを用いているコードはなおも性能問題を抱えている。

一般に、良いAPI設計には良いパフォーマンスがついてくるものである。
**パフォーマンス向上のためにAPIをゆがませるのは筋が悪い。**
そこで得られたパフォーマンス向上は、将来のプラットフォーム変更で消し飛びうるが、ゆがんだAPIを保守する難点はずっと抱えていかねばならない。

## 最適化
うまく設計、実装ができた後になお、性能向上が必用であった場合には、最適化を試みる。

### パフォーマンスを測る
最適化をした前後でパフォーマンス測定を行う必要がある。
どのプログラムの実行に時間がかかっているか予測するのは困難であるため、時間を無駄にしないためにも計測をしながら最適化をすすめていく。

### プロファイリングツール
プロファイリングツールを利用することで、どのメソッドがどれくらい時間がかかり、何回呼ばれているかが分かる。
この時に、アルゴリズムの選択が間違っていないか見ることができる。
アルゴリズムの選択によって、性能は劇的に変わるため、適切なものにする。

また、マイクロベンチマーキングフレームワークである、JMHというツールもある。
これにより、Javaコードの詳細なパフォーマンス情報を可視化できる。

### Javaにおける計測の必要性
Javaでの性能計測は、CやC++といった昔の言語よりもの必要性が大きい。
なぜなら、それらの言語に比べ、CPUで実行される処理と、コードで表現されていることの乖離が大きいからである。

また、Javaでは、実装、リリースのバージョン、プロセッサによって性能がことなる。
違うプラットフォーム上で動くことが分かったとしたら、各々の環境で性能測定をすることが重要である。
その結果として、環境ごとの性能のトレードオフが発生することがしばしばある。

Javaが動く環境はますます複雑化してきているので、パフォーマンスの予想はよりつかなくなってきている。
よって、測定の必要性も増してきていると言える。


# 68.命名慣習には従うべし
## 命名慣習
Javaの命名慣習はJLS6.1にうまくまとまっている。
大雑把にいって、命名慣習は表記的なもの（typographical）と文法的なもの（grammatical）に分けられる。

## typographical

### パッケージ名、モジュール名
パッケージ名、モジュール名はピリオドで区切られたコンポーネントで階層化されて表現される。
コンポーネントはアルファベットの小文字（とまれに数字）で表される。
組織外で使用されるパッケージには、組織のインターネットドメイン名を逆さにしたものから始める（com.googleなどのように）。このルールはjavaとjavaxから始まる標準パッケージに関しては適用範囲外である。ユーザーはjava、javaxで始まるパッケージ、モジュールを作成してはならない。
インターネットドメイン名をパッケージの接頭辞にする詳しいルールはJLS6.1に書いてある。

パッケージ名の残りは、1つ以上のコンポーネント名から構成される。
コンポーネント名は一般に、8文字以下の短い文字列（略語など）であることが推奨される。

### クラス名、インターフェース名
列挙型、注釈型含むクラス名、インターフェース名の名前は、各単語の先頭一文字を大文字にした単語で構成する。
頭字語とmax、min等の一般的な略語を除いて、略語の使用は控えるべきである。
頭字語について、全部大文字で記載するか、先頭一文字のみ大文字にするか、議論の分かれるところであるが、見やすさの観点からここでは先頭一文字を大文字にする法を推したい。

### メソッド名、フィールド名
メソッド名、フィールド名は基本的に、最初の一文字目を小文字にする、というところ以外はクラス名、インターフェース名の規則と同じである。
この規則の唯一の例外は、定数フィールドでは大文字の単語をアンダースコアで区切るようにする。（NEGATIVE_INFINITY）

### ローカル変数
ローカル変数の命名慣習は、フィールド変数のそれとほぼ同じであるが、ローカル変数では文脈に沿った略語を命名することが認められている（i,denom,houseNum等）。
引数となる変数に関しては、メソッドのドキュメントに統合するものとなるので、注意深く命名してやる必要がある。

### 型パラメータ
型パラメータは基本的に一文字で構成される。
Tは任意の型、Eはコレクションの要素の型、KとVはmapのキーと値の型、Xは例外の型、Rは戻り値の型をあらわす。
また、任意の型を複数使う場合の順序は、T、U、VまたはT1、T2、T3である。

## grammatical
命名に関する文法的な規則は、表記規則より柔軟で議論の余地がある。
### パッケージ名、モジュール名
パッケージについては文法上の命名規則はない。

### クラス名、インターフェース名
列挙型を含む、インスタンス化可能なクラスは、単数名詞、名詞句で名前が付けられる（Thread,PriorityQueue,ChessPieceなど）。
インスタンス化しないクラスは、名詞の複数形で命名されることが多い（Collectors,Collectionsなど）。
インターフェースは、クラスと同様の命名規則であったり（Collection,Comparatorなど）、末尾が形容詞的な終わり方になっていたり（Runnable,Iterable,Accessibleなど）する。
注釈型については、様々な用途があるので、これまでに出てきたいずれにも当てはまらない。名詞、動詞、前置詞、形容詞すべてよく使われる（BindingAnnotation, Inject, ImplementedBy,Singletonなど）。

### メソッド名
何らかのアクションを実行するメソッドは、一般的に、動詞、動詞句で命名される（append,drawImageなど）。
booleanを返すメソッドは、isまたはhasで始まり、名詞、名詞句、または形容詞として機能する言葉が続くように命名される（isDigit, isProbablePrime, isEmpty, isEnabled, hasSiblingsなど）。
boolean以外の値を返すものや、オブジェクトの属性を返すメソッドは、名詞、名詞句、getで始まる動詞句で名前が付けられる。
getで始まる動詞句だけが認めれるとする声があるが、その根拠は乏しい。
名詞、名詞句の命名方法を使ったほうが、たいていは可読性が上がる。

```java
if (car.speed() > 2 * SPEED_LIMIT)
    generateAudibleAlert("Watch out for cops!");
```


いくつかのメソッド命名規則には特別な言及が必要である。
インスタンスの型を変換し、独立したオブジェクトとして返すメソッドはtoTypeメソッドと呼ばれたりする（toString、toArrayなど）。
受け取ったオブジェクトと異なる型のオブジェクトを返すメソッドはasTypeメソッドと呼ばれたりする（asListなど）。
呼び出されるオブジェクトと同じ値のプリミティブな値を返すメソッドはtypeValueメソッドと呼ばれたりする（intValueなど）。
ファクトリメソッドの一般的な名前はinclude from, of, valueOf, instance, getInstance, newInstance, getType, newTypeなどがある（Item1）。

### フィールド名、ローカル変数
フィールド名の文法規則はそれほど重要でない。なぜなら、ちゃんと設計されたAPIでは、公開されるフィールドがほとんどないからである。
boolean型のフィールドはアクセサメソッドの最初の文字列だけ消えたものが採用されることが多い（initialized,compositeなど）。
その他のフィールドでは名詞、名詞句であることが多い（height,digits,bodyStyle）。
ローカル変数の文法規則はフィールドよりもっと緩い。

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
# 85.Javaでシリアライズするより、他の方法を考えよ
## シリアライズは脆弱
シリアライゼーションの根本的な問題は、攻撃可能な個所が大きすぎ、その個所もコンスタントに広がっているという点にある。
オブジェクトグラフ（参照による結びつきをもったオブジェクト群というイメージ）は、ObjectInputStreamのreadObjectメソッドで、復元される。
このメソッドでは、型がSerializableを実装している限り、クラスパス上のほぼすべての型のオブジェクトをインスタンス化することができる。
バイトストリームをデシリアライズする過程で、このメソッドはクラスパス上にありSerializeを実装しているあらゆる型のコードを実行しできる。よって、これらすべての型が攻撃対象となる。

### ガジェット、ガジェットチェーン
攻撃対象となりうるserializableなクラスから脆弱性を取り除いたとしても、アプリケーション自体はまだ脆弱であるかもしれない。
serializableな型のメソッドから、危険な処理をしうるメソッド（ガジェットと呼ばれる）を組み合わせて、ガジェットチェーンなるものを作れば、時に、任意のネイティブコードが実行できるようなことも起こる。実際に、2016年にSan Francisco Metropolitan Transit Agency Municipal Railwayに対してこの仕組みを使ったハックがなされた。

### デシリアライゼーションボム
上記のようにガジェットを用いずとも、デシリアライズに多大な時間がかかるストリームは簡単に作れて、これでDoS攻撃ができる。
そのようなストリームはデシリアライゼーションボムといわれる。

```java
// Deserialization bomb - deserializing this stream takes forever
static byte[] bomb() {
    Set<Object> root = new HashSet<>();
    Set<Object> s1 = root;
    Set<Object> s2 = new HashSet<>();
    for (int i = 0; i < 100; i++) {
        Set<Object> t1 = new HashSet<>();
        Set<Object> t2 = new HashSet<>();
        t1.add("foo"); // Make t1 unequal to t2
        s1.add(t1);  s1.add(t2);
        s2.add(t1);  s2.add(t2);
        s1 = t1;
        s2 = t2;
    }
    return serialize(root); // Method omitted for brevity
}
```
上記のコードでは、1つのHashSetが2つのHashSetの要素を持っているという構造が100階層続いている。
HashSetインスタンスを生成するときには、各要素のhashcodeを演算せねばならない。よって、2の100乗回のhashCodeの呼び出しが必要となり、全然処理が終わらなくなる。

## 対処法は？
シリアライズに関する、上記のような攻撃への対処はどのようにすればよいか？

### 他の仕組みを使う
**一番の方法はデシリアライズをしないことだ。**
**新たに書くシステムでJavaのシリアライズを使う理由は一つもない。**
バイトシーケンスとオブジェクトを翻訳するベターな仕組みが存在しており、それらはcross-platform structured-data representationsと呼ばれる。

#### JSONとProtobuf
代表的なcross-platform structured-data representationsはJSONとProtobufというものである。
JSONとProtobufで最も重要な相違点は、JSONはテキストベースで人間が読める形である一方、Protobufはバイナリでより効率的である点だ。

### 信頼できないデータはデシリアライズしない
レガシーなシステムの保守開発などでは、Javaでのシリアライズを避けられないかもしれない。
そういったときには、**信頼できないデータはデシリアライズしない**、という対策を取るべきだ。
特に、信頼できないソースからのRMIトラフィックは受け付けてはならない。

### デシリアライズ時のフィルタリング機能を使う
Javaでのシリアライズを避けられず、デシリアライズするデータの安全性も怪しい場合は、オブジェクトのデシリアライゼーションフィルタであるjava.io.ObjectInputFilter（Java9から導入され、6,7,8にもバックポートされた）を使用すべきだ。
これはストリームがデシリアライズされる前にフィルタリングしてくれる機能を提供してくれる。
クラス単位でリジェクトするかアクセプトするか決められる。この時、ホワイトリスト形式かブラックリスト形式か選択することができるが、ブラックリストは既知の脅威からしか防御できないのでホワイトリストを採用すべき。
フィルタリング機能は、過度なメモリの使用も防いでくれ、過度に深いオブジェクトグラフも防いでくれるが、前述のデシリアライゼーションボムを防ぐ機能はない。

# 86.Serializableを実装するときは十分に気をつけよ
## Serializableにするにあたってのコスト
Serializeにするのは秒でできるが、長期的には大きなコストとなるかもしれない。

### Serializableを実装すると、一度リリースした実装クラスを変更する柔軟性が失われる
クラスがSerializableを実装するということは、バイトストリームエンコーディングされたもの（以降、serialized form）は公開されたAPIの一部となる。
一度クラスを公開したとなれば、永久にそれをサポートすることが求められる。
また、カスタムしていないデフォルトのserialized formでは、privateなフィールドも公開APIの一部となるので、アクセスできるフィールドを最小限にする（Item15）設計が無意味になってしまう。

デフォルトのselialized formを受け入れ、後でクラスの内部表現を変えたとすると、互換性のない変化が起こってしまう。
クライアントが古いバージョンのクラスを使ってインスタンスをシリアライズし、新しいバージョンのクラスでデシリアライズした場合には問題が起きてしまう。
変換を行うことは可能であるが、困難であり、コードが汚くなってしまう。
Serializableを実装するときは長く使うことを考えて、高品質なものを設計するように心掛ける必要がある（Item87,90）。

Serializableの実装において課される制限の一例として、serial version UIDというものが関わってくる。
全てのSerializableなクラスは、serial version UIDという自身を証明するための番号をもっている。（**復元前後でクラスのバージョンが異なっていないかを識別する為のものらしい。**）（http://www.ne.jp/asahi/hishidama/home/tech/java/serial.html）
static final longなフィールドとしてこいつを定義しなかった場合、実行時に自動的に割り振られる。
この値はクラス名、メンバー等に影響を受け、何か変えると、この値も変わってしまう。
UIDを定義せず、互換性も壊れてしまった場合、InvalidClassExceptionが実行時に発生してしまう。

### Serializableを実装すると、バグ、セキュリティホールの可能性が増大する
デシリアライズは「みえないコンストラクタ」のようなものである。みえないがゆえに、コンストラクタによって確立された不変条件（invariant）を保証し、攻撃者に構築中のオブジェクトにアクセスさせないようにする必要があることを忘れがちである。
デフォルトのデシリアライゼーションメカニズムに頼っていると、容易にinvariantを破壊されたり、不正アクセスされたりすることになる。

### Serializableを実装すると、新しいバージョンのクラスをリリースする際にかかる手間が増える
Serializableを実装したクラスが改定されると、新しいバージョンのインスタンスがシリアライズ可能で、古いほうのバージョンでデシリアライズ可能か、また、その逆も調べなければならない。
そのため、バージョン数とシリアライズ実装クラスの積に比例する形でテストケースが増える。
テストの必要量は、Serializable実装クラスの初版が注意深く設計されて入れば減らすことができる（Item87,90）。

## Serializableの実装は気軽に決めてよいものではない
オブジェクトの移送や永続化にJavaのシリアライゼーションを使用しているフレームワークにクラスを組み込むためには、Serializableを実装することは不可欠である。
また、Serializableの実装によって、他のクラスからコンポーネントとして扱うことは容易となる。
しかし、前述の通り、Serializableの実装にはさまざまなコストがある。
クラスを設計する際には、それらを天秤にかける必要がある。

歴史的には、BigInteger,Instantクラスなどの値クラスはSerializableを実装するが、thread poolなどのアクティブなエンティティを表すクラスでは滅多に実装されない。

## 継承用に設計されたクラス、インターフェースは基本、Serializableを実装、継承すべきでない
このルールを破るとそのクラスのサブクラスとなるクラスに、多大な重荷を負わせることになる。
本ルールの例外として、関わるもの全てにSerializable実装を求めるフレームワークに存在するクラス、インターフェースはSerializableを実装することは理解できる。
ThrowableやComponentはSerializableを実装している。
ThrowableがSerializableを実装しているため、RMIはサーバーからクライアントに例外を飛ばすことができる。
ComponentがSerializableを実装しているため、GUIの要素は移送されたり、保存されたりする。SwingとAWTの全盛期でもこの機能はあまり使われていなかったが。

## Serializableで拡張可能でフィールドを持つクラスを実装する場合には気を付ける
インスタンスフィールドに何らかのinvariantがある場合には、サブクラスにはfinalizeメソッドをoverrideさせないようにせねばならない。
そうしないとfinalizer attackの危険（Item8）がある。

また、クラスのinvariantが、インスタンスフィールドの初期化によって壊れてしまうような場合には、readObjectNoDataメソッドを加える必要がある。

```java
private void readObjectNoData()
     throws ObjectStreamException;
```
（**この辺謎**）

## Serializableにしないとなったときの注意
継承用のクラスでSerializableにしないと選択したときに、シリアライザブルなサブクラスを書くのはより手間がかかる。
そのようなクラスの通常のデシリアライズでは、スーパークラスにアクセス可能な引数なしのコンストラクタが必要となる。
それが用意できない場合は、Serialization Proxy Pattern（Item90）を用いる。

## インナークラスはSerializableを実装すべきでない
インナークラスは合成フィールドを使用する。
合成フィールドは、コンパイラーが生成するもので、エンクロージングインスタンスへの参照と、エンクロージングスコープからのローカル変数への参照を保持する。

合成フィールドに対するシリアライズの形式は不定なので、インナークラスでのSerializable実装は避けるべき。
ただし、staticなメンバークラスはSerializable実装可。

# 87.カスタムserialized formの利用を考慮せよ
通常のserialized formを選択した場合、将来修正するということはできなくなると考えねばならない。

## 適切か否か考慮せずにデフォルトのserialized formを選択してはならない
一般に、カスタムserialized formを設計することを選んだ時のエンコーディング結果とほとんど変わらない場合の時だけ、デフォルトserialized formを選ぶべき。
デフォルトserialized formはオブジェクトグラフの物理表現を効率的にエンコーディングしたものである。
つまり、

### デフォルトserialized formでいい場合
**デフォルトserialized formはオブジェクトの物理表現と論理コンテンツが一致している場合に適切であることが多い。**
例えば以下のような、シンプルに人の名前を表現したクラスは、デフォルトserialized formが向いている。

```java
// Good candidate for default serialized form
public class Name implements Serializable {

    /**
     * must be non-null
     * @serial
     */
    private final String lastName;

    /**
     * must be non-null
     * @serial
     */
    private final String firstName;

    /**
     * Middle name, or null if there is none
     * @serial
     */
    private final String middleName;

    public Name(String lastName, String firstName, String middleName) {
        super();
        this.lastName = lastName;
        this.firstName = firstName;
        this.middleName = middleName;
    }

}
```

Nameのインスタンスフィールドが論理的内容と対応している。

**デフォルトserialized formが適切だと判断した場合でも、不変条件やセキュリティを確保するためにreadObjectメソッドを提供せねばならないときもある。**
上記のNameの場合であれば、lastNameとfirstNameがnullでないことを、readObjectメソッドが保証せねばならない。このことはItem88,90で詳細に述べる。

NameのlastName,firstName,middleNameはprivateなフィールドであるにもかかわらず、ドキュメントが付されている。
その理由は、これらのprivateフィールドは、クラスのserialized formとして公開されるからである。
@serialというタグをつけると、生成されるJavadocでserialized formに関する専用ページを作れる。

### デフォルトserialized formが向いてない場合
Nameクラスとは真逆に位置するものとして、以下のような文字列のリストを表すクラスを考える。

```java
// デフォルトserialized formにしてはならない！
public final class StringList implements Serializable {
    private int size = 0;
    private Entry head = null;

    private static class Entry {
        String data;
        Entry previous;
        Entry next;
    }
}
```
論理的には、このクラスは文字列のシーケンスを表している。物理的には、双方向リストとしてのシーケンスを表している。
デフォルトserialized formを受け入れるとすると、serialized formは、連結リストの全要素と、entry間の全リンクを反映したものとなる。

**物理的な表現と論理的な内容の間で乖離がある場合に、デフォルトserialized formを使うことには4つのディスアドバンテージがある。**
* 公開APIとその時の内部表現が、永続的に蜜結合となってしまう
* メモリ空間をめっちゃ食う
* 時間めっちゃ食う
* スタックオーバーフロー起きうる
（**難しくてよくわからん**）

### 改訂版StringList

StringListの合理的なserialized formは、数個の文字列で構成されたlistである。
この構成は、StringListの論理的なデータの表し方である。
以下がwriteObjectとreadObjectを使った、改訂版のStringListである。

```java
package tryAny.effectiveJava;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

// 改良を加えたStringList
public final class StringList2 implements Serializable {
    private transient int size = 0;
    private transient Entry head = null;

    // No longer Serializable
    private static class Entry {
        String data;
        Entry previous;
        Entry next;
    }

    // listに文字列を加える
    public final void add(String s) {

    }

    private void writeObject(ObjectOutputStream s) throws IOException {
        s.defaultWriteObject();
        s.writeInt(size);

        for (Entry e = head; e != null; e = e.next) {
            s.writeObject(e.data);
        }
    }

    private void readObject(ObjectInputStream s) throws IOException, ClassNotFoundException {
        s.defaultReadObject();
        int numElements = s.readInt();

        for (int i = 0; i < numElements; i++) {
            add((String) s.readObject());
        }
    }
}
```

上記のクラスにおいて、writeObjectはまずdefaultWriteObjectメソッドを呼び出し、readObjectはまずdefautlReadObjectメソッドを呼び出している。
クラスの全フィールドがtransientである場合には、defaultWriteObjectメソッド、defautlReadObjectメソッドを呼び出す必要がないといわれることがあるが、そんなことはなく、呼び出さねばならない。
これらの呼び出しがあることで、のちのリリースでtransientでないフィールドを、互換性を保ちながら追加することが可能となる。

性能面に関して、10文字の文字列が10個連なったリストで計測したとき、改訂版StringListは、以前のメモリ量の半分程度になり、シリアライズの速さも倍となり、スタックオーバーフローの心配もなくなった。


### Objectの不変条件が実装と結びつかない場合
hashテーブルの物理的な実装は、hash bucketsの中にキーのハッシュ値が連なったものである。
キーのhash値は実装によって異なるので、デフォルトのserialized formを用いると深刻なバグを生む。

### transient
デフォルトserialized formを利用するかどうかに関わらず、defaultWriteObject を呼び出すと transient 指定されたフィールド以外のフィールドはすべてシリアライズされる。不必要なシリアライズを避けるために、できるだけtransient修飾子をつけるようにする。

transientが付されたフィールドはデシリアライズされたときに、デフォルトの初期値になっている。つまり、参照型変数であればnull、intなどなら0、booleanであればfalseになっている。
それが許容できないのであれば、readObjectメソッドにて設定をするか（Item88）、使用時に遅延初期化する（Item83）。

### 他のメソッドで同期をとっている場合は、シリアライズ時も同期をとる
シリアライズ時も同期をとる必要があるので、writeObjectにもsynchronizedをつける必要がある。

###　serialVersionUIDを明示する
明示することによって、ソースの非互換を防ぐことができる（Item86）。また、serialVersionUIDを実行時に生成しなくてよいので、ちょっとだけ性能が良くなる。
新しくクラスを書く場合には、この番号は何でもよく、別に一意な値でなくともよい。

現存するクラスにUIDを付与し、互換性も保とうとする場合は、古いバージョンのUIDにしてやる必要がある。


# 88.防御的にreadObjectメソッドを書くべし
Item50では、ミュータブルなprivate Dateフィールドを持った、イミュータブルな日付のレンジクラスがあった。
そこでは、コンストラクタとアクセサでDateオブジェクトの防御的コピーを用いることでイミュータブルであることを守っていた。

```java
package tryAny.effectiveJava;

import java.io.Serializable;
import java.util.Date;

public final class Period implements Serializable {
    private final Date start;
    private final Date end;

    /**
     * @param start
     *            the beginning of the period
     * @param end
     *            the end of the period; must not precede start
     * @throws IllegalArgumentException
     *             if start is after end
     * @throws NullPointerException
     *             if start or end is null
     */
    public Period(Date start, Date end) {
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
        if (this.start.compareTo(this.end) > 0)
            throw new IllegalArgumentException(this.start + " after " + this.end);
    }

    public Date start() {
        return new Date(start.getTime());
    }

    public Date end() {
        return new Date(end.getTime());
    }

    public String toString() {
        return start + "-" + end;
    }

}
```

このクラスをSerializableにすることを考える。
物理的な構造と、論理的なデータ内容に齟齬がないため、デフォルトのserialized formを用いる、すなわち、Serializableを実装するだけでよいように思えるが、そのようにすると、不変条件が保たれなくなる。

readObjectメソッドは実質的にpublicなコンストラクタであり、その他のコンストラクタと同様のケアが必要であるという点で問題がある。
コンストラクタでは引数をチェックする必要がある（Item49）のと、必用に際して引数のディフェンシブコピーが要る（Item50）。そのため、readObjectでも同様の考慮がいる。
readObjectでこれらの考慮をし忘れると、攻撃者は不変条件を破ることが可能となる。


## 悪いバイトストリームを流し込むケース
大雑把に言うと、readObjectはバイトストリームを一つの引数として扱うコンストラクタである。
通常、バイトストリームは普通に構築されたインスタンスをシリアライズすることによって生み出されたものである。
問題となるのは、不変条件を犯すために人為的に構築されたバイトストリームである。そのようなバイトストリームは、通常あり得ないオブジェクトの生成を行ってしまう。
下記がその一例（Periodのendがstartよりも前に来てしまう）であるが、自分の環境だと、
```
Exception in thread "main" java.lang.IllegalArgumentException: java.lang.ClassNotFoundException: Period
	at tryAny.effectiveJava.BogusPeriod.deserialize(BogusPeriod.java:31)
	at tryAny.effectiveJava.BogusPeriod.main(BogusPeriod.java:20)
```
が出てしまう。。

```java
package tryAny.effectiveJava;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.ObjectInputStream;

public class BogusPeriod {
    // Byte stream could not have come from real Period instance
    private static final byte[] serializedForm = new byte[] { (byte) 0xac, (byte) 0xed, 0x00, 0x05, 0x73, 0x72, 0x00,
            0x06, 0x50, 0x65, 0x72, 0x69, 0x6f, 0x64, 0x40, 0x7e, (byte) 0xf8, 0x2b, 0x4f, 0x46, (byte) 0xc0,
            (byte) 0xf4, 0x02, 0x00, 0x02, 0x4c, 0x00, 0x03, 0x65, 0x6e, 0x64, 0x74, 0x00, 0x10, 0x4c, 0x6a, 0x61, 0x76,
            0x61, 0x2f, 0x75, 0x74, 0x69, 0x6c, 0x2f, 0x44, 0x61, 0x74, 0x65, 0x3b, 0x4c, 0x00, 0x05, 0x73, 0x74, 0x61,
            0x72, 0x74, 0x71, 0x00, 0x7e, 0x00, 0x01, 0x78, 0x70, 0x73, 0x72, 0x00, 0x0e, 0x6a, 0x61, 0x76, 0x61, 0x2e,
            0x75, 0x74, 0x69, 0x6c, 0x2e, 0x44, 0x61, 0x74, 0x65, 0x68, 0x6a, (byte) 0x81, 0x01, 0x4b, 0x59, 0x74, 0x19,
            0x03, 0x00, 0x00, 0x78, 0x70, 0x77, 0x08, 0x00, 0x00, 0x00, 0x66, (byte) 0xdf, 0x6e, 0x1e, 0x00, 0x78, 0x73,
            0x71, 0x00, 0x7e, 0x00, 0x03, 0x77, 0x08, 0x00, 0x00, 0x00, (byte) 0xd5, 0x17, 0x69, 0x22, 0x00, 0x78 };

    public static void main(String[] args) {
        Period p = (Period) deserialize(serializedForm);
        System.out.println(p);
    }

    // Returns the object with the specified serialized form
    public static Object deserialize(byte[] sf) {
        try {
            InputStream is = new ByteArrayInputStream(sf);
            ObjectInputStream ois = new ObjectInputStream(is);
            return ois.readObject();
        } catch (Exception e) {
            throw new IllegalArgumentException(e.toString());
        }
    }

}
```

上のクラスは本来だと、endの日付がstartの日付より前になったものが表示されるはずであり、これはクラスの不変条件を破っている。

この攻撃を防ぐためには、下記のようにreadObjectメソッドでバリデーションチェックをかけてやる必要がある。
```java
    private void readObject(ObjectInputStream s) throws IOException, ClassNotFoundException {
        s.defaultReadObject();

        if (start.compareTo(end) > 0) {
            throw new InvalidObjectException(start + "after" + end);
        }
    }
```

## 悪い参照を付け加える
上の攻撃は防げたとしても、Periodの条件を守りながらインスタンスを作成し、末尾にPeriodのprivateフィールドのDateへの参照を付け加えることも可能である。

つまり、攻撃者はObjectInputStreamからPeriodインスタンスを読み込み、そのストリームに付与された「悪いオブジェクト参照」を読み込む。
これらの参照によって、攻撃者は、Periodオブジェクト内のDateインスタンスへの参照を得られ、Periodインスタンスを変更することが可能となる。
以下がその例。

```java
package tryAny.effectiveJava;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Date;

public class MutablePeriod {
    public final Period period;

    public final Date start;
    public final Date end;

    public MutablePeriod() {
        try {
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(bos);
            // Period インスタンスの書き込み
            out.writeObject(new Period(new Date(), new Date()));
            // Period インスタンスの特定のプロパティへの参照を作成
            byte[] ref = { 0x71, 0, 0x7e, 0, 5 };
            bos.write(ref);
            ref[4] = 4;
            bos.write(ref);

            // 可変な Period インスタンスの生成
            ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bos.toByteArray()));
            period = (Period) in.readObject();
            start = (Date) in.readObject();
            end = (Date) in.readObject();
        } catch (IOException | ClassNotFoundException e) {
            throw new AssertionError(e);
        }
    }

    public static void main(String[] args) {
        MutablePeriod mp = new MutablePeriod();
        Period p = mp.period;
        Date pEnd = mp.end;

        // Let's turn back the clock
        pEnd.setYear(78);
        System.out.println(p);

        // Bring back the 60s!
        pEnd.setYear(69);
        System.out.println(p);
    }
}
```

このプログラムを実行すると、以下のように出力される。

```
Mon Oct 08 18:43:49 JST 2018-Sun Oct 08 18:43:49 JST 1978
Mon Oct 08 18:43:49 JST 2018-Wed Oct 08 18:43:49 JST 1969
```

Periodインスタンスをそのままにしておくと、内部のコンポーネントを自由に操作されてしまう。
そうなると、Periodのimmutabilityにセキュリティ面で依存しているシステムは、攻撃をされうる。

原因としては、PeriodのreadObjectメソッドにおいて、防御的コピーを取れていなかったことにある。
**オブジェクトがデシリアライズされる時、クライアントが保持してはならないオブジェクト参照を含むフィールドについては、防御的コピーを取ることが必須である。**
具体的には、以下のようなreadObjectにしておくべき。（このとき、startとendはfinalではなくなる）

```java
    private void readObject(ObjectInputStream s) throws IOException, ClassNotFoundException {
        s.defaultReadObject();

        start = new Date(start.getTime());
        end = new Date(end.getTime());

        if (start.compareTo(end) > 0) {
            throw new InvalidObjectException(start + "after" + end);
        }
    }
```

こうすることで、MutablePeriodの実行においても以下のようになり、不正は起こらない。

```java
Mon Oct 08 20:19:56 JST 2018-Mon Oct 08 20:19:56 JST 2018
Mon Oct 08 20:19:56 JST 2018-Mon Oct 08 20:19:56 JST 2018
```

## readObjectがデフォルトのままでよいか否かのリトマス紙：コンストラクタでどうか
transientでないフィールドを引数にとるpublicなコンストラクタを作ること、また、その引数をバリデーションかけずともよいかどうかを問うべき。
もしそれがだめならば、readObjectにおいても防御的コピーを取り、バリデーションチェックをかける必要がある。
代替手段としては、serialization proxy pattern（Item90）を使用するべき。

そのほかのreadObjectとコンストラクタの類似点として、readObjectメソッドの内部で、直接的であれ間接的であれoverrideされうるメソッドを利用してはならない（Item19）。
利用した場合には、オーバーライドされたメソッドが呼び出され、サブクラスの状態がデシリアライズされないまま実行され、エラーとなりうる。

## まとめ
readObjectを書く時のガイドラインを以下にまとめる。

* オブジェクト参照を持つフィールドはprivateにし、防御的コピーを取る。immutableなクラスのmutableなコンポーネントはこれに当たる。
* 不変条件をチェックし、破られた場合はInvalidObjectExceptionをなげる。
* デシリアライズされた後に、オブジェクトグラフ全体にバリデーションをかける必要があるならば、ObjectInputValidationインターフェースを使う。（本書では語らない）
* オーバーライドされうるメソッドは直接的にも間接的にも呼ばない。

# 89.インスタンス制御に対しては、readResolve より enum 型を選ぶべし
Item3で以下のような例でシングルトンパターンを紹介した。

```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();

    private Elvis() {
    ...
    }

    public void leaveTheBuilding() {
    ...
    }
}
```

このクラスはSerializableを実装すると、シングルトンではなくなってしまう。
デフォルトserialized formであるかカスタムserialized form であるかに関わらず、また、readObjectメソッドを提供するか（Item87）に関わらず、シングルトンではなくなってしまう。
readObjectメソッドはデフォルトのものであれ、そうでないものであれ、クラス初期化時に作られたものとは違う、新しく作成したインスタンスを返すようになっている。

## readResolve
readResolveメソッドを使うことで、readObjectで作成されたオブジェクトとは別のインスタンスを返すことができる。

もし、デシリアライズされるクラスが適切にreadResolveメソッドを定義していたら、このメソッドは新しく作成されたオブジェクトに対して、デシリアライズされた後に呼び出される。
このメソッドによって返される参照は、新しく作成されたオブジェクトの代わりとなるものである。この機能を用いると、大体の場合新しく作成されたオブジェクトに対する参照はなくなり、新しく作成されたオブジェクトはすぐにガベージコレクションによって処理可能となる。

上記のElvisクラスがSerializableを実装した場合、以下のようにreadResolveメソッドを付ければシングルトンであることを保証できる。

```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();

    private Elvis() {
    ...
    }

    public void leaveTheBuilding() {
    ...
    }
    private Object readResolve() {
        return INSTANCE;
    }
}
```

このreadResolveメソッドでは、デシリアライズされたオブジェクトを無視し、クラス初期化時に作成されたインスタンスを返却する。
そのため、シリアライズされたElvisインスタンスは何らかのデータを持ってはならない。つまり、すべてのフィールドはtransientで宣言されていなければならない。

**もしreadResolveでインスタンスのコントロールをしようとするならば、参照を持つすべてのフィールドにはtransientをつけねばならない**。
そうでなければ、Item88で見せた例のような攻撃が、readResolveが走る前に行われる可能性がある。

攻撃は少し複雑だが、そのアイデアはシンプルなものである。

まず、stealerクラスを書く。
stealerクラスには、readResolveメソッドと、stealerが隠ぺいするシングルトンのフィールドがある。
シリアライゼーションストリームの中で、シングルトンのtransientでないフィールドをstealerのインスタンスで置き換える。
この時、シングルトンのインスタンスはstealerを含み、stealerはシングルトンの参照を持っている。

シングルトンはstealerを含んでいるので、シングルトンがデシリアライズされる時、最初にstealerのreadResolveメソッドが流れる。
結果として、stealerのreadResolveメソッドが流れるときには、そのインスタンスフィールドには一部デシリアライズされたシングルトンが参照されることとなる。

stealerのreadResolveメソッドは、その参照をインスタンスフィールドからstaticフィールドにコピーし、該当の参照はreadResolveメソッドが流れた後でもアクセス可能となる。
そのあと、readResolveメソッドは、隠したシングルトンのフィールドの正しい型を返す。このようにしないと、シリアライゼーションシステムがシングルトンのフィールドの中にstealerの参照を格納するときに、VMがCastExceptionをスローする。

具体例を示す。以下のような壊れたシングルトンクラスについて考える。

```java
package tryAny.effectiveJava;

import java.io.Serializable;
import java.util.Arrays;

//非 transient プロパティを含む不完全なシングルトン実装
public class Elvis implements Serializable {
    public static final Elvis INSTANCE = new Elvis();

    private Elvis() {
    }

    // 非 transient なプロパティ
    private String[] favoriteSongs = { "Hound Dog", "Heartbreak Hotel" };

    public void printFavorites() {
        System.out.println(Arrays.toString(favoriteSongs));
    }

    private Object readResolve() {
        return INSTANCE;
    }
}
```
stealerクラスは以下のよう。

```java
package tryAny.effectiveJava;

import java.io.Serializable;

//Elvis クラスを攻撃するクラス
public class ElvisStealer implements Serializable {
    // シングルトン以外のインスタンスを保持しておくための static フィールド
    static Elvis impersonator;

    // もう一つの Elvis インスタンス
    private Elvis payload;

    private Object readResolve() {
        // payload に保持されている Elvis インスタンスを impersonator に保持しておく
        impersonator = payload;

        // このプロパティを文字列配列として偽装するので文字列配列を返す
        return new String[] { "A Fool Such as I" };
    }

    private static final long serialVersionUID = 0;
}
```
欠陥シングルトンの2つのインスタンスを生成するお手製ストリームをデシリアライズするクラスが以下になる。（Java10だと動かない？）

```java
package tryAny.effectiveJava;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

public class ElvisImpersonator {
    // 改変した Elvis ストリーム
    private static final byte[] serializedForm = new byte[] { (byte) 0xac, (byte) 0xed, 0x00, 0x05, 0x73, 0x72, 0x00,
            0x05, 0x45, 0x6c, 0x76, 0x69, 0x73, (byte) 0x84, (byte) 0xe6, (byte) 0x93, 0x33, (byte) 0xc3, (byte) 0xf4,
            (byte) 0x8b, 0x32, 0x02, 0x00, 0x01, 0x4c, 0x00, 0x0d, 0x66, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x53,
            0x6f, 0x6e, 0x67, 0x73, 0x74, 0x00, 0x12, 0x4c, 0x6a, 0x61, 0x76, 0x61, 0x2f, 0x6c, 0x61, 0x6e, 0x67, 0x2f,
            0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x3b, 0x78, 0x70, 0x73, 0x72, 0x00, 0x0c, 0x45, 0x6c, 0x76, 0x69, 0x73,
            0x53, 0x74, 0x65, 0x61, 0x6c, 0x65, 0x72, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x01,
            0x4c, 0x00, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64, 0x74, 0x00, 0x07, 0x4c, 0x45, 0x6c, 0x76, 0x69,
            0x73, 0x3b, 0x78, 0x70, 0x71, 0x00, 0x7e, 0x00, 0x02 };

    public static void main(String[] args) {
        Elvis elvis = (Elvis) deserialize(serializedForm);
        Elvis impersonator = ElvisStealer.impersonator;
        elvis.printFavorites();
        impersonator.printFavorites();
    }

    static Object deserialize(byte[] sf) {
        try {
            return new ObjectInputStream(new ByteArrayInputStream(sf)).readObject();
        } catch (IOException | ClassNotFoundException e) {
            throw new IllegalArgumentException(e);
        }

    }
}
```

このプログラムを実行すると、
```
[Hound Dog,Heartbreak Hotel]
[A Fool Such as I]
```
のように表示されるらしい。（Java10で実行したところ動かず。以下の感じになる）

```
Exception in thread "main" java.lang.IllegalArgumentException: java.lang.ClassNotFoundException: Elvis
	at tryAny.effectiveJava.ElvisImpersonator.deserialize(ElvisImpersonator.java:29)
	at tryAny.effectiveJava.ElvisImpersonator.main(ElvisImpersonator.java:19)
Caused by: java.lang.ClassNotFoundException: Elvis
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:582)
	at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:190)
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:499)
	at java.base/java.lang.Class.forName0(Native Method)
	at java.base/java.lang.Class.forName(Class.java:374)
	at java.base/java.io.ObjectInputStream.resolveClass(ObjectInputStream.java:685)
	at java.base/java.io.ObjectInputStream.readNonProxyDesc(ObjectInputStream.java:1877)
	at java.base/java.io.ObjectInputStream.readClassDesc(ObjectInputStream.java:1763)
	at java.base/java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:2051)
	at java.base/java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1585)
	at java.base/java.io.ObjectInputStream.readObject(ObjectInputStream.java:422)
	at tryAny.effectiveJava.ElvisImpersonator.deserialize(ElvisImpersonator.java:27)
	... 1 more
```


想定通りの結果になったとすると、シングルトンであるにも関わらず、異なる2つのインスタンスが存在していることになるので問題である。

この問題はfavoriteSongsフィールドをtransientにすることで解消できる。

## single-element enum
しかし、Elvisクラスを1つの要素をもつenumとして作るほうが筋が良い（Item3）。

もし、シリアライザブルでインスタンスコントロールが必要なクラスをenumで書いたとしたら、Javaによって、宣言されたもの以外のインスタンスはあり得ないということが保証される。
Elvisの例では以下のようになる。

```java
public enum Elvis {
    INSTANCE;
    private String[] favoriteSongs =
            {"Hound Dog", "Heartbreak Hotel"};

    public void printFavorites() {
        System.out.println(Arrays.toString(favoriteSongs));
    }
}
```

enumによって、readResolveによるインスタンスコントロールが時代遅れになったわけではない。
コンパイル時には確定していない、シリアライザブルでインスタンスコントロールが必要なクラスに関しては、enumでは対処することができない。

## readResolveのアクセシビリティ
readResolveをfinalクラスに置くのであれば、privateにすべき。

finalではないクラスに置くのであれば、考慮が必要となる。
privateであれば、サブクラスからはアクセスできない。
package-privateであれば、同じパッケージのサブクラスしかアクセスできない。
protected または publicであれば、全てのサブクラスで使える。

protected または publicの場合で、サブクラスがreadResolveをオーバーライドしない場合、サブクラスをデシリアライズするときにスーパークラスのインスタンスを返すことになるので、ClassCastExceptionを発生させる可能性が高い。

# 90.シリアライズされたインスタンスの代わりに、シリアライズ・プロキシを検討する
本章で述べられてきたリスクを大きく低減させる技法として、シリアライゼーションプロキシパターンがある。

## シリアライゼーションプロキシパターン
シリアライゼーションプロキシパターンでは、まず、private static なインナークラスを作る。
このインナークラス（シリアライゼーションプロキシと呼ばれる）はエンクロージングクラスのインスタンスの論理状態を簡潔に表すようにする。

シリアライゼーションプロキシは1つのコンストラクタをもち、その引数はエンクロージングクラスである。
このコンストラクタでは、単に引数からデータをコピーしてくるのみであり、バリデーションチェックや防御的コピーを取る必要はない。

意図的に、シリアライゼーションプロキシのデフォルトserialized formはエンクロージングクラスの完全なSerialized formとなるようにする。
エンクロージングクラスとシリアライゼーションプロキシの双方とも、Serializableを実装するようにする。

Item50とItem88でみたPeriodクラスのシリアライゼーションプロキシの例は以下である。

```java
// ネストしたクラス。シリアライズ用の専用。
private static class SerializationProxy implements Serializable {
    // フィールドは final にできる
    private final Date start;
    private final Date end;

    SerializationProxy(Period period) {
        // 防御的コピーは必要はない
        this.start = period.start;
        this.end = period.end;
    }

    // UID を設定（Item87）
    private static final long serialVersionUID = 234098243823485285L;
}
```

次に、エンクロージングクラスにwriteReplaceメソッドを加える。例は以下。

```java
private Object writeReplace() {
    return new SerializationProxy(this);
}
```

このメソッドによって、エンクロージングクラスは、シリアライゼーションシステムに対して、シリアライズ対象はシリアライゼーションプロキシであることを明示している。

上記のwriteReplaceがエンクロージングクラスに置かれることで、エンクロージングクラスのインスタンスがシリアライズされることはなくなるはずだが、攻撃者が不変条件を破って、エンクロージングクラスを読み込んでくる場合について防御する必要がある。

そのために、エンクロージングクラスに以下のreadObjectメソッドを置いておく。

```java
// シリアライズ対象クラスの readObject メソッド
private void readObject(ObjectInputStream stream) throw InvalidObjectException {
    throw new InvalidObjectException("Proxy required");
}
```
こうすることで、エンクロージングクラスのシリアライズされたものが読み込まれることはなくなる。

最後に、readResolveメソッドをシリアライゼーションプロキシに配置する。
このreadResolveメソッドでは、エンクロージングクラスと論理的に等しいインスタンスを返すようにする。
本メソッドの存在によって、シリアライズ時にシリアライゼーションプロキシに変換されていたものが、デシリアライズ時にエンクロージングクラスの形に戻されることになる。

readResolveメソッドではエンクロージングクラスのpublicAPIのみを使用して、エンクロージングクラスのインスタンスを生成するが、そこにこのパターンの良さが現れている。
これによって、シリアライゼーションの特徴の多くが消されることになる。なぜなら、デシリアライズされたインスタンスは、コンストラクタ、staticなファクトリ等と同じ方法で作成されることになるからだ。
コンストラクタ、staticファクトリ等が不変条件を守れていれば、デシリアライズされたインスタンスも不変条件を守れていることとなる。

PeriodのシリアライゼーションプロキシのreadResolveメソッドは以下のよう。

```java
private Object readResolve() {
    return new Period(start, end);
}
```

防御的コピーの手法と同様に、シリアライゼーションプロキシでも、偽のバイトストリームによる攻撃、フィールドを盗む攻撃は防ぐことができる。
前述の方法とは違い、シリアライゼーションプロキシでは、	フィールドをfinalにすることができ、クラスをimmutableなものにすることができる（Item17）。
また、シリアライゼーションプロキシを用いれば、どのフィールドが攻撃をうけることを許容してもよいかについて、また、デシリアライズ時の明示的なバリデーションチェックについて考えなくてもよくなる。


本パターンのもう一つの利点として、シリアライズされたときのインスタンスと、デシリアライズされたときのインスタンスで、持つクラスが別のものでよいという点がある。
EnumSet（Item36）について考えてみる。
このクラスでは、コンストラクタはなく、ファクトリメソッドのみがある。
クライアントの立場からみると、そのファクトリメソッドははEnumSetを返すものの、サブクラスであるRegularEnumSetかJumboEnumSetかのいずれかが返ってくることとなる（要素数で変わり、64以下ならRegular）。
ここで、60個の要素を持ったenum setをシリアライズし、そのenum型に5つの要素を追加し、そのenum setをデシリアライズすることを考える。
シリアライズしたときはRegularEnumSetインスタンスであったが、デシリアライズされる時にはJumboEnumSetのほうが適したサイズになっている。
この実装に関して、実際にEnumSetでシリアライゼーションプロキシの仕組みが使われている。具体的には以下のよう。

```java
    private static class SerializationProxy<E extends Enum<E>>
        implements java.io.Serializable
    {

        private static final Enum<?>[] ZERO_LENGTH_ENUM_ARRAY = new Enum<?>[0];

        /**
         * The element type of this enum set.
         *
         * @serial
         */
        private final Class<E> elementType;

        /**
         * The elements contained in this enum set.
         *
         * @serial
         */
        private final Enum<?>[] elements;

        SerializationProxy(EnumSet<E> set) {
            elementType = set.elementType;
            elements = set.toArray(ZERO_LENGTH_ENUM_ARRAY);
        }

        /**
         * Returns an {@code EnumSet} object with initial state
         * held by this proxy.
         *
         * @return a {@code EnumSet} object with initial state
         * held by this proxy
         */
        @SuppressWarnings("unchecked")
        private Object readResolve() {
            // instead of cast to E, we should perhaps use elementType.cast()
            // to avoid injection of forged stream, but it will slow the
            // implementation
            EnumSet<E> result = EnumSet.noneOf(elementType);
            for (Enum<?> e : elements)
                result.add((E)e);
            return result;
        }

        private static final long serialVersionUID = 362491234563181265L;
    }
```

シリアライゼーションプロキシパターンには2つの制限がある。
* ユーザによって拡張可能なクラス（Item19）とは互換性がない。
* オブジェクトグラフに循環を含むようなクラスとの互換性はない。シリアライゼーションプロキシのreadResolveから、そのようなオブジェクトにあるメソッドを呼び出そうとしても、まだオブジェクトがないのでClassCastExceptionが発生してしまう。

また、シリアライゼーションプロキシパターンを使うと、性能的には若干劣化する。
