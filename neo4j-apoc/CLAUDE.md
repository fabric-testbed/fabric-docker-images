# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains Docker images for Neo4j Community Edition with APOC (Awesome Procedures on Cypher) and GDS (Graph Data Science) plugins for the FABRIC project. Images are published to Docker Hub at `fabrictestbed/neo4j-apoc`.

## Repository Structure

The repository is organized by Neo4j version, where each version directory contains:
- `Dockerfile` - Docker image definition
- `apoc.conf` - APOC-specific configuration (enables file imports)
- `README.md` - Version-specific documentation
- `aux/` - Auxiliary files from upstream Neo4j docker definitions (for reference only)

Current maintained versions:
- `5.12.0/` - Latest (Neo4j 5.12.0, APOC 5.x, GDS 2.2.6)
- `5.3.0/` - Neo4j 5.3.0 with APOC 5.3.0, GDS 2.2.6
- `4.1.6/` - Legacy (Neo4j 4.1.6, APOC 4.1.0.10, GDS 1.5.0)
- `4.0.3/` - Legacy (Neo4j 4.0.3, APOC 4.0.0.10, GDS 1.2.1)

## Building and Testing

### Building Docker Images

Build a specific version:
```bash
cd <version>/
docker build -t fabrictestbed/neo4j-apoc:<version> .
```

Example:
```bash
cd 5.12.0/
docker build -t fabrictestbed/neo4j-apoc:5.12.0 .
```

### Running Locally

Create required directories:
```bash
mkdir -p neo4j/data neo4j/imports neo4j/logs
```

Run the container:
```bash
docker run -d \
  --user=$(id -u):$(id -g) \
  --name=neo4j \
  --publish=7473:7473 \
  --publish=7474:7474 \
  --publish=7687:7687 \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  fabrictestbed/neo4j-apoc:<version>
```

Verify startup and plugin installation:
```bash
docker logs neo4j
```

Look for successful plugin installation messages:
- `Installing Plugin 'apoc' from /var/lib/neo4j/labs/apoc-*-core.jar`
- `Installing Plugin 'graph-data-science' from /var/lib/neo4j/products/neo4j-graph-data-science-*.jar`
- `Started.` message indicating successful startup

Access the Neo4j web UI at http://localhost:7474/ (credentials: neo4j/password)

## Architecture Notes

### Version 5.x Images (5.3.0+)

**Key architectural change**: Starting with Neo4j 5.x, APOC ships built-in with the community Docker image.

Docker configuration approach:
- Base image: `neo4j:<version>-community`
- APOC: Pre-bundled in base image, enabled via `NEO4J_PLUGINS` environment variable
- GDS: Downloaded during build from `graphdatascience.ninja` into `/var/lib/neo4j/products/`
- Plugin auto-installation: Handled by base image's entrypoint script
- Import directory: `/imports` (configured via `NEO4J_server_directories_import`)
- APOC file import: Enabled via separate `apoc.conf` file

Configuration files:
- `apoc.conf`: Sets `apoc.import.file.enabled=true` (required for APOC file imports)
- No manual plugin JAR management needed

### Version 4.x Images (4.1.6, 4.0.3)

**Legacy approach**: Plugins must be manually downloaded and configured.

Docker configuration approach:
- Base image: `neo4j:<version>`
- APOC: Downloaded from GitHub releases into `/var/lib/neo4j/plugins/`
- GDS: Downloaded from S3, unzipped into `/var/lib/neo4j/plugins/`
- Configuration: Manually appended to `neo4j.conf` including:
  - `dbms.security.procedures.unrestricted=apoc.*,gds.*`
  - `dbms.security.procedures.whitelist=apoc.*,gds.*`
  - `apoc.import.file.enabled=true`
  - `dbms.directories.import=/imports`

### Common Patterns Across Versions

All images:
- Expose ports: 7474 (HTTP), 7473 (HTTPS), 7687 (Bolt)
- Mount `/data` volume for database storage
- Mount `/imports` volume for APOC file imports
- Run as user `neo4j` (except during initial setup)
- Use base image's entrypoint script (`/startup/docker-entrypoint.sh` or `/docker-entrypoint.sh`)

## Migration Between Major Versions

### Migrating from 4.x to 5.x

Version 5.3.0 introduces breaking changes in Cypher syntax and database format. A multi-stage migration is required.

Migration process (via `5.3.0/aux/migrate.sh`):
1. Dump database from Neo4j 4.1.6 (SF4.0.0 format)
2. Restore in Neo4j 4.4.16 (converts to SF4.3.0 format)
3. Dump again from 4.4.16
4. Restore in Neo4j 5.3.0 with explicit migrate command

Run migration script:
```bash
cd <directory above neo4j/>
../fabric-docker-images/neo4j-apoc/5.3.0/aux/migrate.sh -i
```

Options:
- `-i`: Interactive mode (pauses at each step)
- `-u`: Undo migration and revert to 4.1.6
- `-h`: Show help

**Important**: Always run the migration script before switching to 5.x images.

## Deployment Notes

This repository follows FABRIC project conventions for automated builds:
- Jenkins automatically builds and publishes images to Docker Hub
- Directory structure determines image tags: `<image-name>/<version>/Dockerfile` → `fabrictestbed/<image-name>:<version>`
- New versions require creating an issue first to set appropriate permissions

When adding new versions:
1. Create issue at https://github.com/fabric-testbed/fabric-docker-images/issues
2. Wait for permission setup
3. Follow directory structure: `<version>/Dockerfile`
4. Include version-specific README if needed
