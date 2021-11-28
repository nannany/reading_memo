# Part 1 Understanding the Domain

## Chapter 1 Introducing Domain-Driven Design

### The Importance of a Shared Model

ドメインエキスパート、開発チーム、その他のステークホルダーが共有できるメンタルモデルを作ることがDDDの目的。

ソフトウェアをビジネスドメインにそって作ることで得るうまみとは？

```
市場投入までの時間を短縮。開発者とコードベースが、問題を抱えている人と同じモデルを共有することで、チームは適切なソリューションを迅速に開発できる可能性が高くなります。

ビジネスの価値を高める。問題を正確に把握しているソリューションは、お客様を幸せにし、道を踏み外す可能性を減らします。

無駄の削減。要件が明確であれば、誤解や手戻りによる時間の無駄が減ります。さらに、要件が明確になることで、価値の高いコンポーネントが明らかになり、価値の低いコンポーネントを減らして、そのコンポーネントにより多くの開発労力を割くことができます。

メンテナンスと進化が容易になる。コードで表現されたモデルがドメインエキスパート自身のモデルと密接に一致している場合、コードへの変更が容易になり、エラーの発生も少なくなります。さらに、新しいチームメンバーは、より早くスピードアップすることができます。
```

ここから先で、どのようにして共有のメンタルモデルを作成するのかをみていく。

### Understanding the Domain Through Business Events

- まずはビジネスイベントに着目する
    - ビジネスとは、データを何かに変換することである
    - その変換を理解することが大事
    - *これは始めよう要件定義でもいってた気がする*
- ドメインイベント
    - 物事が変換されるトリガーのことを指している？
    - ドメインイベントは常に過去形。過去に起こった過去形の事象をさす

#### Using Event Storming to Discover the Domain

----

# Part 2 Modeling the Domain

ドメインの分解について、functionalなアプローチとオブジェクト指向なアプローチでの違いを見ていく。

## Chapter 4 Understanding Types

代数的データ型

### Understanding Functions

#### Type Signatures

F#では返却する型を明示しなくても良い。
関数の中にサブ関数を置くこともできる。

#### Functions with Generic Types
 
#### Types and Functions

`type`はオブジェクト指向言語で言うところの`class`とは別物。

関数のoutputがまた関数であることもアリエル。

##### コラム

valuesとobjectsの違いは？

- valueはtypeのうちの1メンバー
  - 関数がvalueでもあり得る
  - immutable
- objectはデータ構造をカプセル化したもの
  - 状態を持つことを期待されている

### Composition of Types

型のcompositionについて語っていく。

#### "AND" Types

#### "OR" Types

[discriminated union](https://docs.microsoft.com/en-us/dotnet/fsharp/language-reference/discriminated-unions)

直積が `product types` で、直和が `sum types` か？

### Simple Types 

### Algebraic Type Systems

代数データ型はドメインモデリングをするにおいて、素晴らしいツールであるらしい。

## Working With F# Types

## Building a Domain Model by Composing Types

実例いっぱい。
*ここをJavaで表現したらどうなるか興味深い*

## Modeling Optional Values, Errors, and Collections

### Modeling Optional Values

基本、F#は必須属性。
null許容するときはoptionをつける

### Modeling Errors

エラーをResult型の1つの列挙子として表現する。
*Flutterとかもこのパターンだった気がする。非同期系の処理はこのパターンかしら*

### Modeling No Value at All

基本的にはF#でvoidすることはできない。
が、unitと書くことで、何も返さないことはできる。

unitがあるということは、どこかで副作用が起きているということ

### Modeling Lists and Collections 

F#でのリストの持ち方。

### Organizing Types in Files and Projects

どうやって型をファイルごとに分割するか、依存順とかどうかくかについて述べている。

## Wrapping Up 

```
この章では、型の概念と関数型プログラミングとの関係を説明し、F#の代数的な型システムを使って、小さな型からより大きな型を作るために型の合成をどのように利用するかを説明しました。

データをANDで結合して作られるレコード型や、データをORで結合して作られる選択肢型（判別型ユニオンとも呼ばれる）、さらにこれらを基にしたOptionやResultなどの一般的な型について紹介しました。

型がどのように機能するかを理解したので、要件を再検討して要件を再検討し、学んだことを使って文書化してみましょう。
```



