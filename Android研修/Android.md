# Android 

* linuxがベース
* pureなandroid →pixcl。大体androidに改造を加えている
* open handset alliance　→　androidの管理団体
* [リファレンス](https://developer.android.com/index.html?hl=ja)
* 標準APIを使い倒せば、画面表示、一覧表示、Sqliteの使用はできる。
* 自分で新しいクラスを作ることはほとんどない
* 作ったandroidアプリはJavaではない？
  * Java→classファイル→dexファイル（Android Runtime(ART)で動作する）
* Darvik → Android Runtime
* JVMは重すぎるのでDarvik作った
* apkファイルは実質zipファイル
* google play に乗っかっているのはapkファイル
* APIレベルに注意する
  * 非推奨になったり、メソッド増えたり
* package名は一意になるようにする。
* package名は小文字
* GoogleとしてはKotlin推し
* googleとjetbrainsは仲いい、googleとoracleは仲悪い
* gradleを採用
* manifestファイル、AndroidManifest.xmlという名前でなければならない。
* アイコンのpngは５つ作らないといけない。解像度が端末によって違うため
* Activityのサブクラスを作成したらmanifestファイルに書かないといけない
* Javaプログラム以外がres配下に入る
* dpi：Androidのピクセルの単位
* AVD → エミュレーター
* エミュレーターは32bit版のほうが早い？？
* GoogleAPI OHAから見るGOOGLEは一社。
* GoogleAPIsは3rdパーティーライブラリ
  * Admob
* エミュレータの速度を改善するには,virtualizaiton technology
* haxm
* 文字列リソースファイル
  * なぜ使うか？→多言語対応のため
  * valuesフォルダに入れる
* resフォルダ配下に作れるフォルダの名称は決まっている
* Androidではspがフォントサイズの単位

## Activity
* 3画面あるなら3アクティビティ必要
* AppCompatActivityのサブクラスを作成する。
  * Activityのサブクラスを作ることはまずない。
  * AppCompatActivityは下位互換性を備えたクラス。
* 古いandroidだとActionBarがない。
* 下位互換性を保つためにsupport libraryをつかう。古いAPIレベルでも新しい端末と同じことができる
* Android jetpack
* androidxから始まるパッケージはjetpackのもの。つまり下位互換性を考慮した部品
* Googleの開発は割とつぎはぎでひどい
* setContentView メソッドでJavaとxmlを結び付けている
* ビジブル状態
  * ex）ダイアログが出てユーザーが操作できない状態

### Activityのライフサイクル

* 大事な概念なのでしっかり理解する必要がある
* 初期化処理メソッド
  * onCreate : 静的な初期化処理 ex)画面のレイアウトリソースファイルとの対応。setContentViewメソッド
  * onStart  : 上と下以外の初期化処理
  * onResume : 動的な初期化処理 ex)Webからデータを取得、DBからデータ取得する

### view
* 重たいアプリを作らないようにする
  * ビューを重ねすぎない → ConstraintLayout
  * 非同期処理をする

```
<intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```
これを書くと最初に呼び出される画面になる

# 画面遷移
* 画像ファイルにはpng、jpgを主に使う
* resumeにリスナー書く
* Listenerがいろいろある。タップするときに反応するのとか、ドラッグしたときに反応するのとか

## intent

* 明示的なインテント
* 暗黙的なインテント
  * broadcast
* putExtra(String,value)で値の受け渡しができる.渡すほうがこれを書く。

# SQLite

* SQLiteOpenHelper
  * DB作成
  * テーブル作成
  * 接続切断
* SQLiteDatabase
  * crud
  * SQL実行
  * 検索だけに用いるときは`getReadableDatabase`を使う
  * queryメソッドで問い合わせ
    * 7つ引数がある。nullにすると無条件
* SQLiteにはBoolean,Date型に当たるものがない
* AndroidのSQLiteのSQLには;の記述が必須。JDBCだといらない
* Device file explorerの`/data/data/${application_package}/databases/${database_name}`ここにデータベースに格納した値が入る
* [DB Browser](https://sqlitebrowser.org/) に上記に作成されたファイルを入れればGUIで見れる
* onUpgradeはDBのversionが上がったら差分を記述する。[flywayを使ったら実装しないみたい](https://qiita.com/opengl-8080/items/6368c19a06521b65a655)

## Context

* ActivityはContextのサブクラス
  * UIを持つこと、操作することができる。
* ServiceはContextのサブクラス
  * UIを持つこと、操作することはできない。
* 裏でやるべき処理？はServiceに実行させる。
* getApplicationContext()で現在のContextをとれる

# RecyclerView

* RecyclerViewはサポートクラス。標準ではないので、使おうと思ったらgradleにdependencyを足す
* １行を表すレイアウトリソースファイルも必要になる
* ViewHolder : 一行分の View を持つ
* LayoutInflater : xmlファイルを引数に食わせるとViewオブジェクトを返してくれる
* Adapter の内部クラスとしてViewHolderを作るのはよくある
* viewの表示はsetVisibilityで制御
  * VISIBLE
  * UNVISIBLE : 透明になる感じ
  * GONE : そもそもなくなる

# メニュー

---
## その他

* keymapをやり直すには？ → vim emulation で簡単に設定できる
* ctrl+shift+t に当たるのはintellijでは何？ 
* 内部クラスから外部クラスのthisを呼ぶときは`外部クラス.this`でいける。Androidだとよく使う
* shift+f6で一括リネーム（intellij）
---

## question

* android studio以外に選択肢はあるのか？ → officialなのはandroid studioのみ。ほかのものは怪しいのでAndroid studio使用を薦める。
* EditTextの以下のコードなんで例外出しているのか？ → 逆コンパイル失敗。公式から持ってくれば紐づけ可能

```
    public Editable getText() {
        throw new RuntimeException("Stub!");
    }
```
* Serviceでやるべき処理とは？ → 大量データのインサートなど
* 一覧表示されたものの詳細をみる、とかはidどうやって特定するのか？ → idを送ってやってdetail側で判断
  * RecyclerViewに含まれているViewのidは複数あっても全部同じということ？ → 同じ