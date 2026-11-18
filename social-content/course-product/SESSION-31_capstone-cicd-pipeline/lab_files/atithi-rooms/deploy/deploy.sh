#!/usr/bin/env bash
set -euo pipefail
IMAGE="$1"; NAME=rooms
PREV=$(docker inspect -f '{{.Config.Image}}' "$NAME" 2>/dev/null || true)
docker pull "$IMAGE"
docker rm -f "$NAME" 2>/dev/null || true
docker run -d --name "$NAME" --restart unless-stopped -p 8081:5000 "$IMAGE"
for i in $(seq 1 20); do
  if curl -fsS http://localhost:8081/health >/dev/null; then
    echo "$(date -Is) deployed $IMAGE (was ${PREV:-none})" | sudo tee -a /var/log/atithi-deploys.log
    exit 0
  fi
  sleep 3
done
echo "$(date -Is) FAILED $IMAGE, rolling back to ${PREV:-none}" | sudo tee -a /var/log/atithi-deploys.log
docker rm -f "$NAME"
[ -n "$PREV" ] && docker run -d --name "$NAME" --restart unless-stopped -p 8081:5000 "$PREV"
exit 1
