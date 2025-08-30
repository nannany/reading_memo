# 起動

- ビルド: `docker build -t slippy .`
- 起動: `docker run --rm -it -p 3000:3000 slippy`

# symlink

symlink扱いのファイルをzipに入れてやると /etc/passwd はダウンロードすることはできた。
同じ容量で `$randdir/flag.txt` を取れる。が、$randdirがわからない。


