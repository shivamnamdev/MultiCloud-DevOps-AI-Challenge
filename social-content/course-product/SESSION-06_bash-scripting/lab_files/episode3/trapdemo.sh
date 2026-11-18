#!/usr/bin/env bash
set -euo pipefail
trap 'echo "cleanup ran (exit code $?)"' EXIT
echo "working"
[ "${1:-ok}" = fail ] && false
echo "finished"
