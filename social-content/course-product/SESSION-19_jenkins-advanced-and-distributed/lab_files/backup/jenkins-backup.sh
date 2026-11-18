#!/usr/bin/env bash
# Back up Jenkins' home folder to S3. Run as a user that can read JENKINS_HOME.
# Real server:  JENKINS_HOME=/var/lib/jenkins BUCKET=your-backup-bucket ./jenkins-backup.sh   (use sudo for tar if needed)
# Practice:     JENKINS_HOME=/var/jenkins_home BUCKET=jenkins-backups ENDPOINT="--endpoint-url http://floci:4566" ./jenkins-backup.sh
set -euo pipefail
: "${JENKINS_HOME:?set JENKINS_HOME}"
: "${BUCKET:?set BUCKET}"
ts=$(date +%Y%m%d-%H%M)
file="/tmp/jenkins-$ts.tgz"
tar --exclude='workspace' --exclude='caches' -czf "$file" -C "$(dirname "$JENKINS_HOME")" "$(basename "$JENKINS_HOME")"
# shellcheck disable=SC2086
aws ${ENDPOINT:-} s3 cp "$file" "s3://$BUCKET/jenkins/" --sse AES256
rm -f "$file"
echo "backup done: $ts"
