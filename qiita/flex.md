# 概要

CSSの練習サイトとして、[FLEXBOX FROGGY](https://flexboxfroggy.com/#ja)と[GRID GARDEN](https://cssgridgarden.com/#ja)を教えてもらったので、そこで得たflexboxとgridの知識についてまとめます

## flex

### flexコンテナー側に書くやつ

* justify-content
  * 配下のアイテムの水平方向の間隔、位置を制御する
* align-items
  * 配下のアイテムの垂直方向の間隔、位置を制御する
* flex-direction
  * アイテムをどのような順序で並べるか操る。縦横どちらに並べるか、リバースするかとか。
* flex-wrap
  * 配下のアイテムを折り返して表示させてよいか制御する
* flex-flow
  * flex-directionとflex-wrapはよく一緒に使われるので、その用途であるらしい。これを使うことで、スペースを区切りでdirection設定と折り返し設定を同時にできる
* align-content
  * wrapによってアイテムが複数行にまたがるようになったときに、その行間をどうするか制御する

### アイテム側に書くやつ

* order
  * 各アイテムの表示順を制御する
* align-self
  * align-itemsと同じ値を取る。該当のアイテムだけ、別の表示方法にすることが可能

## grid


### gridコンテナ側に書くやつ

* grid-template-columns
  * コンテナ内のグリッドを定義する
  * px(ピクセル)とかfr(分数計算できる。https://developer.mozilla.org/ja/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout)とか%とか色々指定できる
* grid-template-rows
  * grid-template-columnsと同様

### gridアイテム側に書くやつ

* grid-column-start、grid-column-end
  * 該当のアイテムが、分割されたグリッドのどこからどこに該当するか制御する
  * `grid-column: 4/6` みたいな書き方もできる
* grid-row
  * grid-column系と同じことができる
* grid-area
  * `grid-area: 1/1/3/6`みたいな感じでgrid-column,grid-rowでやっていたことを簡略化できる
* order
  * グリッドアイテムの順序を変えられる
