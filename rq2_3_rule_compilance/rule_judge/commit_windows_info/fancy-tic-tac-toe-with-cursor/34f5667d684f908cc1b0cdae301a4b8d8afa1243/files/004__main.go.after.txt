package main

import "fmt"

func getGreeting(name string) string {
	if name == "" {
		return "Hello, World!"
	}
	return "Hello, " + name + "!"
}

func main() {
	fmt.Println(getGreeting(""))
}
