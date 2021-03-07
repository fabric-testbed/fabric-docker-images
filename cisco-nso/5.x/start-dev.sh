#!/bin/bash

docker run -tid --name nso-dev \
	--net host \
	-e SSH_PORT=2222 \
	-e ADMIN_USERNAME=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTPS_ENABLE=true \
        -v /opt/nso-dev:/nso \
        -v /opt/nso-dev-logs:/log \
	cisco-nso-dev:5.3-root /run-nso.sh
