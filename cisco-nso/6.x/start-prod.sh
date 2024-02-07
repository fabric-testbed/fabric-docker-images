#!/bin/bash

VERSION=6.2.1
RUNDIR=/opt/nso
LOGDIR=/opt/nso-logs

[[ ! -f "${RUNDIR}" ]] && sudo mkdir -p "${RUNDIR}/packages"
[[ ! -f "${LOGDIR}" ]] && sudo mkdir -p "${LOGDIR}"

docker run -d --name nso-prod \
        --restart unless-stopped \
	--net host \
	-e SSH_PORT=2222 \
	-e ADMIN_USERNAM=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTP_ENABLE=false \
	-e HTTPS_ENABLE=true \
	-v ${RUNDIR}:/nso \
	-v ${LOGDIR}:/log \
	-v ${RUNDIR}/packages:/var/opt/ncs/packages \
	-v /etc/nso/ncs.conf:/etc/ncs/ncs.conf \
        -v /etc/nso/netam-dev_fabric-testbed_net_cert.cer:/nso/ssl/cert/host.cert \
        -v /etc/nso/netam-dev_fabric-testbed_net.key:/nso/ssl/cert/host.key \
	-v /etc/nso/netam-dev_fabric-testbed_net.pem:/nso/ssl/cert/CAcert.pem \
	cisco-nso-base:${VERSION} /run-nso.sh
