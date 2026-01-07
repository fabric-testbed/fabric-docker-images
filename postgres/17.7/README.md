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

To make this README section truly useful for others (or your future self), it’s helpful to include the **pre-requisite** stop command and the **post-upgrade** cleanup steps.

Here is a polished version that covers the full lifecycle of the migration:

---

## Upgrading from PostgreSQL 12 to 17

PostgreSQL does not support in-place major version upgrades. You must migrate the data files using `pg_upgrade`.

### 1. Stop the current database

Ensure the container is stopped so the data files are in a consistent state:

```bash
docker stop database

```

### 2. Run the Migration

Run the following command as a user with root/sudo privileges to ensure correct file permissions:

```bash
docker run --rm \
  -e POSTGRES_INITDB_ARGS="--username=fabric" \
  -v /opt/data/database/postgres:/var/lib/postgresql/12/data \
  -v /opt/data/database/postgres_new:/var/lib/postgresql/17/data \
  tianon/postgres-upgrade:12-to-17 \
  --username=fabric --link

```

> **Note:** The `--link` flag is used to perform the upgrade via hard links, making the process nearly instantaneous and avoiding doubling disk usage.

### 3. Swap Data Directories

After the upgrade reports "Success", swap the old data with the new:

```bash
cd /opt/data/database/
mv postgres postgres_v12_bak
mv postgres_new postgres

```

### 4. Update and Start

1. Clear the WAL/log directory (e.g., `./pg_data/logs`) as version 12 logs are incompatible with 17.
2. Update the `image` tag in `docker-compose.yaml` to `postgres:17`.
3. Start the container: `docker-compose up -d`.

### 5. Post-Upgrade Optimization

Rebuild the database statistics to ensure optimal performance:

```bash
docker exec -u fabric database vacuumdb --all --analyze-in-stages
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
