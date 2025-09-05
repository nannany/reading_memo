https://chatgpt.com/c/68ba420e-128c-8333-95e8-a4ba2ca8b4af

下記のような実装で、nthpwで指定した数だけflagをシャッフルした文字列を返すサイト。


```php
<?php
ini_set("error_reporting", 0);
ini_set("short_open_tag", "Off");

if(isset($_GET['source'])) {
    highlight_file(__FILE__);
}

include "flag.php";

$shuffle_count = abs(intval($_GET['nthpw']));

if($shuffle_count > 1000 or $shuffle_count < 1) {
    echo "Bad shuffle count! We won't have more than 1000 users anyway, but we can't tell you the master password!";
    echo "Take a look at /?source";
    die();
}

srand(0x1337); // the same user should always get the same password!

for($i = 0; $i < $shuffle_count; $i++) {
    $password = str_shuffle($FLAG);
}

if(isset($password)) {
    echo "Your password is: '$password'";
}

?>

<html>
    <head>
        <title>PWgen</title>
    </head>
    <body>
        <h1>PWgen</h1>
        <p>To view the source code, <a href="/?source">click here.</a>
    </body>
</html>
Bad shuffle count! We won't have more than 1000 users anyway, but we can't tell you the master password!Take a look at /?source
```


130文字のflagであることがわかっている。
str_shuffleについては、seedが同じであるならば同じ文字数の文字列のシャッフル結果は必ず同じになる。
123 -> 132 ならば abc -> acb になる。

N=1
7F6_23Ha8:5E4N3_/e27833D4S5cNaT_1i_O46STLf3r-4AH6133bdTO5p419U0n53Rdc80F4_Lb6_65BSeWb38f86{dGTf4}eE8__SW4Dp86_4f1VNH8H_C10e7L62154