//go:build js && wasm

package main

import "syscall/js"

type Game struct {
	Board []string
	text  string
}

func NewGame() *Game {
	return &Game{
		Board: make([]string, 9),
		text:  "hello",
	}
}

func (g *Game) Text() string {
	return g.text
}

func main() {
	c := make(chan struct{}, 0)

	game := NewGame()

	// Register our game in JavaScript
	js.Global().Set("tictactoeGame", js.ValueOf(map[string]interface{}{
		"newGame": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			return game.Board
		}),
		"text": js.FuncOf(func(this js.Value, args []js.Value) interface{} {
			return game.Text()
		}),
	}))

	<-c // Keep running
}
