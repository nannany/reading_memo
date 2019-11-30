# 青山さん

* 新しい技術と向き合う
* 技術力だけ高くてもだめ
  * 組織をスケールさせる力
* OSSを使い仕事をしていくということ
* カンファレンスに行って何が良かったか？
  * 最新の動向
* ブログ等のすすめ
  * 思考のアウトプット
* kubernetesのslackがある
* 副業
  * 本業しっかりしてる
  * プライベート技術しても良い
  * 本業の制約から開放されたい
* 履歴書、ポートフォリオみたいなの作っとくと良い

# アドテク

* DSP?
* SSP？
* 100msの制約は絶対
* オンメモリ戦略
  * 整合性の担保
  * IOモナド？
* リアルタイムなデータはredis
  * MessagePack?
* アクターモデル
  * fire-and-forget
  * 本質ではない処理にはcpuリソース割きたくない
  * 信頼性はat-most-once。重要なメッセージは送れない
* microadd

# 20代プロマネ

@ysk_118

* アジャイルチームを支える会
* 伝えたいこと：マネジメントにチャレンジする人を増やしたい
* 全体最適で成果に導く
* 全員と話す

## マネジのリアル

* 批判
* 別れ
* ネガティブフィードバック
* アンコントローラブル

## 面白さ

* 変化を起こせているときは面白い
* エンジニアのためのマネジメントキャリアパス

# クラウドネイティブな監視

@kameneko1004

* cloud nativeとは？→ 定義がある
* Web3層モデル時代では、簡単にデバッグできた
* マイクロサービスにおいてはしんどい

## 可観測性

* observability：人によって意味合いが異なる
* monitoring,analyticsが目的
* monitoringは想定された障害への対策
* 後からデバッグできるようにanalyticsの観点が必要
* observabilityにはtestingが含まれる 
* observabilityを実現するには？
  * telemetryなツールの導入

## Telemetry

* Metrics
  * 単一のメトリクスからは何もわからないことが多い
  * カーディナリティの高いラベルをもたせると、爆発的にメトリクスが増加する
  * Prometheus
* Logging
  * ストレージ設計注意
  * Grafana Loki
* Tracing
  * Jaeger
* telemetryの課題
  * 構築コストが高い
* observabilityの先
  * 観測データをビジネスに利用する
* distributed system observability


# マルチクラウド・コンテナに最適化したリスクを最小化するcontinuous delivery

清水健司

* spinnaker
* solrをEKS上に構築
* Jenkinsを使うのもありだったが、高度なデプロイメント戦略には不安があった
  * Rolling Updateでは要件を満たせない
* Kubernetes へのデプロイツールを採用
  * Spinnaker
    * パイプラインテンプレート
  * blue,green deployment
  * Jsonを吐く?
  * Warming up query?
