#!/bin/bash
# A stand-in for the marshal (load balancer): nginx in Docker in front of two nginx backends.
# This is NOT an AWS ALB. It shows round robin and "take the broken one out of the list".
docker network create marshalnet >/dev/null 2>&1
for n in web1 web2; do
  docker run -d --name $n --network marshalnet --hostname $n nginx:alpine sh -c \
   "echo '<h1>Atithi Hotels: Book Now</h1><p>Served by $n</p>' > /usr/share/nginx/html/index.html; exec nginx -g 'daemon off;'" >/dev/null
done
docker run -d --name marshal --network marshalnet -p 127.0.0.1:8090:80 -v "$PWD/marshal/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine >/dev/null
sleep 3
hits() { for i in 1 2 3 4 5 6; do curl -s -m 3 localhost:8090 | grep -o 'web[12]' | tr '\n' ' '; done; echo; }
echo "both up:      $(hits)"
docker stop web2 >/dev/null; echo "web2 stopped: $(hits)"
docker start web2 >/dev/null; sleep 6; echo "web2 back:    $(hits)"
docker rm -f web1 web2 marshal >/dev/null; docker network rm marshalnet >/dev/null
