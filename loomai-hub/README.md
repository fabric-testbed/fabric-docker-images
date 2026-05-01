# LoomAI Hub

Multi-user orchestrator for LoomAI on Kubernetes. Handles CILogon OIDC authentication, FABRIC Core API authorization, Kubernetes pod spawning, and configurable-http-proxy route management.

- **Source**: https://github.com/fabric-testbed/loomai/tree/main/hub
- **Docker Hub**: https://hub.docker.com/r/fabrictestbed/loomai-hub

## Versions

| Version | Description |
|---------|-------------|
| 0.1.0   | Initial release — CILogon OAuth, FABRIC authorization, KubeSpawner, idle culler |

## Ports

| Port | Service | Description |
|------|---------|-------------|
| 8081 | Uvicorn | Hub FastAPI service |

## Usage

The Hub is designed to run as part of the LoomAI Helm chart on Kubernetes. See the [Kubernetes deployment docs](https://github.com/fabric-testbed/loomai/blob/main/docs/KUBERNETES.md) for full instructions.

### Standalone (for development)

```bash
docker pull fabrictestbed/loomai-hub:0.1.0
docker run -d \
  -p 8081:8081 \
  -v hub_data:/app/data \
  -e CILOGON_CLIENT_ID=<your-client-id> \
  -e CILOGON_CLIENT_SECRET=<your-client-secret> \
  -e SESSION_SECRET=<random-secret> \
  -e CHP_API_TOKEN=<proxy-auth-token> \
  -e FABRIC_CORE_API=https://uis.fabric-testbed.net \
  fabrictestbed/loomai-hub:0.1.0
```

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `CILOGON_CLIENT_ID` | CILogon OIDC client ID |
| `CILOGON_CLIENT_SECRET` | CILogon OIDC client secret |
| `SESSION_SECRET` | Secret for signing session cookies |
| `CHP_API_TOKEN` | Auth token for configurable-http-proxy API |
| `FABRIC_CORE_API` | FABRIC UIS API base URL |
| `HUB_PREFIX` | URL prefix for hub routes (default: `/hub`) |
| `DATABASE_URL` | SQLAlchemy async database URL (default: SQLite) |
