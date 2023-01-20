# Overview

5.3.0 is a significant departure from the 4-series versions. There are differences
in Cypher syntax and underlying database format, including indices.

## Migration

Prior to turnin on 5.3.0 please run the [migration script](aux/migration.sh) by
starting it above the neo4j/ folder where Neo4j database is mounted into the
docker container:

```
$ cd <directory above neo4j>
$ tree -L 3 neo4j
neo4j
├── data
│   ├── databases
│   │   ├── neo4j
│   │   ├── store_lock
│   │   └── system
│   ├── dbms
│   │   └── auth.ini
│   ├── server_id
│   └── transactions
│       ├── neo4j
│       └── system
└── imports
    └── neo4j.dump
$ ../fabric-docker-images/neo4j-apoc/5.3.0/aux/migrate.sh -h
    This script migrates Neo4j graph database contents from 4.1.6/SF4.00 (via 4.4.16/SF4.3.0) to 5.3.0/SF5.x.
     Use -i to force prompted interactive mode.
     Use -u to try to put things back as they were.
$ ../fabric-docker-images/neo4j-apoc/5.3.0/aux/migrate.sh -i
```
Using `-i` option forces the script to stop at every step waiting for ENTER press.
If something breaks use `-u` option to undo, if possible and set things back to the way they were for 4.1.6
