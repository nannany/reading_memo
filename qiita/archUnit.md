# 概要

**ArchUnit**なるライブラリを使用することで、Javaソースコードがアーキテクチャ違反を犯していないかを、ユニットテストで確認することが可能となります。

ArchUnitでできること、実際にどんなコードになるのか等紹介します。

# ArchUnitについて

ArchUnitは、Javaアーキテクチャに関するユニットテストの実行を支援する[ オープンソースライブラリ ](https://github.com/TNG/ArchUnit)です。  
[TECHNOLOGY RADAR](https://www.thoughtworks.com/radar/tools/archunit)にも掲載された注目ライブラリです。

## ArchUnitでできること

ArchUnitを使うと、以下のようなことをユニットテストで確認することができるようになります。([※]( https://www.archunit.org/userguide/html/000_Index.html#_what_to_check ))

* パッケージ間の依存関係のチェック
* クラス間の依存関係のチェック
* パッケージ、クラス間の包含関係のチェック
* 実装(implements)、継承関係のチェック
* アノテーションのチェック
  * ex)`EntityManager`を継承したクラスは、`@Transactional`が付与されたクラスからのみアクセスされる、みたいなことをチェックできます
* レイヤーのチェック
  * ex）Controller層,Service層,Persistence層の3レイヤがあるときに、`Controller → Service → Persistence`以外のアクセスは許さない、みたいなことをチェックできます
* 循環参照のチェック

## ArchUnitを使うと何が嬉しいのか

アーキテクチャ違反が起こりにくくなります。

従来、アーキテクチャをきれいな状態に保つために、

* コーディングガイドを用意する
* 上位者がコードレビューを行う

といったアナログな対策を行うことが多かったと思います。   
そのため、何らかのヒューマンエラーが発生すると、アーキテクチャ違反したコードがmasterブランチに入ってしまいます。

ArchUnitを使用した場合、ユニットテストでアーキテクチャ違反を検出できるので、CIにてアーキテクチャ違反が起きていないかチェックすることができます。  
よって、**正しくテストが書けているならば**、マージされるコードがアーキテクチャ違反を起こすことはありえません。

## ArchUnitを使ったテスト

導入方法は[ ここ ]( https://www.archunit.org/userguide/html/000_Index.html#_installation )に記述されています。  
以下で示したコードは[ こちら ]( https://github.com/nannany/archUnit )にあります。(JUnit5でテストしています)

ArchUnitを使ったテストを書くに当たって、まず、テストクラスに`@AnalyzeClasses`を付与します。
`packages`で指定したpackageに含まれるクラスがテスト対象となります。

```java
@AnalyzeClasses(packages = "nannany.arch.check.archunit")
public class ArchitectureTest {
```

---

以下は、package名に`service`が入っているpackageからは、package名に`controller`が入っているpackageに依存することはできない、というアーキテクチャをチェックしています。

```java
/**
 * serviceパッケージ配下はcontrollerに依存しない
 */
@ArchTest
public static final ArchRule servicesCantDependOnController = noClasses()
        .that().resideInAnyPackage("..service..")
        .should().dependOnClassesThat().resideInAPackage("..controller..");
```

記述方法は、`should()`の左側にテスト対象となるクラスを、`should()`の右側にルールを書いていくイメージです。  
上記の例だと、`noClasses().that().resideInAnyPackage("..service..")` については、`service`と名のつくpackageに含まれるクラスには`should()`右側のルールに適合するクラスは**ない**、ことを表します。  
`dependOnClassesThat().resideInAPackage("..controller..");` については、`controller`と名のつくpackageに依存する、というるルールを表現しています。

---

ArchUnitでは典型的なアーキテクチャに対するサポートを行っています。  
現状では、[ 多層アーキテクチャ ](https://ja.wikipedia.org/wiki/%E5%A4%9A%E5%B1%A4%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A3)と[ オニオンアーキテクチャ（ヘキサゴナルアーキテクチャ） ](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))に対するサポートがあるようです。  

以下では、多層アーキテクチャをサポートする用途のメソッドを使用して、各層間のアクセスについて、`Controller → Service → Persistence`以外のものがないかチェックしています。

```java
/**
 * layeredArchitectureを使用した
 */
@ArchTest
public static final ArchRule layeredArchitecture = layeredArchitecture()
        .layer("Controllers").definedBy("nannany.arch.check.archunit.controller")
        .layer("Services").definedBy("nannany.arch.check.archunit.service")
        .layer("Repositories").definedBy("nannany.arch.check.archunit.repository")

        .whereLayer("Controllers").mayNotBeAccessedByAnyLayer()
        .whereLayer("Services").mayOnlyBeAccessedByLayers("Controllers")
        .whereLayer("Repositories").mayOnlyBeAccessedByLayers("Services");
```

# 参考

https://www.archunit.org/
https://www.thoughtworks.com/radar/tools/archunit