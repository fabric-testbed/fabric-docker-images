# Overview

5.26.19 LTS is the long-term support release of Neo4j 5.x, supported until June 2028.
This version includes significant stability improvements and is compatible with GDS 2.13.

## Migration

For existing Neo4j 5.x databases (5.3.0 or 5.12.0), the migration process is automatic
within the 5.x family. However, we provide a migration script to ensure safe backup and
verification.

Prior to upgrading to 5.26.19, please run the [migration script](aux/migrate.sh) by
starting it above the neo4j/ folder where Neo4j database is mounted into the
docker container:

```
$ cd <directory above neo4j>
$ tree -L 3 neo4j
neo4j
├── data
│   ├── databases
│   │   ├── neo4j
│   │   ├── store_lock
│   │   └── system
│   ├── dbms
│   │   └── auth.ini
│   ├── server_id
│   └── transactions
│       ├── neo4j
│       └── system
└── imports
$ ../fabric-docker-images/neo4j-apoc/5.26.19/aux/migrate.sh -h
    This script migrates Neo4j graph database from 5.3.0/5.12.0 to 5.26.19 LTS.
     Use -i to force prompted interactive mode.
     Use -u to try to put things back as they were.
$ ../fabric-docker-images/neo4j-apoc/5.26.19/aux/migrate.sh -i
```
Using `-i` option forces the script to stop at every step waiting for ENTER press.
If something breaks use `-u` option to undo, if possible and set things back to the way they were.
