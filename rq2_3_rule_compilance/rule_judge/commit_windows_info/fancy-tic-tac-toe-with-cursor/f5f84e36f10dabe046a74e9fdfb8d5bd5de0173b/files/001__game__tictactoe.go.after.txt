package game

import (
	"fmt"
)

type Game struct {
	board   [9]string
	text    string
	xIsNext bool
}

func (g *Game) MakeMove(position int) error {
	if position < 0 || position >= len(g.board) {
		return fmt.Errorf("invalid position")
	}
	if g.board[position] != "" {
		return fmt.Errorf("cell already occupied")
	}
	if g.xIsNext {
		g.board[position] = "X"
	} else {
		g.board[position] = "O"
	}
	g.xIsNext = !g.xIsNext // Switch turns
	return nil
}

func NewGame() *Game {
	return &Game{
		board:   [9]string{"", "", "", "", "", "", "", "", ""},
		text:    "hello",
		xIsNext: true, // X plays first
	}
}

func (g *Game) Text() string {
	return g.text
}

func (g *Game) Board() [9]string {
	return g.board
}
