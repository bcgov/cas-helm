# This is a quickfix to enable an upstream image to function on OpenShift
# see https://docs.openshift.com/container-platform/3.11/creating_images/guidelines.html
#
# TODO: build a real image properly, instead of pushing this nasty hack directly to the registry
# see https://registry-console-default.pathfinder.gov.bc.ca/registry#/images/wksv3k-tools/cas-airflow

FROM puckel/docker-airflow:1.10.4
# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

LABEL io.openshift.s2i.assemble-user="1000"
USER root
RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install python-lxml -yqq \
    && pip install lxml

COPY root/usr/local/airflow/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
COPY root/usr/local/airflow/config/__init__.py ${AIRFLOW_USER_HOME}/__init__.py
COPY root/usr/local/airflow/config ${AIRFLOW_USER_HOME}/config
COPY root/entrypoint.sh /entrypoint.sh
COPY root/usr/libexec/fix-permissions /usr/libexec/fix-permissions
RUN test "$(id airflow)" = "uid=1000(airflow) gid=1000(airflow) groups=1000(airflow)" && \
    chmod g=u /etc/passwd && \
    usermod -a -G root airflow && \
    /usr/libexec/fix-permissions /usr/local/airflow
USER 1000

