ローカルにSpinnaker入れてもうまく動かなかった。
ので、Azure上にSpinnakerサーバを立てることにする

Spinnaker のVMを立てる

[ここ](https://github.com/Azure/azure-quickstart-templates/tree/master/101-spinnaker#azure-spinnaker-)の「Deploy to Azure」ボタンをクリックする

必須項目はよしなに。ssh public key のところは、
```shell script
ssh-keygen -m PEM -t rsa -b 4096
```

で `~/.ssh/`配下に作成されたpublic key を入れる


