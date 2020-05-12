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

## [Kafka](kafka)

What is Kafka?

- Apache Kafka is an open-source stream-processing software platform developed by LinkedIn and donated to the Apache Software Foundation, written in Scala and Java. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds.
- Official website: https://kafka.apache.org/intro
- Kafka (not official): [https://hub.docker.com/r/bitnami/kafka](https://hub.docker.com/r/bitnami/kafka)
- zookeeper: [https://hub.docker.com/_/zookeeper](https://hub.docker.com/_/zookeeper)

## [ELK](elk)

What is Elastic Stack (ES or ELK)?

- "ELK" is the acronym for three open source projects: Elasticsearch, Logstash, and Kibana. Elasticsearch is a search and analytics engine. Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch. Kibana lets users visualize data with charts and graphs in Elasticsearch. The Elastic Stack is the next evolution of the ELK Stack.
- Official website: [https://www.elastic.co/](https://www.elastic.co/)
- elasticsearch: [https://hub.docker.com/_/elasticsearch](https://hub.docker.com/_/elasticsearch)
- logstash: [https://hub.docker.com/_/logstash](https://hub.docker.com/_/logstash)
- kibana: [https://hub.docker.com/_/kibana](https://hub.docker.com/_/kibana)

## Prometheus

reference: [https://hub.docker.com/r/prom/prometheus/](https://hub.docker.com/r/prom/prometheus/)

## Grafana

reference: [https://hub.docker.com/r/grafana/grafana](https://hub.docker.com/r/grafana/grafana)

## [AuthzForce RESTful PDP](authzforce-pdp/)

What is AuthzForce PDP?
- A Spring-based REST implementation of an AuthzForce PDP based on AuthzForce core engine
- AuthzForce [documentation](https://authzforce-ce-fiware.readthedocs.io/en/latest/)
- AuthzForce on [GitHub](https://github.com/authzforce)
