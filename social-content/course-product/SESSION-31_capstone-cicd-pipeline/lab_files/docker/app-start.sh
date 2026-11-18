#!/bin/sh
# Put Jenkins' public key where the SSH door expects it, start SSH, then run Docker's engine in the foreground.
set -e
install -o ubuntu -g docker -m 600 /keys/app_key.pub /home/ubuntu/.ssh/authorized_keys
/usr/sbin/sshd
exec dockerd-entrypoint.sh --insecure-registry registry:5000
