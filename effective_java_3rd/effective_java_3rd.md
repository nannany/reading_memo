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



# 6章.ENUMとアノテーション
# 34.intの定数の代わりにenumを使うべし
* enumをいつ使えばよいか？→コンパイル時に明らかになっている定数のセットが必要な時はいつでも！
* constant-specific methodは馴染みがなくてしっくりこなかった。。以下の説明が分かりやすかった。
<http://d.hatena.ne.jp/hageyahhoo/20091115/1258258461>

# 35.ordinalよりもインスタンスフィールドの値を使うべし
* そもそもordinalメソッドはEnumSetやEnumMap用に使われるものであって、大半のプログラマは使わないものである。

# 36.bitフィールドの替わりにEnumSetを用いるべし
