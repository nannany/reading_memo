# HIDDEN

```
HIDDEN
200
My friend asked me to find his hidden flag in this link .. Can you help me?

Link
Author:Tr'GFx
```

* Flag is somewhere here と書かれたページに飛ばされるがそこから何をすればよいのかわからない。。

* Censysでホスト名調べたらフラグがあった。
Securinets{HiDDeN_D@tA_In_S3lF_S3iGnEd_CeRtifICates}

* Certificate Chainの中にあった。
* 証明書の詳細のオブジェクトの中。

# EZ

```
EZ
712
Welcome to Securinets, this one is an easy one.

Please make sure you hash the WORD with sha1 (lowercase hash letter)

The final flag is : Securinets{the_hash_of_the_word}

Pic Link
Author:BlueWhale
```

# Feedback

```
Feedback
921
I created this website to get your feedback on our CTF.

Can you check if it's secure ?

Link
Author:Tr'GFx
```

* XSSぽいと思いつつ。なにをすればよいのか。。


# SQL Injected

```
SQL Injected
994
Task url: https://web5.ctfsecurinets.com 

You can download the source code here

Author: Oussama

ps: i don't like the task's name
```

* まずはソースを読んでいく。
* PHPのdie()メソッドはexitと同等らしい。
* PHPのrequire_once()メソッドはなんか読み込むらしい。Pythonのimport的なやつかな
* セッション内のroleの値が1であればフラグを読み取るページにイケルっぽい。roleが1であることがadminの条件であるようなので、adminのセッションを盗めればよい
* 


# Trading values

```
Trading values
999
N00B developers are an easy target. Try to exploit the application feature to get the hidden flag.

Link
Author:TheEmperors
```

* 1秒ごとに表が再描画されるようなページが現れる。
* 
