# トラブル内容

Windows上の Git Bash で開発をしていると、コマンドに渡した引数が

# 解決策

* パス変換が起きてほしくない場合は、`export MSYS_NO_PATHCONV=1`のようにして`MSYS_NO_PATHCONV`環境変数を設定しておく
* パス変換をしてほしい場面では、`MSYS_NO_PATHCONV`環境変数を削除しておく(すでに設定しているなら、`unset -v MSYS_NO_PATHCONV`を実行する)

# 捕捉

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

一方で、ls.exe や echo.exe は msys-2.0.dll に依存しています。

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

## 参考

http://www.mingw.org/wiki/Posix_path_conversion