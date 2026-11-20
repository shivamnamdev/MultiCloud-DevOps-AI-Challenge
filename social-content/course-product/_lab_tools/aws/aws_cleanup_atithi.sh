#!/bin/bash
# Deletes lab resources that are TAGGED Project=atithi-lab (or named atithi-*). Shows a plan first and changes
# nothing unless you pass --yes.   ./aws_cleanup_atithi.sh          (plan only)
#                                  ./aws_cleanup_atithi.sh --yes    (really delete)
# PROTECTED: any IAM user, group, role or policy whose name starts with atithi-lab (your lab user, its group, its policies).
# Handles today: EventBridge rules, S3 buckets (all versions), Lambda, alarms, SNS, SQS, log groups, CloudFront (disable, then delete on a second run), Auto Scaling groups and launch templates, load balancers (+listeners) and target groups, EC2 instances,
# Elastic IPs, EBS volumes, EBS snapshots, AMIs, key pairs, security groups, IAM users/groups/roles/instance profiles/policies atithi-*.
# NOT handled yet (added when each session's lab has been tested): NAT gateways, RDS, VPCs. aws_leftovers.sh lists those if they exist.
set -u
P="${AWS_PROFILE:-atithi-lab}"; R="${LAB_REGION:-ap-south-1}"
export AWS_PAGER=
a() { aws --profile "$P" --region "$R" "$@"; }
YES=0; [ "${1:-}" = "--yes" ] && YES=1
TAG="Name=tag:Project,Values=atithi-lab"
say() { if [ $YES -eq 1 ]; then echo "DELETE  $*"; else echo "would delete  $*"; fi; }
echo "== Cleanup ($([ $YES -eq 1 ] && echo REAL || echo PLAN ONLY)): profile=$P region=$R"
# --- Session 12/15 resources: schedules first (they keep firing), then triggers, functions, alarms, topics, queues, logs, S3, CloudFront
for r in $(a events list-rules --name-prefix atithi- --query 'Rules[].Name' --output text); do
  say "EventBridge rule $r"
  [ $YES -eq 1 ] && { ids=$(a events list-targets-by-rule --rule $r --query 'Targets[].Id' --output text); [ -n "$ids" ] && a events remove-targets --rule $r --ids $ids >/dev/null; a events delete-rule --name $r; }
done
for b in $(a s3api list-buckets --query "Buckets[?starts_with(Name,'atithi-')].Name" --output text); do
  say "S3 bucket $b (every version and delete marker, then the bucket)"
  [ $YES -eq 1 ] && {
    a s3api put-bucket-notification-configuration --bucket $b --notification-configuration '{}' >/dev/null 2>&1
    for kind in Versions DeleteMarkers; do
      while :; do
        a s3api list-object-versions --bucket $b --max-items 500 --query "{Objects: ${kind}[].{Key:Key,VersionId:VersionId}, Quiet: \`true\`}" --output json > /tmp/.atithi-del.json 2>/dev/null
        python3 -c "import json,sys;d=json.load(open('/tmp/.atithi-del.json'));sys.exit(0 if d.get('Objects') else 1)" || break
        a s3api delete-objects --bucket $b --delete file:///tmp/.atithi-del.json >/dev/null
      done
    done
    rm -f /tmp/.atithi-del.json; a s3 rb s3://$b; }
done
for fn in $(a lambda list-functions --query "Functions[?starts_with(FunctionName,'atithi-')].FunctionName" --output text); do say "Lambda function $fn"; [ $YES -eq 1 ] && a lambda delete-function --function-name $fn; done
for al in $(a cloudwatch describe-alarms --alarm-name-prefix atithi- --query 'MetricAlarms[].AlarmName' --output text); do say "alarm $al"; [ $YES -eq 1 ] && a cloudwatch delete-alarms --alarm-names $al; done
for t in $(a sns list-topics --query "Topics[?contains(TopicArn,':atithi-')].TopicArn" --output text); do say "SNS topic $t"; [ $YES -eq 1 ] && a sns delete-topic --topic-arn $t; done
for q in $(a sqs list-queues --queue-name-prefix atithi- --query 'QueueUrls[]' --output text); do say "SQS queue $q"; [ $YES -eq 1 ] && a sqs delete-queue --queue-url $q; done
for lg in $(a logs describe-log-groups --log-group-name-prefix /atithi/ --query 'logGroups[].logGroupName' --output text) $(a logs describe-log-groups --log-group-name-prefix /aws/lambda/atithi- --query 'logGroups[].logGroupName' --output text); do say "log group $lg"; [ $YES -eq 1 ] && a logs delete-log-group --log-group-name $lg; done
# CloudFront: only distributions whose Comment starts with "atithi". Disable first; deleting needs it to be Deployed+disabled (a few minutes): run again.
for d in $(a cloudfront list-distributions --query "DistributionList.Items[?starts_with(Comment,'atithi')].Id" --output text 2>/dev/null | tr '\t' '\n' | grep -v '^None$'); do
  en=$(a cloudfront get-distribution --id $d --query 'Distribution.DistributionConfig.Enabled' --output text); stt=$(a cloudfront get-distribution --id $d --query 'Distribution.Status' --output text)
  if [ "$en" = "True" ]; then say "CloudFront distribution $d (disable now; run again in ~5 min to delete)"
    [ $YES -eq 1 ] && { a cloudfront get-distribution-config --id $d --output json > /tmp/.atithi-cf.json; et=$(python3 -c "import json;print(json.load(open('/tmp/.atithi-cf.json'))['ETag'])"); python3 -c "import json;d=json.load(open('/tmp/.atithi-cf.json'))['DistributionConfig'];d['Enabled']=False;json.dump(d,open('/tmp/.atithi-cf-off.json','w'))"; a cloudfront update-distribution --id $d --if-match $et --distribution-config file:///tmp/.atithi-cf-off.json >/dev/null; rm -f /tmp/.atithi-cf*.json; }
  elif [ "$stt" = "Deployed" ]; then say "CloudFront distribution $d (delete)"; [ $YES -eq 1 ] && a cloudfront delete-distribution --id $d --if-match "$(a cloudfront get-distribution --id $d --query ETag --output text)"
  else echo "CloudFront distribution $d is still updating; run again in a few minutes"; fi
done
for o in $(a cloudfront list-origin-access-controls --query "OriginAccessControlList.Items[?starts_with(Name,'atithi-')].Id" --output text 2>/dev/null | tr '\t' '\n' | grep -v '^None$'); do say "CloudFront origin access control $o"; [ $YES -eq 1 ] && a cloudfront delete-origin-access-control --id $o --if-match "$(a cloudfront get-origin-access-control --id $o --query ETag --output text)" 2>&1 | tail -1; done
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
for r in $(a iam list-roles --query "Roles[?starts_with(RoleName,'atithi-') && !starts_with(RoleName,'atithi-lab')].RoleName" --output text); do
  say "IAM role $r"
  [ $YES -eq 1 ] && { for pa in $(a iam list-attached-role-policies --role-name $r --query 'AttachedPolicies[].PolicyArn' --output text); do a iam detach-role-policy --role-name $r --policy-arn $pa; done; a iam delete-role --role-name $r; }
done
for u in $(a iam list-users --query "Users[?starts_with(UserName,'atithi-') && !starts_with(UserName,'atithi-lab')].UserName" --output text); do
  say "IAM user $u (keys, password, policies, group memberships)"
  [ $YES -eq 1 ] && {
    for k in $(a iam list-access-keys --user-name $u --query 'AccessKeyMetadata[].AccessKeyId' --output text); do a iam delete-access-key --user-name $u --access-key-id $k; done
    a iam delete-login-profile --user-name $u >/dev/null 2>&1
    for pa in $(a iam list-attached-user-policies --user-name $u --query 'AttachedPolicies[].PolicyArn' --output text); do a iam detach-user-policy --user-name $u --policy-arn $pa; done
    for gr in $(a iam list-groups-for-user --user-name $u --query 'Groups[].GroupName' --output text); do a iam remove-user-from-group --user-name $u --group-name $gr; done
    a iam delete-user --user-name $u; }
done
for gr in $(a iam list-groups --query "Groups[?starts_with(GroupName,'atithi-') && !starts_with(GroupName,'atithi-lab')].GroupName" --output text); do
  say "IAM group $gr"
  [ $YES -eq 1 ] && {
    for pa in $(a iam list-attached-group-policies --group-name $gr --query 'AttachedPolicies[].PolicyArn' --output text); do a iam detach-group-policy --group-name $gr --policy-arn $pa; done
    a iam delete-group --group-name $gr; }
done
for pa in $(a iam list-policies --scope Local --query "Policies[?starts_with(PolicyName,'atithi-') && !starts_with(PolicyName,'atithi-lab')].Arn" --output text); do
  say "IAM policy $pa"
  [ $YES -eq 1 ] && { for v in $(a iam list-policy-versions --policy-arn $pa --query 'Versions[?!IsDefaultVersion].VersionId' --output text); do a iam delete-policy-version --policy-arn $pa --version-id $v; done; a iam delete-policy --policy-arn $pa; }
done
echo "== Done. Now run ./aws_leftovers.sh to confirm."
