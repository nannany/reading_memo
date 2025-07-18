package main

import (
	"fmt"
	"log"
	"os"
	"syscall"
	"unsafe"
)

const (
	EV_ADD     = 0x0001
	EV_DELETE  = 0x0002
	EV_CLEAR   = 0x0020
	EV_ENABLE  = 0x0004
	EV_ONESHOT = 0x0010

	EVFILT_VNODE = (-4)

	NOTE_DELETE = 0x0001
	NOTE_WRITE  = 0x0002
	NOTE_EXTEND = 0x0004
	NOTE_ATTRIB = 0x0008
	NOTE_LINK   = 0x0010
	NOTE_RENAME = 0x0020
	NOTE_REVOKE = 0x0040
)

type Kevent struct {
	Ident  uint64
	Filter int16
	Flags  uint16
	Fflags uint32
	Data   int64
	Udata  *byte
}

func watchFile(filename string) {
	kq, err := syscall.Kqueue()
	if err != nil {
		log.Fatal("kqueue error:", err)
	}
	defer syscall.Close(kq)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal("open file error:", err)
	}
	defer file.Close()

	fd := int(file.Fd())

	var event Kevent
	event.Ident = uint64(fd)
	event.Filter = EVFILT_VNODE
	event.Flags = EV_ADD | EV_CLEAR
	event.Fflags = NOTE_DELETE | NOTE_WRITE | NOTE_EXTEND | NOTE_ATTRIB | NOTE_LINK | NOTE_RENAME | NOTE_REVOKE

	_, _, errno := syscall.Syscall6(
		syscall.SYS_KEVENT,
		uintptr(kq),
		uintptr(unsafe.Pointer(&event)),
		1,
		0,
		0,
		0,
	)

	if errno != 0 {
		log.Fatal("kevent register error:", errno)
	}

	fmt.Printf("Watching file: %s\n", filename)
	fmt.Println("Waiting for events... (Press Ctrl+C to stop)")

	for {
		var events [10]Kevent
		n, _, errno := syscall.Syscall6(
			syscall.SYS_KEVENT,
			uintptr(kq),
			0,
			0,
			uintptr(unsafe.Pointer(&events[0])),
			uintptr(len(events)),
			0,
		)

		if errno != 0 {
			log.Fatal("kevent wait error:", errno)
		}

		for i := 0; i < int(n); i++ {
			event := events[i]

			fmt.Printf("Event received on fd %d: ", event.Ident)

			if event.Fflags&NOTE_DELETE != 0 {
				fmt.Print("DELETE ")
			}
			if event.Fflags&NOTE_WRITE != 0 {
				fmt.Print("WRITE ")
			}
			if event.Fflags&NOTE_EXTEND != 0 {
				fmt.Print("EXTEND ")
			}
			if event.Fflags&NOTE_ATTRIB != 0 {
				fmt.Print("ATTRIB ")
			}
			if event.Fflags&NOTE_LINK != 0 {
				fmt.Print("LINK ")
			}
			if event.Fflags&NOTE_RENAME != 0 {
				fmt.Print("RENAME ")
			}
			if event.Fflags&NOTE_REVOKE != 0 {
				fmt.Print("REVOKE ")
			}

			fmt.Println()
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run kqueue_file_watcher.go <filename>")
		os.Exit(1)
	}

	filename := os.Args[1]

	if _, err := os.Stat(filename); os.IsNotExist(err) {
		fmt.Printf("File %s does not exist\n", filename)
		os.Exit(1)
	}

	watchFile(filename)
}
