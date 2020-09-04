#!/bin/bash

docker run -d --name nso-prod \
	--net host \
	-e SSH_PORT=2222 \
	-e ADMIN_USERNAM=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTPS_ENABLE=true \
	-v /opt/nso:/nso \
	-v /opt/nso-logs:/log \
	-v /opt/nso/packages:/var/opt/ncs/packages \
	cisco-nso-base:5.3-root /run-nso.sh
