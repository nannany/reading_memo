# Part1 Terraform bootcamp

- 第1章はTerraformの基本的な情報を語る。最後にEC2の作成をする
- 第2章はTerraformの状態管理など深く掘り下げていく
- 第3章は変数やforなど
- 第4章は1~3のまとめ

## 1. Getting started with Terraform

- プロビジョニング（terraform）と構成管理(ansible etc)は本質的に異なるが、プロビジョニングのおかげで構成管理が不要になったところもある
- Terraformが勝者である理由を説明していく

### 1.1 What makes Terraform so great?

- Terraformを特徴付けている6つの特徴
    - プロビジョニングツール: インフラをデプロイできる
    - 使いやすさ
    - オープンソース
    - 宣言的
    - クラウドベンダーに依存しない
    - 表現力と拡張性

#### 1.1.1 Provisioning tool

構成管理ツールとプロビジョニングツールの違いは、根底にある哲学の違い。 構成管理ツールはミュータブルインフラで、プロビジョニングツールはイミュータブルインフラ。

ミュータブルインフラは、今あるサーバーにアップデートをかけていく。 一方、イミュータブルインフラは今あるサーバを気にせずインフラを使いすてで扱える。

まとめると、これらの違いは再利用と使い捨ての対立になる。

#### 1.1.2 Easy to use

HashiCorp Configuration Language(HCL)というわかりやすい言語で記述される。

HCLとJSONは1:1で変換できるため、外部のシステムとの連携もできる。

#### 1.1.3 Free and source software

#### 1.1.4 Declarative programming

１つ１つの手順ではなくて、最終的なあるべき姿を記述することで動くプログラミング手法（宣言的プログラミング）に則っている。

#### 1.1.5 Cloud-agnostic

#### 1.1.6 Richly expressive and highly extensible

Cloud Formationに比べて表現力が高いっぽい

### 1.2 "Hello Terraform"

#### 1.2.1 Writing the Terraform configuration

```terraform
resource "aws_instance" "helloworld" {
  ami = "ami-09dd2e08d601bff67"
  instance_type = "t2.micro"
  tags = {
    Name = "HelloWorld"
  }
}
```

`resource`で、何らかのリソースを生成しますよと宣言する。
`aws_instance`で作成するリソースの種類を、`helloworld`でそのリソースに名前をつけている。

括弧の中で、リソースに渡す引数を宣言している。

#### 1.2.2 Configureing the AWS provider

providerを指定

```terraform
provider "aws" {
  region = "ap-northeast-1"
}
resource "aws_instance" "helloworld" {
  ami = "ami-09dd2e08d601bff67"
  instance_type = "t2.micro"
  tags = {
    Name = "HelloWorld"
  }
}
```

#### 1.2.3 Initializing Terraform

`terraform init`

これで色々なものをダウンロードしてるっぽい

そのディレクトリに`.terraform`ディレクトリと`.terraform.lock.hcl`ファイルができる

#### 1.2.4 Deploying the EC2 instance

`terraform apply`

これが成功するとインフラ出来上がる。 その前にどのような変更が走るのか`terraform plan`で確認できる

#### 1.2.5 Destroying the EC2 instance

`terraform destroy`で作成したリソース消える。

`terraform show`で定義したものが現状どうなっているか確認できる

### 1.3 Brave new "Hello Terraform"

data source なる仕組みを利用して、動的にargumentを変えることができる。

例えば、そのとき最新のaws_amiを持ってくるみたいな。

#### 1.3.1 Modifying the Terraform configuration

```terraform
provider "aws" {
  region = "ap-northeast-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name = "name"
    values = [
      "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  owners = [
    "099720109477"]
}

resource "aws_instance" "helloworld" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  tags = {
    Name = "HelloWorld"
  }
}
```

`data`でデータソースを定義できる。 データソースはリソース定義の中で利用するものと考えて良さそう。

`aws_ami`でデータソースの種別を特定し、`ubuntu`で識別するための名前をつけている。

#### 1.3.2 Applying changes

#### 1.3.3 Destroying the infrastructure

### 1.4 Fireside chat

### Summary

- Terraformは、宣言型のIaCプロビジョニングツールです。パブリッククラウドやプライベートクラウドにリソースを展開することができます。
- Terraformは、(1)プロビジョニングツール、(2)使いやすい、(3)無償・オープンソース、(4)宣言型、(5)クラウドにとらわれない、(6)表現力・拡張性に優れています。
- Terraformの主要な要素は、リソース、データソース、プロバイダです。
- コードブロックを連鎖させることで、動的なデプロイを行うことができます。
- Terraformプロジェクトをデプロイするには、まず設定コードを書き、次にプロバイダーやその他の入力変数を設定し、Terraformを初期化し、最後に変更を適用する必要があります。後始末は destroy コマンドで行います。

## 2. Life cycle of a Terraform resource

ローカルオンリーリソースでTerraformのリソースのライフサイクルを学んでいく。

### 2.1 Process overview

#### 2.1.1 Life cycle function hook

`resource`はCRUD全てhookできる。`data`はRのみ。

### 2.2 Declaring a local file resource

```terraform
terraform {
  required_version = ">= 0.15"
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "literature" {
  filename = "art_of_war.txt"
  content = <<-EOT
      Sun Tzu said: The art of war is of vital importance to the State.
 
      It is a matter of life and death, a road either to safety or to 
      ruin. Hence it is a subject of inquiry which can on no account be
      neglected.
    EOT
}
```

`terraform`周りはterraformのバージョンとか、どこにファイルを保存するかとか決めるとこ。

### 2.3 Initializing the workspace

`terraform init`は冪等性あり。

`terraform init`コマンド実行すると、下記みたいなファイルが出来上がる。

```
.
├── .terraform
│   └── providers
│       └── registry.terraform.io
│           └── hashicorp
│               └── local
│                   └── 2.0.0
│                       └── darwin_amd64
│                           └── terraform-provider-local_v2.0.0_x5
├── .terraform.lock.hcl
└──  main.tf
 
7 directories, 3 files
```

### 2.4 Generating an execution plan

`terrafomr plan`を事前にやっておくこと推奨。

エラー出る場合は、`TF_LOG=trace`を有効にしてログをいっぱい出すてもある。

遅い時は`parallelism=30`みたいに並列度をあげれば良いかも。
https://qiita.com/minamijoyo/items/7945ec527270ee2af5c3

![terraform planのながれ](スクリーンショット%202021-08-29%2011.38.55.png)

#### 2.4.1 Inspecting the plan

```shell
terraform plan -out plan.out
terraform show -json plan.out > plan.json
```

これでplan内容をjsonにだせる。

### 2.5 Creating the local file resource

こんな感じで、plan.outで出した通りにapplyすることもできる。
`terraform plan -out plan.out && terraform apply "plan.out"`

planで事前にやることを必ず確認すること。terraformは不注意に扱うとインフラをぶっ壊すので。

`tfstate`ファイルは更新したり消したりしないこと。

### 2.6 Performing No-Op

この時は、`terraform plan`でLocal providerのreadを呼んでいる。

main.tfとterraform.tfstateに差分がなければ何もしない。

### 2.7 Updating the local file resource

`auto-appvrove`でyesとうたなくても良い

#### 2.7.1 Detecting configuration drift

作成されたリソースがterraformコマンド以外で直接変更された場合は、planで検知できる。 Local providerの場合、変更を検知したら、createする動きになる。他のproviderはどうなんだろう？

#### 2.7.2 Terraform refresh

`terrafomr refresh`を利用すれば現状のインフラ状態と、stateファイルを一致させることができる。

作者的にはほぼ使わない機能らしい。

### 2.8 Deleting the local file resource

### 2.9 Fireside chat

Terraformはシンプルな状態管理エンジン。

### Summary

- Terraformのローカルプロバイダーは、あなたのマシン上にテキストファイルを作成・管理することができます。これは通常、「実際の」インフラを接着するために使用されますが、それ自体が教材としても役立ちます。
- リソースの作成は、実行計画に基づいた一定の順序で行われます。この順序は、暗黙の依存関係に基づいて自動的に計算されます。
- 管理されている各リソースには、ライフサイクル機能のフックが関連付けられています。Create()、Read()、Update()、Delete()です。Terraformはこれらの関数フックを通常の操作の一部として呼び出します。
- Terraformの設定コードを変更してterraform applyを実行すると、既存のマネージドリソースが更新されます。また、terraform
  refreshを使用すると、現在デプロイされている内容に基づいて状態ファイルを更新することができます。
- Terraformは計画時に状態ファイルを読み込んで、適用時にどのようなアクションを取るかを決定します。状態ファイルを失わないようにすることが重要で、そうするとTerraformは管理しているすべてのリソースを把握できなくなります。

## 3. Functional programming

関数型プログラミングの特徴

- 副作用ない
- 高階関数
- immutable

この章では、Terraform言語を構成する関数、式、テンプレート、その他のダイナミクス機能について深く掘り下げていく。

### 3.1 Fun with Mad Libs

Mad Libsなる言葉遊びゲームを作る

#### 3.1.1 Input variables

`variable`で変数を宣言できる。 だいたい言葉通りの意味。

- default
- description
- type
- validation

#### 3.1.2 Assigning values with a variable definition file

tfvars拡張子ファイルに変数とその値を格納。

#### 3.1.3 Validating variables

バリデーション

#### 3.1.4 Shuffling lists

`uuid()`と`timestamp()`のみ不純な関数なので、いずれこれらは非推奨になるかも。

#### 3.1.5 Functions

terraformではユーザー定義関数がサポートされていない。 拡張しようと思ったらproviderを書く必要がある。

ここでは`templatefile`関数を使っていく。

#### 3.1.6 Output values

`output`エレメントを使う。

#### 3.1.7 Templates

#### 3.1.8 Printing output

### 3.2 Generating many Mad Libs stories

#### 3.2.1 for expressions

for文の使い方について

#### 3.2.2 Local values

ローカル変数の定義について

#### 3.2.3 Implicit dependencies

`terraform graph`でみれる依存関係について

- 循環依存は許されない
- 何にも依存していないものは最初に作られ、最後に削除される
- 同じ依存レベルの場合はどの順序になるかはコントロールできない

小規模プロジェクトでもない限り、依存グラフはすぐに大きくなってしまう。 その時には基本グラフを見ても何も得られなくなる。

#### 3.2.4 count parameter

#### 3.2.5 Conditional expressions

三項演算子。

`[][0]`は常にエラーを返す。

#### 3.2.6 More templates

#### 3.2.7 Local file

今回はCLI出力ではなく、ファイルに出していく。

```terraform
resource "local_file" "mad_libs" {
  count = var.num_files
  filename = "madlibs/madlibs-${count.index}.txt"
  content = templatefile(element(local.templates, count.index),
  {
    nouns = random_shuffle.random_nouns[count.index].result
    adjectives = random_shuffle.random_adjectives[count.index].result
    verbs = random_shuffle.random_verbs[count.index].result
    adverbs = random_shuffle.random_adverbs[count.index].result
    numbers = random_shuffle.random_numbers[count.index].result
  })
}
```

`element`関数でmoduloを扱える。

#### 3.2.8 Zipping files

`archive_file`データソースでファイルの圧縮をできる。

`depends_on`でデータソース、リソースの実行順序を操作できる。

#### 3.2.9 Applying changes

データソースで作ったzipファイルは`terraform destroy`しても消えない。

### 3.3 Fireside chat

Terraformで使える表現が載っている。

### Summary

- 入力変数はTerraformの設定をパラメータ化します。ローカル値は、式の結果を保存します。出力値は、ユーザーや他のモジュールにデータを渡します。
- for式では、ある複雑な型を別の型に変換することができます。また、他のfor式と組み合わせて高次の関数を作ることもできます。
- ランダム性は制限されなければなりません。uuid()やtimestamp()などのレガシー関数は、Terraformに非収束状態による微妙なバグをもたらすため、使用しないでください。
- ArchiveプロバイダでZipファイルを作成します。データソースを適切なタイミングで実行するために、明示的な依存関係を指定する必要があるかもしれません。
- templatefile() は、補間変数で使用されるのと同じ構文でテンプレートファイルを作成できます。この関数に渡された変数のみがテンプレート化の対象となります。
- count メタ引数は、リソースの複数のインスタンスを動的に提供することができます。countで生成されたリソースのインスタンスにアクセスするには、ブラケット表記の[]を使用します。

## 4 Deploying a multi-tiered web application in AWS

AWSで３層アプリケーションを作成していく。

### 4.1 Architecture

![アーキテクチャ](スクリーンショット%202021-08-29%2018.20.30.png)

作者は小さいコンポーネントで実装を分けるべきとしており、ここでは
- networking
- database
- autoscaling
の観点で分けることを推奨している。
  
terraformではこのような分割を`modules`を用いて行う。

### 4.2 Terraform modules

```
モジュールは、関連するリソースをグループ化して再利用可能なコンポーネントを作成するための、自己完結型のコードパッケージです。モジュールがどのように動作するかを知らなくても、入力と出力を設定する方法を知っていれば、使用することができます。モジュールは、ソフトウェアの抽象化とコードの再利用を促進する便利なツールです。
```

#### 4.2.1 Module syntax

moduleはレゴブロックの構成要素みたいなもの。

`module`は`resource`宣言に似ている。

#### 4.2.2 What is the root module?

rootモジュールがあるディレクトリで`terraform apply`する。

子モジュールがさらに子モジュールをもったり、ネストしていくこともある。

#### 4.2.3 Standard module structure

[Standard module structure](https://www.terraform.io/docs/language/modules/develop/index.html#standard-module-structure)

moduleごとに下記を持つべきとのこと。
- `main.tf`: エントリーポイント
- `outputs.tf`: アウトプット
- `variables.tf`: インプット

![module構成](スクリーンショット%202021-08-29%2018.39.45.png)

### 4.3 Root module

root moduleではnamespace,ssh_keypair,regionをインプットとして受け取る。

root moduleはこれらの要素からなる。

- variables.tf:Input variables
- terraform.tfvars:Variables definition file
- providers.tf:Provider declarations
- main.tf:Entry point for Terraform
- outputs.tf:Output values
- versions.tf:Provider version locking

#### 4.3.1 Code

上記６ファイルの説明の段落。


[variables.tf](4sho/variables.tf)  
受け取るパラメータの定義。具体的な値を`terraform.tfvars`に記載。


[terraform.tfvars](4sho/terraform.tfvars)  

[provider.tf](4sho/provider.tf)

[main.tf](4sho/main.tf)

[outputs.tf](4sho/outputs.tf)

[versions.tf](4sho/versions.tf)
バージョンを固定する。
本来は`terraform init`した後に作る。

### 4.4 Networking module

`namespace`をインプットに、`vpc`,`sg`の情報を出力する。
その過程の副作用として、リソースができると考えれば良い。

[variables.tf](4sho/modules/networking/variables.tf)

[main.tf](4sho/modules/networking/main.tf)

[outputs.tf](4sho/modules/networking/outputs.tf)

### 4.5 Database module

namespace,vpc,sgを受け取る。db_configを吐き出す。

#### 4.5.1 Passing data from the networking module

ネットワークモジュールからルートモジュールに「バブリング」して、データベースモジュールに「トリクルダウン」します。

循環的に依存しなければ、2つのモジュールは互いに依存できる。
ただ、相互依存はデザインとしていけてないのでしないこと。

anyタイプは極力使わないようにすること。モジュール間の値の受け渡しくらい。

[variables.tf](4sho/modules/database/variables.tf)

#### 4.5.2 Generating a random password

[main.tf](4sho/modules/database/main.tf)

最小限の情報をoutputする。
[outputs.tf](4sho/modules/database/outputs.tf)

terraform apply後にデータベースのパスワードの値は知りたいので、rootモジュールのoutputsに書くこと。

### 4.6 Autoscaling module

ここが一番複雑

#### 4.6.1 Trickling down data

まず、autoscalingモジュールに情報を落とすように、rootモジュールを書き換える必要がある。

[variables.tf](4sho/modules/autoscaling/variables.tf)

#### 4.6.2 Templating a cloudinit_config

autoscaling moduleとして下記を用意する。
[main.tf](4sho/modules/autoscaling/main.tf)

`aws_autoscaling_group`で利用する設定を下記のように作る。
[cloud_config.yaml](4sho/modules/autoscaling/cloud_config.yaml)

DNS名を出すように下記のように`outputs.tf`をかく。
[outputs.tf](4sho/modules/autoscaling/outputs.tf)

### 4.7 Deploying the web application

`outputs.tf`のデータベースパスワードの方は、`sensitive = true`付けないといけないっぽい

なんか現状502になる、が、一旦ここは諦めて先に進む。多分アプリの設定が悪い。

### 4.8 Fireside chat

### Summary

* AWSでの多層ウェブアプリケーションなどの複雑なプロジェクトも、Terraformモジュールの助けを借りれば簡単に設計・展開することができます。
* ルートモジュールは、プロジェクトのメインエントリーポイントです。変数定義ファイル（terraform.tfvars）を使用して、ルートレベルで変数を設定します。これらの変数は、必要に応じて子モジュールに組み込まれていきます。
* ネストしたモジュールは、コードを子モジュールにまとめます。子モジュールは、他の子モジュールの中に無制限に入れ子にすることができます。一般的には、モジュールの階層が3～4階層以上になると、理解しにくくなるので避けたほうがいいでしょう。
* 多くの人がTerraform Registryという公開サイトでモジュールを公開しています。このようなオープンソースのモジュールを使えば、自分で同等のコードを書く必要はなく、モジュールのインターフェイスの使い方を覚えるだけで、大幅に時間を短縮することができます。
* モジュール間のデータの受け渡しは、バブルアップとトリクルダウンという手法で行われます。モジュール間でのデータの受け渡しは、バブルアップやトリクルダウンといった手法で行われます。この手法では多くの定型文が必要となるため、モジュール間でのデータの受け渡しが最小限となるようにコードを最適化することをお勧めします。

# Part2 Terraform in the wild

- 5章はAzureを利用したサーバーレスWebアプリ。
- 6章はTerraformのプレイナイスルール？の紹介。
- 7章はk8sとGCP。CI/CDパイプラインを作成する
- 8章は3つのクラウドを1つのシナリオにまとめたもの。

## 5 Serverless made easy

サーバーレスの定義は定まっていないけど、下記二点は合意できる。

- 使った分だけ払う料金体系
- 最小限のオペコスト

この章ではAzure Functionsを使う。

### 5.1 The “two-penny website”

### 5.2 Architecture and planning

![](スクリーンショット%202021-09-12%2015.05.20.png)

#### 5.2.1 Sorting by group and then by size

筆者曰く、1つのTerraformファイルで2〜300行に納めること推奨らしい。

1つのファイルに打ち込む場合は、上から順に依存関係の少ないものを記述していくことが推奨される。
または、関連するリソースごとにまとめることも推奨。
ここでは後者の方法を取る。

### 5.3 Writing the code

TBW

# 6 Terraform with friend

コードを共有することは簡単であるが、状態を共有することは難しい。
ステートファイルをVCSにチェックインすることはセキュリティ、レースコンディションの面から推奨されない。

レースコンディション＝競合状態
一人がterraform applyをして、一人がterraform destroyをする、みたいなことが同時に起こるとよくない。

S3リモートバックエンドモジュールなるものを使ってなんとかするらしい。


## 6.1 Standard and enhanced backends

バックエンドでは次のようなことができるらしい。

* ロッキングによるステートファイルへのアクセスの同期化
* 機密情報を安全に保存
* ステートファイルのすべてのリビジョンの履歴を保持
* CLI操作のオーバーライド

## 6.2 Developing an S3 backend module

### 6.2.1 Architecture

S3バックエンドは4つの構成要素でできてる。
- ロックするためのDynamoDB
- S3バケットと暗号化のためのKMS
- IAM
- housekeeping?

### 6.2.2 Flat modules

nestするモジュールに対抗する概念。
メリットとしては、こちらの方がボイラープレートが少ない。

一般に、中規模のコードベースであればflatよりで、大規模になるにつれてnestしたほうがいいようになる。

flatの方がglobal変数が多用されるが、これは規模が大きくなるとどこで参照されているかわかりづらくなる。

### 6.2.3 Writing the code

