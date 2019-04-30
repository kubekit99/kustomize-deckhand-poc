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

### Creating CRDs in kubectl

```
kubectl apply -f base/crds/

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
```

### Instantiating base airship components

- This is still WIP

```bash
kubectl create namespace airship
```

```bash
kubectl apply -k airship/

armadachart.armada.airshipit.org/armada-htk created
armadachart.armada.airshipit.org/calico-htk created
armadachart.armada.airshipit.org/ceph-htk created
armadachart.armada.airshipit.org/cinder-rabbitmq created
armadachart.armada.airshipit.org/cinder created
armadachart.armada.airshipit.org/coredns-htk created
armadachart.armada.airshipit.org/coredns created
armadachart.armada.airshipit.org/deckhand-htk created
armadachart.armada.airshipit.org/drydock-htk created
armadachart.armada.airshipit.org/elasticsearch created
armadachart.armada.airshipit.org/fluent-logging created
armadachart.armada.airshipit.org/glance-rabbitmq created
armadachart.armada.airshipit.org/glance created
armadachart.armada.airshipit.org/grafana created
armadachart.armada.airshipit.org/haproxy-htk created
armadachart.armada.airshipit.org/haproxy created
armadachart.armada.airshipit.org/heat-rabbitmq created
armadachart.armada.airshipit.org/heat created
armadachart.armada.airshipit.org/horizon created
armadachart.armada.airshipit.org/ingress-kube-system-htk created
armadachart.armada.airshipit.org/ingress-kube-system created
armadachart.armada.airshipit.org/keystone-rabbitmq created
armadachart.armada.airshipit.org/keystone created
armadachart.armada.airshipit.org/kibana created
armadachart.armada.airshipit.org/kubernetes-apiserver-htk created
armadachart.armada.airshipit.org/kubernetes-apiserver created
armadachart.armada.airshipit.org/kubernetes-calico-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-calico-etcd created
armadachart.armada.airshipit.org/kubernetes-calico created
armadachart.armada.airshipit.org/kubernetes-controller-manager-htk created
armadachart.armada.airshipit.org/kubernetes-controller-manager created
armadachart.armada.airshipit.org/kubernetes-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-etcd created
armadachart.armada.airshipit.org/kubernetes-proxy-htk created
armadachart.armada.airshipit.org/kubernetes-proxy created
armadachart.armada.airshipit.org/kubernetes-scheduler-htk created
armadachart.armada.airshipit.org/kubernetes-scheduler created
armadachart.armada.airshipit.org/libvirt created
armadachart.armada.airshipit.org/maas-htk created
armadachart.armada.airshipit.org/mariadb-htk created
armadachart.armada.airshipit.org/nagios created
armadachart.armada.airshipit.org/neutron-rabbitmq created
armadachart.armada.airshipit.org/neutron created
armadachart.armada.airshipit.org/nfs-provisioner created
armadachart.armada.airshipit.org/nova-rabbitmq created
armadachart.armada.airshipit.org/nova created
armadachart.armada.airshipit.org/openstack-ceph-config created
armadachart.armada.airshipit.org/openstack-ingress-controller created
armadachart.armada.airshipit.org/openstack-mariadb created
armadachart.armada.airshipit.org/openstack-memcached created
armadachart.armada.airshipit.org/openvswitch created
armadachart.armada.airshipit.org/osh-helm-toolkit created
armadachart.armada.airshipit.org/osh-infra-ceph-config created
armadachart.armada.airshipit.org/osh-infra-helm-toolkit created
armadachart.armada.airshipit.org/osh-infra-ingress-controller created
armadachart.armada.airshipit.org/osh-infra-mariadb created
armadachart.armada.airshipit.org/osh-infra-radosgw created
armadachart.armada.airshipit.org/podsecuritypolicy created
armadachart.armada.airshipit.org/postgres-htk created
armadachart.armada.airshipit.org/promenade-htk created
armadachart.armada.airshipit.org/prometheus-alertmanager created
armadachart.armada.airshipit.org/prometheus-kube-state-metrics created
armadachart.armada.airshipit.org/prometheus-node-exporter created
armadachart.armada.airshipit.org/prometheus-openstack-exporter created
armadachart.armada.airshipit.org/prometheus-process-exporter created
armadachart.armada.airshipit.org/prometheus created
armadachart.armada.airshipit.org/shipyard-htk created
armadachart.armada.airshipit.org/tenant-ceph-client created
armadachart.armada.airshipit.org/tenant-ceph-config created
armadachart.armada.airshipit.org/tenant-ceph-htk created
armadachart.armada.airshipit.org/tenant-ceph-ingress created
armadachart.armada.airshipit.org/tenant-ceph-mon created
armadachart.armada.airshipit.org/tenant-ceph-osd created
armadachart.armada.airshipit.org/tenant-ceph-rgw created
armadachart.armada.airshipit.org/tiller-htk created
armadachart.armada.airshipit.org/ucp-armada created
armadachart.armada.airshipit.org/ucp-barbican-htk created
armadachart.armada.airshipit.org/ucp-barbican created
armadachart.armada.airshipit.org/ucp-ceph-client-update created
armadachart.armada.airshipit.org/ucp-ceph-client created
armadachart.armada.airshipit.org/ucp-ceph-config created
armadachart.armada.airshipit.org/ucp-ceph-ingress created
armadachart.armada.airshipit.org/ucp-ceph-mon created
armadachart.armada.airshipit.org/ucp-ceph-osd created
armadachart.armada.airshipit.org/ucp-ceph-provisioners created
armadachart.armada.airshipit.org/ucp-ceph-rgw created
armadachart.armada.airshipit.org/ucp-deckhand created
armadachart.armada.airshipit.org/ucp-divingbell-htk created
armadachart.armada.airshipit.org/ucp-divingbell created
armadachart.armada.airshipit.org/ucp-drydock created
armadachart.armada.airshipit.org/ucp-ingress-htk created
armadachart.armada.airshipit.org/ucp-ingress created
armadachart.armada.airshipit.org/ucp-keystone-htk created
armadachart.armada.airshipit.org/ucp-keystone-memcached created
armadachart.armada.airshipit.org/ucp-keystone created
armadachart.armada.airshipit.org/ucp-maas created
armadachart.armada.airshipit.org/ucp-mariadb created
armadachart.armada.airshipit.org/ucp-memcached-htk created
armadachart.armada.airshipit.org/ucp-postgresql created
armadachart.armada.airshipit.org/ucp-promenade created
armadachart.armada.airshipit.org/ucp-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/ucp-rabbitmq-htk created
armadachart.armada.airshipit.org/ucp-rabbitmq created
armadachart.armada.airshipit.org/ucp-shipyard created
armadachart.armada.airshipit.org/ucp-tiller created
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

To cleanup

```bash
kubectl delete -k airship
```

### Instantiating base airsloop components

- This is still WIP

```bash
kubectl create namespace airsloop
```

```bash
kubectl apply -k overlays/airsloop/

armadachart.armada.airshipit.org/armada-htk created
armadachart.armada.airshipit.org/calico-htk created
armadachart.armada.airshipit.org/ceph-htk created
armadachart.armada.airshipit.org/cinder-rabbitmq created
armadachart.armada.airshipit.org/cinder created
armadachart.armada.airshipit.org/coredns-htk created
armadachart.armada.airshipit.org/coredns created
armadachart.armada.airshipit.org/deckhand-htk created
armadachart.armada.airshipit.org/drydock-htk created
armadachart.armada.airshipit.org/elasticsearch created
armadachart.armada.airshipit.org/fluent-logging created
armadachart.armada.airshipit.org/glance-rabbitmq created
armadachart.armada.airshipit.org/glance created
armadachart.armada.airshipit.org/grafana created
armadachart.armada.airshipit.org/haproxy-htk created
armadachart.armada.airshipit.org/haproxy created
armadachart.armada.airshipit.org/heat-rabbitmq created
armadachart.armada.airshipit.org/heat created
armadachart.armada.airshipit.org/horizon created
armadachart.armada.airshipit.org/ingress-kube-system-htk created
armadachart.armada.airshipit.org/ingress-kube-system created
armadachart.armada.airshipit.org/keystone-rabbitmq created
armadachart.armada.airshipit.org/keystone created
armadachart.armada.airshipit.org/kibana created
armadachart.armada.airshipit.org/kubernetes-apiserver-htk created
armadachart.armada.airshipit.org/kubernetes-apiserver created
armadachart.armada.airshipit.org/kubernetes-calico-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-calico-etcd created
armadachart.armada.airshipit.org/kubernetes-calico created
armadachart.armada.airshipit.org/kubernetes-controller-manager-htk created
armadachart.armada.airshipit.org/kubernetes-controller-manager created
armadachart.armada.airshipit.org/kubernetes-etcd-htk created
armadachart.armada.airshipit.org/kubernetes-etcd created
armadachart.armada.airshipit.org/kubernetes-proxy-htk created
armadachart.armada.airshipit.org/kubernetes-proxy created
armadachart.armada.airshipit.org/kubernetes-scheduler-htk created
armadachart.armada.airshipit.org/kubernetes-scheduler created
armadachart.armada.airshipit.org/libvirt created
armadachart.armada.airshipit.org/maas-htk created
armadachart.armada.airshipit.org/mariadb-htk created
armadachart.armada.airshipit.org/nagios created
armadachart.armada.airshipit.org/neutron-rabbitmq created
armadachart.armada.airshipit.org/neutron created
armadachart.armada.airshipit.org/nfs-provisioner created
armadachart.armada.airshipit.org/nova-rabbitmq created
armadachart.armada.airshipit.org/nova created
armadachart.armada.airshipit.org/openstack-ceph-config created
armadachart.armada.airshipit.org/openstack-ingress-controller created
armadachart.armada.airshipit.org/openstack-mariadb created
armadachart.armada.airshipit.org/openstack-memcached created
armadachart.armada.airshipit.org/openvswitch created
armadachart.armada.airshipit.org/osh-helm-toolkit created
armadachart.armada.airshipit.org/osh-infra-ceph-config created
armadachart.armada.airshipit.org/osh-infra-helm-toolkit created
armadachart.armada.airshipit.org/osh-infra-ingress-controller created
armadachart.armada.airshipit.org/osh-infra-mariadb created
armadachart.armada.airshipit.org/osh-infra-radosgw created
armadachart.armada.airshipit.org/podsecuritypolicy created
armadachart.armada.airshipit.org/postgres-htk created
armadachart.armada.airshipit.org/promenade-htk created
armadachart.armada.airshipit.org/prometheus-alertmanager created
armadachart.armada.airshipit.org/prometheus-kube-state-metrics created
armadachart.armada.airshipit.org/prometheus-node-exporter created
armadachart.armada.airshipit.org/prometheus-openstack-exporter created
armadachart.armada.airshipit.org/prometheus-process-exporter created
armadachart.armada.airshipit.org/prometheus created
armadachart.armada.airshipit.org/shipyard-htk created
armadachart.armada.airshipit.org/tenant-ceph-client created
armadachart.armada.airshipit.org/tenant-ceph-config created
armadachart.armada.airshipit.org/tenant-ceph-htk created
armadachart.armada.airshipit.org/tenant-ceph-ingress created
armadachart.armada.airshipit.org/tenant-ceph-mon created
armadachart.armada.airshipit.org/tenant-ceph-osd created
armadachart.armada.airshipit.org/tenant-ceph-rgw created
armadachart.armada.airshipit.org/tiller-htk created
armadachart.armada.airshipit.org/ucp-armada created
armadachart.armada.airshipit.org/ucp-barbican-htk created
armadachart.armada.airshipit.org/ucp-barbican created
armadachart.armada.airshipit.org/ucp-ceph-client-update created
armadachart.armada.airshipit.org/ucp-ceph-client created
armadachart.armada.airshipit.org/ucp-ceph-config created
armadachart.armada.airshipit.org/ucp-ceph-ingress created
armadachart.armada.airshipit.org/ucp-ceph-mon created
armadachart.armada.airshipit.org/ucp-ceph-osd created
armadachart.armada.airshipit.org/ucp-ceph-provisioners created
armadachart.armada.airshipit.org/ucp-ceph-rgw created
armadachart.armada.airshipit.org/ucp-deckhand created
armadachart.armada.airshipit.org/ucp-divingbell-htk created
armadachart.armada.airshipit.org/ucp-divingbell created
armadachart.armada.airshipit.org/ucp-drydock created
armadachart.armada.airshipit.org/ucp-ingress-htk created
armadachart.armada.airshipit.org/ucp-ingress created
armadachart.armada.airshipit.org/ucp-keystone-htk created
armadachart.armada.airshipit.org/ucp-keystone-memcached created
armadachart.armada.airshipit.org/ucp-keystone created
armadachart.armada.airshipit.org/ucp-maas created
armadachart.armada.airshipit.org/ucp-mariadb created
armadachart.armada.airshipit.org/ucp-memcached-htk created
armadachart.armada.airshipit.org/ucp-postgresql created
armadachart.armada.airshipit.org/ucp-promenade created
armadachart.armada.airshipit.org/ucp-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/ucp-rabbitmq-htk created
armadachart.armada.airshipit.org/ucp-rabbitmq created
armadachart.armada.airshipit.org/ucp-shipyard created
armadachart.armada.airshipit.org/ucp-tiller created
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

To cleanup

```bash
kubectl delete -k overlays/airsloop
```
