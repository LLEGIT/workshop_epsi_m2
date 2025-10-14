#!/usr/bin/env bash
set -euo pipefail
TIMESTAMP=$(date +%F_%H%M)
BACKUP_DIR=/backups/cassandra/${TIMESTAMP}
mkdir -p "${BACKUP_DIR}"
CONTAINER=cassandra
echo "Creating snapshots on Cassandra nodes (local POC single container)..."
docker exec "${CONTAINER}" nodetool snapshot -t backup_${TIMESTAMP}
# Copy snapshot files from container to host backups (example path)
docker cp "${CONTAINER}":/var/lib/cassandra/data "${BACKUP_DIR}"
echo "Cassandra snapshot copied to ${BACKUP_DIR}"
