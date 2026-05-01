# LoomAI Hub — Multi-user orchestrator for Kubernetes deployments
# Handles CILogon OIDC auth, FABRIC authorization, pod spawning, proxy management
#
# Convention: fabrictestbed/loomai-hub:<version>
# Source:     https://github.com/fabric-testbed/loomai

ARG LOOMAI_VERSION=v0.4.0
ARG LOOMAI_REPO=https://github.com/fabric-testbed/loomai.git

# --- Stage 1: Clone source ---
FROM alpine/git:latest AS source
ARG LOOMAI_VERSION
ARG LOOMAI_REPO
RUN git clone --depth 1 --branch ${LOOMAI_VERSION} ${LOOMAI_REPO} /src

# --- Stage 2: Final image ---
FROM python:3.11-slim

LABEL maintainer="komal.thareja@gmail.com"
LABEL org.opencontainers.image.source="https://github.com/fabric-testbed/loomai"

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY --from=source /src/hub/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --from=source /src/hub/app/ app/

# Create non-root user
RUN useradd -m -s /bin/bash hub && \
    mkdir -p /app/data && chown -R hub:hub /app/data

ENV HUB_PREFIX=/hub
ENV DATABASE_URL=sqlite+aiosqlite:///./data/hub.db

EXPOSE 8081

USER hub

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081", "--log-level", "info"]
