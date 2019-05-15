# Deckhand-Kustomize POC where objects are K8s CRDs (spec, status)

##  Introduction

- This is still work in progress
- We were success at creating kubernetes file description using kustomize
  in deckhand-kustomize-poc.
- This directory aims at finding a way to migrate from the Airship 1.x structure
  to the possible Airship 2.x structure.

##  Procedure

- Brut force fork of the airship-treasuremap files
- Keep only global, type and site directory
- add crds and kustomizeconfig under global
- create the kustomization.yaml under global, type/foundry, type/sloop
  and each site/xxx folder
- run `sed -i -f pegleg2crd.sed xxx.yaml` on all the files
- for i in `cat foo`; do sed -e '/^  name:/ s/_/-/g' $i > $i.tmp; mv $i.tmp $i; done
- for i in `cat foo`; do sed -e "/name: / s;-global$;;g" $i > $i.tmp; mv $i.tmp $i; done
- TODO: run the ../tools/readasit.py to transfer substitutions from metadata to spec

##  Testing

###  Global Config Syntax Check

```bash
kustomize build global
```

###  Type Foundry Syntax Check

```bash
kustomize build type/foundry
```

###  Type Sloop Syntax Check

```bash
kustomize build type/sloop
```

###  Site Airship-Seaworthy deployment

```bash
kustomize build site/airship-seaworthy
```

###  Site Airskiff deployment

```bash
kustomize build site/airskiff
```

###  Site Airsloop deployment

```bash
kustomize build site/airsloop
```
