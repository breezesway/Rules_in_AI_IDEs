package game

import "testing"

func TestText(t *testing.T) {
	game := NewGame()
	if game.Text() != "hello" {
		t.Errorf("Expected text to be 'hello', got %q", game.Text())
	}
}
