package main

import (
	"fmt"
	"net"
)

func main() {
	// マルチキャストアドレスとポート
	multicastAddr := "224.0.0.1:9999"

	// UDP接続を作成
	addr, err := net.ResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		panic(err)
	}

	conn, err := net.ListenMulticastUDP("udp", nil, addr)
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	fmt.Printf("UDP multicast client listening on %s\n", multicastAddr)

	// バッファを作成
	buffer := make([]byte, 1024)

	for {
		// マルチキャストメッセージを受信
		n, srcAddr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Printf("Error reading message: %v\n", err)
			continue
		}

		// 受信したメッセージを表示
		message := string(buffer[:n])
		fmt.Printf("Received from %s: %s\n", srcAddr, message)
	}
}
