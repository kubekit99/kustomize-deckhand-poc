# Notes

## Test rendering

```bash 
kustomize build ./overlay/site1
```

## Using kubectl 1.14

```bash
prompt$ kubectl apply -k overlays/site1/

configmap/site1-the-configmap created
secret/site1-site-values created
secret/site1-the-secret created
deployment.apps/site1-the-deployment created
```

```bash
prompt$ kubectl get all
NAME                                        READY   STATUS              RESTARTS   AGE
pod/site1-the-deployment-75d577dd78-c4n8j   0/1     RunContainerError   0          6s
pod/site1-the-deployment-75d577dd78-ckbwh   0/1     RunContainerError   1          6s
pod/site1-the-deployment-75d577dd78-lqhk5   0/1     RunContainerError   1          6s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   5h22m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/site1-the-deployment   0/3     3            0           6s

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/site1-the-deployment-75d577dd78   3         3         0       6s
```

```bash
kubectl describe deployment/site1-the-deployment
Name:                   site1-the-deployment
Namespace:              default
CreationTimestamp:      Tue, 23 Apr 2019 15:09:40 -0500
Labels:                 app=demo-var
Annotations:            deployment.kubernetes.io/revision: 1
                        kubectl.kubernetes.io/last-applied-configuration:
                          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"app":"demo-var"},"name":"site1-the-deployment","namesp...
Selector:               app=demo-var
Replicas:               3 desired | 3 updated | 3 total | 0 available | 3 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=demo-var
           deployment=hello
  Containers:
   the-container:
    Image:      monopole/hello:1
    Port:       8080/TCP
    Host Port:  0/TCP
    Command:
      hello
      --port=8080
      site1-the-deployment
    Environment:
      SECRET_TOKEN:  site1-the-secret
      VALUE_1:       YWRtaW4=
      VALUE_2:       MWYyZDFlMmU2N2Rm
      VALUE_3:       site1-specific-value
    Mounts:          <none>
  Volumes:           <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   site1-the-deployment-75d577dd78 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  92s   deployment-controller  Scaled up replica set site1-the-deployment-75d577dd78 to 3
```
