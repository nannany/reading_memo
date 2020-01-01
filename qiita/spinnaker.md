spinnakerでそもそも何ができるのか

動かして見る系ある？

どこまでやるか

とりあえず使ってみる
https://www.spinnaker.io/setup/install/
## Halyardをインストールする

Halyardって何をしてくれるやつ？

Halyardなくてもできるらしいが、おすすめできないらしい

[ ここ ](https://www.spinnaker.io/setup/install/halyard/#install-halyard-on-docker)に従ってインストール

Ubuntuにインストール
```shell script
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh

sudo bash InstallHalyard.sh
```

------

homeに .hal ディレクトリを作成
```shell script
mkdir ~/.hal
```

docker コマンド実行
```shell script
docker run -p 8084:8084 -p 9000:9000 \
    --name halyard --rm \
    -v ~/.hal:/home/spinnaker/.hal \
    -it \
    gcr.io/spinnaker-marketplace/halyard:stable
```

コンテナの中に
```shell script
docker exec -it halyard bash
```

-----

## クラウドプロバイダを選択する

### AWS

Azureでうまく行かなかったので、AWSでやってく
https://www.spinnaker.io/setup/install/providers/kubernetes-v2/aws-eks/

```shell script
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

`aws configure` 等でAWSの設定はできている前提
下記、限られたregionでしか成功しない。下記はoregonで実行
↓
ap-northeast-1, us-west-2
双方で失敗した
unsupported Kubernetes version (Service: AmazonEKS; Status Code:400

https://github.com/spinnaker/spinnaker.github.io/issues/1518
に従って、versionを1.10から1.14にしてみる


```shell script
curl -O https://d3079gxvs8ayeg.cloudfront.net/templates/managing.yaml
aws cloudformation deploy --stack-name spinnaker-managing-infrastructure-setup --template-file managing.yaml \
--parameter-overrides UseAccessKeyForAuthentication=false EksClusterName=spinnaker-cluster --capabilities CAPABILITY_NAMED_IAM
```

上のやつだとうまく行かない。。。
↓
1.14だとap-northeast-1でもおｋ
なのだが、その後のSpinnakerがのっかるノードを作成するときに、対応するamiがないと言われるのでus-west-2にしとく

```shell script
VPC_ID=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`VpcId`].OutputValue' --output text)
CONTROL_PLANE_SG=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`SecurityGroups`].OutputValue' --output text)
AUTH_ARN=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`AuthArn`].OutputValue' --output text)
SUBNETS=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`SubnetIds`].OutputValue' --output text)
MANAGING_ACCOUNT_ID=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`ManagingAccountId`].OutputValue' --output text)
EKS_CLUSTER_ENDPOINT=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`EksClusterEndpoint`].OutputValue' --output text)
EKS_CLUSTER_NAME=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`EksClusterName`].OutputValue' --output text)
EKS_CLUSTER_CA_DATA=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`EksClusterCA`].OutputValue' --output text)
SPINNAKER_INSTANCE_PROFILE_ARN=$(aws cloudformation describe-stacks --stack-name spinnaker-managing-infrastructure-setup --query 'Stacks[0].Outputs[?OutputKey==`SpinnakerInstanceProfileArn`].OutputValue' --output text)
```

管理される側のアカウントで以下実行

```shell script
curl -O https://d3079gxvs8ayeg.cloudfront.net/templates/managed.yaml  

aws cloudformation deploy --stack-name spinnaker-managed-infrastructure-setup --template-file managed.yaml \
--parameter-overrides AuthArn=$AUTH_ARN ManagingAccountId=$MANAGING_ACCOUNT_ID --capabilities CAPABILITY_NAMED_IAM
```


以下のような設定を`~/.kube/config`ファイルに書き込んで、kubectlでの接続先を設定する
endpoint-url は　`aws eks describe-cluster --name spinnaker-cluster| jq '.cluster.endpoint' | tr -d '"'`
base64-encoded-ca-cert は　`aws eks describe-cluster --name spinnaker-cluster| jq '.cluster.certificateAuthority.data' | tr -d '"'`
cluster-name は spinnaker-cluster
[aws-iam-authenticator](https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/install-aws-iam-authenticator.html#w158aac27c11b5b3)をインストールしておく

```shell script
apiVersion: v1
clusters:
- cluster:
    server: <endpoint-url>
    certificate-authority-data: <base64-encoded-ca-cert>
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: aws-iam-authenticator
      args:
        - "token"
        - "-i"
        - "<cluster-name>"
        # - "-r"
        # - "<role-arn>"
      env: # 以下、default以外でAWSに繋いでいる場合は記述する
        - name: AWS_PROFILE
          value: spinnaker
```

ここから
Halyardにどの環境のkubernetesを使うことを教え込む
```shell script
hal config provider kubernetes enable
hal config provider kubernetes account add my-k8s-account --provider-version v2 --context $(kubectl config current-context)
hal config features edit --artifacts true
```

Spinnakerが乗っかるワーカーノードをデプロイする
```shell script
curl -O https://d3079gxvs8ayeg.cloudfront.net/templates/amazon-eks-nodegroup.yaml
aws cloudformation deploy --stack-name spinnaker-eks-nodes --template-file amazon-eks-nodegroup.yaml \
--parameter-overrides NodeInstanceProfile=$SPINNAKER_INSTANCE_PROFILE_ARN \
NodeInstanceType=t2.large ClusterName=$EKS_CLUSTER_NAME NodeGroupName=spinnaker-cluster-nodes ClusterControlPlaneSecurityGroup=$CONTROL_PLANE_SG \
Subnets=$SUBNETS VpcId=$VPC_ID --capabilities CAPABILITY_NAMED_IAM
```


<spinnaker-role-arn>の部分に変数AUTH_ARNを入れてやったファイルを作成する。
ファイル名は ` aws-auth-cm.yaml` に。

```shell script
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: <spinnaker-role-arn>
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
```

`kubectl apply -f aws-auth-cm.yaml` 実行する。

`kubectl get nodes --watch` したが、NotReadyになる。。。


## どの環境にSpinnakerをインストールするか選択する

### Azure上にSpinnakerサーバを建てようとした。

```shell script
hal config deploy edit --type distributed --account-name my-azure-account
```

が、
```
Account my-azure-account is not in a provider that supports  distributed installation of Spinnaker yet
```

1.28.0-20191119172816 においてはだめな模様

### LocalにSpinnakerサーバを立てる

Halyardをdockerでインストールした場合は必要なベースのDebianに必要なパッケージが入っていないためだめらしい

```shell script
hal config deploy edit --type localdebian
```

## 外部ストレージを選択する

アプリケーションの設定などをどこかに保存する必要がある

ここではAzure Storageを使ってみる

サブスクリプションをセットする。なにに？？
```shell script
az login
az account set --subscription `az account list | jq '.[].id' | tr -d '"'` 
```

リソースグループを作る
```shell script
RESOURCE_GROUP="SpinnakerStorage"
az group create --name $RESOURCE_GROUP --location japaneast
```

ストレージアカウントを作る
ストレージアカウント名は３〜２４文字で数と小文字のみ使える模様

```shell script
STORAGE_ACCOUNT_NAME="storagenannany"
az storage account create --resource-group $RESOURCE_GROUP --sku STANDARD_LRS --name $STORAGE_ACCOUNT_NAME
STORAGE_ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT_NAME --query [0].value | tr -d '"')
```

halyardにストレージの設定を教え込む

```shell script
hal config storage azs edit \
  --storage-account-name $STORAGE_ACCOUNT_NAME \
  --storage-account-key $STORAGE_ACCOUNT_KEY
```

halyard にストレージがAzure Storageであることを教え込む

```shell script
hal config storage edit --type azs
```

## Spinnakerをデプロイして、UIと接続する

`hal version list` コマンドで、使えるSpinnakerのversionを確認する
使うと決めたversionを設定する

```shell script
hal config version edit --version 1.17.5
```

Spinnakerを設定する

```shell script
sudo hal deploy apply
```

Spinnaker のUIに接続する??

```shell script
hal deploy connect
```

ブラウザから`http://localhost:9000`に行くとSpinnakerの画面に行ける

## Configをバックアップする



# 参考

https://www.spinnaker.io/


https://s3.amazonaws.com/aws-quickstart/quickstart-spinnaker/doc/spinnaker-on-the-aws-cloud.pdf

## Azureでできなかった

Azureでやってみる
azコマンドを[インストール](https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli-apt?view=azure-cli-latest)する。

Azureにログインして、支払いを行う subscription を設定する

```shell script
az login
SUBSCRIPTION_ID=`az account list | jq '.[].id'`
az account set --subscription $SUBSCRIPTION_ID
```

Service Principalを作成する

```shell script
az ad sp create-for-rbac --name "Spinnaker"
# az ad sp list の appOwnerTenantId
APP_ID=`az ad sp list  | jq '.[] | select(.appDisplayName == "Spinnaker") | .appId'`
# az ad sp list の appOwnerTenantId
TENANT_ID=`az ad sp list  | jq '.[] | select(.appDisplayName == "Spinnaker") | .appOwnerTenantId'`
```

プリンシパル作成時にJSON形式で表示される情報はどこかに控えておく

リソースグループを作成する

```shell script
RESOURCE_GROUP="Spinnaker"
az group create --name "Spinnaker" --location "japaneast"
```

暗号化する鍵を作成する
```shell script
VAULT_NAME="SpinnakerVaultNannany"
az keyvault create --enabled-for-template-deployment true --resource-group $RESOURCE_GROUP --name $VAULT_NAME
az keyvault set-policy --secret-permissions get --name $VAULT_NAME --spn $APP_ID
az keyvault secret set --name VMUsername --vault-name $VAULT_NAME --value nannany

ssh-keygen -m PEM -t rsa -b 4096
az keyvault secret set --name VMSshPublicKey --vault-name $VAULT_NAME --value @~/.ssh/id_rsa
```

halにAzureのもろもろを設定する

```shell script
docker run -d -p 8084:8084 -p 9000:9000 \
    --name halyard --rm \
    -v ~/.hal:/home/spinnaker/.hal \
    -it \
    -e APP_ID=$APP_ID \
    -e TENANT_ID=$TENANT_ID \
    -e SUBSCRIPTION_ID=$SUBSCRIPTION_ID \
    -e VAULT_NAME=$VAULT_NAME \
    -e RESOURCE_GROUP=$RESOURCE_GROUP \
    gcr.io/spinnaker-marketplace/halyard:stable
```

halyardのコンテナに入った上で、

```shell script
hal config provider azure enable

hal config provider azure account add my-azure-account \
  --client-id $APP_ID \
  --tenant-id $TENANT_ID \
  --subscription-id $SUBSCRIPTION_ID \
  --default-key-vault $VAULT_NAME \
  --default-resource-group $RESOURCE_GROUP \
  --packer-resource-group $RESOURCE_GROUP \
  --app-key
```

このときにパスワードを聞かれるので、サービスプリンシパル作成時に控えたpasswordを入力する


