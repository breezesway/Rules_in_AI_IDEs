package game

type Game struct {
	board []string
	text  string
}

func (g *Game) Board() interface{} {
	return g.board
}

func NewGame() *Game {
	return &Game{
		board: make([]string, 9),
		text:  "hello",
	}
}

func (g *Game) Text() string {
	return g.text
}
