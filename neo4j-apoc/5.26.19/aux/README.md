## Overview

Files in this folder aren't actually used - they are from the original neo4j
[community docker definition](https://github.com/neo4j/docker-neo4j-publish)
to help make sense of what docker_entrypoint is doing.

The reference files (docker-entrypoint.sh, neo4j.conf, neo4jlabs-plugins.json) are
based on Neo4j 5.26.19 community edition.

The migration scripts (migrate.sh, migration-notes.md) are actively used for
upgrading from Neo4j 5.3.0/5.12.0 to 5.26.19 LTS.
