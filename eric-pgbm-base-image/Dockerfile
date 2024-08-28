ARG OS_BASE_IMAGE_NAME=sles
ARG OS_BASE_IMAGE_REPO=armdocker.rnd.ericsson.se/proj-ldc/common_base_os_release
ARG OS_BASE_IMAGE_TAG=6.16.0-13

FROM $OS_BASE_IMAGE_REPO/$OS_BASE_IMAGE_NAME:$OS_BASE_IMAGE_TAG

ARG BUILD_DATE
ARG REVISION
ARG IMAGE_VERSION
ARG OS_BASE_IMAGE_TAG
ENV PYTHONPATH=/python/

LABEL com.ericsson.product-number="CXC 174 1531" \
      org.opencontainers.image.title="Document Database Benchmark Base Image" \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.revision=${REVISION} \
      org.opencontainers.image.vendor="Ericsson" \
      org.opencontainers.image.version=${IMAGE_VERSION}

RUN zypper ar -C -G -f https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-ldc-repo-rpm-local/common_base_os/sles/$OS_BASE_IMAGE_TAG?ssl_verify=no LDC-SLES15 && \
    zypper --non-interactive ref -f -r LDC-SLES15 && \
    zypper clean -a