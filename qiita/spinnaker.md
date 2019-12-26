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

====

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

===

## クラウドプロバイダを選択する

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

## Configをバックアップする

# 参考

https://www.spinnaker.io/