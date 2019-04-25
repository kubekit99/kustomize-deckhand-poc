# Deckhand-Kustomize POC with minimal changes to deckhand documents

## json possible patch

kustomize supports patches based on [JSONPatch](https://tools.ietf.org/html/rfc6902)

```json
   [
     { "op": "test", "path": "/a/b/c", "value": "foo" },
     { "op": "remove", "path": "/a/b/c" },
     { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] },
     { "op": "replace", "path": "/a/b/c", "value": 42 },
     { "op": "move", "from": "/a/b/c", "path": "/a/b/d" },
     { "op": "copy", "from": "/a/b/d", "path": "/a/b/e" }
   ]
```

## json based full replace

```bash
kustomize build overlays/replacejson
diff <(kustomize build overlays/replacejson) build/generated_replacejson.yml
```

## json based add

```bash
kustomize build overlays/addjson
diff <(kustomize build overlays/addjson) build/generated_addjson.yaml 
```

## json based replace and remove

```bash
kustomize build overlays/replaceone
diff <(kustomize build overlays/replaceone) build/generated_replaceone.yaml 
```

## standard patch merge

```bash
kustomize build overlays/patchmerge
diff <(kustomize build overlays/patchmerge) build/generated_patchmerge.yaml 
```

Check that replacejson and patchmerge have the same result on the objects

```bash
diff <(kustomize build overlays/patchmerge) <(kustomize build overlays/replacejson)
```


