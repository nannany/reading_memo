# Udemy RabbitMQコース

## Lecture4

* 処理に長いことかかるシステムと同期的に通信するわけにはいかない

## Lecture7

* 

rabbitmqを立ち上げるためのdockerコマンド

```
docker run -d --rm --name rabbitmqtest -p 15672:15672 -p 5672:5672 -t rabbitmq:3-management
```

## Lecture22

* Jsonを使用する理由

RabbitMQはどんな値でもやり取りすることができ、柔軟性がある。その柔軟性ゆえ、1つのpublisherではデリミタを;、もう1つで|| みたいなことが起きうる。
そうなると、subscriber側は大変なので、統一したフォーマットとして、JSONが必要となってくる。
 
## Lecture22

* RabbitMQにおいて、来たメッセージをキューに分配するのがExchange
  * Fanout、Direct、Topicなどの種類がある
* ExchangeはメッセージのRouting Keyに従って分配される
* メッセージとキューの結びつきをBindingという

## Lecture27

* Exchangeの種類
  * Fanout：ブロードキャストでキューにメッセージ渡すかんじ
  * Direct：Routing Keyをもとに行先キューを決めるかんじ
  * Topic：Routing Keyをもとに行先キューを決めるが、Routing Keyに`*`とか`#`が使える

## Lecture30

* エラーが出た場合の扱い
* springだと、例外が出た場合はもう一回キューに入れて、もっかい処理しようとする。それがうまくいくはずない処理だったら無限ループってしまう
* consumerのプログラム側で、requeueされるの防ぎ、DLX（Dead Letter Exchange）にメッセージを送ることができる
* DLXに入ったメッセージは、↑のとは別のconsumerで処理される

## Lecture37

* consumerでの例外の扱い方は2種類ある
  *  `AmqpRejectAndDontRequeueException`をスローする
  *  application.propertiesをいじって、マニュアルモードにして、エラーの時は `channel.basicReject()`、おけーな時は`channel.basicAck()`みたいにする
  * `channel.basicReject()`は、RabbitMQ側に受け入れられなかったことを示し、`channel.basicAck()`はうまくいったことを示す

## Lecture39

* RabbitMQのRestAPIがあり、そこからいろいろ登録できたりする。
