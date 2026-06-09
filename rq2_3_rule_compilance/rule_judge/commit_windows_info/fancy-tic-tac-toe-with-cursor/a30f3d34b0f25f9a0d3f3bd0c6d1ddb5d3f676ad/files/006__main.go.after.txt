//go:build js && wasm

package main

import (
	"syscall/js"
	"tictactoe/game"
)

func main() {
	c := make(chan struct{}, 0)

	game := game.NewGame()

	// Register our game in JavaScript
	js.Global().Set("tictactoeGame", js.ValueOf(map[string]interface{}{
		"newGame": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			return game.Board()
		}),
		"text": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			return game.Text()
		}),
	}))

	<-c // Keep running
}
