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
armadachart.armada.airshipit.org/pref1-armada-htk configured
armadachart.armada.airshipit.org/pref1-calico-htk configured
armadachart.armada.airshipit.org/pref1-ceph-htk configured
armadachart.armada.airshipit.org/pref1-cinder-rabbitmq configured
armadachart.armada.airshipit.org/pref1-cinder configured
armadachart.armada.airshipit.org/pref1-coredns-htk configured
armadachart.armada.airshipit.org/pref1-coredns configured
armadachart.armada.airshipit.org/pref1-deckhand-htk configured
armadachart.armada.airshipit.org/pref1-drydock-htk configured
armadachart.armada.airshipit.org/pref1-elasticsearch configured
armadachart.armada.airshipit.org/pref1-fluent-logging configured
armadachart.armada.airshipit.org/pref1-glance-rabbitmq configured
armadachart.armada.airshipit.org/pref1-glance configured
armadachart.armada.airshipit.org/pref1-grafana configured
armadachart.armada.airshipit.org/pref1-haproxy-htk configured
armadachart.armada.airshipit.org/pref1-haproxy configured
armadachart.armada.airshipit.org/pref1-heat-rabbitmq configured
armadachart.armada.airshipit.org/pref1-heat configured
armadachart.armada.airshipit.org/pref1-horizon configured
armadachart.armada.airshipit.org/pref1-ingress-kube-system-htk configured
armadachart.armada.airshipit.org/pref1-ingress-kube-system configured
armadachart.armada.airshipit.org/pref1-keystone-rabbitmq configured
armadachart.armada.airshipit.org/pref1-keystone configured
armadachart.armada.airshipit.org/pref1-kibana configured
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-global configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico configured
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-global configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd configured
armadachart.armada.airshipit.org/pref1-kubernetes-proxy-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-proxy configured
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler configured
armadachart.armada.airshipit.org/pref1-libvirt configured
armadachart.armada.airshipit.org/pref1-maas-htk configured
armadachart.armada.airshipit.org/pref1-mariadb-htk configured
armadachart.armada.airshipit.org/pref1-nagios configured
armadachart.armada.airshipit.org/pref1-neutron-rabbitmq configured
armadachart.armada.airshipit.org/pref1-neutron configured
armadachart.armada.airshipit.org/pref1-nfs-provisioner configured
armadachart.armada.airshipit.org/pref1-nova-rabbitmq configured
armadachart.armada.airshipit.org/pref1-nova configured
armadachart.armada.airshipit.org/pref1-openstack-ceph-config configured
armadachart.armada.airshipit.org/pref1-openstack-ingress-controller configured
armadachart.armada.airshipit.org/pref1-openstack-mariadb configured
armadachart.armada.airshipit.org/pref1-openstack-memcached configured
armadachart.armada.airshipit.org/pref1-openvswitch configured
armadachart.armada.airshipit.org/pref1-osh-helm-toolkit configured
armadachart.armada.airshipit.org/pref1-osh-infra-ceph-config configured
armadachart.armada.airshipit.org/pref1-osh-infra-helm-toolkit configured
armadachart.armada.airshipit.org/pref1-osh-infra-ingress-controller configured
armadachart.armada.airshipit.org/pref1-osh-infra-mariadb configured
armadachart.armada.airshipit.org/pref1-osh-infra-radosgw configured
armadachart.armada.airshipit.org/pref1-podsecuritypolicy configured
armadachart.armada.airshipit.org/pref1-postgres-htk configured
armadachart.armada.airshipit.org/pref1-promenade-htk configured
armadachart.armada.airshipit.org/pref1-prometheus-alertmanager configured
armadachart.armada.airshipit.org/pref1-prometheus-kube-state-metrics configured
armadachart.armada.airshipit.org/pref1-prometheus-node-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus-openstack-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus-process-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus configured
armadachart.armada.airshipit.org/pref1-shipyard-htk configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-client-global configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-client configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-config configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-htk configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-ingress configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-mon configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-osd configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-rgw configured
armadachart.armada.airshipit.org/pref1-tiller-htk configured
armadachart.armada.airshipit.org/pref1-ucp-armada configured
armadachart.armada.airshipit.org/pref1-ucp-barbican-htk configured
armadachart.armada.airshipit.org/pref1-ucp-barbican configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-client-update-global configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-client configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-config configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-ingress configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-mon configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-osd configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-provisioners configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-rgw configured
armadachart.armada.airshipit.org/pref1-ucp-deckhand configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell-global configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell-htk configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell configured
armadachart.armada.airshipit.org/pref1-ucp-drydock configured
armadachart.armada.airshipit.org/pref1-ucp-ingress-htk configured
armadachart.armada.airshipit.org/pref1-ucp-ingress configured
armadachart.armada.airshipit.org/pref1-ucp-keystone-htk configured
armadachart.armada.airshipit.org/pref1-ucp-keystone-memcached configured
armadachart.armada.airshipit.org/pref1-ucp-keystone configured
armadachart.armada.airshipit.org/pref1-ucp-maas-global configured
armadachart.armada.airshipit.org/pref1-ucp-maas configured
armadachart.armada.airshipit.org/pref1-ucp-mariadb configured
armadachart.armada.airshipit.org/pref1-ucp-memcached-htk configured
armadachart.armada.airshipit.org/pref1-ucp-postgresql configured
armadachart.armada.airshipit.org/pref1-ucp-promenade-global configured
armadachart.armada.airshipit.org/pref1-ucp-promenade configured
armadachart.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter configured
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq-htk configured
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq configured
armadachart.armada.airshipit.org/pref1-ucp-shipyard configured
armadachart.armada.airshipit.org/pref1-ucp-tiller configured
armadachartgroup.armada.airshipit.org/pref1-ingress-kube-system configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-container-networking configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-core configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-dns configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-etcd configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-haproxy configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-proxy configured
armadachartgroup.armada.airshipit.org/pref1-openstack-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-openstack-cinder configured
armadachartgroup.armada.airshipit.org/pref1-openstack-compute-kit configured
armadachartgroup.armada.airshipit.org/pref1-openstack-glance configured
armadachartgroup.armada.airshipit.org/pref1-openstack-heat configured
armadachartgroup.armada.airshipit.org/pref1-openstack-horizon configured
armadachartgroup.armada.airshipit.org/pref1-openstack-ingress-controller configured
armadachartgroup.armada.airshipit.org/pref1-openstack-keystone configured
armadachartgroup.armada.airshipit.org/pref1-openstack-mariadb configured
armadachartgroup.armada.airshipit.org/pref1-openstack-memcached configured
armadachartgroup.armada.airshipit.org/pref1-openstack-radosgw configured
armadachartgroup.armada.airshipit.org/pref1-openstack-tenant-ceph configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-dashboards configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ingress-controller configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-logging configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-mariadb configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-monitoring configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-nfs-provisioner configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-prometheus-openstack-exporter configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-radosgw configured
armadachartgroup.armada.airshipit.org/pref1-podsecuritypolicy configured
armadachartgroup.armada.airshipit.org/pref1-ucp-armada configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-update configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph configured
armadachartgroup.armada.airshipit.org/pref1-ucp-core configured
armadachartgroup.armada.airshipit.org/pref1-ucp-deckhand configured
armadachartgroup.armada.airshipit.org/pref1-ucp-divingbell configured
armadachartgroup.armada.airshipit.org/pref1-ucp-drydock configured
armadachartgroup.armada.airshipit.org/pref1-ucp-keystone configured
armadachartgroup.armada.airshipit.org/pref1-ucp-promenade configured
armadachartgroup.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter configured
armadachartgroup.armada.airshipit.org/pref1-ucp-shipyard configured
armadamanifest.armada.airshipit.org/pref1-cluster-bootstrap configured
armadamanifest.armada.airshipit.org/pref1-full-site configured
deckhandcertificate.deckhand.airshipit.org/pref1-admin configured
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver-etcd configured
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver configured
deckhandcertificate.deckhand.airshipit.org/pref1-armada configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-anchor configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node configured
deckhandcertificate.deckhand.airshipit.org/pref1-controller-manager configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-genesis configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis configured
deckhandcertificate.deckhand.airshipit.org/pref1-scheduler configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd-peer configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd-peer configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd-peer configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd-peer configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-admin configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver-etcd configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-armada configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-anchor configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-controller-manager configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-genesis configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-scheduler configured
deckhandpassphrase.deckhand.airshipit.org/pref1-airsloop-crypt-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-fsid configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-swift-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ipmi-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-maas-region-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-stack-user-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-trustee-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-horizon-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-elasticsearch-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-session-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-nagios-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-openstack-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-prometheus-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-access-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-access-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-ldap-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-cache-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-placement-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-private-docker-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-tenant-ceph-fsid configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-armada-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-openstack-exporter-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-postgres-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-promenade-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-postgres-password configured
deckhandprivatekey.deckhand.airshipit.org/pref1-service-account configured
deckhandpublickey.deckhand.airshipit.org/pref1-airship-ssh-public-key configured
deckhandpublickey.deckhand.airshipit.org/pref1-airsloop-ssh-public-key configured
deckhandpublickey.deckhand.airshipit.org/pref1-service-account configured
drydockbaremetalnode.drydock.airshipit.org/pref1-airsloop-compute-1 configured
drydockbootaction.drydock.airshipit.org/pref1-airship-target configured
drydockbootaction.drydock.airshipit.org/pref1-apparmor-profiles configured
drydockbootaction.drydock.airshipit.org/pref1-promjoin-systemd-unit configured
drydockbootaction.drydock.airshipit.org/pref1-promjoin configured
drydockbootaction.drydock.airshipit.org/pref1-seccomp-profiles configured
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-hp-generic configured
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-r720xd configured
drydockhostprofile.drydock.airshipit.org/pref1-compute-r720xd configured
drydockhostprofile.drydock.airshipit.org/pref1-cp-global configured
drydockhostprofile.drydock.airshipit.org/pref1-dp-global configured
drydocknetwork.drydock.airshipit.org/pref1-calico configured
drydocknetwork.drydock.airshipit.org/pref1-oam configured
drydocknetwork.drydock.airshipit.org/pref1-oob configured
drydocknetwork.drydock.airshipit.org/pref1-overlay configured
drydocknetwork.drydock.airshipit.org/pref1-pxe configured
drydocknetwork.drydock.airshipit.org/pref1-storage configured
drydocknetworklink.drydock.airshipit.org/pref1-data configured
drydocknetworklink.drydock.airshipit.org/pref1-oob configured
drydocknetworklink.drydock.airshipit.org/pref1-pxe configured
drydockregion.drydock.airshipit.org/pref1-airsloop configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-infra-service-accounts configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-service-accounts configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-ucp-service-accounts configured
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-apparmor-loader configured
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-default configured
peglegcommonaddresses.pegleg.airshipit.org/pref1-common-addresses configured
peglegcommonsoftwareconfig.pegleg.airshipit.org/pref1-common-software-config configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-endpoints configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-infra-endpoints configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-ucp-endpoints configured
peglegscript.pegleg.airshipit.org/pref1-configure-ip-rules configured
peglegseccompprofile.pegleg.airshipit.org/pref1-seccomp-default configured
peglegsitedefinition.pegleg.airshipit.org/pref1-airsloop configured
peglegsoftwareversions.pegleg.airshipit.org/pref1-software-versions configured
promenadedocker.promenade.airshipit.org/pref1-docker-global configured
promenadegenesis.promenade.airshipit.org/pref1-genesis-global configured
promenadegenesis.promenade.airshipit.org/pref1-genesis-site configured
promenadehostsystem.promenade.airshipit.org/pref1-host-system created
promenadekubelet.promenade.airshipit.org/pref1-kubelet configured
promenadekubernetesnetwork.promenade.airshipit.org/pref1-kubernetes-network configured
promenadepkicatalog.promenade.airshipit.org/pref1-cluster-certificates configured
shipyarddeploymentconfiguration.shipyard.airshipit.org/pref1-deployment-configuration configured
shipyarddeploymentstrategy.shipyard.airshipit.org/pref1-deployment-strategy configured
```

### Verifying syntax of files with airship

This is still WIP

```bash
kubectl create namespace airship
```

```bash
kubectl apply -k airship/

armadachart.armada.airshipit.org/pref1-armada-htk configured
armadachart.armada.airshipit.org/pref1-calico-htk configured
armadachart.armada.airshipit.org/pref1-ceph-htk configured
armadachart.armada.airshipit.org/pref1-cinder-rabbitmq configured
armadachart.armada.airshipit.org/pref1-cinder configured
armadachart.armada.airshipit.org/pref1-coredns-htk configured
armadachart.armada.airshipit.org/pref1-coredns configured
armadachart.armada.airshipit.org/pref1-deckhand-htk configured
armadachart.armada.airshipit.org/pref1-drydock-htk configured
armadachart.armada.airshipit.org/pref1-elasticsearch configured
armadachart.armada.airshipit.org/pref1-fluent-logging configured
armadachart.armada.airshipit.org/pref1-glance-rabbitmq configured
armadachart.armada.airshipit.org/pref1-glance configured
armadachart.armada.airshipit.org/pref1-grafana configured
armadachart.armada.airshipit.org/pref1-haproxy-htk configured
armadachart.armada.airshipit.org/pref1-haproxy configured
armadachart.armada.airshipit.org/pref1-heat-rabbitmq configured
armadachart.armada.airshipit.org/pref1-heat configured
armadachart.armada.airshipit.org/pref1-horizon configured
armadachart.armada.airshipit.org/pref1-ingress-kube-system-htk configured
armadachart.armada.airshipit.org/pref1-ingress-kube-system configured
armadachart.armada.airshipit.org/pref1-keystone-rabbitmq configured
armadachart.armada.airshipit.org/pref1-keystone configured
armadachart.armada.airshipit.org/pref1-kibana configured
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-apiserver configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-global configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico-etcd configured
armadachart.armada.airshipit.org/pref1-kubernetes-calico configured
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-controller-manager configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-global configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-etcd configured
armadachart.armada.airshipit.org/pref1-kubernetes-proxy-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-proxy configured
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler-htk configured
armadachart.armada.airshipit.org/pref1-kubernetes-scheduler configured
armadachart.armada.airshipit.org/pref1-libvirt configured
armadachart.armada.airshipit.org/pref1-maas-htk configured
armadachart.armada.airshipit.org/pref1-mariadb-htk configured
armadachart.armada.airshipit.org/pref1-nagios configured
armadachart.armada.airshipit.org/pref1-neutron-rabbitmq configured
armadachart.armada.airshipit.org/pref1-neutron configured
armadachart.armada.airshipit.org/pref1-nfs-provisioner configured
armadachart.armada.airshipit.org/pref1-nova-rabbitmq configured
armadachart.armada.airshipit.org/pref1-nova configured
armadachart.armada.airshipit.org/pref1-openstack-ceph-config configured
armadachart.armada.airshipit.org/pref1-openstack-ingress-controller configured
armadachart.armada.airshipit.org/pref1-openstack-mariadb configured
armadachart.armada.airshipit.org/pref1-openstack-memcached configured
armadachart.armada.airshipit.org/pref1-openvswitch configured
armadachart.armada.airshipit.org/pref1-osh-helm-toolkit configured
armadachart.armada.airshipit.org/pref1-osh-infra-ceph-config configured
armadachart.armada.airshipit.org/pref1-osh-infra-helm-toolkit configured
armadachart.armada.airshipit.org/pref1-osh-infra-ingress-controller configured
armadachart.armada.airshipit.org/pref1-osh-infra-mariadb configured
armadachart.armada.airshipit.org/pref1-osh-infra-radosgw configured
armadachart.armada.airshipit.org/pref1-podsecuritypolicy configured
armadachart.armada.airshipit.org/pref1-postgres-htk configured
armadachart.armada.airshipit.org/pref1-promenade-htk configured
armadachart.armada.airshipit.org/pref1-prometheus-alertmanager configured
armadachart.armada.airshipit.org/pref1-prometheus-kube-state-metrics configured
armadachart.armada.airshipit.org/pref1-prometheus-node-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus-openstack-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus-process-exporter configured
armadachart.armada.airshipit.org/pref1-prometheus configured
armadachart.armada.airshipit.org/pref1-shipyard-htk configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-client-global configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-client configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-config configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-htk configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-ingress configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-mon configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-osd configured
armadachart.armada.airshipit.org/pref1-tenant-ceph-rgw configured
armadachart.armada.airshipit.org/pref1-tiller-htk configured
armadachart.armada.airshipit.org/pref1-ucp-armada configured
armadachart.armada.airshipit.org/pref1-ucp-barbican-htk configured
armadachart.armada.airshipit.org/pref1-ucp-barbican configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-client-update-global configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-client configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-config configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-ingress configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-mon configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-osd configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-provisioners configured
armadachart.armada.airshipit.org/pref1-ucp-ceph-rgw configured
armadachart.armada.airshipit.org/pref1-ucp-deckhand configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell-global configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell-htk configured
armadachart.armada.airshipit.org/pref1-ucp-divingbell configured
armadachart.armada.airshipit.org/pref1-ucp-drydock configured
armadachart.armada.airshipit.org/pref1-ucp-ingress-htk configured
armadachart.armada.airshipit.org/pref1-ucp-ingress configured
armadachart.armada.airshipit.org/pref1-ucp-keystone-htk configured
armadachart.armada.airshipit.org/pref1-ucp-keystone-memcached configured
armadachart.armada.airshipit.org/pref1-ucp-keystone configured
armadachart.armada.airshipit.org/pref1-ucp-maas-global configured
armadachart.armada.airshipit.org/pref1-ucp-maas configured
armadachart.armada.airshipit.org/pref1-ucp-mariadb configured
armadachart.armada.airshipit.org/pref1-ucp-memcached-htk configured
armadachart.armada.airshipit.org/pref1-ucp-postgresql configured
armadachart.armada.airshipit.org/pref1-ucp-promenade-global configured
armadachart.armada.airshipit.org/pref1-ucp-promenade configured
armadachart.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter configured
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq-htk configured
armadachart.armada.airshipit.org/pref1-ucp-rabbitmq configured
armadachart.armada.airshipit.org/pref1-ucp-shipyard configured
armadachart.armada.airshipit.org/pref1-ucp-tiller configured
armadachartgroup.armada.airshipit.org/pref1-ingress-kube-system configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-container-networking configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-core configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-dns configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-etcd configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-haproxy configured
armadachartgroup.armada.airshipit.org/pref1-kubernetes-proxy configured
armadachartgroup.armada.airshipit.org/pref1-openstack-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-openstack-cinder configured
armadachartgroup.armada.airshipit.org/pref1-openstack-compute-kit configured
armadachartgroup.armada.airshipit.org/pref1-openstack-glance configured
armadachartgroup.armada.airshipit.org/pref1-openstack-heat configured
armadachartgroup.armada.airshipit.org/pref1-openstack-horizon configured
armadachartgroup.armada.airshipit.org/pref1-openstack-ingress-controller configured
armadachartgroup.armada.airshipit.org/pref1-openstack-keystone configured
armadachartgroup.armada.airshipit.org/pref1-openstack-mariadb configured
armadachartgroup.armada.airshipit.org/pref1-openstack-memcached configured
armadachartgroup.armada.airshipit.org/pref1-openstack-radosgw configured
armadachartgroup.armada.airshipit.org/pref1-openstack-tenant-ceph configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-dashboards configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-ingress-controller configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-logging configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-mariadb configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-monitoring configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-nfs-provisioner configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-prometheus-openstack-exporter configured
armadachartgroup.armada.airshipit.org/pref1-osh-infra-radosgw configured
armadachartgroup.armada.airshipit.org/pref1-podsecuritypolicy configured
armadachartgroup.armada.airshipit.org/pref1-ucp-armada configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-config configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph-update configured
armadachartgroup.armada.airshipit.org/pref1-ucp-ceph configured
armadachartgroup.armada.airshipit.org/pref1-ucp-core configured
armadachartgroup.armada.airshipit.org/pref1-ucp-deckhand configured
armadachartgroup.armada.airshipit.org/pref1-ucp-divingbell configured
armadachartgroup.armada.airshipit.org/pref1-ucp-drydock configured
armadachartgroup.armada.airshipit.org/pref1-ucp-keystone configured
armadachartgroup.armada.airshipit.org/pref1-ucp-promenade configured
armadachartgroup.armada.airshipit.org/pref1-ucp-prometheus-openstack-exporter configured
armadachartgroup.armada.airshipit.org/pref1-ucp-shipyard configured
armadamanifest.armada.airshipit.org/pref1-cluster-bootstrap configured
armadamanifest.armada.airshipit.org/pref1-full-site configured
deckhandcertificate.deckhand.airshipit.org/pref1-admin configured
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver-etcd configured
deckhandcertificate.deckhand.airshipit.org/pref1-apiserver configured
deckhandcertificate.deckhand.airshipit.org/pref1-armada configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-etcd-anchor configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-calico-node configured
deckhandcertificate.deckhand.airshipit.org/pref1-controller-manager configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubelet-genesis configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer configured
deckhandcertificate.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis configured
deckhandcertificate.deckhand.airshipit.org/pref1-scheduler configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd-peer configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-calico-etcd configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd-peer configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes-etcd configured
deckhandcertificateauthority.deckhand.airshipit.org/pref1-kubernetes configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd-peer configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-calico-etcd configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd-peer configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes-etcd configured
deckhandcertificateauthoritykey.deckhand.airshipit.org/pref1-kubernetes configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-admin configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver-etcd configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-apiserver configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-armada configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-etcd-anchor configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-calico-node configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-controller-manager configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-compute-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubelet-genesis configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-1 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-2 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-airsloop-control-3 configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-anchor configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis-peer configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-kubernetes-etcd-genesis configured
deckhandcertificatekey.deckhand.airshipit.org/pref1-scheduler configured
deckhandpassphrase.deckhand.airshipit.org/pref1-airsloop-crypt-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-fsid configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ceph-swift-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ipmi-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-maas-region-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-barbican-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-cinder-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-glance-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-stack-user-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-heat-trustee-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-horizon-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-elasticsearch-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-grafana-oslo-db-session-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-nagios-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-openstack-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-oslo-db-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-prometheus-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-access-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-admin-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-access-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-infra-rgw-s3-elasticsearch-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-ldap-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-keystone-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-neutron-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-nova-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-cache-secret-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-oslo-db-exporter-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-osh-placement-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-private-docker-key configured
deckhandpassphrase.deckhand.airshipit.org/pref1-tenant-ceph-fsid configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-airflow-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-armada-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-barbican-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-deckhand-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-drydock-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-keystone-oslo-db-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-maas-postgres-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-openstack-exporter-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-db-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-oslo-messaging-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-postgres-admin-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-promenade-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-rabbitmq-erlang-cookie configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-keystone-password configured
deckhandpassphrase.deckhand.airshipit.org/pref1-ucp-shipyard-postgres-password configured
deckhandprivatekey.deckhand.airshipit.org/pref1-service-account configured
deckhandpublickey.deckhand.airshipit.org/pref1-airship-ssh-public-key configured
deckhandpublickey.deckhand.airshipit.org/pref1-airsloop-ssh-public-key configured
deckhandpublickey.deckhand.airshipit.org/pref1-service-account configured
drydockbaremetalnode.drydock.airshipit.org/pref1-airsloop-compute-1 configured
drydockbootaction.drydock.airshipit.org/pref1-airship-target configured
drydockbootaction.drydock.airshipit.org/pref1-apparmor-profiles configured
drydockbootaction.drydock.airshipit.org/pref1-promjoin-systemd-unit configured
drydockbootaction.drydock.airshipit.org/pref1-promjoin configured
drydockbootaction.drydock.airshipit.org/pref1-seccomp-profiles configured
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-hp-generic configured
drydockhardwareprofile.drydock.airshipit.org/pref1-dell-r720xd configured
drydockhostprofile.drydock.airshipit.org/pref1-compute-r720xd configured
drydockhostprofile.drydock.airshipit.org/pref1-cp-global configured
drydockhostprofile.drydock.airshipit.org/pref1-dp-global configured
drydocknetwork.drydock.airshipit.org/pref1-calico configured
drydocknetwork.drydock.airshipit.org/pref1-oam configured
drydocknetwork.drydock.airshipit.org/pref1-oob configured
drydocknetwork.drydock.airshipit.org/pref1-overlay configured
drydocknetwork.drydock.airshipit.org/pref1-pxe configured
drydocknetwork.drydock.airshipit.org/pref1-storage configured
drydocknetworklink.drydock.airshipit.org/pref1-data configured
drydocknetworklink.drydock.airshipit.org/pref1-oob configured
drydocknetworklink.drydock.airshipit.org/pref1-pxe configured
drydockregion.drydock.airshipit.org/pref1-airsloop configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-infra-service-accounts configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-osh-service-accounts configured
peglegaccountcatalogue.pegleg.airshipit.org/pref1-ucp-service-accounts configured
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-apparmor-loader configured
peglegapparmorprofile.pegleg.airshipit.org/pref1-airship-default configured
peglegcommonaddresses.pegleg.airshipit.org/pref1-common-addresses configured
peglegcommonsoftwareconfig.pegleg.airshipit.org/pref1-common-software-config configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-endpoints configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-osh-infra-endpoints configured
peglegendpointcatalogue.pegleg.airshipit.org/pref1-ucp-endpoints configured
peglegscript.pegleg.airshipit.org/pref1-configure-ip-rules configured
peglegseccompprofile.pegleg.airshipit.org/pref1-seccomp-default configured
peglegsitedefinition.pegleg.airshipit.org/pref1-airsloop configured
peglegsoftwareversions.pegleg.airshipit.org/pref1-software-versions configured
promenadedocker.promenade.airshipit.org/pref1-docker-global configured
promenadegenesis.promenade.airshipit.org/pref1-genesis-global configured
promenadegenesis.promenade.airshipit.org/pref1-genesis-site configured
promenadehostsystem.promenade.airshipit.org/pref1-host-system created
promenadekubelet.promenade.airshipit.org/pref1-kubelet configured
promenadekubernetesnetwork.promenade.airshipit.org/pref1-kubernetes-network configured
promenadepkicatalog.promenade.airshipit.org/pref1-cluster-certificates configured
shipyarddeploymentconfiguration.shipyard.airshipit.org/pref1-deployment-configuration configured
shipyarddeploymentstrategy.shipyard.airshipit.org/pref1-deployment-strategy configured
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
drydockregion.drydock.airshipit.org/pref2-pref1-airsloop created
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
promenadegenesis.promenade.airshipit.org/pref2-pref1-genesis-global created
promenadegenesis.promenade.airshipit.org/pref2-pref1-genesis-site created
promenadehostsystem.promenade.airshipit.org/pref2-pref1-host-system created
promenadekubelet.promenade.airshipit.org/pref2-pref1-kubelet created
promenadekubernetesnetwork.promenade.airshipit.org/pref2-pref1-kubernetes-network created
promenadepkicatalog.promenade.airshipit.org/pref2-pref1-cluster-certificates created
shipyarddeploymentconfiguration.shipyard.airshipit.org/pref2-pref1-deployment-configuration created
shipyarddeploymentstrategy.shipyard.airshipit.org/pref2-pref1-deployment-strategy created
```

To cleanup

```bash
kubectl delete -k overlays/airsloop
```
