import boto3
ec2 = boto3.client("ec2")
def lambda_handler(event, context):
    r = ec2.describe_instances(Filters=[
        {"Name": "tag:Env", "Values": ["dev"]},
        {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if ids:
        ec2.stop_instances(InstanceIds=ids)
    print(f"stopped: {ids}")
    return {"stopped": ids}
