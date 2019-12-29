Consumer Driven Contracts 
ConsumerとProviderでIFを取り決めておいて、それをもとにテストを実施するイメージ

CDC、なんとなく考え方はわかるのだが、実際どうやってテスト実行しているのか？

[クックパッド](https://techlife.cookpad.com/entry/2017/04/03/113417)
マイクロサービス化にともなって、テスト大変になった。
APIで連結する部分はmockを使用してやっていたが、
デメリットとして、Provider側が変更された場合に検知できないという問題があった。
