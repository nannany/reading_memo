# 概要

明確な理由はあまりないのですが、ホストOSである Windows で仮想化ソフトに VirtualBox を使用し、ゲストOSの Ubuntu を立ち上げ、そこを主な開発環境にしようと試みました。

その際、Ubuntu でのキーマッピングがあまりに Windows のそれと違っていたのでだいぶやりにくく感じ、Windowsのキーマッピングになんとか寄せようと試みたのでその記録を書き連ねていきます。

# 動作環境

動作環境は以下のようです。

* ホストOS： Windows10 Home 
* 仮想化ソフト： VirtualBox 6.0.10
* ゲストOS： Ubuntu 19.04

また、使用しているキーボードは108キーボードです。

# Windowsでのキーカスタマイズはどんな感じだったのか？

Windows上では、[enthumble](https://qiita.com/mhara/items/d2d072592a4db9243c99)というキーボードカスタマイズツールを使っています。

enthumbleについては、私の意識している範囲だと以下の機能を提供してくれていました。

* 無変換を押すとIMEをOFFにする
* 変換を押すとIMEをONにする
* 無変換か変換を押しながら他のキーを押した場合の動作をカスタマイズできる
  * 例）変換 + h = ← 

無変換、変換を押して他のキーを押した場合の挙動のカスタマイズは以下のようにしていました。(※自由にカスタマイズするためには980円の有料版をダウンロードする必要があります。)
詳しい見方は[このページ](https://qiita.com/mhara/items/44064da2d77ddbd258b7)が参考になります。

```
[HowToUse]
Check=http://jp.enthumble.com/
Name=enthumble version 4.0
[KEY]
Space={Enter}
Muhenkan={Esc}
Henkan={Esc}
Hiragana={}
F1=#{1}
F2=#{2}
F3=#{3}
F4=#{4}
F5=#{5}
F6=#{6}
F7=#{7}
F8=#{8}
F9=#{9}
F10={Volume_Mute}
F11={Volume_Down}{Volume_Down}
F12={Volume_Up}{Volume_Up}
F18={}
F19={}
1={F1}
2={F2}
3={F3}
4={F4}
5={F5}
6={F6}
7={F7}
8={F8}
9={F9}
0={F10}
-={F11}
Hat={F12}
\={}
Q=^{PgUp}
W=^{PgDn}
E=^{Home}
R=^{End}
T=^{t}
Y={Backspace}
U={PgUp}
I={Insert}
O={delete}
P={up}
@={}
LB={}
A=^{a}
S=^{s}
D={PgDn}
F=^{f}
G=^{g}
H={left}
J={down}
K={up}
L={right}
Semicolon={}
:={}
RB={}
Z=^{z}
X=^{x}
C=^{c}
V=^{v}
B=^{b}
N={alt down}{left}{alt up}
M={alt down}{up}{alt up}
,={delete}
.={alt down}{right}{alt up}
/={}
Backslash={}
Up={vkF2sc070B}{vkF3sc029}{ASC 33194}
Down={vkF2sc070B}{vkF3sc029}{ASC 33195}
Left={vkF2sc070B}{vkF3sc029}{ASC 33193}
Right={vkF2sc070B}{vkF3sc029}{ASC 33192}
LButton=^{PgUp}
MButton={MButton}
RButton=^{PgDn}
WheelUp={}
WheeDown={}
PageUp=^{PgUp}
PageDown=^{PgDn}
Home={}
End={}
Delete={}
backspace={}
Enter={}
Escape={}
Hankaku={}
Tab={}
Capslock={}
Lwin={}
Rwin={}
Insert={}
```


# Ubuntu上で設定したこと

Ubuntu上での日本語入力環境としては、fcitx-mozcを使用しています。
無変換を押したらIMEがOFFになり、変換を押したらIMEがONになる、という挙動はfcitxの設定で再現するよう試みました。
また、無変換、変換を押しながら他のキーを押した場合の挙動のカスタマイズは、xkeysnailというツールを使用しました。

## fcitxの入力メソッド切り替え設定

`fcitx-configtool`で表示される画面で、以下のように「キーボード-日本語-日本語(OADG 109A)」と「Mozc」入力メソッドを設定します。
(108キーボードはなかったので109で代用しましたが、現状特に問題は起きていません)

次に、「全体の設定」タブをクリックし、「Show Advanced Options」にチェックを入れます。
「入力メソッドをオンに」に「Henkanmode」を指定し、「入力メソッドをオフに」に「Muhenkan」を指定します。

これで無変換を押せば半角英数入力になり、変換を押せば日本語入力になるはずです。

## xkeysnail

キーのマッピングのカスタマイズには[xmodmap](https://wiki.archlinux.jp/index.php/Xmodmap)や[remap](https://github.com/k0kubun/xremap)などがありましたが、一番後発であるという理由で[xkeysnail](https://github.com/mooz/xkeysnail)を使用しました。

[このページ](https://qiita.com/mooz@github/items/c5f25f27847333dd0b37)をみて、以下2点あたりが特に利点に感じました。

* アプリケーションごとにキーバインド設定ができる
  * 例)chromeとVSCodeで別のキーバインド設定ができる
* 他のツールに比べ、ほとんどの場所でキーバインド設定が効く

### xkeysnailのインストール方法

以下コマンドの実行でインストールできます。
```
sudo apt install python3-pip
sudo pip3 install xkeysnail
```

### xkeysnailのconfig.py 

config.py というファイルにカスタマイズ内容を記述していきます。
記述方法は[ここ](https://qiita.com/mooz@github/items/c5f25f27847333dd0b37#define_keymapcondition-mappings-name)に記載されています。

カスタマイズする際に頭を悩ませた点なのですが、xkeysnailの仕様として、修飾キーには`Control`、`Alt`、`Shift`、`Windows`キーのいずれかしか選択できません。
理想としては無変換、変換キーを修飾キーに使用したかったのですが、



### xkeysnailのサービス化

~/.config/systemd/user/xkeysnail.service
を作成。
systemctl --user enable xkeysnail 
を実行してシンボリックリンクを作成。

sudo groupadd uinput

sudo usermod -aG input,uinput vagrant   

https://qiita.com/samurai20000@github/items/2e1d779e806a7e8543d6

# まとめ


###

~/.config/fcitx/config に fcitx の入力切替に関する設定が載っています。

gsettings list-recursively でショートカットがどのように設定されているか見れる。

ctrl+alt+@ でグレイブだせるはず。。なぜvimででない → 入力メソッドのオンオフの片方が`になっていた。。

xkeysnail をサービス化して、失敗する。

journalctl -o verbose _PID=~~

```
Sat 2019-08-17 23:16:27.839596 PDT [s=018b5ea1065b4eca938caedebbf94c60;i=7952;b=
    PRIORITY=6
    SYSLOG_FACILITY=3
    _UID=1000
    _GID=1000
    _CAP_EFFECTIVE=0
    _SELINUX_CONTEXT=unconfined
    _AUDIT_LOGINUID=1000
    _SYSTEMD_OWNER_UID=1000
    _SYSTEMD_UNIT=user@1000.service
    _SYSTEMD_SLICE=user-1000.slice
    _SYSTEMD_USER_SLICE=-.slice
    _MACHINE_ID=9f431bdbd7044796a650f3421beb0f08
    _HOSTNAME=ubuntu1904.localdomain
    _TRANSPORT=stdout
    _SYSTEMD_CGROUP=/user.slice/user-1000.slice/user@1000.service/xkeysnail.serv
    _SYSTEMD_USER_UNIT=xkeysnail.service
    SYSLOG_IDENTIFIER=xkeysnail
    _COMM=xkeysnail
    _EXE=/usr/bin/python3.7
    _CMDLINE=/usr/bin/python3 /usr/local/bin/xkeysnail /home/vagrant/.ghq/github
    MESSAGE=  File "/usr/local/lib/python3.7/dist-packages/xkeysnail/__init__.py
    _AUDIT_SESSION=4
    _SYSTEMD_INVOCATION_ID=dd0c986db07548f391e8a2ef1b1699b8
    _BOOT_ID=9f5087462fd443608af496685c0aebb6
    _STREAM_ID=4fc206f8a940436e9c6a9edcca2323ea
    _PID=1551
Sat 2019-08-17 23:16:27.839596 PDT [s=018b5ea1065b4eca938caedebbf94c60;i=7953;b=
    PRIORITY=6
    SYSLOG_FACILITY=3
    _UID=1000
    _GID=1000
    _CAP_EFFECTIVE=0
    _SELINUX_CONTEXT=unconfined
    _AUDIT_LOGINUID=1000
    _SYSTEMD_OWNER_UID=1000
    _SYSTEMD_UNIT=user@1000.service
    _SYSTEMD_SLICE=user-1000.slice
    _SYSTEMD_USER_SLICE=-.slice
    _MACHINE_ID=9f431bdbd7044796a650f3421beb0f08
    _HOSTNAME=ubuntu1904.localdomain
    _TRANSPORT=stdout
    _SYSTEMD_CGROUP=/user.slice/user-1000.slice/user@1000.service/xkeysnail.serv
    _SYSTEMD_USER_UNIT=xkeysnail.service
    SYSLOG_IDENTIFIER=xkeysnail
    _COMM=xkeysnail
    _EXE=/usr/bin/python3.7
    _CMDLINE=/usr/bin/python3 /usr/local/bin/xkeysnail /home/vagrant/.ghq/github
    MESSAGE=    print(__logo__.strip())
    _AUDIT_SESSION=4
    _SYSTEMD_INVOCATION_ID=dd0c986db07548f391e8a2ef1b1699b8
    _BOOT_ID=9f5087462fd443608af496685c0aebb6
    _STREAM_ID=4fc206f8a940436e9c6a9edcca2323ea
    _PID=1551
Sat 2019-08-17 23:16:27.839596 PDT [s=018b5ea1065b4eca938caedebbf94c60;i=7954;b=
    PRIORITY=6
    SYSLOG_FACILITY=3
    _UID=1000
    _GID=1000
    _CAP_EFFECTIVE=0
    _SELINUX_CONTEXT=unconfined
    _AUDIT_LOGINUID=1000
    _SYSTEMD_OWNER_UID=1000
    _SYSTEMD_UNIT=user@1000.service
    _SYSTEMD_SLICE=user-1000.slice
    _SYSTEMD_USER_SLICE=-.slice
    _MACHINE_ID=9f431bdbd7044796a650f3421beb0f08
    _HOSTNAME=ubuntu1904.localdomain
    _TRANSPORT=stdout
    _SYSTEMD_CGROUP=/user.slice/user-1000.slice/user@1000.service/xkeysnail.serv
    _SYSTEMD_USER_UNIT=xkeysnail.service
    SYSLOG_IDENTIFIER=xkeysnail
    _COMM=xkeysnail
    _EXE=/usr/bin/python3.7
    _CMDLINE=/usr/bin/python3 /usr/local/bin/xkeysnail /home/vagrant/.ghq/github
    MESSAGE=UnicodeEncodeError: 'latin-1' codec can't encode characters in posit
    _AUDIT_SESSION=4
    _SYSTEMD_INVOCATION_ID=dd0c986db07548f391e8a2ef1b1699b8
    _BOOT_ID=9f5087462fd443608af496685c0aebb6
    _STREAM_ID=4fc206f8a940436e9c6a9edcca2323ea
    _PID=1551
```