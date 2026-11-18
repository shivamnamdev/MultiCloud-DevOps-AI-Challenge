#!/usr/bin/env bash
set -euo pipefail

log()   { echo "[$(date +%T)] $*"; }
usage() { echo "Usage: $0 <service> [disk-limit-percent]"; exit 1; }

[ $# -ge 1 ] || usage
service="$1"
limit="${2:-90}"
fail=0

disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge "$limit" ]; then log "FAIL disk ${disk}%"; fail=1; else log "OK   disk ${disk}%"; fi

if systemctl is-active --quiet "$service"; then log "OK   $service"; else log "FAIL $service"; fail=1; fi

exit "$fail"
