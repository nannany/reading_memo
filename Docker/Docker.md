# 1章 コンテナとはなにか、そしてなぜ注目されているのか
コンテナの利点。
* コンテナは、ホストOSとリソースを共有するためVMよりはるかに効率的。
* コンテナはポータビリティがとても高く、動作環境の違いによって生まれるバグを撲滅してくれるかもしれない。
* コンテナは軽量なので、VMに比べて多くのコンテナを1台のホストマシンで実行できる。
* ユーザーは設定、インストールの問題に煩わされなくなる。開発者は、ユーザーの環境差異を心配せずにすむようになる。

そもそもVMとコンテナでは目的が違う。
VMは異なる環境の完全エミュレートであり、コンテナはアプリケーションをポータブルにし、単体で動作させることにある。

# 2章 インストール
インストールを行う。
実行した環境は以下のよう。
```bash
uname -a
Linux vagrant-ubuntu-trusty-64 3.13.0-139-generic #188-Ubuntu SMP Tue Jan 9 14:43:09 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

Dockerのインストールコマンドをうつ。
```bash
curl https://get.docker.com > /tmp/install.sh
/tmp/install.sh
```

自分のユーザをdockerグループに加える。
```bash
sudo usermod -aG docker $USER
```

うまくできてたら、docker version で以下のように出る。
```bash
docker version
```

```
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        e68fc7a
 Built:             Tue Aug 21 17:24:58 2018
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       e68fc7a
  Built:            Tue Aug 21 17:23:24 2018
  OS/Arch:          linux/amd64
  Experimental:     false
```

# 3章 はじめの一歩
```bash
docker run debian echo "Hello world"
```
↓表示結果
```
Unable to find image 'debian:latest' locally
latest: Pulling from library/debian
55cbf04beb70: Pull complete
Digest: sha256:f1f61086ea01a72b30c7287adee8c929e569853de03b7c462a8ac75e0d0224c4
Status: Downloaded newer image for debian:latest
Hello world
```

docker run はコンテナの起動を受け持つコマンドで、debian は使いたいイメージの名前である。

表示の1行目はローカルにDebianのイメージがないことを示す。
そのあとDockerがDocker Hubをオンラインでチェックして、最新バージョンのDebianのイメージをダウンロードする。
ダウンロード後、Dockerがイメージをコンテナに変えて、その中で echo "Hello world"を実行する。

2回目の実行
```
vagrant@vagrant-ubuntu-trusty-64:~$ docker run debian echo "Hello world"
Hello world
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker run -i -t debian /bin/bash
root@83ce046ebf00:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@83ce046ebf00:/# echo "afdsdsfds"
afdsdsfds
root@83ce046ebf00:/# exit
exit
```

-iと-tでtty付きのインタラクティブセッション（？）を要求する
/bin/bash でbashシェルが立ち上がる


## 3.2　基本のコマンド群
```
vagrant@vagrant-ubuntu-trusty-64:~$ docker run -h CONTAINER -i -t debian /bin/bash
root@CONTAINER:/# mv /bin /basket
root@CONTAINER:/# ls
bash: ls: command not found
```

別ターミナルを立ち上げてdocker psする
```
vagrant@vagrant-ubuntu-trusty-64:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
a72bc666c053        debian              "/bin/bash"         2 minutes ago       Up 2 minutes                            stupefied_bassi
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker inspect stupefied_bassi | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2",
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker inspect --format {{.NetworkSettings.IPAddress}} stupefied_bassi
172.17.0.2
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker diff stupefied_bassi
C /.wh..wh.plnk
A /.wh..wh.plnk/82.659222
D /bin
A /basket
A /basket/bash
A /basket/cat
A /basket/chgrp
A /basket/chmod
A /basket/chown
A /basket/cp
A /basket/dash
A /basket/date
A /basket/dd
A /basket/df
A /basket/dir
A /basket/dmesg
A /basket/dnsdomainname
A /basket/domainname
A /basket/echo
A /basket/egrep
A /basket/false
A /basket/fgrep
A /basket/findmnt
A /basket/grep
A /basket/gunzip
A /basket/gzexe
A /basket/gzip
A /basket/hostname
A /basket/ip
A /basket/ln
A /basket/login
A /basket/ls
A /basket/lsblk
A /basket/mkdir
A /basket/mknod
A /basket/mktemp
A /basket/more
A /basket/mount
A /basket/mountpoint
A /basket/mv
A /basket/nisdomainname
A /basket/pidof
A /basket/ping
A /basket/ping4
A /basket/ping6
A /basket/pwd
A /basket/rbash
A /basket/readlink
A /basket/rm
A /basket/rmdir
A /basket/run-parts
A /basket/sed
A /basket/sh
A /basket/sh.distrib
A /basket/sleep
A /basket/ss
A /basket/stty
A /basket/su
A /basket/sync
A /basket/tailf
A /basket/tar
A /basket/tempfile
A /basket/touch
A /basket/true
A /basket/umount
A /basket/uname
A /basket/uncompress
A /basket/vdir
A /basket/wdctl
A /basket/which
A /basket/ypdomainname
A /basket/zcat
A /basket/zcmp
A /basket/zdiff
A /basket/zegrep
A /basket/zfgrep
A /basket/zforce
A /basket/zgrep
A /basket/zless
A /basket/zmore
A /basket/znew
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker logs stupefied_bassi
root@CONTAINER:/# mv /bin /basket
root@CONTAINER:/# ls
bash: ls: command not found
root@CONTAINER:/# cd
root@CONTAINER:~# ls
bash: ls: command not found
root@CONTAINER:~# pwd
/root
root@CONTAINER:~# ps
bash: ps: command not found
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                        PORTS               NAMES
a72bc666c053        debian              "/bin/bash"            15 minutes ago      Exited (127) 47 seconds ago                       stupefied_bassi
83ce046ebf00        debian              "/bin/bash"            19 minutes ago      Exited (0) 19 minutes ago                         pensive_swanson
0dc7ae846a21        debian              "echo 'Hello world'"   21 minutes ago      Exited (0) 21 minutes ago                         naughty_gates
bda38828beba        debian              "echo 'Hello world'"   27 minutes ago      Exited (0) 27 minutes ago                         suspicious_chaplygin
```


```
vagrant@vagrant-ubuntu-trusty-64:~$ docker rm stupefied_bassi
stupefied_bassi
```

cowsayをコンテナの中でインストール

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker commit cowsay test/cowsayimage
sha256:a7fe095e54c25cb78d6247c568f9978ab5670895e1fb33da2c622ce420f12cae
```

```
vagrant@vagrant-ubuntu-trusty-64:~$ docker run test/cowsayimage /usr/games/cowsay "Moo"
 _____
< Moo >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

上でやった手順を自動構築するのがDockerfile

## 3.3 Dockerfileからのイメージ構築
Dockerfileを作る

```
vagrant@vagrant-ubuntu-trusty-64:~/docker/cowsay$ docker build -t test/cowsay-dockerfile .
```


## 3.5 redis

```
vagrant@vagrant-ubuntu-trusty-64:~/docker/cowsay$ docker run --rm -it --link myredis:redis redis /bin/bash
root@31505dcd2129:/data# redis-cli -h redis -p 6379
redis:6379> ping
PONG
redis:6379> set "abc" 123
OK
redis:6379> get "abc"
"123"
```

コンテナ間の共有できるものとして、ボリュームがある

```
vagrant@vagrant-ubuntu-trusty-64:~/docker/cowsay$ docker run --rm --volumes-from myredis -v $(pwd)/backup:/backup debian cp /data/dump.rdb /backup
vagrant@vagrant-ubuntu-trusty-64:~/docker/cowsay$ ls backup
dump.rdb
```

# 4章 Dockerの基礎

## 4.1 Dockerのアーキテクチャ

### 4.1.1 基盤の技術
Dockerデーモンはruncドライバでコンテナを作成する。
runcは、カーネルのcgroupsとnamespacesと密接にかかわっている。

UFS

### 4.1.2 周辺の技術
* swarm：Dockerのクラスタリングソリューション。複数のDockerホストをまとめてくれる。
* Compose：複数のDockerコンテナから合成されるアプリケーションの構築と実行のためのツール
* Machine：Dockerホストのインストールをする
* Kitematic：Dockerコンテナの実行管理のためのGUI
* Docker Trusted Registry：ローカル版のDocker Hub


各分野のソリューション
* ネットワーキング：Weave、Project Calico、Overlay
* サービスディスカバリ：Consul、Registrator、SkyDNS、etcd
* オーケストレーションおよびクラスタ管理：Kubernetes、Marathon、Fleet

### 4.1.3 Dockerのホスティング


## 4.2 イメージの構築

### 4.2.1 ビルドコンテキスト
通常はDockerfileのあるパス

### 4.2.2 イメージのレイヤ

```
vagrant@vagrant-ubuntu-trusty-64:~/docker/cowsay$ docker build -t  echotest .
Sending build context to Docker daemon  6.144kB
Step 1/3 : FROM busybox:latest
latest: Pulling from library/busybox
8c5a7da1afbc: Pull complete
Digest: sha256:cb63aa0641a885f54de20f61d152187419e8f6b159ed11a251a09d115fdff9bd
Status: Downloaded newer image for busybox:latest
 ---> e1ddd7948a1c
Step 2/3 : RUN echo "This should work"
 ---> Running in 5297bf71b6ad
This should work
Removing intermediate container 5297bf71b6ad
 ---> d55030ebe553
Step 3/3 : RUN /bin/bash -c echo "This won't"
 ---> Running in 9bfb46b582af
/bin/sh: /bin/bash: not found
The command '/bin/sh -c /bin/bash -c echo "This won't"' returned a non-zero code: 127
```

### 4.2.3 キャッシュ


### 4.2.4 ベースイメージ

### 4.2.5 Dockerfileの命令

## 4.3 外界とのコンテナの接続
ホストマシンのポートとコンテナのポートの結び付けを行う。

## 4.4　

# 5章 開発でのDockerの利用

文字列に応じてイメージを作成するWebアプリをDocker上で作る。

## 5.1 "Hello World"
python、Flaskを使う。
https://github.com/using-docker/using_docker_in_dev
からソースコード等落とせる。

sed -i -e "s/Docker/World/" app/identidock.py

uWSGIのバージョンは2.0.13にしたら動いた。

docker run -d -p 9090:9090 -p 9191:9191 identidock

Dockerfile内でユーザは必ず設定すべし。さもなくば、すべてコンテナ内でrootとして実行されてしまう。

# 6章 シンプルなWebアプリケーションの作成

## 基本的なWebページの作成










