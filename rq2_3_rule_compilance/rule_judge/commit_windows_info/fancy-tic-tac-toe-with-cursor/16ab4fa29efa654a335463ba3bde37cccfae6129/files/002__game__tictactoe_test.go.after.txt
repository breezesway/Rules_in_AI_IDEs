package game

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestText(t *testing.T) {
	game := NewGame()
	assert.Equal(t, "hello", game.Text(), "should return hello text")
}

func TestInitialBoard(t *testing.T) {
	game := NewGame()
	expected := [9]string{"", "", "", "", "", "", "", "", ""}

	assert.Equal(t, expected, game.Board(), "should start with empty board")
}

func TestMakeMove(t *testing.T) {
	game := NewGame()
	game.MakeMove(4) // center cell

	board := game.Board()
	assert.Equal(t, "X", board[4], "should place X in the center cell")
}
