# Deckhand-Kustomize POC where objects are K8s CRDs (spec, status)

## json based replace patch

```bash
kustomize build overlays/site1 > build/generated_site1.yaml
diff <(kustomize build overlays/site1) build/generated_site1.yaml
```
