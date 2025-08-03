.global _start # このラベルが外部公開されるという宣言
.text # これから先はプログラムが始まる宣言
_start:
mov $1, %rax # writeシステムコール（1）
mov $1, %rdi # 出力先ファイルハンドル（1: stdout）をセット
lea message(%rip), %rsi # 出力したいメッセージアドレスをセット
mov $13, %rdx # 文字数をセット
syscall # writeの実行
mov $60, %rax # exitシステムコール
xor %rdi, %rdi # リターンコード（ここではエラーなし、0）
syscall # 終了呼び出し
message: # データ領域のラベル（いわゆる定数名）
.ascii "Hello, world\n" # テキストデータ
