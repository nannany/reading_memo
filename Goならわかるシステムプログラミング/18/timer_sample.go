package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("Timer processing sample")

	// time.After を使った基本的なタイマー
	fmt.Println("5秒後にメッセージを表示します...")
	timer1 := time.After(5 * time.Second)
	<-timer1
	fmt.Println("5秒経過しました！")

	// time.Ticker を使った定期実行
	fmt.Println("1秒間隔で3回メッセージを表示します...")
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ticker.C:
			count++
			fmt.Printf("Tick %d回目 (現在時刻: %s)\n", count, time.Now().Format("15:04:05"))
			if count >= 3 {
				fmt.Println("終了します")
				return
			}
		}
	}
}
