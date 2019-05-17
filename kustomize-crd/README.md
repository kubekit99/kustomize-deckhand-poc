# THIS REPOSITORY IS OBSOLETE. CONTENT HAS BEEN MIGRATED ONTO [Keleustes](https://github.com/keleustes/)

# Official CRD-Kustomize demo

## Build

```bash
kustomize build demo > build/generated.yaml
```

## Test

```bash
kustomize build demo | grep -A 2 ".*Ref"
```

```bash
kustomize build demo | grep BEE_ACTION
```
