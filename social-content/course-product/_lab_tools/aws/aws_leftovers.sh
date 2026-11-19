#!/bin/bash
# READ ONLY. Lists everything in the lab Region that could still be costing money, and your remaining credits.
# Run it at the end of every lab:   ./aws_leftovers.sh
# Settings (optional):  AWS_PROFILE (default atithi-lab)   LAB_REGION (default ap-south-1)
set -u
P="${AWS_PROFILE:-atithi-lab}"; R="${LAB_REGION:-ap-south-1}"
export AWS_PAGER=
a() { aws --profile "$P" --region "$R" "$@"; }
total=0
show() {  # show "title" command...   prints the lines the command returns, if any
  local title="$1"; shift
  local out; out=$("$@" 2>/dev/null | sed '/^None$/d;/^$/d')
  local n; n=$(printf '%s' "$out" | grep -c .)
  if [ "$n" -gt 0 ]; then echo "!! $title ($n)"; printf '%s\n' "$out" | sed 's/^/     /'; total=$((total + n)); fi
}
echo "== Leftover check: profile=$P region=$R  ($(date '+%Y-%m-%d %H:%M'))"
show "EC2 instances (not terminated)" a ec2 describe-instances --filters Name=instance-state-name,Values=pending,running,stopping,stopped,shutting-down --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType]' --output text
show "EBS volumes" a ec2 describe-volumes --query 'Volumes[].[VolumeId,State,Size]' --output text
show "EBS snapshots (yours)" a ec2 describe-snapshots --owner-ids self --query 'Snapshots[].[SnapshotId,VolumeSize]' --output text
show "Elastic IPs" a ec2 describe-addresses --query 'Addresses[].[AllocationId,PublicIp,InstanceId]' --output text
show "AMIs (yours)" a ec2 describe-images --owners self --query 'Images[].[ImageId,Name]' --output text
show "NAT gateways (active)" a ec2 describe-nat-gateways --filter Name=state,Values=pending,available --query 'NatGateways[].[NatGatewayId,State]' --output text
show "VPC endpoints" a ec2 describe-vpc-endpoints --query 'VpcEndpoints[].[VpcEndpointId,VpcEndpointType]' --output text
show "VPC peering connections" a ec2 describe-vpc-peering-connections --filters Name=status-code,Values=active,pending-acceptance --query 'VpcPeeringConnections[].[VpcPeeringConnectionId,Status.Code]' --output text
show "VPCs other than the default" a ec2 describe-vpcs --filters Name=is-default,Values=false --query 'Vpcs[].[VpcId,CidrBlock]' --output text
show "Security groups named atithi-*" a ec2 describe-security-groups --query "SecurityGroups[?starts_with(GroupName,'atithi-')].[GroupId,GroupName]" --output text
show "Key pairs named atithi-*" a ec2 describe-key-pairs --query "KeyPairs[?starts_with(KeyName,'atithi-')].[KeyName]" --output text
show "Launch templates" a ec2 describe-launch-templates --query 'LaunchTemplates[].[LaunchTemplateName]' --output text
show "Auto Scaling groups" a autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[].[AutoScalingGroupName,DesiredCapacity]' --output text
show "Load balancers" a elbv2 describe-load-balancers --query 'LoadBalancers[].[LoadBalancerName,Type]' --output text
show "Target groups" a elbv2 describe-target-groups --query 'TargetGroups[].[TargetGroupName]' --output text
show "RDS instances" a rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus]' --output text
show "RDS manual snapshots" a rds describe-db-snapshots --snapshot-type manual --query 'DBSnapshots[].[DBSnapshotIdentifier]' --output text
show "Lambda functions" a lambda list-functions --query 'Functions[].[FunctionName]' --output text
show "CloudWatch alarms" a cloudwatch describe-alarms --query 'MetricAlarms[].[AlarmName,StateValue]' --output text
show "SNS topics" a sns list-topics --query 'Topics[].[TopicArn]' --output text
show "SQS queues" a sqs list-queues --query 'QueueUrls' --output text
show "EventBridge rules" a events list-rules --query 'Rules[].[Name,State]' --output text
show "CloudWatch log groups" a logs describe-log-groups --query 'logGroups[].[logGroupName]' --output text
show "Secrets Manager secrets" a secretsmanager list-secrets --query 'SecretList[].[Name]' --output text
show "S3 buckets named atithi-*" a s3api list-buckets --query "Buckets[?starts_with(Name,'atithi-')].[Name]" --output text
# Only distributions whose comment starts with "atithi" (others in the account are not ours and are never listed or touched).
show "CloudFront distributions with comment atithi*" aws --profile "$P" --region us-east-1 cloudfront list-distributions --query "DistributionList.Items[?starts_with(Comment,'atithi')].[Id,Status,Enabled]" --output text
show "IAM roles named atithi-*" aws --profile "$P" iam list-roles --query "Roles[?starts_with(RoleName,'atithi-')].[RoleName]" --output text
show "IAM instance profiles named atithi-*" aws --profile "$P" iam list-instance-profiles --query "InstanceProfiles[?starts_with(InstanceProfileName,'atithi-')].[InstanceProfileName]" --output text
show "IAM customer policies named atithi-*" aws --profile "$P" iam list-policies --scope Local --query "Policies[?starts_with(PolicyName,'atithi-')].[PolicyName]" --output text
echo "-- credits:"; aws --profile "$P" --region us-east-1 freetier get-account-plan-state --query 'accountPlanRemainingCredits.[amount,unit]' --output text 2>/dev/null | sed 's/^/     remaining: /'
if [ "$total" -eq 0 ]; then echo "== NOTHING LEFT. Clean."; else echo "== $total thing(s) left. Delete them, or run ./aws_cleanup_atithi.sh (shows a plan first)."; fi
exit $(( total > 0 ))
