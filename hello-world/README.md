# THIS REPOSITORY IS OBSOLETE. CONTENT HAS BEEN MIGRATED ONTO [Keleustes](https://github.com/keleustes/)

# Notes

## Test rendering

```bash 
kustomize build ./overlay/staging > ./build/staging.yaml
kustomize build ./overlay/production > ./build/production.yaml
```

## Using kubectl 1.14

```bash
prompt$ kubectl apply -k overlays/staging/

configmap/staging-the-map created
service/staging-the-service created
deployment.apps/staging-the-deployment created
```

```bash
prompt$ kubectl get all

NAME                                          READY   STATUS    RESTARTS   AGE
pod/staging-the-deployment-69b9c8c646-r5cjd   1/1     Running   0          84s
pod/staging-the-deployment-69b9c8c646-w2j54   1/1     Running   0          84s
pod/staging-the-deployment-69b9c8c646-z46ps   1/1     Running   0          84s

NAME                          TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes            ClusterIP      10.96.0.1       <none>        443/TCP          142m
service/staging-the-service   LoadBalancer   10.103.235.68   <pending>     8666:31556/TCP   84s

NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/staging-the-deployment   3/3     3            3           84s

NAME                                                DESIRED   CURRENT   READY   AGE
replicaset.apps/staging-the-deployment-69b9c8c646   3         3         3       84s

```

```bash
prompt$ kubectl delete -k overlays/staging/

configmap "staging-the-map" deleted
service "staging-the-service" deleted
deployment.apps "staging-the-deployment" deleted
```

```bash
prompt$ kubectl get all

NAME                                          READY   STATUS        RESTARTS   AGE
pod/staging-the-deployment-69b9c8c646-r5cjd   0/1     Terminating   0          3m17s
pod/staging-the-deployment-69b9c8c646-w2j54   0/1     Terminating   0          3m17s
pod/staging-the-deployment-69b9c8c646-z46ps   0/1     Terminating   0          3m17s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   144m
```
