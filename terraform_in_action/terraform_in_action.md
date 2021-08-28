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

構成管理ツールとプロビジョニングツールの違いは、根底にある哲学の違い。
構成管理ツールはミュータブルインフラで、プロビジョニングツールはイミュータブルインフラ。

ミュータブルインフラは、今あるサーバーにアップデートをかけていく。
一方、イミュータブルインフラは今あるサーバを気にせずインフラを使いすてで扱える。

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


