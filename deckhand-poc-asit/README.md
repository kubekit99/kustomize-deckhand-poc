# Deckhand-Kustomize POC with minimal changes to deckhand documents

## json based replace patch

```bash
kustomize build overlays/replacejson
diff <(kustomize build overlay/replacejson) build/generated_replacejson.yml
```

## json based replace add

```bash
kustomize build overlays/addjson
diff <(kustomize build overlays/addjson) build/generated_addjson.yaml 
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


