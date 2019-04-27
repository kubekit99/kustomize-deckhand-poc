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

### Convertion into CRDs

```bash
csplit crds.yaml '/^---$/' '{*}'
```

After lots of manual steps:
- ArmadaXXX do not have proper definitions (will get definition for parrallel POCs)
- properties and additionalProperties is not supported by CRDs. (see commented out definition)
- definition and $ref are not supported by CRDs (had to inline types)
- AnyOf is not supported by CRDs. (had to peak on type)
- Deckhand type could be removed and transformed into secrets...but later.

### Creating CRDs in kubectl

```
kubectl apply -f airship/crds/
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

### Verifying syntax of files with airship

This is still WIP

```bash
kubectl create namespace airship
```

```bash
kubectl apply -k airship/
armadachart.armada.airshipit.org/pref1-armada-htk created
armadachart.armada.airshipit.org/pref1-calico-htk created
armadachart.armada.airshipit.org/pref1-ceph-htk created
armadachart.armada.airshipit.org/pref1-cinder-rabbitmq created
armadachart.armada.airshipit.org/pref1-cinder created
armadachart.armada.airshipit.org/pref1-coredns-htk created
armadachart.armada.airshipit.org/pref1-coredns created
armadachart.armada.airshipit.org/pref1-deckhand-htk created
armadachart.armada.airshipit.org/pref1-drydock-htk created
armadachart.armada.airshipit.org/pref1-elasticsearch created
armadachart.armada.airshipit.org/pref1-fluent-logging created
armadachart.armada.airshipit.org/pref1-glance-rabbitmq created
armadachart.armada.airshipit.org/pref1-glance created
armadachart.armada.airshipit.org/pref1-grafana created
armadachart.armada.airshipit.org/pref1-haproxy-htk created
armadachart.armada.airshipit.org/pref1-haproxy created
armadachart.armada.airshipit.org/pref1-heat-rabbitmq created
armadachart.armada.airshipit.org/pref1-heat created
armadachart.armada.airshipit.org/pref1-horizon created
armadachart.armada.airshipit.org/pref1-ingress-kube-system-htk created
armadachart.armada.airshipit.org/pref1-ingress-kube-system created
armadachart.armada.airshipit.org/pref1-keystone-rabbitmq created
armadachart.armada.airshipit.org/pref1-keystone created
armadachart.armada.airshipit.org/pref1-kibana created
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver created
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-global created
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd created
armadachart.armada.airshipit.org/pref1-kubernetes-calico created
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager created
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-global created
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-etcd created
armadachart.armada.airshipit.org/pref1-kubernetes-proxy-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-proxy created
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler-htk created
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler created
armadachart.armada.airshipit.org/pref1-libvirt created
armadachart.armada.airshipit.org/pref1-maas-htk created
armadachart.armada.airshipit.org/pref1-mariadb-htk created
armadachart.armada.airshipit.org/pref1-nagios created
armadachart.armada.airshipit.org/pref1-neutron-rabbitmq created
armadachart.armada.airshipit.org/pref1-neutron created
armadachart.armada.airshipit.org/pref1-nfs-provisioner created
armadachart.armada.airshipit.org/pref1-nova-rabbitmq created
armadachart.armada.airshipit.org/pref1-nova created
armadachart.armada.airshipit.org/pref1-openstack-ceph-config created
armadachart.armada.airshipit.org/pref1-openstack-ingress-controller created
armadachart.armada.airshipit.org/pref1-openstack-mariadb created
armadachart.armada.airshipit.org/pref1-openstack-memcached created
armadachart.armada.airshipit.org/pref1-openvswitch created
armadachart.armada.airshipit.org/pref1-osh-helm-toolkit created
armadachart.armada.airshipit.org/pref1-osh-infra-ceph-config created
armadachart.armada.airshipit.org/pref1-osh-infra-helm-toolkit created
armadachart.armada.airshipit.org/pref1-osh-infra-ingress-controller created
armadachart.armada.airshipit.org/pref1-osh-infra-mariadb created
armadachart.armada.airshipit.org/pref1-osh-infra-radosgw created
armadachart.armada.airshipit.org/pref1-podsecuritypolicy created
armadachart.armada.airshipit.org/pref1-postgres-htk created
armadachart.armada.airshipit.org/pref1-promenade-htk created
armadachart.armada.airshipit.org/pref1-prometheus-alertmanager created
armadachart.armada.airshipit.org/pref1-prometheus-kube-state-metrics created
armadachart.armada.airshipit.org/pref1-prometheus-node-exporter created
armadachart.armada.airshipit.org/pref1-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/pref1-prometheus-process-exporter created
armadachart.armada.airshipit.org/pref1-prometheus created
armadachart.armada.airshipit.org/pref1-shipyard-htk created
armadachart.armada.airshipit.org/pref1-tenant-ceph-client-global created
armadachart.armada.airshipit.org/pref1-tenant-ceph-client created
armadachart.armada.airshipit.org/pref1-tenant-ceph-config created
armadachart.armada.airshipit.org/pref1-tenant-ceph-htk created
armadachart.armada.airshipit.org/pref1-tenant-ceph-ingress created
armadachart.armada.airshipit.org/pref1-tenant-ceph-mon created
armadachart.armada.airshipit.org/pref1-tenant-ceph-osd created
armadachart.armada.airshipit.org/pref1-tenant-ceph-rgw created
armadachart.armada.airshipit.org/pref1-tiller-htk created
armadachart.armada.airshipit.org/pref1-ucp-armada created
armadachart.armada.airshipit.org/pref1-ucp-barbican-htk created
armadachart.armada.airshipit.org/pref1-ucp-barbican created
armadachart.armada.airshipit.org/pref1-ucp-ceph-client-update-global created
armadachart.armada.airshipit.org/pref1-ucp-ceph-client created
armadachart.armada.airshipit.org/pref1-ucp-ceph-config created
armadachart.armada.airshipit.org/pref1-ucp-ceph-ingress created
armadachart.armada.airshipit.org/pref1-ucp-ceph-mon created
armadachart.armada.airshipit.org/pref1-ucp-ceph-osd created
armadachart.armada.airshipit.org/pref1-ucp-ceph-provisioners created
armadachart.armada.airshipit.org/pref1-ucp-ceph-rgw created
armadachart.armada.airshipit.org/pref1-ucp-deckhand created
armadachart.armada.airshipit.org/pref1-ucp-divingbell-global created
armadachart.armada.airshipit.org/pref1-ucp-divingbell-htk created
armadachart.armada.airshipit.org/pref1-ucp-divingbell created
armadachart.armada.airshipit.org/pref1-ucp-drydock created
armadachart.armada.airshipit.org/pref1-ucp-ingress-htk created
armadachart.armada.airshipit.org/pref1-ucp-ingress created
armadachart.armada.airshipit.org/pref1-ucp-keystone-htk created
armadachart.armada.airshipit.org/pref1-ucp-keystone-memcached created
armadachart.armada.airshipit.org/pref1-ucp-keystone created
armadachart.armada.airshipit.org/pref1-ucp-maas-global created
armadachart.armada.airshipit.org/pref1-ucp-maas created
armadachart.armada.airshipit.org/pref1-ucp-mariadb created
armadachart.armada.airshipit.org/pref1-ucp-memcached-htk created
armadachart.armada.airshipit.org/pref1-ucp-postgresql created
armadachart.armada.airshipit.org/pref1-ucp-promenade-global created
armadachart.armada.airshipit.org/pref1-ucp-promenade created
armadachart.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq-htk created
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq created
armadachart.armada.airshipit.org/pref1-ucp-shipyard created
armadachart.armada.airshipit.org/pref1-ucp-tiller created
armadachartgroup.armada.airshipit.org/pref1-ingress-kube-system created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-container-networking created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-core created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-dns created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-etcd created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-haproxy created
armadachartgroup.armada.airshipit.org/pref1-kubernetes-proxy created
armadachartgroup.armada.airshipit.org/pref1-openstack-ceph-config created
armadachartgroup.armada.airshipit.org/pref1-openstack-cinder created
armadachartgroup.armada.airshipit.org/pref1-openstack-compute-kit created
armadachartgroup.armada.airshipit.org/pref1-openstack-glance created
armadachartgroup.armada.airshipit.org/pref1-openstack-heat created
armadachartgroup.armada.airshipit.org/pref1-openstack-horizon created
armadachartgroup.armada.airshipit.org/pref1-openstack-ingress-controller created
armadachartgroup.armada.airshipit.org/pref1-openstack-keystone created
armadachartgroup.armada.airshipit.org/pref1-openstack-mariadb created
armadachartgroup.armada.airshipit.org/pref1-openstack-memcached created
armadachartgroup.armada.airshipit.org/pref1-openstack-radosgw created
armadachartgroup.armada.airshipit.org/pref1-openstack-tenant-ceph created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ceph-config created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-dashboards created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ingress-controller created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-logging created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-mariadb created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-monitoring created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-nfs-provisioner created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/pref1-osh-infra-radosgw created
armadachartgroup.armada.airshipit.org/pref1-podsecuritypolicy created
armadachartgroup.armada.airshipit.org/pref1-ucp-armada created
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-config created
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-update created
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph created
armadachartgroup.armada.airshipit.org/pref1-ucp-core created
armadachartgroup.armada.airshipit.org/pref1-ucp-deckhand created
armadachartgroup.armada.airshipit.org/pref1-ucp-divingbell created
armadachartgroup.armada.airshipit.org/pref1-ucp-drydock created
armadachartgroup.armada.airshipit.org/pref1-ucp-keystone created
armadachartgroup.armada.airshipit.org/pref1-ucp-promenade created
armadachartgroup.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/pref1-ucp-shipyard created
armadamanifest.armada.airshipit.org/pref1-cluster-bootstrap created
armadamanifest.armada.airshipit.org/pref1-full-site created
deckhandcertificate.deckhand.airshipit.org/pref1-admin created
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver-etcd created
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver created
deckhandcertificate.deckhand.airshipit.org/pref1-armada created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node created
deckhandcertificate.deckhand.airshipit.org/pref1-controller-manager created
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-genesis created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer created
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis created
deckhandcertificate.deckhand.airshipit.org/pref1-scheduler created
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes created
deckhandcertificatekey.deckhand.airshipit.org/pref1-admin created
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver-etcd created
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver created
deckhandcertificatekey.deckhand.airshipit.org/pref1-armada created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node created
deckhandcertificatekey.deckhand.airshipit.org/pref1-controller-manager created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-genesis created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis created
deckhandcertificatekey.deckhand.airshipit.org/pref1-scheduler created
deckhandpassphrase.deckhand.airshipit.org/pref1-airsloop-crypt-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-swift-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ipmi-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-maas-region-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-stack-user-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-trustee-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-horizon-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-elasticsearch-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-session-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-nagios-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-openstack-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-prometheus-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-access-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-access-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-ldap-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-cache-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-placement-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-private-docker-key created
deckhandpassphrase.deckhand.airshipit.org/pref1-tenant-ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-armada-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-openstack-exporter-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-postgres-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-promenade-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-postgres-password created
deckhandprivatekey.deckhand.airshipit.org/pref1-service-account created
deckhandpublickey.deckhand.airshipit.org/pref1-airship-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/pref1-airsloop-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/pref1-service-account created
drydockbaremetalnode.drydock.airshipit.org/pref1-airsloop-compute-1 created
drydockbootaction.drydock.airshipit.org/pref1-airship-target created
drydockbootaction.drydock.airshipit.org/pref1-apparmor-profiles created
drydockbootaction.drydock.airshipit.org/pref1-promjoin-systemd-unit created
drydockbootaction.drydock.airshipit.org/pref1-promjoin created
drydockbootaction.drydock.airshipit.org/pref1-seccomp-profiles created
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-hp-generic created
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-r720xd created
drydockhostprofile.drydock.airshipit.org/pref1-compute-r720xd created
drydockhostprofile.drydock.airshipit.org/pref1-cp-global created
drydockhostprofile.drydock.airshipit.org/pref1-dp-global created
drydocknetwork.drydock.airshipit.org/pref1-calico created
drydocknetwork.drydock.airshipit.org/pref1-oam created
drydocknetwork.drydock.airshipit.org/pref1-oob created
drydocknetwork.drydock.airshipit.org/pref1-overlay created
drydocknetwork.drydock.airshipit.org/pref1-pxe created
drydocknetwork.drydock.airshipit.org/pref1-storage created
drydocknetworklink.drydock.airshipit.org/pref1-data created
drydocknetworklink.drydock.airshipit.org/pref1-oob created
drydocknetworklink.drydock.airshipit.org/pref1-pxe created
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-infra-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/pref1-ucp-service-accounts created
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-apparmor-loader created
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-default created
peglegcommonaddresses.pegleg.airshipit.org/pref1-common-addresses created
peglegcommonsoftwareconfig.pegleg.airshipit.org/pref1-common-software-config created
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-infra-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/pref1-ucp-endpoints created
peglegscript.pegleg.airshipit.org/pref1-configure-ip-rules created
peglegseccompprofile.pegleg.airshipit.org/pref1-seccomp-default created
peglegsitedefinition.pegleg.airshipit.org/pref1-airsloop created
peglegsoftwareversions.pegleg.airshipit.org/pref1-software-versions created
promenadedocker.promenade.airshipit.org/pref1-docker-global created
shipyarddeploymentconfiguration.shipyard.airshipit.org/pref1-deployment-configuration created
shipyarddeploymentstrategy.shipyard.airshipit.org/pref1-deployment-strategy created

Error from server (Invalid): error when creating "airship/": drydockregions.drydock.airshipit.org "pref1-airsloop" ... 
Error from server (Invalid): error when creating "airship/": promenadegenesiss.promenade.airshipit.org "pref1-genesis-global" ...
Error from server (Invalid): error when creating "airship/": promenadegenesiss.promenade.airshipit.org "pref1-genesis-site" ...
Error from server (Invalid): error when creating "airship/": promenadehostsystems.promenade.airshipit.org "pref1-host-system" ...
Error from server (Invalid): error when creating "airship/": promenadekubelets.promenade.airshipit.org "pref1-kubelet" ...
Error from server (Invalid): error when creating "airship/": promenadekubernetesnetworks.promenade.airshipit.org "pref1-kubernetes-network" ...
Error from server (Invalid): error when creating "airship/": promenadepkicatalogs.promenade.airshipit.org "pref1-cluster-certificates" ...
```

To cleanup

```bash
kubectl delete -k airship
```

### Verifying syntax of files with airsloop

This is still WIP

```bash
kubectl create namespace airsloop
```

```bash
kubectl apply -k overlays/airsloop/
armadachart.armada.airshipit.org/pref2-pref1-armada-htk created
armadachart.armada.airshipit.org/pref2-pref1-calico-htk created
armadachart.armada.airshipit.org/pref2-pref1-ceph-htk created
armadachart.armada.airshipit.org/pref2-cinder-rabbitmq created
armadachart.armada.airshipit.org/pref2-cinder created
armadachart.armada.airshipit.org/pref2-pref1-coredns-htk created
armadachart.armada.airshipit.org/pref2-pref1-coredns created
armadachart.armada.airshipit.org/pref2-pref1-deckhand-htk created
armadachart.armada.airshipit.org/pref2-pref1-drydock-htk created
armadachart.armada.airshipit.org/pref2-elasticsearch created
armadachart.armada.airshipit.org/pref2-fluent-logging created
armadachart.armada.airshipit.org/pref2-glance-rabbitmq created
armadachart.armada.airshipit.org/pref2-glance created
armadachart.armada.airshipit.org/pref2-grafana created
armadachart.armada.airshipit.org/pref2-pref1-haproxy-htk created
armadachart.armada.airshipit.org/pref2-pref1-haproxy created
armadachart.armada.airshipit.org/pref2-heat-rabbitmq created
armadachart.armada.airshipit.org/pref2-heat created
armadachart.armada.airshipit.org/pref2-horizon created
armadachart.armada.airshipit.org/pref2-pref1-ingress-kube-system-htk created
armadachart.armada.airshipit.org/pref2-ingress-kube-system created
armadachart.armada.airshipit.org/pref2-keystone-rabbitmq created
armadachart.armada.airshipit.org/pref2-keystone created
armadachart.armada.airshipit.org/pref2-pref1-kibana created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-apiserver-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-apiserver created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-calico-etcd-global created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-calico-etcd-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-calico-etcd created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-calico created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-controller-manager-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-controller-manager created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-etcd-global created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-etcd-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-etcd created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-proxy-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-proxy created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-scheduler-htk created
armadachart.armada.airshipit.org/pref2-pref1-kubernetes-scheduler created
armadachart.armada.airshipit.org/pref2-pref1-libvirt created
armadachart.armada.airshipit.org/pref2-pref1-maas-htk created
armadachart.armada.airshipit.org/pref2-pref1-mariadb-htk created
armadachart.armada.airshipit.org/pref2-pref1-nagios created
armadachart.armada.airshipit.org/pref2-neutron-rabbitmq created
armadachart.armada.airshipit.org/pref2-neutron created
armadachart.armada.airshipit.org/pref2-pref1-nfs-provisioner created
armadachart.armada.airshipit.org/pref2-nova-rabbitmq created
armadachart.armada.airshipit.org/pref2-nova created
armadachart.armada.airshipit.org/pref2-pref1-openstack-ceph-config created
armadachart.armada.airshipit.org/pref2-openstack-ingress-controller created
armadachart.armada.airshipit.org/pref2-openstack-mariadb created
armadachart.armada.airshipit.org/pref2-pref1-openstack-memcached created
armadachart.armada.airshipit.org/pref2-pref1-openvswitch created
armadachart.armada.airshipit.org/pref2-pref1-osh-helm-toolkit created
armadachart.armada.airshipit.org/pref2-pref1-osh-infra-ceph-config created
armadachart.armada.airshipit.org/pref2-pref1-osh-infra-helm-toolkit created
armadachart.armada.airshipit.org/pref2-osh-infra-ingress-controller created
armadachart.armada.airshipit.org/pref2-osh-infra-mariadb created
armadachart.armada.airshipit.org/pref2-pref1-osh-infra-radosgw created
armadachart.armada.airshipit.org/pref2-pref1-podsecuritypolicy created
armadachart.armada.airshipit.org/pref2-pref1-postgres-htk created
armadachart.armada.airshipit.org/pref2-pref1-promenade-htk created
armadachart.armada.airshipit.org/pref2-pref1-prometheus-alertmanager created
armadachart.armada.airshipit.org/pref2-pref1-prometheus-kube-state-metrics created
armadachart.armada.airshipit.org/pref2-pref1-prometheus-node-exporter created
armadachart.armada.airshipit.org/pref2-pref1-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/pref2-pref1-prometheus-process-exporter created
armadachart.armada.airshipit.org/pref2-prometheus created
armadachart.armada.airshipit.org/pref2-pref1-shipyard-htk created
armadachart.armada.airshipit.org/pref2-pref1-tenant-ceph-client-global created
armadachart.armada.airshipit.org/pref2-tenant-ceph-client created
armadachart.armada.airshipit.org/pref2-pref1-tenant-ceph-config created
armadachart.armada.airshipit.org/pref2-pref1-tenant-ceph-htk created
armadachart.armada.airshipit.org/pref2-tenant-ceph-ingress created
armadachart.armada.airshipit.org/pref2-pref1-tenant-ceph-mon created
armadachart.armada.airshipit.org/pref2-tenant-ceph-osd created
armadachart.armada.airshipit.org/pref2-pref1-tenant-ceph-rgw created
armadachart.armada.airshipit.org/pref2-pref1-tiller-htk created
armadachart.armada.airshipit.org/pref2-ucp-armada created
armadachart.armada.airshipit.org/pref2-pref1-ucp-barbican-htk created
armadachart.armada.airshipit.org/pref2-ucp-barbican created
armadachart.armada.airshipit.org/pref2-pref1-ucp-ceph-client-update-global created
armadachart.armada.airshipit.org/pref2-ucp-ceph-client created
armadachart.armada.airshipit.org/pref2-pref1-ucp-ceph-config created
armadachart.armada.airshipit.org/pref2-ucp-ceph-ingress created
armadachart.armada.airshipit.org/pref2-pref1-ucp-ceph-mon created
armadachart.armada.airshipit.org/pref2-ucp-ceph-osd created
armadachart.armada.airshipit.org/pref2-ucp-ceph-provisioners created
armadachart.armada.airshipit.org/pref2-pref1-ucp-ceph-rgw created
armadachart.armada.airshipit.org/pref2-ucp-deckhand created
armadachart.armada.airshipit.org/pref2-pref1-ucp-divingbell-global created
armadachart.armada.airshipit.org/pref2-pref1-ucp-divingbell-htk created
armadachart.armada.airshipit.org/pref2-pref1-ucp-divingbell created
armadachart.armada.airshipit.org/pref2-ucp-drydock created
armadachart.armada.airshipit.org/pref2-pref1-ucp-ingress-htk created
armadachart.armada.airshipit.org/pref2-ucp-ingress created
armadachart.armada.airshipit.org/pref2-pref1-ucp-keystone-htk created
armadachart.armada.airshipit.org/pref2-pref1-ucp-keystone-memcached created
armadachart.armada.airshipit.org/pref2-ucp-keystone created
armadachart.armada.airshipit.org/pref2-pref1-ucp-maas-global created
armadachart.armada.airshipit.org/pref2-pref1-ucp-maas created
armadachart.armada.airshipit.org/pref2-ucp-mariadb created
armadachart.armada.airshipit.org/pref2-pref1-ucp-memcached-htk created
armadachart.armada.airshipit.org/pref2-pref1-ucp-postgresql created
armadachart.armada.airshipit.org/pref2-pref1-ucp-promenade-global created
armadachart.armada.airshipit.org/pref2-pref1-ucp-promenade created
armadachart.armada.airshipit.org/pref2-pref1-ucp-prometheus-openstack-exporter created
armadachart.armada.airshipit.org/pref2-pref1-ucp-rabbitmq-htk created
armadachart.armada.airshipit.org/pref2-ucp-rabbitmq created
armadachart.armada.airshipit.org/pref2-ucp-shipyard created
armadachart.armada.airshipit.org/pref2-pref1-ucp-tiller created
armadachartgroup.armada.airshipit.org/pref2-pref1-ingress-kube-system created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-container-networking created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-core created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-dns created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-etcd created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-haproxy created
armadachartgroup.armada.airshipit.org/pref2-pref1-kubernetes-proxy created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-ceph-config created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-cinder created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-compute-kit created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-glance created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-heat created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-horizon created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-ingress-controller created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-keystone created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-mariadb created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-memcached created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-radosgw created
armadachartgroup.armada.airshipit.org/pref2-pref1-openstack-tenant-ceph created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-ceph-config created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-dashboards created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-ingress-controller created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-logging created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-mariadb created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-monitoring created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-nfs-provisioner created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/pref2-pref1-osh-infra-radosgw created
armadachartgroup.armada.airshipit.org/pref2-pref1-podsecuritypolicy created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-armada created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-ceph-config created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-ceph-update created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-ceph created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-core created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-deckhand created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-divingbell created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-drydock created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-keystone created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-promenade created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-prometheus-openstack-exporter created
armadachartgroup.armada.airshipit.org/pref2-pref1-ucp-shipyard created
armadamanifest.armada.airshipit.org/pref2-cluster-bootstrap created
armadamanifest.armada.airshipit.org/pref2-full-site created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-admin created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-apiserver-etcd created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-apiserver created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-armada created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-node-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-calico-node created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-controller-manager created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-compute-1 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubelet-genesis created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-1 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-2 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-3 created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-anchor created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-genesis-peer created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-genesis created
deckhandcertificate.deckhand.airshipit.org/pref2-pref1-scheduler created
deckhandcertificateauthority.deckhand.airshipit.org/pref2-pref1-calico-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/pref2-pref1-calico-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-peer created
deckhandcertificateauthority.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd created
deckhandcertificateauthority.deckhand.airshipit.org/pref2-pref1-kubernetes created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref2-pref1-calico-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref2-pref1-calico-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-peer created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd created
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref2-pref1-kubernetes created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-admin created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-apiserver-etcd created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-apiserver created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-armada created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-node-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-calico-node created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-controller-manager created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-compute-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubelet-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubelet-genesis created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-1-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-1 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-2-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-2 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-3-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-airsloop-control-3 created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-anchor created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-genesis-peer created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-kubernetes-etcd-genesis created
deckhandcertificatekey.deckhand.airshipit.org/pref2-pref1-scheduler created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-airsloop-crypt-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ceph-swift-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ipmi-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-maas-region-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-barbican-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-barbican-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-barbican-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-barbican-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-cinder-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-cinder-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-cinder-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-cinder-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-cinder-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-glance-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-glance-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-glance-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-glance-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-glance-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-stack-user-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-heat-trustee-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-horizon-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-elasticsearch-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-grafana-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-grafana-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-grafana-oslo-db-session-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-nagios-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-openstack-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-prometheus-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-rgw-s3-admin-access-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-rgw-s3-admin-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-rgw-s3-elasticsearch-access-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-infra-rgw-s3-elasticsearch-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-ldap-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-keystone-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-neutron-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-neutron-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-neutron-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-neutron-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-neutron-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-nova-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-nova-oslo-messaging-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-nova-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-nova-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-nova-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-oslo-cache-secret-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-oslo-db-exporter-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-osh-placement-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-private-docker-key created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-tenant-ceph-fsid created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-airflow-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-airflow-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-armada-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-barbican-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-barbican-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-deckhand-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-deckhand-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-drydock-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-drydock-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-keystone-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-keystone-oslo-db-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-maas-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-maas-postgres-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-openstack-exporter-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-oslo-db-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-oslo-messaging-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-postgres-admin-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-promenade-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-rabbitmq-erlang-cookie created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-shipyard-keystone-password created
deckhandpassphrase.deckhand.airshipit.org/pref2-pref1-ucp-shipyard-postgres-password created
deckhandprivatekey.deckhand.airshipit.org/pref2-pref1-service-account created
deckhandpublickey.deckhand.airshipit.org/pref2-pref1-airship-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/pref2-pref1-airsloop-ssh-public-key created
deckhandpublickey.deckhand.airshipit.org/pref2-pref1-service-account created
drydockbaremetalnode.drydock.airshipit.org/pref2-pref1-airsloop-compute-1 created
drydockbootaction.drydock.airshipit.org/pref2-pref1-airship-target created
drydockbootaction.drydock.airshipit.org/pref2-pref1-apparmor-profiles created
drydockbootaction.drydock.airshipit.org/pref2-pref1-promjoin-systemd-unit created
drydockbootaction.drydock.airshipit.org/pref2-pref1-promjoin created
drydockbootaction.drydock.airshipit.org/pref2-pref1-seccomp-profiles created
drydockhardwareprofile.drydock.airshipit.org/pref2-pref1-dell-hp-generic created
drydockhardwareprofile.drydock.airshipit.org/pref2-pref1-dell-r720xd created
drydockhostprofile.drydock.airshipit.org/pref2-pref1-compute-r720xd created
drydockhostprofile.drydock.airshipit.org/pref2-pref1-cp-global created
drydockhostprofile.drydock.airshipit.org/pref2-pref1-dp-global created
drydocknetwork.drydock.airshipit.org/pref2-pref1-calico created
drydocknetwork.drydock.airshipit.org/pref2-pref1-oam created
drydocknetwork.drydock.airshipit.org/pref2-pref1-oob created
drydocknetwork.drydock.airshipit.org/pref2-pref1-overlay created
drydocknetwork.drydock.airshipit.org/pref2-pref1-pxe created
drydocknetwork.drydock.airshipit.org/pref2-pref1-storage created
drydocknetworklink.drydock.airshipit.org/pref2-pref1-data created
drydocknetworklink.drydock.airshipit.org/pref2-pref1-oob created
drydocknetworklink.drydock.airshipit.org/pref2-pref1-pxe created
peglegaccountcatalogue.pegleg.airshipit.org/pref2-pref1-osh-infra-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/pref2-pref1-osh-service-accounts created
peglegaccountcatalogue.pegleg.airshipit.org/pref2-pref1-ucp-service-accounts created
peglegapparmorprofile.pegleg.airshipit.org/pref2-pref1-airship-apparmor-loader created
peglegapparmorprofile.pegleg.airshipit.org/pref2-pref1-airship-default created
peglegcommonaddresses.pegleg.airshipit.org/pref2-pref1-common-addresses created
peglegcommonsoftwareconfig.pegleg.airshipit.org/pref2-pref1-common-software-config created
peglegendpointcatalogue.pegleg.airshipit.org/pref2-pref1-osh-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/pref2-pref1-osh-infra-endpoints created
peglegendpointcatalogue.pegleg.airshipit.org/pref2-pref1-ucp-endpoints created
peglegscript.pegleg.airshipit.org/pref2-pref1-configure-ip-rules created
peglegseccompprofile.pegleg.airshipit.org/pref2-pref1-seccomp-default created
peglegsitedefinition.pegleg.airshipit.org/pref2-pref1-airsloop created
peglegsoftwareversions.pegleg.airshipit.org/pref2-pref1-software-versions created
promenadedocker.promenade.airshipit.org/pref2-pref1-docker-global created
shipyarddeploymentconfiguration.shipyard.airshipit.org/pref2-pref1-deployment-configuration created
shipyarddeploymentstrategy.shipyard.airshipit.org/pref2-pref1-deployment-strategy created

Error from server (Invalid): error when creating "airship/": drydockregions.drydock.airshipit.org "pref2-pref1-airsloop" ... 
Error from server (Invalid): error when creating "airship/": promenadegenesiss.promenade.airshipit.org "pref2-pref1-genesis-global" ...
Error from server (Invalid): error when creating "airship/": promenadegenesiss.promenade.airshipit.org "pref2-pref1-genesis-site" ...
Error from server (Invalid): error when creating "airship/": promenadehostsystems.promenade.airshipit.org "pref2-pref1-host-system" ...
Error from server (Invalid): error when creating "airship/": promenadekubelets.promenade.airshipit.org "pref2-pref1-kubelet" ...
Error from server (Invalid): error when creating "airship/": promenadekubernetesnetworks.promenade.airshipit.org "pref2-pref1-kubernetes-network" ...
Error from server (Invalid): error when creating "airship/": promenadepkicatalogs.promenade.airshipit.org "pref2-pref1-cluster-certificates" ...
```

To cleanup

```bash
kubectl delete -k overlays/airsloop
```
