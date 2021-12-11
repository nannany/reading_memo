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

イベント、コマンド、ビジネスワークフローを正確に定義するとどうなる？

#### Using Event Storming to Discover the Domain

- イベントを見つけるなら、イベントストーミング
  - 開発者やドメインエキスパートとその他のステークホルダーを巻き込んだワークショップ 
  - イベントストーミング
    - https://www.eventstorming.com/

#### Discovering the Domain: An Order-Taking System

- イベントストーミングの利点
  - ビジネスの理解を共有できる
  - 知らない部分をしれたり、洞察を深められたりする

#### コラム

```
シナリオは、お客様（または他のユーザー）が達成したいゴール（例えば、注文など）を記述したものです。これは、アジャイル開発における「ストーリー」に似ています。ユースケースは、シナリオをより詳細にしたもので、ゴールを達成するために必要なユーザーとのやり取りやその他のステップを一般的な言葉で表現したものです。シナリオもユースケースもユーザー中心の概念であり、ユーザーの視点から見たインタラクションに焦点を当てています。
ビジネス・プロセスは、（個々のユーザーではなく）ビジネスが達成したいと思う目標を記述したものです。シナリオと似ていますが、ユーザー中心ではなく、ビジネス中心に考えられています。
ワークフローは、ビジネスプロセスの一部を詳細に記述したものです。つまり、ビジネスゴールやサブゴールを達成するために、従業員（またはソフトウェアコンポーネント）が行う必要のある正確なステップを記載したものです。ここでは、ワークフローを一人の人間やチームができることに限定することで、ビジネスプロセスが複数のチームにまたがっている場合（注文プロセスのように）、全体のビジネスプロセスを一連の小さなワークフローに分割し、それらを何らかの方法で調整することができます。
```

#### Expanding the Events to the Edges

#### Documenting Commands

コマンドがトリガーとなって、ドメインイベントが発生する。

```
これらのイベントをいくつか壁に貼ったら、"何がこれらのドメインイベントを起こしたのか？"と尋ねてみるかもしれません。誰かが、あるいは何かが、ある活動を起こそうとしたのです。例えば、お客様が注文書を受け取ってほしいと思っていたり、上司があなたに何かをしてほしいと頼んでいたりします。
これらの要求をDDDの用語ではコマンドと呼びます（OOプログラミングで使われるコマンドパターンと混同しないでください）。コマンドは常に命令形で書かれます："Do this for me."
```

### Partishoning the Doamin into SubDomain
 
ドメインをサブドメインに区切っていく。

### Creating s Solution Using Bounded Context

- 問題空間と解決空間
- 境界づけられたコンテキスト

#### Getting the Contexts Right

どうやったら境界をうまくひけるのか？

- ドメインエキスパートに耳を傾ける
- 現在の部署構造に着目する
- 境界を引くことを忘れない
- 疎結合な設計
- ビジネスワークフローを優先して考える

#### Creating Context Maps

- コンテクストマップ 
  - 境界づけられたコンテクスト間でのやりとりを表現するためのマップ

#### Focusing on the Most Important Bounded Contexts

- ドメインの中でも特に重要な役割を果たすものがコアドメイン
- そのほかにsupportive domain, generic domainという区分けをしている

何がコアドメインになるかは、その事業の内容による。
コアドメインに注力して取り組むべし。

### Creating a Ubiquitous Language

- Ubiquitous Language
  - プロジェクトの設計、ソースコードで共通して利用する言葉 
  - どの境界づけられたコンテキストで使われるかによって意味合いが変わってくるはず

### Summarizing the Concepts of Domain-Driven Design

```
ドメインとは、私たちが解決しようとしている問題に関連する知識の領域であり、簡単に言えば、「ドメイン・エキスパート」が精通している領域のことです。
ドメイン・モデルは、特定の問題に関連するドメインの側面を表現する単純化のセットです。ドメインモデルは解決空間の一部であり、ドメインモデルが表現するドメインは問題空間の一部です。ユビキタス言語 
ユビキタス言語とは，ドメインに関連する概念や語彙の集合であり，チームメンバーとソースコードの両方で共有される．
境界のあるコンテキストとは，他のサブシステムと区別できる明確な境界を持った解決空間内のサブシステムである．境界のあるコンテキストは，しばしば問題空間のサブドメインに対応します．また、境界のあるコンテキストは、独自の概念と語彙を持ち、ユビキタス言語の独自の方言を持っています。
コンテキスト・マップとは、バウンデッド・コンテキストの集合体とそれらの間の関係を示す高レベルの図である。
ドメインイベントとは、システム内で起こったことを記録したものです。イベントは常に過去形で記述される。イベントは多くの場合、追加のアクティビティを引き起こします。
コマンドとは、あるプロセスの実行を要求するもので、人や他のイベントによって起動されます。プロセスが成功すると、システムの状態が変化し、1つまたは複数のドメインイベントが記録されます。
```

### Wrapping Up

`Focus on events and processes rather than data.`
これよく分からない。データの中身はとりあえずまだいいよ、後で詳細詰めるからって話なのか？

#### Events and Processes
この本で出す具体例の話。

#### Subdomains and Bounded Contexts
この本で出す具体例の話。

#### The Ubiquitous Language
この本で出す具体例の話。

#### What's Next

## Chapter 2 Understanding the Domain

### Interview with a Domain Expert

ドメインエキスパートとの会話の中で気づきをえる。
会話の中で、自分の勘違いに気づけることがある。

#### Understanding the Non-functional Requirements

システムの可用性、デザインに関わる情報をえる。

#### Understanding the Rest of the Workflow

#### Thinking About Inputs and Outputs

インプットは注文フォーム、アウトプットは？

確認書送付は副作用。

OrderPlaced event をBillingコンテキストにnotifiy


### Fighting the Impulse to Do Database-Driven Design

バイアスを入れない

### Fighting the Impulse to Do Class-Driven Design

バイアスを入れない。  
技術的詳細はまだ入れない。ここではドメインエキスパートが理解できるようにする。

### Documenting the Domain

Workflow の書き方とか。

### Driven Deeper into the Order Taking Workflow

会話。ドメイン知識を貯める。

### Representing Complexity in Our Domain Model

#### Representing Constraints

#### Representing the Life Cycle of an Order

### Wrapping Up

```
後半のモデリングの段階に移るときに、必要なものがたくさんあるので、要求の収集は今はやめておきましょう。
その前に、この章で学んだことを振り返ってみましょう。

設計中に実装の詳細に入り込まないことが重要であることを学びました。
DDDはデータベースドリブンでもクラスドリブンでもありません。
DDDはデータベース駆動でもクラス駆動でもありません。

そして、ドメインエキスパートの話をよく聞くと、今回のような比較的シンプルなシステムであっても、多くの複雑さが見えてきました。
例えば、当初は単一の「オーダー」が存在すると考えていましたが、調査を進めていくうちに、オーダーのライフサイクルを通じて、それぞれがわずかに異なるデータや動作を持つ、多くのバリエーションがあることがわかりました。
```

#### What's Next

```
この注文受付のワークフローをF#の型システムを使ってどのようにモデル化するかをまもなく見ていきます。
しかし、その前に、一歩下がって全体像を見つめ直し、完全なシステムをソフトウェア・アーキテクチャに変換する方法について議論しましょう。
これが次の章のテーマになります。
```

## Chapter 3 A Functional Architecture

C4アプローチの用語を使う。

### Bounded Contexts as Autonomous Software Components

最初からマイクロサービス目指さなくても良い。

### Communicating Between Bounded Contexts

1つサービス。

### Wrapping Up

```
この章では、さらにいくつかのDDD関連の概念や用語を紹介してきましたので、それらを1つにまとめてみましょう。
- ドメインオブジェクト（Domain Object）は、データ転送オブジェクト（Data Transfer Object）とは対照的に、あるコンテキストの境界内でのみ使用するために設計されたオブジェクトです。
- Data Transfer Object（DTO）とは、コンテキスト間でシリアル化して共有するように設計されたオブジェクトのことです。
- Shared Kernel、Customer/Supplier、Conformist は、境界のあるコンテクスト間の異なる種類の関係です。
- ACL（Anti-Corruption Layer）とは、結合を減らしてドメインが独立して進化できるように、あるドメインから別のドメインに概念を変換するコンポーネントです。
- Persistence Ignorance（永続性無視）とは、ドメインモデルがドメイン自体の概念のみに基づいており、データベースやその他の永続性メカニズムを意識したものであってはならないということです。
```

### What's Next

```
これで、ドメインの理解と、そのソリューションを設計するための一般的なアプローチができたので、個々のワークフローのモデリングと実装という課題に移ることができます。
これからの数章では、F#の型システムを使って、ワークフローとそれが使用するデータを定義し、ドメインの専門家や開発者でない人でも理解できるコンパイル可能なコードを作成します。
まずは、関数型プログラマにとって型とは何か、オブジェクト指向設計におけるクラスとはどう違うのかを理解する必要があります。
それは次の章のテーマです。
```

---

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

### Working With F# Types

### Building a Domain Model by Composing Types

実例いっぱい。
*ここをJavaで表現したらどうなるか興味深い*

### Modeling Optional Values, Errors, and Collections

#### Modeling Optional Values

基本、F#は必須属性。
null許容するときはoptionをつける

#### Modeling Errors

エラーをResult型の1つの列挙子として表現する。
*Flutterとかもこのパターンだった気がする。非同期系の処理はこのパターンかしら*

#### Modeling No Value at All

基本的にはF#でvoidすることはできない。
が、unitと書くことで、何も返さないことはできる。

unitがあるということは、どこかで副作用が起きているということ

#### Modeling Lists and Collections 

F#でのリストの持ち方。

#### Organizing Types in Files and Projects

どうやって型をファイルごとに分割するか、依存順とかどうかくかについて述べている。

### Wrapping Up 

```
この章では、型の概念と関数型プログラミングとの関係を説明し、F#の代数的な型システムを使って、小さな型からより大きな型を作るために型の合成をどのように利用するかを説明しました。

データをANDで結合して作られるレコード型や、データをORで結合して作られる選択肢型（判別型ユニオンとも呼ばれる）、さらにこれらを基にしたOptionやResultなどの一般的な型について紹介しました。

型がどのように機能するかを理解したので、要件を再検討して要件を再検討し、学んだことを使って文書化してみましょう。
```

## Chapter 5 Domain Modeling with Types   

### Reviewing the Domain Model

2章で見たモデルを再掲している。

### Seeing Patterns in a Domain Model

- simple value
- combinations of values with and
- choices with or
- workflows

これらをF#の型を使ってどう表現していくかを見ていく。

### Modeling Simple Values

実態としてはintそのものであっても、ドメインエキスパート目線からみたら別々のものであるものを区別するように型をつける。

```
type CustomerId = CustomerId of int
```

こういうのを`simple types`という。

#### Working with Single Case Unions

#### Constrained Values

simple valuesの制限については次の章で扱う。

#### Avoiding Performance Issues with Simple Types

- 高いパフォーマンスが求められる領域で、シンプルな値をラッピングすることについて
  - F#の例で説明してるからそんな意味かも。。
  - structなるものを使う
  - 配列の話はそのままプリミティブバリューを持っていいよってこと？？

### Modeling Complex Data

代数的データ型を使ってどうなるか見ていく。

#### Modeling with Record Types

#### Modeling Unknown Types

- まだ型が決まっていないところのために、Undefinedエイリアスを用意する。
  - 設計過程で一旦こうしとくみたいな感じ
  
#### Modeling with Choice Types

- 決まった個数の中から選べる型
  - *Javaだとenumかsealedクラス使うところかな*

### Modeling Workflows with Functions

- 動詞系で表すところについて

#### Working with Complex Inputs and Outputs

- 複数のアウトプットがある部分はそれようにrecordつくってやる

*ここでいう変換をメソッドとして表現するか、関数変数として表現すべきか？*

複数のインプットがある時は `A -> B -> C`みたいな感じにできるし、`A`と`B`をひっくるめた型を作成することもできる。

```
どの方法が良いのでしょうか？上記のケースでは、ProductCatalogが「実際の」入力ではなく依存関係にある場合、セパレート・パラメータ・アプローチを使用したいと思います。これにより、機能的にはディペンデンシー・インジェクションに相当するものを使うことができます。これについては、注文処理のパイプラインを実装する際の「依存関係の注入」で詳しく説明します。
一方で、両方の入力が常に必要であり、互いに強く結びついている場合は、レコードタイプでそのことを明確にします。(状況によっては、単純なレコード型の代わりにタプルを使うこともできますが、一般的には名前付きの型を使った方が良いでしょう)。
```

DIの絡みは9章ぽい

#### Documenting Effects in the Function Signature

effects
https://levelup.gitconnected.com/what-is-effect-or-effectful-mean-in-functional-programming-7fc7323b52b4

monadを使って表現するものがeffects？
monadは下記参照。
https://qiita.com/koher/items/6f4a8d8b3ad3142bf645#%E3%83%A2%E3%83%8A%E3%83%89%E3%81%A8%E3%81%97%E3%81%A6%E3%81%AEoptional

### A Question of Identity: Value Objects

DDDの世界では、一意に特定できるものがEntityで、そうでないものがValue Object

#### Implementing Equality for Value Objects

### A Question of Identity: Entities

### Wrapping Up

```
この章では、F#の型システムを使って、単純な型、レコード型、選択肢型を使ってドメインをモデル化する方法を学びました。
この章では、stringやintなどの開発者向けの言葉ではなく、ProductCodeやOrderQuantityなどのドメインのユビキタス言語を使用しました。
マネージャー型やハンドラー型を定義したことは一度もありません。

また、さまざまな種類のアイデンティティーや、DDDのコンセプトであるValue ObjectやEntityを型を使ってモデル化する方法についても学びました。
また、一貫性を確保する方法として、「集約」という概念も紹介されました。

そして、この章の最初に出てきたテキストドキュメントとよく似た型のセットを作りました。
大きな違いは、これらの型定義はすべてコンパイル可能なコードであり、アプリケーションの他のコードに含めることができるということです。
これにより、アプリケーションのコードは常にドメイン定義と同期しており、ドメイン定義が変更されると、アプリケーションのコンパイルに失敗することになります。
デザインをコードと同期させようとする必要はありません-デザインこそがコードなのです

型をドキュメントとして使用するこのアプローチは非常に一般的であり、他のドメインにも適用できることは明らかでしょう。
現時点では実装がされていないので、ドメインエキスパートと共同作業をする際に、アイデアをすぐに試すのに最適な方法です。
もちろん、単なるテキストなので、ドメインエキスパートは特別なツールを必要とせずに簡単にレビューすることができますし、もしかしたら自分でいくつかのタイプを書くこともできるかもしれません。

しかし、デザインについてはまだいくつかの点で課題があります。
単純な型が常に正しく制約されるようにするにはどうすればよいか？
アグリゲートの整合性をどうやって確保するか？
秩序の異なる状態をどのようにモデル化するのか？これらのトピックは次の章で取り上げます。
```


