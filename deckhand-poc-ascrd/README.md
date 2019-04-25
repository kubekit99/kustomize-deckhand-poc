# Deckhand-Kustomize POC where objects are K8s CRDs (spec, status)

## Simple patch merge and name reference 

```bash
kustomize build overlays/site1
diff <(kustomize build overlays/site1) build/generated_site1.yaml
```

## Test variable replacement

```bash
kustomize build overlays/replacement
diff <(kustomize build overlays/replacement) build/generated_replacement.yaml
```
