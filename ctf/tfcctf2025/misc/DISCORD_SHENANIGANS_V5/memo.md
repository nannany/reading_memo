https://chatgpt.com/c/68b19832-3988-832d-9441-84755b0a367a

```text
The announcement shenanigans are in play again.
As a small hint, maybe bulking up on the nothingness was the best way to hide it. ;) Go get your shovels ready!

Leave the photos alone, man! The flag is not there.
```

```text
発表の悪ふざけがまた始まった。
ちょっとしたヒントとして、何もないところを膨らませることが、それを隠す最良の方法だったのかもしれない。） シャベルを用意してこい！

写真はほっとけよ！旗がない。
```

----

とりあえずdiscordのannouncementsに貼ってあった画像は upcoming_tfcctf.png という名前で保存した。

---

`zsteg upcoming_tfcctf.png`すると

```text

b1,r,lsb,xy         .. file: MPEG ADTS, AAC, v4 Main, 88.2 kHz, surround + side

b1,r,msb,xy         .. 
b1,g,lsb,xy         .. file: MPEG ADTS, AAC, v4 Main, 96 kHz

b1,g,msb,xy         .. 
b1,b,lsb,xy         .. file: MPEG ADTS, AAC, v4 LTP, 96 kHz
```

これはrgbのlsb(最後のビット)に音声データ(ADTS/AAC)が隠されていることを示している。


```shell
# 赤チャンネル LSB, bit1
zsteg -E b1,r,lsb,xy upcoming_tfcctf.png > r_b1_lsb_xy.bin

# 緑
zsteg -E b1,g,lsb,xy upcoming_tfcctf.png > g_b1_lsb_xy.bin

# 青
zsteg -E b1,b,lsb,xy upcoming_tfcctf.png > b_b1_lsb_xy.bin


zsteg -E b1,rgb,lsb,xy upcoming_tfcctf.png > rgb_b1_lsb_xy.bin

```

ここまでやってみたけどffmpegでwavに変換することができない。

諦め。

# 参考
なんか良さげなサイトあった。
https://georgeom.net/StegOnline/image

ただ、これでは解けず。


