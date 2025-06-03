helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/

helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml

kubectl apply -f k8s-dashboard/dashboard-adminuser.yaml --namespace kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml

kubectl apply -f k8s-dashboard/clusterrolebinding.yaml --namespace kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml

kubectl apply -f k8s-dashboard/secret.yaml -n kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml

kubectl apply -f k8s-dashboard/k8s-dashboard-svc.yml -n kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml

kubectl get secret admin-user -n kubernetes-dashboard --kubeconfig k3s-with-docker-compose/output/kubeconfig.yaml -o jsonpath="{.data.token}" | base64 --decode
