import boto3
ec2 = boto3.client("ec2")
specs = [("web1", "dev", "asha", "t3.micro"), ("web2", "dev", None, "t3.small"), ("db1", "prod", "ravi", "t3.large")]
for name, env, owner, size in specs:
    tags = [{"Key": "Name", "Value": name}, {"Key": "Env", "Value": env}]
    if owner: tags.append({"Key": "Owner", "Value": owner})
    ec2.run_instances(ImageId="ami-12345678", InstanceType=size, MinCount=1, MaxCount=1,
                      TagSpecifications=[{"ResourceType": "instance", "Tags": tags}])
print("seeded", len(specs))
