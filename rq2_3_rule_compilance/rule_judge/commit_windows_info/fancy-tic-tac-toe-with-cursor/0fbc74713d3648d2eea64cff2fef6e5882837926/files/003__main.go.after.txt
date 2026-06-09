//go:build js && wasm

package main

import "syscall/js"

type Game struct {
	Board []string
}

func NewGame() *Game {
	return &Game{
		Board: make([]string, 9),
	}
}

func main() {
	c := make(chan struct{}, 0)

	// Register our game in JavaScript
	js.Global().Set("tictactoeGame", js.ValueOf(map[string]interface{}{
		"newGame": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			game := NewGame()
			return game.Board
		}),
	}))

	<-c // Keep running
}
