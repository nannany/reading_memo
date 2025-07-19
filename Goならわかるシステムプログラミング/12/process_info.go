package main

import (
	"fmt"
	"os"
	"runtime"
)

func main() {
	// プロセスID取得
	fmt.Printf("Process ID: %d\n", os.Getpid())

	// 親プロセスID取得
	fmt.Printf("Parent Process ID: %d\n", os.Getppid())

	// 実行中のgoroutine数
	fmt.Printf("Number of goroutines: %d\n", runtime.NumGoroutine())

	// CPU使用数
	fmt.Printf("Number of CPUs: %d\n", runtime.NumCPU())

	// 実行ファイル名取得
	if exec, err := os.Executable(); err == nil {
		fmt.Printf("Executable: %s\n", exec)
	}

	// 作業ディレクトリ取得
	if wd, err := os.Getwd(); err == nil {
		fmt.Printf("Working directory: %s\n", wd)
	}

	// 環境変数取得（一部）
	fmt.Printf("PATH: %s\n", os.Getenv("PATH"))
	fmt.Printf("HOME: %s\n", os.Getenv("HOME"))

	// ユーザID・グループID取得
	fmt.Printf("User ID: %d\n", os.Getuid())
	fmt.Printf("E User ID: %d\n", os.Geteuid())
	fmt.Printf("Group ID: %d\n", os.Getgid())
	fmt.Printf("E Group ID: %d\n", os.Getegid())

}
