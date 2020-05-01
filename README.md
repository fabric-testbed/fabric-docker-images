# Docker tooling for FABRIC

Docker images or related Compose definitions for use with the FABRIC project. All images that are created for the FABRIC project should be thouroughly documented and have publically available images registered in DockerHub ([https://hub.docker.com](https://hub.docker.com))

**NOTE**: initial commit contains only the references to the basic images without any modificaton for FABRIC, which will be assigned at a later date.

## [Neo4j/APOC](neo4j)

What is Neo4j?

- Neo4j is an open-source, NoSQL, native graph database that provides an ACID-compliant transactional backend for your applications. Initial development began in 2003, but it has been publicly available since 2007. The source code, written in Java and Scala, is available for free on GitHub or as a user-friendly desktop application download. Neo4j has both a Community Edition and Enterprise Edition of the database. The Enterprise Edition includes all that Community Edition has to offer, plus extra enterprise requirements such as backups, clustering, and failover abilities.
- Official Docker image: [https://hub.docker.com/_/neo4j/](https://hub.docker.com/_/neo4j/)
- GitHub repository: [https://github.com/neo4j/docker-neo4j-publish](https://github.com/neo4j/docker-neo4j-publish)

What is APOC?

- APOC stands for Awesome Procedures on Cypher. Before APOC’s release, developers needed to write their own procedures and functions for common functionality that Cypher or the Neo4j database had not yet implemented for support. Each developer might write his own version of these functions, causing a lot of duplication.

## Kafka

reference:

- kafka (not official): [https://hub.docker.com/r/bitnami/kafka](https://hub.docker.com/r/bitnami/kafka)
- zookeeper: [https://hub.docker.com/_/zookeeper](https://hub.docker.com/_/zookeeper)

## ELK

reference:

- elasticsearch: [https://hub.docker.com/_/elasticsearch](https://hub.docker.com/_/elasticsearch)
- logstash: [https://hub.docker.com/_/logstash](https://hub.docker.com/_/logstash)
- kibana: [https://hub.docker.com/_/kibana](https://hub.docker.com/_/kibana)

## Prometheus

reference: [https://hub.docker.com/r/prom/prometheus/](https://hub.docker.com/r/prom/prometheus/)

## Grafana

reference: [https://hub.docker.com/r/grafana/grafana](https://hub.docker.com/r/grafana/grafana)
