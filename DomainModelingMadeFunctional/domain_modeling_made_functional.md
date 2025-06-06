https://github.com/swlaschin/DomainModelingMadeFunctional

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

### Partitioning the Domain into SubDomain

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

何がコアドメインになるかは、その事業の内容による。 コアドメインに注力して取り組むべし。

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

ドメインエキスパートとの会話の中で気づきをえる。 会話の中で、自分の勘違いに気づけることがある。

#### Understanding the Non-functional Requirements

システムの可用性、デザインに関わる情報をえる。

#### Understanding the Rest of the Workflow

#### Thinking About Inputs and Outputs

インプットは注文フォーム、アウトプットは？

確認書送付は副作用。

OrderPlaced event をBillingコンテキストにnotify

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

#### Transferring Data Between Bounded Context

- Domain ObjectとDTOについて

#### Trust Boundaries and Validation

- workflowの最初と最後にゲートを用意
    - 入力ゲートでやることはいわゆるバリデーション
        - not nullとか何文字以下だとか
    - 出力ゲートでやることは他のコンテキストに出していいか否かのチェック
        - PANを削除するとか

### Contracts Between Bounded Contexts

```
Shared Kernel関係とは、2つのコンテキストが何らかの共通のドメインデザインを共有しており、関係するチームが協力する必要がある場合です。
たとえば、私たちのドメインでは、受注コンテキストと出荷コンテキストは、配送先住所について同じ設計を使用しなければならないと言うかもしれません。
受注コンテキストは住所を受け入れ、それを検証し、出荷コンテキストは同じ住所を使用してパッケージを出荷します。
この関係では、イベントまたはDTOの定義の変更は、影響を受ける他のコンテキストの所有者との協議によってのみ行われる必要があります。

顧客/サプライヤーまたは消費者主導型契約[17]の関係は、下流のコンテキストが、上流のコンテキストに提供させたい契約を定義するものである。
2つのドメインは、上流のコンテキストが契約の義務を果たす限り、独立して進化することができます。
このドメインでは、課金コンテキストが契約を定義し（「これは顧客に請求するために必要なものです」）、次に受注コンテキストがその情報のみを提供し、それ以上は提供しないかもしれません。

適合的な関係は、消費者主導型とは正反対である。
下流のコンテキストは、上流のコンテキストから提供された契約を受け入れ、それに合わせて自身のドメインモデルを適応させる。
私たちのドメインでは、受注コンテキストは、製品カタログによって定義された契約を受け入れ、それをそのまま使用するようにコードを適応させるだけかもしれない。
```

#### Anti-Corruption Layers

- 腐敗防止層の主な役目は2つのコンテキスト間の翻訳
    - バリデーションなどは主な役目ではない(が、やるのは事実てことだよね？)

#### A Context Map with Relationship

```
受注(order-taking)と出荷(shipping)のコンテクスト間の関係は、「Shared Kernel」、つまり通信契約を共同で所有することになります。

受注(order-taking)と請求(billing)の関係は "消費者主導の契約 "であり、請求コンテキストが契約を決定し、受注システムが請求コンテキストに必要なデータを正確に供給することを意味する。

受注(order-taking)と商品カタログ(product-catalog)の関係は、"Conformist "であり、受注コンテキストは商品カタログと同じモデルを使用するようにサブミットすることを意味する。

最後に、外部のアドレスチェックサービスは我々のドメインと全く似ていないモデルを持っているので、それとのインタラクションに明示的なアンチコラプションレイヤーを挿入することにします。
これはサードパーティーコンポーネントを使用する際によくあるパターンです。
ベンダーロックインを回避し、後で別のサービスに乗り換えることができるようになる。
```

逆コンウェイの法則
https://www.thoughtworks.com/radar/techniques/inverse-conway-maneuver

### Workflows Within a Bounded Context

- 7章と関連

#### Workflow Inputs and Outputs

- PlaceOrder が入力
- OrderPlaced イベントが出力
- order-takingとbillingには`customer/supplier`関係があるので、Billingが必要とする情報をworkflowで生み出す
- Workflow は戻り値としてイベントを戻す
- `OrderAcknowledgementSent`これは何者だ？
    - メールを送ったことを認知するためのイベントかな

#### Avoid Domain Events Within a Bounded Context

- 隠れた依存関係
    - 内部限定のイベントを持つのではなくて、外部に出してしまう
    - globalでmutableな状態を持たない
        - この辺りは2章3章でも扱う

### Code Structure Within a Bounded Context

- layered architectureの問題
    - transaction script

#### The Onion Architecture

- 9章

#### Keep I/O at the Edges

- 副作用を避けたい
- database or file system に対する処理が副作用
- I/Oをオニオンの外側に追い込む
- 12章

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

F#では返却する型を明示しなくても良い。 関数の中にサブ関数を置くこともできる。

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

基本、F#は必須属性。 null許容するときはoptionをつける

#### Modeling Errors

エラーをResult型の1つの列挙子として表現する。
*Flutterとかもこのパターンだった気がする。非同期系の処理はこのパターンかしら*

#### Modeling No Value at All

基本的にはF#でvoidすることはできない。 が、unitと書くことで、何も返さないことはできる。

unitがあるということは、どこかで副作用が起きているということ

#### Modeling Lists and Collections

F#でのリストの持ち方。

Mapはあまり使わないらしい。なぜだ？

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
    - Javaだとからのクラスにする？->それだと設計途中であることはわからない。

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

monadを使って表現するものがeffects？ monadは下記参照。
https://qiita.com/koher/items/6f4a8d8b3ad3142bf645#%E3%83%A2%E3%83%8A%E3%83%89%E3%81%A8%E3%81%97%E3%81%A6%E3%81%AEoptional

### A Question of Identity: Value Objects

DDDの世界では、一意に特定できるものがEntityで、そうでないものがValue Object

#### Implementing Equality for Value Objects

structural equality
https://kotlinlang.org/docs/equality.html

### A Question of Identity: Entities

自分が名前を変えたとしても同じ自分であるように、ある種識別子を持つようなオブジェクトをEntityという。

置かれるコンテキストによって、その物体がEntityにもValue Objectにもなり得る。

#### Identifiers for Entities

Entityを識別する値を割り振る必要がある。

#### Adding Identifiers to Data Definitions

識別子を型の外側におくか、内側におくか？ パターンマッチングの時に、IDも含めて取れるので、内側に置くことが多い。

#### Implementing Equality for Entities

識別子の比較のみでequalかどうかみれるようにしておく必要がある。

そのためにequalsとhashCodeをオーバーライドしている

オブジェクト同士の比較を禁じることもできるっぽい。
(コンパイルで弾ける)
これは多分Javaだと無理。

#### Immutability and Identity

イミュータブルにどうEntityを扱う？

### Aggregates

Orderlineってなんだっけ？

Orderの中にOrderLineがあるような構造であるとき、つまり、Orderの中にOrderlineフィールドがあるような状況の時に、
Order,OrderLineともにimmutableならば、OrderLineを変更した時にOrderも変更しないといけない。

トップレベルのEntity、上記でいうOrderみたいなものを aggregate とよぶ。

#### Aggregates Enforce Consistency and Invariants

詳細は６章で

#### Aggregates References

OrderにCustomerを関連づけたい場合は、Customerをフィールドに持たせるのではなく、CustomerIdを持たせるのがよかろう。
(第三正規化みたいな考え方と思った)

aggregateがテーブルやserializeの単位になるだろう。

`consistency boundary`?

domain modelにおけるaggregatesが持つ重要な役割は以下。

- アグリゲートは、トップレベルのエンティティが "ルート" として機能し、単一のユニットとして扱うことができるドメインオブジェクトのコレクションです。
- アグリゲート内部のオブジェクトに対するすべての変更は、トップレベルを経由してルートに適用されなければならず、アグリゲート内部のすべてのデータが同時に正しく更新されることを保証する一貫性の境界として機能する。
- アグリゲートは、永続性、データベーストランザクション、およびデータ転送の原子単位である。

#### Column

DDDの用語について

- Value ObjectはIDを持たないドメインオブジェクトである。同じデータを含む2つのValue Objectは同一とみなされます。Value Object は不変でなければならず、一部でも変更されると別の Value Object になる。バリューオブジェクトの例としては、名前、住所、場所、お金、日付などがあります。
- エンティティは、ドメインオブジェクトであり、プロパティが変更されても持続する本質的な同一性を持っています。エンティティオブジェクトは一般的にIDまたはキーフィールドを持ち、同じID/キーを持つ2つのエンティティは同じオブジェクトとみなされます。エンティティは通常、寿命があり、変更の履歴があるドメインオブジェクトを表します（ドキュメントなど）。エンティティーの例としては、顧客、注文、製品、請求書などがある。
- 集約は、関連するオブジェクトの集まりで、ドメイン内の一貫性を確保し、データトランザクションで原子単位として使用するために、単一のコンポーネントとして扱われるものである。他のエンティティは、集約をその識別子によってのみ参照すべきである。これは、"ルート "として知られる集約の "トップレベル "メンバのIDである。

### Putting It All Together

`and`はなんだ？

#### The Challenge Revisited: Can Types Replace Documentation?

F#はC#やJavaより読みやすかろうと述べておる。

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

## Chapter 6 Integrity and Consistency in the Domain

境界づけられたコンテキスト内の、信頼できるドメインについて、`integrity`と`consistency`という側面から見ていく章。
`integrity`は完全性と訳されるらしい。

```
ここでいう「完全性（または妥当性）」とは、データの一部が正しいビジネスルールに従っていることを意味する。例えば 
- 例えば、UnitQuantityは1〜1000の間であると言いました。
- コード内でこれを何度も確認する必要があるでしょうか。注文は、常に少なくとも1つの注文行を持つ必要があります。
- 注文は、出荷部門に送信される前に、有効な配送先住所を持つ必要があります。
```

`consistency`は一貫性。

```
ここでいう一貫性とは、ドメインモデルの異なる部分が事実について同意していることを意味する。以下はその例である．
- ある注文の請求金額の合計は、個々の行の合計であるべきです。もし合計が異なれば、データに矛盾がある。
- 注文が行われると、それに対応する請求書が作成されなければならない。注文書は存在するが、請求書が存在しない場合、データの整合性がとれなくなる。
- 注文時に割引クーポンコードを使用する場合、そのクーポンコードを使用済みとマークし、再度使用できないようにしなければならない。注文書がそのバウチャーを参照しているにもかかわらず、バウチャーが使用済みとマークされていない場合、データの整合性がとれない。
```

上記のようなことを、どのように型を使って表現していくか？

### The Integrity of Simple Values

前の章で、Stringやintで表現できる値でも型を与えるようにしていた。

現実世界のドメインでは、何らかの制限があることがほとんど。`CustomerName`にはtabを含まないとか。

immutableな値であることが保証されているならば、生成時のチェックだけで、他の使用箇所においては防御的なコーディングをする必要がない。
これは結構immutableを推す上で大事なことかもしれない。mutableなものだと、途中で変えられることがあるし。(my opinion)

constructorをprivateにしちゃう。 これ、インスタンス生成の中で値のチェックを必ずさせることが目的としてあるはずだが、それのみならコンストラクタでもできるくない？

- コンストラクタは受け取った値をはめ込むだけ、という暗黙の了解がある？
- F#だとロジックを書けない？

なんか後者な気がする。

署名ファイル？
-> Rustの所有権みたいな話につながったりするのかしら？

### Units of Measure

[測定単位](https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/units-of-measure)

[国際単位系](https://ja.wikipedia.org/wiki/%E5%9B%BD%E9%9A%9B%E5%8D%98%E4%BD%8D%E7%B3%BB) はF#にはデフォで入ってるようだ。

Javaにもあるっぽい。  
https://www.baeldung.com/javax-measure

### Enforcing Invariants with the Type System

型によってデータの完全性を担保する。

リストが空でないということも、`NonEmptyList`なる型を使える。(F#の言語そのものにはないが、3rdパーティライブラリとして提供されてるっぽい)
Javaだと良さげなライブラリはなさそう。

### Capturing Business Rules in the Type System

お客さんのメールアドレスに対して、認証済みのものであるか、未認証のものであるかを見分けるにあたっても、

- 認証済みのメールアドレス
- 未認証のメールアドレス

で型を作成するべき。

また、認証済みのメールアドレスを作成できるものは限定しておくべき。

---
email, 郵便番号のいずれかは必要となる、というような場合においては、

```f#
type Contact = {
   Name: Name
   Email: EmailContactInfo option
   Address: PostalContactInfo option
}
```

とすると、両方がない場合を型以外の部分で制御しないといけないので、

```f#
type ContactInfo = 
    | EmailOnly of EmailContactInfo
    | AddrOnly of PostalContactInfo 
    | EmailAndAddr of BothContactMethods
```

みたいに型で分ける。

これ、類似のもので数が増えた場合結構大変そう。。
とはいえ、上記のようにすると、ContactInfoが3つ以外の状態ではありえないことはすぐにわかる。

-> 増えた場合は別の構造を考えるのがよかろう。

#### Making Illegal States Unrepresentable in Our Domain

今回この本で考えているケースだと、validate済みのorderと未validateのorderで型を分けられる。

### Consistency

```
この章ではこれまで、ドメイン内のデータの完全性を強制する方法について見てきました。

では最後に、関連する概念である「一貫性」について見ていきましょう。本章の冒頭で、一貫性の要件の例をいくつか見てきました。
注文の合計金額は、個々の行の合計金額でなければなりません。もし合計が異なれば、データに一貫性がありません。
注文が行われると、それに対応する請求書が作成されなければならない。注文書が存在し、請求書が存在しない場合、データの整合性がとれなくなる。
注文時に割引クーポンコードを使用する場合、そのクーポンコードを使用済みとマークし、再度使用できないようにしなければならない。
注文書がそのバウチャーを参照しているにもかかわらず、バウチャーが使用済みとマークされていない場合、データに一貫性がない。

ここで説明するように、一貫性は技術用語ではなくビジネス用語であり、一貫性が意味するものは常に文脈に依存する。
例えば、商品の価格が変更された場合、未出荷の注文は直ちに新しい価格に更新されるべきでしょうか。
顧客のデフォルトの住所が変更された場合はどうでしょうか？未出荷の注文は直ちに新しい住所に更新すべきでしょうか？これらの質問に対する正しい答えはありません。

しかし、一貫性を保つことは設計に大きな負担をかけることになり、コストもかかるので、できることならその必要性を回避したいものです。
要件収集の際、プロダクトオーナーはしばしば、望ましくない、現実的でないレベルの一貫性を求めることがあります。
しかし、多くの場合、一貫性の必要性を回避したり、遅らせたりすることができる。

最後に、一貫性と永続性の原子性は関連していることを認識することが重要である。
例えば、注文がアトミックに永続化されない場合、注文が内部的に一貫していることを保証する意味はありません。
注文のさまざまな部分が別々に永続化され、ある部分が保存されなかった場合、後でその注文を読み込む人は、内部的に一貫性のない注文を読み込むことになります。
```

#### Consistency Within a Single Aggregate

aggregateが一貫性を保つ単位。

aggregateを永続化する場合には、1つのトランザクションで行うべき。

#### Consistency Between Different Contexts 

別のコンテキストと関わる一貫性を維持するためにどうするか？

[スターバックスの話](https://code.google.com/archive/p/gregors-ramblings-ja/wikis/18_starbucks.wiki) を引き合いに出していた。

結果整合性
即時に一貫した状態になる必要がないのであれば、イベントを発行して、リスナーがそれを処理する形に持っていけば良い。

補正トランザクションパターン
https://docs.microsoft.com/ja-jp/azure/architecture/patterns/compensating-transaction

#### Consistency Between Aggregates in the Same Context

同じ境界づけられたコンテキスト内で上記と同様の状況が起きたらどうするか？
-> 場合によるが、原則1つのアグリゲートを1つのトランザクションで行うべき。
集約をどうにか使い回すよりは、新しい集約の単位を作るべき。

#### Multiple Aggregates Acting on the Same Data

```
先ほど、アグリゲートは整合性制約を適用するために機能すると強調しましたが、同じデータに対して機能する複数のアグリゲートがある場合、どのようにして制約が一貫して適用されることを確認できるでしょうか。
例えば、口座の残高に作用し、残高がマイナスにならないことを保証する必要がある、口座アグリゲートと送金アグリゲートがあるとします。

多くの場合、制約が型を使用してモデル化されている場合、複数の集約間で共有することができます。
例えば、口座残高が決してゼロ以下にならないという要件は、NonNegativeMoney型を使用してモデル化することができます。
これが適用できない場合は、共有の検証関数を使用することができます。
これは、オブジェクト指向モデルに対する関数型モデルの利点のひとつです。
検証関数は特定のオブジェクトに添付されず、グローバルな状態に依存しないので、異なるワークフローで容易に再利用できます。
```

ここのオブジェクト指向モデルとの比較はよくわからないなぁ。


### Wrapping Up

```
この章では、ドメイン内のデータが信頼できることを保証する方法を学びました。

単純な型には「スマートなコンストラクタ」を、より複雑な型には「不正な状態を表現できないようにする」ことを組み合わせることで、型システムそのものを使って多くの種類の整合性ルールを強制できることを確認しました。
これにより、コードの自己文書化が進み、ユニットテストの必要性も少なくなります。

また、1つの境界コンテキスト内と境界コンテキスト間で一貫したデータを維持することについて調べ、1つの集合体内で作業するのでなければ、即時の一貫性よりも最終的な一貫性のために設計すべきだと結論付けました。

次の章では、注文を出すワークフローをモデル化しながら、これらすべてを実践していきます。
```

## Chapter 7 Modeling Workflows as Pipelines

### The Workflow Input

#### Commands as Input

#### Sharing Common Structures Using Generics

同様の構造を共有したい場合、ooでは基底クラスを作ったりする。
functionalの世界では、それをgenericsで実行する。

#### Combining Multiple Commands in One Type

受け取るコマンドが複数ある場合の話？ -> 選択型を使って云々やっている。
あんまり腹落ちはしていない

### Modeling an Order as a Set of States

orderは静的なドキュメントではなくて、さまざまな状態を変遷していくものである。
馬鹿正直にやると、各状態のフラグをもたせることになる。
このアプローチは色々な問題を抱えている。

- このシステムは、さまざまなフラグによって示されるように、明らかに状態を持っています。しかし、状態は暗黙的なもので、これを処理するためには多くの条件コードが必要になります。
- また、状態によっては他の状態では不要なデータもあり、それらをすべて1つのレコードに入れると設計が複雑になる。例えば、AmountToBillは "priced "ステートでのみ必要ですが、他のステートには存在しないため、フィールドをオプションにする必要があります。
- どのフィールドがどのフラグに対応するのかが明確ではありません。AmountToBillはIsPricedが設定されているときに設定される必要がありますが、設計上それが強制されないため、データの一貫性を保つためにコメントに頼らざるを得ません。

これよりは、各状態で別の型を作ってあげたほうが良い。


`Quote`ってなんだっけ？ -> 見積もりか

#### Adding New State Types as Requirements Change

型で状態を分けるメリットとしては、既存のコードに変更を加えなくても拡張できることにある

### State Machines

stateの遷移を表す図のことをstate machineと呼んでいる。

stateの遷移の例としては、
- emailの検証済み、未検証、
- カートのempty, active, 支払い済み
- 配送において、荷物の、配送中、配送済み、配達されていない
みたいな感じ
  
- [StatePattern](https://ja.wikipedia.org/wiki/State_%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3)との絡みとかある？
  
#### Why Use State Machines?

state machineを利用することによって得られる利点。

- それぞれの状態は、許容される動作が異なる場合があります。
  - たとえば、ショッピングカートの例では、アクティブなカートだけが支払いを行うことができ、支払われたカートは追加することができません。前の章で、未確認/確認済みメールの設計について説明したとき、確認済みメールアドレスにのみパスワードリセットを送信できるというビジネスルールを見ました。各状態に個別の型を使用することで、その要件を関数の署名に直接エンコードし、コンパイラーを使用してそのビジネスルールが遵守されていることを確認することができました。
- すべての状態が明示的に文書化されている。
  - 暗黙の了解で文書化されていない重要な状態を持つことは容易である。ショッピングカートの例では、「空のカート」は「アクティブなカート」と異なる動作をするが、これがコードで明示的に文書化されることは稀だろう。
- このように、起こりうるすべての可能性を考えさせるのが、設計ツールなのです。
  - 設計でよくあるエラーの原因は、特定のエッジケースが処理されていないことです。ステートマシンは、すべてのケースを強制的に考えさせます。例えば
    - すでに認証されているメールアドレスを認証しようとするとどうなりますか？
    - 空のショッピングカートから商品を削除しようとするとどうなりますか？
    - すでに「配達済み」になっている荷物を配達しようとするとどうなるのでしょうか？

オートマトンとかとの絡み。
どういう関係なんだろう。
-> 
有限オートマトンという概念が、有限個の状態と遷移と動作の組み合わせからなる振る舞いのモデルをさす。
それを具体的に表現する手段の1つがステートマシン。
https://ja.wikipedia.org/wiki/%E6%9C%89%E9%99%90%E3%82%AA%E3%83%BC%E3%83%88%E3%83%9E%E3%83%88%E3%83%B3

#### How to Implement Simple State Machines in F#

### Modeling Each Step in the Workflow with Types

state machineの各ステップをみていく

各ステップとは,validate, pricing, acknowledgement

#### The Validation Step

validateOrderというステップにおいては、ProductCode、住所のチェックに依存している。
これをどう表現するか？

ここでいう依存とはなんだろう?

dependencyとなる引数を先に持ってきているが、これはアプリケーションの分割？を容易にすることにつながるらしい。
-> partial application

#### The Pricing Step

#### The Acknowledge Order Step

受注確認の文言を作って、メールをお客さんに送る。

PricedOrderを受け取って、メールを送信する感じ

#### Creating the Events to Return

配送のために`OrderPlaced`,課金のために`BillableOrderPlaced`も`OrderAckowledgementSent`に加えてアウトプットとして必要。

これら3つを内包した型を定義するよりは、これら3つの選択型である`PlaceOrderEvent`のリストを返却するのが良い。

### Documenting Effects

#### Effects in the Validation Step

effectsは言葉通り、物理世界に影響を与えるものと捉えるのが良かろう。
http://like-a-boss.net/2014/12/31/effects-versus-side-effects.html

ここだと、バリデーションで外部に問い合わせる必要があって、それをAsync,Resultで囲んでいる。

#### Effects in the Pricing Step

金額がマイナスだったり、めちゃデカかったりする時はエラーになるので、それを考慮してResultにした感じ。

#### Effects in the Acknowledge Step

### Composing the Workflow from the Steps 

AsyncResultとかにくるまっているから、functionをそのまま繋げるといったsimpleなことはできない。
ここの解決は実装の章で見ていく

### Are Dependencies Part of the Design?

workflowの依存関係を引数に入れるべきかはガイドラインがある。

- publicなAPIの場合は隠す。
  - 呼ぶ人はそんなもの知ったこっちゃないので
- 内部で使われるものに関しては引数でとる。
  - 何に依存しているか明らかになるので良い。

モノリスなアプリにおけるドメインわけの話に見える。普通ならドメインごとにapiで連携するはずなので。

### The Complete Pipeline

ここまでのおさらい。

`DomainApi.fs`に外部公開する、つまり、入出力の型の定義をかく。

#### The Internal Steps

`PlaceOrderWorkflow.fs`に内部で使う型の定義を書く。

### Long-Running Workflows

他のステップから値が返ってくるスピードが遅い場合、storageに情報を保存してやり取りするのもあり。

long-running workflowをSagasと呼ぶらしい。
http://vasters.com/archive/Sagas.html

### Wrapping Up

```
この章では、型のみを使用してワークフローをモデル化する方法について学びました。

私たちは、ワークフローへの入力を文書化することから始め、特にコマンドをどのようにモデル化するかについて学びました。
次に、ステートマシンを使って、ドキュメントやライフサイクルを持つ他のエンティティをどのようにモデル化するかを検討しました。
また、各ステップの依存関係や効果を文書化することにも力を入れました。

その過程で、何百もの型を作成したように思います（実際には約30の型しかありませんでした）。
これは本当に必要だったのでしょうか？多すぎるのでしょうか？
多いように見えるかもしれませんが、私たちは実行可能なドキュメント、つまりドメインを伝えるコードを作成しようとしていることを思い出してください。
もしこれらの型を作らなかったとしても、検証済み注文と価格決定済み注文の違いや、ウィジェットコードと通常の文字列の違いを文書化しなければならないでしょう。

なぜ、ドキュメントをコードそのものにしないのでしょうか？もちろん、常にバランスは必要です。
ここでは、すべてをこの方法で文書化した場合にどのように見えるかを示すために、意図的に極端な方法をとっています。
もし、この方法があなたの状況にとって行き過ぎだと思われるなら、あなたのニーズに合わせて自由に縮小してください。
いつものように、あなたは、ドメインに貢献し、目の前のタスクに最も役立つことを行う必要があります。
```

### What's Next

```
この4章はモデリングに終始してきましたが、ついに最終章に到達し、実際の実装に手を染めることができるようになりました!

この章では、先に進む前に明らかにしておきたいことがあります。
この本では、要求の収集、モデリング、コーディングをそれぞれ別のセクションに分けました。
これは、直線的な「ウォーターフォール」型の開発を推奨しているように見えるかもしれませんが、全くそのような意図はありません。
実際のプロジェクトでは、要件収集とモデリング、モデリングとプロトタイピングを継続的に組み合わせ、顧客や専門家にできるだけ早くフィードバックできるようにする必要があります。
実際、型を使ったモデリングの要点は、ドメインエキスパートが直接モデルを読むことができるため、要件からモデリングへ、そしてまたモデリングへ、数日ではなく数分で戻ることができるようにすることなのです。

これで、実装の章を始める準備ができました。
最初のステップとして、関数がどのように機能するのか、そして関数からどのようにアプリケーションを構築するのかを理解することを確認しましょう。
次の章でそれを行います。
```

# Part 3 Implementing the Model

関数型のテクニックを使って実装していく。
コンポジション、部分アプリケーション？、モナド

## Chapter 8 Understanding Functions

関数型言語のいいところをみていく

### Functions, Functions, Everywhere

オブジェクト指向言語と関数型言語は色々な面で考え方が違う。

### Functions Are Things 

Inputとparameterの違いって何だっけ？

#### Treating Functions as Things in F#

#### Functions as Input

関数をInputととしてとる例をみていく

#### Functions as Output

関数をOutputとしている例を見ていく

#### Currying

複数のパラメータをもつ関数を、1つのパラメータを持つ関数に変換することをカリー化という。

F#では明示的にカリー化をせずとも、すでにカリー化された関数になっている？

#### Partial Application

パラメータを織り込んでしまう技法をpartial applicationと呼ぶらしい。日本語訳は？

### Total Functions

全域関数。

値の閾値が一部外れるような関数のことを[ 部分関数 ](https://scrapbox.io/mrsekut-p/%E9%83%A8%E5%88%86%E9%96%A2%E6%95%B0)というらしい。

全てのインプットには紐づくアウトプットがあるという考え方のこと？
全域関数は[写像](https://scrapbox.io/mrsekut-p/%E5%86%99%E5%83%8F)のことらしい

https://softwareengineering.stackexchange.com/questions/334874/in-the-context-of-functional-programming-what-are-total-functions-and-partia

### Composition

関数の合成の話っぽい

#### Composition of Functions in F#

ある関数のアウトプットと、ある関数のインプットが同じ場合に、`piping`という手段で合成を行うことが多い。
linuxのパイプと同じ

#### Building an Entire Application from Functions

小さなfunctionを繋げていって、繋げていって、アプリケーションを作る

serviceとかworkflowって明確な区分あったっけ？

#### Challenges in Composing Functions

アウトプットとインプットの型が合わない時はどうやって合成する？
->
何らかの関数をかます。例えば、intからOption<int>に変換するのなら、Someをかます。

### Wrapping Up 

```
この章では、F#における関数型プログラミングの基本的な概念、すなわち、あらゆる場所で関数をビルディングブロックとして使用し、それらを構成可能なように設計することを紹介しました。
この原則を理解した上で、いよいよ本格的なコーディングに入ります。次の章では、これらの概念を実践し、発注ワークフローのパイプラインを構築することから始めます。
```

## Chapter 9 Implementation: Composing a Pipeline

これまで見てきた例について、関数の合成を行っていく。
関数の合成を行っていく際には、依存に関わる部分とeffectsが生じる関数が単純な合成を阻む。

この章ではDIについて見ていく。effectsに関するところについては次の章で見る。

### Working with Simple Types

createというファクトリメソッド
値を容易に取り出すためにvalueメソッドを用意

### Using Function Types to Guide the Implementation

function型を使う利点について述べているが全く分からない。
F#に限定された話か？

### Implementing the Validation Step

`toCustomerInfo`や`toAddress`は変換ヘルパーメソッド

#### Creating a Valid, Checked Address

addressをチェックするところの実装

F#の実装方法でつまづくようになってきたな。。

partial applicationについておさらい

#### Creating the Order Lines

letで出てくる()ってなんだっけ?
->
https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/functions/let-bindings#type-annotations

`to~~`みたいなファクトリメソッドの紹介

#### Creating Function Adapters

汎用的に利用できるadapterのようなものを作成
function transformer

### Implementing the Rest of the Steps

#### Implementing the Acknowledgment Step

`sendAcknowledgment`の実装詳細はまだ明らかにしなくとも良い

#### Creating the Events

`createBillingEvent`で`BillableOrderPlaced`イベントを作成する

最小公倍数の手法(lowest common multiple approach)ってなんだっけ？
-> 多分そのまま最小公倍数の意味

`listOfOption`でoption をlistにする。

yieldとはなんだっけ？
https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/sequences#the-yield-keyword
yieldを使えば、シーケンスの要素を返すことができる。
yield []の形にすれば、listの中の要素をバラしてシーケンスの要素とすることができる。

互換性のないものを共有型にするテクニックを使っているらしい。
上記でいくとどこだ？
PlaceOrderEventで選択型を作っているところか？

### Composing the Pipeline Steps Together

```F#
let placeOrder: PlaceOrderWorkflow = 
  fun unvalidateOrder -> 
    unvalidatedOrder
    |> validateOrder
    |> priceOrder
    |> acknowledgeOrder
    |> createEvents
```

シンプルにやりたいことを示したコードは上記のようになるが、パイプライン間でのinput, outputの齟齬がある。
validateOrderの周りを見てみると、
- validateOrderのinputには依存関係の2つのインプットが追加で必要
- validateOrderのoutputを利用するpriceOrderは、そのoutputの他に1つの依存関係が別途必要

従前の章でも述べたように、この齟齬をなくすのが関数型プログラミングにおける困難な部分の1つ。
解決方法としては、ここではpartial applicationを使う。

下記みたいに１つのパラメータを持つ関数に変形する。

```F#
let validateOrder' = validateOrder checkProductCodeExists checkAddressExists
```

この章では注入するcheckProductCodeExists や checkAddressExists の詳細については述べていない。

次に依存性の注入方法を見ていく

### Injection Dependencies

オブジェクト指向プログラミングなら、依存関係の解決にはIoCコンテナを使うことが多い。
一方、関数型プログラミングの場合は依存関係が暗黙の了解になることを嫌う。
依存性を明示的なパラメータとして渡す。
"reader monad", "free monad"みたいな手法があるらしい。

コンポジションルートにて、依存関係の具体を注入する。
コンポジションルートはアプリケーションのエントリポイントのある位置というイメージ。

Suave frameworkの例が一番わかりやすいかも。
ここでメインで言いたいことは、DIについてはコンポジションルート内で具体を入れてやり、それを各下位の関数に渡してやるということ。

#### Too Many Dependencies?

依存関係を整理する工夫をしましょうねという話。

全ての依存関係を全部同じようにバケツリレーさせるようなことはしない。
`checkAddressExists`に関して、endpoint, credential, unvalidatedAddressの3つを渡すものであったなら、
endpointとcredentialの2つはコンポジションルートで具体化してしまって、partial application化してしまう。

あらかじめ埋め込む(prebuild)ようなヘルパー関数を作成して、外から渡す依存の数を減らす。

### Testing Dependencies

テストコードの名前はダブルクオートで囲うことが多い。

関数型プログラミングで記述することによって得られるメリット
```
これはごく小さな例ですが、関数型プログラミングの原理をテストに用いることで、実用的なメリットが得られることがすでにわかっています。
• validateOrder関数はステートレスです。 何も変異させず、同じ入力で呼び出しても同じ出力を得ることができます。このため、この関数のテストは簡単です。
• すべての依存関係が明示的に渡されているので、どのように動作するか理解しやすいです。
• すべての副作用は、関数自体に直接ではなく、パラメータにカプセル化されています。これにより、関数のテストが容易になり、副作用の制御も容易になりました。
```

```
テストは大きなテーマであり、ここでは説明しきれません。ここでは、F#に適した人気のテストツールをいくつか紹介します。
• FsUnit は、NUnitやXUnitといった標準的なテストフレームワークを、 F#で使いやすい構文でまとめたものです。
• Unquoteは、テストの失敗に至るまでのすべての値を示しています(いわば "unrolling the stack "です)。
• もしあなたが NUnit のような「サンプルベース」のテストアプローチしか知らないのであれば、ぜひ「プロパティベース」のテストアプローチを調べてみてください。FsCheckは、F#の主要なプロパティベースのテストライブラリです。
• Expectoは軽量なF#のテストフレームワークで、[<Test>]のような特別な属性を必要とせず、標準的な関数をテストフィクスチャとして使用します。
```

サンプルベース、プロパティベースとは？
->
https://blogs.oracle.com/otnjp/post/know-for-sure-with-property-based-testing-ja

### The Assembled Pipeline

これまで作成してきた部品が具体的にどうファイルに記述されるかを伝えている。

### Wrapping Up

```
この章では、パイプラインのステップの実装と依存関係の処理に全面的に集中した。
各ステップの実装は、1つのインクリメンタルな変換を行うことに焦点を絞ったもので、単独での推論やテストが容易なものでした。

しかし、ステップを合成するときに、型が一致しないことがありました。そこで、3つの重要な関数型プログラミングの手法を導入しました。
- 「adapter function」を使って、関数をある「形」から別の「形」に変換する。この例では、checkProductCodeExistsの出力をboolからProductCodeに変更する。
- イベントと同じように、異なる型を共通の型に「Lifting」することで、すべての型を共通のPlaceOrderEvent型に変換する。
- 部分的なアプリケーションを使用して依存関係を関数に焼き付けることで、関数をより簡単に構成できるようになり、また呼び出し元から不要な実装の詳細を隠すことができます。

本書の後半で、これらの同じテクニックを再び使用することになります。

まだ、1つ触れていないことがあります。
この章では、エフェクトの処理を避け、代わりにエラー処理に例外を使用しました。
これは構成する上では便利ですが、文書化する上では最悪で、私たちが望むような、より明示的な関数シグネチャではなく、まやかしの関数シグネチャを導くことになります。
次の章では、それを修正します。すべての結果型を関数型に戻し、それをどのように扱うかを学びます。
```

## Chapter 10 Implementation: Working with Errors 

Errorについてみていく

ここまではResultを意図的に除いて例外を出すことにしていたがここでは考慮する。

```
より一般的には、エラー処理に対する関数的アプローチを探り、醜い条件分岐やtry/catch文でコードを汚染することなく、エレガントにエラーを捕捉するテクニックを開発します。
また、ある種のエラーをドメインエラーとして扱い、ドメイン駆動設計の他の部分と同じように注意を払うべき理由についても説明します。
```

### Using the Result Type to Make Errors Explicit

total functionを作りたい。起きうる結果全てを型によって表現したい、という意味合い。
Resultを利用する。

例外を起こしてしまうということはこの型だけでは表現しきれていないということ。

下記みたいにすれば、どんなエラーが起きているか明示的に表現できる。

```
type CheckAddressExists = 
  UnvalidatedAddress -> Result<CheckAddress, AddressValidationError>
and AddressValidationError =
  | InvalidFormat of string
  | AddressNotFound of string
```

この型からわかること。
- 入力はUnvalidatedAddressです。
- 検証が成功した場合、出力は(おそらく異なる)次のようになります。
- 検証が成功しなかった場合は、フォーマットが無効であるか、アドレスが見つからないことが原因です。

### Working with Domain Errors

全てのエラーを網羅的に記述することは無理なので、エラーを分類して対処するアプローチを考える。
エラーは3種に大別できる。

- ドメインエラー
  - これはビジネスプロセスの一部として予想されるエラーであり、ドメインの設計に含まれなければなりません。
    - 例えば、請求書によって拒否された注文や、無効な製品コードを含む注文などです。ビジネスでは、このようなことに対処するための手順がすでに用意されており、コードにはこれらのプロセスを反映させる必要があります。
- パニック
  - パニックとは、処理不可能なシステムエラー(「メモリ不足」など)やエラーなど、システムを未知の状態にするエラーのことです。
- インフラエラー
  - ネットワークのタイムアウトや認証失敗など、アーキテクチャの一部として想定されるが、ビジネスプロセスの一部ではなく、ドメインにも含まれないエラーのこと。

ドメインエラーに関しては、他と同様にドメインの一部であり、ドメインモデルに組み込まれるべきであるもの。

モデル化したくないエラーはトップレベル関数でキャッチするようにする。
パニックに関しては基本、モデル化しない。インフラエラーはモデル化するしないの剪定の方法は場合によりけりっぽい

#### Modeling Domain Errors in Types 

受注生産のワークフローにおけるエラーについて考えている。
エラーの型を選択型にする。
型に応じて処理を変えたりする。

選択型を利用してエラーを表現することのメリットは下記。

```
このように選択タイプを使用することの良い点は、うまくいかない可能性のあるすべての事柄について、コードの中で明示的なドキュメントとして機能することです。
また、エラーに関連する追加情報も明示的に表示されます。
さらに、要件の変化に応じて選択タイプを簡単に拡張(または縮小)できるだけでなく、安全性も確保されています。
というのも、コンパイラは、このリストに対してパターンマッチを行うコードが、ケースを見逃した場合に警告を発することを保証するからです。
```

#### Error Handling Makes Your Code Ugly

各ステップでエラー処理をすると、コードがエラー処理ばかりになってしまう。

### Chaining Result-Generating Functions

図をいっぱい使って説明している。
成功のルートと失敗のルートで大別して、失敗に関しては2つの入り口があるということで、アダプターが必要という話をしている。

#### Implementing the Adapter Block

変換のアダプターは簡単に作ることができる。

- 入力は「switch」関数です。出力は新しい2トラックのみの関数で、2トラックの入力と2トラックの出力を持つラムダとして表されます。
- ツートラックの入力が成功した場合、その入力をswitch関数に渡します。switch関数の出力はtwo-trackの値なので、これ以上何もする必要はありません。
- ツートラック入力が故障の場合は、スイッチ機能をバイパスして故障を返します。

ツートラックインプットは、いわゆるResult型であるっぽい。

下記のbind、mapを用いる。
```
let bind switchFn =
  fun twoTrackInput ->.
    match twoTrackInput with
  | Ok success -> switchFn success 
  | Error failure -> Error failure 
```

```
let map f aResult = 
  match aResult with
    | Ok success -> Ok (f success) 
    | Error failure -> Error failure 
```

#### Organizing the Result Functions

Result関数をどのようにコードに入れていくか？

下記がコード実装例。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/master/src/OrderTaking/Result.fs

型名と同じmoduleの中にコードを入れていくのが一般的。

#### Composition and Type Checking

下記みたいな感じで構成していく。

```F#
type FunctionA = Apple -> Result<Bananas, ...>
type FunctionB = Bananas -> Result<Cherries, ...>
type FunctionA = Cherries -> Result<Lemon, ...>

let functionA: FunctionA = ...
let functionB: FunctionB = ...
let functionC: FunctionC = ...

let functionABC input = 
  input 
  |> functionA
  |> Result.bind functionB
  |> Result.bind functionC
```

#### Converting to a Common Error Type

パイプラインの全ての関数は同じエラータイプを持つ必要がある。
そのための変換を行う必要がある。

こんな関数を用意する。
```F#
let mapError f aResult = 
  match aResult with
  | Ok success -> Ok success
  | Error failure -> Error (f failure)
```

下記のような感じで使う。

```F#
let functionA: FunctionA = ...
let functionB: FunctionB = ...

let functionAWithFruitError input = 
  input |> functionA |> Result.mapError AppleErrorCase

let functionBWithFruitError input = 
  input |> functionB |> Result.mapError BananaErrorCase
  

let functionAB input = 
  input 
  |> functionAWithFruitError
  |> Result.bind functionBWithFruitError
```

AppleErrorCaseとBananaErrorCaseはFruitErrorの選択型。
FruitErrorが共通のエラー。

### Using bind and map in Our Pipeline

エラーの部分を具体例でやってみる。

```F#
let placeOrder unvalidatedOrder =
  unvalidatedOrder
  |> validateOrderAdapted
  |> Result.bind priceOrderAdapted
  |> Result.map acknowledgeOrder
  |> Result.map createEvents
```

上記でもまだコンパイルはできない。
acknowledgeOrderの出力はcreateEventsの入力にはならない。

### Adapting Other Kinds of Functions to th Two-Track Model

- 例外を発生させる関数
- 何も返さない関数

について、ここではみていく。

#### Handling Exception

これまでで、多くの例外はドメイン設計の一部ではなく、トップレベル以外では補足する必要がないとしてきた。
しかし、ドメインの一部として扱いたい場合はどうするか？

リモートサービスからの応答がタイムアウトした時のことを考える。

まず、エラーの原因となったサービスに関する型を定義する。

```F#
type ServiceInfo = {
  Name: string
  Endpoint: uri
}
```

次に上記をベースとしたエラーの型を定義

```F#
type RemoteServiceError = {
  Service: ServiceInfo
  Exception: System.Exception
}
```

こんな感じでエラーを出力するアダプターを作る

```F#
let serviceExceptionAdapter serviceInfo serviceFn x = 
  try
    Ok(serviceFn x)
  with
  | :? TimeoutException as ex -> 
    Error {Service=serviceInfo; Exception=ex}
  | :? AuthorizationException as ex -> 
    Error {Service=serviceInfo; Exception=ex}
```

最終的にはこんな感じに

```F#
let checkAddressExistsR address = 
  let adaptedService = serviceExceptionAdapter serviceInfo checkAddressExists
  
  address 
  |> adaptedService
  |> Result.mapError RemoteService
```

#### Handling Dead-End Functions

入力を受け取って何も返さない関数について。

例としては、ロギング、データベースへの書き込み、キューへのポストなど。

ここでは、元となるinputをそのまま後続へ流すと同時に、dead-endな関数を実行するようにする。
その際には、下記のようなtee関数を使う。

```F#
let tee f x = 
  f x 
  x
```

### Making Life Easier with Computation Expression

F#には`computation expressions`なるものがある。

```F#
let placeOrder unvalidatedOrder
  = unvalidatedOrder
  |> validateOrderAdapted
  |> Result.bind priceOrderAdapted 
  |> Result.map acknowledgeOrder 
  |> Result.map createEvents
```

上記コードが、`computation expressions`を使うと下記のようになる。

```F#
let placeOrder unvalidatedOrder 
  = result {.
    let! validatedOrder =
      validateOrder unvalidatedOrder
      |> Result.mapError PlaceOrderError.Validation
    let! pricedOrder =
      priceOrder validatedOrder
      |> Result.mapError PlaceOrderError.Pricing
    let acknowledgmentOption = 
      acknowledgeOrder pricedOrder
    let events =
      createEvents pricedOrder acknowledgmentOption
    return events
  }
```

このコードがどう機能する？

- 結果の計算式は、resultという単語で始まり、中括弧で囲まれたブロックを含みます。
- 特殊なlet!キーワードはletのように見えますが、実際には結果を"unwrap"して内部の値を取得します。let! validatedOrder=...のvalidatedOrderは通常の値であり、直接priceOrder関数に渡すことができます。
- エラーの種類はブロック全体で同じでなければならないため、先ほどと同様にResult.mapErrorを使用してエラーの種類を共通の種類に解除します。エラーは結果式では明示されていませんが、その型は一致している必要があります。
- ブロックの最後の行では、ブロックの全体的な値を示すreturnキーワードを使用しています。

[ computation expression ](https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/computation-expressions)

async用のも用意されている。

#### Composing Computation Expression

resultを使うことによって、部品と部品を組み合わせることが容易になる。

#### Validating an Order with Results

ここまでの例に関して、`computation expression`を利用すると下記のようになる。

```F#
let validateOrder :ValidateOrder =
  fun checkProductCodeExists checkAddressExists unvalidatedOrder
    -> result {.
      let! orderId =
        unvalidatedOrder.OrderId
        |> OrderId.create
        |> Result.mapError ValidationError
      let! customerInfo = 
        unvalidatedOrder.CustomerInfo 
        |> toCustomerInfo
        let ! shippingAddress = ... 
        let! billingAddress = ... 
        let! lines = ...
      let validatedOrder :ValidatedOrder = { 
        OrderId = orderId
        CustomerInfo = customerInfo OrderId=
        shippingAddress BillingAddress = billingAddress 
        billiAddres Lines = lines
    }
    return validatedOrder 
  }
```

validateOrderにおいては、ValidationErrorにエラーを統一する。
OrderId.create においてはエラー時にstringが返ってくるのでl、mapErrorしてValidationErrorにしてやる必要がある。

```F#
module OrderId =

    /// Return the string value inside an OrderId
    let value (OrderId str) = str

    /// Create an OrderId from a string
    /// Return Error if input is null, empty, or length > 50
    let create fieldName str =
        ConstrainedType.createString fieldName OrderId 50 str
```

https://github.com/swlaschin/DomainModelingMadeFunctional/blob/master/src/OrderTakingEvolved/Common.SimpleTypes.fs#L224-L232
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/master/src/OrderTakingEvolved/Common.SimpleTypes.fs#L83-L91

#### Working with List of Result

`toValidatedOrderLine`ってなんだっけ？
-> 1つのUnvalidatedOrderを受け取って、検証する関数。これが今回Resultで戻ってくることになった。

今回欲しいのはResultのlistではなくて、listのResult。

sequenceなる関数を作って list of Result を Result of list にする。

List.foldbackは下記の感じ。
https://fsharp.github.io/fsharp-core-docs/reference/fsharp-collections-listmodule.html#foldBack
listの1つの要素とstate valueを変換する関数と、list、初期値を引数に与えている感じ。

### Monads and More

Monadについて。

monadicな関数とは？
->
普通の値を受け取って、それを何らかエンハンスして返すような関数のことをさす。

```
技術的には、「モナド」とは、単に3つの要素を持つものを指す言葉です。
•データ構造
•いくつかの関連機能
•関数がどのように動作しなければならないか
についてのいくつかのルールここでのデータ構造は、Result型です。
モナドであるためには、データ型は2つの関連する関数も持っていなければならず、return とバインドします。
•return(pureとも呼ばれる)は、通常の値をモナディック型に変える関数です。ここで使用している型はResultなので、return関数は単なるOkコンストラクタです。
•bind(flatMapとも呼ばれる)は、モナディック関数(ここではResultを生成する関数)を連結するための関数です。この章の前半で、Resultに対するbindの実装方法を見ました。
これらの関数がどのように動作すべきかのルールは「モナドの法則」と呼ばれ、威圧的に聞こえますが、実際には実装が正しく、変なことをしていないことを確認するための常識的なガイドラインです。モナドの法則については、インターネットで簡単に調べることができますので、ここでは触れません。
```

#### Composing in Parallel with Applicatives

applicativesなるものについて。

ここでは詳細は説明できないが、validation errorのような、最初の１つだけを取り上げるというよりは、起きたエラー全てを持っておきたい、みたいな場合に使う何からしい。

### Adding the Async Effect

asyncの部分を入れ込むと下記のようになる

```F#
let validateOrder : ValidateOrder =
    fun checkProductCodeExists checkAddressExists unvalidatedOrder ->
        asyncResult {
            let! orderId =
                unvalidatedOrder.OrderId
                |> toOrderId
                |> AsyncResult.ofResult
            let! customerInfo =
                unvalidatedOrder.CustomerInfo
                |> toCustomerInfo
                |> AsyncResult.ofResult
            let! checkedShippingAddress =
                unvalidatedOrder.ShippingAddress
                |> toCheckedAddress checkAddressExists
            let! shippingAddress =
                checkedShippingAddress
                |> toAddress
                |> AsyncResult.ofResult
            let! checkedBillingAddress =
                unvalidatedOrder.BillingAddress
                |> toCheckedAddress checkAddressExists
            let! billingAddress  =
                checkedBillingAddress
                |> toAddress
                |> AsyncResult.ofResult
            let! lines =
                unvalidatedOrder.Lines
                |> List.map (toValidatedOrderLine checkProductCodeExists)
                |> Result.sequence // convert list of Results to a single Result
                |> AsyncResult.ofResult
            let pricingMethod =
                unvalidatedOrder.PromotionCode
                |> PricingModule.createPricingMethod

            let validatedOrder : ValidatedOrder = {
                OrderId  = orderId
                CustomerInfo = customerInfo
                ShippingAddress = shippingAddress
                BillingAddress = billingAddress
                Lines = lines
                PricingMethod = pricingMethod
            }
            return validatedOrder
        }
```

ValidatedOrderの中身もAsyncResultにしなきゃいけないのか？

### Wrapping Up 

```
エラー処理と非同期効果に対する型安全なアプローチを取り入れた、パイプラインの改訂版実装が完成しました。
上のメインのplaceOrderの実装はまだ非常に明確で、流れを乱す醜いエラー処理コードはありません。
確かに、すべての型を正しく揃えるために厄介な変換をしなければなりませんでしたが、その余分な努力は、すべてのパイプラインコンポーネントが何の問題もなく一緒に機能するという確信に報われるのです。

次の数章では、ドメインと外界の間のインタラクションの実装に取り組みます。
データのシリアライズとデシリアライズの方法と、データベースへの状態の永続化の方法です。
```

## Chapter 11 Serialization 

外部インフラと連携する上で、シリアライズは避けられない。
ここではドメインオブジェクトの変換についてみていく。

### Persistence vs. Serialization

ここでの永続性の定義は、「状態が、それを作成したプロセスよりも長く続くこと」
シリアル化は、「ドメイン固有の表現からバイナリ、json、xmlなどの永続化が容易な表現に変換するプロセス」

この章ではシリアル化に焦点をあて、次の章で永続化についてみていく。

### Designing for Serialization

シリアライズ、デシリアライズはDTOで行う。
なので、ドメイン->DTOへの変換やDTO->ドメインへの変換が必要で、ドメイン固有のvalidationは変換時に実施する。

### Connecting the Serialization Code to the Workflow

json,dto,domainへの変換をへてworkflowに繋げられるよね、という説明。

#### DTOs as a Contract Between Bounded Contexts

境界づけられたコンテキスト間での契約を変える際には、慎重に行う必要がある。

### A Complete Serialization Example

toDomain, fromDomainはDTOに持たせる。
toDomainはドメインのチェックで失敗する可能性があるので、Result型で返す。

#### Wrapping the JSON Serializer

Newtonsoft.jsonなるライブラリでjsonへのシリアライズをしている。

#### A Complete Serialization Pipeline

シリアライズパイプラインは簡単だけど、デシリアライズはResultが変える場合があるからややこしい。
Result.mapErrorでもってエラーを共通の型にするようにしている。

デシリアライズ時のエラーを予期される状態として処理すべきか、パニックとして処理すべきかは呼び出し元の信頼度による。

#### Working with Other Serializers

シリアライズをjsonにしたり、xmlにしたりする場合には別途プロパティをDTOに足す必要がある。
ここにドメインとDTOを分けた意味が出る。ドメインはこのようなインフラ側の都合に汚染されない。

#### Working with Multiple Versions of a Serialized Type

DTOのバージョンを複数保持しなければいけない場合が出てくるかもしれない。
これについては本書では解説しない。

[Versioning in an Event Sourced System](https://www.goodreads.com/book/show/34327067-versioning-in-an-event-sourced-system)が詳しい。

### How to Translate Domain Types to DTOs

ドメインをDTOにどのように変換していくかをみていく。

#### Single-Case Union

これまでsimple typeと呼んできたもの。

```F#
type ProductCode = ProductCode of string 
```

上記の例だったら、stringがDTOでの型になる。

#### Options

optionの場合、Noneならnullに置き換える。
intとか、プリミティブなものに関しては、Nullable<int>のようなものを使用する必要がある。
https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/nullable-value-types

#### Records

各フィールドがDTOと同等のものに変換できるのであれば、DTOでもレコードとして利用できる。
本文の例をみるのが一番良い。

#### Collections

コレクションを扱う場合は、シリアル化のフォーマットによってどう変換するか異なる。

#### Discriminated Unions Used as Enumerations

ENUMをシリアライズ、デシリアライズする時の対応。

#### Tuples

tupleについて、これは対応したシリアライズ形式はないので、特別にDTOを定義する必要がある。

#### Choice Types

選択型の場合どうするか？

各選択型についてフィールドを持たせ、タグでそれを判別するような形。

下記のようなドメインがある場合を考える。

```
type Name = {
 First : String50
 Last : String50
}

type Example =
 | A
 | B of int
 | C of string list
 | D of Name
```

この場合、DTOは以下の感じ。

```
type NameDto = {
 First : string
 Last : string
}

type ExampleDto = {
 Tag : string // "A", "B", "C", "D "のいずれか。
 // Aの場合、データはありません。
 BData : Nullable<int> // Bケースのデータ
 CData : string[] // Cケースのデータ 
 DData : NameDto // Dの場合のデータ
}
```

シリアル化は下記の感じになる。

```
let nameDtoFromDomain (name:Name) :NameDto 
 let first = name.First |>String50.value
 let last = name.Last |> String50.value
 {First=First; Last=Last}

let fromDomain (domainObj:Example) :ExampleDto = 
 let nullBData = Nullable()
 let nullCData = null
 let nullDData = Unchecked.defaultof<NameDto>
 match domainObj with
 | A ->
  {Tag="A"; BData=nullBData; CData=nullCData; DData=nullDData}
 | B i ->
  let bdata = Nullable i
  {Tag="B"; BData=bdata; CData=nullCData; DData=nullDData}
 | C strList ->
  let cdata = strList |> List.toArray
  {Tag="C"; BData=nullBData; CData=cdata; DData=nullDData}
 | D name ->
  let ddata = name |> nameDtoFromDomain
  {Tag="D"; BData=nullBData; CData=nullCData; DData=ddata}
```

デシリアライズの時は以下の感じ。タグでswitchする。

```
let nameDtoToDomain (nameDto:NameDto) :Result<Name,string> =
 result {
  let! first = nameDto.First |> String50.create 
  let! last = nameDto.Last |> String50.create 
  return {First=first; Last=last}
}

let toDomain dto :Result<Example,string> = 
 match dto.Tag with
  | "A" -> OK A
  | "B" ->
   if dto.BData.HasValue then
    dto.BData.Value|> B|> Ok
   else
    Error "B data not expected to be null"
  | "C" ->
   match dto.CData with
   | null ->
    Error "C data not expected to be null" 
   | _ ->
    dto.CData|> Array.toList|> C|> Ok
  | "D" ->
   match box dto.DData with
   | null ->
    Error "D data not expected to be null" 
   | _ ->
    dto.DData
    |> nameDtoToDomain // 結果を返す...
    |> Result.map D // ...だから "map "を使わなければならない。
    | _ ->
     // その他のケース
     let msg = sprintf "Tag '%s' not recognized" dto.Tag 
     Error msg
```

#### Serializing Records and Choice Types Using Maps

互いのIFをあまり決めずに、とりあえずMapで値を保持するパターン。
キーバリューマップには何でも含められる一方、契約が全くないので期待値のミスマッチがあっても気づくことができない。

#### Generics

本書にも書いてあるが、シリアル化が必要なジェネリック型はほとんどないはず。

やるとしたらこんな感じっぽい。
```
type PlaceOrderResultDto =
 { 
  IsError : bool
  OkData :PlaceOrderEventDto[] 
  ErrorData :PlaceOrderErrorDto
 }
```

### Wrapping Up

```
この章では、境界のあるコンテキストとクリーンなドメインを離れ、インフラの厄介な世界へと足を踏み入れました。
この章では、境界のあるコンテキストと外の世界をつなぐ仲介役として、直列化可能なデータ転送オブジェクトを設計する方法を学び、独自の実装に役立つ多くのガイドラインを調べました。

シリアライゼーションは外の世界との相互作用の一種ですが、それだけではありません。
ほとんどのアプリケーションでは、ある種のデータベースと対話する必要があります。
次の章では、リレーショナルデータベースやNoSQLデータベースでドメインモデルを動作させるための、永続化のテクニックと課題に目を向けます。
```

## Chapter 12 Persistence

NoSQLとトラディショナルなSQLでの永続化についてみていく。

最初に、DDDにおける永続化のガイドラインをみていく

- 永続化を端に追いやる
- コマンド(アップデート)とクエリ(リード)を分ける。
- バウンデッドコンテクストは、独自のデータストアを所有する

### Pushing Persistence to the Edges

ロジックの部分はドメインに固めて、I/Oを行う部分はworkflowの端に追いやり、読み込み、保存のみを行うようにする。

I/Oを行う部品はparameterとして受け取り、外部からstubを入れられるようにする。

#### Making Decisions Based on Queries 

pureなコードの中間でDBからの読み込みに基づいて判断を下したい場合はどうする？
-> 
I/Oとロジックが何層にも重なる場合には、[Long-Running Workflows](#Long-Running Workflows)を利用する。

#### Where's the Repository Pattern?

Repositoryパターンは関数型言語にはそぐわない。

### Command-Query Separation

- insert,update, deleteはDBの状態を変更し、データを得ることが主目的ではない
- readはDBの状態を変更せず、有益なデータを得る

上記の２種で明確に分けて考える。

こんな型になりそうだ。
```
type DbError = ...   
type DbResult<'a> = AsyncResult<'a,DbError>     

type InsertData = Data -> DbResult<Unit>   
type ReadData = Query -> DbResult<Data>   
type UpdateData = Data -> DbResult<Unit>   
type DeleteData = Key -> DbResult<Unit>
```

#### Command-Query Responsibility Segregation

command, queryで同じ部品を使うのは良くない。

- クエリで得られるデータとデータ作成で必要なものは異なることが多い
- クエリとコマンドは独立して進化することが多い
- 複数のエンティティを一度にかえすクエリもある

書き込みと読み込みを分けると下記の感じに。

```
type SaveCustomer = WriteModel.Customer -> DbResult<Unit>
type LoadCustomer = CustomerId -> DbResult<ReadModel.Customer>
```

#### CQRS and Database Segregation

データベースを論理的に２つに分け、片方はクエリ専用、片方はコマンド専用としてしまう。

#### Event Sourcing

状態に変化があるたびに、その変化を表すオブジェクトが永続される

### Bounded Contexts Must Own Their Data Storage

境界づけられたコンテキストにて、自身のDBを保有しなければならない。
そして、ある境界づけられたコンテキストのDBに対して、別の境界づけられたコンテキストからアクセスしてはならない。

- 境界のあるコンテキストは、自分のデータストレージと関連するスキーマを所有しなければならず、他の境界のあるコンテキストと調整することなく、いつでもそれらを変更することができます。
- 他のシステムは、バウンドしたコンテキストが所有するデータに直接アクセスすることはできません。その代わりに、クライアントは束縛されたコンテキストのパブリックAPIを使用するか、データストアの何らかのコピーを使用する必要があります。

#### Working with Data from Multiple Domains

OLTPとOLAP?
->
https://www.gixo.jp/blog/2934/

複数のコンテキストのデータが必要となる例として、BIツールをあげている。

BIツールで複数のコンテキストのデータを集める方法として、
- イベントのサブスクライブ
- ETLを使ったデータのコピー
- [キューブ](https://it-trend.jp/bi/article/cube)の開発

をあげている。

### Working with Document Databases

document dbを使ってjson文字列を保存する例を出している。

### Working with Relational Databases

RDBの考え方と関数型の考え方は割と近い、が、異なる部分もあるので注意。

ソースコードにおけるオブジェクトとデータベースのカラムとの間で起こる齟齬をインピーダンスミスマッチと呼んでいる。
昔からそこの整合性を合わせるのに苦労してきた。
インピーダンスミスマッチの話はこの辺りがわかりやすかった。
https://ja.wikipedia.org/wiki/%E3%82%A4%E3%83%B3%E3%83%94%E3%83%BC%E3%83%80%E3%83%B3%E3%82%B9%E3%83%9F%E3%82%B9%E3%83%9E%E3%83%83%E3%83%81

関数型言語の操作とデータベースの操作は似ている。
myopinion: これは達人に学ぶSQL徹底指南でも言ってた。

集合指向のオペレーション(SELECT, WHERE)はリスト指向のオペレーション(map, filter)と同様である。

---
集合指向についての言及は下記。
https://mickindex.sakura.ne.jp/database/db_laws.html
一方、リスト指向については特にネットから引っ張ってこれなかった。
---

ただ、dbはプリミティブな値しか格納できないし、選択型にうまく対応しているわけではない。

#### Mapping Choice Types to Tables

選択型をDBに入れる際にどうすればいいか？がテーマの節。

要約すると、下記の2つが解答。 
- 全て１つのテーブルに入れる
  - フラグを表すカラムを用意する
  - null許容なカラムができる
- 各々のケースで1つのテーブルにする
  - 親テーブルでフラグを持ち、子テーブルがケースの分だけある

参考資料(o/r mappingに関する資料)
http://www.agiledata.org/essays/mappingObjects.html

共通部分が多い場合は前者で、少ない場合は後者にすることが多い
(具体例は本を参照)

```mermaid
erDiagram

ContactInfo {
  int ContactId 
  bit IsEmail
  bit IsPhone
  nvarchar EmailAddress
  nvarchar PhoneNumber
}
```

```mermaid
erDiagram

ContactInfo {
  int ContactId 
  bit IsEmail
  bit IsPhone
}
ContactEmail {
  int ContactId 
  nvarchar EmailAddress
}
ContactPhone {
  int ContactId 
  nvarchar PhoneNumber
}
ContactInfo ||--o| ContactEmail : contains
ContactInfo ||--o| ContactPhone : contains
```

#### Mapping Nested Types to Tables

型が他の型をネストしているときは？
->
- インナータイプがDDDのEntityで、独自のアイデンティティを持つ場合は、別のテーブルに格納する必要があります。
- インナータイプがDDDのバリューオブジェクトで、独自のアイデンティティを持たない場合は、親データと「インライン」で保存する必要があります。

(具体例は本を参照)

entityは別テーブルにして、valueオブジェクトは同じテーブルに含める。

```mermaid
erDiagram

Order {
  int OrderId 
  varchar ShippingAddress1
  varchar ShippingAddress2
  varchar ShippingAddressCity
  varchar BillingAddress1
  varchar BillingAddress2
  varchar BillingAddressCity
}
OrderLine {
  int OrderLineId
  int OrderId 
  int ProductId
  int Quantity
}
Order ||--|{ OrderLine : contains
```

#### Reading from a Relational Database

F#ではORM使わないことが多い。

[ type provider ](https://zenn.dev/flipflap/articles/fsharp-typeprovider) なるものを利用すると、コンパイル時に不備に気づける。
コンパイル時にsqlの不備に気づける、みたいなのはよくわからなかった。
それはつまり、本物のdbと常にコネクションを持っておかねばならないということ？

DBから取得して、ドメインに変換するところまでを具体例として書いている。

#### Reading Choice Types from a Relational Database

選択型について、１つのテーブルで表現した場合のDBからドメインに変換する例をあげている。

#### Writing to a Relational Database

テーブルへの登録の具体例をあげている。

`<-`は変数への値の代入。
https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/symbol-and-operator-reference/#symbols-used-in-imperative-expressions

### Transactions

トランザクション単位での登録について具体例をあげている。

また、複数のデータソースに対して同一トランザクションでやろうということに対しては、スターバックスは２相コミットをしない話を例にあげて、厳密な一貫性を求めるよりは補償トランザクションを考えるべきと述べている。
https://docs.microsoft.com/ja-jp/azure/architecture/patterns/compensating-transaction

### Wrapping Up

```
この章では、まず、クエリとコマンドを分離する、I/Oをエッジに留める、境界のあるコンテキストが自身のデータストアを所有する、といった永続化の高レベルな原則をいくつか見てきました。
そして、リレーショナルデータベースと対話するための低レベルのメカニズムに飛び込みました。

そして、本書の第3部の終わりを迎えました。
ドメイン内の純粋な型と関数 (第9章実装: パイプラインの構成)、エラー処理 (第10章実装: エラーの処理)、エッジでのシリアライズ (第11章シリアライズ)、そして本章では状態を保存するためのデータベースです。
しかし、私たちはまだ全く終わっていません。
軍隊のことわざに、"敵と接触して生き残る計画はない "というのがあります。
では、新しいことを学び、設計を変更する必要があるときはどうするのでしょうか？それが、次の最終章のテーマです。
```

## Chapter 13 Evolving a Design and Keeping It Clean

コードの変更がどのようにして行われるかをみていく。
ここでは4種類の変化を見ていく。

- ワークフローに新しいステップを追加する
- ワークフローへの入力変更
- 重要なドメインタイプ(注文)の定義を変更し、それがシステムにどのように影響するかを見る
- ワークフロー全体をビジネスルールに合わせて変換する

### Change 1: Adding Shipping Charges 

送料の計算方法を追加してみる。

```
地方の州への配送は一律の価格(例えば 5ドル)、遠隔地への発送は別料金(例えば10ドル)、他国への発送はさらに 別料金(20ドル)となります。
```

#### Using Active Patterns to Simplify Business Logic

アクティブパターンを利用して簡素化する。
https://docs.microsoft.com/ja-jp/dotnet/fsharp/language-reference/active-patterns
結構理解するのが難しい。
値に一時的な区分を与えるみたいな感じ？

カテゴライズとロジックを分離している。

#### Creating a New Stage in the Workflow

動作しているコードに手を入れると複雑化するので、shippingInfoを計算するステップを加える。

PricedOrderにShippingInfoフィールドを追加する形にするか？それとも新しい型を作るか？
新しい型を作る利点。

- AcknowledgeOrderステップがPricedOrderWithShippingInfoを入力として期待するように修正された場合、ステージの順序を間違えることはありません。
- PricedOrderのフィールドとしてShippingInfoを追加した場合、送料の計算が行われる前に何に初期化すべきでしょうか?単にデフォルト値に初期化するだけでは、バグが発生する可能性があります。

ShippingInfoをどのように含めるべきかも議論されている。

あとは実装で示している。

#### Other Reasons to Add Stages to the Pipeline

要件の変更に応じてパイプラインにステージを追加するようにしている。
この方法でできることの例が下記。

- 運用の透明性を高めるためのステージを追加することで、パイプライン内で何が起こっているのかを簡単に確認することができます。ロギング、パフォーマンスメトリクス、監査などを簡単に追加することができます。
- 認証をチェックするステージを追加し、それが失敗した場合には、パイプラインの残りの部分をスキップして、失敗パスに送り込むことができます。
- 入力からの設定やコンテキストに基づいて、コンポジションのルートにステージを動的に追加・削除することもできます

### Change 2: Adding Support for VIP Customers

VIPカスタマーを加えるような改修をする場合を考える。

CustomerInfoに情報を持たせるようにする。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/Common.CompoundTypes.fs#L25-L29

#### Adding a New Input to the Workflow

下記の変更だけ入れて、typeだけ更新するとコンパイルエラーが生じる。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/Common.CompoundTypes.fs#L25-L29

情報の入り口であるDTOと、Domainそのものと、変換処理であるvalidateCustomerInfoを修正する。

#### Adding the Free Shipping Rule to the Workflow

VIPなら配送料を無料にするためのコードをワークフローのどこかに入れる必要がある。
この時、既存のコードをいじるのではなく、新たにセグメントを入れ込むのがよかろう。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/PlaceOrder.Implementation.fs#L321-L333
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/PlaceOrder.Implementation.fs#L457

### Change 3: Adding Support for Promotion Codes

プロモーションコードで割引する仕組みを入れたい。

具体的にはこんな感じの要件
- ご注文の際に、お客様が任意でプロモーションコードを入力することができます。
- このコードがある場合、特定の商品には異なる（低い）価格が与えられます。
- 注文書には、プロモーション割引が適用されたことが表示されるはずです。

最後のやつは全体に結構な影響がある。

#### Adding a Promotion Code to the Domain Model

ドメインモデルにPromotionCodeを加える。

加えて、OrderDto、UnvalidatedOrderにPromotionCodeを加える。

#### Changing the Pricing Logic

promotion codeがあったらそれ用の価格計算をして、なかったら別の価格計算をする。
これをどうやって設計するか？

元々は商品価格取得には下記のような型を用意していた。
```F#
type GetProductPrice = ProductCode -> Price
```

しかし、現在はpromotion codeに基づいて、別のGetProductPriceをしたい。
ロジック的には
- プロモーションコードが存在する場合、そのプロモーションコードに関連する価格を返す GetProductPrice 関数を提供する。
- プロモーションコードが存在しない場合、元のGetProductPrice関数を提供する。


下記を用意して、
```F#
type PricingMethod = 
  | Standard
  | Promotion of PromotionCode
```

ValidatedOrderにPricingMethodを加える。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/PlaceOrder.InternalTypes.fs#L49

PricingMethodを元に計算する関数を返す。
```F#
type = GetPricingFunction = PricingMethod -> GetProductPrice
```

#### Implementing the GetPricingFunction

具体的な実装は下記のような感じ。
https://github.com/swlaschin/DomainModelingMadeFunctional/blob/70f7a53254382883bc04cd3cd739820663fdab3a/src/OrderTakingEvolved/PlaceOrder.Pricing.fs#L23-L55

#### Documenting the Discount in an Order Line

該当の商品に対して割引が適用されたかどうかを記す必要がある。

そのためにPricedOrderLineにCommentを加える。

priceOrder関数でやることは下記
- まず、GetPricingFunction "factory "から価格関数を取得します。
- 次に、各行について、その価格設定関数を用いて価格を設定する。
- 最後に、プロモーションコードが使用された場合、行のリストに特別なコメント行を追加します。

#### More Complicated Pricing Schemes



### Wrapping Up 

```
この章では、4つの要件変更に対応して設計を進化させる中で、型駆動のドメインモデリングと、関数からワークフローを作成する構成的アプローチのメリットを確認しました。

型駆動設計では、ドメイン型に新しいフィールドを追加すると（ValidatedOrderにVipStatusを追加するなど）、すぐにコンパイラーエラーが発生し、データの出所を特定することを余儀なくされました。
その結果、コンパイラーエラーがなくなるまで、他の型を修正するように誘導される。

同様に、プロモーションコードの例で依存関係の1つを変更したとき（GetProductPriceからより複雑なGetPricingFunctionへ）、これも多くのコンパイラーエラーを引き起こしました。
しかし、コードが修正され、コンパイラーエラーがなくなった後、私たちの実装が再び正しく動作していることに非常に自信を持つことができます。

また、ワークフローを構築する上で、関数合成を利用することのメリットも分かりました。
ワークフローに新しいセグメントを簡単に追加することができ、他のセグメントはそのままにしておくことができます。
もちろん、既存のコードに変更を加えないということは、バグが発生する可能性も低くなります。

最後に、「営業時間」の例では、「インターフェースとしての関数型」のおかげで、既存のコードとのプラグイン互換性を維持しながら、関数全体を強力に変換できることを確認しました。
```

### Wrapping Up the Book

```
この本では、bounded contextsのような抽象度の高いものから、シリアライズ形式の細かなものまで、さまざまな分野をカバーしています。

Webサービス、セキュリティ、運用の透明性など、多くの重要なトピックをカバーする機会はありませんでしたが、そのうちのいくつかを紹介します。
しかし、本書を読み進める過程で、どのような設計問題にも適用できるテクニックやスキルが身についていれば幸いです。

ここでは、これまで述べてきた中で最も重要なプラクティスをいくつか紹介します。
- 低レベルの設計を開始する前に、ドメインについて深く、共通の理解を深めることを目指すべきである。私たちは、このプロセスで非常に役立つ発見技術（イベントストーミング）とコミュニケーション技術（ユビキタス言語の使用）をいくつか取り上げました。
- そして、各ワークフローは、入力と出力を明示した独立したパイプラインとして表現されるべきです。
- コードを書く前に、ドメインの名詞と動詞の両方を捕らえるために、型に基づいた表記法を使用して要件を捕らえることを試みるべきである。これまで見てきたように、名詞はほとんど常に代数的な型システムで、動詞は関数で表すことができる。
- 重要な制約やビジネスルールは、可能な限り型システムに取り込むようにしなければならない。私たちのモットーは、「違法な状態を表現できないようにする」ことです。" 
- また、関数は「純粋」で「完全」であるように設計する必要があり、可能なすべての入力は明示的に文書化された出力を持ち（例外なし）、すべての動作は完全に予測可能です（隠れた依存関係なし）。

このようなプロセスを経て、受注・発注のワークフローでは、実装の指針と制約となる詳細な型のセットを作成することができました。

そして、実装の過程では、次のような関数型プログラミングの重要なテクニックを繰り返し使用しました。
- 小さな関数の組み合わせだけで、完全なワークフローを構築する。
- 依存関係や後回しにしたい意思決定があるときは、関数をパラメータ化する。
- 部分適用を使用して依存関係を関数に焼き付けることで、関数をより簡単に構成し、不要な実装の詳細を隠すことができます。
- 他の関数を様々な形に変換できる特殊な関数を作成する . 特に、bind - エラーを返す関数を、簡単に合成できる2トラック関数に変換するために使用する「アダプタブロック」について学びました。
- 異種の型を共通の型に " リフトアップ " することで、型の不一致の問題を解決する。

この本では、関数型プログラミングとドメインモデリングが非常に相性が良いことを納得してもらうことを目的としました。
そして、あなたが学んだことを自分のアプリケーションに応用する自信を得てくれることを願っています。
```

