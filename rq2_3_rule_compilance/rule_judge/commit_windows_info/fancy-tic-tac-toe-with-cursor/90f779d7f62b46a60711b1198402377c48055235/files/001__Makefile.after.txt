GOFILES := $(shell find . -name '*.go')
WASMFILE := web/static/main.wasm
WASMEXEC := web/static/wasm_exec.js

$(WASMFILE): $(GOFILES)
	GOOS=js GOARCH=wasm go build -o $(WASMFILE)

.PHONY: test
test:
	go test ./...

$(WASMEXEC):
	cp "$(shell go env GOROOT)/lib/wasm/wasm_exec.js" $(WASMEXEC)

.PHONY: serve
serve:
	cd web/static && python -m http.server 8080

.PHONY: setup
setup: $(WASMEXEC) $(WASMFILE)

.PHONY: watch
watch:
	fswatch -o . -e ".*" -i "\\.go$$" | xargs -n1 -I{} make

