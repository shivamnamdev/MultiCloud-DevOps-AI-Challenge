#!/bin/bash
# Session 11 on the emulator: target group, load balancer, listener, target health, ASG attached to the group.
set -u
VPC=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
S1=$(aws ec2 describe-subnets --query 'Subnets[0].SubnetId' --output text)
S2=$(aws ec2 describe-subnets --query 'Subnets[1].SubnetId' --output text)
SGA=$(aws ec2 create-security-group --group-name alb-sg --description marshal --vpc-id $VPC --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $SGA --protocol tcp --port 80 --cidr 0.0.0.0/0 >/dev/null
TG=$(aws elbv2 create-target-group --name web-tg --protocol HTTP --port 80 --vpc-id $VPC --health-check-path / --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 describe-target-groups --names web-tg --query 'TargetGroups[0].[HealthCheckProtocol,HealthCheckPath,HealthyThresholdCount,UnhealthyThresholdCount,HealthCheckIntervalSeconds]' --output text
I1=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --subnet-id $S1 --query 'Instances[0].InstanceId' --output text)
I2=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --subnet-id $S2 --query 'Instances[0].InstanceId' --output text)
aws elbv2 register-targets --target-group-arn $TG --targets Id=$I1 Id=$I2 && echo "registered 2"
LB=$(aws elbv2 create-load-balancer --name atithi-alb --subnets $S1 $S2 --security-groups $SGA --scheme internet-facing --type application --query 'LoadBalancers[0].LoadBalancerArn' --output text)
aws elbv2 describe-load-balancers --names atithi-alb --query 'LoadBalancers[0].[Type,Scheme,State.Code,length(AvailabilityZones)]' --output text
aws elbv2 create-listener --load-balancer-arn $LB --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$TG --query 'Listeners[0].[Port,Protocol]' --output text
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[TargetHealth.State]' --output text | tr '\n' ' '; echo "(right after creating)"
sleep 40
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[TargetHealth.State,TargetHealth.Reason]' --output text
echo "== an Auto Scaling group attached to the target group, health check type ELB"
aws ec2 create-launch-template --launch-template-name atithi-web --launch-template-data '{"ImageId":"ami-ubuntu2404-arm64","InstanceType":"t4g.micro"}' >/dev/null
SUBS=$(aws ec2 describe-subnets --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')
aws autoscaling create-auto-scaling-group --auto-scaling-group-name web-asg --launch-template LaunchTemplateName=atithi-web,Version='$Latest' \
  --min-size 2 --max-size 4 --desired-capacity 2 --vpc-zone-identifier "$SUBS" --target-group-arns $TG --health-check-type ELB --health-check-grace-period 120
sleep 8
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names web-asg --query 'AutoScalingGroups[0].[HealthCheckType,HealthCheckGracePeriod]' --output text
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names web-asg --query 'AutoScalingGroups[0].Instances[].[InstanceId,LifecycleState,HealthStatus]' --output text
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State,TargetHealth.Reason]' --output text
echo "== clean up, in the script's order: ASG, load balancer, target group"
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg --min-size 0 --desired-capacity 0; sleep 5
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name web-asg && echo "ASG deleted"
L=$(aws elbv2 describe-listeners --load-balancer-arn $LB --query 'Listeners[0].ListenerArn' --output text)
aws elbv2 delete-listener --listener-arn $L; aws elbv2 delete-load-balancer --load-balancer-arn $LB && echo "ALB deleted"
aws elbv2 delete-target-group --target-group-arn $TG && echo "target group deleted"
aws ec2 delete-launch-template --launch-template-name atithi-web >/dev/null
aws ec2 terminate-instances --instance-ids $I1 $I2 >/dev/null; echo done
