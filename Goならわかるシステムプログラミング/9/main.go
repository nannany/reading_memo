package main

import (
	"fmt"
	"io"
	"os"
)

func open(filename, data string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.WriteString(data)
	return err
}

func read(filename string) (string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return "", err
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}

	return string(content), nil
}

func main() {
	filename := "sample.txt"
	data := "Hello, World!\nThis is a sample file created with os.Create().\n"

	// ファイルを作成して書き込み
	err := open(filename, data)
	if err != nil {
		panic(err)
	}
	fmt.Printf("File '%s' created and written.\n", filename)

	// ファイルを読み込み
	content, err := read(filename)
	if err != nil {
		panic(err)
	}
	fmt.Printf("File content:\n%s", content)

	// ファイルを削除
	err = os.Remove(filename)
	if err != nil {
		panic(err)
	}
	fmt.Printf("File '%s' deleted.\n", filename)
}
