# Azure CLIのインストール

下記のページの「MSIインストーラのダウンロード」からmsiをダウンロードして、実行。
https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli-windows?view=azure-cli-latest

`az login`コマンドを実行するとブラウザが立ち上がるので、自分のアカウントでログインする。

# やること

github上にあるソースコードを、Azure DevOpsのPipelinesでCIをまわす。  

githubへのpushをトリガーとして、CIが回り始め、ジョブの中でソースのビルドを実行し、Dockerイメージを作成し、作成したイメージをDocker HubにPUSHする。

# 前提

Azureにアカウントを作っている。

# pipelineを作る手順

まず、Azure DevOpsにログインし、以下の画面に遷移して、pipelineを押下。

![①](welcome_to_project.bmp)

以下のような画面がでたら、New pipelineを押下。

![②](create_pipeline.bmp)

以下の画面で、GitHubを押下。

![③](select_source.bmp)

以下の画面で、Authorizeを押下。

![④](oauth.bmp)

以下の画面で、Authorize AzurePipelinesを押下。

![⑤](oauth2.bmp)

以下の画面で、GitHubのパスワードを入力。

![⑥](confirm_password.bmp)

以下のような画面から、連携したいリポジトリを選択。

![⑦](select_repo.bmp)

以下の画面で、Docker imageを選択。

![⑧](configure_pipeline.bmp)

デフォルトで以下のようなYAMLの生成が促されるので、Save and run押下。

![⑨](default.bmp)

Save and run押下。

![⑩](save_and_run.bmp)

ジョブが走る。成功したら以下のような画面になる。

![⑪](success.bmp)
