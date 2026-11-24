#!/bin/bash
# READ-ONLY. Shows what the console demo has created in the lab region (account id is hidden). Changes nothing.
#   ./demo_s8_verify.sh            summary of instances, key pairs, security groups, volumes, Elastic IPs
#   ./demo_s8_verify.sh i-0abc...  also details of one instance (type, IMDS settings, SG rules, tags, user data size)
P="${AWS_PROFILE:-atithi-lab}"; R="${LAB_REGION:-ap-south-1}"; export AWS_PAGER=
a() { aws --profile "$P" --region "$R" "$@" </dev/null; }
echo "== $(date +%H:%M:%S)  region=$R"
echo "-- instances (not terminated)"
a ec2 describe-instances --filters "Name=instance-state-name,Values=pending,running,stopping,stopped" \
  --query "Reservations[].Instances[].[InstanceId,InstanceType,State.Name,PublicIpAddress||'-',Tags[?Key=='Name']|[0].Value||'-']" --output text
echo "-- key pairs";       a ec2 describe-key-pairs --query "KeyPairs[].[KeyName,KeyType]" --output text
echo "-- security groups (non-default)"
a ec2 describe-security-groups --query "SecurityGroups[?GroupName!='default'].[GroupId,GroupName]" --output text
echo "-- volumes";         a ec2 describe-volumes --query "Volumes[].[VolumeId,Size,VolumeType,State]" --output text
echo "-- elastic IPs";     a ec2 describe-addresses --query "Addresses[].[PublicIp,InstanceId||'unattached']" --output text
if [ -n "${1:-}" ]; then
  echo "== detail $1"
  a ec2 describe-instances --instance-ids "$1" --query "Reservations[0].Instances[0].{type:InstanceType,ami:ImageId,az:Placement.AvailabilityZone,state:State.Name,key:KeyName,imds:MetadataOptions,publicIp:PublicIpAddress,tags:Tags,sgs:SecurityGroups[].GroupName,profile:IamInstanceProfile.Arn||'none',ebsOptimized:EbsOptimized,monitoring:Monitoring.State}" --output json | sed -E 's/[0-9]{12}/ACCOUNT/g'
  for g in $(a ec2 describe-instances --instance-ids "$1" --query "Reservations[0].Instances[0].SecurityGroups[].GroupId" --output text); do
    echo "-- inbound rules of $g"; a ec2 describe-security-groups --group-ids $g --query "SecurityGroups[0].IpPermissions[].[IpProtocol,FromPort,ToPort,IpRanges[].CidrIp|join(',',@)]" --output text; done
  echo "-- user data bytes: $(a ec2 describe-instance-attribute --instance-id "$1" --attribute userData --query 'UserData.Value' --output text | base64 --decode 2>/dev/null | wc -c | tr -d ' ')"
  echo "-- volumes of it"; a ec2 describe-volumes --filters "Name=attachment.instance-id,Values=$1" --query "Volumes[].[VolumeId,Size,VolumeType,Encrypted,DeleteOnTermination||'?']" --output text
fi
