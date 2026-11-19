#!/bin/bash
# Session 15 on the emulator: custom metric, alarm that notifies a topic, SNS fan-out to an SQS inbox,
# a log group with retention and a metric filter. Needs the emulator (see ./emulator/start.sh).
set -u
echo "-- custom metric"; aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 1
aws cloudwatch list-metrics --namespace Atithi/Booking --query 'Metrics[].[Namespace,MetricName,Dimensions[0].Name,Dimensions[0].Value]' --output text
echo "-- the topic, an email subscriber (stays pending), and an SQS inbox to watch deliveries"
T=$(aws sns create-topic --name ops-alerts --query TopicArn --output text)
aws sns subscribe --topic-arn $T --protocol email --notification-endpoint asha@example.com >/dev/null
QU=$(aws sqs create-queue --queue-name ops-inbox --query QueueUrl --output text)
QA=$(aws sqs get-queue-attributes --queue-url $QU --attribute-names QueueArn --query Attributes.QueueArn --output text)
aws sns subscribe --topic-arn $T --protocol sqs --notification-endpoint $QA >/dev/null
aws sns publish --topic-arn $T --subject test --message "hello from the alarm desk" >/dev/null
aws sqs receive-message --queue-url $QU --wait-time-seconds 3 --query 'Messages[0].Body' --output text | python3 -c "import sys,json;d=json.loads(sys.stdin.read());print(d['Type'],'|',d['Subject'],'|',d['Message'])"
echo "-- an alarm that rings the topic (Sum of FailedBookings over 60 s > 5)"
aws cloudwatch put-metric-alarm --alarm-name failed-bookings --namespace Atithi/Booking --metric-name FailedBookings --dimensions Name=Service,Value=booking \
  --statistic Sum --period 60 --evaluation-periods 1 --threshold 5 --comparison-operator GreaterThanThreshold --alarm-actions $T --ok-actions $T
aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 9
for i in $(seq 1 12); do st=$(aws cloudwatch describe-alarms --alarm-names failed-bookings --query 'MetricAlarms[0].StateValue' --output text); echo "t+$((i*10))s $st"; [ "$st" = ALARM ] && break; sleep 10; done
aws sqs receive-message --queue-url $QU --max-number-of-messages 5 --wait-time-seconds 3 --query 'Messages[].Body' --output text | python3 -c "
import sys,json
for part in sys.stdin.read().split('\t'):
    part=part.strip()
    if not part: continue
    d=json.loads(part)
    try:
        m=json.loads(d['Message']); print(d['Subject'], '|', m['AlarmName'], m['OldStateValue'], '->', m['NewStateValue'])
    except Exception: print(d.get('Subject'))"
echo "-- logs: retention, filter, metric filter"
aws logs create-log-group --log-group-name /atithi/booking; aws logs put-retention-policy --log-group-name /atithi/booking --retention-in-days 14
aws logs create-log-stream --log-group-name /atithi/booking --log-stream-name web1
NOW=$(python3 -c "import time;print(int(time.time()*1000))")
aws logs put-log-events --log-group-name /atithi/booking --log-stream-name web1 --log-events timestamp=$NOW,message="INFO booking ok" timestamp=$((NOW+1)),message="ERROR db timeout" timestamp=$((NOW+2)),message="ERROR db timeout" timestamp=$((NOW+3)),message="WARN slow" >/dev/null
aws logs filter-log-events --log-group-name /atithi/booking --filter-pattern ERROR --query 'events[].message' --output text
aws logs put-metric-filter --log-group-name /atithi/booking --filter-name errors --filter-pattern ERROR --metric-transformations metricName=BookingErrors,metricNamespace=Atithi/Booking,metricValue=1
aws logs describe-metric-filters --log-group-name /atithi/booking --query 'metricFilters[0].[filterName,filterPattern,metricTransformations[0].metricName]' --output text
echo "-- recovery"
aws cloudwatch put-metric-data --namespace Atithi/Booking --metric-name FailedBookings --dimensions Service=booking --value 1
for i in $(seq 1 10); do st=$(aws cloudwatch describe-alarms --alarm-names failed-bookings --query 'MetricAlarms[0].StateValue' --output text); echo "t+$((i*10))s $st"; [ "$st" = OK ] && break; sleep 10; done
