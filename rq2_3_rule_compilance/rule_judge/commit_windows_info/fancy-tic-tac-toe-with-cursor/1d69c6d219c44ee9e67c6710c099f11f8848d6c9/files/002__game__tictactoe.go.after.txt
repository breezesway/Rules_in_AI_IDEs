package game

import (
	"fmt"
)

type Game struct {
	board [9]string
	text  string
}

func (g *Game) MakeMove(position int) error {
	if position < 0 || position > 8 {
		return fmt.Errorf("invalid position")
	}
	if g.Board()[position] != "" {
		return fmt.Errorf("cell already occupied")
	}
	g.board[position] = "X"
	return nil
}

func NewGame() *Game {
	return &Game{
		board: [9]string{"", "", "", "", "", "", "", "", ""},
		text:  "hello",
	}
}

func (g *Game) Text() string {
	return g.text
}

func (g *Game) Board() [9]string {
	return g.board
}
