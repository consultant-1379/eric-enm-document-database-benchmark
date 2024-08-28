ARG BASE_IMAGE_REPO=armdocker.rnd.ericsson.se/proj_oss_releases/enm
ARG BASE_IMAGE_TAG=base

FROM $BASE_IMAGE_REPO/eric-enm-document-database-benchmark-base-image:$BASE_IMAGE_TAG

ARG BUILD_DATE
ARG REVISION
ARG IMAGE_VERSION

LABEL com.ericsson.product-number="CXC 174 1531" \
      org.opencontainers.image.title="Document Database Benchmark Init Wait" \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.revision=${REVISION} \
      org.opencontainers.image.vendor="Ericsson" \
      org.opencontainers.image.version=${IMAGE_VERSION}

RUN zypper --non-interactive in curl && \
    zypper clean -a

COPY wait_for_agent.sh wait_for_orchestrator.sh /
RUN chmod +x wait_for_agent.sh wait_for_orchestrator.sh

USER 1000