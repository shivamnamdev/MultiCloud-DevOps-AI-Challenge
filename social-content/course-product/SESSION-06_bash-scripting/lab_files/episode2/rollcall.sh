#!/usr/bin/env bash
down=0
while read -r host; do
  if ping -c1 -W1 "$host" >/dev/null 2>&1; then
    echo "UP   $host"
  else
    echo "DOWN $host"
    down=$((down + 1))
  fi
done < servers.txt
echo "Not answering: $down"
