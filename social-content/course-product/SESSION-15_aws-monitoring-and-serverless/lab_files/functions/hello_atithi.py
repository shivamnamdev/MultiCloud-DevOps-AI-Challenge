import os, json
def lambda_handler(event, context):
    name = event.get("name", "guest")
    greeting = os.environ.get("GREETING", "Namaste")
    print(f"invoked for {name}")
    return {"statusCode": 200, "body": json.dumps({"message": f"{greeting}, {name}!"})}
