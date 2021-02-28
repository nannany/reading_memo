# FilterChainProxyについて

https://www.fatalerrors.org/a/1dxx2A.html

FilterChainProxyを、WebServer(tomcatとか？)がもっている仕組みであるFilterに入れ込む。
FilterChainProxyの中に、複数のChain群があり、リクエストのパスに応じてどのFilterを通過させるかがきまる。

---

# HttpSecurityについて

https://mp.weixin.qq.com/s/Kk5c5pK5_LFcCpcnIr2VrA

* `SecurityFilterChain`の唯一の実装クラスが`DefaultSecurityFilterChain`
* `SecurityBuilder`は何のために使われるかというと、フィルタチェインのビルドに使われる。
* `AbstractSecurityBuilder`クラスはSecurityBuilderインターフェースを実装しており、このクラスで行われている主なことの一つは、ビルド全体が一度だけビルドされることを保証することです。
* `AbstractConfiguredSecurityBuilder`はいろいろやってるけど大事なのは2つ。
  * `add`で`configurers`フィールドに`xxxConfigurer`を集める
  * `doBuild`で状態の更新、初期化を行う
* `HttpSecurity`で`cors()`とか`httpBasic()`とかのメソッドが用意されている。
  * これらで`AbstractConfiguredSecurityBuilder`の`configurers`に`SecurityConfigurer`をぶち込む。

---

# SecurityConfigurerについて
https://www.fatalerrors.org/a/in-depth-understanding-of-securityconfigurer.html

SecurityConfigurerの実装クラスは3つ
* SecurityConfigurerAdapter
* GlobalAuthenticationConfigurerAdapter
* WebSecurityConfigurer

## SecurityConfigurerAdapter

`CompositeObjectPostProcessor`の説明がよくわからない。

## GlobalAuthenticationConfigurerAdapter

## WebSecurityConfigurer

---
## SecurityConfigurerAdapterについて

SecurityConfigurerAdapterの実装クラスで、SpringSecurityに用意されているのは以下3つ。

* UserDetailsAwareConfigurer
* AbstractHttpConfigurer
* LdapAuthenticationProviderConfigurer

Ldapのやつは最近は使わない。

### UserDetailsAwareConfigurer

### AbstractHttpConfigurer

たくさんの実装クラスがある。
紹介されているのは、`AbstractAuthenticationFilterConfigurer`、`FormLoginConfigurer`。

---

# WebSecurityConfigurerAdapter


