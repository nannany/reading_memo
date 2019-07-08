# 概要

KubernetesのPodの死活監視について、

* KubernetesのLiveness・Readiness
* Spring Boot Actuator
を用いて実施してみます。
おおむね[本記事](https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps)の翻訳となります。


# Spring Boot Actuatorについて

Spring Boot Actuatorを使用すれば、監査・死活監視・メトリクス収集のためのエンドポイントをアプリケーションの中に容易に組み込むことができます。

# Kubernetesによるヘルスチェック

Kubernetesでは Liveness Probe と Readiness Probe という2種のヘルスチェックがあります。
これらのヘルスチェックを駆使して、アプリケーションのダウンタイムを極力小さくするようにしています。

各ヘルスチェックの内容はマニフェストファイルにて設定することができます。
Liveness Probe と Readiness Probe ではヘルスチェックで問題があった場合の挙動が異なります。

Liveness Probe で問題を検知した場合には、コンテナの再起動をします。
一方、Readiness Probe で問題を検知した場合には、該当のPodにはリクエストが送られないようになります。

## レイヤ4での設定

以下のマニフェストは、Liveness Probe、Readiness Probe でトランスポート層のヘルスチェックをしている例です。

```
apiVersion: v1
kind: Pod
metadata:
  name: goproxy
  labels:
    app: goproxy
spec:
  containers:
  - name: goproxy
    image: k8s.gcr.io/goproxy:0.1
    ports:
    - containerPort: 8080
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 2
      failureThreshold: 1
      successThreshold: 1
    livenessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 15
      periodSeconds: 20
      timeoutSeconds: 2
      failureThreshold: 1
      successThreshold: 1
```

ヘルスチェックについて、設定している各フィールドの意味は以下のようです。

* initialDelaySeconds : コンテナが作成されてから、ヘルスチェックを開始するまでに待機する秒数
* periodSeconds : ヘルスチェックを実施する間隔。デフォルトは10sで最小値は1s
* timeoutSeconds : ヘルスチェックがタイムアウトとなる秒数。デフォルトは1sで最小値は1s
* failureThreshold : ヘルスチェック失敗とみなすまでに施行する回数。readiness の場合はPodが not ready となる。liveness の場合はPodを再起動する。デフォルトは3回で、最小値は1回
* successThreshold : ヘルスチェックが失敗した後に成功したと見なされるための最小連続成功回数。デフォルトは1回で最小値は1回

## レイヤ7でヘルスチェック

扱うコンテナがWebサーバーである場合には、TCPよりもHTTPを使用したヘルスチェックのほうが信頼できる結果を得られます。

Kubernetesでは、以下3種類のヘルスチェック方法が用意されています。

* exec : コンテナ内でbashスクリプトを実施し、エラーコードを返したら失敗とみなす
* tcpSocket : 指定されたポートに対してTCP接続を確立できるか確かめ、確立できなければ失敗とみなす(上記はこれ)
* httpGet : コンテナ上で動いているサーバーに対してHTTPのGETリクエストを送信し、200以上400未満のレスポンスが返れば成功とみなす

httpGet によるヘルスチェックではさらに以下のようなフィールドが加わります。

* host : 接続先ホスト名。デフォルトは自身のPodのIP
* scheme : 接続に使われるプロトコル。HTTPかHTTPS。デフォルトはHTTP
* path : Webサーバーにアクセスする際のパス
* httpHeaders : リクエストの中に含めるパス
* port : アクセスする際のポート

レイヤ7でのヘルスチェックをおこｎ


# 参考URL

https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps

-- 
Spring boot actuator でデフォルトで設定できるのはHTTP通信だと、

* health
* info

のみ。
