package main

import (
	"fmt"
	"io"
	"net"
)

func main() {
	// Connect to localhost:8888 using net.Dial()
	conn, err := net.Dial("tcp", "localhost:8888")
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	// Send HTTP GET request
	request := "GET / HTTP/1.1\r\n" +
		"Host: localhost:8888\r\n" +
		"User-Agent: Go-Client\r\n" +
		"Connection: close\r\n" +
		"\r\n"

	// Write the request to the connection
	_, err = conn.Write([]byte(request))
	if err != nil {
		panic(err)
	}

	// Read the response
	response, err := io.ReadAll(conn)
	if err != nil {
		panic(err)
	}

	// Print the response
	fmt.Printf("Response from server:\n%s\n", string(response))
}
