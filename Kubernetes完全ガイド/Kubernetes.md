# 3章 Kubernetes環境の選択肢

## 3.1 Kubernetes環境の種別
3種類があり得る。

ローカルkubernetes
Kubernetes構築ツール
マネージドKubernetes

## 3.2 ローカルKubernetes

### 3.2.1 Minikube

ハイパーバイザが必用。windowsだとVirtualBox等。

homebrewを使用したMinikube環境構築が始まる。。
windowsユーザはしれっと無視される。

以下独自で。
https://github.com/kubernetes/minikube/releases
に行って、installerを取得。

なんか動いたけど、どうやってVirtualBox認識したんだ？？


### 3.2.2 Docker for Mac

Macでないので無視

## 3.3 Kubernetes構築ツール

できなさそうなのでとばす
オンプレミスでのKubernetes環境構築がいろいろ書いてある。

## 3.4 パブリッククラウド上のマネージドKubernetesサービス

### 3.4.1 GKE（Google Kubernetes Engine）

gcloudは普通にググってインストーラからインストール。
gcloud components install kubectl
でkubectlはインストールできる。

マスターのバージョンは 1.11.2-gke.15 にした。
gcloud container clusters create k8s ^
--cluster-version 1.11.2-gke.15 ^
--zone asia-northeast1-a ^
--num-nodes 3

kubectl create --save-config clusterrolebinding iam-cluster-admin-binding ^
--clusterrole=cluster-admin ^
--user=ymym1990ymym@gmail.com

# 4章 APIリソースとkubectl

## 4.2 Kubernetesの基礎

Kubernetes MasterとKubernetes Nodeの2種類のノードから、Kubernetesは成り立っている。
Masterが持つAPIにリクエストを送ることでいろいろできる。

## 4.3 Kubernetesとリソース

大きく分けて5種のリソースがある。(リソース？？)

### 4.3.1 Workloadsリソース

クラスタ上でコンテナを起動させるためのリソース。workloadリソースの中にも8種類の分類があるらしい。

### 4.3.2 Discovery&LBリソース

コンテナのサービスディスカバリ、クラスタ外部からのアクセス可能なエンドポイントの提供などをするリソース。

### 4.3.3 Config&Storageリソース

永続ボリュームを提供するリソース。

### 4.3.4 Clusterリソース

### 4.3.5 Metadataリソース

## 4.4 Namespaceによる仮想的なクラスタの分離

ユーザ毎（一般とadminみたいな）にアクセスできるクラスタを制御することが可能らしい。

## 4.5 CLIツールkubectl

### 4.5.1 認証情報とContext（config）

認証情報の設定ができる。

kubectl config set-cluster prd-cluster --server=https://localhost:6443

kubectl config set-credentials admin-user ^
  --client-certificate=./sample.crt ^
  --client-key=./sample.key ^
  --embed-certs=true

crtファイル等作らなければならないのでいったん飛ばす


### 4.5.2 kubectx/kubensによる切り替え

kubectx/kubensを用いればContext、Namespaceの切り替えが素早くできる。

### 4.5.3 マニフェストとリソースの作成/削除/更新（create/delete/apply）

ポッドの作成、削除、更新コマンドを紹介。

### 4.5.4 リソース作成においてもapplyを使うべき理由

リソースの作成においても、createコマンドではなく、applyコマンドを使用したほうがよい。
差分が見えやすいためらしい。

### 4.5.5 マニフェストファイルの設計

1つのファイルに複数の定義できたり、複数のマニフェストファイルの定義を一気に適用できたりする。

### 4.5.6 アノテーションとラベル


### 4.5.7 Pruneによるリソースの削除(--prune)

pruneをつけることによって、差分を見て、マニフェストファイルがなくなってたらpod削除してくれる。

### 4.5.8 エディタによる編集（edit)

エディタで変更作業を行える

### 4.5.9 リソースの一部情報の更新（set）

マニフェストファイルを変更せずとも、setでリソースの変更を行えるが、手元のマニフェストファイルとの齟齬が生じるためあまり使わないほうがいい。


### 4.5.10 リソースの情報取得（get）

いろいろな情報を得られる

### 4.5.11 リソースの詳細情報取得（describe）

いろいろな情報を得られる

### 4.5.12 実際のリソースの使用量の確認（top）

いろいろな情報を得られる

### 4.5.13 Pod上でのコマンドの実行（exec）

コンテナに対してSSHしたみたいにできる

### 4.5.14 Podのログ確認（logs）

コンテナで排出したログをみれる。podごとにみれる

### 4.5.15 Sternによる高度なログ確認

全コンテナのログを一気に見れる

### 4.5.16 コンテナとローカルマシンの間でのファイルのコピー（cp）

双方向でコピー可能

### 4.5.17 ローカルマシンからPodへのポートフォワーディング（port-forward）

ポートフォワーディングができる

### 4.5.18 Kubernetesの補完機能（completion)

これwindowsでも使えるんか？？

### 4.5.19 Kubernetesにおけるデバッグ（completion)

-vオプションでいろいろできる

### 4.5.20 kubectlのその他のTIPS

何度も打つコマンドはalias作成する

現在操作対象のクラスタ、Namespaceを明示できるkube-ps1なるものがあるらしい

Podが起動しない場合のデバッグ方法が書かれている

# 5章 workloadsリソース

## 5.1 workloadリソースの概要

8種ある。それぞれ親子関係があり、Podが最小単位

## 5.2 Pod

1つ以上のコンテナからできている。同一Pod内のコンテナはIPを共有している。

### 5.2.1 Podのデザインパターン

サイドカーパターン、アンバサダーパターン、アダプタパターンがある。

### 5.2.2 Podの作成

4章でやった気がする

### 5.2.3 2つのコンテナを内包したPodの作成

### 5.2.4 コンテナへのログインとコマンドの実行

### 5.2.5 ENTRYPOINT/CMD と command/args

DockerのENTRYPOINTやCMDをk8sから上かくことが可能

### 5.2.6 Pod名の制限

アンダーバーとか使えない

### 5.2.7 PodのDNS設定とサービスディスカバリ


