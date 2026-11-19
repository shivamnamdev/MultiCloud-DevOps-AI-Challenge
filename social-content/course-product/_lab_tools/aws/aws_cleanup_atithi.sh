#!/bin/bash
# Deletes lab resources that are TAGGED Project=atithi-lab (or named atithi-*). Shows a plan first and changes
# nothing unless you pass --yes.   ./aws_cleanup_atithi.sh          (plan only)
#                                  ./aws_cleanup_atithi.sh --yes    (really delete)
# Handles today: EC2 instances, Elastic IPs, EBS volumes, EBS snapshots, AMIs, key pairs, security groups.
# NOT handled yet (added when each session's lab has been tested): NAT gateways, load balancers, Auto Scaling, RDS,
# Lambda, alarms, topics, S3, CloudFront, IAM, VPCs. aws_leftovers.sh lists those if they exist.
set -u
P="${AWS_PROFILE:-atithi-lab}"; R="${LAB_REGION:-ap-south-1}"
export AWS_PAGER=
a() { aws --profile "$P" --region "$R" "$@"; }
YES=0; [ "${1:-}" = "--yes" ] && YES=1
TAG="Name=tag:Project,Values=atithi-lab"
say() { if [ $YES -eq 1 ]; then echo "DELETE  $*"; else echo "would delete  $*"; fi; }
echo "== Cleanup ($([ $YES -eq 1 ] && echo REAL || echo PLAN ONLY)): profile=$P region=$R"
IDS=$(a ec2 describe-instances --filters "$TAG" Name=instance-state-name,Values=pending,running,stopping,stopped --query 'Reservations[].Instances[].InstanceId' --output text)
for i in $IDS; do say "instance $i"; done
[ $YES -eq 1 ] && [ -n "$IDS" ] && { a ec2 terminate-instances --instance-ids $IDS >/dev/null; echo "waiting for termination..."; a ec2 wait instance-terminated --instance-ids $IDS; }
for al in $(a ec2 describe-addresses --filters "$TAG" --query 'Addresses[].AllocationId' --output text); do
  say "elastic IP $al"; [ $YES -eq 1 ] && { a ec2 disassociate-address --association-id "$(a ec2 describe-addresses --allocation-ids $al --query 'Addresses[0].AssociationId' --output text | sed 's/^None$//')" >/dev/null 2>&1; a ec2 release-address --allocation-id $al; }
done
for v in $(a ec2 describe-volumes --filters "$TAG" Name=status,Values=available --query 'Volumes[].VolumeId' --output text); do say "volume $v"; [ $YES -eq 1 ] && a ec2 delete-volume --volume-id $v; done
for s in $(a ec2 describe-snapshots --owner-ids self --filters "$TAG" --query 'Snapshots[].SnapshotId' --output text); do say "snapshot $s"; [ $YES -eq 1 ] && a ec2 delete-snapshot --snapshot-id $s; done
for m in $(a ec2 describe-images --owners self --filters "$TAG" --query 'Images[].ImageId' --output text); do say "AMI $m (deregister; delete its snapshot next run)"; [ $YES -eq 1 ] && a ec2 deregister-image --image-id $m; done
for k in $(a ec2 describe-key-pairs --query "KeyPairs[?starts_with(KeyName,'atithi-')].KeyName" --output text); do say "key pair $k"; [ $YES -eq 1 ] && a ec2 delete-key-pair --key-name $k >/dev/null; done
for g in $(a ec2 describe-security-groups --query "SecurityGroups[?starts_with(GroupName,'atithi-')].GroupId" --output text); do say "security group $g"; [ $YES -eq 1 ] && a ec2 delete-security-group --group-id $g; done
echo "== Done. Now run ./aws_leftovers.sh to confirm."
