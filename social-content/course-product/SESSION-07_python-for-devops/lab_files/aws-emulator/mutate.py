import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

# dev buildings only
resp = ec2.describe_instances(Filters=[{"Name": "tag:Env", "Values": ["dev"]}])
ids = [i["InstanceId"] for r in resp["Reservations"] for i in r["Instances"]]
print("dev buildings:", len(ids))

# paginator: force small pages so the pagination is visible
pages = list(ec2.get_paginator("describe_instances").paginate(PaginationConfig={"PageSize": 1}))
print("pages of size 1:", len(pages))

iid = ids[0]
print("--- DryRun create_tags")
try:
    ec2.create_tags(Resources=[iid], Tags=[{"Key": "Owner", "Value": "kiran"}], DryRun=True)
except ClientError as e:
    print("code:", e.response["Error"]["Code"])

print("--- DryRun stop_instances")
try:
    ec2.stop_instances(InstanceIds=ids, DryRun=True)
except ClientError as e:
    print("code:", e.response["Error"]["Code"])
    state = ec2.describe_instances(InstanceIds=[iid])["Reservations"][0]["Instances"][0]["State"]["Name"]
    print("state after the dry run:", state)

print("--- real stop plus waiter")
ec2.stop_instances(InstanceIds=ids)
ec2.get_waiter("instance_stopped").wait(InstanceIds=ids)
for r in ec2.describe_instances(InstanceIds=ids)["Reservations"]:
    for i in r["Instances"]:
        print(i["InstanceId"], i["State"]["Name"])

print("--- real create_tags, then the report again")
ec2.create_tags(Resources=[iid], Tags=[{"Key": "Owner", "Value": "kiran"}])
