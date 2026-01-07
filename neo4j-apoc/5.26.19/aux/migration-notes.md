# Migrating from Neo4j 5.3.0/5.12.0 to 5.26.19 LTS

## References
- [Neo4j 5.x Upgrade Documentation](https://neo4j.com/docs/operations-manual/current/upgrade/)
- [GDS 2.13 Compatibility](https://neo4j.com/docs/graph-data-science/current/installation/)
- [Neo4j 5.26.19 Docker Image](https://github.com/neo4j/docker-neo4j-publish)

## Key Differences from 4.x to 5.x Migration

The 5.x to 5.26.19 migration is significantly simpler than 4.x to 5.x because:
- **Store Format**: Compatible within 5.x family (automatic upgrade)
- **No Intermediate Version**: Direct upgrade possible
- **Index Types**: No BTREE to RANGE conversion needed
- **Commands**: Same neo4j-admin syntax throughout 5.x

## Overview of Migration Process

Within the 5.x family, Neo4j automatically upgrades the database format when
starting a newer version. The process is:

1. Backup current database (safety)
2. Optional: Create dump for portability
3. Start 5.26.19 container
4. Automatic upgrade occurs on startup
5. Verify successful upgrade

## Step by Step Manual Process

### 1. Backup Current Database

```bash
$ docker container stop neo4j
$ docker container rm neo4j
$ tar -czf neo4j-5x-backup.tar.gz neo4j/
```

### 2. Optional: Create Database Dump

For maximum safety and portability:

```bash
$ docker run -d --user=$(id -u):$(id -g) --name=neo4j-dump \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  fabrictestbed/neo4j-apoc:5.3.0 sleep infinity

$ docker exec neo4j-dump neo4j-admin database dump neo4j --to-path=/imports

$ docker container stop neo4j-dump
$ docker container rm neo4j-dump
```

**Note**: Neo4j 5.x uses different syntax than 4.x:
- **5.x syntax**: `neo4j-admin database dump neo4j --to-path=/imports`
- **4.x syntax**: `neo4j-admin dump --database=neo4j --to=/imports/neo4j.dump`

### 3. Start Neo4j 5.26.19

```bash
$ docker run -d --user=$(id -u):$(id -g) --name=neo4j \
  --publish=7473:7473 \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  fabrictestbed/neo4j-apoc:5.26.19
```

### 4. Monitor Upgrade

```bash
$ docker logs -f neo4j
```

Look for messages indicating successful startup:
```
INFO  Starting...
INFO  This instance is ServerId{...}
INFO  ======== Neo4j 5.26.19 ========
INFO  Bolt enabled on 0.0.0.0:7687.
INFO  Remote interface available at http://localhost:7474/
INFO  Started.
```

### 5. Verify Upgrade

1. Open http://localhost:7474/
2. Login with neo4j/password
3. Run verification query:
   ```cypher
   CALL dbms.components() YIELD name, versions, edition
   RETURN name, versions, edition
   ```
4. Verify version shows 5.26.19
5. Check plugins are loaded:
   ```cypher
   CALL dbms.procedures() YIELD name
   WHERE name STARTS WITH 'apoc' OR name STARTS WITH 'gds'
   RETURN DISTINCT split(name, '.')[0] AS plugin, count(*) AS procedureCount
   ```

### 6. Rollback if Needed

If issues occur:
```bash
$ docker container stop neo4j
$ docker container rm neo4j
$ rm -rf neo4j/
$ tar -xzf neo4j-5x-backup.tar.gz
$ docker run -d --user=$(id -u):$(id -g) --name=neo4j \
  --publish=7473:7473 \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  fabrictestbed/neo4j-apoc:5.3.0
```

## Using the Automated Migration Script

The migration script automates the above process:

```bash
$ cd <directory above neo4j/>
$ ../fabric-docker-images/neo4j-apoc/5.26.19/aux/migrate.sh -i
```

**Options**:
- `-i`: Interactive mode (pauses at each step)
- `-u`: Undo migration and restore from backup
- `-h`: Show help

The script will:
1. Verify directory structure
2. Stop any running containers
3. Create timestamped backup
4. Optionally create database dump
5. Start Neo4j 5.26.19
6. Monitor startup logs
7. Display verification instructions

## Neo4j 5.26.19 LTS Benefits

- **Long-term Support**: Supported until June 2028
- **Stability**: Focus on reliability over new features
- **GDS 2.13**: Latest Graph Data Science library
- **Production Ready**: Recommended for production deployments

## Troubleshooting

### Container fails to start
Check logs for errors:
```bash
docker logs neo4j
```

Common issues:
- Insufficient memory (increase Docker memory limit)
- Port conflicts (check ports 7474, 7473, 7687)
- Permission issues (check volume mount permissions)

### Plugins not loading
Verify plugins in logs:
```bash
docker logs neo4j | grep -i "plugin\|apoc\|gds"
```

Should see:
```
Installing Plugin 'apoc' from /var/lib/neo4j/labs/apoc-*-core.jar
Installing Plugin 'graph-data-science' from /var/lib/neo4j/products/neo4j-graph-data-science-*.jar
```

### Database version mismatch
If you see version mismatch errors, the automatic upgrade may have failed.
Use the backup to restore and investigate logs.

## Additional Resources

- [Neo4j Operations Manual](https://neo4j.com/docs/operations-manual/current/)
- [Graph Data Science Documentation](https://neo4j.com/docs/graph-data-science/current/)
- [APOC Documentation](https://neo4j.com/docs/apoc/current/)
