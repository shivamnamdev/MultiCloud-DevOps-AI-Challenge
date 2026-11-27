#!/bin/zsh
export KUBECONFIG=./kubeconfig
cd .
log() { echo "$(date +%H:%M:%S) $*"; }
watch_for() { # seconds label
  end=$((SECONDS+$1)); last=""
  while [ $SECONDS -lt $end ]; do
    cur=$(kubectl get hpa php-apache -o jsonpath='{.status.currentReplicas}/{.status.desiredReplicas} cpu={.status.currentMetrics[0].resource.current.averageUtilization}%' 2>/dev/null)
    [ "$cur" != "$last" ] && { log "$2 $cur"; last="$cur"; }
    sleep 5
  done
}
log "== PHASE 1: default behavior"
kubectl autoscale deploy php-apache --cpu=50% --min=1 --max=6 | tail -1
kubectl run load --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
kubectl run load2 --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
watch_for 150 "load on  "
kubectl delete pod load load2 --now | tail -2; log "LOAD STOPPED"
watch_for 420 "load off "
log "== PHASE 2: scaleDown.stabilizationWindowSeconds=30"
kubectl delete hpa php-apache | tail -1
cat <<'Y' | kubectl apply -f - | tail -1
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: php-apache}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: php-apache}
  minReplicas: 1
  maxReplicas: 6
  metrics: [{type: Resource, resource: {name: cpu, target: {type: Utilization, averageUtilization: 50}}}]
  behavior:
    scaleDown: {stabilizationWindowSeconds: 30}
Y
kubectl run load --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
kubectl run load2 --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
watch_for 120 "load on  "
kubectl delete pod load load2 --now | tail -2; log "LOAD STOPPED"
watch_for 180 "load off "
log "DONE"
