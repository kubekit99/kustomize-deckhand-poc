# Actual deckhand poc

## json based replace patch

```bash
kustomize build overlays/staging
diff <(kustomize build overlay/staging) build/generated_staging.yml
```

## json based replace add

```bash
kustomize build overlays/production
diff <(kustomize build overlays/production) build/generated_production.yaml 
```
