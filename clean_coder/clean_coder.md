# 第1章 プロ意識

## 

# 第4章 コーディング

本章では、筆者個人のコーディングの規則、原則についての説明をする。

## 準備

疲労時や心配事があるときはコードを書かないようにする。

## フローゾーン

ゾーンに入るのは良いことではない。
割込みは避けられないので、割り込まれても親切にふるまうべき。

## 書きたいのに書けない

書けないときはペアプロしたり、創造的インプット（人によって違うが小説を読む等を指している）をする。

## デバッグ

TDDを導入するなどして、デバッグの時間を限りなく0に近づける努力をするべき。

## 自分のペースを保つ

疲れてやってもしょうがない

## 遅れ

希望観測的な見積もりをしてはいけない。
残業は

* 個人的に余裕がある場合
* 2週間以内など期間が短い場合
* 残業しても間に合わない場合の次善策を上司が持っている場合

等の条件がそろっている場合にしかするべきでない。
完了の定義をしておき、偽の完了報告を許さないようにする。

## ヘルプ

他の人を手伝うことによって得るものがある。
協力を求めたらすぐに終わることを1人で行き詰まるのはプロではない。

# 第5章 テスト駆動開発

## 結論は出た

TDDに効果があることは確認されている。プロならばやるべき。

## TDDの3原則

以下がTDDの3原則
1. 失敗するユニットテストを書くまでプロダクションコードを書いてはいけない。
1. テストを失敗させる目的以外でユニットテストを書いてはいけない。なお、コンパイルできないのも失敗に含まれる。
1. 失敗しているユニットテストが成功するまで他のプロダクションコードを書いてはいけない。
 
TDDの利点としては以下のよう。
* テストが通ればリリース可能であるとある程度は思える。
* バグ混入率が下がる
* リファクタしやすくなる
* テストを見ることによってテストされるコードの使い方が分かる
* テストしやすい設計を試みるようになり、優れた設計になる

## TDDは何ではないか

銀の弾丸ではない。
利点を鑑みて、導入するか決めよ。

# 第6章 練習

プロは必ず練習する。プログラマの練習方法について記述する。

## 練習の背景

昔はコンパイル、ビルドにとても時間がかかっていたが今はそんなことない。
それゆえにプログラマー自身の思考速度、意思決定速度が生産性に大きく関与するようになっている。

## コーディング道場

http://butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata
ボーリングゲームのコーディングを繰り返し行うことで、下記の効果が見込める。

* ホットキー、イディオム？の学習
* TDD、CIの規律の学習
* よくある問題と解決策の組み合わせを潜在意識に植え付け、現実のプログラミングの解決方法に活かす

## 経験を広げる

仕事のプロジェクトだけやっていると技術の幅が広がらない。
仕事で使用していない言語のオープンソースに貢献するなどで幅を広げる。


# 第7章 受け入れテスト

## 要求のコミュニケーション

実際に動いている状態をみるということは、新しい情報が入ってくるということ。その情報はシステムの見方を変える。
そのため、要求を詳細化していくと開発中のシステムとはかけ離れていく

## 受け入れテスト

受入テストとは、要求の完了を定義するためにステークホルダーとプログラマーが協力して書くテストのこと。
受入テストは極力自動化していく。
受入テストを書くタイミングは、「後期の詳細化」原則に従って、できるだけ遅くにする。

ユニットテストはプログラマがプログラマのために書くものだが、受け入れテストはビジネスがビジネスのために書くテストである。


# 第8章 テスト戦略

プロの開発チームに必要なのは優れたテスト戦略。

## QAは何も見つけてはいけない

開発チームとしてはQAチームが何か見つけるようなことがない状態を目指すべき。

## テスト自動化ピラミッド

### ユニットテスト

ユニットテストの目的は、システムを低レベルから仕様化すること。

### コンポーネントテスト

受け入れテストの1種。ビジネスルールの受け入れテストとなる。
入力データをコンポーネントにわたし、出力データを集め、その正しさを検証する。他のシステムコンポーネントと結合している場合はモック等をつかう。

