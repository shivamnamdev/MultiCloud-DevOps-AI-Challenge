# Session 10 lab guide: EC2 storage and scaling

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. We ran the **commands** against `floci`, a free program that imitates AWS on your own machine (it is not AWS), and the **Linux** steps for real in a container.
> - **Emulator, worked:** volumes (create, attach, the same-tower rule, detach, delete), launch templates, Auto Scaling groups (create, scale, replace a lost building, the max limit, the delete rules), a target-tracking policy (created, never triggered).
> - **Emulator, did NOT work:** **snapshots** (`UnsupportedOperation: Operation CreateSnapshot is not supported`) and **creating an AMI from a building** (`IncorrectInstanceState ... it has no running container to capture`). So the script's "Photograph se Restore" and "Apna Model Hotel Banao" labs, and anything that needs a real disk image, were **not** run.
> - **Linux for real:** format, mount, `fstab` with `nofail`, and a copy-and-restore test, on a file standing in for the disk.
> - **Not tested at all:** the console, real device names (`nvme1n1`), CloudWatch metrics, `stress` pushing CPU over 40% so the group scales out on its own, real timing, real prices.

> **Update, tested on real AWS (ap-south-1, t3.micro, Ubuntu 24.04, deleted the same day).** What the emulator could not do, now run for real:
> - **Same-tower rule:** `InvalidVolume.ZoneMismatch ... is not in the same availability zone as instance`. A new gp3 volume came with **3000 IOPS and 125 MB/s** by default. The new volume showed as `nvme1n1`; `blkid` on it printed nothing and exited `2` (empty, safe to format). Then `mkfs -t ext4`, mount, an `fstab` line with `nofail`, `umount` and `mount -a` brought the file back.
> - **Snapshot and restore:** an 8 GB nearly empty volume took about **1 minute** to reach `completed`. A volume made from it in the same zone mounted at `/restore` with the file and the **same UUID**.
> - **AMI:** `create-image` took about **3 minutes** to become `available`. An instance launched from it with **no user data** served the page. **But the page is baked into the image, so it still said the builder's hostname.** If you want each building to show its own name, rewrite the page at boot (`lab_files/userdata_asg.sh`). Before you deregister an AMI, its snapshot cannot be deleted (`InvalidSnapshot.InUse`); **after deregistering, the snapshot stays** and keeps billing until you delete it.
> - **Auto Scaling:** the first group in an account creates a service-linked role: our scaling policy call failed once (`ServiceLinkedRoleFailure`) and the group launched nothing for about 2 minutes until we set the desired capacity again, so allow for a slow first start. After terminating one building by hand, the group noticed and started a replacement in about **1 min 45 s**. `desired 3` above `max 2` is refused (`New SetDesiredCapacity value 3 is above max value 2`), deleting a group with instances fails (`ResourceInUse`). The **target tracking policy at 40% CPU** (load from `stress-ng`) added a building about **6.5 minutes** after the load started, and later removed one when the load was gone (alarm `AlarmLow`).
> - **Max size is 2, not 3, in our run**, because a new account has a 5 vCPU limit and a t3.micro uses 2.
> - Not tested: the console screens, real prices.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 30 min, Part C 40 min |
| **Cost** | Free here. On real AWS, volumes and snapshots bill while they exist, and so do buildings; the cleanup in the script and below matters. |
| **Skill check before you start** | Session 5B (disks, `mkfs`, `fstab`, LVM), Session 8 (the emulator setup, instances). |

## Before you start

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(This starts the emulator and an `aws` wrapper that runs in Docker. Run `docker rm -f floci-lab` when you finish. See the Session 8 guide for details.) `lab_files/ebs_asg_demo.sh` runs all of Parts A and C in one go; read it, then run it.

---

## Part A: the storeroom attached to a building (Episodes 1 and 2)

### A1. The same-tower rule

```bash
I=$(aws ec2 run-instances --image-id ami-ubuntu2404-arm64 --instance-type t4g.micro --query 'Instances[0].InstanceId' --output text)
AZ=$(aws ec2 describe-instances --instance-ids $I --query 'Reservations[0].Instances[0].Placement.AvailabilityZone' --output text)
V0=$(aws ec2 create-volume --volume-type gp3 --size 8 --availability-zone us-east-1a --query VolumeId --output text)
aws ec2 attach-volume --volume-id $V0 --instance-id $I --device /dev/sdf
```

(We chose a zone different from the building's.) Expected (ours): `InvalidParameterValue ... The volume 'vol-...' and instance 'i-...' must be in the same Availability Zone`. This is the script's warning, **reproduced**: "same AZ ka dhyaan rakho, warna attach hi nahi hoga". Now the right zone:

```bash
V=$(aws ec2 create-volume --volume-type gp3 --size 8 --availability-zone $AZ --query VolumeId --output text)
aws ec2 describe-volumes --volume-ids $V --query 'Volumes[0].[VolumeType,Size,State,Iops,Throughput]' --output text
aws ec2 attach-volume --volume-id $V --instance-id $I --device /dev/sdf --query State --output text
aws ec2 describe-volumes --volume-ids $V --query 'Volumes[0].[State,Attachments[0].Device]' --output text
```

We saw `gp3 8 available None 125` (the emulator filled in 125 MB/s throughput and no IOPS value, which is its own default), `attaching`, then `in-use /dev/sdf`. The state moves `available` → `in-use`, as in the script's picture.

### A2. Snapshots: not tested

`aws ec2 create-snapshot --volume-id $V` failed in the emulator (`Operation CreateSnapshot is not supported`). Run the script's snapshot lab on a real account: write a file, snapshot, wait for `Completed`, create a volume from it in the **same tower**, attach, mount at `/restore`, read the file, then delete the extra volume and the snapshot.

### A3. The Linux half, tested for real

On a real building the commands are `lsblk`, `blkid`, `mkfs -t ext4`, `mount`, an `fstab` line with `nofail`, and a restore test. We ran the **same Linux commands** in the practice container from Session 5/6 (privileged, run as root), with a 200 MB file attached as a loop device instead of an EBS volume (`lab_files/ebs_local_demo.sh`):

```bash
docker cp lab_files/ebs_local_demo.sh atithi-web1:/tmp/
docker exec -u root atithi-web1 bash /tmp/ebs_local_demo.sh
```

What we saw:

- `blkid` on the empty disk printed nothing and exited `2`. **Empty means it is safe to format**, which is why the script says to check first.
- After `mkfs -t ext4` and `mount`: `/dev/loop0 172M 24K 158M 1% /data`.
- With the fstab line `UUID=... /data ext4 defaults,nofail 0 2`, then `umount /data` and `mount -a`, the file came back: `after umount + mount -a: important`.
- A **copy of the disk image** (our stand-in for "snapshot, then new volume") mounted at `/restore` showed `restore test: important`. Its UUID was the same as the original's. Both mounted without trouble on ext4. (On XFS a second disk with the same UUID usually needs `-o nouuid` to mount at the same time; we did not test XFS here.)
- Everything was cleaned up, and `losetup -a` showed no devices left.

**Check yourself:**

- [ ] You saw the same-tower error and know the fix.
- [ ] You can say what an empty `blkid` means, and why `nofail` is in the `fstab` line.
- [ ] You know which snapshot steps you still have to do on a real account.

---

## Part B: images (Episode 3)

Building an AMI from a running building (`aws ec2 create-image`) is **not supported** by the emulator we used, so the script's lab (nginx, create image `atithi-web-v1`, launch from "My AMIs", then deregister and delete the snapshot) is a real-account lab.

Things from the script to do there, and watch for: the new building shows the page with **no user data**; **deregistering the AMI does not delete its snapshot** (delete it separately, or the storage bill continues); put a version in the AMI name (`-v1`).

We also learned something from the emulator's image list: AMIs have an **architecture**. `ami-ubuntu2404-arm64` only runs on ARM families (`t4g`), and an x86 image such as `ami-ubuntu2404-amd64` on `t3` (see the Session 8 guide). Remember this when you build an AMI: it carries the architecture of the building you made it from.

---

## Part C: Auto Scaling (Episode 4)

### C1. Template, group and policy

```bash
aws ec2 create-launch-template --launch-template-name atithi-web --launch-template-data '{"ImageId":"ami-ubuntu2404-arm64","InstanceType":"t4g.micro"}'
SUBS=$(aws ec2 describe-subnets --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')
aws autoscaling create-auto-scaling-group --auto-scaling-group-name atithi-asg \
  --launch-template LaunchTemplateName=atithi-web,Version='$Latest' --min-size 1 --max-size 3 --desired-capacity 1 --vpc-zone-identifier "$SUBS"
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names atithi-asg \
  --query 'AutoScalingGroups[0].Instances[].[InstanceId,LifecycleState,HealthStatus,AvailabilityZone]' --output text
aws autoscaling put-scaling-policy --auto-scaling-group-name atithi-asg --policy-name cpu40 --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":40}'
```

Expected (ours): a launch template id (`lt-...`), one instance (`InService Healthy`, in one of the two towers), and the policy ARN `...scalingPolicy:atithi-asg:cpu40`. The group spreads buildings over the subnets (towers) you list. **Creating the policy is all we could do:** nothing pushed CPU over 40%, so we did not see a scale-out by the policy itself (the script's `stress` lab).

### C2. Scale, lose a building, hit the limits

```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name atithi-asg --desired-capacity 2
# take the first instance id from the describe command, then:
aws ec2 terminate-instances --instance-ids i-...
aws autoscaling describe-scaling-activities --auto-scaling-group-name atithi-asg --query 'Activities[].[StatusCode,Cause]' --output text
aws autoscaling set-desired-capacity --auto-scaling-group-name atithi-asg --desired-capacity 5
```

What we saw:

- After `desired 2`, a second building appeared (`Pending`, then `InService`).
- After we terminated one by hand, the group **made a replacement** within about 20 seconds: two `InService Healthy` buildings again, with different ids. The activity list said `An instance was started in response to a desired capacity change.`
- `desired 5` was refused: `ValidationError ... New DesiredCapacity=5 must be between MinSize=1 and MaxSize=3`.

### C3. Deleting a group the right way

```bash
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name atithi-asg
aws autoscaling update-auto-scaling-group --auto-scaling-group-name atithi-asg --min-size 0 --desired-capacity 0
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name atithi-asg
```

The first delete failed: `ResourceInUse ... Auto Scaling group 'atithi-asg' has 2 instance(s). Set ForceDelete=true`. After scaling to zero, the delete worked. This is the script's cleanup advice: **set desired and minimum to 0, then delete**, or the group keeps making buildings (and rent).

Finally detach and delete the volume, delete the template, terminate the building (`lab_files/ebs_asg_demo.sh` does all of this), and check that `describe-instances` (running) and `describe-volumes` show nothing: we saw `0` and `0`.

**Check yourself:**

- [ ] You saw the group replace a building you terminated.
- [ ] You saw both refusals (above the max, delete with instances).
- [ ] You know that the scaling policy and snapshots are the two things you did not see work.

---

## Clean up

```bash
docker rm -f floci-lab
```

On real AWS: delete the Auto Scaling group first, then the launch template, the AMI **and its snapshot**, extra volumes and snapshots, and the buildings, in every Region you used.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `must be in the same Availability Zone` | Volume and building in different towers | Create the volume in the building's zone |
| `ResourceInUse` deleting a group | It still has buildings | Desired and minimum to 0, then delete |
| `Operation CreateSnapshot is not supported` | The emulator | Use a real account |
| `mount: ... wrong fs type` after `mkfs` | Formatted the wrong device, or not yet formatted | Check `lsblk` and `blkid` first |
| Building will not boot after an `fstab` edit | A bad line without `nofail` | Use `nofail`, test with `mount -a` first |

## What we did not test

- **Snapshots and AMIs:** creation, restore, `Completed` status, deregister, and the leftover snapshot.
- **Real device names,** `nvme1n1`, and the volume types' real speeds.
- **Scaling by the policy itself:** `stress`, CloudWatch CPU, the Activity tab, cooldowns, and the real time it takes.
- **The console** and **real costs.**
