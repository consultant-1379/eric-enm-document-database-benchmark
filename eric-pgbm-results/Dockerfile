ARG BASE_IMAGE_REPO=armdocker.rnd.ericsson.se/proj_oss_releases/enm
ARG BASE_IMAGE_TAG=base

FROM $BASE_IMAGE_REPO/eric-enm-document-database-benchmark-base-image:$BASE_IMAGE_TAG

ARG BUILD_DATE
ARG REVISION
ARG IMAGE_VERSION

LABEL com.ericsson.product-number="CXC 174 1531" \
      org.opencontainers.image.title="Document Database Benchmark Orchestrator" \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.revision=${REVISION} \
      org.opencontainers.image.vendor="Ericsson" \
      org.opencontainers.image.version=${IMAGE_VERSION}

COPY requirements.txt /tmp/

ARG CNIV_PYPI_HOST=arm.seli.gic.ericsson.se
ARG CNIV_PYPI_REPO=$CNIV_PYPI_HOST/artifactory/proj-eric-enm-document-database-benchmark-pypi-local/

RUN zypper --non-interactive in python311 python311-pip && \
    pip install -I --no-cache-dir --trusted-host $CNIV_PYPI_HOST \
        --index-url https://${CNIV_PYPI_REPO} \
        -r /tmp/requirements.txt && \
    zypper clean -a

COPY src/main/python/pgbm ./python/pgbm
COPY src/main/python/scripts/result_service.py ./python/scripts/result_service.py
USER 1000