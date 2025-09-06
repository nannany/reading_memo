```text
I put my flag into this program, but now I lost the flag. Here is the program, and the output. Could you use it to find the flag?
```

## Writeup (ImaginaryCTF 2025 – comparing)

### 概要
- `comparing.cpp` はフラグを2文字ずつ `(flag[2i], flag[2i+1], i)` のタプルにして優先度キューへ。
- 比較関数は「(文字1のASCII)+(文字2のASCII)」が小さいタプルほど先に出る（実質 min-heap）。
- キューから2つずつ取り出し，1行目は i1 の1文字目と i2 の1文字目，2行目は i1 の2文字目と i2 の2文字目を使って出力文字列を生成する。

### 出力フォーマット
- 偶数 i のとき `even(val1, val3, i)` を出力:
  - `x = str(val1) + str(val3)`（val1 は i1 の1文字目ASCII，val3 は i2 の1文字目ASCII）
  - `s = x + str(i) + reversed(x)` という左右対称構造。
- 奇数 i のとき `odd(val1, val3, i)` を出力:
  - `s = str(val1) + str(val3) + str(i)`（加算ロジックは実質0）。
- 2行目は同様に，`val2`（i1 の2文字目ASCII）と `val4`（i2 の2文字目ASCII）で作る。

ポイント: 各行にはインデックス i が含まれる（偶数は中央，奇数は末尾）。偶数行は左右対称から i の位置と `x` を一意に復元できる。

### 復元手順
1) 出力を2行1組（ペア）で処理。
   - 1行目から i1 と (i1の1文字目, i2の1文字目) を復元。
   - 2行目から i2 と (i1の2文字目, i2の2文字目) を復元。
2) これを全ペア分繰り返し，インデックス i ごとに `(flag[2i], flag[2i+1])` を埋める。
3) i=0..15 の順で連結してフラグ完成。

比較関数は合計値のタイブレークをしていないが，上記の復元は行順に依存しないため問題なし。

### ソルバ
- 追加ファイル: `ctf/ImaginaryCTF_2025/comparing/solve.py`
- 使い方:
  - `python3 ctf/ImaginaryCTF_2025/comparing/solve.py < ctf/ImaginaryCTF_2025/comparing/output.txt`
- 出力されたフラグ:

```
ictf{cu3st0m_c0mp@r@t0rs_1e8f9e}
```
