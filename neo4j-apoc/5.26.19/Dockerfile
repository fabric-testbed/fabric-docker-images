# Dockerfile for Neo4j with APOC plugin
FROM neo4j:5.26.19-community
LABEL maintainer="komal.thareja@gmail.com"

# We leverage the original image as much as we can.
# details of the base image are here:
# https://github.com/neo4j/docker-neo4j-publish (5.26.19/community)

# Neo4j community docker comes with APOC already downloaded, just need GDS
ENV GDS_VERSION=2.13.7

RUN apt-get update; apt-get install -y unzip

# Create a graph import directory
RUN mkdir /imports \
  && chmod -R 777 /imports

# do everything as user neo4j below
USER neo4j

# auto-enable these plugins
ENV NEO4J_PLUGINS='["apoc", "graph-data-science"]'
ENV NEO4J_server_directories_import="/imports"

# update config files
#RUN sed -i 's/server.directories.import=import/server.directories.import=\/imports/' /var/lib/neo4j/conf/neo4j.conf

# we generally want the following settings, but they appear to be in effect already:
# dbms.security.procedures.unrestricted=apoc.*,gds.*
# dbms.security.procedures.whitelist=apoc.*,gds.*

# need to set apoc.import.file.enabled=true in a separate conf file
COPY apoc.conf /var/lib/neo4j/conf/apoc.conf

# Fetch the GDS Plugin into expected location
RUN wget --directory-prefix=/var/lib/neo4j/products \
  https://graphdatascience.ninja/neo4j-graph-data-science-${GDS_VERSION}.jar

VOLUME /imports
EXPOSE 7474 7473 7687

# we are reusing the entrypoint of the original docker
ENTRYPOINT ["tini", "-g", "--", "/startup/docker-entrypoint.sh"]
CMD ["neo4j"]
