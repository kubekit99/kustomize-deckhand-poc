# kustomize-patch-non-k8s
# original code:
https://github.com/johnhny/kustomize-patch-non-k8s

patchesStrategicMerge for non-kubernetes resources
https://github.com/kubernetes-sigs/kustomize/issues/742

## Additional Notes

Added the kustomizeconfig directory

```bash
diff <(kustomize build deployment) generated_deployment.yml
```

```bash
diff <(kustomize build bee) generated_bee.yml
```

