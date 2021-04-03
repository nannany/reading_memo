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

```aidl
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

## 9.4 Adding a filter at the location of another in the chain

この章ではフィルターチェーンの中にフィルターを組み込んでいく。

authentication部分をオリジナルのフィルターにしてみる。
認証の典型的なパターンとしては以下のようなものがある。

* 特定のheaderの値をもとに認証をする
* 共通鍵を利用して作成した署名をもとに認証する
* ワンタイムパスワードを利用して認証する

例としては一番目の特定の値による認証を行う。

フィルターを同じポジションに置いた場合は適用の順番が不定になるので、フィルターの順番はちゃんと決めること。

## 9.5 Filter implementations provided by Spring Security

SpringSecurity提供のFilterを使うと便利。

OncePerRequestFilterでは、
* HttpServletRequestにキャスト不要
* filterが適応されない場合をロジックで定義することができる(shouldNotFilter) 
* デフォルトでは非同期リクエストやエラーディスパッチリクエストには適用されないが、用意されているメソッドをoverrideすることで変更可能

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
