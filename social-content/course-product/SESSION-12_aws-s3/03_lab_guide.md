# Session 12 lab guide: AWS S3

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Everything below ran against `floci`, a free program that imitates AWS on your own machine. It is **not** S3. It is good for practising the commands and for seeing the shape of the answers. Where it differs from real S3, this guide says so.
> - **Worked as the script says:** keys and prefixes, `cp`, `ls`, `sync` (and the danger of `--delete`), `head-object`, versioning with a delete marker brought back, a lifecycle rule saved and read back, storage class on upload, a bucket policy saved and read back, a **presigned URL that really expires**, a CloudFront distribution and an invalidation (API only), emptying a versioned bucket.
> - **Did NOT behave like S3:** it did **not** refuse a request for a private object without a signature (we got `200`, the script expects `AccessDenied`), it did **not** enforce the HTTPS-only Deny, and the default encryption did not show on objects. CloudFront deployed and invalidated **instantly**, not in minutes.
> - **Not tested at all:** the console, real durability and availability (an idea, not a command), costs, replication, an EC2 role reading a bucket, OAC with a real bucket policy, the CloudFront URL in a browser, a custom domain, certificates, static website hosting served over HTTP.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 35 min, Part C 35 min, Part D 30 min |
| **Cost** | Free here. Real S3 bills for storage, requests and data out. Delete test buckets, including every old version. |
| **Skill check before you start** | Sessions 8 and 9 (the emulator setup, IAM policies and ARNs). Docker installed. |

## Before you start

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(See the Session 8 guide for what this does. Run `docker rm -f floci-lab` when you finish.) The AWS command runs inside a container that can see **only your current folder**, so keep your files, and any `file://...` JSON, in the folder where you run the command. `lab_files/s3_demo.sh` runs a tidy version of Parts A to D.

---

## Part A: the first warehouse (Episode 1)

### A1. Boxes, labels and prefixes

```bash
B=atithi-photos-asha-1                         # bucket names are unique worldwide: add your own name
aws s3 mb s3://$B
echo "room 101" > front.txt
aws s3 cp front.txt s3://$B/rooms/101/front.txt
aws s3 ls s3://$B/ --recursive
aws s3 ls s3://$B/
aws s3 ls s3://$B/rooms/
aws s3api put-object --bucket $B --key empty-folder/
aws s3api list-objects-v2 --bucket $B --prefix empty-folder/ --query 'Contents[].[Key,Size]' --output text
```

Expected (ours): `rooms/101/front.txt` with `9` bytes; `aws s3 ls s3://$B/` showed `PRE rooms/`, and `.../rooms/` showed `PRE 101/`. `PRE` is "prefix", not a folder. The script's point, shown: the key `rooms/101/front.txt` is one label. The "folder" you create in the console is a zero-byte key that ends with `/`: ours listed as `empty-folder/ 0`.

### A2. `sync`, and what `--delete` really deletes

```bash
mkdir -p photos/101 photos/102; echo a > photos/101/a.txt; echo b > photos/102/b.txt
aws s3 sync ./photos s3://$B/rooms/
aws s3 sync ./photos s3://$B/rooms/ --delete --dryrun
```

The first sync uploaded the two files. Run it again a few seconds later: nothing is uploaded if nothing changed. (Run it again **immediately** and our emulator uploaded the files a second time: its clock and your file's clock were within the same second. Real S3 timestamps differ, so do not read much into that.) When we changed `a.txt` the next sync picked up only that file.

Now the dry run with `--delete`, which is the lesson:

```
(dryrun) upload: photos/101/a.txt to s3://.../rooms/101/a.txt
(dryrun) delete: s3://.../rooms/101/front.txt
(dryrun) upload: photos/102/b.txt to s3://.../rooms/102/b.txt
```

`--delete` removes **every object under that prefix that is not in your local folder**, including `rooms/101/front.txt`, which we had uploaded earlier with `cp`. Real run: it was deleted. The script's sentence "jo box local folder mein nahi hai, use godown se bhi hata do" is literal. **Always run `--dryrun` first.** (We used `--dryrun` with `sync`; the AWS CLI lists it as an option of `cp`, `mv`, `rm` and `sync`, which we did not try.)

### A3. A box's information, without downloading it

```bash
aws s3api head-object --bucket $B --key rooms/101/front.txt --query '[ContentLength,ContentType,StorageClass]' --output text
```

Expected: `9 text/plain STANDARD`. `aws s3` is the everyday tool; `aws s3api` is one S3 API call at a time.

### A4. The default answer is "no"

The script opens an object's URL in the browser and expects `AccessDenied`. **We could not reproduce that.** Our emulator answered a plain, unsigned URL for a private object with `200` and the file's contents. On real S3 a private bucket with Block Public Access on answers `403 AccessDenied`. Try it on a real bucket.

Block Public Access itself we could set and read back:

```bash
aws s3api put-public-access-block --bucket $B --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api get-public-access-block --bucket $B --query PublicAccessBlockConfiguration --output text
```

Expected: `True True True True`.

**Check yourself:**

- [ ] You can say why `rooms/` is not a folder.
- [ ] You ran `sync --delete --dryrun` and read what it would delete.

---

## Part B: undo, and the slow slide to cheaper shelves (Episode 2)

### B1. Versioning and delete markers

```bash
aws s3api put-bucket-versioning --bucket $B --versioning-configuration Status=Enabled
echo v1 > note.txt; aws s3 cp note.txt s3://$B/
echo v2 > note.txt; aws s3 cp note.txt s3://$B/
aws s3api list-object-versions --bucket $B --prefix note.txt --query 'Versions[].[VersionId,IsLatest,Size]' --output text
aws s3 rm s3://$B/note.txt
aws s3 ls s3://$B/note.txt
aws s3api list-object-versions --bucket $B --prefix note.txt --query '{Versions:length(Versions),DeleteMarkers:length(DeleteMarkers)}' --output text
M=$(aws s3api list-object-versions --bucket $B --prefix note.txt --query 'DeleteMarkers[0].VersionId' --output text)
aws s3api delete-object --bucket $B --key note.txt --version-id $M
aws s3 ls s3://$B/note.txt
aws s3 cp s3://$B/note.txt -
```

What we saw: two versions with different ids (one `IsLatest True`); after `aws s3 rm`, `ls` showed **nothing**, but there were still `2` versions and `1` delete marker; after deleting the marker's version id, the file was back and `aws s3 cp ... -` printed `v2`. That is the script's "undo" lab, step for step.

### B2. A lifecycle rule

`lab_files/lifecycle.json` has one rule: objects under `rooms/` go to `STANDARD_IA` after 30 days, and old versions are removed after 60.

```bash
aws s3api put-bucket-lifecycle-configuration --bucket $B --lifecycle-configuration file://lifecycle.json
aws s3api get-bucket-lifecycle-configuration --bucket $B --query 'Rules[0].[ID,Filter.Prefix,Transitions[0].Days,Transitions[0].StorageClass,NoncurrentVersionExpiration.NoncurrentDays]' --output text
```

Expected (ours): `thirty-days-to-IA rooms/ 30 STANDARD_IA 60`. The emulator also printed `"TransitionDefaultMinimumObjectSize": "all_storage_classes_128K"`: a hint that real S3 has a minimum object size rule for transitions. We did not check it. **The emulator never actually moves objects**: it stores the rule. The script's real wait ("30 din baad") cannot be tested here.

A storage class chosen at upload time:

```bash
echo cold > old.txt
aws s3 cp old.txt s3://$B/archive/old.txt --storage-class STANDARD_IA
aws s3api head-object --bucket $B --key archive/old.txt --query StorageClass --output text
```

Expected: `STANDARD_IA`.

### B3. Emptying a versioned bucket

```bash
aws s3 rb s3://$B
aws s3 rb s3://$B --force
```

We tried both on a bucket with versions. Both failed with **`BucketNotEmpty`**. `--force` deleted the visible objects, but the old versions and delete markers stayed (we counted 7 versions and 6 markers left). The script's warning ("versioning on ho to saare versions bhi hatane padte hain") is right. `lab_files/empty_versioned_bucket.sh BUCKET` lists every version and marker and deletes them with `delete-objects`, then removes the bucket. It worked: `remove_bucket: ...`. **Read the bucket name twice: this is permanent.** (A lifecycle rule that expires old versions is the gentle way on a real bucket.)

**Check yourself:**

- [ ] You deleted a file and brought it back with a version id.
- [ ] You know why `rb --force` was not enough.

---

## Part C: locks and sharing (Episode 3)

### C1. A bucket policy

`https-only.json` (from the script, with your bucket name in place of `BUCKET`) denies any request that is not over HTTPS:

```bash
cat > https-only.json <<EOF
{"Version":"2012-10-17","Statement":[{"Sid":"DenyInsecure","Effect":"Deny","Principal":"*","Action":"s3:*",
 "Resource":["arn:aws:s3:::$B","arn:aws:s3:::$B/*"],"Condition":{"Bool":{"aws:SecureTransport":"false"}}}]}
EOF
aws s3api put-bucket-policy --bucket $B --policy file://https-only.json
aws s3api get-bucket-policy --bucket $B --query Policy --output text
```

Expected (ours): the same JSON back, with `Effect Deny`, `Action s3:*` and the condition `aws:SecureTransport false`. Notice the two resource lines, bucket and `bucket/*`: the same two ARNs as in Session 9. **We could not test that the Deny blocks a request**: the emulator answered plain `http` requests normally.

### C2. Presigned URLs

```bash
U=$(aws s3 presign s3://$B/rooms/101/c.txt --expires-in 300)
echo "$U" | tr '?&' '\n\n'
```

The link is the object's address plus `X-Amz-Algorithm`, `X-Amz-Credential`, `X-Amz-Date`, `X-Amz-Expires`, `X-Amz-SignedHeaders` and `X-Amz-Signature`. (Treat it like a password until it expires.) Fetch it from inside the emulator's Docker network, because its address is the emulator's:

```bash
docker run --rm --network awslab curlimages/curl -s -w ' [%{http_code}]' "$U"
U2=$(aws s3 presign s3://$B/rooms/101/c.txt --expires-in 3); sleep 5
docker run --rm --network awslab curlimages/curl -s -w ' [%{http_code}]' "$U2"
```

Expected (ours): the first returned the file's content and `[200]`. The 3-second link, fetched after 5 seconds: `<Error><Code>AccessDenied</Code><Message>Request has expired.</Message></Error> [403]`. **The expiry is real**, the script's "paanch minute baad ... Request has expired" confirmed (with 3 seconds, to save time).

### C3. Not tested

The EC2 role reading `rooms/*` (needs a real instance, Session 9's role lab), KMS encryption, Object Lock, replication, S3 access logs, and CloudTrail data events. Default encryption: we read `AES256` as the bucket's default, and the emulator did not show `ServerSideEncryption` on the object itself, so we have **no evidence** for what real objects show.

**Check yourself:**

- [ ] You saw a presigned URL work and then expire.
- [ ] You can say why the policy has two resource lines.
- [ ] You know that the HTTPS-only Deny is untested here.

---

## Part D: the brochure stand (Episode 4)

### D1. Static website settings, and CloudFront, by API

```bash
aws s3api put-bucket-website --bucket $B --website-configuration '{"IndexDocument":{"Suffix":"index.html"},"ErrorDocument":{"Key":"error.html"}}'
aws s3api get-bucket-website --bucket $B --query '[IndexDocument.Suffix,ErrorDocument.Key]' --output text
OAC=$(aws cloudfront create-origin-access-control --origin-access-control-config Name=atithi-oac,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3 --query OriginAccessControl.Id --output text)
```

Website settings read back as `index.html error.html`. The origin access control got an id. Then a distribution config (the script's lab: origin is the bucket with origin path `/site`, the OAC, default root object `index.html`, redirect to HTTPS), created with `aws cloudfront create-distribution --distribution-config file://dist.json`. Ours was reported `Deployed` at once with a domain like `ekuevoma79xbkp.cloudfront.net`. (Real distributions take minutes, and you must paste the bucket policy CloudFront gives you, which we did not.) We built `dist.json` (see `lab_files/dist.json.example`, replace `BUCKET` and `OAC_ID`) with the field names from the AWS CLI reference, `"CachePolicyId":"658327ea-f89d-4fab-a63d-7e88639e58f6"` being AWS's managed "CachingOptimized" policy id, which the emulator accepted. **We never opened the CloudFront URL.**

### D2. Invalidation

```bash
aws cloudfront create-invalidation --distribution-id $DID --invalidation-batch 'Paths={Quantity=1,Items=["/*"]},CallerReference=inv1' --query 'Invalidation.[Id,Status]' --output text
```

Expected (ours): an id and `Completed`. On real CloudFront it starts as `InProgress` and takes a while. The script's other advice (put a version in the file name, `app.3f2a.js`) needs no test.

### D3. Deleting a distribution takes two steps

```bash
aws cloudfront delete-distribution --id $DID --if-match $ETAG
```

First attempt, while enabled: `DistributionNotDisabled`. After `update-distribution` with `Enabled: false` (we edited the config JSON and sent it back with the new ETag), the delete worked. This is the script's "pehle disable karo phir delete karo".

### D4. Clean up

```bash
./empty_versioned_bucket.sh $B
docker rm -f floci-lab
rm -rf photos front.txt note.txt old.txt
```

On real AWS: disable then delete the distribution, empty the bucket **with all versions**, delete it, and check S3, CloudFront and billing again the next day.

**Check yourself:**

- [ ] You know the two steps to delete a distribution.
- [ ] You know what you did **not** see: the page through CloudFront, and the 403 from a private bucket.

---

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `BucketNotEmpty` after `rb --force` | Versions or delete markers remain | `lab_files/empty_versioned_bucket.sh` |
| `sync --delete` removed files you wanted | They were not in the local folder | Always `--dryrun` first |
| `Unable to load paramfile file://...` | The CLI runs in a container that sees only your current folder | Keep the JSON in the folder where you run the command |
| `403` for a file you can see | Missing list permission turns 404 into 403 | Check the policy (Session 9, ARNs) |
| Presigned link stops working | It expired, or the creator lost the permission | Make a new one |
| `DistributionNotDisabled` | Deleting an enabled distribution | Disable it, wait, then delete |

## What we did not test

- **Real S3 behaviour:** `AccessDenied` for private objects, the HTTPS-only Deny, default encryption on objects, real lifecycle transitions, real timestamps in `sync`, replication, and the 11-nines durability (an idea).
- **Real CloudFront:** the URL, caching and TTLs, the `403` for a missing file, the bucket policy for OAC, a custom domain and certificate, and deployment time.
- **An EC2 role reading the bucket,** and **costs.**
