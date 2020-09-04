#!/bin/bash

docker run -d --name nso-prod \
	--net host \
	-e ADMIN_USERNAM=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTPS_ENABLE=true \
	-v /opt/nso:/nso \
	-v /opt/nso-logs:/log \
	cisco-nso-base:5.3-root /run-nso.sh
