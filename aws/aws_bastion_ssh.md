# 疑問に思った点、つまずいた点

* VPC消したら紐づくセキュリティグループも消える？→消える
* VPC内にEC2たてるとなると、サブネットが必ずいる？→いる
* awscliの`--query`はwindows10のコマンドプロンプトではうまく実行できない。powershellを使う

# cliを使って操作する準備

1. pip install awscliコマンドを打ってawscliをインストールする
2. https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/getting-started_create-admin-group.html に従ってAdministrator を作成
3. aws configureコマンドを打って、awscliとAdministratorを紐づける

# bastionのインスタンス生成

## bastionを入れるVPCを整備

1. bastion用VPC作成  
```
aws ec2 create-vpc --cidr-block 10.1.0.0/16 
aws ec2 create-tags --resources vpc-0074168dfa72a5826 --tags Key=Name,Value=bastion_cli
```
2. bastion用サブネット作成  
```
aws ec2 create-subnet --vpc-id vpc-0074168dfa72a5826 --cidr-block 10.1.0.0/24
aws ec2 create-tags --resources subnet-0bb7116ca38f5a80f --tags Key=Name,Value=bastion_subnet_cli
```
3. インターネットゲートウェイの作成  
```
aws ec2 create-internet-gateway
```
4. bastion用VPCにインターネットゲートウェイをアタッチ  
```
aws ec2 attach-internet-gateway --vpc-id  vpc-0074168dfa72a5826 --internet-gateway-id igw-06c61291eaba0ac1f
```
5. bastion用VPCにカスタムルートテーブルを作成  
```
aws ec2 create-route-table --vpc-id vpc-0074168dfa72a5826
```
6. インターネットゲートウェイへのすべてのトラフィック (0.0.0.0/0) をポイントするルートテーブルでルートを作成  
```
aws ec2 create-route --route-table-id rtb-0362a010826fc18bc --destination-cidr-block 0.0.0.0/0 --gateway-id igw-06c61291eaba0ac1f
```
7. サブネットとカスタムルートテーブルを紐づける  
```
aws ec2 associate-route-table  --subnet-id subnet-0bb7116ca38f5a80f --route-table-id rtb-0362a010826fc18bc
```

## bastionのインスタンス作成
1. キーペアを作成する  
```
aws ec2 create-key-pair --key-name bastion_cli_key --query 'KeyMaterial' --output text > bastion_cli_key.pem
```
2. bastionインスタンス用セキュリティグループ作成。22番ポートにくるSSHのみ許可  
```
aws ec2 create-security-group --group-name SSHAccess --description "Security group for SSH access" --vpc-id vpc-0074168dfa72a5826
aws ec2 authorize-security-group-ingress --group-id sg-04fa98bf54b2c3602 --protocol tcp --port 22 --cidr 0.0.0.0/0
```
3. EC2インスタンス作成。無料枠のAMI（Amazonマシンイメージ）を選択  
```
aws ec2 run-instances --image-id ami-0d7ed3ddb85b521a6 --count 1 --instance-type t2.micro --key-name bastion_cli_key --security-group-ids sg-04fa98bf54b2c3602 --subnet-id subnet-0bb7116ca38f5a80f
```
4. ElasticIPを新規発行  
```
aws ec2 allocate-address --domain vpc
```
5. ElasticIPをEC2インスタンスにアタッチ  
```
aws ec2 associate-address --allocation-id eipalloc-0cab4412fd7b91c64 --instance i-03472fc06af6b8690
```
6. SSHで該当のインスタンスに接続できるか確認（powershell使用）  
```
ssh -i .ssh\bastion_cli_key.pem ec2-user@52.198.210.184
```


# bastion経由で操作したいインスタンス(testインスタンス)作成

1. testインスタンス用VPC作成



