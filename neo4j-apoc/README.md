### Versions available:

Available in this repo:
- 4.0.3, (APOC 4.0.0.10, GDS 1.2.1) latest: ([Dockerfile](4.0.3/))

Available from RENCI-NRIG/impact-docker-images:
- 3.5.0, latest: ([Dockerfile](https://github.com/RENCI-NRIG/impact-docker-images/tree/master/neo4j/3.5.0))
- 3.4.7: ([Dockerfile](https://github.com/RENCI-NRIG/impact-docker-images/tree/master/neo4j/3.4.7))

### What is Neo4j?

- Neo4j is an open-source, NoSQL, native graph database that provides an ACID-compliant transactional backend for your applications. Initial development began in 2003, but it has been publicly available since 2007. The source code, written in Java and Scala, is available for free on GitHub or as a user-friendly desktop application download. Neo4j has both a Community Edition and Enterprise Edition of the database. The Enterprise Edition includes all that Community Edition has to offer, plus extra enterprise requirements such as backups, clustering, and failover abilities.
- Official Docker image: [https://hub.docker.com/_/neo4j/](https://hub.docker.com/_/neo4j/)
- GitHub repository: [https://github.com/neo4j/docker-neo4j-publish](https://github.com/neo4j/docker-neo4j-publish)

### What is APOC?

- [APOC](https://neo4j.com/developer/neo4j-apoc/) stands for Awesome Procedures on Cypher. Before APOC’s release, developers needed to write their own procedures and functions for common functionality that Cypher or the Neo4j database had not yet implemented for support. Each developer might write his own version of these functions, causing a lot of duplication.


### What is GDS?

This [library](https://neo4j.com/docs/graph-data-science/current/introduction/) provides efficiently implemented, parallel versions of common graph algorithms for Neo4j, exposed as Cypher procedures.

### How to run

The docker definition has two required volumes - one in which Neo4j stores its data and another, from which APOC can import external file (e.g. GraphML) into Neo4j. Both must be specified when starting up the container.

1. **Neo4j Data** - map to `/data` of the container
2. **APOC Imports** - map to `/imports` of the container

Example:

```
$ mkdir -p neo4j/data
$ mkdir -p neo4j/imports
$ echo password > neo4j/password
```

Then start the docker:
```docker
$ docker run -d \
  --user=$(id -u):$(id -g) \
  --name=neo4j \
  --publish=7473:7473 \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  fabrictestbed/neo4j:latest
```

Once the container completes it's startup script a web UI will be running at [http://localhost:7474/](http://localhost:7474/)

Verify that container has completed script

```console
$ docker logs neo4j
Changed password for user 'neo4j'.
Active database: graph.db
Directories in use:
  home:         /var/lib/neo4j
  config:       /var/lib/neo4j/conf
  logs:         /var/lib/neo4j/logs
  plugins:      /var/lib/neo4j/plugins
  import:       /var/lib/neo4j/import
  data:         /var/lib/neo4j/data
  certificates: /var/lib/neo4j/certificates
  run:          /var/lib/neo4j/run
Starting Neo4j.
2019-01-03 14:54:32.205+0000 WARN  Unknown config option: causal_clustering.discovery_listen_address
2019-01-03 14:54:32.212+0000 WARN  Unknown config option: causal_clustering.raft_advertised_address
2019-01-03 14:54:32.212+0000 WARN  Unknown config option: causal_clustering.raft_listen_address
2019-01-03 14:54:32.213+0000 WARN  Unknown config option: ha.host.coordination
2019-01-03 14:54:32.213+0000 WARN  Unknown config option: causal_clustering.transaction_advertised_address
2019-01-03 14:54:32.213+0000 WARN  Unknown config option: causal_clustering.discovery_advertised_address
2019-01-03 14:54:32.214+0000 WARN  Unknown config option: ha.host.data
2019-01-03 14:54:32.214+0000 WARN  Unknown config option: causal_clustering.transaction_listen_address
2019-01-03 14:54:32.240+0000 INFO  ======== Neo4j 3.5.0 ========
2019-01-03 14:54:32.259+0000 INFO  Starting...
2019-01-03 14:54:46.751+0000 INFO  Bolt enabled on 0.0.0.0:7687.
2019-01-03 14:54:50.397+0000 INFO  Started.
2019-01-03 14:54:52.575+0000 INFO  Remote interface available at http://localhost:7474/
...
```

Open web UI at [http://localhost:7474/](http://localhost:7474/)

<img width="80%" alt="web UI on start" src="https://user-images.githubusercontent.com/5332509/50646321-c0009580-0f43-11e9-90d8-1f63f612f6f1.png">

Login wiht user/pass = neo4j/password

<img width="80%" alt="web UI post login" src="https://user-images.githubusercontent.com/5332509/50646322-c0992c00-0f43-11e9-821b-3a131f9c95ca.png">
