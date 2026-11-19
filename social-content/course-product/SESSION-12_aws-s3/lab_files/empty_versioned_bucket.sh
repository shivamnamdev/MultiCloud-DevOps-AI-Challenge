#!/bin/bash
# Empties a VERSIONED bucket (every version and every delete marker), then removes it.
# `aws s3 rb --force` is not enough: it leaves versions and markers behind (BucketNotEmpty).
# (The AWS command runs in a container that sees the current folder, so the JSON files are kept here.)
# Usage: ./empty_versioned_bucket.sh BUCKET      (read the name twice: this is permanent)
set -eu
B="${1:?usage: empty_versioned_bucket.sh BUCKET}"
for kind in Versions DeleteMarkers; do
  aws s3api list-object-versions --bucket "$B" \
    --query "{Objects: ${kind}[].{Key:Key,VersionId:VersionId}, Quiet: \`true\`}" --output json > ".del-$kind.json"
  if python3 -c "import json,sys;d=json.load(open('.del-$kind.json'));sys.exit(0 if d['Objects'] else 1)"; then
    aws s3api delete-objects --bucket "$B" --delete "file://.del-$kind.json" >/dev/null
  fi
done
aws s3 rb "s3://$B"
rm -f .del-Versions.json .del-DeleteMarkers.json
