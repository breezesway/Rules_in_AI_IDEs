//go:build js && wasm

package main

import (
	"syscall/js"
	"tictactoe/game"
)

func main() {
	c := make(chan struct{}, 0)

	g := game.NewGame()

	// Register our game in JavaScript
	js.Global().Set("game", js.ValueOf(map[string]interface{}{
		"text": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			return g.Text()
		}),
		"board": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			board := g.Board()
			// Convert Go array to JavaScript array
			jsBoard := make([]interface{}, len(board))
			for i, cell := range board {
				jsBoard[i] = cell
			}
			return jsBoard
		}),
	}))

	<-c // Keep running
}
