# THIS REPOSITORY IS OBSOLETE. CONTENT HAS BEEN MIGRATED ONTO [Keleustes](https://github.com/keleustes/)

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

List of notes taken to create original documents:

Clone airship-shipyard repo

```bash
cd airship-shipyard
cd tools/airship pegleg site -r /target collect airsloop -s collect
```

After generating in airship-treasuremap
 
```bash
cp $HOME/airship-treasuremap/collect/airship-treasuremap.yaml . 
```

Add kind, apiversion and replace (data: by spec: which is convinient for lexical ordering
of yaml dictionnaries)

```bash
sed -f ../../tools/pegleg2crd.sed airship-treasuremap.yaml > airship/airship.yaml 
```

Transfer duplicated declaration from airship.yaml to airsloop.yaml until
kustomize build works with only airship.yaml in resources and airsloop.yaml in patchMerge
sections

Note:
- Moved the duplicated/overrides from airship/airship.yaml to overlays/airsloop/airsloop.yaml
- usage of name: especially for (-global) seems inconsistent.

Note: Detected small issues in override such as:
- name: elasticsearch-global
- name: neutron-fixme

```bash
prompt$ kustomize build overlays/airsloop
Error: failed to find an object with armada.airshipit.org_v1alpha_ArmadaChart|fluent-logging to apply the patch
```

```bash
vi airship/airship.yaml overlays/airsloop/airsloop.yaml
```

Normalize using kustomize

```bash
vi airsloop/kustomize.yaml (only keep airship.yaml in resources)
kustomize build airsloop > new_airship.yaml
mv new_airship.yaml airsloop/airship.yaml
```

```bash
vi airsloop/kustomize.yaml (only keep airsloop.yaml in resources)
kustomize build airsloop > new_airsloop.yaml
mv new_airsloop.yaml overlays/airsloop/airsloop.yaml
```

Manual manipulation
- move all the DeckhandDataSchema into base/crds/crds.yaml
- created a airsloop/kustomizeconfig for each CRD left in the airsloop.yaml
- remove all the remainings "schema"

### Testing kustomize against site manifest

#### TreasureMap Airship deployment

```bash
kustomize build airship
diff <(kustomize build airship) build/generated_airship.yaml
```
#### TreasureMap Airsloop deployment

```bash
kustomize build overlays/airsloop
diff <(kustomize build overlays/airsloop) build/generated_airsloop.yaml
```

## Processing CRDs

### Notes

Here are the following issues that still need to be addresed:

- Added "jeb" or "JEB" in some "required" fields in validation. Since the substitution plugin is not implemented
  yet, some required fields are not part of the CRD hence the syntax is incorrect.
- Need to implement a plugin to automatize the usage of variables as in [replacement](https://github.com/kubekit99/kustomize-deckhand-poc/blob/master/deckhand-poc-ascrd/replacement/sample-doc.yaml). 
  This most likely means converting/moving/leveraging the substitution section of the CRDs.
- Need to implement a script to convert the layering section of the CRDs into Kustomize override.
- Need to improve the airship/kustomizeconfig to improve the "prefix" mechanism and the refs object.
- Need to understand how to leverage the crds section of airship/kustomization.yaml
- kubectl apply -k xxx is leveraging the validation of the CRDs.
- kubectl get act -n airship give the list of charts deployed.
- kubectl describe object -n airship gives a pretty user frendly view of the object
- Need to figure out how to replace the DechkhandXXX objects by secrets and get the other objects to point to those.


Will use this section to add additional notes

### Convertion into CRDs

To create the CRDs out of the DeckhandDataSchema object extracted from the original airship.yaml  

#### Procedure


```bash
csplit crds.yaml '/^---$/' '{*}'
...
lots of manual steps
```

#### CRDs Considerations

Quick notes:

- ArmadaXXX do not have proper definitions (will get definition for parrallel POCs)
- properties and additionalProperties is not supported by CRDs. (see commented out definition)
- definition and $ref are not supported by CRDs (had to inline types)
- AnyOf is not supported by CRDs. (had to peak on type)
- Deckhand type could be removed and transformed into secrets...but later.

### Improvements to kustomize

Multiple improvments have been done to kustomize
- Extend var different beyond just string. int64, bool, float64 are also supported.
- Added "Inline" concept based on the Var and NameRef syntax. This allow to copy/inline sections
  of a CRD into another CRD.
- Code available in github at: [repo](https://github.com/kubekit99/kustomize-deckhand-poc) 

### Creating CRDs in kubectl

```
make install

kubectl label nodes airship openstack-control-plane=enabled --overwrite
node/airship not labeled
kubectl label nodes airship ucp-control-plane=enabled --overwrite
node/airship not labeled
kubectl label nodes airship ceph-mds=enabled --overwrite
node/airship not labeled
kubectl label nodes airship ceph-mgr=enabled --overwrite
node/airship not labeled
kubectl label nodes airship ceph-mon=enabled --overwrite
node/airship not labeled
kubectl label nodes airship ceph-rgw=enabled --overwrite
node/airship not labeled
kubectl apply -f ./base/namespaces
namespace/ceph created
namespace/nfs created
namespace/openstack created
namespace/osh-infra created
namespace/tenant-ceph created
namespace/ucp created
namespace/pegleg created
namespace/shipyard created
namespace/drydock created
kubectl apply -f ./base/crds/
customresourcedefinition.apiextensions.k8s.io/armadacharts.armada.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/armadachartgroups.armada.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/armadamanifests.armada.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandcertificates.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandcertificateauthoritys.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandcertificateauthoritykeys.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandcertificatekeys.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandpassphrases.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandprivatekeys.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/deckhandpublickeys.deckhand.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockbaremetalnodes.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockbootactions.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockhardwareprofiles.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockhostprofiles.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydocknetworks.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydocknetworklinks.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockracks.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/drydockregions.drydock.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegaccountcatalogues.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegapparmorprofiles.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegcommonaddressess.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegcommonsoftwareconfigs.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegendpointcatalogues.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegscripts.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegseccompprofiles.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegsitedefinitions.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/peglegsoftwareversionss.pegleg.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadedockers.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadegenesiss.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadehostsystems.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadekubelets.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadekubernetesnetworks.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadekubernetesnodes.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/promenadepkicatalogs.promenade.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/shipyarddeploymentconfigurations.shipyard.airshipit.org created
customresourcedefinition.apiextensions.k8s.io/shipyarddeploymentstrategys.shipyard.airshipit.org created
kubectl apply -n ceph -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -n nfs -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -n openstack -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -n osh-infra -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -n tenant-ceph -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -n ucp -f ./base/operator
deployment.apps/armada-operator created
role.rbac.authorization.k8s.io/armada-operator created
rolebinding.rbac.authorization.k8s.io/armada-operator created
serviceaccount/armada-operator created
kubectl apply -f ./base/cluster/cluster_role.yaml
clusterrole.rbac.authorization.k8s.io/cluster-armada-operator created
kubectl apply -f ./base/cluster/cluster_role_binding.yaml
clusterrolebinding.rbac.authorization.k8s.io/cluster-armada-operator created
```

### Instantiating base airship components

- This is still WIP

Once improvment in kustomize are merged and the last bugs fixed:

To Install

```bash
kubectl apply -k airship
or kubectl apply -k overlays/airsloop/
```
Later once all the kustomize improvemnts are merged into kubectl 

```bash
kubectl apply -f build/generated_airship.yaml
or kubectl apply -f build/generated_airsloop.yaml

```bash
$ kubectl apply -f build/generated_airsloop.yaml
armadachart.armada.airshipit.org/ucp-ceph-client-update created
armadachart.armada.airshipit.org/ucp-ceph-client created
armadachart.armada.airshipit.org/ucp-ceph-ingress created
armadachart.armada.airshipit.org/ucp-ceph-mon created
armadachart.armada.airshipit.org/ucp-ceph-osd created
armadachart.armada.airshipit.org/ucp-ceph-provisioners created
armadachart.armada.airshipit.org/ucp-ceph-rgw created
armadachart.armada.airshipit.org/coredns created
armadachart.armada.airshipit.org/haproxy created
armadachart.armada.airshipit.org/ingress-kube-system created
armadachart.armada.airshipit.org/kubernetes-apiserver created
armadachart.armada.airshipit.org/kubernetes-calico-etcd created
armadachart.armada.airshipit.org/kubernetes-calico created
armadachart.armada.airshipit.org/kubernetes-controller-manager created
armadachart.armada.airshipit.org/kubernetes-etcd created
armadachart.armada.airshipit.org/kubernetes-proxy created
armadachart.armada.airshipit.org/kubernetes-scheduler created
armadachart.armada.airshipit.org/prometheus-kube-state-metrics created
armadachart.armada.airshipit.org/prometheus-node-exporter created
armadachart.armada.airshipit.org/prometheus-process-exporter created
armadachart.armada.airshipit.org/ucp-tiller created
armadachart.armada.airshipit.org/nfs-provisioner created
armadachart.armada.airshipit.org/cinder-rabbitmq created
armadachart.armada.airshipit.org/cinder created
armadachart.armada.airshipit.org/glance-rabbitmq created
armadachart.armada.airshipit.org/glance created
armadachart.armada.airshipit.org/heat-rabbitmq created
armadachart.armada.airshipit.org/heat created
armadachart.armada.airshipit.org/horizon created
armadachart.armada.airshipit.org/keystone-rabbitmq created
armadachart.armada.airshipit.org/keystone created
armadachart.armada.airshipit.org/libvirt created
armadachart.armada.airshipit.org/neutron-rabbitmq created
armadachart.armada.airshipit.org/neutron created
armadachart.armada.airshipit.org/nova-rabbitmq created
armadachart.armada.airshipit.org/nova created
armadachart.armada.airshipit.org/openstack-ceph-config created
armadachart.armada.airshipit.org/openstack-ingress-controller created
armadachart.armada.airshipit.org/openstack-mariadb created
armadachart.armada.airshipit.org/openstack-memcached created
armadachart.armada.airshipit.org/openvswitch created
armadachart.armada.airshipit.org/prometheus-openstack-exporter created
armadachart.armada.airshipit.org/tenant-ceph-config created
armadachart.armada.airshipit.org/tenant-ceph-rgw created
armadachart.armada.airshipit.org/elasticsearch created
armadachart.armada.airshipit.org/fluent-logging created
armadachart.armada.airshipit.org/grafana created
armadachart.armada.airshipit.org/kibana created
armadachart.armada.airshipit.org/nagios created
armadachart.armada.airshipit.org/osh-infra-ceph-config created
armadachart.armada.airshipit.org/osh-infra-ingress-controller created
armadachart.armada.airshipit.org/osh-infra-mariadb created
armadachart.armada.airshipit.org/osh-infra-radosgw created
armadachart.armada.airshipit.org/prometheus-alertmanager created
armadachart.armada.airshipit.org/prometheus created
armadachart.armada.airshipit.org/armada-htk created
armadachart.armada.airshipit.org/calico-htk created
armadachart.armada.airshipit.org/ceph-htk created
armadachart.armada.airshipit.org/coredns-htk created
armadachart.armada.airshipit.org/deckhand-htk created
armadachart.armada.airshipit.org/drydock-htk created
armadachart.armada.airshipit.org/haproxy-htk created
armadachart.armada.airshipit.org/ingress-kube-system-htk created
armadachart.armada.airshipit.org/kubernetes-apiserver-htk created
armadachart.armada.airshipit.org/kubernetes-calico-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-controller-manager-htk created
armadachart.armada.airshipit.org/kubernetes-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-proxy-htk created
armadachart.armada.airshipit.org/kubernetes-scheduler-htk created
armadachart.armada.airshipit.org/maas-htk created
armadachart.armada.airshipit.org/mariadb-htk created
armadachart.armada.airshipit.org/osh-helm-toolkit created
armadachart.armada.airshipit.org/osh-infra-helm-toolkit created
armadachart.armada.airshipit.org/postgres-htk created
armadachart.armada.airshipit.org/promenade-htk created
armadachart.armada.airshipit.org/shipyard-htk created
armadachart.armada.airshipit.org/tenant-ceph-htk created
armadachart.armada.airshipit.org/tiller-htk created
armadachart.armada.airshipit.org/ucp-barbican-htk created
armadachart.armada.airshipit.org/ucp-divingbell-htk created
armadachart.armada.airshipit.org/ucp-ingress-htk created
armadachart.armada.airshipit.org/ucp-keystone-htk created
armadachart.armada.airshipit.org/ucp-memcached-htk created
armadachart.armada.airshipit.org/ucp-rabbitmq-htk created
armadachart.armada.airshipit.org/tenant-ceph-client created
armadachart.armada.airshipit.org/tenant-ceph-ingress created
armadachart.armada.airshipit.org/tenant-ceph-mon created
armadachart.armada.airshipit.org/tenant-ceph-osd created
armadachart.armada.airshipit.org/podsecuritypolicy created
armadachart.armada.airshipit.org/ucp-armada created
armadachart.armada.airshipit.org/ucp-barbican created
armadachart.armada.airshipit.org/ucp-ceph-config created
armadachart.armada.airshipit.org/ucp-deckhand created
armadachart.armada.airshipit.org/ucp-divingbell created
armadachart.armada.airshipit.org/ucp-drydock created
armadachart.armada.airshipit.org/ucp-ingress created
armadachart.armada.airshipit.org/ucp-keystone-memcached created
armadachart.armada.airshipit.org/ucp-keystone created
armadachart.armada.airshipit.org/ucp-maas created
armadachart.armada.airshipit.org/ucp-mariadb created
armadachart.armada.airshipit.org/ucp-postgresql created
armadachart.armada.airshipit.org/ucp-promenade created
armadachart.armada.airshipit.org/ucp-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/ucp-rabbitmq created
armadachart.armada.airshipit.org/ucp-shipyard created
armadachartgroup.armada.airshipit.org/ingress-kube-system created
armadachartgroup.armada.airshipit.org/kubernetes-container-networking created
armadachartgroup.armada.airshipit.org/kubernetes-core created
armadachartgroup.armada.airshipit.org/kubernetes-dns created
armadachartgroup.armada.airshipit.org/kubernetes-etcd created
armadachartgroup.armada.airshipit.org/kubernetes-haproxy created
armadachartgroup.armada.airshipit.org/kubernetes-proxy created
armadachartgroup.armada.airshipit.org/openstack-ceph-config created
armadachartgroup.armada.airshipit.org/openstack-cinder created
armadachartgroup.armada.airshipit.org/openstack-compute-kit created
armadachartgroup.armada.airshipit.org/openstack-glance created
armadachartgroup.armada.airshipit.org/openstack-heat created
armadachartgroup.armada.airshipit.org/openstack-horizon created
armadachartgroup.armada.airshipit.org/openstack-ingress-controller created
armadachartgroup.armada.airshipit.org/openstack-keystone created
armadachartgroup.armada.airshipit.org/openstack-mariadb created
armadachartgroup.armada.airshipit.org/openstack-memcached created
armadachartgroup.armada.airshipit.org/openstack-radosgw created
armadachartgroup.armada.airshipit.org/openstack-tenant-ceph created
armadachartgroup.armada.airshipit.org/osh-infra-ceph-config created
armadachartgroup.armada.airshipit.org/osh-infra-dashboards created
armadachartgroup.armada.airshipit.org/osh-infra-ingress-controller created
armadachartgroup.armada.airshipit.org/osh-infra-logging created
armadachartgroup.armada.airshipit.org/osh-infra-mariadb created
armadachartgroup.armada.airshipit.org/osh-infra-monitoring created
armadachartgroup.armada.airshipit.org/osh-infra-nfs-provisioner created
armadachartgroup.armada.airshipit.org/osh-infra-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/osh-infra-radosgw created
armadachartgroup.armada.airshipit.org/podsecuritypolicy created
armadachartgroup.armada.airshipit.org/ucp-armada created
armadachartgroup.armada.airshipit.org/ucp-ceph-config created
armadachartgroup.armada.airshipit.org/ucp-ceph-update created
armadachartgroup.armada.airshipit.org/ucp-ceph created
armadachartgroup.armada.airshipit.org/ucp-core created
armadachartgroup.armada.airshipit.org/ucp-deckhand created
armadachartgroup.armada.airshipit.org/ucp-divingbell created
armadachartgroup.armada.airshipit.org/ucp-drydock created
armadachartgroup.armada.airshipit.org/ucp-keystone created
armadachartgroup.armada.airshipit.org/ucp-promenade created
armadachartgroup.armada.airshipit.org/ucp-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/ucp-shipyard created
armadamanifest.armada.airshipit.org/cluster-bootstrap created
armadamanifest.armada.airshipit.org/full-site created
deckhandcertificate.deckhand.airshipit.org/admin created
deckhandcertificate.deckhand.airshipit.org/apiserver-etcd created
deckhandcertificate.deckhand.airshipit.org/apiserver created
deckhandcertificate.deckhand.airshipit.org/armada created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/calico-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/calico-node-peer created
deckhandcertificate.deckhand.airshipit.org/calico-node created
deckhandcertificate.deckhand.airshipit.org/controller-manager created
deckhandcertificate.deckhand.airshipit.org/kubelet-airsloop-compute-1 created
deckhandcertificate.deckhand.airshipit.org/kubelet-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/kubelet-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/kubelet-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/kubelet-genesis created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-genesis-peer created
deckhandcertificate.deckhand.airshipit.org/kubernetes-etcd-genesis created
deckhandcertificate.deckhand.airshipit.org/scheduler created
deckhandcertificateauthority.deckhand.airshipit.org/calico-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/calico-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/kubernetes-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/kubernetes-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/kubernetes created
deckhandcertificateauthoritykey.deckhand.airshipit.org/calico-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/calico-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/kubernetes-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/kubernetes-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/kubernetes created
deckhandcertificatekey.deckhand.airshipit.org/admin created
deckhandcertificatekey.deckhand.airshipit.org/apiserver-etcd created
deckhandcertificatekey.deckhand.airshipit.org/apiserver created
deckhandcertificatekey.deckhand.airshipit.org/armada created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/calico-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/calico-node-peer created
deckhandcertificatekey.deckhand.airshipit.org/calico-node created
deckhandcertificatekey.deckhand.airshipit.org/controller-manager created
deckhandcertificatekey.deckhand.airshipit.org/kubelet-airsloop-compute-1 created
deckhandcertificatekey.deckhand.airshipit.org/kubelet-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/kubelet-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/kubelet-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/kubelet-genesis created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-genesis-peer created
deckhandcertificatekey.deckhand.airshipit.org/kubernetes-etcd-genesis created
deckhandcertificatekey.deckhand.airshipit.org/scheduler created
deckhandpassphrase.deckhand.airshipit.org/airsloop-crypt-password created
deckhandpassphrase.deckhand.airshipit.org/ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/ceph-swift-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ipmi-admin-password created
deckhandpassphrase.deckhand.airshipit.org/maas-region-key created
deckhandpassphrase.deckhand.airshipit.org/osh-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-barbican-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-barbican-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-barbican-password created
deckhandpassphrase.deckhand.airshipit.org/osh-barbican-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-cinder-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-cinder-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-cinder-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-cinder-password created
deckhandpassphrase.deckhand.airshipit.org/osh-cinder-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-glance-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-glance-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-glance-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-glance-password created
deckhandpassphrase.deckhand.airshipit.org/osh-glance-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-password created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-stack-user-password created
deckhandpassphrase.deckhand.airshipit.org/osh-heat-trustee-password created
deckhandpassphrase.deckhand.airshipit.org/osh-horizon-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-elasticsearch-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-grafana-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-grafana-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-grafana-oslo-db-session-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-nagios-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-openstack-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-prometheus-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-rgw-s3-admin-access-key created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-rgw-s3-admin-secret-key created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-rgw-s3-elasticsearch-access-key created
deckhandpassphrase.deckhand.airshipit.org/osh-infra-rgw-s3-elasticsearch-secret-key created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-ldap-password created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-keystone-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-neutron-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-neutron-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-neutron-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-neutron-password created
deckhandpassphrase.deckhand.airshipit.org/osh-neutron-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-nova-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/osh-nova-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-nova-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/osh-nova-password created
deckhandpassphrase.deckhand.airshipit.org/osh-nova-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/osh-oslo-cache-secret-key created
deckhandpassphrase.deckhand.airshipit.org/osh-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/osh-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/osh-placement-password created
deckhandpassphrase.deckhand.airshipit.org/private-docker-key created
deckhandpassphrase.deckhand.airshipit.org/tenant-ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/ucp-airflow-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-airflow-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-armada-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-barbican-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-deckhand-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-deckhand-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-drydock-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-drydock-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-maas-admin-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-maas-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-openstack-exporter-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-postgres-admin-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-promenade-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/ucp-shipyard-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/ucp-shipyard-postgres-password created
deckhandprivatekey.deckhand.airshipit.org/service-account created
deckhandpublickey.deckhand.airshipit.org/airship-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/airsloop-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/service-account created
drydockbaremetalnode.drydock.airshipit.org/airsloop-compute-1 created
drydockbootaction.drydock.airshipit.org/airship-target created
drydockbootaction.drydock.airshipit.org/apparmor-profiles created
drydockbootaction.drydock.airshipit.org/promjoin-systemd-unit created
drydockbootaction.drydock.airshipit.org/promjoin created
drydockbootaction.drydock.airshipit.org/seccomp-profiles created
drydockhardwareprofile.drydock.airshipit.org/dell-hp-generic created
drydockhardwareprofile.drydock.airshipit.org/dell-r720xd created
drydockhostprofile.drydock.airshipit.org/compute-r720xd created
drydockhostprofile.drydock.airshipit.org/cp created
drydockhostprofile.drydock.airshipit.org/dp created
drydocknetwork.drydock.airshipit.org/calico created
drydocknetwork.drydock.airshipit.org/oam created
drydocknetwork.drydock.airshipit.org/oob created
drydocknetwork.drydock.airshipit.org/overlay created
drydocknetwork.drydock.airshipit.org/pxe created
drydocknetwork.drydock.airshipit.org/storage created
drydocknetworklink.drydock.airshipit.org/data created
drydocknetworklink.drydock.airshipit.org/oob created
drydocknetworklink.drydock.airshipit.org/pxe created
drydockregion.drydock.airshipit.org/airsloop created
peglegaccountcatalogue.pegleg.airshipit.org/osh-infra-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/osh-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/ucp-service-accounts created
peglegapparmorprofile.pegleg.airshipit.org/airship-apparmor-loader created
peglegapparmorprofile.pegleg.airshipit.org/airship-default created
peglegcommonaddresses.pegleg.airshipit.org/common-addresses created
peglegcommonsoftwareconfig.pegleg.airshipit.org/common-software-config created
peglegendpointcatalogue.pegleg.airshipit.org/osh-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/osh-infra-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/ucp-endpoints created
peglegscript.pegleg.airshipit.org/configure-ip-rules created
peglegseccompprofile.pegleg.airshipit.org/seccomp-default created
peglegsitedefinition.pegleg.airshipit.org/airsloop created
peglegsoftwareversions.pegleg.airshipit.org/software-versions created
promenadedocker.promenade.airshipit.org/docker created
promenadegenesis.promenade.airshipit.org/genesis created
promenadehostsystem.promenade.airshipit.org/host-system created
promenadekubelet.promenade.airshipit.org/kubelet created
promenadekubernetesnetwork.promenade.airshipit.org/kubernetes-network created
promenadepkicatalog.promenade.airshipit.org/cluster-certificates created
shipyarddeploymentconfiguration.shipyard.airshipit.org/deployment-configuration created
shipyarddeploymentstrategy.shipyard.airshipit.org/deployment-strategy created
```
### Understand the deployment of the charts by the armada-operators and argo

```bash
kubectl get act --all-namespaces
NAMESPACE     NAME                                STATE      TARGET STATE   SATISFIED
ceph          ucp-ceph-client-update              running    deployed       false
ceph          ucp-ceph-mon                        running    deployed       false
ceph          ucp-ceph-rgw                        running    deployed       false
kube-system   coredns
kube-system   haproxy
kube-system   ingress-kube-system
kube-system   kubernetes-apiserver
kube-system   kubernetes-calico
kube-system   kubernetes-calico-etcd
kube-system   kubernetes-controller-manager
kube-system   kubernetes-etcd
kube-system   kubernetes-proxy
kube-system   kubernetes-scheduler
kube-system   prometheus-kube-state-metrics
kube-system   prometheus-node-exporter
kube-system   prometheus-process-exporter
kube-system   ucp-tiller
nfs           nfs-provisioner                     deployed   deployed       true
openstack     cinder                              running    deployed       false
openstack     cinder-rabbitmq                     deployed   deployed       true
openstack     elasticsearch                                  deployed
openstack     fluent-logging                                 deployed
openstack     glance                              running    deployed       false
openstack     glance-rabbitmq                     running    deployed       false
openstack     grafana                                        deployed
openstack     heat
openstack     heat-rabbitmq                       running    deployed       false
openstack     horizon
openstack     keystone                            running    deployed       false
openstack     keystone-rabbitmq                   running    deployed       false
openstack     libvirt                             running    deployed       false
openstack     neutron                             running    deployed       false
openstack     neutron-rabbitmq                    running    deployed       false
openstack     nova                                running    deployed       false
openstack     nova-rabbitmq                       running    deployed       false
openstack     openstack-ceph-config               running    deployed       false
openstack     openstack-ingress-controller        running    deployed       false
openstack     openstack-mariadb                   running    deployed       false
openstack     openstack-memcached                 running    deployed       false
openstack     openvswitch                         running    deployed       false
openstack     prometheus-openstack-exporter       running    deployed       false
openstack     tenant-ceph-config                             deployed
openstack     tenant-ceph-rgw                                deployed
osh-infra     kibana                              running    deployed       false
osh-infra     nagios                              deployed   deployed       true
osh-infra     osh-infra-ceph-config               running    deployed       false
osh-infra     osh-infra-ingress-controller        deployed   deployed       true
osh-infra     osh-infra-mariadb                   deployed   deployed       true
osh-infra     osh-infra-radosgw                   running    deployed       false
osh-infra     prometheus                          deployed   deployed       true
osh-infra     prometheus-alertmanager             deployed   deployed       true
pegleg        armada-htk
pegleg        calico-htk
pegleg        ceph-htk
pegleg        coredns-htk
pegleg        deckhand-htk
pegleg        drydock-htk
pegleg        haproxy-htk
pegleg        ingress-kube-system-htk
pegleg        kubernetes-apiserver-htk
pegleg        kubernetes-calico-etcd-htk
pegleg        kubernetes-controller-manager-htk
pegleg        kubernetes-etcd-htk
pegleg        kubernetes-proxy-htk
pegleg        kubernetes-scheduler-htk
pegleg        maas-htk
pegleg        mariadb-htk
pegleg        osh-helm-toolkit
pegleg        osh-infra-helm-toolkit
pegleg        postgres-htk
pegleg        promenade-htk
pegleg        shipyard-htk
pegleg        tenant-ceph-htk
pegleg        tiller-htk
pegleg        ucp-barbican-htk
pegleg        ucp-divingbell-htk
pegleg        ucp-ingress-htk
pegleg        ucp-keystone-htk
pegleg        ucp-memcached-htk
pegleg        ucp-rabbitmq-htk
tenant-ceph   tenant-ceph-client                  running    deployed       false
tenant-ceph   tenant-ceph-ingress                 deployed   deployed       true
tenant-ceph   tenant-ceph-mon                     running    deployed       false
tenant-ceph   tenant-ceph-osd                     deployed   deployed       true
ucp           podsecuritypolicy                   running    deployed       false
ucp           ucp-armada                          running    deployed       false
ucp           ucp-barbican                        running    deployed       false
ucp           ucp-ceph-client                     running    deployed       false
ucp           ucp-ceph-config                                deployed
ucp           ucp-ceph-ingress                    deployed   deployed       true
ucp           ucp-ceph-osd                        running    deployed       false
ucp           ucp-ceph-provisioners               running    deployed       false
ucp           ucp-deckhand                                   deployed
ucp           ucp-divingbell                                 deployed
ucp           ucp-drydock
ucp           ucp-ingress                                    deployed
ucp           ucp-keystone                                   deployed
ucp           ucp-keystone-memcached                         deployed
ucp           ucp-maas                                       deployed
ucp           ucp-mariadb                                    deployed
ucp           ucp-postgresql                                 deployed
ucp           ucp-promenade                                  deployed
ucp           ucp-prometheus-openstack-exporter              deployed
ucp           ucp-rabbitmq                                   deployed
ucp           ucp-shipyard                                   deployed
```

```bash
kubectl describe act glance-rabbitmq -n openstack

Name:         glance-rabbitmq
Namespace:    default
Labels:       component=glance
              name=glance-rabbitmq-global
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"armada.airshipit.org/v1alpha1","kind":"ArmadaChart","metadata":{"annotations":{},"labels":{"component":"glance","name":"gla...
API Version:  armada.airshipit.org/v1alpha1
Kind:         ArmadaChart
Metadata:
  Creation Timestamp:  2019-05-02T21:18:49Z
  Generation:          1
  Resource Version:    705592
  Self Link:           /apis/armada.airshipit.org/v1alpha1/namespaces/default/armadacharts/glance-rabbitmq
  UID:                 e0b77813-6d1f-11e9-8670-0800272e6982
Spec:
  Chart Name:  glance-rabbitmq
  Dependencies:
    osh-helm-toolkit
  Install:
    No Hooks:  false
  Namespace:   openstack
  Release:     glance-rabbitmq
  Source:
    Location:   https://git.openstack.org/openstack/openstack-helm-infra
    Reference:  a367bacb4bd3af55dd11dbc5c9855749a123779d
    Subpath:    rabbitmq
    Type:       git
  Upgrade:
    No Hooks:  false
    Pre:
      Delete:
        Labels:
          Release Group:  airship-glance-rabbitmq
        Type:             job
  Values:
    Endpoints:
      Oslo Messaging:
        Auth:
          Erlang Cookie:  airsloop123
          User:
            Password:  airsloop123
            Username:  glance-rabbitmq-admin
        Host Fqdn Override:
          Default:  <nil>
        Hosts:
          Default:  glance-rabbitmq
        Namespace:  openstack
        Path:       /glance
        Port:
          Amqp:
            Default:  5672
          Http:
            Default:  15672
        Scheme:       rabbit
      Prometheus Rabbitmq Exporter:
        Host Fqdn Override:
          Default:  <nil>
        Hosts:
          Default:  glance-rabbitmq-exporter
        Namespace:  openstack
        Path:
          Default:  /metrics
        Port:
          Metrics:
            Default:  9095
        Scheme:
          Default:  http
    Images:
      Tags:
    Labels:
      Prometheus Rabbitmq Exporter:
        Node Selector Key:    openstack-control-plane
        Node Selector Value:  enabled
      Server:
        Node Selector Key:    openstack-control-plane
        Node Selector Value:  enabled
    Monitoring:
      Prometheus:
        Enabled:  true
    Pod:
      Replicas:
        Server:  1
  Wait:
    Labels:
      Release Group:  airship-glance-rabbitmq
    Resources:
      Type:   statefulset
    Timeout:  900
Events:       <none>
```

```bash
jb447c@airship:~/src/github.com/kubekit99/kustomize-deckhand-poc/deckhand-poc-ascrd$ kubectl describe amf full-site
Name:         full-site
Namespace:    default
Labels:       name=full-site-global
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"armada.airshipit.org/v1alpha1","kind":"ArmadaManifest","metadata":{"annotations":{},"labels":{"name":"full-site-global"},"l...
API Version:  armada.airshipit.org/v1alpha1
Kind:         ArmadaManifest
Metadata:
  Creation Timestamp:  2019-05-02T21:18:50Z
  Generation:          1
  Resource Version:    705730
  Self Link:           /apis/armada.airshipit.org/v1alpha1/namespaces/default/armadamanifests/full-site
  UID:                 e1a6a3d9-6d1f-11e9-8670-0800272e6982
Spec:
  Chart Groups:
    podsecuritypolicy
    kubernetes-proxy
    kubernetes-container-networking
    kubernetes-dns
    kubernetes-etcd
    kubernetes-haproxy
    kubernetes-core
    ingress-kube-system
    ucp-ceph
    ucp-ceph-config
    ucp-core
    ucp-keystone
    ucp-divingbell
    ucp-armada
    ucp-deckhand
    ucp-drydock
    ucp-promenade
    ucp-shipyard
    ucp-prometheus-openstack-exporter
    osh-infra-ingress-controller
    osh-infra-ceph-config
    osh-infra-radosgw
    osh-infra-logging
    osh-infra-monitoring
    osh-infra-mariadb
    osh-infra-dashboards
    openstack-ingress-controller
    openstack-ceph-config
    openstack-tenant-ceph
    openstack-mariadb
    openstack-memcached
    openstack-keystone
    openstack-radosgw
    openstack-glance
    openstack-cinder
    openstack-compute-kit
    openstack-heat
    osh-infra-prometheus-openstack-exporter
    openstack-horizon
  Release Prefix:  airship
Events:            <none>
```

### Delete the site definition

```bash
kubectl delete -k airship
or kubectl delete -k overlays/airsloop/
```

Later once all the kustomize improvemnts are merged into kubectl 

```bash
kubectl delete -f build/generated_airship.yaml
or kubectl delete -f build/generated_airsloop.yaml
```

### Cleanup the CRD and operators

Remove the CRD definitions and the operators

```bash
$ make purge

kubectl delete -n ceph -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -n nfs -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -n openstack -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -n osh-infra -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -n tenant-ceph -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -n ucp -f ./base/operator --ignore-not-found=true
deployment.apps "armada-operator" deleted
role.rbac.authorization.k8s.io "armada-operator" deleted
rolebinding.rbac.authorization.k8s.io "armada-operator" deleted
serviceaccount "armada-operator" deleted
kubectl delete -f ./base/cluster/cluster_role_binding.yaml --ignore-not-found=true
clusterrolebinding.rbac.authorization.k8s.io "cluster-armada-operator" deleted
kubectl delete -f ./base/cluster/cluster_role.yaml --ignore-not-found=true
clusterrole.rbac.authorization.k8s.io "cluster-armada-operator" deleted
kubectl delete -f ./base/namespaces --ignore-not-found=true
namespace "ceph" deleted
namespace "nfs" deleted
namespace "openstack" deleted
namespace "osh-infra" deleted
namespace "tenant-ceph" deleted
namespace "ucp" deleted
namespace "pegleg" deleted
namespace "shipyard" deleted
namespace "drydock" deleted
kubectl delete -f ./base/crds/ --ignore-not-found=true
customresourcedefinition.apiextensions.k8s.io "armadacharts.armada.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "armadachartgroups.armada.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "armadamanifests.armada.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandcertificates.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandcertificateauthoritys.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandcertificateauthoritykeys.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandcertificatekeys.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandpassphrases.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandprivatekeys.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "deckhandpublickeys.deckhand.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockbaremetalnodes.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockbootactions.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockhardwareprofiles.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockhostprofiles.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydocknetworks.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydocknetworklinks.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockracks.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "drydockregions.drydock.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegaccountcatalogues.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegapparmorprofiles.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegcommonaddressess.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegcommonsoftwareconfigs.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegendpointcatalogues.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegscripts.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegseccompprofiles.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegsitedefinitions.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "peglegsoftwareversionss.pegleg.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadedockers.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadegenesiss.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadehostsystems.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadekubelets.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadekubernetesnetworks.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadekubernetesnodes.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "promenadepkicatalogs.promenade.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "shipyarddeploymentconfigurations.shipyard.airshipit.org" deleted
customresourcedefinition.apiextensions.k8s.io "shipyarddeploymentstrategys.shipyard.airshipit.org" deleted
```
