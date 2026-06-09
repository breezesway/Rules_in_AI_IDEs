package game

import (
	"fmt"
)

type Game struct {
	board   [9]string
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
		xIsNext: true, // X plays first
	}
}

func (g *Game) Text() string {
	if g.xIsNext {
		return "X to move"
	}
	return "O to move"
}

func (g *Game) Board() [9]string {
	return g.board
}

func (g *Game) Winner() string {
	winningCombinations := [][3]int{
		{0, 1, 2}, // Top row
		{3, 4, 5}, // Middle row
		{6, 7, 8}, // Bottom row
		{0, 3, 6}, // Left column
		{1, 4, 7}, // Middle column
		{2, 5, 8}, // Right column
		{0, 4, 8}, // Diagonal \
		{2, 4, 6}, // Diagonal /
	}

	for _, combo := range winningCombinations {
		if g.board[combo[0]] != "" && g.board[combo[0]] == g.board[combo[1]] && g.board[combo[1]] == g.board[combo[2]] {
			return g.board[combo[0]] // Return the winner ("X" or "O")
		}
	}

	return "" // No winner
}
