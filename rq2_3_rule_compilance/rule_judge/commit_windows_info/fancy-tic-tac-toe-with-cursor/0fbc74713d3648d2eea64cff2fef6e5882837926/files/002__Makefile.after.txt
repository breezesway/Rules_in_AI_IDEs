

web/static/main.wasm: *.go
	GOOS=js GOARCH=wasm go build -o web/static/main.wasm

run: web/static/main.wasm
	cd web/static && python3 -m http.server 8080

