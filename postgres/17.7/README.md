# PostgreSQL 17.7 for FABRIC

This is a FABRIC-specific PostgreSQL 17.7 image that allows multiple databases to be created in the same container.

## Building the Image

```bash
cd postgres/17.7/
docker build -t fabrictestbed/postgres:17.7 .
```

## Usage

### Basic Example

```bash
docker run -d \
  --name postgres17 \
  -e POSTGRES_PASSWORD=testpassword \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_MULTIPLE_DATABASES=am,broker,controller \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  fabrictestbed/postgres:17.7
```

### Docker Compose Example

```yaml
database:
  image: fabrictestbed/postgres:17.7
  container_name: actordb
  restart: always
  environment:
    - POSTGRES_PASSWORD=testpassword
    - POSTGRES_USER=testuser
    - POSTGRES_MULTIPLE_DATABASES=am,broker,controller
  volumes:
    - pgdata:/var/lib/postgresql/data
  ports:
    - "5432:5432"

volumes:
  pgdata:
```

## Environment Variables

- `POSTGRES_PASSWORD` - Required. Password for the PostgreSQL user
- `POSTGRES_USER` - Required. PostgreSQL superuser name
- `POSTGRES_MULTIPLE_DATABASES` - Optional. Comma-separated list of databases to create on initialization
  - For each database name (e.g., "am"), the script creates:
    - A database named "am"
    - A user named "am"
    - Grants all privileges on the "am" database to the "am" user

## Verification

Check that multiple databases were created:

```bash
docker exec postgres17 psql -U testuser -c "\l"
```

Expected output should show the default `postgres` database plus your custom databases (`am`, `broker`, `controller`).

## PostgreSQL 12 to 17 Migration Guide

### 1. Data Migration

Run the upgrade utility as root to handle system-level file permissions:

```bash
docker run --rm \
  -e POSTGRES_INITDB_ARGS="--username=fabric" \
  -v /opt/data/database/postgres:/var/lib/postgresql/12/data \
  -v /opt/data/database/postgres_new:/var/lib/postgresql/17/data \
  tianon/postgres-upgrade:12-to-17 \
  --username=fabric

```

### 2. File Swap & Restart

```bash
cd /opt/data/database/
mv postgres postgres_v12_old
mv postgres_new postgres

# Update docker-compose.yml image to fabrictestbed/postgres:17 beforehand
docker compose up -d

```

### 3. Collation & Index Maintenance

Essential to prevent index corruption due to OS-level library changes:

```bash
# Refresh Collation Versions
docker exec database psql -U fabric -t -c "SELECT datname FROM pg_database WHERE datallowconn" | \
xargs -I {} docker exec database psql -U fabric -d {} -c "ALTER DATABASE \"{}\\" REFRESH COLLATION VERSION;"
```
```
docker exec database vacuumdb -U fabric --all --analyze-in-stages
docker exec database reindexdb -U fabric --all
```

### 4. Network Access

Allow internal Docker traffic and reload configuration:

```bash
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /opt/data/database/postgres/pg_hba.conf
docker exec database psql -U fabric -c "SELECT pg_reload_conf();"
docker restart database
```

## What's New in PostgreSQL 17

Key improvements over PostgreSQL 12:

- **Performance**: Significant improvements in query execution, especially for partitioned tables
- **Logical Replication**: Enhanced features and better performance
- **Partitioning**: Better partition pruning and management
- **JSON/JSONB**: New functions and operators
- **Parallelism**: More operations support parallel execution
- **Monitoring**: Extended statistics and better query introspection

## Official Documentation

- [PostgreSQL 17 Documentation](https://www.postgresql.org/docs/17/)
- [PostgreSQL 17 Release Notes](https://www.postgresql.org/docs/17/release-17.html)
- [Official PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
