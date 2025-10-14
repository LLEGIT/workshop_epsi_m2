#!/usr/bin/env bash
set -euo pipefail

ADMIN_NET=${1:-""}
LOG_PREFIX="FW_DOCKER"

# get docker network subnets
get_subnet() { docker network inspect "$1" -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}' 2>/dev/null || true; }

WEB_SUBNET=$(get_subnet web)
BACKEND_SUBNET=$(get_subnet backend)
MON_SUBNET=$(get_subnet monitoring)

echo "Web: $WEB_SUBNET, Backend: $BACKEND_SUBNET, Mon: $MON_SUBNET"

iptables -N DOCKER-USER 2>/dev/null || true
iptables -F DOCKER-USER

iptables -N DOCKER-USER-LOG 2>/dev/null || true
iptables -F DOCKER-USER-LOG
iptables -A DOCKER-USER-LOG -m limit --limit 10/min -j LOG --log-prefix "$LOG_PREFIX: " --log-level 4
iptables -A DOCKER-USER-LOG -j DROP

iptables -A DOCKER-USER -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A DOCKER-USER -i lo -j ACCEPT

# allow traefik public ports
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# allow internal necessary flows (examples)
# web -> backend : GLPI -> MariaDB
iptables -A DOCKER-USER -s "${WEB_SUBNET}" -d "${BACKEND_SUBNET}" -p tcp --dport 3306 -j ACCEPT
iptables -A DOCKER-USER -s "${WEB_SUBNET}" -d "${BACKEND_SUBNET}" -p tcp --dport 9042 -j ACCEPT

# monitoring scrapes
iptables -A DOCKER-USER -s "${MON_SUBNET}" -d "${BACKEND_SUBNET}" -p tcp --dport 9100 -j ACCEPT
iptables -A DOCKER-USER -s "${MON_SUBNET}" -d "${BACKEND_SUBNET}" -p tcp --dport 8080 -j ACCEPT

# final log & drop
iptables -A DOCKER-USER -j DOCKER-USER-LOG

echo "Firewall rules applied (DOCKER-USER)."
iptables -L DOCKER-USER -n --line-numbers
