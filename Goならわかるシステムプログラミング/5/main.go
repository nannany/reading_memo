package main

import (
	"fmt"
	"os"
)

func main() {
	// ディレクトリを作成
	err := os.Mkdir("testdir", 0755)
	if err != nil {
		fmt.Printf("ディレクトリ作成エラー: %v\n", err)
		return
	}
	fmt.Println("ディレクトリ 'testdir' を作成しました")

	// ファイルを作成
	file, err := os.Create("testdir/sample.txt")
	if err != nil {
		fmt.Printf("ファイル作成エラー: %v\n", err)
		return
	}
	defer file.Close()

	// ファイルに書き込み
	content := "これはサンプルファイルです。\n作成日時: " + fmt.Sprintf("%v", os.Getenv("USER"))
	_, err = file.WriteString(content)
	if err != nil {
		fmt.Printf("ファイル書き込みエラー: %v\n", err)
		return
	}

	fmt.Println("ファイル 'testdir/sample.txt' を作成しました")

	// 作成したファイルの情報を表示
	info, err := file.Stat()
	if err != nil {
		fmt.Printf("ファイル情報取得エラー: %v\n", err)
		return
	}

	fmt.Printf("ファイルサイズ: %d bytes\n", info.Size())
	fmt.Printf("作成時刻: %v\n", info.ModTime())
}
