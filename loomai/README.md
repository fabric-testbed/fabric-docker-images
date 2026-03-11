# LoomAI

AI-assisted experiment designer for the [FABRIC testbed](https://fabric-testbed.net/).

- **Source**: https://github.com/fabric-testbed/loomai
- **Docker Hub**: https://hub.docker.com/r/fabrictestbed/loomai

## Versions

| Version | LoomAI Release | Description |
|---------|---------------|-------------|
| 0.0.1   | v0.0.1        | Initial release |

## Ports

| Port | Service | Description |
|------|---------|-------------|
| 3000 | Nginx | Web UI frontend |
| 8000 | Uvicorn | FastAPI backend API |
| 8889 | JupyterLab | Per-slice notebook environments |
| 9100-9199 | SSH Proxy | Tunnel proxies for VM web apps |

## Usage

```bash
docker pull fabrictestbed/loomai:0.0.1
docker run -d \
  -p 3000:3000 -p 8000:8000 -p 8889:8889 -p 9100-9199:9100-9199 \
  -v fabric_work:/home/fabric/work \
  fabrictestbed/loomai:0.0.1
```



