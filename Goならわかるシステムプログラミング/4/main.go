package main

import (
	"time"
)

func main() {
	println("start")
	// 時刻を表示
	timer := time.After(10 * time.Second)

	<-timer
	println("10s")
}
