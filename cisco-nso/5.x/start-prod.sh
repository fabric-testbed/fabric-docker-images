#!/bin/bash

VERSION=5.5
RUNDIR=/opt/nso
LOGDIR=/opt/nso-logs

[[ ! -f "${RUNDIR}" ]] && sudo mkdir -p "${RUNDIR}/packages"
[[ ! -f "${LOGDIR}" ]] && sudo mkdir -p "${LOGDIR}"

docker run -d --name nso-prod \
	--net host \
	-e SSH_PORT=2222 \
	-e ADMIN_USERNAM=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTP_ENABLE=false \
	-e HTTPS_ENABLE=true \
	-v ${RUNDIR}:/nso \
	-v ${LOGDIR}:/log \
	-v ${RUNDIR}/packages:/var/opt/ncs/packages \
	cisco-nso-base:${VERSION} /run-nso.sh
