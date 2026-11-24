#!/bin/bash
# Deletes lab resources that start with "atithi" in the lab project. PLANS FIRST: nothing is deleted without --yes.
#   ./gcp_cleanup_atithi.sh          shows what would be deleted
#   ./gcp_cleanup_atithi.sh --yes    deletes it, then runs gcp_leftovers.sh
# Touches only: GKE clusters, Artifact Registry repos, Cloud Run services and storage buckets whose name starts with "atithi".
# Settings (optional):  LAB_PROJECT (default: your gcloud project)   LAB_REGION (default asia-south1)
set -u
G="${GCLOUD:-gcloud}"
P="${LAB_PROJECT:-$($G config get-value project 2>/dev/null)}"; R="${LAB_REGION:-asia-south1}"
[ -n "$P" ] || { echo "No project set. Run: gcloud config set project PROJECT_ID"; exit 2; }
YES=0; [ "${1:-}" = "--yes" ] && YES=1
HERE="$(cd "$(dirname "$0")" && pwd)"
echo "== GCP cleanup ($( [ $YES = 1 ] && echo DELETE || echo PLAN only )): project=$P"
n=0
act() {  # act "what" command...
  local what="$1"; shift
  n=$((n + 1)); echo " - $what"
  if [ "$YES" = 1 ]; then "$@" </dev/null 2>&1 | grep -vi warning | tail -2 | sed 's/^/     /'; fi
}
# Clusters first: deleting a cluster also removes its load balancers and disks.
for line in $($G container clusters list --project "$P" --filter="name~^atithi" --format="value(name,location)" 2>/dev/null </dev/null | tr '\t' ','); do
  c="${line%%,*}"; l="${line##*,}"
  act "GKE cluster $c ($l)" $G container clusters delete "$c" --location "$l" --project "$P" --quiet
done
# The JSON format keeps the full path: projects/P/locations/L/repositories/NAME
for line in $($G artifacts repositories list --project "$P" --filter="name~/atithi" --format="json(name)" 2>/dev/null </dev/null | grep '"name"' | cut -d'"' -f4); do
  l=$(echo "$line" | cut -d/ -f4); r=$(echo "$line" | cut -d/ -f6)
  act "Artifact Registry repo $r ($l)" $G artifacts repositories delete "$r" --location "$l" --project "$P" --quiet
done
for s in $($G run services list --project "$P" --filter="metadata.name~^atithi" --format="value(metadata.name,region)" 2>/dev/null </dev/null | tr '\t' ','); do
  act "Cloud Run service ${s%%,*}" $G run services delete "${s%%,*}" --region "${s##*,}" --project "$P" --quiet
done
for b in $($G storage buckets list --project "$P" --filter="name~^atithi" --format="value(storage_url)" 2>/dev/null </dev/null); do
  act "Storage bucket $b (and its objects)" $G storage rm -r "$b" --project "$P"
done
if [ "$n" -eq 0 ]; then echo " nothing named atithi* to delete."; fi
if [ "$YES" = 1 ]; then echo; "$HERE/gcp_leftovers.sh"; else [ "$n" -gt 0 ] && echo && echo "Nothing was deleted. Run again with --yes to delete the items above."; fi
