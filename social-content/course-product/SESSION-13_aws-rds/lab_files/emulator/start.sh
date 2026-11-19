#!/bin/bash
# Starts the practice AWS (the floci emulator) and a network for the AWS CLI container.
# Free, local, and NOT the real AWS. Stop it with: docker rm -f floci-lab
docker network create awslab 2>/dev/null
docker rm -f floci-lab >/dev/null 2>&1
docker run -d --name floci-lab --network awslab -p 127.0.0.1:4566:4566 floci/floci:latest
echo "Waiting for the emulator..."; sleep 5
export PATH="$(cd "$(dirname "$0")" && pwd):$PATH"
aws sts get-caller-identity
