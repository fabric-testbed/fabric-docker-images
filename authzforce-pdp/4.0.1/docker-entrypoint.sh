#!/usr/bin/env bash
set -e

### populate contents of /conf (putting it into host filesystem if external mount is used)
_pdp_conf_copy() {
  cd /opt/authzforce/conf
  cp *.xml *.xsd *.yml /conf
  cd -
}

_pdp_policy_copy() {
  cd /opt/authzforce/policies
  cp *.xml /policies
  cd -
}
### main ###

_pdp_policy_copy

# external volume mounts will be empty on initial run, but don't overwrite an existing config
if [[ ! -f /conf/application.yml ]]; then
  _pdp_conf_copy
fi

#exec "${@}"


JAVA_OPTS="-Dloader.path=/extensions -Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Djavax.xml.accessExternalSchema=all -Xms1024m -Xmx2048m -XX:+UseConcMarkSweepGC -server"
java ${JAVA_OPTS} -jar /opt/authzforce/bin/pdp-${PDP_VERSION}-app.jar --spring.config.location=classpath:/,file:/conf/application.yml

# in case it crashes
tail -f /dev/null
