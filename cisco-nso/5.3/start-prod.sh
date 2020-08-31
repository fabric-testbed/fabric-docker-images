#!/bin/bash

docker run -d --name nso-prod \
	-p 80:80 \
	-p 443:443 \
	-p 2222:22 \
	-p 4569:4569 \
	-p 4334:4334 \
	-p 830:830 \
	-e ADMIN_USERNAM=admin \
	-e ADMIN_PASSWORD=<passwd> \
	-e HTTPS_ENABLE=true \
	-v /opt/nso:/nso \
	-v /opt/nso-logs:/log \
	-v /opt/ncs:/src \
	cisco-nso-prod:5.3-root
