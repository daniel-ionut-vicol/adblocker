# adblocker

## Install selenium grid

helm install --kubeconfig ../kube.config selenium ./ seleniumGrid --namespace selenium --create-namespace

## Upgrade selenium grid

helm upgrade --kubeconfig ../kube.config selenium ./ seleniumGrid --namespace selenium

## Install MySql

https://bitnami.com/stack/mysql/helm



helm repo add bitnami https://charts.bitnami.com/bitnami
helm install --kubeconfig ../kube.config mysql bitnami/mysql --namespace mysql --create-namespace

## Upgrade MySql

helm upgrade mysql bitnami/mysql --namespace mysql


