これでやってみるか
https://aws.amazon.com/jp/blogs/opensource/continuous-delivery-spinnaker-amazon-eks/

* AWS Cloud9 の環境作成する
* AWS Cloud9 の環境設定する
* Amazon EKS のクラスターを作成する
* Spinnaker をインストール、設定する
* クリーンアップ



## AWS Cloud9 の環境作成する
### VPC作成する
VPCの設定がまるまる抜けているので、やる
[ ここ ]( https://docs.aws.amazon.com/ja_jp/cloud9/latest/user-guide/vpc-settings.html#vpc-settings-create-vpc )

* [ VPCコンソール ](https://console.aws.amazon.com/vpc)にある、「VPCウィザードの起動」をクリック
* 1個のパブリックサブネットを持つVPCを選択
* 「VPC名」「サブネット名」に任意の名前を入力して、その他はデフォルトのまま「VPCの作成」をクリック
* VPCダッシュボードで、先程名付けた「VPC名」に該当するVPCを選択し、「説明」タブの「ネットワークACL」の右のリンクをクリックする
* 「インバウンドのルール」タブを選択し、「インバウンドのルールの編集ボタン」をクリックする

```shell script
jq '.prefixes[] | select(.service=="CLOUD9") | select(.region=="ap-northeast-1")' < ip-ranges.json
```
で出力されるIPを入力する

画面をポチポチやりながら作成する

VPCができたら、画面ポチポチしてCloud9作成。
Networkの設定のところで先ほど作成したVPCを入力する


## AWS Cloud9 の環境設定する

kubectl, aws-iam-authenticator を Cloud9に入れる

```shell script
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/aws-iam-authenticator

chmod +x ./aws-iam-authenticator

mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH

echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc

aws-iam-authenticator  help
```

awscliをアップグレードする

```shell script
pip install awscli --upgrade --user
```

eksctlをインストールする

```shell script
curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sudo mv /tmp/eksctl /usr/local/bin
```

Terraformをインストールする

```shell script
wget https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip
unzip terraform_0.12.4_linux_amd64.zip
sudo mv terraform /usr/local/bin/
export PATH=$PATH:/usr/local/bin/terraform
```


Halyardをインストールする
```shell script
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh
sudo bash InstallHalyard.sh
sudo update-halyard
hal -v
```

## Amazon EKS のクラスターを作成する

強い権限を持ったIAMユーザーを作ってクラスターのおいて、
`aws configure --profile spin` みたいな感じで、登録しとく。
その上で、`export AWS_PROFILE=spin` して、クラスターの作成をする
本当はだめな気がする

本番用 Amazon EKSクラスターを作成する
```shell script
eksctl create cluster --name=eks-prod --nodes=3 
```

UAT用 Amazon EKSクラスターを作成する
```shell script
eksctl create cluster --name=eks-uat --nodes=3 
```

Spinnaker用 Amazon EKSクラスターを作成する
```shell script
eksctl create cluster --name=eks-spinnaker --nodes=2 
```

## Spinnaker をインストール、設定する

1. kubectlにおけるcontextを追加する

```shell script
aws eks update-kubeconfig --name eks-spinnaker --region ap-northeast-1 --alias eks-spinnaker

aws eks update-kubeconfig --name eks-uat --region ap-northeast-1 --alias eks-uat

aws eks update-kubeconfig --name eks-prod --region ap-northeast-1 --alias eks-prod
```

2. halyardのバージョンを確認する
これいる？？
```shell script
hal -v
```

3. Docker registoryを作成する
Docker Hub を使用することをhalyardに教え込む
usernameの部分には自身のユーザー名を打ち込みます
```shell script
hal config provider docker-registry enable 

hal config provider docker-registry account add nannany-docker --address index.docker.io --username nannany --password
```

4. github アカウントを登録する

```shell script
hal config artifact github enable

hal config artifact github account add spinnaker-github --username nannany --password --token
```

5. Kubernetesアカウントを設定する

#### 本番クラスターの設定

```shell script
hal config provider kubernetes enable

kubectl config use-context eks-prod
```

変数CONTEXTに現在のcontextを設定
```shell script
CONTEXT=$(kubectl config current-context)
```

サービスアカウントを作成する
```shell script
kubectl apply --context $CONTEXT -f https://spinnaker.io/downloads/kubernetes/service-account.yml
```

作成したサービスアカウントからトークンを抜き出す

```shell script
TOKEN=$(kubectl get secret --context $CONTEXT \
   $(kubectl get serviceaccount spinnaker-service-account \
       --context $CONTEXT \
       -n spinnaker \
       -o jsonpath='{.secrets[0].name}') \
   -n spinnaker \
   -o jsonpath='{.data.token}' | base64 --decode)
```

kubernetes の設定を追記する
```shell script
kubectl config set-credentials ${CONTEXT}-token-user --token $TOKEN

kubectl config set-context $CONTEXT --user ${CONTEXT}-token-user
```

`eks-prod cluster`をKubernetes Providerとして登録する
```shell script
hal config provider kubernetes account add eks-prod --provider-version v2 \
 --docker-registries nannany-docker --context $CONTEXT
```

#### UATクラスターの設定

変数CONTEXTに現在のcontextを設定
そして、サービスアカウント作成
```shell script
kubectl config use-context eks-uat 

CONTEXT=$(kubectl config current-context) 

kubectl apply --context $CONTEXT \
    -f https://spinnaker.io/downloads/kubernetes/service-account.yml
```

作成したサービスアカウントからトークンを抜き出す

```shell script
TOKEN=$(kubectl get secret --context $CONTEXT \
   $(kubectl get serviceaccount spinnaker-service-account \
       --context $CONTEXT \
       -n spinnaker \
       -o jsonpath='{.secrets[0].name}') \
   -n spinnaker \
   -o jsonpath='{.data.token}' | base64 --decode)
```

kubeconfigファイルに設定を追記
```shell script
kubectl config set-credentials ${CONTEXT}-token-user --token $TOKEN

kubectl config set-context $CONTEXT --user ${CONTEXT}-token-user
```


`eks-uat cluster`をKubernetes Providerとして登録する
```shell script
hal config provider kubernetes account add eks-uat --provider-version v2 \
 --docker-registries nannany-docker --context $CONTEXT
```

#### Spinnaker クラスターの設定

contextを切り替えて、サービスアカウントを作成する
```shell script
kubectl config use-context eks-spinnaker 

CONTEXT=$(kubectl config current-context)

kubectl apply --context $CONTEXT \
    -f https://spinnaker.io/downloads/kubernetes/service-account.yml
```

作成したサービスアカウントからトークンを抜き出す

```shell script
TOKEN=$(kubectl get secret --context $CONTEXT \
   $(kubectl get serviceaccount spinnaker-service-account \
       --context $CONTEXT \
       -n spinnaker \
       -o jsonpath='{.secrets[0].name}') \
   -n spinnaker \
   -o jsonpath='{.data.token}' | base64 --decode)
```

kubeconfigに設定を追記
```shell script
kubectl config set-credentials ${CONTEXT}-token-user --token $TOKEN

kubectl config set-context $CONTEXT --user ${CONTEXT}-token-user
```

`eks-uat cluster`をKubernetes Providerとして登録する

```shell script
hal config provider kubernetes account add eks-spinnaker --provider-version v2 \
 --docker-registries nannany-docker  --context $CONTEXT
```

6. artifact サポート？をいれる

```shell script
hal config features edit --artifacts true
```

7. Spinnakerを分散インストールすることをhalyardに教え込む

```shell script
hal config deploy edit --type distributed --account-name eks-spinnaker
```

8. SpinnakerでS3を使えるように設定する


<access-key>には、最初に作成したIAMユーザーのアクセスキーを入力する
```shell script
export YOUR_ACCESS_KEY_ID=<access-key>
export YOUR_ACCESS_KEY_ID=

hal config storage s3 edit --access-key-id $YOUR_ACCESS_KEY_ID  --secret-access-key 
```

入力後、secret access keyを求められるので、入力

halyardにストレージとして、S3を使用することを教え込む

```shell script
hal config storage edit --type s3
```

9. インストールするSpinnakerのバージョンを指定し、デプロイ

```shell script
hal version list

export VERSION=1.15.0
hal config version edit --version $VERSION

hal deploy apply
```

10. Spinnaker がインストールされているか確認する

```shell script
kubectl -n spinnaker get svc
```

11. Elastic Loadbalancerを使用して、Spinnakerを公開する

```shell script
export NAMESPACE=spinnaker

kubectl -n ${NAMESPACE} expose service spin-gate --type LoadBalancer \
  --port 80 --target-port 8084 --name spin-gate-public 

kubectl -n ${NAMESPACE} expose service spin-deck --type LoadBalancer \
  --port 80 --target-port 9000 --name spin-deck-public  

export API_URL=$(kubectl -n $NAMESPACE get svc spin-gate-public -o jsonpath='{.status.loadBalancer.ingress[0].hostname}') 

export UI_URL=$(kubectl -n $NAMESPACE get svc spin-deck-public -o jsonpath='{.status.loadBalancer.ingress[0].hostname}') 

hal config security api edit --override-base-url http://${API_URL} 

hal config security ui edit --override-base-url http://${UI_URL}

hal deploy apply
```

12. もう一回確認する

```shell script
kubectl -n spinnaker get svc
```

13. Spinnakerコンソールにログインする

12のコマンド結果が以下みたいな感じになる
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP                                                                    PORT(S)        AGE
spin-clouddriver   ClusterIP      10.100.81.71     <none>                                                                         7002/TCP       3m47s
spin-deck          ClusterIP      10.100.227.41    <none>                                                                         9000/TCP       3m46s
spin-deck-public   LoadBalancer   10.100.82.52     ~~~~~~~~~~~.ap-northeast-1.elb.amazonaws.com   80:30884/TCP   2m36s
spin-echo          ClusterIP      10.100.58.79     <none>                                                                         8089/TCP       3m46s
spin-front50       ClusterIP      10.100.65.76     <none>                                                                         8080/TCP       3m45s
spin-gate          ClusterIP      10.100.255.44    <none>                                                                         8084/TCP       3m45s
spin-gate-public   LoadBalancer   10.100.225.51    ~~~~~~~~~~~.ap-northeast-1.elb.amazonaws.com    80:30648/TCP   2m36s
spin-igor          ClusterIP      10.100.37.116    <none>                                                                         8088/TCP       3m46s
spin-orca          ClusterIP      10.100.204.159   <none>                                                                         8083/TCP       3m46s
spin-redis         ClusterIP      10.100.12.240    <none>                                                                         6379/TCP       3m47s
spin-rosco         ClusterIP      10.100.188.226   <none>                                                                         8087/TCP       3m44s
```
`spin-deck-public`のEXTERNAL-IPにアクセスする

-----------------

kubectl get nodesが成功しない。。
```shell script
error: You must be logged in to the server (Unauthorized)
```
↓
`eksctl create cluster` を強い権限で実行すると行けるっぽい


