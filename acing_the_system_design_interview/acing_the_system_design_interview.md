# Front matter

この本は2部構成。

- Part 1: システム設計面接で議論される様々なトピックを典型的な教科書形式でカバーする。非機能要件、API仕様、システムデータモデル、分散トランザクション、オブザーバビリティ、ログ管理といった側面から始まる。
- Part 2: Part 1でカバーされた概念を参照する、サンプル面接質問の議論が含まれる。Craigslistの設計、レート制限、通知サービス、データベースバッチ監査、オートコンプリート、Flickr、CDN、テキストメッセージングアプリ、Airbnb、ニュースフィード、Amazonのトップ10製品ダッシュボードの設計などが含まれる。

# 1 A walkthrough of system design concepts

```text
『Acing the System Design Interview』の第1章「システムデザインの概念を概観する」は、システムデザインの基本的な考え方とスケーリングの主要概念を紹介しています。
• システムデザインはトレードオフの議論である [1.1, 36]：
    ◦ システム設計の意思決定は、要件を満たすための異なるアプローチとそのトレードオフを比較検討することが重要です [1.1, 36]。
    ◦ 例として、Gzip圧縮はネットワークトラフィックを減らす一方で、CPUとメモリを消費するトレードオフがあります。
• 本書の目的 [1.3, 37]：
    ◦ システムデザイン関連の資料をまとめ、知識基盤を構築し、知識のギャップを特定する手助けをすることを目指しています [1.3, 37]。
• システムの様々なサービスをスケーリングするための議論 [1.4, 5]：
    ◦ スケーラビリティの定義：サービスの「スケーラビリティ」とは、負荷の変化（ユーザー数やリクエスト数の増減）に対応するため、割り当てられたリソースを容易かつ費用対効果の高い方法で変更する能力です。これは垂直スケーリング（より強力な単一ホストへのアップグレード）と水平スケーリング（複数のホストに負荷を分散する）に分けられ、本書では主に水平スケーリングが議論されます。
    ◦ 初期デプロイメント [1.4.1, 5, 38]：最初のアプリケーションは、コンシューマーアプリ（ブラウザ、iOS、Android）、ステートレスなバックエンドサービス、そして単一のSQLデータベースというシンプルな構成から始まります。
    ◦ スケーリング戦略の導入 [1.4.2-1.4.10, 5]：
        ▪ GeoDNS [1.4.2, 42, 43]：複数のデータセンターにサービスを配置し、ユーザーを地理的に最も近いデータセンターに誘導することで、レイテンシを最小化します。
        ▪ CDN (Content Distribution Network) [1.4.4, 45, 46]：静的ファイル（JavaScript、CSS、画像など）のコピーを世界中のデータセンターに保存し、ユーザーに最低レイテンシで提供します。これにより、レイテンシ、スループット、信頼性、コストが改善されます。
        ▪ 水平スケーラビリティとクラスター管理 [1.4.5, 5, 10]：サービスが**冪等（べきとう）**であれば、追加のホストをプロビジョニングすることで要求負荷をサポートできます。
        ▪ 機能的パーティショニングと横断的関心事の集中管理 [1.4.6, 5, 14]：共通の機能（ロギング、監視、アラート、認証・認可など）を共有サービスに集約するアプローチが紹介されています。
        ▪ サービスメッシュ / サイドカーパターン [1.4.6, 5, 16]：APIゲートウェイの代替案として、各サービスホストにサイドカーを配置して横断的な関心事を処理するパターンです。
        ▪ CQRS (Command Query Responsibility Segregation) [1.4.9, 55]：書き込み操作と読み取り操作を異なるサービスに機能的に分割するマイクロサービスパターンです。これにより、スケーラビリティが向上し、メンテナンスが容易になりますが、複雑さも増します。
        ▪ サーバーレス (FaaS - Function as a Service) [1.4.10, 56, 57]：AWS LambdaのようなFaaSプラットフォームは、使用頻度の低いエンドポイントや厳密なレイテンシ要件のない機能を費用対効果の高い方法で実装でき、開発者はビジネスロジックに集中できます。ただし、「コールドスタート」などの考慮事項があります。
第1章は、主にバックエンドサービスのスケーリングに関する概念と技術に焦点を当て、その多様性と複雑性を強調しています。
```

## 1.1 It is a discussion about tradeoffs

システム設計は正解があるわけではなく、アート。

## 1.2 Should you read this book?

システム設計に関する知識を深めたい人はよんでもいいんじゃない？

## 1.3 Overview of this book

この本は2つのパートに分かれる。1つ目はsystem design interviewで議論されるトピックについてのテキストブック的解説。
2つ目はサンプルインタビューを通じて、1つ目で学んだことを実際にどう使うかを示す。

## 1.4 Prelude—A brief discussion of scaling the various services of a system

### 1.4.1 The beginning: A small initial deployment of our app


:::note
Brotliという圧縮アルゴリズムを使うと、gzipよりも圧縮率が高いらしい。
:::

### 1.4.2 Scaling with GeoDNS

:::note
GeoDNSは、ユーザーを地理的に最も近いデータセンターに誘導することで、レイテンシを最小化する。
:::

### 1.4.3 Adding a caching service


### 1.4.4 Content distribution network

### 1.4.5 A brief discussion of horizontal scalability and cluster management, continuous integration, and continuous deployment

### 1.4.6 Functional partitioning and centralization of cross-cutting concerns

- ログとかの機能横断的機能
- 外部からの通信に関しては、api gatewayの利用
- CQRS

### 1.4.7 Batch and streaming extract, transform, and load (ETL)

### 1.4.8 Other common services

### 1.4.9 Cloud vs. bare metal

cloudの利点を論じてる。
- エンジニアのコスト削減
- セットアップの容易さ
- 初期費用が安い
- 多くの人から使われるという観点から、cloudの方が使いやすい
- upgradeがしやすい

デメリットはベンダーロックインしてしまうこと。

### 1.4.10 Serverless (Function as a Service)

:::note
OpenFaaSというオープンソースのFaaSプラットフォームもある。
:::

:::note
sprint cloud functionsはビジネスロジックと、ベンダー固有のglueコードを別の層に分離し、プログラマーにはビジネスロジックのみを意識させるようになってるみたい
:::

### 1.4.11 Conclusion: Scaling backend services

# 2 A typical system design interview flow



2.5 Logging, monitoring, and alerting
2.6 Search bar
2.7 Other discussions
2.8 Post-interview reflection and assessment
3 Non-functional requirements
3.2 Availability
3.3 Fault-tolerance
3.5 Consistency
3.6 Accuracy
3.10 Privacy
3.11 Cloud native
3.12 Further reading
4 Scaling databases
4.3 Replication
4.4 Scaling storage capacity with sharded databases
4.5 Aggregating events
4.6 Batch and streaming ETL
4.7 Denormalization
4.8 Caching
4.9 Caching as a separate service
4.10 Examples of different kinds of data to cache and how to cache them
4.11 Cache invalidation
4.12 Cache warming
4.13 Further reading
5 Distributed transactions
5.1 Event Driven Architecture (EDA)
5.2 Event sourcing
5.3 Change Data Capture (CDC)
5.4 Comparison of event sourcing and CDC
5.5 Transaction supervisor
5.6 Saga
5.7 Other transaction types
5.8 Further reading
6 Common services for functional partitioning
6.1 Common functionalities of various services
6.2 Service mesh / sidecar pattern
6.3 Metadata service
6.4 Service discovery
6.5 Functional partitioning and various frameworks
6.6 Library vs. service
6.7 Common API paradigms
Part 2
7 Design Craigslist
7.1 User stories and requirements
7.2 API
7.3 SQL database schema
7.4 Initial high-level architecture
7.5 A monolith architecture
7.6 Using a SQL database and object store
7.7 Migrations are troublesome
7.8 Writing and reading posts
7.9 Functional partitioning
7.10 Caching
7.11 CDN
7.12 Scaling reads with a SQL cluster
7.13 Scaling write throughput
7.14 Email service
7.15 Search
7.16 Removing old posts
7.17 Monitoring and alerting
7.18 Summary of our architecture discussion so far
7.19 Other possible discussion topics
8 Design a rate-limiting service
8.3 Functional requirements
8.5 Discuss user stories and required service components
8.6 High-level architecture
8.7 Stateful approach/sharding
8.8 Storing all counts in every host
8.9 Rate-limiting algorithms
8.10 Employing a sidecar pattern
8.11 Logging, monitoring, and alerting
8.12 Providing functionality in a client library
8.13 Further reading
9 Design a notification/alerting service
9.1 Functional requirements
9.2 Non-functional requirements
9.3 Initial high-level architecture
9.4 Object store: Configuring and sending notifications
9.5 Notification templates
9.6 Scheduled notifications
9.7 Notification addressee groups
9.8 Unsubscribe requests
9.9 Handling failed deliveries
9.10 Client-side considerations regarding duplicate notifications
9.11 Priority
9.12 Search
9.13 Monitoring and alerting
9.14 Availability monitoring and alerting on the notification/alerting service
9.15 Other possible discussion topics
9.16 Final notes
10 Design a database batch auditing service
10.1 Why is auditing necessary?
10.2 Defining a validation with a conditional statement on a SQL query’s result
10.3 A simple SQL batch auditing service
10.4 Requirements
10.5 High-level architecture
10.6 Constraints on database queries
10.7 Prevent too many simultaneous queries
10.8 Other users of database schema metadata
10.9 Auditing a data pipeline
10.10 Logging, monitoring, and alerting
10.11 Other possible types of audits
10.12 Other possible discussion topics
10.13 References
11 Autocomplete/typeahead
11.1 Possible uses of autocomplete
11.2 Search vs. autocomplete
11.3 Functional requirements
11.4 Nonfunctional requirements
11.5 Planning the high-level architecture
11.6 Weighted trie approach and initial high-level architecture
11.7 Detailed implementation
11.8 Sampling approach
11.9 Handling storage requirements
11.10 Handling phrases instead of single words
11.11 Logging, monitoring, and alerting
11.12 Other considerations and further discussion
12 Design Flickr
12.1 User stories and functional requirements
12.2 Non-functional requirements
12.3 High-level architecture
12.4 SQL schema
12.5 Organizing directories and files on the CDN
12.6 Uploading a photo
12.7 Downloading images and data
12.8 Monitoring and alerting
12.9 Some other services
12.10 Other possible discussions
13 Design a Content Distribution Network (CDN)
13.1 Advantages and disadvantages of a CDN
13.2 Requirements
13.3 CDN authentication and authorization
13.4 High-level architecture
13.5 Storage service
13.6 Common operations
13.7 Cache invalidation
13.8 Logging, monitoring, and alerting
13.9 Other possible discussions on downloading media files
14 Design a text messaging app
14.1 Requirements
14.2 Initial thoughts
14.3 Initial high-level design
14.4 Connection service
14.5 Sender service
14.6 Message service
14.7 Message sending service
14.9 Logging, monitoring, and alerting
14.10 Other possible discussion points
15 Design Airbnb
15.1 Requirements
15.2 Design decisions
15.3 High-level architecture
15.4 Functional partitioning (注：このセクションは、提示されたコンテンツリストの抜粋には明示的に番号付けされていませんが、会話履歴と書籍コンテンツのフローに基づいて含まれています。)
15.5 Create or update a listing
15.6 Approval service
15.7 Booking service
15.8 Availability service
15.9 Logging, monitoring, and alerting
15.10 Other possible discussion points
16 Design a news feed
16.1 Requirements
16.2 High-level architecture
16.3 Prepare feed in advance
16.4 Validation and content moderation
16.5 Logging, monitoring, and alerting
16.6 Other possible discussion points
17 Design a dashboard of top 10 products on Amazon by sales volume
17.1 Requirements
17.2 Initial thoughts
17.3 Initial high-level architecture
17.4 Aggregation service
17.5 Batch pipeline
17.6 Streaming pipeline
17.7 Approximation
17.8 Dashboard with Lambda architecture
17.9 Kappa architecture approach
17.10 Logging, monitoring, and alerting
17.11 Other possible discussion points
17.12 References
A Monoliths vs. microservices
A.1 Disadvantages of monoliths
A.2 Advantages of monoliths
A.3 Advantages of services
A.5 References
B OAuth 2.0 authorization and OpenID Connect authentication
B.1 Authorization vs. authentication
B.2 Prelude: Simple login, cookie-based authentication
B.3 Single sign-on (SSO)
B.4 Disadvantages of simple login
B.5 OAuth 2.0 flow
B.6 Other OAuth 2.0 flows
B.7 OpenID Connect authentication
C C4 Model
D Two-phase commit (2PC)