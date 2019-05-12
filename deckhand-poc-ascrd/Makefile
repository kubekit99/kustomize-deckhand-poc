
install:
	kubectl apply -f ./base/namespaces
	kubectl apply -f ./base/crds/
	kubectl apply -n ceph -f ./base/operator
	kubectl apply -n nfs -f ./base/operator
	kubectl apply -n openstack -f ./base/operator
	kubectl apply -n osh-infra -f ./base/operator
	kubectl apply -n tenant-ceph -f ./base/operator
	kubectl apply -n ucp -f ./base/operator
	kubectl apply -f ./base/cluster/cluster_role.yaml
	kubectl apply -f ./base/cluster/cluster_role_binding.yaml

purge:
	kubectl delete -n ceph -f ./base/operator --ignore-not-found=true
	kubectl delete -n nfs -f ./base/operator --ignore-not-found=true
	kubectl delete -n openstack -f ./base/operator --ignore-not-found=true
	kubectl delete -n osh-infra -f ./base/operator --ignore-not-found=true
	kubectl delete -n tenant-ceph -f ./base/operator --ignore-not-found=true
	kubectl delete -n ucp -f ./base/operator --ignore-not-found=true
	kubectl delete -f ./base/cluster/cluster_role_binding.yaml --ignore-not-found=true
	kubectl delete -f ./base/cluster/cluster_role.yaml --ignore-not-found=true
	kubectl delete -f ./base/namespaces --ignore-not-found=true
	kubectl delete -f ./base/crds/ --ignore-not-found=true

