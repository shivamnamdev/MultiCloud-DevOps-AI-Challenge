# The "app building": a host with its own Docker engine, an SSH door, sudo and curl. Practice only.
FROM docker:27-dind
RUN apk upgrade --no-cache && apk add --no-cache openssh bash curl sudo shadow
RUN ssh-keygen -A
# A locked account would make SSH refuse key logins, so give "ubuntu" an unused password (the door accepts keys only).
RUN adduser -D -s /bin/bash -G docker ubuntu && echo 'ubuntu:unused-password-123' | chpasswd
RUN echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu
RUN printf 'PasswordAuthentication no\nPubkeyAuthentication yes\n' > /etc/ssh/sshd_config.d/10-lab.conf
RUN mkdir -p /home/ubuntu/.ssh && chmod 700 /home/ubuntu/.ssh && chown ubuntu:docker /home/ubuntu/.ssh
RUN touch /var/log/atithi-deploys.log && chmod 666 /var/log/atithi-deploys.log
COPY app-start.sh /usr/local/bin/app-start.sh
RUN chmod +x /usr/local/bin/app-start.sh
ENTRYPOINT ["/usr/local/bin/app-start.sh"]
