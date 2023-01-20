### Versions available:

Available in this repo (and via [FABRIC Docker Hub](https://hub.docker.com/repository/docker/fabrictestbed/neo4j-apoc)):
- 5.3.0, (APOC 5.3.0, GDS 2.2.6) latest: ([Dockerfile](5.3.0/), [README](5.3.0/README.md)) - big change with this version in how APOC and GDS are handled. Requires that [migration script](5.3.0/aux/migration.sh) is run.
- 4.1.6, (APOC 4.1.0.10, GDS 1.5.0) latest: ([Dockerfile](4.1.6/))
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
- Note that APOC has become an integral part of Neo4j rather than being a contributed package. With version 5.x it ships built into the community Docker definition


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
$ mkdir -p neo4j/logs
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
  fabrictestbed/neo4j-apoc:latest
```

Note: the `neo4j/password` is not a file name, rather password for neo4j admin is set to `password`.

Once the container completes it's startup script a web UI will be running at [http://localhost:7474/](http://localhost:7474/)

Verify that container has completed script


```console
$ docker logs neo4j-5
Installing Plugin 'apoc' from /var/lib/neo4j/labs/apoc-*-core.jar to /var/lib/neo4j/plugins/apoc.jar
Applying default values for plugin apoc to neo4j.conf
Installing Plugin 'graph-data-science' from /var/lib/neo4j/products/neo4j-graph-data-science-*.jar to /var/lib/neo4j/plugins/graph-data-science.jar
Applying default values for plugin graph-data-science to neo4j.conf
Changed password for user 'neo4j'. IMPORTANT: this change will only take effect if performed before the database is started for the first time.
2023-01-17 19:03:51.210+0000 INFO  Starting...
2023-01-17 19:03:51.888+0000 INFO  This instance is ServerId{f5752c51} (f5752c51-6ca7-4fdb-aabd-6bf28d49fec3)
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
2023-01-17 19:03:53.006+0000 INFO  ======== Neo4j 5.3.0 ========
2023-01-17 19:03:53.487+0000 INFO  GDS compatibility: for Neo4j Settings 4.x -- not available, for Neo4j Settings 5.1 -- not available, for Neo4j Settings 5.2.0 -- not available, for Neo4j Settings 5.3 -- available, selected: Neo4j Settings 5.3
2023-01-17 19:03:53.487+0000 INFO  GDS compatibility: for Neo4j 4.3 -- not available, for Neo4j 4.4 -- not available, for Neo4j 5.1 -- not available, for Neo4j 5.2.0 -- not available, for Neo4j 5.3 -- available, selected: Neo4j 5.3
2023-01-17 19:04:14.205+0000 INFO  Bolt enabled on 0.0.0.0:7687.
2023-01-17 19:04:15.396+0000 INFO  Remote interface available at http://localhost:7474/
2023-01-17 19:04:15.401+0000 INFO  id: C47DD3A66FD19AE58D758A006AC089891E23EF1C555E2709C00FBC312D0AD144
2023-01-17 19:04:15.402+0000 INFO  name: system
2023-01-17 19:04:15.402+0000 INFO  creationDate: 2023-01-17T16:51:11.758Z
2023-01-17 19:04:15.402+0000 INFO  Started.
...
```
Note: the APOC and GDS plugins are installed from local files within the docker. If you see them being fetched from URLs, something isn't working right.

Open web UI at [http://localhost:7474/](http://localhost:7474/)

<img width="80%" alt="web UI on start" src="https://user-images.githubusercontent.com/5332509/50646321-c0009580-0f43-11e9-90d8-1f63f612f6f1.png">

Login wiht user/pass = neo4j/password

<img width="80%" alt="web UI post login" src="https://user-images.githubusercontent.com/5332509/50646322-c0992c00-0f43-11e9-821b-3a131f9c95ca.png">

## Upgrading databases

- For version 4.x and below, the `dbms.allow_upgrade=true` setting had to be in effect for the database engine to update the
database structure (the process is one-way and reversion is not possible without backups).
- For version 5.x the upgrade is automatic
