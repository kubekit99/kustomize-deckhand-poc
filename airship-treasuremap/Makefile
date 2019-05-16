
install:
	kubectl label nodes airship openstack-control-plane=enabled --overwrite
	kubectl label nodes airship ucp-control-plane=enabled --overwrite
	kubectl label nodes airship ceph-mds=enabled --overwrite
	kubectl label nodes airship ceph-mgr=enabled --overwrite
	kubectl label nodes airship ceph-mon=enabled --overwrite
	kubectl label nodes airship ceph-rgw=enabled --overwrite
	kubectl apply -f ./deploy/namespaces
	kubectl apply -f ./deploy/crds/
	kubectl apply -n ceph -f ./deploy/operator
	kubectl apply -n nfs -f ./deploy/operator
	kubectl apply -n openstack -f ./deploy/operator
	kubectl apply -n osh-infra -f ./deploy/operator
	kubectl apply -n tenant-ceph -f ./deploy/operator
	kubectl apply -n ucp -f ./deploy/operator
	kubectl apply -f ./deploy/cluster/cluster_role.yaml
	kubectl apply -f ./deploy/cluster/cluster_role_binding.yaml

purge:
	kubectl delete -n ceph -f ./deploy/operator --ignore-not-found=true
	kubectl delete -n nfs -f ./deploy/operator --ignore-not-found=true
	kubectl delete -n openstack -f ./deploy/operator --ignore-not-found=true
	kubectl delete -n osh-infra -f ./deploy/operator --ignore-not-found=true
	kubectl delete -n tenant-ceph -f ./deploy/operator --ignore-not-found=true
	kubectl delete -n ucp -f ./deploy/operator --ignore-not-found=true
	kubectl delete -f ./deploy/cluster/cluster_role_binding.yaml --ignore-not-found=true
	kubectl delete -f ./deploy/cluster/cluster_role.yaml --ignore-not-found=true
	kubectl delete -f ./deploy/namespaces --ignore-not-found=true
	kubectl delete -f ./deploy/crds/ --ignore-not-found=true

