ARG BASE_IMAGE_REPO=armdocker.rnd.ericsson.se/proj_oss_releases/enm
ARG BASE_IMAGE_TAG=base-5.0

FROM $BASE_IMAGE_REPO/eric-enm-document-database-benchmark-base-image:$BASE_IMAGE_TAG

RUN zypper --non-interactive in python3 python3-pip && \
    pip3 install pylint pycodestyle pytest-cov pyyaml && \
    pip3 install requests && \
    zypper install -y python3-prometheus_client && \
    zypper clean -a