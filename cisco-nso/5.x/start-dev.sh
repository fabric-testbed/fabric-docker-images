#!/bin/bash

VERSION=5.5
RUNDIR=/opt/nso-dev
LOGDIR=/opt/nso-dev-logs

[[ ! -f "${RUNDIR}" ]] && sudo mkdir -p "${RUNDIR}"
[[ ! -f "${LOGDIR}" ]] && sudo mkdir -p "${LOGDIR}"

docker run -tid --name nso-dev \
	--restart unless-stopped \
	-e SSH_PORT=2222 \
	-e ADMIN_USERNAME=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTPS_ENABLE=true \
        -v ${RUNDIR}:/nso \
        -v ${LOGDIR}:/log \
	cisco-nso-dev:${VERSION} /run-nso.sh
