#!/bin/bash
# The gatehouse (bastion) idea with real SSH, in Docker. Three machines:
#   laptop  : on the public network only
#   bastion : on the public AND the private network (the gatehouse)
#   app     : on the private network only (no route from the laptop)
# Needs the image from Session 6: docker build -t atithi-ubuntu:lab -f ../../SESSION-06_bash-scripting/lab_files/Dockerfile.ubuntu ../../SESSION-06_bash-scripting/lab_files
set -u
docker network create pubnet >/dev/null 2>&1; docker network create privnet >/dev/null 2>&1
for n in bastion app; do
  docker run -d --name $n --hostname $n --privileged --tmpfs /run --tmpfs /run/lock --network $( [ $n = app ] && echo privnet || echo pubnet ) atithi-ubuntu:lab >/dev/null
done
docker network connect privnet bastion
docker run -d --name laptop --hostname laptop --network pubnet atithi-ubuntu:lab sleep infinity >/dev/null
sleep 8
docker exec -u ubuntu laptop ssh-keygen -q -t ed25519 -N "" -f /home/ubuntu/atithi.pem
PUB=$(docker exec -u ubuntu laptop cat /home/ubuntu/atithi.pem.pub)
for n in bastion app; do
  docker exec -u ubuntu $n bash -c "mkdir -p ~/.ssh && echo '$PUB' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
done
O="-o StrictHostKeyChecking=no -o LogLevel=ERROR -o BatchMode=yes -o ConnectTimeout=4 -i /home/ubuntu/atithi.pem"
L() { docker exec -u ubuntu laptop "$@"; }
echo "1) laptop to the gatehouse:"; L ssh $O ubuntu@bastion 'echo "in the gatehouse: $(hostname)"'
echo "2) laptop straight to the private building:"; L ssh $O ubuntu@app hostname 2>&1 | tail -1
echo "3a) the script's command: -i key plus -J (the key is NOT offered to the gatehouse hop):"; L ssh $O -J ubuntu@bastion ubuntu@app 'echo "in the private building: $(hostname)"' 2>&1 | tail -1
echo "3b) the key given to both hops with a config file:"
docker exec -u ubuntu laptop bash -c 'cat > ~/.ssh/config <<CFG
Host bastion app
  User ubuntu
  IdentityFile ~/atithi.pem
  IdentitiesOnly yes
  StrictHostKeyChecking no
  LogLevel ERROR
Host app
  ProxyJump bastion
CFG
chmod 600 ~/.ssh/config'
L ssh -o BatchMode=yes app 'echo "in the private building: $(hostname)"'
echo "3c) -J with an agent that holds the key:"
L bash -c 'eval $(ssh-agent -s) >/dev/null; ssh-add ~/atithi.pem 2>&1 | tail -1; ssh -F /dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR -o BatchMode=yes -J ubuntu@bastion ubuntu@app "echo in the private building: \$(hostname)"'
echo "4) is the key on the gatehouse?"; docker exec -u ubuntu bastion bash -c 'ls ~/.ssh; ls ~/*.pem 2>&1 | tail -1'
echo "5) the gatehouse is the only road: stop it"; docker stop bastion >/dev/null
L ssh -o BatchMode=yes app hostname 2>&1 | tail -1
docker rm -f bastion app laptop >/dev/null; docker network rm pubnet privnet >/dev/null
