# LoomAI - AI-assisted experiment designer for FABRIC testbed
# Builds a single container with FastAPI backend + React/Next.js frontend + Nginx
#
# Convention: fabrictestbed/loomai:<version>
# Source:     https://github.com/fabric-testbed/loomai

ARG LOOMAI_VERSION=v0.0.1
ARG LOOMAI_REPO=https://github.com/fabric-testbed/loomai.git

# --- Stage 1: Clone source ---
FROM alpine/git:latest AS source
ARG LOOMAI_VERSION
ARG LOOMAI_REPO
RUN git clone --depth 1 --branch ${LOOMAI_VERSION} ${LOOMAI_REPO} /src

# --- Stage 2: Build frontend ---
FROM node:18-alpine AS frontend-build
WORKDIR /app
ENV NEXT_BUILD_MODE=export
# Increase memory for Next.js build
ENV NODE_OPTIONS="--max-old-space-size=4096"
COPY --from=source /src/frontend/package.json /src/frontend/package-lock.json ./
RUN npm ci
COPY --from=source /src/frontend/ .
RUN npm run build

# --- Stage 3: Final image ---
FROM python:3.11-slim

LABEL maintainer="komal.thareja@gmail.com"
LABEL org.opencontainers.image.source="https://github.com/fabric-testbed/loomai"

WORKDIR /app

# Install system deps for FABlib + nginx + supervisord + tmux + sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libffi-dev libssl-dev openssh-client git \
    nginx supervisor tmux sudo curl \
    && rm -rf /var/lib/apt/lists/*

# Create fabric user with passwordless sudo
RUN useradd -m -s /bin/bash -d /home/fabric fabric && \
    echo "fabric ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/fabric && \
    chmod 0440 /etc/sudoers.d/fabric

# Install Python dependencies
COPY --from=source /src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install JupyterLab for per-slice notebook environments
RUN pip install --no-cache-dir jupyterlab
# Default JupyterLab terminals to bash
RUN mkdir -p /etc/jupyter && \
    echo "c.ServerApp.terminado_settings = {'shell_command': ['/bin/bash']}" \
    > /etc/jupyter/jupyter_server_config.py

# Install Node.js for AI CLI tools
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install AI CLI tools
RUN pip install --no-cache-dir aider-chat streamlit
RUN npm install -g @anthropic-ai/claude-code @charmland/crush opencode-ai

# Copy backend code
COPY --from=source /src/backend/app/ app/

# Copy version file for update checks (read by backend)
COPY --from=source /src/frontend/src/version.ts /app/VERSION

# Copy builtin slice-libraries (slice templates, VM templates, recipes)
COPY --from=source /src/slice-libraries/ slice-libraries/

# Copy AI tools config (skills, agents, shared context)
COPY --from=source /src/ai-tools/ ai-tools/

# Copy built frontend
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Nginx config — use localhost since backend runs in same container
RUN rm -f /etc/nginx/sites-enabled/default
# Set pid file to a writable location for non-root nginx
RUN sed -i 's|pid /run/nginx.pid;|pid /tmp/nginx.pid;|' /etc/nginx/nginx.conf || \
    sed -i '1i pid /tmp/nginx.pid;' /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Fix nginx directories for non-root operation
RUN mkdir -p /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /var/lib/nginx && \
    chown -R fabric:fabric /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /var/lib/nginx

# Supervisord config to run both nginx and uvicorn as fabric user
COPY supervisord.conf /etc/supervisor/conf.d/fabric-webui.conf

# Set up fabric user home and storage
RUN mkdir -p /home/fabric/work/fabric_config && chown -R fabric:fabric /home/fabric
ENV FABRIC_CONFIG_DIR=/home/fabric/work/fabric_config
ENV FABRIC_STORAGE_DIR=/home/fabric/work
ENV HOME=/home/fabric

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Frontend on 3000, backend on 8000, 8889 for JupyterLab, 9100-9199 for SSH tunnel proxies
EXPOSE 3000 8000 8889 9100-9199

ENTRYPOINT ["/app/entrypoint.sh"]
