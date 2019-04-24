# Changing Kustomize configuration

## Saving current configuration

```bash
prompt$ kustomize config save -d base/kustomizeconfig
```

## Modifying Kustomize configuration

```bash
prompt$ cd base/kustomizeconfig
prompt$ ls
```
## Using new Kustomize Configuration

- Note 0: Still WIP
- Note 1: the configurations of the kustomization.yaml has been created in brute force way.
- Note 2: Would probably not want to override all the defaults of kustomize tools as
  this example shows.

```bash
prompt$ kustomize build base
```

