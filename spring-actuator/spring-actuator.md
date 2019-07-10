# 概要

KubernetesのPodの死活監視について、

* KubernetesのLiveness・Readiness
* Spring Boot Actuator
を用いて実施してみます。
おおむね[この記事](https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps)の翻訳となります。


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

つまり、上記のマニフェストにおいて、Readiness Probe は、コンテナ作成から5s後に、10秒間隔でTCPの8080に接続できるかチェックし、
2秒で接続できなかったらタイムアウトとみなし、ヘルスチェックが1回失敗したらPodを not ready にし、失敗後に1回成功したら ready にする、
というようなことをします。

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

Spring Boot Actuator を用いることで、監査・死活監視・メトリクス収集のためのエンドポイントをアプリケーションに組み込むことができます。
今回は死活監視の用途で使用します。

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

意図的にLiveness Probe が失敗するような状況を作り、コンテナが再作成されることを確認します。

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

```
Normal   Created    75s (x3 over 2m46s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Created container
Normal   Started    75s (x3 over 2m46s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Started container
Warning  Unhealthy  33s (x4 over 84s)    kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Readiness probe failed: HTTP probe failed with statuscode: 503
Normal   Pulling    30s (x4 over 3m3s)   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  pulling image "nannany/liveness-probe-example:latest"
Warning  Unhealthy  30s (x3 over 2m6s)   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Liveness probe failed: HTTP probe failed with statuscode: 503
Normal   Killing    30s (x3 over 2m6s)   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Killing container with id docker://liveness-probe:Container failed liveness probe.. Container will be killed and recreated.
Normal   Pulled     27s (x4 over 2m50s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Successfully pulled image "nannany/liveness-probe-example:latest"
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


```
Events:
  Type     Reason     Age                From                                                        Message
  ----     ------     ----               ----                                                        -------
  Normal   Scheduled  115s               default-scheduler                                           Successfully assigned default/readiness-probe to gke-standard-cluster-1-default-pool-b350d2ec-svw3
  Normal   Pulling    115s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  pulling image "nannany/readiness-probe-example:latest"
  Normal   Pulled     110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Successfully pulled image "nannany/readiness-probe-example:latest"
  Normal   Created    110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Created container
  Normal   Started    110s               kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Started container
  Warning  Unhealthy  63s (x3 over 68s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Readiness probe failed: HTTP probe failed with statuscode: 503
```

# 参考URL

https://www.baeldung.com/spring-boot-kubernetes-self-healing-apps
https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html

-- 

Spring boot actuator でデフォルトで設定できるのはHTTP通信だと、

* health
* info

のみ。


---

Name:         liveness-probe
Namespace:    default
Priority:     0
Node:         gke-standard-cluster-1-default-pool-b350d2ec-svw3/10.146.0.3
Start Time:   Wed, 10 Jul 2019 21:15:28 +0900
Labels:       app=liveness-probe
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"app":"liveness-probe"},"name":"liveness-probe","namespace":"defaul...
              kubernetes.io/limit-ranger: LimitRanger plugin set: cpu request for container liveness-probe
Status:       Running
IP:           10.0.1.7
Containers:
  liveness-probe:
    Container ID:   docker://f5f4f6e2eb4ab43fccf018590248a92279312eaab32d1153c0f5c9a5fb94007c
    Image:          nannany/liveness-probe-example:latest
    Image ID:       docker-pullable://nannany/liveness-probe-example@sha256:e8151a7fbb1d6c323b244d04b01526eadb0d51096338ca7a2e7f5935bb373d1d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Wed, 10 Jul 2019 21:18:37 +0900
    Last State:     Terminated
      Reason:       Error
      Exit Code:    143
      Started:      Wed, 10 Jul 2019 21:17:49 +0900
      Finished:     Wed, 10 Jul 2019 21:18:34 +0900
    Ready:          True
    Restart Count:  4
    Requests:
      cpu:        100m
    Liveness:     http-get http://:8080/actuator/health delay=20s timeout=2s period=8s #success=1 #failure=1
    Readiness:    http-get http://:8080/actuator/health delay=10s timeout=2s period=3s #success=1 #failure=1
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-rvgsx (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-rvgsx:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-rvgsx
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason     Age                    From                                                        Message
  ----     ------     ----                   ----                                                        -------
  Normal   Scheduled  3m47s                  default-scheduler                                           Successfully assigned default/liveness-probe to gke-standard-cluster-1-default-pool-b350d2ec-svw3
  Normal   Created    2m14s (x3 over 3m44s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Created container
  Normal   Started    2m14s (x3 over 3m43s)  kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Started container
  Normal   Pulling    89s (x4 over 3m47s)    kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  pulling image "nannany/liveness-probe-example:latest"
  Warning  Unhealthy  89s (x3 over 3m5s)     kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Liveness probe failed: HTTP probe failed with statuscode: 503
  Normal   Killing    89s (x3 over 3m5s)     kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Killing container with id docker://liveness-probe:Container failed liveness probe.. Container will be killed and recreated.
  Warning  Unhealthy  89s (x5 over 2m20s)    kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Readiness probe failed: HTTP probe failed with statuscode: 503
  Normal   Pulled     86s (x4 over 3m44s)    kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Successfully pulled image "nannany/liveness-probe-example:latest"

---
Name:         liveness-probe
Namespace:    default
Priority:     0
Node:         gke-standard-cluster-1-default-pool-b350d2ec-svw3/10.146.0.3
Start Time:   Wed, 10 Jul 2019 21:21:03 +0900
Labels:       app=liveness-probe
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"app":"liveness-probe"},"name":"liveness-probe","namespace":"defaul...
              kubernetes.io/limit-ranger: LimitRanger plugin set: cpu request for container liveness-probe
Status:       Running
IP:           10.0.1.8
Containers:
  liveness-probe:
    Container ID:   docker://60d512acdf9005759b85ab2b21af860376db03f5bc218258bbb81ca0bf622269
    Image:          nannany/liveness-probe-example:latest
    Image ID:       docker-pullable://nannany/liveness-probe-example@sha256:e8151a7fbb1d6c323b244d04b01526eadb0d51096338ca7a2e7f5935bb373d1d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Wed, 10 Jul 2019 21:21:07 +0900
    Ready:          True
    Restart Count:  0
    Requests:
      cpu:        100m
    Liveness:     http-get http://:8080/actuator/health delay=20s timeout=2s period=8s #success=1 #failure=1
    Readiness:    http-get http://:8080/actuator/health delay=10s timeout=2s period=3s #success=1 #failure=1
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-rvgsx (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-rvgsx:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-rvgsx
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age   From                                                        Message
  ----    ------     ----  ----                                                        -------
  Normal  Scheduled  24s   default-scheduler                                           Successfully assigned default/liveness-probe to gke-standard-cluster-1-default-pool-b350d2ec-svw3
  Normal  Pulling    23s   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  pulling image "nannany/liveness-probe-example:latest"
  Normal  Pulled     21s   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Successfully pulled image "nannany/liveness-probe-example:latest"
  Normal  Created    20s   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Created container
  Normal  Started    20s   kubelet, gke-standard-cluster-1-default-pool-b350d2ec-svw3  Started container
