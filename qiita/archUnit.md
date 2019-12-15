# 概要

**ArchUnit**なるライブラリを使用することで、Javaソースコードのアーキテクチャを自動テストすることが可能となります。

ArchUnitでできること、実際にどんなコードになるのか等紹介します。

# ArchUnitについて

ArchUnitはJavaアーキテクチャに関する自動テストを行う、オープンソースライブラリです。  

## ArchUnitでできること

ArchUnitを使うと、以下のようなことを自動テストで確認することができます。([※]( https://www.archunit.org/userguide/html/000_Index.html#_what_to_check ))

* パッケージ間の依存関係のチェック
* クラス間の依存関係のチェック
* パッケージ、クラス間の包含関係のチェック
* 実装(implements)、継承関係のチェック
* アノテーションのチェック
* レイヤーのチェック
  * ex）Controller層,Service層,Persistence層の3レイヤがあるときに、`Controller → Service → Persistence`以外の依存関係は許さない
* 循環参照のチェック

## ArchUnitを使うと何が嬉しいのか

CIでの自動テストでアーキテクチャがクリーンであることを担保できます。

従来、アーキテクチャを保つために、

* コーディングガイドを用意する
* 上位者がコードレビューを行う

のようなことを行ってきたと思います。    
ArchUnitを導入することで、自動テストでのアーキテクチャチェックが可能となり、CIでアーキテクチャがクリーンであることを担保できるようになります。


## ArchUnitを使ったテスト

導入方法は[ ここ ]( https://www.archunit.org/userguide/html/000_Index.html#_installation )に記述されています。  
以下で示したコードは[ こちら ]( https://github.com/nannany/archUnit )にあります。(JUnit5でテストしています)

まず、テストクラスに`@AnalyzeClasses`を付与します。
`packages`で指定したpackageに含まれるクラスがテスト対象となります。

```java
@AnalyzeClasses(packages = "nannany.arch.check.archunit")
public class ArchitectureTest {
```

以下は、package名に`service`が入っているpackageからは、package名に`controller`が入っているpackageに依存することはできないことをチェックしています。

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

# 参考

https://www.archunit.org/
https://www.thoughtworks.com/radar/tools/archunit