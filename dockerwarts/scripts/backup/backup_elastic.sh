#!/usr/bin/env bash
set -euo pipefail
# Elasticsearch snapshot using snapshot repository on mounted backups volume
REPO_PATH="/backups/elasticsearch"
mkdir -p "${REPO_PATH}"
curl -XPUT "http://localhost:9200/_snapshot/backup_repo" -H 'Content-Type: application/json' -d "{\"type\":\"fs\",\"settings\":{\"location\":\"${REPO_PATH}\"}}"
SNAP_NAME="snapshot_$(date +%F_%H%M)"
curl -XPUT "http://localhost:9200/_snapshot/backup_repo/${SNAP_NAME}?wait_for_completion=true"
echo "Elasticsearch snapshot ${SNAP_NAME} complete"
