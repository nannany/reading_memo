# この本の構成

最初の1，2章でセキュリティ一般のことを述べる。  

3章以降ではSpringSecuriｔｙを使うにあたって必要な項目を細かく見ていく。

3章はユーザーマネージメントについて学ぶ。

4章はユーザーのパスワードについて学ぶ。

5章は認証のロジックについて学ぶ。

6章は2章から5章のハンズオンを行う。

7章は認可の設定について論じる。

8章は具体的に認可のHTTPリクエストについてみていく。

9章は


## 20201128

2章。ハンズオン  
ベーシック認証 ⇒ デフォルトで入れてくる

2.2 の図がすごい分かりやすい

WebSecurityConfigurationAdapter
で動きを定義

InMemoryUserDetailsManager ⇒ どっちかというとテスト用

UserDetailsManager ⇒ 作ったり、削除したり
⇒ こいつを継承してDBに保存したりだとか。

UserDetails ⇒ こいつを継承なりして、めーるアドレスを持たせたりする。

ログインのログをfilter部分でできたり

# 2. Hello Spring Security

Spring Security の最初のステップ


## 20201226

勉強会。
3章を学ぶ。
UserDetails周りの扱いを学べた。 

## 20201227

勉強会のとこまで追いつくようにする。

1章サマリの翻訳

* Spring Securityは、Springアプリケーションのセキュリティを確保するための主要な選択肢です。さまざまなスタイルやアーキテクチャに適用される多くの選択肢を提供しています。
* セキュリティはシステムのレイヤーに分けて適用する必要があり、レイヤーごとに異なるプラクティスを使用する必要があります。
* セキュリティは、ソフトウェアプロジェクトの最初から考慮すべき横断的な懸念事項です。
* 通常、攻撃のコストは、そもそも脆弱性を回避するための投資コストよりも高くなります。
* Open Web Application Security Projectは、脆弱性やセキュリティに関する懸念事項に関しては、参考になる素晴らしい場所です。
* 時には小さなミスが大きな被害をもたらすこともあります。例えば、ログやエラーメッセージを通して機密データを公開することは、アプリケーションに脆弱性を導入する一般的な方法です。

### 2章

モノリシックなアプリなら、Springの重厚な設定は一か所にすればよかったんだけど、マイクロサービスになって、それらを書くコストが顕在化してきた。  
そこでSpringBootの登場

SpringSecurityの各構成要素の概念図？みたいなものが重要っぽい

* 認証フィルタは、認証要求を認証マネージャに委任し、その応答に基づいてセキュリティコンテキストを構成します。
* 認証マネージャは、認証プロバイダを使用して認証を処理します。
* 認証プロバイダは、認証ロジックを実装します。
* ユーザ詳細サービスは、ユーザ管理責任を実装し、認証プロバイダは認証ロジックで使用します。
* パスワードエンコーダーは、パスワード管理を実装しており、認証プロバイダは認証ロジックで使用します。
* セキュリティコンテキストは、認証処理後の認証データを保持します。

UserDetailsServiceのBean定義をした際に、PasswordEncoderのBean定義が必要なのはなんで？

次2．3.1から

## 20201229

* Spring Security in actionの2.3.1において、 UserDetailsManagerのBean定義のみしたら、なぜPasswordEncoderがなくて怒られるのか？

次は2.3.4から

## 20201230

2.3.4 にて、基本的にSpring Security側で想定されている責務配置に逆らわないこと。

configuration クラスも責務によって分けること


2章まとめ

* Spring Bootは、アプリケーションの依存関係にSpring Securityを追加する際に、いくつかのデフォルト設定を提供します。
* 認証と認可のための基本的なコンポーネントを実装します。UserDetailsService、PasswordEncoder、AuthenticationProviderです。
* Userクラスでユーザーを定義することができます。ユーザーは、少なくともユーザー名、パスワード、および権限を持つ必要があります。権限とは、アプリケーションのコンテキストでユーザに実行させるアクションのことです。
* Spring Securityが提供するUserDetailsServiceの簡単な実装はInMemoryUserDetailsManagerです。このようなUserDetailsServiceのインスタンスにユーザーを追加して、アプリケーションのメモリ上でユーザーを管理することができます。
* NoOpPasswordEncoderはパスワードを平文で使うPasswordEncoder契約の実装です。この実装は、例を学習したり、(たぶん)概念を証明するのには適していますが、本番さながらのアプリケーションには適していません。
* AuthenticationProvider 契約を使用して、アプリケーションにカスタム認証ロジックを実装することができます。
* 設定を書く方法は複数ありますが、1つのアプリケーションでは、1つのアプローチを選択し、それに固執するべきです。そうすることで、コードがすっきりして理解しやすくなります。


### 3章

UserはUserDetailsを実装したクラス

### 4章 パスワードを扱う

* PasswordEncoderについてみていく
* Spring Securityが提供する暗号モジュールを見ていく

3章までで、クライアントから渡されたユーザーの情報を引っ張ってくるまでの動作を見ていた。  
AuthenticationProvider は　PasswordEncoderを使ってパスワードの検証をする。

PasswordEncoderが用意しているメソッドは、`encode` `matches`の2つ。  
`upgradeEncoding`は何者？

* PasswordEncoderは、認証ロジックの中で最も重要な責任の一つを担っています。
* Spring Securityはハッシュアルゴリズムにいくつかの選択肢を提供しており、実装は選択の問題となっています。
* Spring Security Cryptoモジュール(SSCM)は、鍵生成器と暗号化器の実装に様々な選択肢を提供します。
* キージェネレータは、暗号化アルゴリズムで使用される鍵の生成を支援するユーティリティオブジェクトです。
* 暗号化器は、データの暗号化と復号化を適用するのに役立つユーティリティオブジェクトです。


# 20201231

まとめる

### 4.1.1 PasswordEncoderのIFについて理解する

```java
public interface PasswordEncoder {

  String encode(CharSequence rawPassword);
  boolean matches(CharSequence rawPassword, String encodedPassword);

  default boolean upgradeEncoding(String encodedPassword) { 
    return false; 
  }
}
```

encodeは、与えられたパスワードの文字列を特定のハッシュ関数などでエンコードすることを目的としている。  
matchesは、受け取ったパスワードとエンコードされたパスワードの検証を目的としてる。

upgradeEncodingは、受け取ったエンコード済みのパスワードを再度エンコードかけるかどうかを判断することを目的としている。

### 4.1.2 自前でPasswordEncoderを実装する

自前でPasswordEncoderを実装する方針を取って見せている。

### 4.1.3 Springが用意してるPasswordEncoderの実装を使う

* NoOpPasswordEncoder-- パスワードをエンコードせず、平文で保持します。この実装は例としてのみ使用します。パスワードをハッシュ化しないので、実世界のシナリオでは決して使用すべきではありません。
* StandardPasswordEncoder-- パスワードのハッシュ化に SHA-256 を使用します。この実装は現在非推奨となっており、新しい実装では使用すべきではありません。なぜ非推奨なのかというと、もう十分に強力ではないと考えられるハッシュアルゴリズムを使用しているからです。
* Pbkdf2PasswordEncoder--パスワードベースのキー導出関数 2 (PBKDF2) を使用します。
* BCryptPasswordEncoder--パスワードをエンコードするために bcrypt 強力ハッシュ関数を使用します。
* SCryptPasswordEncoder-- パスワードをエンコードするために scrypt ハッシュ関数を使用します。

NoOpとStandardは非推奨

### 4.1.4 DelegatingPasswordEncoderについて

途中で暗号化の方式が変わったりした時には、このPasswordEncoderを用いる。

encodingとencryptingとhashingの違い
ここはとばす。


## 4.2 Spring Security Crypto module(sscm)について

### 4.2.1 key generator キー生成

Spring Securityが提供するキー生成部品について

### 4.2.2 encryptors 暗号と復号

TextEncryptor と ByteEncryptor がある。同じ責務だけど、input,outputが違う

Encryptorを生成するのには、Encryptorsを利用する。

ByteEncryptorを生成するのは  
* `Encryptors.standard()` 
* `Encryptors.stronger()`
で、その名の通りstrongerのほうが強度の強い暗号化ができる

TextEncryptor を生成するのは、

* Encryptors.text()
* Encryptors.delux()
* Encryptors.queryableText()
の3つ。 Encryptors.noOpText() もあるけどこれはテスト用。
`text`は内部で上のstandardを使っていて、`delux`はstrongerを使っている
queryableTextを使うと、同じプロセスで暗号化した場合には、同じ値になる。

# 20210102

## 5.1 AuthenticationProviderについて

フレームワークを使う際に気を付けることが書いてあり、共感できる内容であった。

* フレームワーク、特にアプリケーションで広く使われているものは、多くの頭の良い個人が参加して書かれています。そうであっても、フレームワークが不適切に実装されることがあるとは考えにくいでしょう。問題があればフレームワークのせいだと結論づける前に、常にアプリケーションを分析してください。
* フレームワークを使うことを決めるときは、少なくともその基本をよく理解していることを確認してください。
* フレームワークについて学ぶために使うリソースに注意してください。ウェブ上で見つけた記事には、手っ取り早く回避策を行う方法が書かれていることがありますが、必ずしもクラスデザインを正しく実装する方法が書かれているとは限りません。
* 研究には複数のソースを使いましょう。誤解を明らかにするために、何かをどのように使うかわからないときには、概念実証を書きましょう。
* フレームワークを使うと決めた場合は、そのフレームワークの意図した目的のために可能な限り使いましょう。例えば、あなたがSpring Securityを使っていて、セキュリティ実装のためにフレームワークの提供するものに頼らずにカスタムコードを書く傾向があるとします。なぜこのようなことが起こるのか、質問を投げかけてみてください。

# 20210109 

## 5.1 AuthenticationProviderについて

5.1.1ではSpringSecurityが認証をどう表現するか見ていく  
5.1.2ではAuthenticationProviderのIFを見ていく  
5.1.3ではカスタム↓AuthenticationProviderをみていく

### 5.1.1 Authenticationの表現方法

AuthenticationはPrincipalを継承している

```java
public interface Authentication extends Principal, Serializable {

  Collection<? extends GrantedAuthority> getAuthorities();
  Object getCredentials();
  Object getDetails();
  Object getPrincipal();
  boolean isAuthenticated();
  void setAuthenticated(boolean isAuthenticated) 
     throws IllegalArgumentException;
}
```

### 5.1.2 

# 20210221

# 7

認可の話をしていく

##　7.1 
この章では認可とロールの話をしていく。

`UserDetails`には`GrantedAuthority`が複数含まれている。

`GrantedAuthority`のインターフェースはこんな感じ。
```java
public interface GrantedAuthority extends Serializable {
  String getAuthority();
}
```

`UserDetails`では`GrantedAuthority`のリストを返すようになっている。

```java
public interface UserDetails extends Serializable {
  Collection<? extends GrantedAuthority> getAuthorities();

  // Omitted code
}
```

### 7.1.1 Restricting access for all endpoints based on user authorities

すべてのエンドポイントについて、ユーザーの権限でアクセス制御する例をみせている。

下記のメソッドを使ってアクセス制御する例をみせている。
* `hasAuthority`
* `hasAnyAuthority`
* `access`

accessはSpEL(Spring Expression Language)を利用して柔軟に記述することができるが、複雑になる可能性も高まるので、hasAnyAuthority、hasAuthority で対応するのが望ましい。

### 7.1.2 Restricting access for all endpoints based on user roles

authorityが複数集まって形成されるのがrole。

この章では、Userへのroleの付与の仕方を扱っている。`ROLE_`を付与する必要があるか、いらないか、みたいなことを書いてる。

### 7.1.3 Restricting access to all endpoints

`denyAll`を利用して、すべてのリクエストをはじくことができる。
これをどこで利用するかの例
* パスパラメータ内にメールアドレスが入ってくるようなリクエストがあったとして、`.com`で終わるアドレスのみを許可したいときに使う(それ以外はdenyAllではじく)
* 一つのサービスを2つのゲートウェイから共有するときに、各ゲートウェイごとに特定のパスへのアクセスは禁止させたい場合


#### まとめ

* 認可とは、アプリケーションが認証されたリクエストが許可されているかどうかを決定するプロセスです。認可は常に認証の後に行われます。
* 認証済みユーザーの権限と役割に基づいて、アプリケーションがどのようにリクエストを認可するかを設定します。
* アプリケーションでは、認証されていないユーザーに対して特定の要求が可能であることを指定することもできます。
* アプリでは、denyAll() メソッドを使用してすべての要求を拒否したり、 permitAll() メソッドを使用してすべての要求を許可したりするように構成できます。


# 8

この章では、各リクエストごとに異なった制御の仕方をできるようにする。リクエストを見分けるために、下記のmatcherを使う。

* MVC matchers 
* Ant matchers
* regex matchers

## 8.1 Using matcher methods to select endpoints

* ルールは明示的に記述するべき。
* ルールの記述は細かいものから書いて包括的なものは後に書く。

`hola`のエンドポイントに関しては、permitAllの挙動になっている。  
こちらは、ユーザーパスワードなしだと普通に200が返るが、登録されていないユーザー、パスワードでリクエストすると401が返される。

## 8.2 Selecting requests for authorization using MVC matchers

```
mvcMatchers(HttpMethod method, String... patterns)
mvcMatchers(String... patterns)
```

## 8.3 Selecting requests for authorization using Ant matchers

```
antMatchers(HttpMethod method, String patterns)
antMatchers(String patterns)
antMatchers(HttpMethod method)
```

## 8.4 Selecting requests for authorization using regex matchers

```
regexMatchers(HttpMethod method, String regex)
regexMatchers(String regex)
```

#### まとめ

* 実際のシナリオでは、異なる要求に対して異なる認証規則を適用することがよくあります。
* パスと HTTP メソッドに基づいて認証ルールが設定されているリクエストを指定します。これを行うには、Matcher メソッドを使用します。MVC、Ant および regex です。
* MVC マッチャと Ant マッチャは似たようなもので、一般的にはこれらのオプションのいずれかを選択して、 認証制限を適用するリクエストを参照することができます。
* 要件が複雑すぎて Ant や MVC 式では解決できない場合は、より強力な正規表現を使用して実装することができます。


# 20210304 
一枚の画として、SpringSecurityの全体像を表現できるとよいと感じた。
Filterは3章あたりで出てきたAuthenticationFilterの抽象度を上げたものと理解できる。

# 9. Implementing filters 

Filterについてみていく

FilterはManagerクラスに処理を預けることが多い。Filterの処理が終わったら、次のFilterが動き出す。

## 9.1 Implementing filters in the Spring Security architecture

* ServletRequest
* ServletResponse
* FilterChain
をFilterではパラメータとして扱う。
  
SpringSecurityが用意してくれているFilterとしては以下のようなものがある。

* BasicAuthenticationFilter
* CsrfFilter
* CorsFilter

Orderでどの順番でFilterをかけるか決められる。

## 9.2 Adding a filter before an existing one in the chain

BasicAuthenticationFilterの前にカスタムフィルターを置く方法を論じている

## 9.3 Adding a filter after an existing one in the chain

ここでは9.2とは反対に、後にFilterを付け足す方法を論じている

9.2,9.3のコードがssia-ch9-ex1。

## 9.4 Adding a filter at the location of another in the chain

この章ではフィルターチェーンの中にフィルターを組み込んでいく。

authentication部分をオリジナルのフィルターにしてみる。
認証の典型的なパターンとしては以下のようなものがある。

* 特定のheaderの値をもとに認証をする
* 鍵を利用して作成した署名をもとに認証する
* ワンタイムパスワードを利用して認証する

例としては一番目の特定の値による認証を行う。

フィルターを同じポジションに置いた場合は適用の順番が不定になるので、フィルターの順番はちゃんと決めること。

9.4のコードがssia-ch9-ex2
このコードはorderが一緒になっているけど、本当はしないほうがいい。

## 9.5 Filter implementations provided by Spring Security

SpringSecurity提供のFilterを使うと便利。

OncePerRequestFilterでは、
* HttpServletRequestにキャスト不要。(HTTPのリクエストにしか対応してないけど、ほとんどこれ使う)
* filterが適応されない場合をロジックで定義することができる(shouldNotFilter) 
* デフォルトでは非同期リクエストやエラーディスパッチリクエストには適用されないが、用意されているメソッドをoverrideすることで変更可能

9.5のコードがssia-ch9-ex3

## まとめ

* HTTPリクエストをインターセプトするWebアプリケーションアーキテクチャの第1層は、フィルターチェーンです。Spring Securityアーキテクチャの他のコンポーネントと同様に、要件に合わせてカスタマイズすることができます。
* 既存のフィルタの前、既存のフィルタの後、または既存のフィルタの位置に新しいフィルタを追加することで、フィルタチェーンをカスタマイズすることができます。
* 既存のフィルタの同じ位置に複数のフィルタを持つことができます。この場合、フィルタを実行する順番は定義されていません。
* フィルタチェインを変更することで、アプリケーションの要件に合わせて認証と認証をカスタマイズすることができます。

# 20210309 

# 10. Applying CSRF protection and CORS

SpringSecurityのCSRF、CORSの設定について論じる章。

## 10.1 Applying cross-site request forgery (CSRF) protection in applications

この章では、CSRFの防御策とそれをいつ使うかについて論じる。
まずは仕組みを解説し、それからCSRFの対処方法についての話に移る。

### 10.1.1 How CSRF protection works in Spring Security

具体例として、以下のような流れでCSRFは実行される。
* ユーザーがとある認証が必要なサーバーに認証をパスする
* ユーザーが悪意のあるメールを受け取り、その中にあるリンクを踏む
* リンクの先には最初に認証をパスしたサーバーに対して、データを全消去するような命令を飛ばすスクリプトが仕込まれている
* すでに認証済みであるので、ユーザーの意図しない、スクリプトによる命令でデータが全消去されてしまう

CSRFの対策としては、最初にページを取得するGET命令時に、ページ内にユニークなトークンを仕込ませておき、その後の操作においては該当のトークンがなければ受け付けないようにする

SpringSecurityでは、CsrfFilterという部品がCsrfTokenRepositoryFilterという部品を使って、CSRF対策をしていく。

CsrfTokenRepositoryFilterは、デフォルトではセッションにトークンを保存する。

### 10.1.2 Using CSRF protection in practical scenarios

同じサーバーでフロントとバック両方を担当する場合にCSRFトークンは機能する。  
モバイルや、SPA系では別の対策を打つ必要がある。  

### 10.1.3 Customizing CSRF protection

特定のエンドポイントにのみCSRF対応を入れるような実装を例示している。

CSRFを外部に保存するための部品もSpringSecurityで用意してくれている。

## 10.2 Using cross-origin resource sharing

CORSとは何か。`example.com`から`api.example.com`にはアクセスを許さないみたいな話。

最近はVueやReactの台頭もあって、フロントとバックが分かれるパターンが多い。


### 10.2.1 How does CORS work?

iframe でも問題になりうる。[iframe](https://developer.mozilla.org/ja/docs/Web/HTML/Element/iframe)はWebページ内に地図を埋め込んだりするあれ。

* Access-Control-Allow-Origin
* Access-Control-Allow-Methods
* Access-Control-Allow-Headers

ssia-ch10-ex4で例あり。localhostと127.0.0.1でもCORSは起こるので、それを利用して検証する。  
あたりまえだけど、127.0.0.1:8080でアクセスしたら普通に通信は成功する。
localhost:8080でアクセスしたら、想定通りCORSエラーを引き起こせる。

CORSは承認や保護とは違う。なので、バックエンドのAPI自体は正常に実行される。

preflightこみのリクエストの流れ。
![img.png](img.png)

### 10.2.2 Applying CORS policies with th @CrossOrigin annotation

### 10.2.3 Applying CORS using a CorsConfiguration

`@CrossOrigin`を利用するか、`CorsConfiguration`を利用するか問題。
アノテーションでやると、透明性が上がる？が、いくつもアノテーションを記述しなければならないため冗長。

ここの例では`CorsConfigurationSource`をconfigureメソッドの中に直接書いてるけど、現実世界のアプリはさらに設定が長くなるだろうから、本当は分離したほうがいい。

* クロスサイトリクエストフォージェリ（CSRF）とは、ユーザーを騙してフォージェリ用のスクリプトを含むページにアクセスさせる攻撃の一種です。このスクリプトは、アプリケーションにログインしているユーザーになりすまし、ユーザーに代わってアクションを実行することができます。
* CSRF対策は、Spring Securityではデフォルトで有効になっています。
* Spring SecurityのアーキテクチャにおけるCSRF保護ロジックのエントリーポイントはHTTPフィルタです。
* CORS(Cross-over Resource Sharing)とは、特定のドメインでホストされているウェブアプリケーションが、他のドメインのコンテンツにアクセスしようとする状況を指します。デフォルトでは、ブラウザはこの現象を許しません。CORSを設定すると、ブラウザで実行されるWebアプリケーションで、リソースの一部を別のドメインから呼び出すことができるようになります。
* CORS は、@CrossOrigin アノテーションを使用してエンドポイントに対して設定することも、HttpSecurity オブジェクトの cors() メソッドを使用して設定クラスで集中的に設定することもできます。

### 20210508

#### CSRF

10章。CSRFとCORS。

CSRFの怖いところ。設定を誤ると全てに及ぶ？

X-CSRF-TOKENはSpringSecurityオリジナル？

CsrfFilterがある。情報を取得するようなメソッドに対してはデフォルトでは防がない。
GETで値を更新するようなことをするとだめ。
(GETも含めるようにすることは可能)

CsrfFilterはCsrfTokenRepositoryを使う。

_csrfをCsrfFilterが埋め込む。

同じセッション期間中だと同じx-csrf-tokenが使われる。
リロードしても同じセッションで結んでいるのであれば、同じx-csrf-tokenが返ってくる。

SpringBootThymeleafの部分よくわからず。

#### CORS


# 11 Hands-on:A separation of responsibilities

client、認証サーバ、ビジネスロジックサーバで構成されたシステムを作っていく。

## 11.1 The scenario and requirements of the example

この段落では、本章で作っていくアプリの説明をする。

3つの構成要素からなるようなアプリを作る。

* クライアント --これはバックエンドを消費するアプリケーションです。モバイルアプリや、Angular、ReactJS、Vue.jsなどのフレームワークで開発されたWebアプリケーションのフロントエンドなどが考えられます。システムのクライアント部分は実装していませんが、現実のアプリケーションに存在することを念頭に置いています。クライアントを使ってエンドポイントを呼び出す代わりに、cURLを使います。
* 認証サーバー --これは、ユーザー資格情報のデータベースを持つアプリケーションです。このアプリケーションの目的は、ユーザーの認証情報（ユーザー名とパスワード）に基づいてユーザーを認証し、ワンタイムパスワード（OTP）をSMSで送信することです。この例では、実際にSMSを送信しないので、OTPの値をデータベースから直接読み取ることにします。この章では、SMSを送信しないでこのアプリケーション全体を実装します。後で、AWS SNS（https://aws.amazon.com/sns/）やTwillio（https://www .twilio.com/sms）など、お好みのサービスを使ってメッセージを送信するように拡張することもできます。
* ビジネスロジックサーバー --クライアントが消費するエンドポイントを公開するアプリケーションです。これらのエンドポイントへのアクセスを保護する必要があります。ユーザーは、エンドポイントを呼び出す前に、ユーザー名とパスワードで認証を行い、OTPを送信する必要があります。ユーザーは、SMSメッセージでOTPを受け取ります。このアプリケーションはターゲット・アプリケーションなので、Spring Securityで保護します。

流れとしては、

* 1回目の認証
  * クライアントがビジネスロジックサーバーの`/login`エンドポイントに、username:passwordとともにアクセス
  * ビジネスロジックサーバーが認証サーバーの`/user/auth`エンドポイントに、username:passwordとともにアクセス
  * 認証サーバーにて、受け取ったusername:passwordをdbから探して認証
  * 認証できたら、認証サーバーからクライアントにSMS経由でOTPを送信
* 2回目の認証
  * クライアントがビジネスロジックサーバーの`/login`エンドポイントに、username:codeとともにアクセス
  * ビジネスロジックサーバーが認証サーバーに、受け取ったusername:codeの組み合わせは正しいか確認
  * 正しい場合は、ビジネスロジックサーバーからクライアントにトークンを返却する
* それ以降、クライアントからビジネスロジックサーバーにきたアクセスは、トークンを元に認可を行う 

※ここではビジネスロジックサーバーでもパスワードを共有しているが、本来パスワードはクライアントと認証サーバー間でのみ共有されるべき

## 11.2 Implementing and using tokens

トークンにはUUIDとかJWTがあり得る。
トークンはOAuth2でも大事な要素。

### 11.2.1 What is a token?

トークンはアクセスカードのようなもの。

実装レベルだと、username:passwordで認証した時、トークンを発行して、DBなどに保存しておき、クライアントに返却する。
クライアントは以後、その受け取ったトークンとともにビジネスロジックサーバーにアクセスする。

トークンによる制御で複雑化しているように見えるが、どのような利点があるのだろうか。以下のような利点がある。

* トークンを使用すると、すべてのリクエストで認証情報を共有する必要がなくなります。
* 有効期限の短いトークンを定義することができます。
* 認証情報を無効にすることなく、トークンを無効にすることができます。
* トークンは、クライアントがリクエストで送信する必要のあるユーザー権限などの詳細を保存することもできます。
  * トークンを使って、ユーザーの権限や役割などの詳細を保存することができます。この方法では、サーバーサイドのセッションをクライアントサイドのセッションに置き換えることができ、水平方向のスケーリングに柔軟に対応できます。この方法については、第12章から第15章までのOAuth 2のフローで詳しく説明しています。
    * ??詳しくは１２〜１５章らしいので一旦飲み込む
* トークンは、システム内の別のコンポーネントに認証責任を委ねるのに役立ちます。

### 11.2.2 What is a JSON Web Token?

JWTはjson web token

例としてはこんな感じ

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImRhbmllbGxlIn0.wg6LFProg7s_KvFxvnYGiZF-Mj4rr-0nJA1tVGZNn8U
```

ピリオド区切りになっていて、最初の部分がヘッダー、次の部分がボディ。それぞれがbase64エンコードされている。

戻すと以下のような感じ。

```
{
  "alg": "HS256"
}

{
  "username": "danielle"
}
```

ボディ部は長くしない事推奨。なぜなら、長いとリクエストのレイテンシーが大きくなり、暗号化の時間も長くなるから。

最後の部分は署名データ。

この章ではJJWTというライブラリを利用してJWTのパースと生成を行う。

## 11.3 Implementing the authentication server

この章では、認証サーバーの実装をしていく。

用意するのは3つのエンドポイント

* `/user/add`--後で実装をテストするために使用するユーザーを追加します。
* `/user/auth`...認証情報を使ってユーザーを認証し、ワンタイムパスワードをSMSで送信します。ここでは、SMSを送信する部分は削除していますが、練習として行うことができます。
* `/otp/check`--OTPの値が、認証サーバが特定のユーザのために以前に生成したものであることを確認します。

## 11.4 Implementing the business logic server

下記の順序で実装していく。

1. セキュリティを確保したいリソースを表すエンドポイントを作成します。
1. 最初の認証ステップを実装します。このステップでは、クライアントがユーザ認証情報（ユーザ名とパスワード）をビジネスロジック・サーバに送信してログインします。
1. クライアントが認証サーバから受け取ったOTPをビジネス・ロジック・サーバに送信する第2認証ステップを実装します。OTPによって認証されると、クライアントは、ユーザーのリソースにアクセスするために使用できるJWTを取得します。
1. JWTに基づいた認証を行う。ビジネス・ロジック・サーバは、クライアントから受け取ったJWTを検証し、有効であれば、クライアントにリソースへのアクセスを許可します。

### 11.4.1 Implementing the Authentication objects

### 11.4.2 Implementing the proxy to the authentication server

### 11.4.3 Implementing the AuthenticationProvider interface

### 11.4.4 Implementing the filters

### 11.4.5 Writing the security configurations

### 11.4.6 Testing the whole system

2つ引数を持つAuthenticationコンストラクタはまだ認証されていない。
3つ引数を持つAuthenticationコンストラクタは認証ずみ。

username:passwordの認証でダメだったときに403を返しているのはどこだ？？
⇨
RestTemplateのpostForEntityは４００系で返ってきたら、HttpClientErrorExceptionを投げるので、それに反応してる

## Summary

* カスタムの認証・認可を実装する際には、必ずSpring Securityが提供するコントラクトを利用してください。AuthenticationProvider、AuthenticationManager、UserDetailsServiceなどがそれにあたります。このアプローチにより、わかりやすいアーキテクチャを実装することができ、アプリケーションのエラーが少なくなります。
* トークンは、ユーザーの識別子です。トークンが生成された後にサーバーがそれを認識する限り、トークンはどのような実装でも構いません。トークンの例としては、アクセスカードやチケット、美術館の入り口でもらうステッカーなどがあります。
* トークンの実装には、シンプルなUUID（Universally Unique Identifier）を使用することもできますが、JSON Web Tokens（JWT）として実装されたトークンを見かけることが多くあります。JWTには、リクエストで交換されたデータを保存できること、転送中に変更されていないことを保証するために署名できることなど、複数の利点があります。
* JWT トークンは、署名されている場合もあれば、完全に暗号化されている場合もあります。署名されたJWTトークンはJSON Web Token Signed (JWS)と呼ばれ、詳細が暗号化されたものはJSON Web Token Encrypted (JWE)と呼ばれます。
* JWTにはあまり多くの詳細情報を保存しないようにしましょう。署名または暗号化する場合、トークンが長ければ長いほど、署名または暗号化に必要な時間が長くなります。また、HTTPリクエストのヘッダーにトークンを送信することを覚えておいてください。トークンが長ければ長いほど、各リクエストに追加するデータが多くなり、アプリケーションのパフォーマンスに影響を与える可能性があります。
* 私たちは、システムの保守や拡張を容易にするために、システム内の責任を分離することを好みます。このような理由から、ハンズオンの例では、認証を別のアプリに分離し、それを認証サーバーと呼びました。クライアントにサービスを提供するバックエンド・アプリケーション（ビジネス・ロジック・サーバと呼ぶ）は、クライアントを認証する必要があるときに、別の認証サーバを使用します。
* 多要素認証（MFA）とは、あるリソースにアクセスする際に、ユーザーが複数回、異なる方法で認証を求められる認証戦略です。この例では、ユーザーは、ユーザー名とパスワードを使用した後、SMSメッセージで受信したOTPを検証することで、特定の電話番号にアクセスできることを証明しなければなりません。このようにして、ユーザーのリソースは認証情報の盗難からよりよく保護されます。
* 多くの場合、問題を解決するための良い解決策は1つだけではありません。常にすべての可能な解決策を検討し、時間が許せば、すべてのオプションの概念実証を実施して、どれが自分のシナリオにより適しているかを理解してください。

# 12 How does OAuth2 work?

## 12.1 The OAuth2 framework

Basic認証でダメなのか？という問いからスタートしている。
Basic認証ではリクエストのたびにパスワードがネットワーク上に飛んでしまう。
また、複数のアプリケーションが存在するときに、何も工夫をしない場合は各アプリケーションのクレデンシャルをクライアントは記憶しておかねばならない。

## 12.2 The Components of the OAuth2 authentication architecture

登場人物の紹介

* リソースサーバー -- ユーザーが所有するリソースをホストするアプリケーション。リソースには、ユーザーのデータや、ユーザーが許可した行動が含まれます。
* ユーザー（リソースオーナーとも呼ばれる） --リソースサーバーが公開するリソースを所有する個人。ユーザーは通常、自分を識別するためのユーザー名とパスワードを持つ。
* クライアント --ユーザーに代わって、ユーザーが所有するリソースにアクセスするアプリケーション。クライアントは、自分自身を識別するためにクライアントIDとクライアントシークレットを使用します。これらの認証情報はユーザーの認証情報と同じではないので注意が必要です。クライアントは、リクエストを行う際に自分自身を識別するための独自の認証情報を必要とします。
* 認可サーバー --リソースサーバーが公開しているユーザーのリソースにアクセスすることをクライアントに認可するアプリケーションです。認可サーバーは、クライアントがユーザーに代わってリソースにアクセスする権限があると判断すると、トークンを発行する。クライアントはこのトークンを使って、自分が認可サーバーから認可されたことをリソースサーバーに証明します。リソースサーバーは、クライアントが有効なトークンを持っていれば、クライアントが要求したリソースへのアクセスを許可します。

## 12.3 Implementation choices with OAuth2 

各grant typeについての紹介

### 12.3.1 Implementing the authorization code grant type

認可コードフローについての説明。
大事なのは、リソースオーナーのクレデンシャルがクライアントには知られないこと。？？

認可エンドポイントには下記のクエリストリングを引き連れてアクセスする

* response_type (code) は、クライアントが認可コードを期待していることを認可サーバーに伝えるものです。クライアントはアクセストークンを取得するためにこの認可コードを必要とします。
* client_id には、アプリケーションを識別するためのクライアントIDの値を指定します。
* redirect_uri：認証成功後にユーザーをどこにリダイレクトするかを認可サーバーに伝えるものです。認証サーバーは、各クライアントのデフォルトのリダイレクトURIをすでに知っていることがあります。このため、クライアントはリダイレクトURIを送信する必要はありません。
* scopeは、第5章で説明したgiven authorityと似ています。
* state は、第 10 章で説明した CSRF 保護に使用するクロスサイトリクエストフォージェリ (CSRF) トークンを定義します。

直接トークンを返却せず、まず認可コードを払い出す理由は、クライアントの正当性を図るため。??

トークンエンドポイントには以下を引き連れてアクセスする。

* コード（ステップ1で受け取った認証コード）を入力します。これにより、ユーザーが認証したことが証明されます。
* client_idとclient_secret、これはクライアントの認証情報です。
* redirect_uri。これはステップ1で検証のために使われたものと同じです。
* grant_typeはauthorization_codeという値を持ち、使用されるフローの種類を特定します。サーバーが複数のフローをサポートしている場合もあるので、現在実行されている認証フローを常に指定することが重要です。

### 12.3.2 Implementing the password grant type

resource owner credentials grant type

クライアントと認可サーバーが同じ組織内の物であれば有効な手段。

クライアントにクレデンシャルが発露してしまう。

### 12.3.3 Implementing the client credentials grant type

クライアントアプリ自体がAPIキーを持っていて、それを元にトークンを取得するようなタイプ

### 12.3.4 Using refresh tokens to obtain new access token 

ユーザビリティ、セキュリティの観点からリフレッシュトークンは必要。

リフレッシュトークンがない場合、アクセストークンの有効期限が切れるたびにログイン作業をしなければならない。
また、そのログイン作業をどこかに記憶させておいたusername:passwordによる認証にすると、ユーザーの秘匿情報の発露につながりセキュリティ上問題がある。　　
リフレッシュトークンであれば、無効化が容易。

## 12.4 The sins of OAuth2

OAuth2 の弱点、気をつけるところ。

* クライアントでのクロスサイトリクエストフォージェリ(CSRF)の使用--ユーザーがログインしている状態で、アプリケーションがCSRF保護メカニズムを適用していなければ、CSRFは可能です。第10章では、Spring Securityで実装されているCSRF対策について詳しく説明しました。
* クライアントの認証情報を盗む--保護されていない認証情報を保存したり転送したりすると、攻撃者が認証情報を盗み出して使用することが可能になります。
* トークンの再生--第13章と第14章で学ぶように、トークンはOAuth 2の認証・認可アーキテクチャの中で、リソースにアクセスするために使用する鍵です。これをネットワークで送信しますが、時には傍受されることもあります。傍受された場合、トークンは盗まれますが、再利用することができます。例えば、自宅の玄関の鍵を紛失したとします。どうなるでしょうか？他の誰かがその鍵を使って何度でもドアを開けることができるのです（リプレイ）。第14章では、トークンの詳細と、トークンのリプレイを防ぐ方法について学びます。
* トークンの乗っ取り--認証プロセスを妨害され、リソースへのアクセスに使用できるトークンを盗まれることです。これは、リフレッシュトークンを使用する際の潜在的な脆弱性でもあります。リフレッシュトークンも傍受され、新しいアクセストークンを取得するために使用される可能性があります。I recommend this helpful article: http://blog.intothesymmetry.com/2015/06/on-oauth-token-hijacks-for-fun-and.html

## 12.5 Implementing a simple single sign-on application

### 12.5.1 Managing the authorization server

githubを認可サーバーとして使う

下記から認可サーバーとしての設定を行う。  
https://github.com/settings/applications/new

### 12.5.2 Starting the implementation

`oauth2Login()`は認証フィルター`OAuth2LoginAuthenticationFilter`を追加している。

### 12.5.3 Implementing ClientRegistration

`ClientRegistration`はOAuth2におけるクライアントを表している。

`CommonOAuth2Provider`を使うことで、設定を省力できる。

### 12.5.4 Implementing ClientRegistrationRepository

`OAuth2LoginAuthenticationFilter`から利用する`ClientRegistration`を登録するために`ClientRegistrationRepository`を利用する。

※@Beanで定義するか、configurationで定義するか、どちらか一方に統一する。可読性の観点から、混ぜるのはだめ。

### 12.5.5 The pure magic of Spring Boot configuration

`@Bean`で定義、`configuration`で定義、の他にpropertyファイルで定義という選択肢がある

### 12.5.6 Obtaining details about an authenticated user

### 12.5.7 Testing the application

* http://localhost:8080
  * まずここにアクセス
* http://localhost:8080/oauth2/authorization/github
  * いきなりgithubの認可エンドポイントにはとばさず、ここにリダイレクトさせる。これはSpringSecurityならでは？
* https://github.com/login/oauth/authorize?response_type=code&client_id=~&scope=read:user&state=~=&redirect_uri=http://localhost:8080/login/oauth2/code/github
  * githubの認可エンドポイント。
* http://localhost:8080/login/oauth2/code/github?code=~&state=~
  * ここにアクセスした時に、サーバー側でトークンを取得しているはず。
* http://localhost:8080
  * ゴール

# 13 OAuth 2: Implementing the authorization server

OAuth２系のサポート状況は下記参照

https://github.com/spring-projects/spring-security/wiki/OAuth-2.0-Features-Matrix

## 13.1 Writing your own authorization server implementation

`@EnableAuthorizationServer`つけたら、認可サーバーに必要なエンドポイントが勝手に設定される。多分。

## 13.2 Defining user management

基本的には３章、４章で行ったことと同じことをしてuserの管理をする。
ただし、SecurityContextへの認証情報の保存はしない。代わりにTokenStoreで管理する。

## 13.3 Registering clients with the authorization server

`ClientDetails`系と`UserDetails`系は似ている。

## 13.4 Using the password grant type

ch13-ex1で確認。

