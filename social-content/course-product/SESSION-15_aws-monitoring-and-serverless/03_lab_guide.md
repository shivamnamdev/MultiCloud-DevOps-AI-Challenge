# Session 15 lab guide: AWS monitoring and serverless

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Two kinds of test were used:
> - **Emulator (`floci`, not AWS)** for the **API**: custom metrics, alarms that really evaluate data and notify a topic, SNS, an SQS inbox to watch the messages arrive, log groups, retention, metric filters, an EventBridge schedule, a Lambda function **record**, and an S3 notification setting.
> - **Real, on your laptop:** the three Lambda **handlers**, run as plain Python with the events Lambda would send. One of them (`stop-dev`) ran against the emulator's EC2.
> **Lambda functions did not run in the emulator**: `invoke` answered `Unhandled` with `Failed to start Lambda container: Docker is not reachable ... Lambda functions run in Docker containers.` (We did not give the emulator access to the Docker socket.) Also **not tested:** real emails, real EC2 CPU metrics and the `stress` lab, detailed monitoring, Logs Insights results (our query came back `Failed`), cold starts and the real memory and cost comparison, S3 events that actually trigger a function, billing alarms, and the console.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 30 min, Part C 30 min, Part D 30 min |
| **Cost** | Free here. On real AWS, alarms, custom metrics, log storage and Lambda calls each have a small charge. Remove the nightly schedule when you finish, or it keeps running. |
| **Skill check before you start** | Sessions 7 (boto3, `requests`), 8, 9 (the emulator setup, roles), 12 (S3). Docker installed. |

## Before you start

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(See the Session 8 guide. Run `docker rm -f floci-lab` when you finish.) `lab_files/monitoring_demo.sh` runs Parts A and B; `lab_files/serverless_demo.sh` runs the API half of Part C; `lab_files/functions/run_handlers.py` runs the handlers.

---

## Part A: meters and alarms (Episode 1)

### A1. A metric: namespace, name, dimension

```bash
aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 1
aws cloudwatch list-metrics --namespace Atithi/Booking --query 'Metrics[].[Namespace,MetricName,Dimensions[0].Name,Dimensions[0].Value]' --output text
```

Expected (ours): `Atithi/Booking FailedBookings Service booking`: the three words of the script, in one line. (Memory and disk are not metrics EC2 sends by itself; that needs an agent. We did not test the agent.)

### A2. An alarm that watches a meter

The script's CPU alarm needs a real building. We used a **custom** metric instead, so that we could make it breach by hand:

```bash
aws cloudwatch put-metric-alarm --alarm-name failed-bookings --namespace Atithi/Booking --metric-name FailedBookings \
  --dimensions Name=Service,Value=booking --statistic Sum --period 60 --evaluation-periods 1 \
  --threshold 5 --comparison-operator GreaterThanThreshold
aws cloudwatch describe-alarms --alarm-names failed-bookings --query 'MetricAlarms[0].[StateValue,Threshold,Period,EvaluationPeriods]' --output text
aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 9
```

Expected (ours): the alarm starts in **`INSUFFICIENT_DATA`**, and after you put a value above the threshold it moves to **`ALARM`** (about 20 to 50 seconds for us). After a low value (`1`) and a minute or so, it went back to **`OK`**. The three states of the script, with real transitions. `aws cloudwatch describe-alarm-history --alarm-name failed-bookings` shows each change (`StateUpdate ... from INSUFFICIENT_DATA to ALARM`). Also: `aws cloudwatch set-alarm-state ... --state-value ALARM` lets you force a state to test whatever listens, as we did once.

The script's own lab (`CPUUtilization > 60`, `stress --cpu 2` on an EC2 building, detailed monitoring) needs a real instance. We did not run it.

### A3. The "which readings" question

The script's `2 of 3` datapoints rule is the `--datapoints-to-alarm` option (with `--evaluation-periods 3`). We created an alarm with `--datapoints-to-alarm 1` and `--treat-missing-data notBreaching` and read the settings back (`describe-alarms` showed `notBreaching`). We did not watch a "2 of 3" alarm behave.

**Check yourself:**

- [ ] You saw an alarm go `INSUFFICIENT_DATA`, `ALARM`, then `OK`.
- [ ] You can say what namespace, metric name and dimension mean.

---

## Part B: logs, and the alarm desk (Episode 2)

### B1. A topic, and a way to see what it sends

An email subscription cannot be confirmed here, so we also subscribed an **SQS queue** and read the messages from it. That shows exactly what a topic's subscribers receive.

```bash
T=$(aws sns create-topic --name ops-alerts --query TopicArn --output text)
aws sns subscribe --topic-arn $T --protocol email --notification-endpoint asha@example.com
QU=$(aws sqs create-queue --queue-name ops-inbox --query QueueUrl --output text)
QA=$(aws sqs get-queue-attributes --queue-url $QU --attribute-names QueueArn --query Attributes.QueueArn --output text)
aws sns subscribe --topic-arn $T --protocol sqs --notification-endpoint $QA
aws sns publish --topic-arn $T --subject test --message "hello from the alarm desk"
aws sqs receive-message --queue-url $QU --wait-time-seconds 3 --query 'Messages[0].Body' --output text
```

Expected (ours): a JSON with `"Type": "Notification"`, `"Subject": "test"` and `"Message": "hello from the alarm desk"`. **No email was sent** (the email subscription just had an id; on real AWS it would be `PendingConfirmation` until Asha clicks the link, the script's step). The publish-subscribe idea is the script's loudspeaker: one message, every subscriber.

### B2. The alarm rings the topic

Add `--alarm-actions $T --ok-actions $T` to the alarm from Part A (or recreate it with them), then push the metric over the threshold:

```bash
aws cloudwatch put-metric-alarm --alarm-name failed-bookings ... --alarm-actions $T --ok-actions $T
aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 9
aws sqs receive-message --queue-url $QU --max-number-of-messages 5 --wait-time-seconds 3 --query 'Messages[].Body' --output text
```

What we received in the inbox: a notification with the subject `ALARM: "failed-bookings"` and a message body (JSON) containing `AlarmName failed-bookings`, `OldStateValue INSUFFICIENT_DATA` and `NewStateValue ALARM`. That is the script's "ALARM ka email", up to the point where the email would be sent. The `OK` message follows when it recovers.

### B3. Log groups, retention, filters

```bash
aws logs create-log-group --log-group-name /atithi/booking
aws logs put-retention-policy --log-group-name /atithi/booking --retention-in-days 14
aws logs create-log-stream --log-group-name /atithi/booking --log-stream-name web1
NOW=$(python3 -c "import time;print(int(time.time()*1000))")
aws logs put-log-events --log-group-name /atithi/booking --log-stream-name web1 \
  --log-events timestamp=$NOW,message="INFO booking ok" timestamp=$((NOW+1)),message="ERROR db timeout" timestamp=$((NOW+2)),message="ERROR db timeout" timestamp=$((NOW+3)),message="WARN slow"
aws logs filter-log-events --log-group-name /atithi/booking --filter-pattern ERROR --query 'events[].message' --output text
aws logs put-metric-filter --log-group-name /atithi/booking --filter-name errors --filter-pattern ERROR \
  --metric-transformations metricName=BookingErrors,metricNamespace=Atithi/Booking,metricValue=1
aws logs describe-metric-filters --log-group-name /atithi/booking --query 'metricFilters[0].[filterName,filterPattern,metricTransformations[0].metricName]' --output text
```

Expected (ours): retention `14`, the two `ERROR db timeout` lines, and the metric filter `errors ERROR BookingErrors`. A metric filter turns log lines into a number you can alarm on. **Logs Insights:** the script's query (`fields @timestamp, @message | filter @message like /ERROR/ | stats count() by bin(5m)`) was accepted by `aws logs start-query`, but the result status was **`Failed`** with no rows in the emulator. Try it in the real console.

**Billing alarms and Budgets** (Scene 5): not tested.

**Check yourself:**

- [ ] You saw an alarm's message arrive at a subscriber.
- [ ] You can say what a metric filter does and what retention is for.

---

## Part C: the freelancer (Episodes 3 and 4)

### C1. A function record, and the invoke that fails here

```bash
cd lab_files
mkdir -p build; cp functions/hello_atithi.py build/; (cd build && python3 -c "import zipfile;z=zipfile.ZipFile('fn.zip','w');z.write('hello_atithi.py');z.close()")
aws lambda create-function --function-name hello-atithi --runtime python3.12 --role arn:aws:iam::000000000000:role/lambda-basic --handler hello_atithi.lambda_handler --zip-file fileb://build/fn.zip --environment Variables={GREETING=Namaste} --memory-size 128 --timeout 10
aws lambda invoke --function-name hello-atithi --payload fileb://build/event.json build/out.json
```

(You make the execution role first; `serverless_demo.sh` does all of this.) `create-function` printed `hello-atithi python3.12 128 10 Active`: runtime, memory, timeout. `invoke` returned `200 Unhandled` with the Docker error quoted at the top. So the script's lab (test with `{"name": "Asha"}`, read `START`, `END` and `REPORT` lines, compare 128 MB with 512 MB) is for a real account. We could not compare duration or cost.

### C2. The handlers, run for real

```bash
cd functions
python3 run_handlers.py
```

(It runs with plain Python. Add boto3 and `AWS_ENDPOINT_URL` for the third handler, as below.) Expected (ours):

```
== hello_atithi
invoked for Asha
{'statusCode': 200, 'body': '{"message": "Namaste, Asha!"}'}
invoked for guest
{'statusCode': 200, 'body': '{"message": "Swagat, guest!"}'}
```

The handler reads its settings from the environment (`GREETING`), uses `event.get("name", "guest")` for a missing field, and `print` is what lands in the logs. Changing `GREETING` changed the answer: environment variables are how one function serves many settings.

**The S3 photo handler and the `+` in names.**

```
== photo_logger with the key exactly as S3 sends it (a space becomes +)
new photo: s3://atithi-photos/uploads/room 101.jpg
raw key without decoding would have been: uploads/room+101.jpg
a key with a real plus sign arrives as %2B: uploads%2Fa%2Bb.jpg -> uploads/a+b.jpg
```

S3 puts the key in the event URL-encoded: a space is `+` and a real plus is `%2B`. `urllib.parse.unquote_plus` undoes both. Without it, a function that looks for `uploads/room 101.jpg` would never find it. The script's `room 101.jpg` test is exactly this trap. (We simulated the event. We could not upload a file and see S3 call the function.)

### C3. `stop-dev`: only dev buildings that are running

With the emulator running, `run_handlers.py` also creates three buildings (two tagged `Env=dev`, one `Env=prod`), stops one dev building by hand, and calls `stop_dev.lambda_handler`:

```bash
docker run --rm --network awslab -v "$PWD:/f" -w /f -e AWS_ENDPOINT_URL=http://floci-lab:4566 \
  -e AWS_ACCESS_KEY_ID=test -e AWS_SECRET_ACCESS_KEY=test -e AWS_DEFAULT_REGION=us-east-1 \
  python:3.12-slim bash -c 'pip install -q boto3; python run_handlers.py'
```

What we saw: `stopped: ['i-5eb1e90b9df5b7a4a']`, then `stopped now: ['dev-1']` and the final states `prod-1 running`, `dev-2 stopped`, `dev-1 stopped`. The handler stopped **only** the running dev building: the prod one was left alone and the already-stopped dev one was not touched again. That is the script's tag filter (`tag:Env=dev` and `instance-state-name=running`) doing its job.

The narrow role, checked with the simulator:

```bash
aws iam put-role-policy --role-name lambda-basic --policy-name stop-dev-only --policy-document file://stopdev-policy.json
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::000000000000:role/lambda-basic --action-names ec2:StopInstances --resource-arns '*' --query 'EvaluationResults[0].EvalDecision' --output text
```

`ec2:DescribeInstances` and `ec2:StopInstances` came back `allowed`; `ec2:TerminateInstances` and `ec2:RunInstances` came back `implicitDeny`. The function could stop buildings, and nothing more.

### C4. The nightly schedule: a mistake in the first script

The script's example was `cron(30 15 * * ? *)` with the words "UTC ke hisaab se raat ke ek bajke tees minute". We worked it out:

| Expression (UTC) | Time in India (UTC+5:30) |
|---|---|
| `cron(30 15 * * ? *)` (first script) | **21:00** the same evening |
| `cron(0 20 * * ? *)` (now in the script) | **01:30** the next night |

`15:30 UTC` is 1:30 at UTC+10 (Australia), not in India. EventBridge cron expressions are always in **UTC**; convert from your own time zone. We saved the corrected rule on the emulator:

```bash
aws events put-rule --name stop-dev-nightly --schedule-expression 'cron(0 20 * * ? *)' --state ENABLED
aws events put-targets --rule stop-dev-nightly --targets "Id=1,Arn=arn:aws:lambda:us-east-1:000000000000:function:hello-atithi"
aws events describe-rule --name stop-dev-nightly --query '[ScheduleExpression,State]' --output text
```

Expected: `cron(0 20 * * ? *) ENABLED`. (The emulator also accepted a five-field expression, `cron(30 15 * * *)`, with no error. AWS's documentation says EventBridge cron expressions have **six** fields, so this is another place the emulator is more lenient than AWS; we did not test the real service.) It never fires a function here.

### C5. The warehouse bell

```bash
aws lambda add-permission --function-name hello-atithi --statement-id s3-invoke --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::atithi-photos-n --source-account 000000000000
aws s3api put-bucket-notification-configuration --bucket atithi-photos-n --notification-configuration file://notif.json
aws s3api get-bucket-notification-configuration --bucket atithi-photos-n --query 'LambdaFunctionConfigurations[0].[Events[0],Filter.Key.FilterRules[0].Value,Filter.Key.FilterRules[1].Value]' --output text
```

(`notif.json` is in `serverless_demo.sh`.) Expected: `s3:ObjectCreated:* uploads/ .jpg`: only `.jpg` files under `uploads/` ring the bell. Saving it first failed with `Unable to validate the following destination configurations` when the function did not exist yet. Once it existed, the emulator accepted the setting **even before** we added the permission for S3 to call it. Real AWS also checks that permission, which the script says ("function ko resource policy ne kaise ijaazat di"): do not rely on the emulator here. `get-policy` showed the statement: principal `s3.amazonaws.com`, action `lambda:InvokeFunction`.

Not tested: retries, dead-letter queues, idempotency, concurrency, and a loop where the function writes to the bucket that triggers it (Scene 3's warning).

**Check yourself:**

- [ ] You ran all three handlers and saw `room+101.jpg` decode.
- [ ] You can say why `15:30 UTC` was the wrong time for India.
- [ ] You know the function never ran **inside** the emulator.

---

## Clean up

```bash
docker rm -f floci-lab
docker network rm awslab
rm -rf lab_files/build
```

On real AWS: delete the **schedule** first (it keeps firing), then the S3 trigger, the functions and their log groups, the alarm, the topic and its subscriptions, and the billing alert. The script's cleanup order matters because a forgotten schedule or alarm quietly costs money.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Alarm stuck in `INSUFFICIENT_DATA` | No data in the period, or the wrong dimension | Check namespace, name and dimensions match the metric exactly |
| Subscription never receives mail (real AWS) | Not confirmed | Click the link in the confirmation mail |
| Function cannot find `room 101.jpg` | S3 sends `room+101.jpg` | `urllib.parse.unquote_plus` |
| Schedule fires at the wrong hour | Cron is in UTC | Convert from your time zone |
| `Unable to validate the following destination configurations` | The function is missing, or S3 may not call it | Create it, then `lambda add-permission` |
| `Unhandled ... Docker is not reachable` | The emulator cannot start function containers | Run the function code locally (`run_handlers.py`) or use a real account |

## What we did not test

- **Real EC2 metrics and the `stress` lab,** detailed monitoring, and memory or disk through the agent.
- **Real notifications:** email delivery and subscription confirmation.
- **Logs Insights** results, billing alarms and Budgets.
- **Lambda running:** cold starts, the memory and cost comparison, retries, concurrency, dead-letter queues, S3 events that really trigger a function.
- **The console.**
