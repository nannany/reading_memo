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

マスターのバージョンは 1.11.2-gke.18 にした。
gcloud container clusters create k8s ^
--cluster-version 1.12.7-gke.10 ^
--zone asia-northeast1-a ^
--num-nodes 3

gcloud container clusters get-credentials k8s --zone asia-northeast1-a

kubectl create --save-config clusterrolebinding iam-cluster-admin-binding ^
--clusterrole=cluster-admin ^
--user=ymym1990ymym@gmail.com

# 4章 APIリソースとkubectl

## 4.2 Kubernetesの基礎

Kubernetes MasterとKubernetes Nodeの2種類のノードから、Kubernetesは成り立っている。
masterが持つapiにリクエストを送ることでいろいろできる。

## 4.3 kubernetesとリソース

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

### 5.2.8 静的な名前解決の設定

## 5.3 ReplicaSet/ReplicationController

### 5.3.2 Podの停止とセルフヒーリング
障害が発生しても、指定したpod数を満たすようにコンテナ起動してくれる

### 5.3.4 ReplicaSetのスケーリング
基本的にはapplyでのスケーリングがおすすめ。インフラasコードを実剣するため。

## 5.4 Deployment
Deploymentの中にReplicaSetがあり、その中にPodがあるイメージ

### 5.4.3 変更のrollback
rolloutを使う機会は少ない。applyを使って戻すことのほうが多い

### 5.4.9 マニフェストファイルを書かずにDeploymentを作成する
マニフェストファイルを書かずにDeploymentを作成することもできるが、できるだけ作成してやったほうがいい

## 5.5 DaemonSet
ReplicaSetの特殊形。
1ノードに1Podずつ配置される。
ログ収集など必ず各ノードで動作させたいプロセスのために使われることが多い。

### 5.5.2 DaemonSetのアップデート戦略
基本はRollingupdate

## 5.6 StatefulSet
データベースなどステートフルなワークロードに対応するリソース。
デフォルトでは順次起動する

### 5.6.4 StatefulSetのアップデート戦略


## 5.7 Job
バッチ処理的なものに向いているリソース。

## 5.8 CronJob
CronJobとJobの関係は、DeploymentとReplicaSetの関係に似ている。
CronJobがJobを管理する。

# 6章 Discovery&LBリソース

コンテナのエンドポイント提供や、コンテナのディスカバリに利用される。
ServiceはL4ロードバランシングを行い、IngressはL7ロードバランシングをおこなう。

Serviceの利用で得られるメリットは
* Pod宛のトラフィックのロードバランシング
* サービスディスカバリとクラスタ内DNS

### 6.2.1 Pod宛トラフィックのロードバランシング

### 6.2.2 クラスタ内DNSとサービスディスカバリ
immutableに保つために、IPではなく、Service名での名前解決を試みるべし。

## 6.3 ClusterIP Service

### 6.3.2 ClusterIP仮想IPの静的な指定

## 6.4 ExternalIP Service

## 6.5 NodePort Service
ExternalIP Serviceでは指定したノードからの転送を行っていたが、全ノードでうけたトラフィックがコンテナに転送される。

### 6.5.3 ノード間通信の排除
externalTrafficPolicyがLocalにすると、特定のノードのPodにトラフィックを送ることができる。

## 6.6 LoadBalancer Service

### 6.6.5 GKEやクラウドプロバイダでの注意点
Serviceを作成したままクラスタを削除すると、GCLBの課金は残ってしまうので注意。


## 6.7 Headless Service

## 6.8 ExternalName Service
これを用いることにより、外部サービスとの連携を疎に保つことができる。

## 6.9 Non-Selector Service
正直よくわからん。。

## 6.10 Ingress
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=sample.example.com"
k create secret tls --save-config tls-sample --key tls.key --cert tls.crt

# 7章 config&Storageリソース
設定ファイル、パスワード等機密情報のインジェクト、永続化ボリュームの提供のために使われる。

## 7.2 環境変数の利用
コンテナに対する設定の渡し方は、環境変数、ファイルが置かれた領域のマウントで行うことが多い。

## 7.3 Secret
ユーザ名、パスワード等の機密情報を保持するリソース
スキーマレス？？

### 7.3.5 Secretの利用
Secretの情報を利用する方法としては、環境変数として渡す方式と、Volumeとしてマウントする方式の2種類がある。
環境変数として渡した場合には、動的に変更することはできない。

### 7.3.6 kubesecの利用
Google Cloud KMS等で暗号鍵を作成して、kubesecを利用してSecretの暗号化を行う。
Secretのデータ構造を保ったまま、値だけ暗号化してくれるので可読性が高い。

### 7.3.7 SecretとConfigMapの使い分け

## 7.4 ConfigMap

### 7.4.1 ConfigMapの作成
* kubectlでファイルから値を参照して作成
* kubectlで直接値を渡して作成
* マニフェストから作成

### 7.4.2 ConfigMapの利用
* 環境変数として渡す
* Volumeとしてマウント

環境変数として渡した場合には、動的に変更することはできない。

## 7.5 PersistentVolumeClaim

### 7.5.1 Volume,PersistentVolume,PersistentVolumeの違い

* Volume：NFS、ホスト等のあらかじめ用意された利用可能なボリュームを指す。ここではボリュームの削除、新規作成等はできない
* PersistentVolume：外部の永続ボリュームを提供するシステムと連携し、新規ボリューム作成、ボリューム削除を行うことができる
* PersistentVolumeClaim：PersistentVolumeリソースをアサインするためのリソース

## 7.6 Volume

### 7.6.1 emptyDir
Pod用の一時的なディスク領域。PodがTerminateされると削除される。

### 7.6.2 hostPath
k8sNode上の領域をコンテナにマッピングする。
セキュリティ的に、信頼できないコンテナが乗る場合は使用すべきでない。

### 7.6.3 downwardAPI

### 7.6.4 projected
Secret,ConfigMap,downwardAPI,serviceAccountTokenのボリュームマウントを一か所に集約するプラグイン。

## 7.7 PersistentVolume（PV）

### 7.7.1 PersistentVolumeの種類

### 7.7.2 PersistentVolumeの作成
ボリュームの種類についてラベルを付けておくことが望ましい。
アクセスモードとしては、

* ReadWriteOnce:単一ノードからRW可能
* ReadOnlyMany:複数ノードからR可能
* ReadWriteMany:複数ノードからRW可能
がある。

ReclaimPolicy（PersistentVolumeを使い終わった後の処理）も以下3つから決められる。

* Delete：削除する
* Retain：保持する。ほかのpvcによって再度マウントされることはない。
* Recycle：データ削除し、pvcによって再度マウントされる。（推奨されてない）

## 7.8 PersistentClaim（PVC）

### 7.8.1 PersistentVolumeClaimの設定
PersistentVolumeClaimでの要求容量がPersistentVolumeの容量より小さければ、割り当てが行われてしまうことに注意。

### 7.8.2 PersistentVolumeClaimの作成

### 7.8.3 Podからの利用

### 7.8.4 Dynamic Provisioning
pvcが発行されたタイミングでpvが作成されるので容量の無駄が生じない。

### 7.8.5 PersistentVolumeClaimResizeによるボリュームの拡張
alphaクラスタを作成して確認。

gcloud beta container clusters create k8s-alpha ^
--zone asia-northeast1-a ^
--cluster-version 1.11.2-gke.18 ^
--enable-kubernetes-alpha
↑のコマンドで謎エラーが出てうまくアルファクラスタを作れない。

"ERROR: (gcloud.beta.container.clusters.create) ResponseError: code=400, message=Auto_upgrade and auto_repair are not supported for clusters with enable_kubernetes_alpha = true"

resizeは大きくすることのみ可能。

### 7.8.6 StatefulSetでのPersistentVolumeClaim（volumeClaimTemplate)
volumeChaimTemlateを利用すると、別途PersistentVolumeClaimを定義する必要がなくなる

## 7.9 volumeMountsで利用可能なオプション

### 7.9.1 ReadOnlyマウント
ReadOnlyでマウントすれば、書き込みはできない。

### 7.9.2 subPath

# 8章 ClusterリソースとMetadataリソース

## 8.1 ClusterリソースとMetadataリソースの概要
Clusterリソースはセキュリティまわりの設定やクォータ設定などクラスタの挙動を制御するためのリソース。
Metadataリソースはクラスタ上にコンテナを起動させるために利用するリソース。

## 8.2 Node

## 8.3 Namespace

# 9章 リソース管理とオートスケーリング

## 9.1 リソースの制限
Requestsはリソースの下限を示す。Limitsは上限。
Requestsに示した分のリソースがノードにあれば、スケジューリングは行われる。

### 9.1.1 GPUなどのリソース制限

### 9.1.2 オーバーコミットとリソース不足

## 9.2 ClusterAutoscalerとリソース不足
Pending状態のPodができたときに初めてスケールする。
基本方針として、RequestsとLimitsの差をつけすぎない、Requestsを大きくしすぎない、ようにする。


## 9.3 LimitRangeによるリソース制限
Pod、Container、PersistentVolumeClaimでLimitRange（Metadataのうちの１つ）を設定可能

### 9.3.1 デフォルトで作成されているLimitRange
デフォルトではCPUのdefaultRequestが100mに設定されている。

### 9.3.2 Containerに対するLimitRange

### 9.3.3 Podに対するLimitRange

### 9.3.3 Podに対するLimitRange
クラウド環境ではDynamicprovisioningで簡単にPersistentVolumeを作成することができるが、LimitRangeを作成しておくことで、一定容量以上のボリュームを作成させないようにできる。


## 9.4 QoS Class
Podに設定される。BestEffort,Guaranteed,Burstableの3種があり、自動で設定される。

## 9.5 ResourceQuotaによるNamespaceのリソースクォータ制限
ネームスペースごとに利用可能なリソース数、量の制限を書けることが可能。

### 9.5.1 作成可能なリソース数の制限

### 9.5.2 リソース使用量の制限

## 9.6 HorizontalPodAutoscaler（HPA)
Metadataの一種。
Deployment、ReplicaSetのレプリカ数をCPU負荷等に応じて自動的にスケーリングさせるリソース。
30秒に一回、オートスケーリングするかチェックする。


## 9.7 VerticalPodAutoscaler（VPA)
HPAがスケールアウトであったのに対して、こちらはPodのスケールアップ

## 9.8 まとめ
オートスケーリングの方式には3種類ある。
* Cluster Autoscaler：Podを起動できるノードが存在しない場合に、ノードを新規追加
* HorizontalPodAutoscaler：Podのレプリカ数を負荷に応じて自動的に増減
* VerticalPodAutoscaler：Podに割り当てられているリソースを負荷に応じて自動的に増減


# 10章 ヘルスチェックとコンテナのライフサイクル

## 10.1 ヘルスチェック

### 10.1.1 LivenessProbeとReadinessProbe2種類のヘルスチェック機構
LivenessProbeとReadinessProbeがある。
LivenessProbeはPodが正常に動作しているかを確認する。失敗時にはPodを再起動する。
ReadinessProbeはPodがサービスイン可能な状態になっているかを確認する。失敗時には、そこにトラフィックを流さないようにする。

デフォルトでは、ロードバランサーからノードまでのチェックはICMPチェックなどしかしないので、ちゃんと上記を設定しておく必要がある。


### 10.1.2 3種類のヘルスチェック方式
exec、httpGet、tcpSocketの3種類のヘルスチェック方式がある。
execはコマンドを実行し、終了コードが0か否かで判断。
httpGetはHTTP GETリクエストのステータスコードで判断。
tcpSocketはTCPセッションが確立できるかで判断。

### 10.1.3 ヘルスチェックの間隔

### 10.1.4 ヘルスチェックの作成

### 10.1.5 Liveness Probeの失敗

### 10.1.6 Readines Probeの失敗

## 10.2 コンテナのライフサイクルと再始動（restartPolicy）

### 10.2.1 Always
Podで実行しているコマンドの成功/失敗にかかわらず常に再起動する。

### 10.2.2 OnFailure
失敗した場合には再起動する。

### 10.2.3 Never
成功でも失敗でも再起動しない。

## 10.3 Init Containers
メインコンテナを起動させる前に、別のコンテナを起動させるための処理

## 10.4 起動時と終了時に任意のコマンドを実行する（postStart/preStop）

## 10.5 Podの安全な停止とタイミング

## 10.6 リソースを削除したときの挙動

# 11章 メンテナンスとノードの停止

## 11.1 ノードの停止とPodの停止
ライブマイグレーション機能は存在しないので、メンテナンス等でノードを停止する際には、Podも停止する必要がある。

## 11.2 スケジューリング対象からの除外と復帰（cordon/uncordon）
k8sのノードはSchedulingEnabledとSchedulingDisabledのいずれかのステータスを持っている。
kubectl cordonコマンドで切り替えられる

## 11.3 ノードの排出処理によるノードの退避（drain）
該当ノード上のPodを退避できる。（Deploymentとかの場合）

## 11.4 PodDisruptionBudget（PDB）による安全な退避
PodDisruptionBudgetリソースを使うことで、Podの最小起動数、最大停止数を指定してノード上からのPodの追い出しができる。

# 12章 高度で柔軟なスケジューリング

## 12.1 高度なスケジューリングとAffinity/Anti-Affinity
Affinty：特定の条件に一致するところにスケジューリングすることを意味する。
Anti-Affinity：特定の条件に一致しないところにスケジューリングすることを意味する。

## 12.2 ビルトインノードラベルとラベルの追加
ビルトインノードラベル：ノードにあらかじめ付与されているラベル。

## 12.3 nodeSelector(Simplest Node Affinity)
nodeSelectorを使用することで特定のノードにPodを配置できるが、それほど柔軟に条件指定はできない。

## 12.4 Node Affinity
requiredDuringSchedulingIgnoredDuringExecutionで必須のスケジューリングポリシーを指定
preferredDuringSchedulingIgnoredDuringExecutionで優先的に考慮されるスケジューリングポリシーを指定

## 12.5 matchExpressionsのオペレータとset-based条件
matchExpressionsの定義について

### 12.5.1 In/NotInオペレータ
In:keyラベルの値がvaluesラベルのいずれかに一致する。
NotIn:keyラベルの値がvaluesラベルのいずれにも一致しない。

### 12.5.2 Exists/DoesNotExistsオペレータ
Exists：keyラベルが存在するかどうか。
DoesNotExists：keyラベルが存在しないかどうか。

### 12.5.3 Gt/Ltオペレータ
Gt:keyラベルの値が、valuesラベルで指定された値より大きいかどうか。
Lt:keyラベルの値が、valuesラベルで指定された値より小さいかどうか。

## 12.6 Node Anti Affinity

## 12.7 Inter-Pod Affinity

### 12.7.1 特定のPodと同じノードで必ず起動する 
k8sのスケジューラは基本的にスケジューリング時の配置を制御するのみ。

### 12.7.2 特定のPodと必ず同じゾーン上で起動し、可能な限り同じノード上で起動する

## 12.8 Inter-Pod Anti-Affinity

## 12.9 複数の条件を組み合わせたPodのスケジューリング 

## 12.10 TaintsとTolerations 
Nodeに対して汚れ（Taints）をつけておき、それを許容（Tolerations）できるPodのみスケジューリングできる仕組み。
対象のノードを特定の用途に向けた専用ノードにする場合などに用いる。例えば、プロダクション用ノードにはその他のワークロードを混在させたくないなど。


### 12.10.1 Taintsの付与 
kubectl taint コマンドでノードにTaintsを付与できる。Key=Value:Effect形式で構成される。Key、Valueは任意の値で、Effectは以下3種類の値。

#### PreferNoSchedule
可能な限りスケジューリングを行わない。ここしかないってなったら候補になる。

#### NoSchedule
スケジューリングは行われないが、条件にマッチするノードですでに動いているPodには影響がない。

#### NoExecute
マッチするノード上ではPodを決して動作させない。

### 12.10.2 Tolerationsを指定したPodの起動 

### 12.10.3 NoExecuteの一定時間の許容 
NoExecuteの場合において、条件が一致する場合に、一定時間だけ稼働を許容する設定をすることもできる。

### 12.10.4 複数のTaintとTolerations 
ノードが複数のTaintを持っている場合は、Tolerationsはそれらすべての条件を満たさねば、スケジューリングされない。

## 12.11 PriorityClassによるPodの優先度と退避
Podに優先度をつけて、その値で比較して既存のPodを退避させることができる。
Podに優先度を付与するためには、PriorityClassを作成する必要がある。
Pod側の定義のpriorityClassNameでそのPriorityClassを指定してやる。

Inter-Pod Affinityを設定してあるPodを追い出さないために、Inter-Pod Affinityに設定しているPodは優先度を高くしておく。

## 12.12 その他のスケジューリング
独自実装したスケジューラプログラムを使用することも可能。

# 13章 セキュリティ

## 13.1 ServiceAccount
