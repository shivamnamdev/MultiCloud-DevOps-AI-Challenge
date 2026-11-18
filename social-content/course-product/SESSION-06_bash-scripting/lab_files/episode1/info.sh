#!/usr/bin/env bash
host=$(hostname)
user=$(whoami)
today=$(date +%F)
echo "Building: $host | Staff: $user | Date: $today"
df -h / | tail -1
du -sh "$1"
