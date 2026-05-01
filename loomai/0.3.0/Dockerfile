# LoomAI - AI-assisted experiment designer for FABRIC testbed
# Builds a single container with FastAPI backend + React/Next.js frontend + Nginx
#
# Convention: fabrictestbed/loomai:<version>
# Source:     https://github.com/fabric-testbed/loomai

ARG LOOMAI_VERSION=v0.3.3
ARG LOOMAI_REPO=https://github.com/fabric-testbed/loomai.git

# --- Stage 1: Clone source ---
FROM alpine/git:latest AS source
ARG LOOMAI_VERSION
ARG LOOMAI_REPO
RUN git clone --depth 1 --branch ${LOOMAI_VERSION} ${LOOMAI_REPO} /src

# --- Stage 2: Build frontend ---
FROM node:22-alpine AS frontend-build
WORKDIR /app
COPY --from=source /src/frontend/package.json /src/frontend/package-lock.json ./
RUN npm ci --prefer-offline --no-audit && npm cache clean --force
COPY --from=source /src/frontend/ .
RUN npm run build && rm -rf node_modules

# --- Stage 3: Final image ---
FROM python:3.11-slim

LABEL maintainer="komal.thareja@gmail.com"
LABEL org.opencontainers.image.source="https://github.com/fabric-testbed/loomai"

WORKDIR /app

# Install all system deps in one layer: build tools, runtime, Node.js
# Build deps (gcc, python3-dev, libffi-dev) are purged after pip install
COPY --from=source /src/backend/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libffi-dev libssl-dev \
    openssh-client git nginx supervisor tmux sudo curl \
    vim nano less htop strace tree jq wget rsync zip unzip \
    iputils-ping dnsutils net-tools traceroute ripgrep \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y jupyter-collaboration jupyter-collaboration-ui jupyter-docprovider jupyter-server-ydoc jupyter-server-documents 2>/dev/null || true \
    && rm -f /usr/local/etc/jupyter/jupyter_server_config.d/jupyter_server_documents.json \
       /usr/local/etc/jupyter/jupyter_server_config.d/jupyter_collaboration.json 2>/dev/null || true \
    && apt-get purge -y gcc python3-dev libffi-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Create fabric user with passwordless sudo
RUN useradd -m -s /bin/bash -d /home/fabric fabric && \
    echo "fabric ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/fabric && \
    chmod 0440 /etc/sudoers.d/fabric

# Nginx + supervisor config (changes rarely — good cache layer)
RUN rm -f /etc/nginx/sites-enabled/default \
    && (sed -i 's|pid /run/nginx.pid;|pid /tmp/nginx.pid;|' /etc/nginx/nginx.conf || \
        sed -i '1i pid /tmp/nginx.pid;' /etc/nginx/nginx.conf) \
    && mkdir -p /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /var/lib/nginx \
    && chown -R fabric:fabric /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /var/lib/nginx

RUN cat > /etc/nginx/conf.d/default.conf <<'NGINX'
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 3000;
    root /usr/share/nginx/html;
    index index.html;

    client_max_body_size 500m;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /jupyter/ {
        proxy_pass http://127.0.0.1:8889;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 604800s;
        proxy_send_timeout 604800s;
        proxy_buffering off;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 604800s;
        proxy_send_timeout 604800s;
        proxy_buffering off;
    }
}
NGINX

RUN cat > /etc/supervisor/conf.d/fabric-webui.conf <<'CONF'
[supervisord]
nodaemon=true
user=root
logfile=/dev/stdout
logfile_maxbytes=0

[program:backend]
command=uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/app
user=fabric
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:nginx]
command=nginx -g "daemon off;"
user=fabric
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
CONF

# Copy static assets that change occasionally
COPY --from=source /src/ai-tools/ ai-tools/

# Install loomai CLI (pure Python — no compiled deps)
COPY --from=source /src/cli/ /app/cli/
RUN pip install --no-cache-dir /app/cli/ && rm -rf /app/cli/

# Copy built frontend (changes on frontend builds)
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Copy backend code (changes most often — last for best cache)
COPY --from=source /src/backend/app/ app/
COPY --from=source /src/backend/scripts/ scripts/
COPY --from=source /src/frontend/src/version.ts /app/VERSION

# Set up fabric user home and storage
RUN mkdir -p /home/fabric/work/fabric_config && chown -R fabric:fabric /home/fabric
ENV FABRIC_CONFIG_DIR=/home/fabric/work/fabric_config
ENV FABRIC_STORAGE_DIR=/home/fabric/work
ENV HOME=/home/fabric

# Copy entrypoint script
COPY --from=source /src/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Frontend on 3000, backend on 8000, 8889 for JupyterLab, 9100-9199 for SSH tunnel proxies
EXPOSE 3000 8000 8889 9100-9199

ENTRYPOINT ["/app/entrypoint.sh"]
