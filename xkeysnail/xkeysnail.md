# 概要

# 動作環境

# xkeysnail


## xkeysnailのインストール方法


## xkeysnailのconfig.py 

## xkeysnailのサービス化

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

