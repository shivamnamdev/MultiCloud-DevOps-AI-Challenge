#!/bin/sh
# Rebuild content from the course notes, then start the study app.
cd "$(dirname "$0")" || exit 1
python3 tools/ingest.py && python3 tools/server.py "$@"
