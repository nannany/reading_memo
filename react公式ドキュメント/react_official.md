# React公式ドキュメント

評価: ⭐️⭐️⭐️⭐️⭐️
ステータス: 読了
種別: 記事

# UIの記述

- [x]  https://ja.react.dev/learn/your-first-component

  迷うところなし

- [x]  https://ja.react.dev/learn/importing-and-exporting-components

  名前付きエクスポートはimportとexportで名前が一致していなければならない

- [x]  https://ja.react.dev/learn/writing-markup-with-jsx

  明示的にtagを閉じる必要がある。

  単一のルート要素を返す

  classはclassNameにするなど、react domコンポーネントの書き方に合わせる https://ja.react.dev/reference/react-dom/components/common

- [x]  https://ja.react.dev/learn/javascript-in-jsx-with-curly-braces

  {{}}でオブジェクトを渡せる

- [x]  https://ja.react.dev/learn/passing-props-to-a-component

  childrenの使い方がのってる

- [x]  https://ja.react.dev/learn/conditional-rendering
- [x]  https://ja.react.dev/learn/rendering-lists
- [x]  https://ja.react.dev/learn/keeping-components-pure

  strict mode、何がstrictなのか分からなかったが、2回純粋関数を呼び出すことによって、意図していない副作用があるか否かをチェックするという意味でstrictなのか。なるほど

- [x]  https://ja.react.dev/learn/understanding-your-ui-as-a-tree

  レンダーツリー、依存関係ツリー

  レンダーツリーはreactコンポーネントのツリー。ルートに近い方のコンポーネントを変更すると影響が大きく、リーフに行くにつれて頻繁に変更される。レンダーパフォーマンスの理解に役立つ概念

  依存関係ツリーはモジュールの依存関係。jsのimportによる構造と理解。バンドルする時のパフォーマンスに影響を与えると理解。


# **インタラクティビティの追加**

- [x]  https://ja.react.dev/learn/responding-to-events

  イベントハンドラには関数を渡す。関数呼び出しを渡すのではない

  イベントハンドラは適切なhtml tagに設定する。buttonに設定できるところをdivにしたりしないようにする

  reactではonScroll以外のイベントは全て伝播する

- [x]  https://ja.react.dev/learn/state-a-components-memory

  useStateはinitialの値しか与えていないのに、どのようにしてstateを特定しているのか？→内部的にはただの配列で持っていて、暗黙的に定義順で当て込めているのでできてる

  useStateはトップレベルに置かないとエラーになる

- [x]  https://ja.react.dev/learn/render-and-commit

  とりが、レンダ、コミットの三段階がある

- [x]  https://ja.react.dev/learn/state-as-a-snapshot

  次のrenderが起こるまでstateは変わらない、というのはあるある

- [x]  https://ja.react.dev/learn/queueing-a-series-of-state-updates

  setNumber(n ⇒ 5)のように渡した関数は、キューにつまれ、次のレンダーのタイミングで処理される

- [x]  https://ja.react.dev/learn/updating-objects-in-state

  スプレッド構文は１つの深さのコピーしかしない。つまり2つ以上の深さはコピーできない

  深い階層のあるstateについては、まずフラットにすることを考える。それが困難なら、immerの利用を考える　https://immerjs.github.io/immer/

- [x]  https://ja.react.dev/learn/updating-arrays-in-state

  配列の追加についてはspread構文

  削除はfilterを使う

  更新はmap

  挿入にはslice

  reverseとかしたい場合はコピーしてそれに変更加える。ただし、spread 構文を使ってコピーした場合は階層が1つなので注意


# Stateの管理

- [x]  https://ja.react.dev/learn/reacting-to-input-with-state

  storybookについての説明がある。多くの視覚状態をパッと見れるようにしたやつ

  リデューサなるものを使えばstateを1つのオブジェクトに管理できるらしい

- [x]  https://ja.react.dev/learn/choosing-the-state-structure

  stateをうまく扱う原則

  関連するstateをまとめる

  x、y座標みたいなやつ

  stateの矛盾を避ける

  stateの重複を避ける

  stateの深いネストを避ける

- [x]  https://ja.react.dev/learn/sharing-state-between-components

  公式な用語ではないが、制御コンポーネント、非制御コンポーネントという言葉がある。非制御は自らがstateを持ち、親にコントロールを任せていない状態のコンポーネント。制御はその逆で、propsを通じて親がそのコンポーネントを制御する

- [x]  https://ja.react.dev/learn/preserving-and-resetting-state

  reactはレンダーツリーの位置と関連付けてstateを記憶する。

  下記の2つは(変数の云々は抜きにしても)ことなる位置にツリーができる。前者はdivのトップにCounterが配置されるが、後者はdivの[0]と[1]にCounterが配置される。

   ```clojure
         <div>
         {isFancy ? (
           <Counter isFancy={true} /> 
         ) : (
           <Counter isFancy={false} /> 
         )}
   ```


```clojure
    <div>
      {isPlayerA &&
        <Counter person="Taylor" />
      }
      {!isPlayerA &&
        <Counter person="Sarah" />
      }
```

[https://azukiazusa.dev/blog/react-activity-component/](https://azukiazusa.dev/blog/react-activity-component/)　activityとよく関係してる話である。activityを絡めれば、コンポーネントを非表示にしてもstateをリセットせずに済む

- [x]  https://ja.react.dev/learn/extracting-state-logic-into-a-reducer

  stateをactionのディスパッチに置き換える、リデューサ関数の作成、コンポーネントからリデューサを使う、の流れで導入

  reduceという名前は、元々のreduceの ここまでの結果 と 現在の要素 を受け取って、次の結果 を返す処理に習っている。つまり、現在のstate と action を受け取って、 次のstate を作るということ。

  reducerは準関数であるべき

  action typeには、userが何をしたかを記述するべきであり、stateをどうしたいかは書かない

  計算プロパティ名というものがある https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/Object_initializer#%E8%A8%88%E7%AE%97%E3%83%97%E3%83%AD%E3%83%91%E3%83%86%E3%82%A3%E5%90%8D

  プロパティ名に[]を使って、[]の中では式をかける感じ

  リデューサを使っていれば、イベントハンドラ（リデューサ呼び出し元）での書き直しが発生しない。リデューサ内部の変更ですむ

- [x]  https://ja.react.dev/learn/passing-data-deeply-with-context

  コンテキストを使う前に検討すべきこと

  propsを渡す方法

  childrenをjsxとして渡す方法

  コンテキストの具体的用途

  theme: darkモードとか

  現在のアカウント

  ルーティング

  state管理

  一般的に、ある情報が、ツリーの様々な部分にある離れたコンポーネントによって必要とされている場合、コンテクストが役立つというサインです

- [x]  https://ja.react.dev/learn/scaling-up-with-reducer-and-context

  今はproviderつけなくても良い

  https://zenn.dev/uhyo/books/react-19-new/viewer/context

  stateのcontextとdispatchのcontextを作る。それをまとめたやつを作ってchildrenとしてcontextを共有したいjsxを受け取る


# 避難ハッチ

- [x]  https://ja.react.dev/learn/referencing-values-with-refs

  refを使うタイミング

  timeout idの保存

  dom要素の保存と操作

  jsxの計算に必要でないその他オブジェクトの保存

  var.currentでuseRefを参照できる

- [x]  https://ja.react.dev/learn/manipulating-the-dom-with-refs

  useRefを使ってdomにfocusを当てるのはよくあること

  useImperativeHandleは親から子にrefを渡すにおいて、そのrefでできることを限定する。親側で該当refをなんでもできることを避けるためにこうする

  flushSync。scrollの管理に使える

- [x]  https://ja.react.dev/learn/synchronizing-with-effects
- [x]  https://ja.react.dev/learn/you-might-not-need-an-effect

  重たい計算のcacheにはuseMemoを使う

  propsが変更した際にeffectを走らせるのは効率が悪い。

  keyでstateをリセットするテクニック

  **あるコードがエフェクトにあるべきか、イベントハンドラにあるべきかわからない場合は、そのコードが実行される*理由*を自問してください。コンポーネントがユーザに*表示されたために*実行されるべきコードにのみエフェクトを使用してください**

  アプリが読み込まれるときに一度だけ実行されるロジックはdidInit変数など用意して制御する

  外部storeの状態をsubscribeする際には**`useSyncExternalStore` を使うのが良い**

- [x]  https://ja.react.dev/learn/lifecycle-of-reactive-effects

  コード内のeffect処理は1つの独立した処理を記述すべき。色々な処理を混ぜない（ex: analyticsの送信と、chatroomの接続を混ぜない）

- [x]  https://ja.react.dev/learn/separating-events-from-effects

  イベントハンドラとエフェクトの違い。イベントハンドラは明確なユーザーの操作に反応する。エフェクトはリアクティブな値を読み取って、それが変わっていたら反応する。

  https://tech.revcomm.co.jp/introduce-react-use-effect-event

  エフェクトイベントとは、エフェクトコードを構成する「パーツ」のうちの非リアクティブな部分です。それを使用するエフェクトの隣に置くようにしましょう

  経験則から言うと、エフェクトイベントは*ユーザ*の視点から起こることに対応する必要があります。

- [x]  https://ja.react.dev/learn/removing-effect-dependencies

  エフェクトの依存値としてのオブジェクトや関数は、可能な限り避けるべきです

- [x]  https://ja.react.dev/learn/reusing-logic-with-custom-hooks

  **カスタムフックは、*state 自体*ではなく、*state を扱うロジック*を共有できるようにするためのもの**

  カスタムフックを作る理由

    1. エフェクトに出入りするデータの流れが非常に明確になる。
    2. コンポーネントがエフェクトの実装そのものではなく、意図にフォーカスできるようになる。
    3. React が新しい機能を追加したときに、コンポーネントを変更せずにエフェクトを削除できるようになる。

  そのうちdata fetchは組み込みのhookが提供されることになろう