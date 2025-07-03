package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/http/httputil"
	"strings"
)

func main() {
	listener, err := net.Listen("tcp", ":8888")
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	fmt.Println("HTTP server listening on :8888")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}

		go func(conn net.Conn) {
			defer conn.Close()

			// Parse the HTTP request
			req, err := http.ReadRequest(bufio.NewReader(conn))
			if err != nil {
				fmt.Printf("Error reading request: %v\n", err)
				return
			}

			// Dump the request to standard output
			dump, err := httputil.DumpRequest(req, true)
			if err != nil {
				fmt.Printf("Error dumping request: %v\n", err)
				return
			}

			fmt.Printf("Request received:\n%s\n", dump)

			// Send a simple response
			response := http.Response{
				StatusCode: http.StatusOK,
				ProtoMajor: 1,
				ProtoMinor: 1,
				Body:       io.NopCloser(strings.NewReader("Hello, World!")),
			}
			response.Write(conn)
		}(conn)
	}
}
