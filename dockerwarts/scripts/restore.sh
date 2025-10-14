#!/bin/bash
# =====================================
# Restore Script for BigData Infrastructure
# =====================================

if [ -z "$1" ]; then
  echo "Usage: ./restore.sh <backup_file.tar.gz>"
  exit 1
fi

BACKUP_FILE=$1
TMP_DIR="/tmp/restore_$(date +%s)"
mkdir -p "$TMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TMP_DIR"

echo "=== Restoring from $BACKUP_FILE ==="

# 1. Restore MariaDB (GLPI)
docker cp "$TMP_DIR/glpi.sql" mariadb:/restore.sql
docker exec mariadb sh -c 'mysql -u root -p"$MARIADB_ROOT_PASSWORD" glpi < /restore.sql'

# 2. Restore Elasticsearch
docker cp "$TMP_DIR/snapshots" elasticsearch:/usr/share/elasticsearch/snapshots
docker exec elasticsearch curl -X POST "localhost:9200/_snapshot/daily_backup/snap_*/_restore"

# 3. Restore Cassandra
docker cp "$TMP_DIR/cassandra_data" cassandra:/var/lib/cassandra/data
docker exec cassandra nodetool refresh

echo "=== Restore completed successfully ==="
