cas-helm
========

This repo is a quick spike to evaluate use of [`helm`](https://helm.sh/) by the Climate Action Secretariat.

All code is derived from [stable charts](https://hub.helm.sh/charts/stable) from the Helm Hub. 


Prerequisites
-------------

Get `helm` via [your favorite package manager](https://github.com/helm/helm#install) before proceeding.


Usage
-----

Try deploying Apache Airflow.

There's no recursive dependency management in helm yet, so deps have to be installed in order:

```bash
helm dep up postgresql
helm dep up airflow
helm dep up cas-airflow
helm install --namespace "wksv3k-tools" cas-airflow cas-airflow
helm upgrade --atomic --timeout 600s --namespace "wksv3k-tools" cas-airflow cas-airflow
helm delete cas-airflow
```
