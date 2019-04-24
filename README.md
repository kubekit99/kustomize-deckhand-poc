# kustomize-deckhand-poc
Validate the utilization of kustomize to emulate airship-deckhand feature

## kustomize-examples

For convinience purpose, the examples provided with kustomize have been forked here.

## deckhand-functional-tests

For convinience purpose, in order to check parity between deckhand features and kustomize,
the deckhand functional test have been forked here.

## hello-world

- Simple warm up for kustomize utilisation.
- Mainly leverage mergePatch between K8s objects in [kustomization.yaml](./hello-world/overlays/staging/kustomization.yaml) 
- For more details, access associated [README](./hello-world/README.md)

## variable-replacements

- Simple usage of kustomize.
- Mainly leverage vars section in [kustomization.yaml](./variable-replacements/overlays/site1/kustomization.yaml) 
- For more details, access associated [README](./variable-replacements/README.md)

## kustomize-patch-non-k8s

- Forked out of example listed in kustomize issue list
- Validate that simple merge of non k8s objects is possible [kustomization.yaml](./kustomize-patch-non-k8s/bee/kustomization.yaml) 
- For more details, access associated [README](./kustomize-patch-non-k8s/README.md)

## kustomize-crd

- Built out of official README.md for handling CRD configtransformer
- Mainly leverage configuration section in [kustomization.yaml](./kustomize-crd/base/kustomization.yaml) 
- For more details, access associated [README](./kustomize-crd/README.md)

## new-kustomize-config

- WIP
- Currently contains result of `kustomize config save -d`
- Produced files can be referred in the `configurations` sections of the kustomization.yaml
- For more details, access associated [README](./new-kustomize-config/README.md)

## deckhand-poc-asit

- resources are configured using structure as close as possible to existing deckhand.
  apiversion and kind are added to the original yaml file.
- Currently contains armadamanifest and deckhand document
- For more details, access associated [README](./deckhand-poc-asit/README.md)

## deckhand-poc-ascrd

- resources are configured as a little more K8s compliant CRD
- Currently contains armadamanifest and deckhand document
- For more details, access associated [README](./deckhand-poc-ascrd/README.md)
