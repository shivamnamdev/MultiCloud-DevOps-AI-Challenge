import boto3

ec2 = boto3.client("ec2")
for page in ec2.get_paginator("describe_instances").paginate():
    for r in page["Reservations"]:
        for i in r["Instances"]:
            tags = {t["Key"]: t["Value"] for t in i.get("Tags", [])}
            flag = "" if "Owner" in tags else "  <- no Owner tag"
            print(i["InstanceId"], i["InstanceType"], i["State"]["Name"], tags.get("Name", "-"), flag)
