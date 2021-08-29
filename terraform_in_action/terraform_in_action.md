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

作成されたリソースがterraformコマンド以外で直接変更された場合は、planで検知できる。
Local providerの場合、変更を検知したら、createする動きになる。他のproviderはどうなんだろう？


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
- Terraformの設定コードを変更してterraform applyを実行すると、既存のマネージドリソースが更新されます。また、terraform refreshを使用すると、現在デプロイされている内容に基づいて状態ファイルを更新することができます。
- Terraformは計画時に状態ファイルを読み込んで、適用時にどのようなアクションを取るかを決定します。状態ファイルを失わないようにすることが重要で、そうするとTerraformは管理しているすべてのリソースを把握できなくなります。