#!/usr/bin/env bash
set -euo pipefail

echo "⭑ Pulling latest code…"
git -C /home/user1/optiflex/optiflex pull

echo "⭑ Building and restarting containers…"
docker-compose -f /home/user1/optiflex/optiflex/docker-compose.prod.yml up -d --build

echo "✔ Deploy complete!"
