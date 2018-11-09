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

Dockerfileいじったdocker-compose build をする。

# 7章 イメージの配布

~/work/20180924でいろいろやる
## 7.5 イメージサイズの削減
一行でいろいろやったほうがイメージサイズの削減ができる。

本当に追い込まれている状況、で説明されている内容良くわからず。

# 8章 Dockerを使った継続的インテグレーションとテスト
docker run -d --name jenkins -p 8080:8080 --volumes-from jenkins-data -v /var/run/docker.sock:/var/run/docker.sock identijenk

# 9章
curl -L https://github.com/docker/machine/releases/download/v0.15.0/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
    chmod +x /tmp/docker-machine &&
    sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
を実行してdocker-machineをインストール。

## 9.1 Docker Machineを使ったリソースのプロビジョニング
docker-machine create --driver digitalocean --digitalocean-access-token ... identihost-do

作業が終わったらホストマシンは削除する。

実働環境では動作させるコンテナのバージョンに注意する。

docker-compose の指定ymlファイルをCOMPOSE_FILEで指定しているが、うまく行かない。
-fで指定してやるとうまくいく。

docker run -it コンテナ /bin/bash
でコンテナの中身見れる。

curl $(docker-machine ip identihost-do)

## 9.3 実行オプション

### 9.3.1 シェルスクリプト
docker-machine scp deploy.sh identihost-do:~/deploy.sh
docker-machine ssh identihost-do

chmod +x deploy.sh
./deploy.sh
### 9.3.2 プロセスマネージャの利用（もしくはsystemdでまとめて管理）

### 9.3.3 設定管理ツールの利用
Ansibleの使用
docker run -it -v ${HOME/.ssh:/root/.ssh:ro} -v $(pwd)/identidock.yml:/ansible/identidock.yml -v $(pwd)/hosts:/etc/ansible/hosts --rm=true generik/ansible ansible-playbook identidock.yml


## 9.4 ホストの設定
DigitalOceanでは設定済みのVMを提供してくれる（ドロップレット）が、ホストOSとインフラには多様な選択肢がある。

### 9.4.1 OSの選択
小規模ならUbuntu、Fedoraで良い。
大規模ならCoreOS、ProjectAtomicなどを用いる。

### 9.4.2 ストレージドライバの選択
AUFS、Overlay、BTRFS、ZFS、Device mapper、VFSがありえる。
筆者のおすすめはAUFSかOverlay。

## 9.5 専門のホスティングの選択肢

### 9.5.1 Trition
内部でVMを使っていない。そのため性能が良い。

### 9.5.2 Google Container Engine
Kubernetes上に構築されたホスティングシステム。
筆者的には一押し。

### 9.5.3 Amazon EC2 Container Service

### 9.5.4 Giant Swarm

## 9.6 永続化データとプロダクションコンテナ

## 9.7 秘密情報の共有

### 9.7.1 秘密情報のイメージへの保存
これはやってはいけない。
イメージにアクセスできる人なら誰でも秘密情報にアクセスできるようになる。

### 9.7.2 環境変数での秘密情報の受け渡し
やるべきでない。
* すべての子プロセスから見えてしまう。
* 環境は保存されることが多い。環境変数がデバッグログ等に出てしまうのがリスク。
* 環境変数は削除できない。

### 9.7.3 ボリュームでの秘密情報の受け渡し
微妙。オペミスでバージョン管理システムにコミットされる可能性がある。

### 9.7.4 キーバリューストアの利用
一番良い。
KeyWhiz、Vault、Cryptがある。

## 9.8 ネットワーキング
11章へ。
Dockerのネットワーク機能をそのまま使っているとしたら非常に低速。

## 9.9 プロダクションレジストリ
レジストリ内のイメージを最新かつ適正に保つことは重要。

## 9.10 継続的デプロイメント/デリバリ

## 9.11 まとめ


# 10章 ロギングとモニタリング

## 10.1 ロギング

### 10.1.1 Dockerでのデフォルトのロギング
docker run --name logtest debian sh -c 'echo "stdout"; echo "stderr" >>2'

docker logs -t logtest

docker run -d --name streamtest debian sh -c 'while true; do echo "tick"; sleep 1; done;'

消す場合
docker rm $(docker ps -aq)

docker logs -f streamtest

ログドライバは複数ある。
json-file、syslog、journald、gelf、fluentd、none

### 10.1.2 ログの集約

### 10.1.3 ELKを使ったロギング

### 10.1.4 syslogを使ったDockerのロギング
ID=$(docker run -d --log-driver=syslog debian sh -c 'i=0; while true; do i=$((i+1)); echo "docker $i"; sleep 1; done;')

## 10.2 rsyslogへのログのフォワード

### 10.2.1 ファイルからのログの取得

## 10.3 モニタリングとアラート

### 10.3.1 Dockerのツールでのモニタリング
docker stats
docker statsで取得できる値はAPIで取れるけど割と使いづらい。
runcやカーネルコールを直接行ってメトリクスを得ることもできる。

statd, influxDB, OpenTSDB, Graphite, Grafanaと言ったツールがある。

### 10.3.2 cAdvisor
docker run -d --name cadvisor -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys:ro -v /var/lib/docker/:/var/lib/docker:ro -p 8080:8080 google/cadvisor:latest

### 10.3.3 クラスタのソリューション
Prometheus

docker run -d --name prometheus -p 9090:9090 -v $(pwd)/prometheus.conf:/prometheus.conf --link cadvisor:cadvisor prom/prometheus -config.file=/prometheus.conf

## 10.4 モニタリング及びロギングの商用ソリューション
たくさんあるので要チェック

## 10.5 まとめ


# 三部 ツールとテクニック

# 11章 ネットワーキングとサービスディスカバリ

## 11.1 アンバサダー

* virtualBoxをインストール
以下を/etc/apt/sources.list に加える。
deb https://download.virtualbox.org/virtualbox/debian wheezy contrib
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
sudo apt-get update
sudo apt-get install virtualbox-5.2

virtualboxの使用は諦める。。。

プロビジョニング
docker-machine create --driver digitalocean --digitalocean-access-token ~~~~~ redis-host
docker-machine create --driver digitalocean --digitalocean-access-token ~~~~~ identidock-host

レディスが動くサーバを対象にする。
eval $(docker-machine env redis-host)

docker run -d --name real-redis redis:3

docker run -d --name real-redis-ambassador \
       -p 6379:6379 \
       --link real-redis:real-redis \
       amouat/ambassador

レディスが動くサーバを対象にする。
eval $(docker-machine env identidock-host)

docker run -d --name redis_ambassador --expose 6379 \
       -e REDIS_PORT_6379_TCP=tcp://$(docker-machine ip redis-host):6379 \
       amouat/ambassador

docker run -d --name dnmonster amouat/dnmonster:1.0

docker run -d --link dnmonster:dnmonster \
           --link redis_ambassador:redis \
           -p 80:9090 \
           amouat/identidock:1.0

確認コマンド
curl $(docker-machine ip identidock-host)

後処理
docker-machine stop redis-host
docker-machine stop identidock-host
docker-machine rm redis-host
docker-machine rm identidock-host

## 11.2 サービスディスカバリ

### 11.2.1 etcd
Docker Machineで新しいホスト

プロビジョニング
docker-machine create -d digitalocean --digitalocean-access-token ~~~ etcd-1
docker-machine create -d digitalocean --digitalocean-access-token ~~~ etcd-2


HOSTA=$(docker-machine ip etcd-1)
HOSTB=$(docker-machine ip etcd-2)

1番目のVM
eval $(docker-machine env etcd-1)

docker run -d -p 2379:2379 -p 2380:2380 -p 4001:4001 \
--name etcd quay.io/coreos/etcd:v2.2.0 \
-name etcd-1 -initial-advertise-peer-urls http://${HOSTA}:2380 \
-listen-peer-urls http://0.0.0.0:2380 \
-listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
-advertise-client-urls http://${HOSTA}:2379 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster \
    etcd-1=http://${HOSTA}:2380,etcd-2=http://${HOSTB}:2380 \
-initial-cluster-state new


2番目のVM
eval $(docker-machine env etcd-2)

docker run -d -p 2379:2379 -p 2380:2380 -p 4001:4001 \
--name etcd quay.io/coreos/etcd:v2.2.0 \
-name etcd-2 -initial-advertise-peer-urls http://${HOSTB}:2380 \
-listen-peer-urls http://0.0.0.0:2380 \
-listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
-advertise-client-urls http://${HOSTA}:2379 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster \
    etcd-1=http://${HOSTA}:2380,etcd-2=http://${HOSTB}:2380 \
-initial-cluster-state new

メンバーのリストを返してもらうcurl。

curl -s http://$HOSTA:2379/v2/members | jq '.'

キーバリューストアに登録するcurl

curl -s http://$HOSTA:2379/v2/keys/service_name -XPUT -d value="service_address" | jq '.'

保存したデータを取得しなおすcurl
curl -s http://$HOSTA:2379/v2/keys/service_name | jq '.'


etcdctlというコマンドラインクライアントでetcdクラスタとやり取りできる

docker run binocarlos/etcdctl -C ${HOSTB}:2379 get service_name

### 11.2.2 SkyDNS
kubernetesのサービスディスカバリで使われている。

etcdにSkyDNSの設定をする。起動時に行う処理を知らせる。
curl -XPUT http://${HOSTA}:2379/v2/keys/skydns/config -d value='{"dns_addr":"0.0.0.0:53", "domain":"identidock.local."}' | jq .

etcd-1上でskydnsを立ち上げる。

eval $(docker-machine env etcd-1)
docker run -d -e ETCD_MACHINES="http://${HOSTA}:2379,http://${HOSTB}:2379" --name dns skynetservices/skydns:2.5.2a

etcd-2上でredisを立ち上げる。それをSkyDNSに追加する。

eval $(docker-machine env etcd-2)

docker run -d -p 6379:6379 --name redis redis:3

curl -XPUT http://${HOSTA}:2379/v2/keys/skydns/local/identidock/redis -d value='{"host":"'$HOSTB'","port":6379}' | jq .

etcd-1で--dnsを使って、ルックアップするDNSコンテナを指定し、新しいコンテナを立ち上げる。

eval $(docker-machine env etcd-1)

docker run --dns $(docker inspect -f {{.NetworkSettings.IPAddress}} dns) -it redis:3 bash

pingを投げてテスト
どうやらサーバ内にpingがないようなので、
apt-get update
apt-get install iputils-ping net-tools
をしてやる必要がある。

ping redis.identidock.local

redis-cli -h redis.identidock.local ping


検索ドメインにidentidockを追加
docker run --dns $(docker inspect -f {{.NetworkSettings.IPAddress}} dns) --dns-search identidock.local -it redis:3 redis-cli -h redis ping

サーバetcd-1に入り、/etc/resolv.confファイルに追記
docker-machine ssh etcd-1

echo -e "domain identidock.local \nnameserver " $(docker inspect -f {{.NetworkSettings.IPAddress}} dns) > /etc/resolv.conf

cat /etc/resolv.conf

動作させる
docker run redis:3 redis-cli -h redis ping

docker run -d --name dnmonster amouat/dnmonster:1.0

DNM_IP=$(docker inspect -f {{.NetworkSettings.IPAddress}} dnmonster)

curl -XPUT http://$HOSTA:2379/v2/keys/sykdns/local/identidock/dnmonster -d value='{"host": "'$DNM_IP'","port":8080'}

docker run -d -p 80:9090 amouat/identidock:1.0
curl $HOSTA


11.2.3 Consul
プロビジョニング
docker-machine create -d digitalocean --digitalocean-access-token ~~~~ consul-1
docker-machine create -d digitalocean --digitalocean-access-token ~~~~ consul-2

HOSTA=$(docker-machine ip consul-1)
HOSTB=$(docker-machine ip consul-2)

eval $(docker-machine env consul-1)

docker run -d --name consul -h consul-1 \
       -p 8300:8300 -p 8301:8301 -p 8301:8301/udp \
       -p 8302:8302/udp -p 8400:8400 -p 8500:8500 \
       -p 172.17.0.1:53:8600/udp \
       gliderlabs/consul agent -data-dir /data -server \
                  -client 0.0.0.0 \
                  -advertise $HOSTA -bootstrap-expect 2

２つめのサーバを立ち上げる。
eval $(docker-machine env consul-2)

docker run -d --name consul -h consul-2 \
       -p 8300:8300 -p 8301:8301 -p 8301:8301/udp \
       -p 8302:8302/udp -p 8400:8400 -p 8500:8500 \
       -p 172.17.0.1:53:8600/udp \
       gliderlabs/consul agent -data-dir /data -server \
                  -client 0.0.0.0 \
                  -advertise $HOSTB -join $HOSTA

クラスタに加わったことを確認
docker exec consul consul members
キ/ーバリューストアの動作確認
curl -XPUT http://$HOSTA:8500/v1/kv/loo -d bar
curl http://$HOSTA:8500/v1/kv/foo | jq .

curl -s http://$HOSTA:8500/v1/kv/foo | jq -r '.[].Value' | base64 -d


eval $(docker-machine env consul-2)

docker run -d -p 6379:6379 --name redis redis:3
curl -XPUT http://$HOSTA:8500/v1/agent/service/register -d '{"name":"redis", "address":"'$HOSTB'","port":6379}'
docker run amouat/network-utils dig @172.17.0.1 +short redis.service.consul

サーバ内のファイルを編集
docker-machine ssh consul-1
/var/lib/boot2docker/profileに--dns、 --dns-searchフラグを追加する。

### 11.2.4 登録
GliderLabsのRegistratorはコンテナの自動登録機能を提供する。

### 11.2.5 その他のソリューション

#### ZooKeeper
Javaで書かれている。
主な利点は成熟度、安定度、現場での活用例の多さ。

#### SmartStack

#### Eureka

#### WeaveDNS

#### docker-discover

## 11.3 ネットワーキングの選択肢
デフォルトのDockerのネットワーキングの選択肢を見ていく。

### 11.3.1 ブリッジ
開発時に最適。実働環境には向かない。

### 11.3.2 ホスト

### 11.3.3 コンテナ
kubernetesが使っている方法。

### 11.3.4 なし

## 11.4 Dockerの新しいネットワーキング

docker network ls

以下のコマンドは動かなくなっている。docker swarm init なるものを実行しないと動かないらしい。。。
docker run -d --name redis1 --net=bridge db.bridge redis

## 11.5 ネットワーキングのソリューション

### 11.5.1 Overlay

docker公式にいいのがある。

### 11.5.2 Weave

docker-machine create -d digitalocean --digitalocean-access-token ~~~ weave-redis

docker-machine ssh weave-redis

sudo curl -sL git.io/weave -o /usr/local/bin/weave
sudo chmod a+x /usr/local/bin/weave
weave launch

どっかークライアントがweaveproxyを指すようにする
eval $(weave env)
docker run --name redis -d redis:3

docker-machine create -d digitalocean --digitalocean-access-token ~~~ weave-identidock

docker-machine ssh weave-identidock "sudo curl -sL https://git.io/weave -o /usr/local/bin/weave && sudo chmod a+x /usr/local/bin/weave"

docker-machine ssh weave-identidock "weave launch $(docker-machine ip weave-redis)"

あとのコマンドも書いてあるとおりにやればうまく行く。

### 11.5.3 Flannel
docker-machine create -d digitalocean --digitalocean-access-token ~~~ flannel-1
docker-machine create -d digitalocean --digitalocean-access-token ~~~ flannel-2

docker-machine ip flannel-1 flannel-2

docker-machine ssh flannel-1
sudo /usr/local/etc/init.d/docker stop
sudo ip link delete docker0

curl -sL https://github.com/coreos/etcd/releases/download/v2.0.13/etcd-v2.0.13-linux-amd64.tar.gz -o etcd.tar.gz

tar xzvf etcd.tar.gz

HOSTA=159.65.42.249
HOSTB=165.227.66.248

nohup etcd-v2.0.13-linux-amd64/etcd \
  -name etcd-1 -initial-advertise-peer-urls http://$HOSTA:2380 \
  -listen-peer-urls http://$HOSTA:2380 \
  -listen-client-urls http://$HOSTA:2370,http://127.0.0.1:2379 \
  -advertise-client-urls http://$HOSTA:2379 \
  -initial-cluster-token etcd-cluster-1 \
  -initial-cluster \
etcd-1=http://$HOSTA:2380,etcd-2=http://$HOSTB:2380 \
  -initial-cluster-state new &

もうひとつのサーバでも同じようなことをやる


docker-machine ssh flannel-2
sudo /usr/local/etc/init.d/docker stop
sudo ip link delete docker0

curl -sL https://github.com/coreos/etcd/releases/download/v2.0.13/etcd-v2.0.13-linux-amd64.tar.gz -o etcd.tar.gz

tar xzvf etcd.tar.gz

HOSTA=159.65.42.249
HOSTB=165.227.66.248

nohup etcd-v2.0.13-linux-amd64/etcd \
  -name etcd-2 -initial-advertise-peer-urls http://$HOSTB:2380 \
  -listen-peer-urls http://$HOSTB:2380 \
  -listen-client-urls http://$HOSTB:2370,http://127.0.0.1:2379 \
  -advertise-client-urls http://$HOSTB:2379 \
  -initial-cluster-token etcd-cluster-1 \
  -initial-cluster \
etcd-1=http://$HOSTA:2380,etcd-2=http://$HOSTB:2380 \
  -initial-cluster-state new &


curl -sL https://github.com/coreos/flannel/releases/download/v0.5.1/flannel-0.5.1-linux-amd64.tar.gz -o flannel.tar.gz

tar xzvf flannel.tar.gz

./etcd-v2.0.13-linux-amd64/etcdctl set /coreos.com/network/config '{ "Network": "10.1.0.0/16" }'
上のコマンドがうまくいかない。。

### 11.5.4 Calico
docker-machine create -d digitalocean --digitalocean-access-token=~~~  --digitalocean-private-networking calico-1
docker-machine create -d digitalocean --digitalocean-access-token=~~~  --digitalocean-private-networking calico-2

HOSTA=159.203.161.184
HOSTB=45.55.51.113

eval $(docker-machine env calico-1)
docker run -d -p 2379:2379 -p 2380:2380 -p 4001:4001 \
--name etcd quay.io/coreos/etcd:v2.2.0 \
-name etcd-1 -initial-advertise-peer-urls http://${HOSTA}:2380 \
-listen-peer-urls http://0.0.0.0:2380 \
-listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
-advertise-client-urls http://${HOSTA}:2379 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster \
etcd-1=http://${HOSTA}:2380,etcd-2=http://${HOSTB}:2380 \
-initial-cluster-state new 


eval $(docker-machine env calico-2)
docker run -d -p 2379:2379 -p 2380:2380 -p 4001:4001 \
--name etcd quay.io/coreos/etcd:v2.2.0 \
-name etcd-2 -initial-advertise-peer-urls http://${HOSTB}:2380 \
-listen-peer-urls http://0.0.0.0:2380 \
-listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
-advertise-client-urls http://${HOSTB}:2379 \
-initial-cluster-token etcd-cluster-1 \
-initial-cluster \
etcd-1=http://${HOSTA}:2380,etcd-2=http://${HOSTB}:2380 \
-initial-cluster-state new 


docker-machine ssh calico-1
curl -sSL -o calicoctl https://github.com/Metaswitch/calico-docker/releases/download/v0.5.2/calicoctl
chmod +x calicoctl

modprobe xt_set

sudo ./calicoctl pool add 192.168.0.0/16 --ipip --nat-outgoing

sudo ./calicoctl node --ip=159.203.161.184
上のコマンド動かない。。

# 12章

## 12.1.1 Swarm
SWARM_TOKEN=$(docker run swarm create)
echo $SWARM_TOKEN
しょっぱなからうまくいかない。

フィルタの設定と実行戦略の設定ができるらしい

## 12.1.2 fleet
バーチャルボックスのバージョンが合わないため撤退

## 12.1.3 Kubernetes

* ポッドという、１～５個位のコンテナ単位で構成される。ポッドは短命なものとして扱われる。
* 単一ポッド内でのネットワーキングは少しトリッキー
* ポッドにラベルを付けて管理する
* 名前でアクセスできるエンドポイントをサービスという。これを使ってアプリケーションからアクセスすることができる。

