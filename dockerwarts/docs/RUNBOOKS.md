
## `docs/RUNBOOKS.md`

Contains runbooks for key alerts (NodeHighCPU, ES down, Cassandra compaction backlog) and step-by-step commands to remediate.

---

# 7 — `.env` sample (`docker/.env`)

```env
# Hosts & DNS
GLPI_HOST=glpi.localhost
GRAFANA_HOST=grafana.localhost
TRAEFIK_ACME_EMAIL=ops@example.com

# Database
MYSQL_ROOT_PASSWORD=root_pass
GLPI_DB_NAME=glpidb
GLPI_DB_USER=glpi
GLPI_DB_PASSWORD=glpi_pass

# Cassandra
CASSANDRA_CLUSTER_NAME=BigDataCluster

# Grafana
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
