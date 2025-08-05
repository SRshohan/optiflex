#!/usr/bin/env bash
set -euo pipefail

# —— Configuration ——  
PROJECT_DIR="/home/user1/optiflex/optiflex"
COMPOSE_FILE="${PROJECT_DIR}/docker-compose.prod.yml"

# —— Deploy steps ——  
echo "⭑ Pulling latest code into ${PROJECT_DIR}…"
cd "${PROJECT_DIR}" || exit 
git pull origin main

echo "⭑ Building and restarting containers…"
sudo docker-compose up -d 

echo "✔ Deploy complete! $(date '+%Y-%m-%d %H:%M:%S')"

