#!/bin/bash
# =====================================
# Backup Script for BigData Infrastructure
# =====================================

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/mnt/backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

echo "=== [$(date)] Starting backup... ==="

# 1. GLPI (MariaDB)
docker exec mariadb sh -c 'mysqldump -u root -p"$MARIADB_ROOT_PASSWORD" glpi > /backup/glpi.sql'
docker cp mariadb:/backup/glpi.sql "$BACKUP_DIR/"

# 2. Elasticsearch snapshot
docker exec elasticsearch curl -X PUT "localhost:9200/_snapshot/daily_backup" -H 'Content-Type: application/json' -d '{
  "type": "fs",
  "settings": { "location": "/usr/share/elasticsearch/snapshots" }
}'
docker exec elasticsearch curl -X PUT "localhost:9200/_snapshot/daily_backup/snap_$TIMESTAMP?wait_for_completion=true"

# 3. Cassandra snapshot
docker exec cassandra nodetool snapshot -t snap_$TIMESTAMP
docker cp cassandra:/var/lib/cassandra/data "$BACKUP_DIR/cassandra_data"

# 4. Compress & store
tar -czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"

echo "=== Backup completed successfully: $BACKUP_DIR.tar.gz ==="
