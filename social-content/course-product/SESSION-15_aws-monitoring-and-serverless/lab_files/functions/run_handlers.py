"""Runs the three Session 15 handlers on your own machine, the way Lambda would call them.
hello_atithi and photo_logger need nothing. stop_dev needs boto3 and AWS_ENDPOINT_URL pointing at the emulator."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

print("== hello_atithi")
import hello_atithi
print(hello_atithi.lambda_handler({"name": "Asha"}, None))
os.environ["GREETING"] = "Swagat"
print(hello_atithi.lambda_handler({}, None))

print("== photo_logger with the key exactly as S3 sends it (a space becomes +)")
import photo_logger, urllib.parse
event = {"Records": [{"s3": {"bucket": {"name": "atithi-photos"}, "object": {"key": "uploads/room+101.jpg"}}}]}
photo_logger.lambda_handler(event, None)
print("raw key without decoding would have been:", event["Records"][0]["s3"]["object"]["key"])
print("a key with a real plus sign arrives as %2B:", urllib.parse.quote_plus("uploads/a+b.jpg"), "->", urllib.parse.unquote_plus("uploads%2Fa%2Bb.jpg"))

if os.environ.get("AWS_ENDPOINT_URL"):
    import boto3
    ec2 = boto3.client("ec2")
    def launch(env, name):
        return ec2.run_instances(ImageId="ami-ubuntu2404-arm64", InstanceType="t4g.micro", MinCount=1, MaxCount=1,
            TagSpecifications=[{"ResourceType": "instance", "Tags": [{"Key": "Env", "Value": env}, {"Key": "Name", "Value": name}]}]
        )["Instances"][0]["InstanceId"]
    ids = {n: launch(e, n) for n, e in [("dev-1", "dev"), ("dev-2", "dev"), ("prod-1", "prod")]}
    ec2.stop_instances(InstanceIds=[ids["dev-2"]])          # one dev building is already asleep
    print("== stop_dev")
    import stop_dev
    out = stop_dev.lambda_handler({}, None)
    inv = {v: k for k, v in ids.items()}
    print("stopped now:", sorted(inv[i] for i in out["stopped"]))
    for r in ec2.describe_instances(InstanceIds=list(ids.values()))["Reservations"]:
        for i in r["Instances"]:
            print(" ", inv[i["InstanceId"]], i["State"]["Name"])
    ec2.terminate_instances(InstanceIds=list(ids.values()))
