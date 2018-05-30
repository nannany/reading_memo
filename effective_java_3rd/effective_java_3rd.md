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
* 

# 6章.ENUMとアノテーション

# 34.intの定数の代わりにenumを使うべし

* enumをいつ使えばよいか？→コンパイル時に明らかになっている定数のセットが必要な時はいつでも！

* constant-specific methodは馴染みがなくてしっくりこなかった。。以下の説明が分かりやすかった。

<http://d.hatena.ne.jp/hageyahhoo/20091115/1258258461>



# 35.ordinalよりもインスタンスフィールドの値を使うべし

* そもそもordinalメソッドはEnumSetやEnumMap用に使われるものであって、大半のプログラマは使わないものである。



# 36.bitフィールドの替わりにEnumSetを用いるべし

