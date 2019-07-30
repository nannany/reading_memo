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


## 15

* Routingにおいて、シャーディングの数の剰余で判断しているため、シャーディングする数の変更は困難になっている

## 16

* 2章まとめ

## 17

* [Elastic Cloud](https://www.elastic.co/jp/cloud/) を使用してみる

## 18 

* Mac、Linuxのインストール手順なのでとばす


## 26 

* Kibana の dev tool を使用してみる。

## 27

* indexの作り方


## 28 

* dev tool でドキュメントを足す？

## 29

* id指定して、データ引っ張る

## 30

* PUTでデータ更新。まるっと入れ替え。

## 31

* POSTで一部更新

## 32

* script作っていろいろ。

## 33

* upsert。なかったら登録、あれば更新のパターン。

## 34

* query でdeleteする

## 35

* index毎消せる

## 36

* _bulkで一気に複数作業できる

## 37

* curlでデータ入れる。

## 38

```
GET /_cat/health?v

GET /_cat/nodes?v

GET /_cat/indices?v

GET _cat/allocation?v

GET _cat/shards?v
```

* 上みたいな感じで健康状態など見れる

## 39

* mappingについて

## 40 

* 各フィールドに対して、よしなに型をマッピングしてくれる

## 41

* メタフィールドについて。_idとか_indexとか

## 42

* https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

## 43

* 明示的にマッピングに型を加える。

## 45

* マッピングをupdateすることはできない。変えるのなら、新たに作るしかない。

## 46 

* マッピングに使われているフィールドについて

## 47

* フィールドを加える

```
PUT /product/default/_mapping
{
  "properties": {
    "description": {
      "type": "text"
    },
    "name": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "tags": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    }
  }
}
```

## 48

* カスタマイズされたフィールドを作成


## 49

* indexを最新化する？
* conflicts=proceed クエリ

## 50 

* マッピングについてのまとめ

# アナライザー

## 51 

* 諸データはそのままelasticsearchに突っ込まれるわけではない。アナライザーを経てから突っ込まれる。

## 52

* Character fileter ⇒ tokenizer ⇒ token filter
* 
