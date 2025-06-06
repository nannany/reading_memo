# React in Depth

ステータス: 読書中
種別: 書籍

<aside>
💡 **Notionヒント：**このページにメモやハイライトなどを記録しましょう。`[[` コマンドを使ってほかのNotionページへのリンクを追加することもできます。詳細は[こちら](https://www.notion.so/ja-jp/help/create-links-and-backlinks)。

</aside>

[](https://www.notion.so)

**目次**

# 1章

reactにまつわるエコシステムについて概観してる。

1章まとめ

```clojure
1章「**Developer’s guide to the React Ecosystem**」は、Reactのエキスパートを目指す開発者にとっての道しるべとなる章です。この章では、**Reactの習熟とは何か**を理解し、**広大なReactのエコシステム**をナビゲートし、**Reactの技術スタックの主要な構成要素**を学び、**適切なReactスタック**を構築する方法を概観します。

この本は、読者がReactの基本的な理解を持ち、簡単なアプリケーションを構築できるレベル（図1.1のB地点）から、さらに高度なレベル（C地点）へと進むことを前提としています。Reactの習熟への道のりは長く、本書では9つの領域（図1.3）を取り上げ、それぞれに1つまたは2つの章を割いて解説します。**第1章では、これらのReactの9つの領域の概要、つまりエコシステム全体の概観を提供します**。

現在のReactエコシステムは非常に広大であり、**150以上のツールとライブラリ**がReactとともに使用されています（図1.4）。Reactアプリケーションの全体的なレイヤー構造（図1.6）を理解することも重要であり、データレイヤーにはzustand、Immer、XStateなどが、基盤レイヤーには多くの異なる技術が含まれる可能性があります。

第1章は、Reactのエコシステムを理解するための舞台を設定し、続く章では、プロジェクトに適した技術やライブラリの選択と作成についてより深く掘り下げていきます。**理論的な知識と実践的な洞察を組み合わせることで、現代のWeb開発の複雑な状況を熟練したReact開発者として乗りこなすための基礎的な理解を身につけることを目指しています**。
```

# 2章 **Advanced component patterns**

```clojure
2章「**高度なコンポーネントパターン**」では、**堅牢なReactアプリケーションを構築するための重要なパターン**を探求します。この章は、**実践的な発見を促す**ように構成されており、Reactコンテキストの既存の知識に基づいて、より高度なテクニックを学びます。

主に解説されるパターンは以下の通りです。

*   **Providerパターン**
    *   複数の関連する値（状態の値とそのセッターなど）を管理するために、Providerパターンを使用してReactコンテキストを拡張する方法を探ります。
    *   基本的なReactコンテキストの使用を超えた**柔軟性と効率性の向上**を提供します。
    *   単純な例から始め、複数の状態値とセッターを処理するプロバイダーで子コンポーネントをラップする方法を示します。
    *   ダークモードの切り替え機能を例に、単一のオブジェクトに複数の値をまとめてコンテキストに渡す方法や、専用のプロバイダーを使用する方法、`use-context-selector`を使った選択可能なコンテキストの作成、そして`recontextual`ツールを使った型安全な選択可能なコンテキストの作成について解説します。
    *   Providerパターンは、大規模なアプリケーション全体で**データと機能を配布および整理する単一の方法**として使用できるほど強力であり、複数のコンテキストを階層的に組み合わせてグローバルおよびローカルな機能を提供できることが述べられています。
    *   `redux-toolkit`などの確立されたツールと比較して、Reactコンテキストと`useContext-Selector`を使用して複雑な状態を管理する方法についても触れられており、パフォーマンス面では同等であることが示唆されています。

*   **Compositeパターン**
    *   **スケーラブルで保守しやすいユーザーインターフェース**を作成する方法を明らかにします。
    *   外部からは名前空間で区切られたように見えるコンポーネントが、内部では通常のコンポーネントとして1つ以上のコンテキストを通じて通信する様子を示します（図2.5）。
    *   ラジオボタングループの例を用いて、単一のコンポーネントで複雑さを増していくことの課題を示し、Compositeパターンを使って複数の小さなコンポーネントに機能を分割することで、コードベースがより直感的で管理しやすくなり、拡張性も向上することを解説します。
    *   各情報チャネルにReactコンテキストを使用することが、このパターンを実装する最も簡単な解決策として挙げられています。

また、複数のカスタムフックを必要とするシナリオの例として、タスクマネージャーの作成が紹介されています。

この章を通じて、Reactの高度なコンポーネントパターンを理解し、より洗練されたReactアプリケーションを構築するための基礎を築くことを目指します。
```

[https://www.reactindepth.dev/browse/ch02](https://www.reactindepth.dev/browse/ch02)

2.1.1から2.1.2にかけて解決した問題点がいまいちわかってない。

rerenderが抑制されたことだと思うのだが、reactのmemoがそもそも何をしているかがよくわかってない。

2.1.3の示唆としては、useContextSelectorを使うべし、か？

(2025/04/07: 2.1を読んだ)

https://livebook.manning.com/book/react-in-depth/chapter-2/82

radio buttonを例に、compositeパターンを実装していた。

jsのロジックで描きすぎず、適切な粒度で部品を分けてやる、contextを使って情報の共有を行う、ことあたりがコツに思えた。

**The Summary pattern**

(2025/04/08: 2.2を読んだ)

summaryパターンでは、uiできにすることと、データ的な観点で気にすることを分離してやるようなイメージ。

これはなんでsummaryパターンというのだろう？

公式で定められているものではなく、その画面の入力値をまとめるものをsummaryというので、それに従った模様。

[https://chatgpt.com/share/67f93b0b-6e80-8009-8576-60e5bb24c1f1](https://chatgpt.com/share/67f93b0b-6e80-8009-8576-60e5bb24c1f1)

# 3章 **Optimizing React performance**

https://livebook.manning.com/book/react-in-depth/chapter-3/c

以下、notebooklmの要約。

3章「Optimizing React percformance」では、Reactアプリケーションの**パフォーマンス最適化**について解説しています。主な内容は以下の通りです。

**3.1 Reactのレンダリングを理解する**

- Reactの関数コンポーネントは、以下の3つの理由で再レンダリングされます。
    - **親コンポーネントが再レンダリングされた場合**
    - **自身の状態（state）が変更された場合**
    - **コンテキスト（context）の値が変更された場合**
- **プロパティ（props）が変更された場合でも、必ずしも再レンダリングされるわけではありません**。再レンダリングの主な要因は親コンポーネントのレンダリングです。
- React 18の開発環境で**Strict Mode**を使用している場合、コンポーネントが意図的に2回レンダリングされることがあります。これは、コンポーネントの設計上の潜在的な問題を早期に発見するためのReactの機能です。

**3.2 再レンダリングを最小限に抑えてパフォーマンスを最適化する**

- ブラウザは通常、1秒間に約60フレームで動作し、各フレームの処理時間は約16ミリ秒です。Reactのレンダリングも1フレームとして扱われるため、レンダリングに時間がかかるとアプリケーションの動作が遅く感じられることがあります。
- ユーザーが快適に操作するためには、ユーザーインターフェースは0.1秒以内に更新されるべきです。
- Reactアプリケーションのパフォーマンスを最適化する上で重要なのは、**不要な再レンダリングを最小限に抑える**ことです。
- *メモ化（Memoization）**は、不要な再計算を避けるための重要なテクニックです。Reactには、コンポーネントやその一部、あるいはコンポーネントに渡すプロパティをメモ化するための機能が用意されています。
    - **`memo()`関数**: コンポーネント全体をメモ化するために使用します。同じプロパティでコンポーネントが再度呼び出された場合、再レンダリングをスキップし、以前に計算された結果を再利用します。
    - **`useMemo`フック**: JSXの一部のような**値をメモ化**するために使用します。依存配列に指定された値が変更されない限り、以前の計算結果を返します。高コストな計算の結果をメモ化するのに役立ちます。
    - **`useCallback`フック**: **関数をメモ化**するために使用します。依存配列が変更されない限り、同じ関数インスタンスを返します。メモ化されたコンポーネントにコールバック関数を渡す際に、不要な再レンダリングを防ぐために重要です。
- メモ化は、アプリケーションが遅くなったときに後から行うのではなく、開発中に適切に適用することで、スムーズなユーザーエクスペリエンスを確保することが推奨されています。ただし、**過度な最適化（早期最適化）は、かえってパフォーマンスを低下させる可能性もある**ため注意が必要です。

**3.3 依存配列を理解する**

- `useEffect`、`useCallback`、`useMemo`、`useLayoutEffect`といった**フック**は、**依存配列**を使用して、いつ効果を実行するか、いつメモ化された値を再計算するかを決定します。
- 依存配列には、フック内で使用される**外部の変数（プロパティ、状態、コンテキストの値など）**を記述する必要があります。これにより、これらの変数のいずれかが変更された場合にのみ、フックが再実行または再計算されます。
- 依存配列を**省略した場合**、コンポーネントが再レンダリングされるたびにフックが実行されます。これは、レンダリングの追跡やパフォーマンス分析などの特定の目的で使用されることがあります。
- `useState`によって返される**セッター関数**や、`useRef`によって返される**オブジェクト**は、コンポーネントのライフサイクルを通じて常に安定しているため、依存配列に含める必要はありません。
- **ESLint**などのリンティングツールは、依存配列が正しく記述されているかどうかをチェックし、予期しない動作を防ぐのに役立ちます。

この章を読むことで、Reactのレンダリングの仕組みを深く理解し、`memo()`、`useMemo`、`useCallback`といったメモ化のテクニックや依存配列の効果的な使い方を習得し、より効率的で高性能なReactアプリケーションを開発するための知識を習得できます。

---

figure3.2よくわからん。second schedule effectで動いたときにclean up処理が動かない扱い？なのが謎い。

figure3.3は理解するのを諦めた。

(2025/04/12 3.1まで読んだ)

- [x]  3.2.1

https://zenn.dev/uhyo/books/react-19-new/viewer/form-action

react19から、formにactionを指定できるようになったらしい。

(2025/05/07 3.2.1まで読んだ)

- [x]  3.2.2
- [x]  3.2.3 **Memoize properties to memoized components**

list3.10でuseCallbackを利用してる意味としては、memo()の中でitemコンポーネントを持っていて、itemコンポーネントはonDeleteで関数を取っているが、onDeleteに渡す関数はその都度作られるので、変更とみなされてしまうのでuseCallbackを利用して再レンダリング時に再計算がなされないようにしている。

つまり、memo()を使っているならイベントハンドラでuseCallbackを利用する必要があるかもしれないということ。

- [x]  3.2.4  **Memoization hooks in detail**

むずい。結局何が言いたいのかよくわからなかった

- [x]  **3.3 Understanding dependency arrays**

javascriptにおける === の比較はオブジェクト型においては参照が等しいか否かを見る。

つまり {} !== {} はtrueになる。

- [x]  **3.3.1 What are dependencies?**
- [x]  **3.3.2 Run on every render by skipping the dependency array**

当たり前だけど、useMemoの2つ目の引数に何も渡さないで、レンダーごとに再計算させるのは無意味。

- [x]  **3.3.3 Skip stable variables from dependencies**

setOpenなどのstateのsetする関数は安定しているので依存配列に加えるべきでない

- [x]  **3.3.4 Get help maintaining dependency arrays**

# 4章 **Better code maintenance with developer tooling**

4章要約

ソースに基づくと、セクション 4は「Better code maintenance with developer tooling（開発ツールによるより良いコードメンテナンス）」というテーマで、コードの保守性を向上させるための**4つの主要な概念**と、それらを達成するのに役立つツールについて解説しています。

この章で伝えたい主要な点は以下の通りです。

- 第4章では、より良いコードメンテナンスのための**4つの指針**となる概念を紹介しています。
- これらの指針は、コードをチームメイトにコミットする**ずっと前にエラーや問題を発見**するのに役立ちます。
- 4つの主要な指針は以下の通りです:
    - **Linting（リンティング）**: ソースコードのマイナーなプログラム上およびスタイルのエラーを自動的にチェックするプロセスです。`eslint` というツールがこのタスクに使用されることが述べられています。変数名のスペルミスなども指摘できます。コード品質、コラボレーション、UX、DXに関連します。
    - **Formatting（フォーマット）**: セミコロンの有無、引用符の種類、改行、ブラケットやカッコ内のスペースなど、**純粋にスタイリングに関する選択**を扱います。これらのスタイリングの選択はコードのパフォーマンスには関係ありませんが、**開発者体験 (DX) とコラボレーションに大きく影響**します。プロジェクト内での一貫性が非常に重要であり、そうでなければ「純粋な無秩序につながる」と述べられています。`Prettier` は、これらのフォーマットを自動的に適用するツールとして紹介されています。フォーマットはコラボレーションとDXに影響します。
    - **PropTypes（プロパティ型）**: コンポーネントに渡されるプロパティの**期待される型を定義**するためのライブラリです。プリミティブ型（bool, string, numberなど）や複雑な型（func, array, objectなど）をサポートし、特定のスペル（例: `PropTypes.bool`, `PropTypes.func`）で定義されます。誤った型のプロパティがコンポーネントに渡された場合に警告を出すのに役立ちます。コード品質、コラボレーション、UX、DXに関連します。
    - **Debugging / Developer Tools（デバッグ／開発者ツール）**: React Developer Tools のようなツールを使用して、コンポーネントツリー内で何が起きているかを理解することです。これにより、なぜコンポーネントが頻繁に再レンダーされるのかなどを突き止めることができます。コード品質、コラボレーション、UX、DXに関連します。

これらのツールと概念をプロジェクトで適切に設定することで、開発プロセスにおいて問題が大きくなる前に効率的に特定し、修正できることが強調されています。

- [x]  **4.1 Reducing errors with linting**
- [x]  **4.1.1 Problems solved by ESLint**
- [x]  **4.1.2 ESLint configurations**

aribnbのガイド

[https://github.com/airbnb/javascript](https://github.com/airbnb/javascript)

- [x]  **4.1.3 How to get started using ESLint**

https://eslint.org/docs/latest/use/integrations

- [x]  **4.2 Increasing productivity with formatters**
- [x]  **4.2.1 Problems solved by Prettier**

自転車おきばの議論を減らせる。prettierで。

- [x]  **4.2.2 Nonstandard rules with Prettier configuration**
- [x]  **4.2.3 How to start using Prettier**

https://prettier.io/docs/editors.html

pre-commitでprettierかけるようにする方法

https://prettier.io/docs/precommit.html#option-4-git-format-staged

- [x]  **4.2.4 Alternative formatters**

- [x]  **4.3 Making components more robust with property constraints**

proptypesを使って、componentに渡ってくる値のチェックをする。

これはreact19ではもう用をなさなくなっているらしい。

これ、typescriptを使えば要らなくない？

→ 要らない。しかもreact19では消える仕組み。

https://chatgpt.com/g/g-p-6809be9401a081919a2241265bbfd78e-frontend/c/682454fb-1944-8009-9355-ebcbf6399f07

故に読まない。

- [x]  **4.4 Debugging applications with React Developer Tools**
- [x]  **4.4.1 Problems solved by debugging**
- [x]  **4.4.2 How to get started using React Developer Tools**
- [x]  **4.4.3 Using the components inspector in React Developer Tools**

propsとか、componentsから操作できないような気がするのだが → 開発環境ではできる。たぶんbuildするときになんかしてる。

- [x]  **4.4.4 Using the profiler in React Developer Tools**

profilerは扱うのが難しいっぽい

- [x]  **4.4.5 Alternatives and other tools**

[https://www.replay.io](https://www.replay.io/) 　is なん？

フロントのバグを再現するために用いるツールのよう

https://chatgpt.com/g/g-p-6809be9401a081919a2241265bbfd78e-frontend/c/68260afa-f9e8-8009-83c6-c8b6d190e3cd

https://www.youtube.com/watch?v=rak2PBNWsjE

# 5章 **TypeScript: Next-level JavaScript**

https://livebook.manning.com/book/react-in-depth/chapter-5/

ソースと会話履歴に基づくと、第5章「**TypeScript: Next-level JavaScript**」では、Reactアプリケーションの開発においてTypeScriptを使用することに焦点を当てています。この章の目的は、開発者がReactマスターへの道のり（本の図で「B」から「C」へ進む段階）において、TypeScriptを活用してコード品質、コラボレーション、ユーザーエクスペリエンス（UX）、開発者エクスペリエンス（DX）を向上させる方法を深く理解することです。

この章で伝えたい主要なポイントは以下の通りです。

- 第5章では、**TypeScriptを使用してJavaScriptのレベルを向上させる**方法を扱っています。
- TypeScriptを使用することで、コンポーネントに渡されるプロパティの期待される**型を定義**し、**ビルド前に型関連のエラーを発見**するのに役立ちます。
- 基本的な型付けとして、関数の引数の型をコロン(`:`)を使って指定する方法が示されています。
- コンポーネントのプロパティを型付けするために**インターフェース**を定義する方法が説明されています（例: `PersonProps`）。
- インターフェース内で**オプショナルなプロパティ**を定義するために`?`を使用する方法が紹介されています（例: `name?` や `age?`）。
- 従業員カードコンポーネントの例を通じて、実際のコンポーネントでTypeScriptを使用する方法が示されています。
- より高度なTypeScriptの概念として**ジェネリクス**が詳細に説明されています。
- ジェネリクスは、関数やコンポーネントが**特定の型に縛られず**に、**様々な型のデータと型安全に連携**できるようにするものです。`<Type>`のような山括弧記法を使用して定義されます。
- `getMiddle`関数の例を用いて、ジェネリクスがどのように異なる型の配列に対して型安全に動作し、TypeScriptが型エラーを検出するかが示されています。
- Reactのコンポーネントの子要素（`children`）の型付けについても触れられています。
- TypeScriptの**ユーティリティ型**が紹介されています。これらには、`PropsWithChildren`、`Omit`、`Pick`などがあり、既存の型を再利用・変換して新しい型を定義するのに役立ちます。
- `Omit`は既存の型から特定のプロパティを除外するために使用され、`Pick`は既存の型から特定のプロパティを選択するために使用されます。これらは、コンポーネントが別のコンポーネント（例えばボタンや評価コンポーネント）のプロパティを一部だけ受け取る場合に便利です。
- インターフェースを拡張する際には、元の型よりもプロパティを厳しくすることはできますが、**緩めることはできない**というTypeScriptのルールが説明されています（例: オプショナルなプロパティを必須にできない）。
- `ComponentPropsWithoutRef`のようなユーティリティ型を使用して、既存のReactコンポーネントのプロパティ型を抽出する方法も示されています。

総じて、第5章はReact開発者がTypeScriptを効果的に活用するための、基本的な型付けからジェネリクスやユーティリティ型といった高度な概念までを網羅しており、より堅牢で保守しやすいコードを書くための知識を提供しています。

- [x]  **5.1 The importance of TypeScript**
- [x]  **5.2 Introduction to TypeScript**
- [x]  **5.2.1 TypeScript files and React**
- [x]  **5.2.2 Static types**
- [x]  **5.2.3 Employee display**
- [x]  **5.2.4 Optional properties**

- [x]  **5.3 Advanced TypeScript with generics**
- [x]  **5.3.1 Understanding generic types**
- [x]  **5.3.2 Typing children**

  childrenの型にはPropsWithChildrenが利用できる。

  PropsWithChildren<HeadingProps>みたいな書き方をできる。

  childrenの型に何らかの制限をかけることはできない(TableRowの子どもにはTableCellのみ取りたい、みたいなことをtypescriptの型で制限することはできない。)

- [x]  **5.3.3 Extending interfaces**

  PickとかOmitを使って型をextendsすることができる

- [x]  **5.3.4 Spreading props in general**

  組み込みのhtmlタグに渡せるpropsを拡張したい時には、 ComponentPropsWithoutRef が使える。 ComponentPropsWithoutRef<"img"> のような感じ。

  カスタムpropsにおいて同様のことをする場合は、 typeof を利用する。 ComponentPropsWithoutRef<typeof Rating> のような感じ。


- [x]  **5.3.5 Restricting and loosening types**

  同名のプロパティの型を緩めたい場合は、同名をomitして、それと同じ名前で再度定義するようにすれば良い。

   ```clojure
   interface AnyStyle extends Omit<Style, "width"> {
     width: number | string | null;
   }
   ```

- [x]  **5.3.6 Using optional and required properties**

optionalプロパティを必須にするようにextendsするに際して、シンプルにやるならその定義を宇和がいてやれば良い

```clojure
interface StringInputProps extends ComponentPropsWithoutRef<"input"> {
  value: string;
}
```

その逆はできない。やりたいなら、5.3.5のようなことをする。

optionalプロパティを複数requireにしたい場合は上記の方法だと煩雑になるので、下記のようにRequire<T>を使うのが良い。

```clojure
type ButtonProps = ComponentPropsWithoutRef<"button">;
type RequireSome<T, K extends keyof T> = T & Required<Pick<T, K>>
type HoverButtonProps = RequireSome<
  ButtonProps,
  "onMouseOver" | "onMouseMove" | "onMouseOut"
>;type ButtonProps = ComponentPropsWithoutRef<"button">;
type RequireSome<T, K extends keyof T> = T & Required<Pick<T, K>>
type HoverButtonProps = RequireSome<
  ButtonProps,
  "onMouseOver" | "onMouseMove" | "onMouseOut"
>;
```

- [ ]  **5.3.7 Using either/or properties**

判別可能なunion型を使って、型の判別ができる https://typescriptbook.jp/reference/values-types-variables/discriminated-union#%E5%88%A4%E5%88%A5%E5%8F%AF%E8%83%BD%E3%81%AA%E3%83%A6%E3%83%8B%E3%82%AA%E3%83%B3%E5%9E%8B%E3%81%A8%E3%81%AF

判別可能なユニオン型を使うことによって、いわゆる直和を表現できる

ただ、discriminated unionを利用した時にspread propsは使えない

```clojure
interface BaseProps {
  productName: string;
  price: number;
}
interface ProductCardSaleProps {
  isOnSale: true;
  salePrice: number;
  saleExpiry: string;
}
interface ProductCardNoSaleProps {
  isOnSale: false;
}
type ProductCardProps = BaseProps &
  (ProductCardSaleProps |
   ProductCardNoSaleProps);
```

- [x]  **5.3.8 Forwarding refs**

react 19ではもはや重要ではないらしい。

昔はrefを渡すときにforwardRefを挟まないといけなかった模様。

# 6章 **Mastering TypeScript with React**

提供された情報に基づくと、第6章は「ReactとTypeScriptを習得する（Mastering TypeScript with React）」というタイトルです。

この章の抜粋から得られる内容は以下の通りです。

- **ReactフックをTypeScriptで型付けする**方法について説明されています。
    - `useState`フックにおける、`null`または`boolean`のような単純な値の型付け。
    - `useState`フックにおける配列の型付け。
    - `useState`フックにおけるオブジェクトの型付け。
- **コンテキストと`useContext`の型付け**について触れられています。
    - シンプルおよび複雑なコンテキストの型付けについて、シンプルなものは型付けが容易である一方、複雑なものはそうではないと述べられています。第2章で触れられたセレクターベースのコンテキストにも関連します。
- **ジェネリックなページネーションの例**が紹介されています。
    - これは、第5章で作成された従業員カードのリスト や、ハイスコアリストなど、異なる種類のコンテンツに対して同様の機能（ページネーション）を適用する方法を示すためのものです。
    - 適切なインターフェースに従う限り、異なる型のオブジェクトに同じ機能を適用するためにジェネリックを使用する方法が示されています。
    - このコードは複雑であると述べられており、全体を完全に理解できなくても問題ない、さらなる情報探索へのインスピレーションを与えるための例だと説明されています。

## 6.1 **Using React hooks in TypeScript**

- [x]  **6.1.1 Typing useState**

こんな感じでisAcceptedをnull or boolean にできる

```clojure
const [isAccepted, setIsAccepted] = useState<null | boolean>(null);
```

stateに配列を持つときはこんな感じ。

```clojure
const [tags, setTags] = useState<string[]>([]);
```

record interfaceなるものがある。

https://typescriptbook.jp/reference/type-reuse/utility-types/record

- [x]  **6.1.2 Typing useRef**
- [x]  **6.1.3 Typing contexts and useContext**
- [x]  **6.1.4 Typing effects**

useEffectのクリーンアップ関数としてfalseを返すようなことをすると、typescriptではエラーになる。その場合は return; を返せば良い。

Destructorとはなんだ？ ⇒ 後片付け用の関数のことを指している

```clojure
type Destructor = () => void | { [UNDEFINED_VOID_ONLY]: never };cod
```

- [x]  **6.1.5 Typing reducers**

https://ja.react.dev/blog/2024/04/25/react-19-upgrade-guide#better-usereducer-typings

- [x]  **6.1.6 Typing memoization hooks**

useCallbackでのtypingについての説明

react compilerでmemo系hookは不要になる可能性がある

- [x]  **6.1.7 Typing the remaining hooks**

説明なし

## **6.2 Generic pagination: An example**

汎用的なpagination部品を作る例。異なった要素でもpaginationできるような部品を作成していく。

- [x]  **6.2.1 Forwarding a reference to a generic component**
- [x]  **6.2.2 Memoizing a generic component**

あんまよくわからん

- [x]  **6.3 Drawbacks of using TypeScript**

欠点らしい欠点はない

- [x]  6.4 TypeScript resources

# 7章 **CSS in JavaScript**

ソースに基づいた第7章の要約を提供します。

第7章は**Reactアプリケーションのスタイリング**に焦点を当てています。この章では、アプリケーションを美しく見せること、さまざまなスタイリング方法を評価すること、そしてコンポーネントをスタイリングする**3つの方法**を探求することを扱っています。

ソースによると、Reactアプリケーションをスタイリングする「最善の方法」は**未解決の問題**であり、プロジェクト、開発チーム、対象ユーザー、個人の好みや専門的な意見など、多くの要件によって最適なソリューションが異なります。

第7章では、`<img>`や`<iframe>`などの要素に対して発火する`onLoad`や`onError`といったイベントハンドラ関数についても言及されていますが、これらはブラウザイベントとは異なり、Reactではバブルアップします。

また、この章では、疑似クラスや疑似要素、そしてメディアクエリなどのアットルール（@記号で始まるCSSルール）といった特定のCSS機能はインラインで適用できず、CSSブロックに配置する必要があることが説明されています。アットルールは、しばしば1つまたは2つの要素に限定されず、グループの要素に対して機能します。

章全体で使用される例示プロジェクトとして、**ボタンアプリケーション**が紹介されています。

第7章では、**styled-components**というスタイリング手法が導入されています。これは、CSSファイルを不要にし、JavaScriptファイル内で直接CSSを使ってコンポーネントを定義できるようにするものです。基本的な考え方は、CSSファイルから直接HTML要素とクラスをコンポーネントとしてインポートするようなものです。styled-componentsは**タグ付きテンプレートリテラル**を使用します。styled-componentsは、キーフレームやメディアクエリのような高度なCSS機能、およびグローバルCSSルールを適用するための関数もサポートしています。

章の最後では、インラインCSS、CSSファイル、CSS Modules、Styled-components、Tailwind CSSといった**さまざまなCSS手法**を、特異性、衝突、コンポジションといった属性に基づいて比較した表が提供されています。styled-componentsは衝突とコンポジションにおいて有利に評価されている一方、特異性については中立的/混在しているとされています。


---

## 7.1 Styling with concerns

- [x] 7.1.1 CSS language features

cssの特徴について述べてる。

- [x] 7.1.2 Developer experience

- [x] 7.1.3 Web application development

- [x] 7.1.4 Why not inline styles?

- [x] 7.1.5 What about existing UI libraries?

## 7.2 The example button application

## 7.3 Method 1: CSS files and class names

cssを別ファイルに切り出す方法(cssをjsの中に入れない)についてのpros/consを論じる。

- [x] 7.3.1 How class names work
- [x] 7.3.2 Setup for class name project
- [x] 7.3.3 Implementation with class names
- [x] 7.3.4 Strengths of the class names approach

- [x] 7.3.5 Weaknesses of the class names approach

cssとjsの同期ができない。
当てるべきスタイルの衝突が起きる。

- [x] 7.3.6 When (not) to use CSS files and class names

小規模で向いてるとのこと

## 7.4 Method 2: CSS Modules

- [x] 7.4.1 How CSS Modules work

*.module.css というファイルをコンパイルして、各コンポーネントごとに固有のcssを作る感じ。

- [x] 7.4.2 Setup for CSS Modules project

viteであればdefaultで対応している。
webpackであれば、css-loaderを使う。

- [x] 7.4.3 Source code with CSS Modules

- [x] 7.4.4 Strengths of CSS Modules

importして使うので、cssとjsの同期が取れる。
class名の衝突が起きない。

- [x] 7.4.5 Weaknesses of CSS Modules

ゆうてもcssとjsのファイルが別なので、行ったり来たりする必要がある。
動的な値に対しては、inline styleを使う必要がある。
最終的なoutputのspecificityの問題が依然としてある。

- [x] 7.4.6 When (not) to use CSS Modules

大規模なところでも使われていたりする。

## 7.5 Method 3: Styled-components

- [x] 7.5.1 How styled-components works

jsの中に、バッククォートを駆使したタグ付きテンプレートリテラルを使って、cssを記述する

- [x] 7.5.2 Setup for styled-components project

styled-componentsは、npmでインストールできる。

- [x] 7.5.3 Source code with styled-components

jsxとcssが同じファイルに書ける。
それゆえ、1つのファイルは長くなりがち。

- [x] 7.5.4 Strengths of styled-components

- [x] 7.5.5 Weaknesses of styled-components

- [x] 7.5.6 When (not) to use styled-components

## 7.6 One problem, infinite solutions

この章では下記の方法を紹介した。
- Inline CSS
- CSS files and class names
- CSS Modules
- Styled-components
- Tailwind CSS


これらについて、星取表を用意してくれてる。
筆者的には styled-componentsが一番良いらしい。


# 8 Data management in React

提供されたソースと会話履歴に基づき、第8章の要約をいたします。

第8章「Reactにおけるデータ管理」では、**Reactアプリケーションにおけるデータの保管、読み取り、変更のプロセス**（ローカルでのデータ管理）について論じられています。アプリケーションに多数のデータを扱い、複雑な方法で操作する必要がある場合、その管理方法について慎重に考える必要があると述べられています。

この章の目的は、データ管理の重要性を紹介し、様々なデータ管理ライブラリを評価することです。特に、アプリケーションのデータ層を5つの異なる方法で構築することに焦点が当てられています。プレゼンテーション層はそのままにし、データ層のみを変更することで、この目的を達成しています。

例として使用されるアプリケーションは、**「100回やる目標トラッキング」アプリケーション**です。これは、do100things.comに触発されており、ユーザーが何かを100回行った回数を記録できます。最終製品は100.bingoに似ています。

アプリケーションのアーキテクチャは、プレゼンテーション層（`things`）とデータ層（`data`）に分割されています。メインの`App`コンポーネントがこれらを結合します。プレゼンテーション層は、リストビューと単一アイテムの詳細ビューという2つのビューを持ち、これらは様々なコンポーネントで構成されています。

データ層とプレゼンテーション層間のやり取りは、APIを公開する4つのカスタムフックを通じて行われます。
*   `useCurrentThing`: 現在表示されている単一アイテムのID、またはリストビューの場合は`null`を返します。
*   `useAllThings`: すべてのアイテムのIDの配列を返します。
*   `useAddThing`: 新しいアイテムを追加する関数を返します。
*   `useThing(id)`: アイテムのデータと、そのアイテムを操作するための関数（`seeThing`, `seeAllThings`, `doThing`, `undoThing`, `undoLastThing`, `removeThing`）を含むオブジェクトを返します。

データは、アプリケーションを表示しているコンピューターのローカルに永続化する必要があります。

章では、以下の5つのデータ管理方法の実装とそのソースコードが示されています（詳細な解説は他の方法に譲りつつ、コード例は提供されています）。

1.  **Pure React (useState + Context)**:
  *   `useState`を使用してデータを管理し、Contextを使ってProviderパターンでアプリケーション全体に配布します。
  *   すべてのデータ保管と操作は`DataProvider.jsx`で行われ、Contextからのデータ取得は`useContext`ラッパーである`useData.js`を通じて行われます。
  *   ローカル永続化は`useEffect`と`localStorage`を使って手動で行われます。
  *   Context全体の値を変更すると、Contextを使用するすべてのコンポーネントが再レンダリングされる可能性があります。複雑なロジックには不向きですが、シンプルな値には適しています。

2.  **Reducing data state (useReduction + useContextSelector + Immer)**:
  *   Providerパターンを使用します。
  *   `useReduction`（レデューサーの定型コードを削減）、`useContextSelector`（Contextの部分的な消費で再レンダリングを最小化）、そして**Immer**（`produce()`を使用してミュータブルなコードでイミュータブルな更新を記述）といったユーティリティライブラリを導入します。
  *   これにより、コードがより簡潔で効率的になります。ローカル永続化は手動ですが、結合された状態オブジェクトを扱うためより容易です。

3.  **Redux Toolkit (RTK)**:
  *   Reduxは、ストアと、アクションによって起動されるレデューサーで構成されるサイクルを持ちます。RTKでは、これらを「スライス」としてまとめて定義します。
  *   Reduxは、内部的にReact Contextを使用する独自のプロバイダー、および`useSelector`、`useDispatch`といったフックを提供します。
  *   RTKにはImmerが組み込まれています。
  *   データ永続化のために、`store.subscribe`を使用してストアの状態変更を監視し、`localStorage`に保存します。
  *   Reduxは成熟しており、実績がありますが、RTKを使ってもなお定型コードが少し存在します。

4.  **Zustand**:
  *   Reduxよりも「ベアボーン」な代替手段として紹介されています。
  *   `create()`という単一の関数があり、これを使用する場所に関係なく同じ状態とアクションを共有するフックを返します。
  *   Contextやプロバイダーは別途必要なく、状態はフック内部に存在します。
  *   Zustandは、Immerをミドルウェアとしてバンドルできます。また、永続化(`persist()`)機能も組み込まれています。
  *   非常にシンプルですが、関連性のない複数のデータストアを整理するためのツールやパターンが組み込まれていないため、大規模での使用はより複雑になる可能性があります。

5.  **XState (State Machine)**:
  *   完全に異なるアプローチで、フロー管理のために状態マシンを使用し、その「コンテキスト」にデータ管理機能が組み込まれています。
  *   状態マシンは`createMachine`で作成され、状態（`list`, `single`）と遷移（`DO_THAT`, `SEE`など）を管理します。
  *   データプロバイダーは、`useInterpret`を使用して状態マシンをラップする役割を担います。
  *   データ永続化は、状態マシン全体の状態（コンテキストを含む）を`localStorage`に保存することで行われます。
  *   この方法は、状態遷移について深く考えることを強制し、バグを減らすのに役立ちます。異なる状態に応じて異なる関数が必要になるため、標準の`useThing`フックは`useThatThing`（リストビュー用）と`useThisThing`（詳細ビュー用）に分割されました。

章のまとめ（8.8節）では、これらの5つの方法を振り返り、他にもJotai、Recoil、Valtioといった代替手段があることを示唆しています。そして、基盤となるデータ管理ライブラリは、コードにわずかな変更を加えるだけで、ほぼすべてのプレゼンテーションコードをそのままに置き換えることができるため、**最初に誤った選択をしても後で変更可能である**と強調しています。最終的に、どのツールを選択するかは、開発者の快適さによると述べられています。


---

## 8.1 Creating a goal-tracking application

100回やることを支援するアプリを作る。
https://100.bingo これが完成系。


## 8.2 Building the application architecture

## 8.3 Managing data in pure React

- [x] 8.3.1 Context

- [x] 8.3.2 Source code

https://www.reactindepth.dev/browse/ch08/context/browse

仕組みをちゃんと見れば理解はできるが、これを自分で書くのはちょっと訓練が入りそう。

providerが中身にcontextを持っている形。


## 8.4 Reducing data state

- [x] 8.4.1 Immer: Writing immutable code mutably

immerを利用すればmutableにstateの更新を記述できる。
これはreactの公式文章にも書いてある。

- [ ] 8.4.2 Source code

useReductionという謎ライブラリを使っている。
下記のような違いで、useReducerを使って公式に従った方が良い。
---

### ざっくり結論

|              | `useReduction`                                                  | React 組み込み `useReducer`                                    |
| ------------ | --------------------------------------------------------------- | ---------------------------------------------------------- |
| 呼び出し結果       | `[state, actions]`（**アクションクリエータの集合**）                           | `[state, dispatch]`（**dispatch 関数**）                       |
| reducer の書き方 | `{ actionName: (state, {payload}) => newState }` という **オブジェクト** | `(state, action) => newState` という **関数**                   |
| アクション送信      | `actions.increment(2)` のように **関数呼び出し**                          | `dispatch({type:'increment', payload:2})` と **オブジェクトを手書き** |
| ボイラープレート     | 少ない（`switch` やアクション型定義不要）                                       | 自前で `switch` 文・アクションクリエータを用意しがち                            |
| デバッグ支援       | 第3引数 `true` で **自動ログ出力**                                        | 標準では無し（自分で `console.log` を挟む）                              |
| 依存関係         | 外部ライブラリ（Stars ≒ 40・最終コミット 2023-02）                              | React 本体のみ                                                 |
| 実装概要         | 内部で `useReducer` を呼び出し、渡されたオブジェクトから action creator を自動生成        | 純粋に reducer 関数と dispatch を返すだけ                             |

([github.com][1], [react.dev][2])

---

## コード比較で見る違い

### `useReducer` 版（素の React）

```tsx
const reducer = (state: number, action: {type: 'inc'|'dec'; payload: number}) => {
  switch (action.type) {
    case 'inc': return state + action.payload;
    case 'dec': return state - action.payload;
    default:     return state;
  }
};

const [count, dispatch] = React.useReducer(reducer, 0);

<button onClick={() => dispatch({type: 'inc', payload: 2})}>+2</button>
```

* アクションオブジェクトを毎回手で書く
* 型定義・`switch` がやや冗長

---

### `useReduction` 版

```tsx
import useReduction from 'use-reduction';

const [count, actions] = useReduction(0, {
  inc: (c, {payload}: {payload: number}) => c + payload,
  dec: (c, {payload}: {payload: number}) => c - payload,
});

<button onClick={() => actions.inc(2)}>+2</button>
```

* reducer を “アクション名 ⇒ ハンドラ” の **マップ** で渡す
* `actions.inc` が自動生成され、第一引数が `payload` になる
* `useReduction(…, …, true)` にすると `console.log({type:'inc', payload:2})` を吐く

---

## どちらを選ぶ？

| シチュエーション                          | 向いている選択肢                                       | 理由                                          |
| --------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| **ローカルな UI 状態**を素早く書きたい           | `useReduction`                                 | action creator 自動生成で記述量が減る                  |
| **公式 API だけで完結**させたい / 依存を増やしたくない | `useReducer`                                   | React だけで足りる                                |
| 複数ファイルに **dispatch を伝搬**して使う      | `useReducer`                                   | dispatch は関数 1 つなので Context などに載せやすい        |
| **型安全**に大量のアクションを扱う               | どちらも可だが `useReduction` は union 型を自分で組まなくて済むため楽 |                                             |
| **長期保守** / ライブラリの活動状況が気になる        | `useReducer`                                   | `useReduction` は小規模 OSS（Star ≒ 40, コミット少なめ） |

---

## まとめ

* **機能面では `useReduction` は単に “アクションクリエータ生成器付き `useReducer`”**。内部実装も `useReducer` を呼んでいるだけなのでパフォーマンスや React の仕組みは変わりません。
* ボイラープレートが減る一方、**依存が増える・ドキュメントが少ない** というトレードオフがあります。
* 小〜中規模の UI コンポーネントで「action オブジェクトを書くのが面倒」と感じたときに導入するイメージです。大規模な状態管理やチーム開発なら、公式のまま + 独自ヘルパー or Redux Toolkit の方が通りが良いことも多いでしょう。

これで違いのイメージを掴んでいただければ幸いです！

[1]: https://github.com/anater/useReduction "GitHub - anater/useReduction: useReducer without boilerplate"
[2]: https://react.dev/reference/react/useReducer?utm_source=chatgpt.com "useReducer - React"

----


# 8.5 Scaling data management with Redux Toolkit
