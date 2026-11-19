#!/bin/bash
# Session 13 on the emulator: the managed ledger's settings, secret, protection, replica. No real database runs behind it.
# Run:  export PATH="$PWD/emulator:$PATH"; ./emulator/start.sh; ./rds_demo.sh
set -u
VPC=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
BSG=$(aws ec2 create-security-group --group-name booking-sg --description booking --vpc-id $VPC --query GroupId --output text)
DSG=$(aws ec2 create-security-group --group-name db-sg --description "records office door" --vpc-id $VPC --query GroupId --output text)
echo "-- db-sg lets 5432 in only from booking-sg:"
aws ec2 authorize-security-group-ingress --group-id $DSG --protocol tcp --port 5432 --source-group $BSG --query 'SecurityGroupRules[0].[FromPort,ReferencedGroupInfo.GroupId]' --output text | sed "s/$BSG/<booking-sg>/"
aws rds create-db-instance --db-instance-identifier atithi-ledger --db-instance-class db.t4g.micro --engine postgres \
  --master-username atithi_admin --manage-master-user-password --allocated-storage 20 --no-publicly-accessible \
  --vpc-security-group-ids $DSG --backup-retention-period 7 --deletion-protection \
  --query 'DBInstance.[DBInstanceStatus,Engine,PubliclyAccessible,DeletionProtection,BackupRetentionPeriod]' --output text
sleep 5
aws rds describe-db-instances --db-instance-identifier atithi-ledger --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address,Endpoint.Port,MultiAZ,StorageEncrypted]' --output text
ARN=$(aws rds describe-db-instances --db-instance-identifier atithi-ledger --query 'DBInstances[0].MasterUserSecret.SecretArn' --output text)
echo "-- the managed password lives in Secrets Manager (password hidden here):"
aws secretsmanager get-secret-value --secret-id "$ARN" --query SecretString --output text | python3 -c "import sys,json; d=json.load(sys.stdin); print({k:('***' if k=='password' else v) for k,v in d.items()})"
echo "-- a read replica record, and deletion protection:"
aws rds create-db-instance-read-replica --db-instance-identifier atithi-ledger-ro --source-db-instance-identifier atithi-ledger --query 'DBInstance.[DBInstanceIdentifier,ReadReplicaSourceDBInstanceIdentifier]' --output text
aws rds delete-db-instance --db-instance-identifier atithi-ledger --skip-final-snapshot 2>&1 | tail -1 | cut -c1-200
aws rds modify-db-instance --db-instance-identifier atithi-ledger --no-deletion-protection >/dev/null
aws rds delete-db-instance --db-instance-identifier atithi-ledger-ro --skip-final-snapshot --query 'DBInstance.DBInstanceStatus' --output text
aws rds delete-db-instance --db-instance-identifier atithi-ledger --skip-final-snapshot --query 'DBInstance.DBInstanceStatus' --output text
