#!/usr/bin/env bash
set -euo pipefail
TIMESTAMP=$(date +%F_%H%M)
BACKUP_DIR=/backups/mysql
mkdir -p "${BACKUP_DIR}"
CONTAINER=mariadb

echo "Dumping MariaDB..."
docker exec "${CONTAINER}" sh -c 'exec mysqldump --single-transaction --all-databases -u root -p"$MYSQL_ROOT_PASSWORD"' > "${BACKUP_DIR}/mysql_${TIMESTAMP}.sql"
gzip "${BACKUP_DIR}/mysql_${TIMESTAMP}.sql"
echo "Backup saved: ${BACKUP_DIR}/mysql_${TIMESTAMP}.sql.gz"
# Optional: rclone or restic upload
