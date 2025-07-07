package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	// マルチキャストアドレスとポート
	multicastAddr := "224.0.0.1:9999"

	// UDP接続を作成
	addr, err := net.ResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		panic(err)
	}

	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	fmt.Printf("UDP multicast time server started on %s\n", multicastAddr)

	// 1秒ごとに時報を送信
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// 現在時刻を取得してフォーマット
			now := time.Now()
			timeStr := now.Format("2006-01-02 15:04:05")
			message := fmt.Sprintf("Time: %s", timeStr)

			// マルチキャストで送信
			_, err := conn.Write([]byte(message))
			if err != nil {
				fmt.Printf("Error sending message: %v\n", err)
			} else {
				fmt.Printf("Sent: %s\n", message)
			}
		}
	}
}
