#!/usr/bin/env bash
set -euo pipefail
log() { echo "[$(date +%T)] $*"; }
check_disk() {
  local limit="$1"
  local used=42
  log "disk check, limit $limit"
  [ "$used" -lt "$limit" ] || return 1
  echo "$used"
}
main() {
  log "start"
  pct=$(check_disk 90)
  echo "captured: $pct"
  if check_disk 10 >/dev/null; then echo "ok"; else echo "check_disk returned $?"; fi
  log "done"
}
main "$@"
