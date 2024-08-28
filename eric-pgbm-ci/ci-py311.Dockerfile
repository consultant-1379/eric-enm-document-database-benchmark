ARG BASE_IMAGE_REPO=armdocker.rnd.ericsson.se/proj_oss_releases/enm
ARG BASE_IMAGE_TAG=base-5.0

FROM $BASE_IMAGE_REPO/eric-enm-document-database-benchmark-base-image:$BASE_IMAGE_TAG

RUN zypper --non-interactive in python311 python311-pip curl && \
    pip3 install pylint pycodestyle pytest-cov  && \
    pip3 install requests pyyaml flask waitress && \
    zypper clean -a