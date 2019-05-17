# THIS REPOSITORY IS OBSOLETE. CONTENT HAS BEEN MIGRATED ONTO [Keleustes](https://github.com/keleustes/)

# Official Kustomize Plugin demo

## Build using builtin-plugins

```bash
kustomize build builtin-plugins
diff <(kustomize build builtin-plugins) build/generated_builtin.yaml
```
## Build using custom-plugins

```bash
kvSources=custom-plugin/xdgconfig/kustomize/plugins/kvSources
mkdir -p $kvSources
go build -buildmode plugin -o $kvSources/kvMaker.so custom-plugin/kvMaker.go
```

```bash
XDG_CONFIG_HOME=custom-plugin/xdgconfig kustomize build --enable_alpha_goplugins_accept_panic_risk custom-plugin
diff <(XDG_CONFIG_HOME=custom-plugin/xdgconfig kustomize build --enable_alpha_goplugins_accept_panic_risk custom-plugin) build/generated_custom.yaml
```

