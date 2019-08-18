# 概要

明確な理由はあまりないのですが、ホストOSである Windows で仮想化ソフトに VirtualBox を使用し、ゲストOSの Ubuntu を立ち上げ、そこを主な開発環境にしようと試みました。

その際、Ubuntu でのキーマッピングがあまりに Windows のそれと違っていたのでだいぶやりにくく感じ、Windowsのキーマッピングになんとか寄せようと試みたのでその記録を書き連ねていきます。

# 動作環境

動作環境は以下のようです。

* ホストOS： Windows10 Home 
* 仮想化ソフト： VirtualBox 6.0.10
* ゲストOS： Ubuntu 19.04

# Windowsでのキーカスタマイズはどんな感じだったのか？

私の

# Ubuntu上で設定したこと

## fcitxの入力メソッド切り替え設定

## xkeysnail

キーのマッピングのカスタマイズには[xmodmap](https://wiki.archlinux.jp/index.php/Xmodmap)や[remap](https://github.com/k0kubun/xremap)などがありましたが、一番後発であるという理由で[xkeysnail](https://github.com/mooz/xkeysnail)を使用しました。

### xkeysnailのインストール方法

### xkeysnailのconfig.py 

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