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

Kubernetes Executor
-------------

The `Kubernetes Executor` runs individual sandboxed pods for each Airflow task & requires some extra setup.

- In the dockerfile we have run `pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh,gcp,kubernetes]==1.10.10`which covers the necessary dependencies.
- Because the worker pod created by the `Kubernetes Executor` is sandboxed, it requires the explicit passing of variables to the pod via `KUBERNETES_ENVIRONMENT_VARIABLES`. https://github.com/apache/airflow/blob/master/airflow/config_templates/default_airflow.cfg#L1072
  - For example under `config` in values.yaml:
    - We have set `AIRFLOW__CORE__REMOTE_LOGGING`: `True`
    - This must also be set on the kubernetes worker pod by adding the same variable to the kubernetes env vars like so: `AIRFLOW__KUBERNETES_ENVIRONMENT_VARIABLES__AIRFLOW__CORE__REMOTE_LOGGING`: `True`
    - Setting the fernet key has to be done inside of `extraEnv` rather than `config`.

Kubernetes - GCS logging
-----
- In order for the worker pod to write to GCS logs (or other external storage) environment variables must be set on the worker as above.
- A connection in airflow must also be created.
- Because the worker is sandboxed it cannot read external volumes. We originally had secrets for the gcp connection bound to a volume outside of the worker, but the worker could not read that volume. So the secrets for writing external logs were moved into the logs volume that the worker does have the ability to read.
