#!/usr/bin/env bash
set -euo pipefail
src="${1:?usage: backup.sh <folder>}"
dest="/tmp/backups"
mkdir -p "$dest"
file="$dest/backup-$(date +%Y%m%d-%H%M).tar.gz"
tar -czf "$file" -C "$src" .
tar -tzf "$file" >/dev/null
find "$dest" -name 'backup-*.tar.gz' -mtime +7 -delete
echo "$(date +%T) OK $file"
