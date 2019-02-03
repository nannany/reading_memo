# やること

Dockerについて理解するために、非常に簡易なアプリケーションのdockerイメージを作って動かしてみる。  
具体的には、"Hello world!" を1秒に1回出すようなアプリケーションを動作させる。
ビルド〜実行まですべてコンテナ上で行うことを目指す。
  
Javaのソースコードは以下のよう。  
https://github.com/nannany/very-simple-application

# 環境

Windows10 HOME 上で実行した。  
Windows上にDockerの動作環境を作成するにあたっては、Docker Toolboxを使用した。  
詳細は以下の記事参照。  
https://qiita.com/idani/items/fb7681d79eeb48c05144

# dockerイメージを作る流れ

dockerイメージ作成のざっくりとした流れは以下の図のような感じ。  
意識すべき登場人物としては、

* 自身のローカル端末
* ビルドコンテキスト
* dockerイメージ

dockerビルドコマンド実行時に、どのパス配下のファイルをビルドコンテキストに追加するかを決める。  
このとき、ビルドコンテキストに持っていきたくないファイルは`.dockerignore`ファイルに記述する。  
 
また、Dockerfile内のCOPY命令で、ビルドコンテキスト内の何をイメージに持っていくか決める。

![イメージ](ビルドコンテキスト.jpg)

# 実行するdockerコマンド

イメージを作成する際に実行するdockerコマンドは、

```
docker build -t simple-application -f Dockerfile.cmd .
```

`-t simple-application` にて、イメージの名称をsimple-applicationにしている。  
`-f Dockerfile.cmd` にて、イメージの作成に際して使用するDockerfileを、上記のコマンドを実行しているパスにあるDockerfile.cmdとしている。（デフォルトは、コマンドを実行しているパスにあるDockerfileが選択される）  
最後の`.`は、コマンドを実行しているパス配下がビルドコンテキストに追加されますよ、ということを意味している。

# Dockerfile

全体としては以下のよう。

```
FROM ubuntu:disco

COPY . .
RUN apt-get update && apt-get install -y \
    maven \
    openjdk-8-jre \
 && cd simple \
 && mvn package
CMD ["java","-jar","simple/target/simple-1.0-SNAPSHOT.jar"]
```


まずはベースイメージを選ぶために、`FROM`を記述する。  
ここでは、適当に`ubuntu:disco`を選択する。  
 
次に、ビルドコンテキストからイメージにファイルをコピーするために、`COPY . .`と記述する。  
 
その次に、ソースのビルド、Javaの実行に必要なパッケージ（mavenとopenjdk）をインストールし、mavenのjar作成コマンドを実行する。

```
RUN apt-get update && apt-get install -y \
    maven \
    openjdk-8-jre \
 && cd simple \
 && mvn package
```

書き方は下記をまねて、レイヤの数の最小化、apt-get updateとinstallを同時にやることを意識した。
http://docs.docker.jp/engine/articles/dockerfile_best-practice.html

最後に、コンテナが起動した後に`java -jar simple/target/simple-1.0-SNAPSHOT.jar`が実行されるように、以下のように記述した。

```
CMD ["java","-jar","simple/target/simple-1.0-SNAPSHOT.jar"]
```

# 動かす

上記で作成したイメージを、以下のコマンドで動作させてみる。
```
docker run simple-application-cmd
```

以下のように表示され、うまくいった。

![hello](hello.gif)


# maven入りのイメージ

上では`ubuntu:disco`をベースイメージに指定して、RUNでmavenとJavaをイメージにインストールした。  
しかし、もともとmavenとJavaが入っているベースイメージが存在しているので、それを使用したDockerfileが以下。（なぜかテストでエラったのでそこはとばした）

```
FROM maven:3-jdk-8

COPY . .
RUN cd simple && mvn package -Dmaven.test.skip=true
CMD ["java","-jar","simple/target/simple-1.0-SNAPSHOT.jar"]
```
