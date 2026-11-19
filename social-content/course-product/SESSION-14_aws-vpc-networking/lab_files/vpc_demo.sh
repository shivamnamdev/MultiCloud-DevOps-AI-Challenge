#!/bin/bash
# Session 14 on the emulator: the Atithi campus, gate, route tables, NAT, security groups and a skywalk.
# Run:  export PATH="$PWD/emulator:$PATH"; ./emulator/start.sh; ./vpc_demo.sh
set -u
V=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=atithi-vpc}]' --query Vpc.VpcId --output text)
mk() { aws ec2 create-subnet --vpc-id $V --cidr-block $1 --availability-zone $2 --query Subnet.SubnetId --output text; }
PA=$(mk 10.0.1.0/24 us-east-1a); PB=$(mk 10.0.2.0/24 us-east-1b); RA=$(mk 10.0.11.0/24 us-east-1a); RB=$(mk 10.0.12.0/24 us-east-1b)
aws ec2 describe-subnets --filters Name=vpc-id,Values=$V --query 'Subnets[].[CidrBlock,AvailabilityZone,AvailableIpAddressCount]' --output text | sort
echo "-- refused: outside the campus, overlapping, too small"
aws ec2 create-subnet --vpc-id $V --cidr-block 192.168.1.0/24 2>&1 | tail -1 | cut -c1-120
aws ec2 create-subnet --vpc-id $V --cidr-block 10.0.1.128/25 2>&1 | tail -1 | cut -c1-120
aws ec2 create-subnet --vpc-id $V --cidr-block 10.0.3.0/29 2>&1 | tail -1 | cut -c1-120
echo "-- the main gate and the public direction board"
IGW=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text); aws ec2 attach-internet-gateway --internet-gateway-id $IGW --vpc-id $V
PUB=$(aws ec2 create-route-table --vpc-id $V --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PUB --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW --query Return --output text
for s in $PA $PB; do aws ec2 associate-route-table --route-table-id $PUB --subnet-id $s --query AssociationId --output text >/dev/null; aws ec2 modify-subnet-attribute --subnet-id $s --map-public-ip-on-launch; done
aws ec2 describe-route-tables --route-table-ids $PUB --query 'RouteTables[0].Routes[].[DestinationCidrBlock,GatewayId]' --output text
echo "-- the dispatch desk (NAT) and the private direction board"
EIP=$(aws ec2 allocate-address --query AllocationId --output text)
NAT=$(aws ec2 create-nat-gateway --subnet-id $PA --allocation-id $EIP --query NatGateway.NatGatewayId --output text); sleep 3
PRV=$(aws ec2 create-route-table --vpc-id $V --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PRV --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT --query Return --output text
for s in $RA $RB; do aws ec2 associate-route-table --route-table-id $PRV --subnet-id $s --query AssociationId --output text >/dev/null; done
echo "-- door guards: gatehouse from my address, app only from the gatehouse"
BSG=$(aws ec2 create-security-group --group-name bastion-sg --description gatehouse --vpc-id $V --query GroupId --output text)
ASG=$(aws ec2 create-security-group --group-name app-sg --description app --vpc-id $V --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $BSG --protocol tcp --port 22 --cidr 203.0.113.7/32 --query 'SecurityGroupRules[0].CidrIpv4' --output text
aws ec2 authorize-security-group-ingress --group-id $ASG --protocol tcp --port 22 --source-group $BSG --query 'SecurityGroupRules[0].FromPort' --output text
echo "-- the skywalk to a second campus"
V2=$(aws ec2 create-vpc --cidr-block 10.1.0.0/16 --query Vpc.VpcId --output text)
PCX=$(aws ec2 create-vpc-peering-connection --vpc-id $V --peer-vpc-id $V2 --query VpcPeeringConnection.VpcPeeringConnectionId --output text)
aws ec2 describe-vpc-peering-connections --vpc-peering-connection-ids $PCX --query 'VpcPeeringConnections[0].Status.Code' --output text
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PCX --query 'VpcPeeringConnection.Status.Code' --output text
aws ec2 create-route --route-table-id $PRV --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PCX --query Return --output text
R2=$(aws ec2 describe-route-tables --filters Name=vpc-id,Values=$V2 --query 'RouteTables[0].RouteTableId' --output text)
aws ec2 create-route --route-table-id $R2 --destination-cidr-block 10.0.0.0/16 --vpc-peering-connection-id $PCX --query Return --output text
echo "-- delete the campus while it still has parts"
aws ec2 delete-vpc --vpc-id $V 2>&1 | tail -1 | cut -c1-140
echo "-- delete the NAT: is the Elastic IP still allocated?"
aws ec2 delete-nat-gateway --nat-gateway-id $NAT >/dev/null; sleep 2
aws ec2 describe-addresses --allocation-ids $EIP --query 'Addresses[0].[PublicIp,AssociationId]' --output text
aws ec2 release-address --allocation-id $EIP && echo "elastic IP released"
