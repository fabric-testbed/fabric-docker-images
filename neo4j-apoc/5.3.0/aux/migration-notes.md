# Starting containers

## Old way

docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-5   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password -e NEO4J_PLUGINS='["apoc", "graph-data-science"]'  neo4j:5.3.0-community

## New way

Explicitly defining plugins
```
docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-5   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password -e NEO4J_PLUGINS='["apoc", "graph-data-science"]'  neo4j-fabric
```

With plugins set inside the Docker:
```
docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-5   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password neo4j-fabric
```

You can also overwrite certain config settings by doing e.g. -e NEO4J_dbms_allow__upgrade=true - to overwrite dbms.allow_upgrade=true in neo4j.conf. Notice that single '_' converts to a '.' and '__' converts to '_'.

Note that for the migration no changes to e.g. docker compose files *besides changing the name of the docker image* should be needed.

# Migrating from Neo4j 4.1 to 5.3

## References
- Backing up Neo4j 4.1 https://neo4j.com/docs/operations-manual/4.1/backup-restore/offline-backup/
- Upgrading to Neo4j 5.X https://neo4j.com/docs/upgrade-migration-guide/current/version-5/migration/migrate-databases/
- Restoring from a dump in 4.X https://neo4j.com/docs/operations-manual/5/backup-restore/restore-dump/

## Misc notes
- stop neo4j - can't be stopped using STOP DATABASE command (only enterprise version); also can't easily be stopped inside the container
  - solution - stop the container, start it with bash command, then get interactive bash to login

## Overview of the migration process

Overall the process involves dumping the neo4j database in 4.1.6 (current version) in SF4.0.0 format, then ingesting it inside an intermediate neo4j 4.4.16 to convert to SF4.3.0 and dumping again to then ingest in neo4j 5.3.0 and issuing explicit migrate command. Note that neo4j-admin extensively used here changed its features between neo4j 4.x and neo4j 5.x.

Everything is done using containerized Neo4j installs. 4.1.6 and 5.3.0 are built for FABRIC. 4.4.16 is an off-the-shelf Neo4j 4.4.16 community container.

1. Dump the neo4j database to /imports/neo4j.dump using last working version 4.1
2. Start with bash an off-the-shelf Neo4j docker 4.4.16
  a. Load dump using bash-start
  b. Start normal but with override migrate to force format migration to SF4.3.0 from SF4.0.0 used in 4.1)
3. Start in bash mode again and dump again to /imports/neo4j.dump (save the previous one)
4. Start Neo4j 5.3.0 in bash mode
  a. Use database load command to load it
  b. Use database migrate command and force tree index overwrites
5. Start Neo4j 5.3.0 normally to test

## Step by step

### Neo4j 4.1 dump
```
$ docker container stop neo4j
$ docker container rm neo4j
$ docker run -d   --user=$(id -u):$(id -g)   --name=neo4j   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports   -e NEO4J_AUTH=neo4j/password   -it fabrictestbed/neo4j-apoc:4.1.6 /bin/bash
$ docker exec -ti neo4j bash
```

Now docker is up, but neo4j is not running. Run neo4j-admin to dump neo4j and system databases (using /imports directory for export)
```
I have no name!@bbb6e52d4797:/var/lib/neo4j/bin$ ./neo4j-admin dump --database=neo4j --to=/imports/neo4j.dump
Done: 38 files, 258.0MiB processed.
```

Stop Neo4j4 4.1 container
```
$ docker container stop neo4j
# remove container state
$ docker container rm neo4j
```

Save the dump file to a safe location
```
$ cp neo4j/imports/neo4j.dump .
```

### Neo4j 4.4.16 intermediate migration
Run it in bash mode first to load the dump
```
$ docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-4.416   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password neo4j:4.4.16-community
I have no name!@8b8851d8e270:/var/lib/neo4j/bin$ ./neo4j-admin load --from=/imports/neo4j.dump --database=neo4j --force
```
Stop and clean container state. Now we need to force upgrade by starting Neo4j (no other option appears possible). Watch the logs.
```
$ docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-4.416   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password -e NEO4J_dbms_allow__upgrade=true neo4j:4.4.16-community
$ docker logs -f neo4j-4.416
...
2023-01-18 03:49:29.026+0000 INFO  [neo4j/93932702] Starting transaction logs migration.
2023-01-18 03:49:29.103+0000 INFO  [neo4j/93932702] Transaction logs migration completed.
2023-01-18 03:49:29.114+0000 INFO  [neo4j/93932702] Successfully finished upgrade of database, took 783ms
```
Stop and clean. Now run in bash mode again to dump (again in new format)
```
$ docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-4.416   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password -e NEO4J_dbms_allow__upgrade=true -ti neo4j:4.4.16-community /bin/bash
$ docker container -ti neo4j-4.416 bash
I have no name!@6293c1e3a85c:/var/lib/neo4j/bin$ ./neo4j-admin dump --database=neo4j --to=/imports/neo4j-4.416.dump
Selecting JVM - Version:11.0.17+8, Name:OpenJDK 64-Bit Server VM, Vendor:Eclipse Adoptium
Done: 40 files, 258.1MiB processed.
I have no name!@6293c1e3a85c:/var/lib/neo4j/bin$ ls /imports/
neo4j-4.416.dump  neo4j.dump
```
Stop and clean. Move neo4j/imports/neo4j-4.416.dump to neo4j/imports/neo4j.dump
```
$ mv neo4j/imports/neo4j-4.416.dump neo4j/imports/neo4j.dump
```

### Working with Neo4j 5.3.0

Start the container with bash:
```
$ docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-5   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password -ti neo4j-fabric /bin/bash
```

Load the dump (make sure the file is named /imports/neo4j.dump) and migrate the database (forcing indexes to  range instead of tree)
```
$ docker exec -ti neo4j-5 bash
I have no name!@d664caa4235f:/var/lib/neo4j/bin$ neo4j-admin database load --overwrite-destination=true --from-path=/imports neo4j
I have no name!@d664caa4235f:/var/lib/neo4j/bin$ neo4j-admin database migrate neo4j --force-btree-indexes-to-range
```

Stop and clean. Restart the database and verify using console.
```
docker run -d   --user=$(id -u):$(id -g)   --name=neo4j-5   --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password neo4j-fabric
```
