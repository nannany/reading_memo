# 1章
* * Spring Dev Tools を用いるとアプリを起動したまま、クラスの変更を動的に反映できる。ホットリローディングというらしい。

# 2章
* JavaConfigなるものがある。
* lombok
* @Configuration が付与されたクラス（JavaConfigというBean定義ファイル）の中にBEANが定義される。
@Autowiredを付与されたクラスは、Bean定義の中からオブジェクトが探され、インジェクトされる。
* @SpringBootApplicationは以下の3つの合成。
  * @EnableAutoConfiguration
  * @Configuration
  * @ComponentScan

* コンポーネントスキャンの対象になるのは、
  * @Component
  * @Controller
  * @Service
  * @Repository

* JPAはJava標準のO/Rマッパーの**仕様**
  * HibernateやEclipseLinkが実装ライブラリとしてある。

* Lombokの@NoArgsConstructorでデフォルトコンストラクタ作成できる。
* Lombokの@AllArgsConstructorで全引数をもつコンストラクタ作成できる。

