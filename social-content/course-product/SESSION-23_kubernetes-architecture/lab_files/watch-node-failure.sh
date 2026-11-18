#!/bin/sh
# Stops one worker node and prints, every 10 seconds, the node status and where the pods are.
# Needs: a kind cluster named lab23 made from kind-3nodes.yaml, and a Deployment named rooms.
NODE=lab23-worker2
echo "=== stopping $NODE at $(date +%T)"; T0=$(date +%s)
docker stop "$NODE" >/dev/null
i=0
while [ $i -lt 50 ]; do
  sleep 10; i=$((i+1))
  el=$(( $(date +%s) - T0 ))
  n=$(kubectl get nodes --no-headers | awk -v n="$NODE" '$1==n{print $2}')
  p=$(kubectl get pods --no-headers -o wide | awk '{printf "%s:%s:%s ", substr($1,length($1)-4), $3, $7}')
  echo "t+${el}s $NODE=$n | $p"
done
echo "=== starting $NODE again"; docker start "$NODE" >/dev/null
