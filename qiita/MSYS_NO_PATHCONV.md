# トラブル内容

Windows上の Git Bash で開発をしていると、コマンドに渡した引数が意図しない形でパス変換されてしまうことがあります。
以下、遭遇して困った具体的な2例をあげます。

## 例1) 起動中のコンテナの中身をみようとして失敗！

`docker exec -it ${起動中コンテナID} /bin/sh` のようにしてコンテナの中身に入りたい場合があります。
この時に、`/bin/sh` 部分が `${Git Bashのルートディレクトリ}/bin/sh` と変換されて docker コマンドに渡されてしまい失敗することがあります。

```
$ docker exec -it 9295d32adf71 /bin/sh
OCI runtime exec failed: exec failed: container_linux.go:348: starting container process caused "exec: \"C:/Program Files/Git/usr/bin/sh\": stat C:/Program Files/Git/usr/bin/sh: no such file or directory": unknown
```

この場合の対応としては `/bin/sh` 部分を `//bin/sh` と記述し、変換させないようにします。

```
$ docker exec -it 9295d32adf71 //bin/sh
/ # ls
bin    dev    etc    home   lib    media  mnt    opt    proc   root   run    sbin   srv    sys    tmp    usr    var
```

または、環境変数 `MSYS_NO_PATHCONV` を 1 に設定してやることで変換を抑制することができます。

```
$ MSYS_NO_PATHCONV=1 docker exec -it 9295d32adf71 /bin/sh
/ # uname
Linux
```

## 例2) envsubst で作成したファイルを kubectl の --from-file で読み込めなくて失敗！

設定値のテンプレートファイルを用意しておき、`envsubst` コマンドでテンプレートファイルに環境変数を埋め込んだファイルをリダイレクトし、
リダイレクトで作成されたファイルを `kubectl create secret --from-file=${作成されたファイルのパス}` のようにして Secret に格納するデータとして使う場合があります。

例1での失敗を活かして、`MSYS_NO_PATHCONV=1` を設定していたとします。
このような時に、envsubst のリダイレクト先のパスと --from-file で指定したパスを `/tmp/env` とすると、
envsubst では `C:\Users\${ユーザー名}\AppData\Local\Temp\env` にファイルが出力される一方で、
kubectl ではそもそも `/tmp/env` などというファイルがないと怒られます。

つまり、以下のようなシェルを実行した場合に、

```sh:envsubst-k8s-sample.sh
cd $(dirname $0)

# MSYS_NO_PATHCONVを設定しておき、勝手にパス変換させないようにする
export MSYS_NO_PATHCONV=1
export HOGE=FOOBAR

envsubst < env.template > /tmp/env

echo $(cat /tmp/env-sample)

kubectl create secret generic my.secret --from-file=/tmp/env
```

(※env.templateは以下のようです)

```sh:env.template
HOGE=$HOGE
```

以下のようなエラーが出てしまうということです。

```
$ ./envsubst-k8s-sample.sh
HOGE=FOOBAR
error: error reading /tmp/env: The system cannot find the path specified.
```

この場合は、kubectl の --from-file で指定したパスを Git Bash 側で変換してもらう必要があります。
変換を再度有効にするには、`MSYS_NO_PATHCONV` 環境変数を削除してやればよいです。
下記のようにシェルを修正すれば想定通りに動作するようになります。

```sh:envsubst-k8s-sample.sh
cd $(dirname $0)

# MSYS_NO_PATHCONVを設定しておき、勝手にパス変換させないようにする
export MSYS_NO_PATHCONV=1
export HOGE=FOOBAR

envsubst < env.template > /tmp/env

echo $(cat /tmp/env-sample)

# パス変換を有効にするために、MSYS_NO_PATHCONV環境変数を削除!
unset MSYS_NO_PATHCONV
kubectl create secret generic my.secret --from-file=/tmp/env
```

```
$ ./envsubst-k8s-sample.sh
HOGE=FOOBAR
secret/my.secret created
```

# 解決策

Git Bash にて行われるパス変換について、解決策をまとめます。

* パス変換が起きてほしくない場合は、`export MSYS_NO_PATHCONV=1` のようにして `MSYS_NO_PATHCONV` 環境変数を設定する
* パス変換をしてほしい場合は、`unset MSYS_NO_PATHCONV` のようにして `MSYS_NO_PATHCONV` 環境変数を削除する

# 補足

パスの変換が起きるのは、msys-1.0.dll や msys-2.0.dll に依存していないEXEファイルの引数においてです。

kubectl.exe や docker.exe は msys-1.0.dll や msys-2.0.dll に依存していないです。

```
$ dumpbin //DEPENDENTS "C:\ProgramData\chocolatey\bin\kubectl.exe"
Microsoft (R) COFF/PE Dumper Version 14.00.24210.0
Copyright (C) Microsoft Corporation.  All rights reserved.


Dump of file C:\ProgramData\chocolatey\bin\kubectl.exe

File Type: EXECUTABLE IMAGE

  Image has the following dependencies:

    mscoree.dll

  Summary

        2000 .reloc
        2000 .rsrc
        6000 .text
```

一方で、envsubst.exe や ls.exe や echo.exe は msys-2.0.dll に依存しています。

```
$ dumpbin //DEPENDENTS "C:\Program Files\Git\usr\bin\cat.exe"
Microsoft (R) COFF/PE Dumper Version 14.00.24210.0
Copyright (C) Microsoft Corporation.  All rights reserved.


Dump of file C:\Program Files\Git\usr\bin\cat.exe

File Type: EXECUTABLE IMAGE

  Image has the following dependencies:

    msys-intl-8.dll
    msys-2.0.dll
    KERNEL32.dll

  Summary

        1000 .bss
        1000 .buildid
        1000 .data
        1000 .idata
        1000 .pdata
        2000 .rdata
        1000 .rsrc
        5000 .text
        1000 .xdata
```

このため、kubectl や docker の引数に渡した値が変換されていることに気づいたときに、
`ls /foo`や`echo /bar`のようなコマンドで変換されていることを確かめようとしてもうまくはいきません。

# 参考

http://www.mingw.org/wiki/Posix_path_conversion