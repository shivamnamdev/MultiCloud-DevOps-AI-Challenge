#!/bin/sh
# Install the public key Jenkins will use (mounted at /keys/agent_key.pub), then run the SSH server.
set -e
install -o jenkins -g jenkins -m 600 /keys/agent_key.pub /home/jenkins/.ssh/authorized_keys
exec /usr/sbin/sshd -D -e
