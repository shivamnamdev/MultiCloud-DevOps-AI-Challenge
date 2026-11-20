# Session 11 lab guide: AWS load balancing

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Three things were used instead, and none of them is an AWS Application Load Balancer that serves traffic:
> - **`floci`** (a free emulator, not AWS) for the **API**: target group, load balancer, listener, target health, and an Auto Scaling group attached to the group.
> - **An `nginx` stand-in for the marshal**, in Docker, to see **round robin and failover** with your own eyes.
> - **Paper** for the ALB-or-NLB quiz.
> **Not tested:** a real ALB's DNS name and routing, real health checks against real web servers, the "unhealthy target is replaced by the Auto Scaling group" loop (the emulator marked targets unhealthy but its group did not react), TLS, listener rules, NLB, and the console.

> **Update, tested on real AWS (ap-south-1, two towers, deleted the same day).** A real Application Load Balancer in front of an Auto Scaling group of nginx buildings (from the Session 10 image):
> - **Target group defaults on real AWS:** `HTTP / 5 2 30` and a 5 second timeout (healthy after 5 passes, unhealthy after 2 failures, every 30 s), the same as the emulator.
> - **Timing:** the load balancer was `active` in about 2 minutes; the targets went `initial` to `healthy` about 2 minutes after that. 10 requests to its DNS name gave **5 and 5** across the two hostnames (round robin).
> - **Security group chain:** the building group allowed port 80 **only from the load balancer's group**. A direct request to a building's public address then **timed out** (curl exit 28), while the load balancer still worked.
> - **Failure:** we stopped nginx on one building. For about **40 seconds** some requests got **502** (the marshal still sent guests there), then the target turned `unhealthy` and every request was `200` from the other building. The group's **ELB health check** then replaced the building (about 90 seconds after the stop): the old target went `draining`, a new one `initial` then `healthy`. This needs `--health-check-type ELB` and a grace period on the group, as the script says.
> - Not tested: TLS and certificates, listener rules, NLB, stickiness.

| | |
|---|---|
| **Time** | Part A 20 min, Part B 20 min, Part C 40 min, Part D 20 min |
| **Cost** | Free here. A real ALB bills by the hour while it exists; delete it first when you clean up. |
| **Skill check before you start** | Sessions 8 and 10 (instances, Auto Scaling, the emulator setup). Docker installed. |

## Before you start

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(See the Session 8 guide for what this does. Run `docker rm -f floci-lab` when you finish.) `lab_files/alb_demo.sh` and `lab_files/marshal_demo.sh` run Parts B to D in one go.

---

## Part A: two buildings and why a marshal (Episode 1)

The script launches two buildings in two towers with a user data page that prints the building's name. On the emulator we could launch buildings, but not see the page: they run no web server. The user data script is the Session 8 one, with the hostname in the page. Run this lab on a real account if you can, or use the stand-in in Part C.

---

## Part B: the marshal's pieces, by API (Episodes 2 and 3)

### B1. A target group with a health check

```bash
VPC=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
TG=$(aws elbv2 create-target-group --name web-tg --protocol HTTP --port 80 --vpc-id $VPC --health-check-path / --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 describe-target-groups --names web-tg --query 'TargetGroups[0].[HealthCheckProtocol,HealthCheckPath,HealthyThresholdCount,UnhealthyThresholdCount,HealthCheckIntervalSeconds]' --output text
```

Expected (ours): `HTTP / 5 2 30`: check path `/`, a target must pass **5** checks to be called healthy, fail **2** to be called unhealthy, one check every **30 seconds**. These are the emulator's defaults. Real ALB defaults may differ, so read your own target group's settings. The point of the script is the same: a health check path, a count, and an interval.

### B2. Register two buildings, create the load balancer and listener

```bash
S1=$(aws ec2 describe-subnets --query 'Subnets[0].SubnetId' --output text)
S2=$(aws ec2 describe-subnets --query 'Subnets[1].SubnetId' --output text)
I1=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --subnet-id $S1 --query 'Instances[0].InstanceId' --output text)
I2=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --subnet-id $S2 --query 'Instances[0].InstanceId' --output text)
aws elbv2 register-targets --target-group-arn $TG --targets Id=$I1 Id=$I2
SGA=$(aws ec2 create-security-group --group-name alb-sg --description marshal --vpc-id $VPC --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $SGA --protocol tcp --port 80 --cidr 0.0.0.0/0
LB=$(aws elbv2 create-load-balancer --name atithi-alb --subnets $S1 $S2 --security-groups $SGA --scheme internet-facing --type application --query 'LoadBalancers[0].LoadBalancerArn' --output text)
aws elbv2 describe-load-balancers --names atithi-alb --query 'LoadBalancers[0].[Type,Scheme,State.Code,length(AvailabilityZones)]' --output text
aws elbv2 create-listener --load-balancer-arn $LB --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$TG
```

Expected (ours): `application internet-facing active 2` (two towers), then the listener `80 HTTP`. It mirrors the console steps of the script: the load balancer has its **own** security group (here `alb-sg`, with port 80 open to the world), and the buildings' security group would then allow port 80 **from the load balancer's group**. (We did not test that second rule.)

### B3. Target health

```bash
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[TargetHealth.State,TargetHealth.Reason]' --output text
```

Right after creating: `initial initial`. About 45 seconds later: **`unhealthy Target.FailedHealthChecks`** for both. That is not a bug in the lab: nothing is listening on port 80 in those emulated buildings, so the check fails, exactly as it would on a real building with nginx stopped. It shows you the two words to look for when a real target is unhealthy. We could not make a target turn `healthy`, because the emulator has no web server to answer.

**The ALB's DNS name.** The load balancer got a DNS name (`atithi-alb-....elb.localhost.floci.io`). We did not open it: the script's "refresh and see the building name change" needs real buildings behind a real ALB. Part C does that with a stand-in.

**Check yourself:**

- [ ] You can name what a target group, a listener and a health check each do.
- [ ] You know why a target is `unhealthy` with `Target.FailedHealthChecks`.

---

## Part C: the marshal you can watch (stand-in)

`lab_files/marshal_demo.sh` starts two nginx buildings, `web1` and `web2`, each serving a page with its own name, and a third nginx as the marshal with a two-server list (`lab_files/marshal/nginx.conf`: round robin, and a server that fails once is left out for 5 seconds). It is **not** an ALB. It shows the behaviour the script describes.

```bash
cd lab_files && ./marshal_demo.sh
```

What we saw (six requests each time):

```
both up:      web1 web2 web1 web2 web1 web2
web2 stopped: web1 web1 web1 web1 web1 web1
web2 back:    web1 web1 web2 web1 web2 web1
```

Guests alternate between the two buildings, a stopped building stops receiving guests with no error shown to the guest, and the building rejoins once it is back. (In the last line `web2` came back into rotation after a short delay. We set a 5 second "leave it out" time in the config, and we did not measure exactly when it rejoined.) A real ALB does this through health checks (interval and thresholds, like B1), not through a failed request, so timings differ. The script's `sudo systemctl stop nginx` step is the same idea.

Clean-up is inside the script (it removes the three containers and the network).

---

## Part D: the Auto Scaling group behind the marshal (Episode 4)

```bash
aws ec2 create-launch-template --launch-template-name atithi-web --launch-template-data '{"ImageId":"ami-ubuntu2404-arm64","InstanceType":"t4g.micro"}'
SUBS=$(aws ec2 describe-subnets --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')
aws autoscaling create-auto-scaling-group --auto-scaling-group-name web-asg --launch-template LaunchTemplateName=atithi-web,Version='$Latest' \
  --min-size 2 --max-size 4 --desired-capacity 2 --vpc-zone-identifier "$SUBS" --target-group-arns $TG --health-check-type ELB --health-check-grace-period 120
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names web-asg --query 'AutoScalingGroups[0].[HealthCheckType,HealthCheckGracePeriod]' --output text
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State,TargetHealth.Reason]' --output text
```

Expected (ours): `ELB 120` (health check type ELB, with the grace period), and a few seconds later two instances `InService Healthy`. When we looked at the target group again, **the group's own two buildings were registered as targets** (both `unhealthy` for the same no-web-server reason). In one run the hand-registered buildings from Part B were no longer listed once the group was attached, in another run we did not see that. Do not rely on either: as the script says, remove your hand-made buildings from the target group yourself.

**The part we could not see.** With health check type `ELB`, a real group is supposed to replace a building the marshal calls unhealthy. In the emulator the group kept reporting `Healthy` while its targets were `unhealthy`, so this loop did **not** run. Test it on a real account as the script says: terminate a building by hand (the group replaces it, as we saw in Session 10), and stop nginx on one (the marshal marks it unhealthy and the group replaces it).

### D1. Clean up in the script's order

```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg --min-size 0 --desired-capacity 0
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name web-asg
L=$(aws elbv2 describe-listeners --load-balancer-arn $LB --query 'Listeners[0].ListenerArn' --output text)
aws elbv2 delete-listener --listener-arn $L
aws elbv2 delete-load-balancer --load-balancer-arn $LB
aws elbv2 delete-target-group --target-group-arn $TG
```

All five calls succeeded (`ASG deleted`, `ALB deleted`, `target group deleted`). The order is the script's: group first, then the load balancer (on real AWS it bills by the hour), then the target group (it cannot go while a listener still points to it, we did not test that rule), then the image and its snapshot.

### D2. The paper quiz

The six cases of the script (path-based routing, a UDP game server, a fixed address, a normal website, huge TCP traffic, WebSocket) have fixed answers in the script: ALB, NLB, NLB, ALB, NLB, ALB. We did not test NLB or WebSocket support.

**Check yourself:**

- [ ] You watched two names alternate, then one disappear and come back.
- [ ] You can name the order of cleanup.
- [ ] You know which behaviours you still have to see on a real account.

---

## Clean up

```bash
docker rm -f floci-lab
docker network rm awslab
```

(`marshal_demo.sh` removes its own containers.) On real AWS: delete the Auto Scaling group, then the ALB, then the target group, then the AMI and snapshot, and check for leftover Elastic IPs and volumes.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Target `unhealthy` with `Target.FailedHealthChecks` | No server on the port, wrong path, or the security group blocks the marshal | Check the three from inside out (Session 5) |
| `502` or `503` from a real ALB | No healthy targets | Look at target health first |
| Marshal stand-in answers only one name | The other building is down, or not on the same Docker network | `docker ps`, and the network name |
| Cannot delete a target group | A listener still uses it | Delete the listener or the load balancer first |

## What we did not test

- **A real ALB:** its DNS name, listener rules, the 5 second to a minute health check timing, TLS and certificates, sticky sessions, the security-group-to-security-group rule.
- **Health-check-driven replacement** by the Auto Scaling group.
- **NLB,** Global Accelerator, and any UDP or WebSocket case.
- **The console** and **real costs.**
