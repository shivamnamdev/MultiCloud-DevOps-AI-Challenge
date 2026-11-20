#!/bin/bash
# Deletes lab resources that are TAGGED Project=atithi-lab (or named atithi-*). Shows a plan first and changes
# nothing unless you pass --yes.   ./aws_cleanup_atithi.sh          (plan only)
#                                  ./aws_cleanup_atithi.sh --yes    (really delete)
# Handles today: Auto Scaling groups and launch templates, load balancers (+listeners) and target groups, EC2 instances,
# Elastic IPs, EBS volumes, EBS snapshots, AMIs, key pairs, security groups, IAM roles/instance profiles/policies atithi-*.
# NOT handled yet (added when each session's lab has been tested): NAT gateways, RDS, Lambda, alarms, topics, S3,
# CloudFront, VPCs. aws_leftovers.sh lists those if they exist.
set -u
P="${AWS_PROFILE:-atithi-lab}"; R="${LAB_REGION:-ap-south-1}"
export AWS_PAGER=
a() { aws --profile "$P" --region "$R" "$@"; }
YES=0; [ "${1:-}" = "--yes" ] && YES=1
TAG="Name=tag:Project,Values=atithi-lab"
say() { if [ $YES -eq 1 ]; then echo "DELETE  $*"; else echo "would delete  $*"; fi; }
echo "== Cleanup ($([ $YES -eq 1 ] && echo REAL || echo PLAN ONLY)): profile=$P region=$R"
for g in $(a autoscaling describe-auto-scaling-groups --query "AutoScalingGroups[?starts_with(AutoScalingGroupName,'atithi-')].AutoScalingGroupName" --output text); do
  say "auto scaling group $g (with its instances)"; [ $YES -eq 1 ] && a autoscaling delete-auto-scaling-group --auto-scaling-group-name $g --force-delete
done
for lb in $(a elbv2 describe-load-balancers --query "LoadBalancers[?starts_with(LoadBalancerName,'atithi-')].LoadBalancerArn" --output text); do
  say "load balancer $lb"; [ $YES -eq 1 ] && a elbv2 delete-load-balancer --load-balancer-arn $lb
done
[ $YES -eq 1 ] && sleep 20
for tg in $(a elbv2 describe-target-groups --query "TargetGroups[?starts_with(TargetGroupName,'atithi-')].TargetGroupArn" --output text); do
  say "target group $tg"; [ $YES -eq 1 ] && a elbv2 delete-target-group --target-group-arn $tg
done
for lt in $(a ec2 describe-launch-templates --query "LaunchTemplates[?starts_with(LaunchTemplateName,'atithi-')].LaunchTemplateId" --output text); do
  say "launch template $lt"; [ $YES -eq 1 ] && a ec2 delete-launch-template --launch-template-id $lt >/dev/null
done
IDS=$(a ec2 describe-instances --filters "$TAG" Name=instance-state-name,Values=pending,running,stopping,stopped --query 'Reservations[].Instances[].InstanceId' --output text)
for i in $IDS; do say "instance $i"; done
[ $YES -eq 1 ] && [ -n "$IDS" ] && { a ec2 terminate-instances --instance-ids $IDS >/dev/null; echo "waiting for termination..."; a ec2 wait instance-terminated --instance-ids $IDS; }
for al in $(a ec2 describe-addresses --filters "$TAG" --query 'Addresses[].AllocationId' --output text); do
  say "elastic IP $al"; [ $YES -eq 1 ] && { a ec2 disassociate-address --association-id "$(a ec2 describe-addresses --allocation-ids $al --query 'Addresses[0].AssociationId' --output text | sed 's/^None$//')" >/dev/null 2>&1; a ec2 release-address --allocation-id $al; }
done
for v in $(a ec2 describe-volumes --filters "$TAG" Name=status,Values=available --query 'Volumes[].VolumeId' --output text); do say "volume $v"; [ $YES -eq 1 ] && a ec2 delete-volume --volume-id $v; done
for m in $(a ec2 describe-images --owners self --filters "$TAG" --query 'Images[].ImageId' --output text); do say "AMI $m (deregister; its snapshot is deleted below)"; [ $YES -eq 1 ] && a ec2 deregister-image --image-id $m; done
for s in $(a ec2 describe-snapshots --owner-ids self --filters "$TAG" --query 'Snapshots[].SnapshotId' --output text); do say "snapshot $s"; [ $YES -eq 1 ] && a ec2 delete-snapshot --snapshot-id $s; done
for k in $(a ec2 describe-key-pairs --query "KeyPairs[?starts_with(KeyName,'atithi-')].KeyName" --output text); do say "key pair $k"; [ $YES -eq 1 ] && a ec2 delete-key-pair --key-name $k >/dev/null; done
# Two passes: one security group may be named in another group's rule (alb-sg in web-sg), so the first pass can fail for it.
for pass in 1 2; do
  for g in $(a ec2 describe-security-groups --query "SecurityGroups[?starts_with(GroupName,'atithi-')].GroupId" --output text); do
    [ $pass -eq 1 ] && say "security group $g"
    [ $YES -eq 1 ] && a ec2 delete-security-group --group-id $g >/dev/null 2>&1
  done
done
for ip in $(a iam list-instance-profiles --query "InstanceProfiles[?starts_with(InstanceProfileName,'atithi-')].InstanceProfileName" --output text); do
  say "instance profile $ip"
  [ $YES -eq 1 ] && { for r in $(a iam get-instance-profile --instance-profile-name $ip --query 'InstanceProfile.Roles[].RoleName' --output text); do a iam remove-role-from-instance-profile --instance-profile-name $ip --role-name $r; done; a iam delete-instance-profile --instance-profile-name $ip; }
done
for r in $(a iam list-roles --query "Roles[?starts_with(RoleName,'atithi-')].RoleName" --output text); do
  say "IAM role $r"
  [ $YES -eq 1 ] && { for pa in $(a iam list-attached-role-policies --role-name $r --query 'AttachedPolicies[].PolicyArn' --output text); do a iam detach-role-policy --role-name $r --policy-arn $pa; done; a iam delete-role --role-name $r; }
done
for pa in $(a iam list-policies --scope Local --query "Policies[?starts_with(PolicyName,'atithi-')].Arn" --output text); do
  say "IAM policy $pa"
  [ $YES -eq 1 ] && { for v in $(a iam list-policy-versions --policy-arn $pa --query 'Versions[?!IsDefaultVersion].VersionId' --output text); do a iam delete-policy-version --policy-arn $pa --version-id $v; done; a iam delete-policy --policy-arn $pa; }
done
echo "== Done. Now run ./aws_leftovers.sh to confirm."
