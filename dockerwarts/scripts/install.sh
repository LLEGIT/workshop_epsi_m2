#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})/.." && pwd -P)"

echo "1/ Creating Docker networks (if missing)"
docker network inspect web >/dev/null 2>&1 || docker network create web
docker network inspect backend >/dev/null 2>&1 || docker network create backend
docker network inspect monitoring >/dev/null 2>&1 || docker network create monitoring

echo "2/ Starting stack"
cd "${ROOT_DIR}/docker"
docker compose pull
docker compose up -d

echo "Done. Services started. Check logs with: docker compose ps && docker compose logs -f"
