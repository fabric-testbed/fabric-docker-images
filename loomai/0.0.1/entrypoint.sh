#!/bin/bash
# Entrypoint: fix volume ownership then start supervisord.
# Runs as root so it can chown the mounted volume, then supervisord
# launches backend and nginx as the fabric user.
chown -R fabric:fabric /home/fabric/work 2>/dev/null || true
exec supervisord -c /etc/supervisor/supervisord.conf
