#!/bin/bash
# READ ONLY. Lists everything in the lab project that could still be costing money.
# Run it at the end of every lab:   ./gcp_leftovers.sh
# Settings (optional):  LAB_PROJECT (default: your gcloud project)   CLOUDSDK_ACTIVE_CONFIG_NAME
set -u
G="${GCLOUD:-gcloud}"
P="${LAB_PROJECT:-$($G config get-value project 2>/dev/null)}"
[ -n "$P" ] || { echo "No project set. Run: gcloud config set project PROJECT_ID"; exit 2; }
total=0
show() {  # show "title" command...   prints the lines the command returns, if any
  local title="$1"; shift
  local out; out=$("$@" 2>/dev/null </dev/null | sed '/^$/d')
  local n; n=$(printf '%s' "$out" | grep -c .)
  if [ "$n" -gt 0 ]; then echo "!! $title ($n)"; printf '%s\n' "$out" | sed 's/^/     /'; total=$((total + n)); fi
}
g() { $G "$@" --project "$P"; }
echo "== GCP leftover check: project=$P  ($(date '+%Y-%m-%d %H:%M'))"
show "GKE clusters" g container clusters list --format="value(name,location,status)"
show "Compute instances" g compute instances list --format="value(name,zone,status)"
show "Persistent disks" g compute disks list --format="value(name,zone,sizeGb)"
show "Load balancer forwarding rules" g compute forwarding-rules list --format="value(name,region,IPAddress)"
show "Target pools" g compute target-pools list --format="value(name,region)"
show "Backend services" g compute backend-services list --format="value(name)"
show "Health checks" g compute health-checks list --format="value(name)"
show "Reserved external IPs" g compute addresses list --format="value(name,region,address,status)"
show "Firewall rules created by GKE" g compute firewall-rules list --filter="name~^gke" --format="value(name)"
show "Cloud NAT routers" g compute routers list --format="value(name,region)"
show "VPC networks other than default" g compute networks list --filter="name!=default" --format="value(name)"
show "Disk snapshots" g compute snapshots list --format="value(name,diskSizeGb)"
show "Artifact Registry repositories" g artifacts repositories list --format="value(name)"
show "Cloud Run services" g run services list --format="value(metadata.name,metadata.namespace)"
show "Cloud SQL instances" g sql instances list --format="value(name,state)"
show "Storage buckets" g storage buckets list --format="value(name)"
show "Pub/Sub topics" g pubsub topics list --format="value(name)"
show "Secret Manager secrets" g secrets list --format="value(name)"
if [ "$total" -eq 0 ]; then echo "OK: nothing that bills was found in project $P."; else echo "Found $total item(s) above. Delete what you do not need; check billing in the console."; fi
echo "Note: the 'default' VPC network, its default firewall rules, and enabled APIs are free and are not listed."
