# This is a quickfix to enable an upstream image to function on OpenShift
# see https://docs.openshift.com/container-platform/3.11/creating_images/guidelines.html
#
# This image is a modified version of
# https://github.com/puckel/docker-airflow/blob/1.10.9/Dockerfile
#
# TODO: build a real image properly, instead of pushing this nasty hack directly to the registry
# see https://registry-console-default.pathfinder.gov.bc.ca/registry#/images/wksv3k-tools/cas-airflow

FROM python:3.7-slim-buster
LABEL maintainer="wenzowski"
LABEL io.openshift.s2i.assemble-user="1000880000"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.10
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS="gcp,kubernetes"
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

USER root
RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        python-lxml \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && groupadd -g 1000880000 airflow \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} -l -u 1000880000 -g 1000880000 airflow \
    && usermod -a -G root airflow \
    && test "$(id airflow)" = "uid=1000880000(airflow) gid=1000880000(airflow) groups=1000880000(airflow),0(root)" \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install lxml \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install 'redis==3.2' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY root/entrypoint.sh /entrypoint.sh
COPY root/usr/local/airflow/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
COPY root/usr/libexec/fix-permissions /usr/libexec/fix-permissions
RUN chmod g=u /etc/passwd && \
    /usr/libexec/fix-permissions ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER 1000880000
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
