# 概要

Kubernetes の Pod のヘルスチェックについて、

* Kubernetes の Liveness Probe・Readiness Probe
* Spring Boot Actuator

を用いて実施してみます。
おおむね[この記事](https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps)の翻訳となります。


# Kubernetesによるヘルスチェック

Kubernetes では Liveness Probe と Readiness Probe という2種のヘルスチェックがあります。
これらのヘルスチェックを駆使して、アプリケーションのダウンタイムを極力小さくするようにしています。

Liveness Probe と Readiness Probe ではヘルスチェックで問題があった場合の挙動が異なります。
Liveness Probe で問題を検知した場合には、コンテナの再起動をします。
一方、Readiness Probe で問題を検知した場合には、該当の Pod にはリクエストが送られないようになります。

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

* tcpSocket : ヘルスチェック方法として、TCP接続ができるかどうかで判断しているということを表す
* tcpSocket.port : ヘルスチェックとしてTCP接続しにいくポート番号
* initialDelaySeconds : コンテナが作成されてから、ヘルスチェックを開始するまでに待機する秒数
* periodSeconds : ヘルスチェックを実施する間隔。デフォルトは10sで最小値は1s
* timeoutSeconds : ヘルスチェックがタイムアウトとなる秒数。デフォルトは1sで最小値は1s
* failureThreshold : ヘルスチェック失敗とみなすまでに施行する回数。Readiness の場合は Pod が not ready となる。Liveness の場合は Pod を再起動する。デフォルトは3回で、最小値は1回
* successThreshold : ヘルスチェックが失敗した後に成功したと見なされるための最小連続成功回数。デフォルトは1回で最小値は1回

## レイヤ7でヘルスチェック

Kubernetesでは、以下3種類のヘルスチェック方法が用意されています。

* exec : コンテナ内でbashスクリプトを実施し、エラーコードを返したら失敗とみなす
* tcpSocket : 指定されたポートに対してTCP接続を確立できるか確かめ、確立できなければ失敗とみなす(上記はこれです)
* httpGet : コンテナ上で動いているサーバーに対してHTTPのGETリクエストを送信し、200以上400未満のレスポンスが返れば成功とみなす

httpGet によるヘルスチェックではさらに以下のようなフィールドが加わります。

* host : 接続先ホスト名。デフォルトは自身のPodのIP
* scheme : 接続に使われるプロトコル。HTTPかHTTPS。デフォルトはHTTP
* path : Webサーバーにアクセスする際のパス
* httpHeaders : リクエストの中に含めるパス
* port : アクセスする際のポート

扱うコンテナがWebサーバーである場合には、TCPよりもHTTPを使用したヘルスチェックのほうが信頼できる結果を得られます。

レイヤ7でのヘルスチェックを行うにおいては、HTTPのGETを受け付けるエンドポイントが必要となります。
Spring Boot Actuator を使用すれば簡単にヘルスチェック用のエンドポイントを用意することができます。

# Spring Boot Actuatorについて

Spring Boot Actuator を用いることで、監査・ヘルスチェック・メトリクス収集のためのエンドポイントをアプリケーションに組み込むことができます。
今回はヘルスチェックの用途で使用します。

Spring Boot Actuator を導入する方法は、Mavenで依存関係を制御しているのであれば、dependencyに下記を加えるだけです。

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

導入することによって、サーバーの状態をエンドポイント`/actuator/health`で確認することができるようになります。

サーバーが生きている場合は以下のような通信を行います。

```
$ curl 192.168.99.100:8080/actuator/health -v
* Expire in 0 ms for 6 (transfer 0x66aab0)
* Uses proxy env variable no_proxy == '192.168.99.100,192.168.99.101'
*   Trying 192.168.99.100...
* TCP_NODELAY set
* Expire in 200 ms for 4 (transfer 0x66aab0)
* Connected to 192.168.99.100 (192.168.99.100) port 8080 (#0)
> GET /actuator/health HTTP/1.1
> Host: 192.168.99.100:8080
> User-Agent: curl/7.64.0
> Accept: */*
>
< HTTP/1.1 200
< Content-Type: application/vnd.spring-boot.actuator.v2+json;charset=UTF-8
< Transfer-Encoding: chunked
< Date: Wed, 10 Jul 2019 11:56:47 GMT
<
{"status":"UP"}
```


落ちている場合は以下のようになります。

```
$ curl 192.168.99.100:8080/actuator/health -v
* Expire in 0 ms for 6 (transfer 0x73aab0)
* Uses proxy env variable no_proxy == '192.168.99.100,192.168.99.101'
*   Trying 192.168.99.100...
* TCP_NODELAY set
* Expire in 200 ms for 4 (transfer 0x73aab0)
* Connected to 192.168.99.100 (192.168.99.100) port 8080 (#0)
> GET /actuator/health HTTP/1.1
> Host: 192.168.99.100:8080
> User-Agent: curl/7.64.0
> Accept: */*
>
< HTTP/1.1 503
< Content-Type: application/vnd.spring-boot.actuator.v2+json;charset=UTF-8
< Transfer-Encoding: chunked
< Date: Wed, 10 Jul 2019 11:47:47 GMT
< Connection: close
<
{"status":"DOWN"}
```

# Liveness Probe

意図的に Liveness Probe が失敗するような状況を作り、コンテナが再作成されることを確認します。

以下のようなクラスを作成し、アプリケーションの起動から30秒まではヘルスチェックに200を返し、30秒経った後は503を返すようにします。

```
@Component
public class CustomHealthIndicator implements HealthIndicator {
 
    private boolean isHealthy = true;
 
    public CustomHealthIndicator() {
        ScheduledExecutorService scheduled =
          Executors.newSingleThreadScheduledExecutor();
        scheduled.schedule(() -> {
            isHealthy = false;
        }, 30, TimeUnit.SECONDS);
    }
 
    @Override
    public Health health() {
        return isHealthy ? Health.up().build() : Health.down().build();
    }
}
```

Podの設定は以下のようにします。
Readiness Probe のヘルスチェックはコンテナ作成の10秒後から3秒間隔で実施され、
Liveness Probe のヘルスチェックはコンテナ作成の20秒後から8秒間隔で実施されます。

```
apiVersion: v1
kind: Pod
metadata:
  name: liveness-probe
  labels:
    app: liveness-probe
spec:
  containers:
    - name: liveness-probe
      image: nannany/liveness-probe-example:latest
      readinessProbe:
        httpGet:
          path: /actuator/health
          port: 8080
        initialDelaySeconds: 10
        timeoutSeconds: 2
        periodSeconds: 3
        failureThreshold: 1
      livenessProbe:
        httpGet:
          path: /actuator/health
          port: 8080
        initialDelaySeconds: 20
        timeoutSeconds: 2
        periodSeconds: 8
        failureThreshold: 1
```

`kubectl describe pod liveness-probe` を実行して出力した情報の Events を確認すると以下のようになっており、Readiness Probe に失敗した後に、Liveness Probe に失敗し、コンテナが再作成されていることが分かります。

```
Warning  Unhealthy  7s (x2 over 10s)  kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Readiness probe failed: HTTP probe failed with statuscode: 503
Normal   Pulling    5s (x2 over 52s)  kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  pulling image "nannany/liveness-probe-example:latest"
Warning  Unhealthy  5s                kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Liveness probe failed: HTTP probe failed with statuscode: 503
Normal   Killing    5s                kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Killing container with id docker://liveness-probe:Container failed liveness probe.. Container will be killed and recreated.
Normal   Pulled     2s (x2 over 49s)  kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Successfully pulled image "nannany/liveness-probe-example:latest"
Normal   Created    2s (x2 over 49s)  kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Created container
Normal   Started    2s (x2 over 49s)  kubelet, gke-standard-cluster-1-default-pool-1623186d-sfjm  Started container
```

# Readiness Probe

以下のようなクラスを作成し、アプリケーションの起動から40秒まではヘルスチェックに503を返し、40秒経った後は200を返すようにします。

```
@Component
public class CustomHealthIndicator implements HealthIndicator {

    private boolean isHealthy = false;

    public CustomHealthIndicator() {
        ScheduledExecutorService scheduled =
                Executors.newSingleThreadScheduledExecutor();
        scheduled.schedule(() -> {
            isHealthy = true;
        }, 40, TimeUnit.SECONDS);
    }

    @Override
    public Health health() {
        return isHealthy ? Health.up().build() : Health.down().build();
    }

}
```

Podの設定は以下のようにします。
Readiness Probe のヘルスチェックはコンテナ作成の40秒後から3秒間隔で実施され、
Liveness Probe のヘルスチェックはコンテナ作成の100秒後から8秒間隔で実施されます。

```
apiVersion: v1
kind: Pod
metadata:
  name: readiness-probe
  labels:
    app: readiness-probe
spec:
  containers:
    - name: readiness-probe
      image: nannany/readiness-probe-example:latest
      readinessProbe:
        httpGet:
          path: /actuator/health
          port: 8080
        initialDelaySeconds: 40
        timeoutSeconds: 2
        periodSeconds: 3
        failureThreshold: 2
      livenessProbe:
        httpGet:
          path: /actuator/health
          port: 8080
        initialDelaySeconds: 100
        timeoutSeconds: 2
        periodSeconds: 8
        failureThreshold: 1
```

Readiness Probe の失敗が数回起きていることが分かります。コンテナ起動から Spring が立ち上がるまでにタイムラグがあるためだと考えられます。

```
  Normal   Pulled     110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Successfully pulled image "nannany/readiness-probe-example:latest"
  Normal   Created    110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Created container
  Normal   Started    110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Started container
  Warning  Unhealthy  63s (x3 over 68s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Readiness probe failed: HTTP probe failed with statuscode: 503
```

# まとめ

本記事では Kubernetes のヘルスチェック機能と Spring Boot Actuator を使用してアプリケーションのヘルスチェックチェックを行いました。
使用したソースコード、YAMLファイルは下記に配置しています。
https://github.com/nannany/spring-actuator-sample


# 参考URL

https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps
https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html
