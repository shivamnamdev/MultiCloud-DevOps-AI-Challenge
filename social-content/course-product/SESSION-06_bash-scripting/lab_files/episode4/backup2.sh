#!/usr/bin/env bash
set -euo pipefail
src="${1:?usage: backup2.sh <folder>}"
dest="/tmp/backups"
mkdir -p "$dest"
file="$dest/backup-$(date +%Y%m%d-%H%M).tar.gz"
part="$file.part"
trap 'rm -f "$part"' EXIT          # a half-made file never stays behind
tar -czf "$part" -C "$src" .
[ "$(tar -tzf "$part" | wc -l)" -gt 0 ]   # an archive with no entries counts as a failure
mv "$part" "$file"                 # the real name appears only when the archive is good
find "$dest" -name 'backup-*.tar.gz' -mtime +7 -delete
echo "$(date +%T) OK $file"
