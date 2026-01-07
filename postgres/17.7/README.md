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

## Upgrading from PostgreSQL 12

If you're upgrading from PostgreSQL 12.3, see [UPGRADE_FROM_12.md](./UPGRADE_FROM_12.md) for detailed migration instructions.

**Important**: This is a major version upgrade and requires data migration. Do not simply point the new container at your old data directory.

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
