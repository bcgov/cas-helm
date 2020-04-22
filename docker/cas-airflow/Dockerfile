# This is a quickfix to enable an upstream image to function on OpenShift
# see https://docs.openshift.com/container-platform/3.11/creating_images/guidelines.html
#
# TODO: build a real image properly, instead of pushing this nasty hack directly to the registry
# see https://registry-console-default.pathfinder.gov.bc.ca/registry#/images/wksv3k-tools/cas-airflow

FROM puckel/docker-airflow:1.10.9
# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
LABEL io.openshift.s2i.assemble-user="1000880000"
USER root
RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install python-lxml -yqq \
    && pip install lxml \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh,gcp,kubernetes]==1.10.10
COPY root/entrypoint.sh /entrypoint.sh
RUN userdel airflow && \
    groupadd -g 1000880000 airflow && \
    useradd -l -u 1000880000 -g 1000880000 -d /usr/local/airflow airflow && \
    usermod -a -G root airflow && \
    test "$(id airflow)" = "uid=1000880000(airflow) gid=1000880000(airflow) groups=1000880000(airflow),0(root)"
COPY root/usr/local/airflow/airflow.cfg /usr/local/airflow/airflow.cfg
COPY root/usr/libexec/fix-permissions /usr/libexec/fix-permissions
RUN chmod g=u /etc/passwd && \
    /usr/libexec/fix-permissions /usr/local/airflow
USER 1000880000
ENTRYPOINT ["/entrypoint.sh"]

