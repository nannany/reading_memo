# 疑問に思った点、つまずいた点

* VPC消したら紐づくセキュリティグループも消える？→消える
* VPC内にEC2たてるとなると、サブネットが必ずいる？→いる
* awscliの`--query`はwindows10のコマンドプロンプトではうまく実行できない。powershellを使う
* EC2を起動するコマンドは？→`aws ec2 start-instances --instance-ids <instance_id>`
* `aws ec2 describe-instance-status`だと起動中のインスタンスしか表示されない
* EC2を再起動するコマンドは？→`aws ec2 reboot-instances --instance-ids <instance_id>`

# cliを使って操作する準備

1. pip install awscliコマンドを打ってawscliをインストールする
2. https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/getting-started_create-admin-group.html に従ってAdministrator を作成
3. aws configureコマンドを打って、awscliとAdministratorを紐づける

# bastionのインスタンス生成

## bastionを入れるVPCを整備

### 1. bastion用VPC作成  

```
aws ec2 create-vpc --cidr-block 10.1.0.0/16 
aws ec2 create-tags --resources vpc-0074168dfa72a5826 --tags Key=Name,Value=bastion_cli
```
### 2. bastion用サブネット作成  

```
aws ec2 create-subnet --vpc-id vpc-0074168dfa72a5826 --cidr-block 10.1.0.0/24
aws ec2 create-tags --resources subnet-0bb7116ca38f5a80f --tags Key=Name,Value=bastion_subnet_cli
```
### 3. インターネットゲートウェイの作成  

```
aws ec2 create-internet-gateway
```

### 4. bastion用VPCにインターネットゲートウェイをアタッチ  

```
aws ec2 attach-internet-gateway --vpc-id  vpc-0074168dfa72a5826 --internet-gateway-id igw-06c61291eaba0ac1f
```
### 5. bastion用VPCにカスタムルートテーブルを作成  

```
aws ec2 create-route-table --vpc-id vpc-0074168dfa72a5826
```
### 6. インターネットゲートウェイへのすべてのトラフィック (0.0.0.0/0) をポイントするルートテーブルでルートを作成  

```
aws ec2 create-route --route-table-id rtb-0362a010826fc18bc --destination-cidr-block 0.0.0.0/0 --gateway-id igw-06c61291eaba0ac1f
```
### 7. サブネットとカスタムルートテーブルを紐づける  

```
aws ec2 associate-route-table  --subnet-id subnet-0bb7116ca38f5a80f --route-table-id rtb-0362a010826fc18bc
```

## bastionのインスタンス作成

### 1. キーペアを作成する  

```
aws ec2 create-key-pair --key-name bastion_cli_key --query 'KeyMaterial' --output text > bastion_cli_key.pem
```
### 2. bastionインスタンス用セキュリティグループ作成。22番ポートにくるSSHのみ許可  

```
aws ec2 create-security-group --group-name SSHAccess --description "Security group for SSH access" --vpc-id vpc-0074168dfa72a5826
aws ec2 authorize-security-group-ingress --group-id sg-04fa98bf54b2c3602 --protocol tcp --port 22 --cidr 0.0.0.0/0
```
### 3. EC2インスタンス作成。無料枠のAMI（Amazonマシンイメージ）を選択  

```
aws ec2 run-instances --image-id ami-0d7ed3ddb85b521a6 --count 1 --instance-type t2.micro --key-name bastion_cli_key --security-group-ids sg-04fa98bf54b2c3602 --subnet-id subnet-0bb7116ca38f5a80f
aws ec2 create-tags --resources i-03472fc06af6b8690 --tags Key=Name,Value=my_bastion
```
### 4. ElasticIPを新規発行  

```
aws ec2 allocate-address --domain vpc
```
### 5. ElasticIPをEC2インスタンスにアタッチ  

```
aws ec2 associate-address --allocation-id eipalloc-0cab4412fd7b91c64 --instance i-03472fc06af6b8690
```
### 6. SSHで該当のインスタンスに接続できるか確認（powershell使用）  

```
ssh -i .ssh\bastion_cli_key.pem ec2-user@52.198.210.184
```

# bastion経由で操作したいインスタンス(targetインスタンス)作成

## targetインスタンスを入れるVPCを整備

### 1. targetインスタンス用VPC作成  

```
aws ec2 create-vpc --cidr-block 10.2.0.0/16 
aws ec2 create-tags --resources vpc-0ed7b004702d6b31f --tags Key=Name,Value=target_cli
```
### 2. targetインスタンス用サブネット作成  

```
aws ec2 create-subnet --vpc-id vpc-0ed7b004702d6b31f --cidr-block 10.2.0.0/24
aws ec2 create-tags --resources subnet-066876581dbfa4f88 --tags Key=Name,Value=target_subnet_cli
```

## targetインスタンス作成(キーペアは前作ったものを使いまわす）

### 1. 秘密鍵（bastion_cli_key)をmy_bastionに転送

```
scp -i .ssh/bastion_cli_key.pem  .ssh/bastion_cli_key.pem ec2-user@52.198.210.184:/home/ec2-user
```

### 2. 秘密鍵の権限を400にして、.ssh配下におさめる

```
ssh -i .ssh\bastion_cli_key.pem ec2-user@52.198.210.184
chmod 400 bastion_cli_key.pem 
mv bastion_cli_key.pem .ssh
```

### 3. VPCどうしをピアリング接続し、その接続を承諾する

```
aws ec2 create-vpc-peering-connection --vpc-id vpc-0ed7b004702d6b31f --peer-vpc-id vpc-0074168dfa72a5826
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id pcx-094d895104a32cf4a
```

### 4. 各VPCのルートテーブルにて、相手のVPCへの通信をピアリング接続に紐づけるようにする

```
# bastion側のカスタムルートテーブルにピアリング接続へのルートを加える
aws ec2 create-route --route-table-id rtb-0362a010826fc18bc --destination-cidr-block 10.2.0.0/16 --vpc-peering-connection-id pcx-094d895104a32cf4a
# target側のメインルートテーブルにピアリング接続へのルートを加える
aws ec2 create-route --route-table-id rtb-02a9cca2b46dac9a2 --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id pcx-094d895104a32cf4a
```

### 5. targetインスタンス用セキュリティグループ作成。22と10000番ポートにくるSSHのみ許可  

```
aws ec2 create-security-group --group-name from_bastion_ssh --description "Security group for SSH access from bastion" --vpc-id vpc-0ed7b004702d6b31f
aws ec2 authorize-security-group-ingress --group-id sg-098ded7f7da9bc597 --protocol tcp --port 22 --source-group sg-04fa98bf54b2c3602
aws ec2 authorize-security-group-ingress --group-id sg-098ded7f7da9bc597 --protocol tcp --port 10000 --source-group sg-04fa98bf54b2c3602
```

### 6. targetのEC2インスタンス作成。無料枠のAMI（Amazonマシンイメージ）を選択  

```
aws ec2 run-instances --image-id ami-0d7ed3ddb85b521a6 --count 1 --instance-type t2.micro --key-name bastion_cli_key --security-group-ids sg-098ded7f7da9bc597 --subnet-id subnet-066876581dbfa4f88
aws ec2 create-tags --resources i-04b09b50680736f5f --tags Key=Name,Value=my_target
```

### 7. bastion経由でtargetインスタンスに接続する  

```
# クライアント端末のpowershellで実行
ssh -i .ssh\bastion_cli_key.pem ec2-user@52.198.210.184
# bastionで実行
ssh -i .ssh/bastion_cli_key.pem ec2-user@10.2.0.78
```

### 8. sshd_configを編集

```
cd /etc/ssh/
# sshd_configを退避 
sudo cp sshd_config sshd_configbk
# sshd_configを編集
sudo vim sshd_config
```

差分はこんな感じ

```
< Port 22
---
> Port 10000
```

### 9. targetインスタンスを再起動

```
aws ec2 reboot-instances --instance-ids i-04b09b50680736f5f
```

### 10. 22番ポートでは接続できず、10000番ポートで接続できることを確認

```
[ec2-user@ip-10-1-0-184 ~]$ ssh -p 22 -i .ssh/bastion_cli_key.pem ec2-user@10.2.0.78
ssh: connect to host 10.2.0.78 port 22: Connection refused
```

```
[ec2-user@ip-10-1-0-184 ~]$ ssh -i .ssh/bastion_cli_key.pem -p 10000 ec2-user@10.2.0.78
Last login: Sun Jan 27 03:35:37 2019 from 10.1.0.184

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
```

### 11. targetインスタンスに紐づくセキュリティグループから、22番ポートの通信許可を外す

```
aws ec2 revoke-security-group-ingress --group-id sg-098ded7f7da9bc597 --protocol tcp --port 22 --source-group sg-04fa98bf54b2c3602
```

