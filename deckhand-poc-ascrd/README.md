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
sed -f ../tools/asit2crd.sed airship-treasuremap.yaml > airship/airship.yaml
```

Manual manipulation
- move all the DeckhandDataSchema into airsloop/crds/crds.yaml
- created a airsloop/kustomizeconfig for each CRD left in the airsloop.yaml
- remove all the remainings "schema"

### Testing kustomize against site manifest

#### TreasureMap Airship deployment

Note: Moved the duplicated/overrides from airship/airship.yaml to overlays/airsloop/airsloop.yaml

```bash
kustomize build airship
diff <(kustomize build airship) build/generated_airship.yaml
```
#### TreasureMap Airsloop deployment

Note: Detected small issues in override such as:
- name: elasticsearch-global
- name: neutron-fixme


```bash
prompt$ kustomize build overlays/airsloop
Error: failed to find an object with armada.airshipit.org_v1alpha_ArmadaChart|fluent-logging to apply the patch
```

```bash
kustomize build overlays/airsloop
diff <(kustomize build overlays/airsloop) build/generated_airsloop.yaml
```

## Processing CRDs

```bash
csplit crds.yaml '/^---$/' '{*}'
```

