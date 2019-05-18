# goal
clean arch の概要。メリットデメリット把握

図が生まれた背景
ヘキサゴナルアーキテクチャ
* 中心となるビジネスロジック以外を交換可能なものにする
* ポート・アダプター　→　ビジネスロジックを点在させない
ゲームによる比喩

## enterprise buisiness rules

ドメイン

## usecase

アプリケーションレイヤー
ドメインにおける問題を解決する

## interface adapters


DIP
依存の方向を気にする。ビジネスロジックは何にも依存しないようにする。

DS：POJO

entity：値オブジェクト


Message Bus
