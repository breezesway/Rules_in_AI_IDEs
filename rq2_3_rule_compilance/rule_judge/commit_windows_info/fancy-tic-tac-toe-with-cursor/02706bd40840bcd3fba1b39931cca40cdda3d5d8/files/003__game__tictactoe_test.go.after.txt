package game

import (
	"github.com/stretchr/testify/assert"
	"testing"
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
