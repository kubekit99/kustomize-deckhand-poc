all: test

clean:
	rm -fr build/_output

kustomize:
	go build -o  custom-plugin/xdgconfig/kustomize/kustomize kustomize.go

kvmaker:
	go build --buildmode plugin --tags=plugin -o custom-plugin/xdgconfig/kustomize/plugin/kvSources/kvMaker.so plugins/deckhand.airshipit.org/v1/kvMaker.go

stringprefixer:
	go build --buildmode plugin --tags=plugin -o custom-plugin/xdgconfig/kustomize/plugin/deckhand.airshipit.org/v1/StringPrefixer.so plugins/deckhand.airshipit.org/v1/StringPrefixer.go

dateprefixer:
	go build --buildmode plugin --tags=plugin -o custom-plugin/xdgconfig/kustomize/plugin/deckhand.airshipit.org/v1/DatePrefixer.so plugins/deckhand.airshipit.org/v1/DatePrefixer.go

servicegenerator:
	go build --buildmode plugin --tags=plugin -o custom-plugin/xdgconfig/kustomize/plugin/deckhand.airshipit.org/v1/ServiceGenerator.so plugins/deckhand.airshipit.org/v1/ServiceGenerator.go

test: stringprefixer dateprefixer kvmaker servicegenerator
	XDG_CONFIG_HOME=custom-plugin/xdgconfig kustomize build --enable_alpha_goplugins_accept_panic_risk custom-plugin
