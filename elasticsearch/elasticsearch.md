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

## 53 

* こんなかんじでやると解析してくれる

```
POST _analyze
{
  "tokenizer": "standard",
  "text": "I'm in the mood for drinking."
}

POST _analyze
{
  "filter": [ "lowercase" ],
  "text": "I'm in the mood for drinking."
}
```

## 54

* inverted index = 転置インデックス を使用して検索している

## 55

* Character Filter
* 

======
形態素解析系はいったん飛ばす
======

# Intro Searching

## 65

* elasticsearchでの検索クエリについて

## 66 

* `GET product/default/_search?q=* `全部とれる
* `GET product/default/_search?q=name:Lobster`ロブスターだけとれる
* `GET product/default/_search?q=tags:Meat AND name:Tuna`タグMeat で 名前Tuna

## 67

* 全部とれる

```
GET product/default/_search
{
  "query": {
    "match_all": {}
  }
}
```

## 68

* クエリ結果の味方について

## 69

* TF/IDF TF：出現頻度 IDF：単語がどれくらい特徴的か
* Okapi BM25 ：スコアを出すアルゴリズム
* explain付与すると、どのようにしてスコア算出されたか見れる

## 70

* debug用途でexplain APIは便利

```
GET product/default/1/_explain
{
  "query": {
    "term": {
      "name": "lobster"
    }
  }
}
```

## 71

* query context? かっこの話？ よくわからん
* query contextはスコアに影響を与える。filterコンテキストは影響を与えない

## 72

* term query と match query
  * term は直でinverted indexに行くけど、match はanalizerを介する

```
GET product/default/_search?explain
{
  "query": {
    "term": {
      "name": "lobster"
    }
  }
}

GET product/default/_search?explain
{
  "query": {
    "term": {
      "name": "Lobster"
    }
  }
}
GET product/default/_search?explain
{
  "query": {
    "match": {
      "name": "Lobster"
    }
  }
}
```

# Term level queries

## 73

* term queryをみてく

## 74 

* booleanフィールドをひっかける

```
GET product/default/_search
{
  "query": {
    "term": {
      "is_active": {
        "value": true
      }
    }
  }
}
```

## 75

* IN句みたいなやつ

```
GET product/default/_search
{
  "query": {
    "terms": {
      "tags.keyword": [
        "Soup",
        "Cake"
        ]
    }
  }
}
```


## 76

* idで絞る

```
GET product/default/_search
{
  "query": {
    "ids": {
      "values": [
1,2,3        ]
    }
  }
}
```

## 77 

* 範囲指定

```
GET product/default/_search
{
  "query": {
    "range": {
      "in_stock": {
        "gte": 2,
        "lte": 5
      }
    }
  }
}

GET product/default/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "2010/01/01",
        "lte": "2010/12/31"
      }
    }
  }
}

GET product/default/_search
{
  "query": {
    "range": {
      "created": {
        "gte": "01-01-2010",
        "lte": "31-12-2010",
        "format": "dd-MM-yyyy"
      }
    }
  }
}
```

## 78

* https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math 
* 基軸の日に足したりする

## 79

* non-nullを調べる

```
GET product/default/_search
{
  "query": {
    "exists": {
      "field": "tags"
    }
  }
}
```

## 80

* prefixの一致指定できる

```
GET product/default/_search
{
  "query": {
    "prefix": {
      "tags.keyword": "Vege"
    }
  }
}
```

## 81

* ワイルドカードを使える
* ?は一文字、*は任意

```
GET product/default/_search
{
  "query": {
    "wildcard": {
      "tags.keyword": "Veg*ble"
    }
  }
}

GET product/default/_search
{
  "query": {
    "wildcard": {
      "tags.keyword": "Veg?ble"
    }
  }
}
```

## 82

* 正規表現を一部使える
* https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html#regexp-syntax

```
GET product/default/_search
{
  "query": {
    "regexp": {
      "tags.keyword": "Veget[a-zA-Z]+ble"
    }
  }
}
```

## 83

* これでデータ入れる

```
curl -H "Content-Type: application/json" -u elastic:${password}  -XPOST  https://94ddc868351e4e5ea5ad7f9f1cf72f37.ap-northeast-1.aws.found.io:9243/recipe/default/_bulk --data-binary '@test-data2.json'
```

* データ準備

## 84 

* match クエリ

```
GET /recipe/default/_search
{
  "query": {
    "match": {
      "title": "Recipes with pasta or spaghetti"
    }
  }
}

GET /recipe/default/_search
{
  "query": {
    "match": {
      "title": {
        "query": "pasta spaghetti",
        "operator": "and"
      }
    }
  }
}
```

## 85 

* matchクエリの順番厳密にした番

```
GET /recipe/default/_search
{
  "query": {
    "match_phrase": {
      "title": "spaghetti puttanesca"
    }
  }
}
```

## 86

* queryで指定した文字に関して、複数のフィールドでmatchしているか見る


```
GET /recipe/default/_search
{
  "query": {
    "multi_match": {
      "query": "pasta",
      "fields": ["title","description"]
    }
  }
}
```

# adding boolean logic to queries

## 87

* Leaf query と compound query
* bool query

## 88

* boolクエリを使った

```
GET /recipe/default/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "ingredients.name": "parmesan"
          }
        }
        ],
        "must_not": [
        {
          "match": {
            "ingredients.name": "tuna"
          }
        }
        ],
        "should": [
        {
          "match": {
            "ingredients.name": "parsley"
          }
        }
        ], 
        "filter": [
        {
          "range": {
            "preparation_time_minutes": {
              "lte": 15
            }
          }
        }
      ]
    }
  }
}


GET /recipe/default/_search
{
  "query": {
    "bool": {
        "should": [
        {
          "match": {
            "ingredients.name": "parmesan"
          }
        }
        ]
    }
  }
}
```

## 89

* どのクエリにマッチするかわかるようにできる

```
GET /recipe/default/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "ingredients.name": {
              "query": "parmesan",
              "_name": "parmesan_must"
            }
          }
        }
        ],
        "must_not": [
        {
          "match": {
            "ingredients.name": {
              "query": "tuna",
              "_name": "tuna_must_not"
            }
          }
        }
        ],
        "should": [
        {
          "match": {
            "ingredients.name": {
              "query": "parsley",
              "_name": "parsley_should"
            }
          }
        }
        ], 
        "filter": [
        {
          "range": {
            "preparation_time_minutes": {
              "lte": 15,
              "_name": "prep_time_filter"
            }
          }
        }
      ]
    }
  }
}
```

## 90

* andとか使ってみる

```
GET /recipe/default/_search
{
  "query": {
    "match": {
      "title": {
        "query":"pasta carbonara",
        "operator": "and"
      }
    }
  }
}

GET /recipe/default/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "title": "`pasta"
          }
        },
        {
          "term": {
            "title": "carbonara"
          }
        }
        ]
    }
  }
}
```


##20 