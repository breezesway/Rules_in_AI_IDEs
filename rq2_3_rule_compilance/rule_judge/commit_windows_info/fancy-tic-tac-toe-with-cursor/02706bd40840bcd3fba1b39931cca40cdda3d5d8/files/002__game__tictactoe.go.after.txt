package game

type Game struct {
	board [9]string
	text  string
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
