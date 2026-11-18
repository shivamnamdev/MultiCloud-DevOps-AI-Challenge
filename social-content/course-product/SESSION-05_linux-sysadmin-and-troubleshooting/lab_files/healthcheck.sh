#!/usr/bin/env bash
disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge 90 ]; then echo "FAIL disk ${disk}%"; fail=1; else echo "OK   disk ${disk}%"; fi
if systemctl is-active --quiet nginx; then echo "OK   nginx"; else echo "FAIL nginx"; fail=1; fi
exit ${fail:-0}
