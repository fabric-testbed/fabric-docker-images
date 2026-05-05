# LoomAI

AI-assisted experiment designer for the [FABRIC testbed](https://fabric-testbed.net/).

- **Source**: https://github.com/fabric-testbed/loomai
- **Docker Hub**: https://hub.docker.com/r/fabrictestbed/loomai

## Versions

| Version | LoomAI Release | Description |
|---------|---------------|-------------|
| 0.4.0    | v0.4.0         | HTTPS deployment, hub-disabled AI tools, tunnel sub-path rewriting for web apps, pre-upgrade pod culling |
| 0.3.0    | v0.3.0         | K8s multi-user support, standalone Docker password protection, token upload flow |
| 0.2.2    | v0.2.2         | Bastion username from UIS API |
| 0.2.0    | v0.2.0         | Release 0.2.0 |
| 0.1.0    | v0.1.0         | Install script, component type filters, heatmap color metric, resource calendar host view |
| 0.0.22   | v0.0.22        | Add loomai CLI, clean up jupyter-collaboration deps |
| 0.0.21   | v0.0.21        | Release 0.0.21 |
| 0.0.17   | v0.0.17        | Release 0.0.17 |
| 0.0.5   | v0.0.5        | Release 0.0.5 |
| 0.0.3   | v0.0.3        | Release 0.0.3 |
| 0.0.2   | v0.0.2        | Aligned Dockerfile with upstream loomai repo |
| 0.0.1   | v0.0.1        | Initial release |

## Ports

| Port | Service | Description |
|------|---------|-------------|
| 3000 | Nginx | Web UI frontend |
| 8000 | Uvicorn | FastAPI backend API |
| 8889 | JupyterLab | Per-slice notebook environments |
| 9100-9199 | SSH Proxy | Tunnel proxies for VM web apps |

## Usage

### Docker Compose (recommended)

```bash
curl -O https://raw.githubusercontent.com/fabric-testbed/fabric-docker-images/main/loomai/0.4.0/docker-compose.yml
docker compose up -d
```

Check the container logs for the auto-generated password:
```bash
docker compose logs | grep "LoomAI password"
```

### Docker Run

```bash
docker pull fabrictestbed/loomai:0.4.0
docker run -d \
  -p 3000:3000 -p 8000:8000 -p 8889:8889 -p 9100-9199:9100-9199 \
  -v fabric_work:/home/fabric/work \
  -e FABRIC_CONFIG_DIR=/home/fabric/work/fabric_config \
  -e FABRIC_STORAGE_DIR=/home/fabric/work \
  --dns 8.8.8.8 --dns 8.8.4.4 \
  --restart unless-stopped \
  fabrictestbed/loomai:0.4.0
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `LOOMAI_PASSWORD` | Set a custom password (default: auto-generated, shown in logs) |
| `LOOMAI_NO_AUTH=1` | Disable password protection (for trusted networks) |
| `LOOMAI_ENABLE_DOCS=1` | Enable Swagger/ReDoc API docs (disabled by default) |
