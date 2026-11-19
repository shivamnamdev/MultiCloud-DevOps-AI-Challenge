#!/bin/bash
# Session 10 on the emulator: volumes, the same-tower rule, launch template, Auto Scaling group.
# Run:  export PATH="$PWD/emulator:$PATH"; ./emulator/start.sh; ./ebs_asg_demo.sh
set -u
I=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --query 'Instances[0].InstanceId' --output text)
AZ=$(aws ec2 describe-instances --instance-ids $I --query 'Reservations[0].Instances[0].Placement.AvailabilityZone' --output text)
OTHER=$(aws ec2 describe-availability-zones --query "AvailabilityZones[?ZoneName!='$AZ'].ZoneName | [0]" --output text)
echo "== instance $I is in $AZ; a volume in $OTHER must be refused"
V0=$(aws ec2 create-volume --volume-type gp3 --size 8 --availability-zone $OTHER --query VolumeId --output text)
aws ec2 attach-volume --volume-id $V0 --instance-id $I --device /dev/sdf 2>&1 | tail -1 | cut -c1-170
aws ec2 delete-volume --volume-id $V0
echo "== a volume in the same tower"
V=$(aws ec2 create-volume --volume-type gp3 --size 8 --availability-zone $AZ --query VolumeId --output text)
aws ec2 attach-volume --volume-id $V --instance-id $I --device /dev/sdf --query State --output text
sleep 1
aws ec2 describe-volumes --volume-ids $V --query 'Volumes[0].[State,Attachments[0].Device]' --output text
echo "== launch template and Auto Scaling group (min 1, max 3)"
aws ec2 create-launch-template --launch-template-name atithi-web \
  --launch-template-data '{"ImageId":"ami-ubuntu2404-arm64","InstanceType":"t4g.micro"}' --query LaunchTemplate.LaunchTemplateId --output text
SUBS=$(aws ec2 describe-subnets --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')
aws autoscaling create-auto-scaling-group --auto-scaling-group-name atithi-asg \
  --launch-template LaunchTemplateName=atithi-web,Version='$Latest' --min-size 1 --max-size 3 --desired-capacity 1 --vpc-zone-identifier "$SUBS"
sleep 3
show() { aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names atithi-asg --query 'AutoScalingGroups[0].Instances[].[InstanceId,LifecycleState,HealthStatus,AvailabilityZone]' --output text; }
show
aws autoscaling put-scaling-policy --auto-scaling-group-name atithi-asg --policy-name cpu40 --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":40}' --query PolicyARN --output text
echo "== desired 2, then terminate one by hand: the group makes another"
aws autoscaling set-desired-capacity --auto-scaling-group-name atithi-asg --desired-capacity 2; sleep 4; show
X=$(show | head -1 | cut -f1); aws ec2 terminate-instances --instance-ids $X --query 'TerminatingInstances[0].CurrentState.Name' --output text; sleep 20; show
echo "== above the max is refused"
aws autoscaling set-desired-capacity --auto-scaling-group-name atithi-asg --desired-capacity 5 2>&1 | tail -1 | cut -c1-150
echo "== delete: refused while it has instances, allowed after scaling to zero"
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name atithi-asg 2>&1 | tail -1 | cut -c1-170
aws autoscaling update-auto-scaling-group --auto-scaling-group-name atithi-asg --min-size 0 --desired-capacity 0; sleep 5
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name atithi-asg && echo "ASG deleted"
aws ec2 delete-launch-template --launch-template-name atithi-web --query LaunchTemplate.LaunchTemplateName --output text
aws ec2 detach-volume --volume-id $V --query State --output text; sleep 1; aws ec2 delete-volume --volume-id $V && echo "volume deleted"
aws ec2 terminate-instances --instance-ids $I --query 'TerminatingInstances[0].CurrentState.Name' --output text
