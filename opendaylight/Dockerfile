FROM openjdk:11
MAINTAINER Ezra Kissel <kissel@es.net>

EXPOSE 8181 8101

RUN mkdir /odl
WORKDIR /odl

RUN wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/0.12.0/opendaylight-0.12.0.tar.gz && \
    tar -xf opendaylight-0.12.0.tar.gz

RUN sed -ie "s/^featuresBoot.*/featuresBoot=config,standard,region,package,kar,management,odl-netconf-connector-all,odl-netconf-topology,odl-restconf-all,odl-bgpcep-bgp,odl-bgpcep-pcep,odl-bgpcep-bmp,odl-bgpcep-bgp-config-example,odl-mdsal-apidocs/g" ./opendaylight-0.12.0/etc/org.apache.karaf.features.cfg

CMD ./opendaylight-0.12.0/bin/karaf
