# adblocker

## Microk8s enabled addons 

dashboard, dns, ingress, metallb , storage, registry, helm3

## Install selenium grid

helm install --kubeconfig ../kube.config selenium ./seleniumGrid --namespace selenium --create-namespace

## Upgrade selenium grid

helm upgrade --kubeconfig ../kube.config selenium ./seleniumGrid --namespace selenium

## Install Php My Admin and mariadb

https://bitnami.com/stack/phpmyadmin/helm

helm repo add bitnami https://charts.bitnami.com/bitnami

helm install --kubeconfig ../kube.config mysql bitnami/phpmyadmin --namespace mysql --create-namespace --set db.bundleTestDB=true --set service.loadBalancerIP=192.168.69.231 --set service.type=LoadBalancer

or the not working one yet :

helm install --kubeconfig ../kube.config mysql bitnami/phpmyadmin --namespace mysql --create-namespace --set db.bundleTestDB=true --set ingress.enabled=true --set ingress.path=/phpmyadmin

## Upgrade Php My Admin and mariadb

helm upgrade --kubeconfig ../kube.config mysql bitnami/phpmyadmin --namespace mysql --set db.bundleTestDB=true --set service.loadBalancerIP=192.168.69.231 --set service.type=LoadBalancer

## Remove Php My Admin and mariadb

helm delete --kubeconfig ../kube.config mysql --namespace mysql

## Deploy Scrapper helm 

helm install --kubeconfig ../kube.config scrapper ./scrapper --namespace scrapper --create-namespace

## Install kafka follow 

https://github.com/confluentinc/cp-helm-charts#installation

helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update
helm install --kubeconfig ../kube.config confluentinc/cp-helm-charts --name my-confluent --version 0.6.0  --namespace scrapper
