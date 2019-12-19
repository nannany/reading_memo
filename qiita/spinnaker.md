spinnakerでそもそも何ができるのか

動かして見る系ある？

どこまでやるか


とりあえず使ってみる
## Halyardをインストールする

Halyardって何をしてくれるやつ？

Halyardなくてもできるらしいが、おすすめできないらしい

[ ここ ](https://www.spinnaker.io/setup/install/halyard/#install-halyard-on-docker)に従ってインストール


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

## クラウドプロバイダを選択する


## どの環境にSpinnakerをインストールするか選択する

## 外部ストレージを選択する

## Configをバックアップする

# 参考

https://www.spinnaker.io/