# 12章
CDIとは何か？なぜ必要なのか？
* context and dependency injection
* クラス同士の関係を疎結合にするために使用
* CDIでインジェクトするクラスには、何らかのスコープアノテーションをつけなければならない。
* CDIとしてインジェクト可能なものを、CDIビーンといい、CDIビーンである条件としては、
  * 具象クラスであること
  * 引数なしのデフォルトコンストラクタを持つこと
  * static付のインナークラスでないこと
* CDIに組み込まれたスコープアノテーションは以下5種
 * RequestScoped
 * SessionScoped
 * ApplicationScoped
 * ConversationScoped
 * Dependent
* `isTransient()` で会話スコープが開始されているか調べられる。
* `@Produces` で、メソッドの戻り値をインジェクトできるようになる。
* `InjectPoint` を用いることで、インジェクト先の情報を得ることができる。(ロガーで使用)
* インターフェースに限定子(Qualifier)なるものをつけてインジェクトすることもできる
* @Alternative と beans.xml の組み合わせの利点
 * 限定子を書く必要がなくなり、実装クラスの選択をプログラムから切り離せる

<font color="red">Alternativeとbeansの組み合わせが複数ある時の書き方は？</font>