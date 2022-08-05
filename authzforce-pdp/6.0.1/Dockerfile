FROM openjdk:11
LABEL maintainer="Ilya Baldin"
LABEL org.label-schema.name="AuthzForce RESTful PDP together with CLI tool and externalizable configuration (/conf) and policy location (/policies)"
# LABEL org.label-schema.description=""

# Based on docker definition from https://github.com/authzforce/restful-pdp/blob/develop/docker/pdp/Dockerfile
# adds the CLI jar to simplify testing

# entry point will copy files from inside docker into host filesystem on first start
# so they can be customized. Policies are assumed to live in /policies
VOLUME ["/conf", "/policies"]

ARG PDP_JAR_VERSION="6.0.1"
ENV PDP_VERSION ${PDP_JAR_VERSION}
ENV PDP_JAR_URL="https://repo1.maven.org/maven2/org/ow2/authzforce/authzforce-ce-restful-pdp-cxf-spring-boot-server/${PDP_JAR_VERSION}/authzforce-ce-restful-pdp-cxf-spring-boot-server-${PDP_JAR_VERSION}.jar"

ARG CLI_JAR_VERSION="20.1.0"
ENV CLI_VERSION ${CLI_JAR_VERSION}
ENV CLI_JAR_URL="https://repo1.maven.org/maven2/org/ow2/authzforce/authzforce-ce-core-pdp-cli/${CLI_JAR_VERSION}/authzforce-ce-core-pdp-cli-${CLI_JAR_VERSION}.jar"

RUN mkdir -p /opt/authzforce/conf
RUN mkdir -p /opt/authzforce/policies
RUN mkdir -p /opt/authzforce/bin

COPY conf/application.yml conf/catalog.xml conf/logback.xml conf/pdp-ext.xsd conf/pdp.xml conf/spring-beans.xml /opt/authzforce/conf/
COPY policies/ExampleProjRequest.xml policies/ExampleProjPolicy.xml /opt/authzforce/policies/

RUN curl --verbose --location $PDP_JAR_URL --output /opt/authzforce/bin/pdp-${PDP_JAR_VERSION}-app.jar &&\
    curl --verbose --location $CLI_JAR_URL --output /opt/authzforce/bin/cli-${CLI_JAR_VERSION}-app.jar &&\
    adduser spring

RUN chmod ugo+rx /opt/authzforce/bin/cli-${CLI_JAR_VERSION}-app.jar

COPY docker-entrypoint.sh /

USER spring:spring

EXPOSE 8080 8443

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]
#ENTRYPOINT ["/usr/bin/tail", "-f", "/dev/null"]
