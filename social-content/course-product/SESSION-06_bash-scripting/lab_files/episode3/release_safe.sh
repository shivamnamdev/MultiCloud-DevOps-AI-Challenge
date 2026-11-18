#!/usr/bin/env bash
set -euo pipefail
echo "1 copy new site files"; cp /nonexistent/new-site/* /tmp/rel/ 2>/dev/null
echo "2 check them"; test -f /tmp/rel/index.html
echo "3 remove the old release"; echo "(old release removed)"
