# overview

* Elastic Stack ⇒ Elastic StackはElastic社が提供するデータの収集・加工・集計・分析のソフトウェア群です。

kibana
logstash 
xpack
beats

* logstash beats からelasticsearchにデータぶち込む。
* elasticsearchAPIで直接データを入れることもできる

## 7

* 1つのクラスター内に複数のノードがある

## 8

* elasticsearchにドキュメントがぶち込まれ、index毎に分類されて登録されている

## 9

* typeという概念があったが、新しいelasticsearchのverからは消えている。
* type と indexの違いは分かりにくかったらしい
* この講座でdefaultといったら、typeのことを指しているらしい？

## 10

## 11

* sharding について
* shardingすることの利点は、とても大きなデータを分割することにより、別のノードにデータを格納できるようになり、拡張が容易になる点にある。

いまいちshardが分からない

## 12

* replicationについて
* shardのレプリカを作成することによって可用性を高めている
* できるreplicaの数はデフォルトだと1つ
* オリジナルなshardとそのreplicaの組み合わせをreplication groupと呼ぶ

## 13

* どのようにshardとreplicaで同期を取っているのかについて
* shardへのadd、deleteが来た場合には、shardが責任を持って同期しているところまでみる？？

## 14

* elasticsearchが外部から来たHTTP通信にどう返しているかの流れについて
* coordinating node が受ける⇒coordinating nodeが他のnodeにきく ⇒ 返ってきた情報をマージしてクライアントに返す

