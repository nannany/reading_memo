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

# 23.

# 6章.ENUMとアノテーション

# 34.intの定数の代わりにenumを使うべし

* enumをいつ使えばよいか？→コンパイル時に明らかになっている定数のセットが必要な時はいつでも！
* constant-specific methodは馴染みがなくてしっくりこなかった。。以下の説明が分かりやすかった。

<http://d.hatena.ne.jp/hageyahhoo/20091115/1258258461>

# 35.ordinalよりもインスタンスフィールドの値を使うべし
* そもそもordinalメソッドはEnumSetやEnumMap用に使われるものであって、大半のプログラマは使わないものである。

# 36.bitフィールドの替わりにEnumSetを用いるべし

# 8章.メソッド

# 49.引数のバリデーションチェックをすべし
* 

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


