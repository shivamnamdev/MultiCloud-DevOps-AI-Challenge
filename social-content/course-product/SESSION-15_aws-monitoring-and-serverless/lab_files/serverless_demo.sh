#!/bin/bash
# Session 15 on the emulator: a function record, a schedule, and an S3 notification. Functions do not RUN here.
set -u
mkdir -p build; cp functions/hello_atithi.py build/hello_atithi.py; (cd build && python3 -c "import zipfile;z=zipfile.ZipFile('fn.zip','w');z.write('hello_atithi.py');z.close()")
aws iam create-role --role-name lambda-basic --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null
aws lambda create-function --function-name hello-atithi --runtime python3.12 --role arn:aws:iam::000000000000:role/lambda-basic --handler hello_atithi.lambda_handler --zip-file fileb://build/fn.zip --environment Variables={GREETING=Namaste} --memory-size 128 --timeout 10 --query '[FunctionName,Runtime,MemorySize,Timeout,State]' --output text
echo '{"name":"Asha"}' > build/event.json
aws lambda invoke --function-name hello-atithi --payload fileb://build/event.json build/out.json --query '[StatusCode,FunctionError]' --output text; cut -c1-160 build/out.json; echo
echo "-- the narrow role"
cat > build/stopdev-policy.json <<'JSON'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["ec2:DescribeInstances","ec2:StopInstances"],"Resource":"*"}]}
JSON
aws iam put-role-policy --role-name lambda-basic --policy-name stop-dev-only --policy-document file://build/stopdev-policy.json
for a in ec2:DescribeInstances ec2:StopInstances ec2:TerminateInstances; do printf "%s: " $a; aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::000000000000:role/lambda-basic --action-names $a --resource-arns '*' --query 'EvaluationResults[0].EvalDecision' --output text; done
echo "-- nightly schedule (UTC): cron(0 20 * * ? *) is 01:30 in India"
aws events put-rule --name stop-dev-nightly --schedule-expression 'cron(0 20 * * ? *)' --state ENABLED --query RuleArn --output text
aws events put-targets --rule stop-dev-nightly --targets "Id=1,Arn=arn:aws:lambda:us-east-1:000000000000:function:hello-atithi" --query FailedEntryCount --output text
aws events describe-rule --name stop-dev-nightly --query '[ScheduleExpression,State]' --output text
echo "-- S3 notification: only uploads/ and .jpg"
aws s3 mb s3://atithi-photos-n >/dev/null
cat > build/notif.json <<'JSON'
{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"arn:aws:lambda:us-east-1:000000000000:function:hello-atithi","Events":["s3:ObjectCreated:*"],"Filter":{"Key":{"FilterRules":[{"Name":"prefix","Value":"uploads/"},{"Name":"suffix","Value":".jpg"}]}}}]}
JSON
aws lambda add-permission --function-name hello-atithi --statement-id s3-invoke --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::atithi-photos-n --source-account 000000000000 --query Statement --output text | cut -c1-90
aws s3api put-bucket-notification-configuration --bucket atithi-photos-n --notification-configuration file://build/notif.json && echo saved
aws s3api get-bucket-notification-configuration --bucket atithi-photos-n --query 'LambdaFunctionConfigurations[0].[Events[0],Filter.Key.FilterRules[0].Value,Filter.Key.FilterRules[1].Value]' --output text
rm -rf build
