# 概要

社会人になり６年強、ずっとWindowsを利用していたのですが、一念発起してMacを利用することにしました。
Mac有識者に伺いつつ、Mac初心者が初期設定でやったことを記します。

## 購入したMac

まず、購入したMacは[MacBook Pro](https://www.apple.com/jp/macbook-pro-13/)の13インチ版です。
スペックは以下のようです。

```
8コアCPU、8コアGPU、16コアNeural Engineを搭載したApple M1チップ
GRAPHICS 065-C96Q 8-core GPU
16GBユニファイドメモリ
512GB SSDストレージ
True Tone搭載13インチRetinaディスプレイ
Thunderbolt / USB 4ポート x 2
Touch BarとTouch ID
PRO APPS 065-C171 NONE
SW LOGIC PRO X 065-C172 NONE
バックライトMagic Keyboard - 日本語（JIS）
```

192,280円でした。

## 周辺機器

また、開発を整えるために以下のものを購入しました。(もともと2台ディスプレイはもってました)

* マウス
  * [Magic Trackpad 2](https://www.apple.com/jp/shop/product/MJ2R2J/A/magic-trackpad-2-シルバー?fnode=ebd272c6a688b941a8bfed43c76420b73d17df962885ce4f9c52d94114ad608cf7f6558f10138bb63f45341330e33e5b9626c72cdc7c97d76719918ac3bdd95002a9090d99c4d690bc2237afecc805332f478b03cc90c537bb6968ea1c5a48914d34f17e654546b05ad3e5032cb49a0d)
    * 14,080円。なかなかのお値段。
* キーボード
  * [REALFORCE for Mac](https://www.realforce.co.jp/products/R2TL-JPVM-WH/)
    * 24,900円。想定通りのお値段。WindowsにおいてもREALFORCEの変荷重だったので、引続き購入。
* ドッキングステーション
  * [Belkin USB-C ハブ ドッキングステーション 8 in 1 M1 MacBook デュアルディスプレイ対応](https://www.amazon.co.jp/dp/B08T2BBGVL/)
    * 14,499円。想定外の出費。M1チップ搭載MacBookでは、通常モニター出力が外部ディスプレイ1つまで。2つ以上の外部ディスプレイに出力しようとなるとDisplayLink対応のアダプターやドッキングステーションが必要となるため購入しました。

下記、無念ですが、結果的に要らなかったものです。

* アダプター
  * [USB-C Digital AV Multiportアダプタ](https://www.apple.com/jp/shop/product/MUF82ZA/A/usb-c-digital-av-multiportアダプタ?fnode=540dfac785e689c1d520f2f513715743c294ddf38a598d0ac6cb6ceb9a415c5e390d7c6d14d57c0bf318235db605ff79936cf7eb0e427d15ff2c8daf4dd712457fd42eb11e83fa2904ec673616dc1e473e194d79dac24f1aff2df2ed68b9d31f3558357087e8aa5b3a94bc09c904651d&fs=fh%3D459d%252B45b0)
    * 7,480円。純正品以外は故障しやすいという評判を受け購入。結果的にBelkinのドッキングステーションを使うことになったため無駄銭。
  * [USB Type C to HDMI 変換アダプター](https://www.amazon.co.jp/gp/product/B088NNLQVS/)
    * 1,322円。２台目のディスプレイと結合するために必要と思い購入。[Display Link非対応](https://yukimejiyoung.com/macbook-air-dual/)なので無駄銭。
  

結果、机の上は以下のような感じになりました。


本当は左側のディスプレイを縦置きしたかったのですが、DisplayLinkで表示させると縦置きできないようなので諦めました。無念。

## キーカスタマイズ

[Karabiner-Elements](https://karabiner-elements.pqrs.org)を入れました。

[GokuRakuJoudo](https://github.com/yqrashawn/GokuRakuJoudo/)と、[GitHubでStarの多いKarabiner定義](https://github.com/nikitavoloboev/dotfiles/blob/master/karabiner/karabiner.edn)を元に定義を作りました。

もともとWindowsの時は(enthumble)[https://jp.enthumble.com]を利用していたので、基本的な移動は親指を使うようにしました。

以下が現状の定義です。  
https://github.com/nannany/my-settings/blob/main/karabiner.edn

## コマンド実行環境を整える

[iTerm2](https://iterm2.com)を入れました。

### パッケージマネージャー

[Homebrew](https://brew.sh/index_ja)を入れました。

### peco,ghq,hubとzle

Macに関係するかというと微妙ですが、[この記事](https://qiita.com/reireias/items/fd96d67ccf1fdffb24ed)を見てやってみたくなったので設定しました。

各コマンドは`brew install peco`,`brew install ghq`,`brew install hub`で入れました。

その上で、`.zshrc`に下記の設定を入れて、`ctrl + r`で履歴検索を、`ctrl + g`でローカルのGitリポジトリ検索を、`ctrl + b`でcloneしたGitHubリポジトリをブラウズできるようにしました。  
現状sshする機会がないので入れていませんが、`ctrl + s`でssh接続先検索も今後入れたいです。

```shell
# history
HISTFILE=$HOME/.zsh_history
HISTSIZE=100000
SAVEHIST=1000000

# share .zshhistory
setopt inc_append_history
setopt share_history

# ctrl + r
function peco-history-selection() {
    BUFFER=`history -n 1 | tac  | awk '!a[$0]++' | peco`
    CURSOR=$#BUFFER
    zle reset-prompt
}

    BUFFER="cd `ghq list -p | peco`"
zle -N peco-history-selection
bindkey '^R' peco-history-selection

# ctrl + g
function peco-ghq-selection() {
    zle accept-line
    zle reset-prompt
}

zle -N peco-ghq-selection
bindkey '^G' peco-ghq-selection

# ctrl + h
function peco-hub-selection() {
    BUFFER="hub browse `ghq list | peco | cut -d "/" -f 2,3`"
    zle accept-line
    zle reset-prompt
}

zle -N peco-hub-selection
bindkey '^B' peco-hub-selection
```

## ウィンドウ管理ツール

[Amethyst](https://github.com/ianyh/Amethyst)をinstallしました。

## ランチャー

[Alfred](https://www.alfredapp.com)をinstallしました。

# 所感

調査不足で無駄なものを買ってしまったことは後悔しましたが、色々整えた後の操作性には今のところ満足しています。(まだ1週間前後だけど)

特にKarabiner-ElementsによるキーカスタマイズはWindowsのenthumbleやのどかよりも大分融通が効く印象でした。

Alfredも課金でまだまだ改善できるところがありそうなので楽しみです。
