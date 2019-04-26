# Deckhand-Kustomize POC where objects are K8s CRDs (spec, status)

## Simple patch merge and name reference 

```bash
kustomize build overlays/site1
diff <(kustomize build overlays/site1) build/generated_site1.yaml
```

## Test variable replacement

```bash
kustomize build replacement
diff <(kustomize build replacement) build/generated_replacement.yaml
```

## Airsloop Document Testing

### Generating airsloop.yaml from original documents

Clone airship-shipyard repo

```bash
cd arship-shipyard
cd tools/airship pegleg site -r /target collect airsloop -s collect
```

```bash
cp /home/jb447c/proj/nc_openstack/airship-treasuremap/collect/airship-treasuremap.yaml .
sed -f ../tools/asit2crd.sed airship-treasuremap.yaml > airsloop/airsloop.yaml
```

Manual manipulation
- move all the DeckhandDataSchema into airsloop/crds/crds.yaml
- created a airsloop/kustomizeconfig for each CRD left in the airsloop.yaml
- remove all the remainings "schema"

### Testing kustomize against site manifest

```bash
kustomize build replacement
diff <(kustomize build replacement) build/generated_replacement.yaml
```

