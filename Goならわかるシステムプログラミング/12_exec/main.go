package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	if len(os.Args) == 1 {
		return
	}

	cmd := exec.Command(os.Args[1], os.Args[2:]...)
	err := cmd.Run()
	if err != nil {
		panic(err)
	}

	state := cmd.ProcessState
	// 各種情報をprint
	fmt.Printf("%v\n", state.String())
	// pid
	fmt.Printf("Process ID: %d\n", state.Pid())
	// system time
	fmt.Printf("System Time: %s\n", state.SystemTime())
	// user time
	fmt.Printf("User Time: %s\n", state.UserTime())
}
