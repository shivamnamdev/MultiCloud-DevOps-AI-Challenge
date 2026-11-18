#!/usr/bin/env bash
set -euo pipefail
log() { echo "[$(date +%T)] $*" >&2; }
check_disk() { log "checking"; echo 42; }
pct=$(check_disk)
echo "captured only the number: $pct"
