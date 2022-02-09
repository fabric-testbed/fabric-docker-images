# Docker tooling for FABRIC

Docker images or related Compose definitions for use with the FABRIC project. All images that are created for the FABRIC project should be thouroughly documented and have publically available images registered in DockerHub ([https://hub.docker.com/orgs/fabrictestbed/repositories](https://hub.docker.com/orgs/fabrictestbed/repositories))

- **NOTE**: initial commit contains only the references to the basic images without any modificaton for FABRIC, which will be assigned at a later date

## How to Contribute

This repository is organized in a way that allows an automated Jenkins service to build and publish the images to the [FABRIC Testbed Docker Hub](https://hub.docker.com/orgs/fabrictestbed/repositories)

The images are built and published based on the conventions used here. As an example, the image [fabrictestbed/neo4j-apoc:4.0.3](https://hub.docker.com/repository/docker/fabrictestbed/neo4j-apoc) was created as such because of how it is defined within this repository:

```console
neo4j-apoc/
    4.0.3/
        Dockerfile
```

Any contributions to this repository should follow the same structure as illustrated above.

- **NOTE**: Certain permissions must be set prior to the first time a new build definition is introduced to the repository. If you plan to add a new definition to the repository, please [create an issue first](https://github.com/fabric-testbed/fabric-docker-images/issues) such that we can set the appropriate permissions ahead of time.

Please see the Pre-requirements at the bottom of this file for useful information on getting started

---

## [Neo4j/APOC/GDS](neo4j-apoc)

What is Neo4j?

- Neo4j is an open-source, NoSQL, native graph database that provides an ACID-compliant transactional backend for your applications. Initial development began in 2003, but it has been publicly available since 2007. The source code, written in Java and Scala, is available for free on GitHub or as a user-friendly desktop application download. Neo4j has both a Community Edition and Enterprise Edition of the database. The Enterprise Edition includes all that Community Edition has to offer, plus extra enterprise requirements such as backups, clustering, and failover abilities.
- Official Docker image: [https://hub.docker.com/_/neo4j/](https://hub.docker.com/_/neo4j/)
- GitHub repository: [https://github.com/neo4j/docker-neo4j-publish](https://github.com/neo4j/docker-neo4j-publish)

What is APOC?

- APOC stands for Awesome Procedures on Cypher. Before APOC’s release, developers needed to write their own procedures and functions for common functionality that Cypher or the Neo4j database had not yet implemented for support. Each developer might write his own version of these functions, causing a lot of duplication.

What is GDS?

- This [library](https://neo4j.com/docs/graph-data-science/current/introduction/) provides efficiently implemented, parallel versions of common graph algorithms for Neo4j, exposed as Cypher procedures.

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

## [ELK with SSL and X-Pack](elk-ssl-xpack)

This shows how to set up **X-Pack security enabled (Free Basic License)** ELK stack with **SSL** using Nginx as a reverse proxy. X-Pack allows **role-based user control** through Kibana and **SSL encryption** between components of ELK stack and remote clients. **Nginx** with a public CA signed SSL certificate redirects outer HTTP/HTTPS traffic to Kibana container running in the host virtual machine.

- Elasticsearch X-Pack: [https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-xpack.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-xpack.html)
- Elasticsearch Stack Free Basic Subscriptions: [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions)
## Prometheus

reference: [https://hub.docker.com/r/prom/prometheus/](https://hub.docker.com/r/prom/prometheus/)

## Grafana

reference: [https://hub.docker.com/r/grafana/grafana](https://hub.docker.com/r/grafana/grafana)

## [AuthzForce RESTful PDP](authzforce-pdp/)

What is AuthzForce PDP?
- A Spring-based REST implementation of an AuthzForce PDP based on AuthzForce core engine
- AuthzForce [documentation](https://authzforce-ce-fiware.readthedocs.io/en/latest/)
- AuthzForce on [GitHub](https://github.com/authzforce)

---

## Pre-requirements
You may need to install Docker and Docker-Compose to build and start services. This section shows how to install Docker and Docker-compose. The instructions below are tested with **CentOS Linux release 7.5.1804 (Core)**.

### 1. Installing Docker CE
> Reference: https://docs.docker.com/engine/install/

#### 1. Remove old versions (if any exists)

```bash
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
```

#### 2. Set up the repository and install Docker Engine
```bash
sudo yum install -y yum-utils

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io
```

#### 3. Start Docker and test if it works

```bash
sudo systemctl start docker

sudo docker run hello-world
```

#### 4. Adding user to docker group 

> You may need to log out and in again to take this change affect. 

```bash
sudo usermod -aG docker your_user_name_here
```

### 2. Installing Docker-compose

> Reference: https://docs.docker.com/compose/install/

#### 1. Download current stable version of Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

#### 2. Apply executable permissions to the binary

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. Test if it works and prints version 

```bash
docker-compose --version
```
