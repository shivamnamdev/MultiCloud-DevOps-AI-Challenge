# Session 09 lab guide: AWS IAM

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Everything below ran against `floci`, a free program that imitates AWS on your own machine. It is **not** AWS, and for IAM that matters a lot:
> - **It does evaluate policies in the policy simulator** (`aws iam simulate-principal-policy`). We used that for the lessons about letters, ARNs, Deny and conditions, and the answers matched the script.
> - **It does NOT enforce permissions on real calls.** A user whose only letter is read-only could still launch an instance with its own key. So we could not see "not authorized" errors.
> - **It does NOT reject an Inactive access key.** After we set a key to Inactive, it still worked. The script's lab ends with `InvalidClientTokenId`; **you will only see that on real AWS.**
> - It does not check **trust policies** (we could assume a role meant for EC2 from a plain user), and it does not track "last used" for keys.
> - Not tested at all: the console, MFA, sign-in with an account alias, IAM Identity Center, the real EC2 role lab, CloudTrail, Access Analyzer, `decode-authorization-message`.
> So: practise the commands and the policy logic here for free, then do the real-enforcement parts on a real account with a throwaway user.

| | |
|---|---|
| **Time** | Part A 20 min, Part B 40 min, Part C 30 min, Part D 30 min |
| **Cost** | Free on the emulator. IAM itself is free on real AWS. |
| **Skill check before you start** | Session 8 (the emulator setup, `aws sts get-caller-identity`), Session 4 (users and groups on Linux). |

## Before you start

```bash
chmod +x lab_files/emulator/*
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(See the Session 8 guide for what these do: they start the emulator and put an `aws` command, which runs in Docker, on your PATH. Run `docker rm -f floci-lab` when you finish.) The JSON files for the letters are in `lab_files/`.

---

## Part A: staff, departments and letters (Episode 1)

### A1. The four commands of the script

```bash
aws iam create-group --group-name Developers
aws iam attach-group-policy --group-name Developers --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess
aws iam create-user --user-name asha-aws
aws iam add-user-to-group --user-name asha-aws --group-name Developers
aws iam list-groups-for-user --user-name asha-aws --query 'Groups[].GroupName' --output text
aws iam list-attached-group-policies --group-name Developers --query 'AttachedPolicies[].PolicyName' --output text
```

Expected (ours): the group ARN `arn:aws:iam::000000000000:group/Developers`, the user ARN `arn:aws:iam::000000000000:user/asha-aws`, then `Developers` and `AmazonEC2ReadOnlyAccess`. The emulator knows the AWS managed policies by their ARN (`aws iam get-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess` returned the name). A console password: `aws iam create-login-profile --user-name asha-aws --password '...' --password-reset-required`. We ran it, and it worked. We did not sign in: there is no console.

Note the name `asha-aws`, not `asha`: the Linux user from Session 4 and the IAM user are different people in different registers.

### A2. Does the letter really apply?

The simulator is how you ask "would this person be allowed to do this?" without trying it:

```bash
U=arn:aws:iam::000000000000:user/asha-aws
aws iam simulate-principal-policy --policy-source-arn $U --action-names ec2:DescribeInstances --query 'EvaluationResults[0].EvalDecision' --output text
aws iam simulate-principal-policy --policy-source-arn $U --action-names ec2:RunInstances --query 'EvaluationResults[0].EvalDecision' --output text
```

Expected (ours): `allowed` for `DescribeInstances` and `implicitDeny` for `RunInstances`: the read-only group letter lets Asha look and not launch. `implicitDeny` is the "everything is denied by default" of Episode 2.

**Check yourself:**

- [ ] You attached the letter to a group, not to the user.
- [ ] You can say what `implicitDeny` means.

---

## Part B: the letter's JSON (Episode 2)

### B1. The least-privilege bucket letter, and the two ARNs

`lab_files/bucket-letter.json` is the script's letter (allow `s3:ListBucket` and `s3:GetObject` on the bucket **and** on the objects):

```bash
P=$(aws iam create-policy --policy-name bucket-read-letter --policy-document file://lab_files/bucket-letter.json --query Policy.Arn --output text)
aws iam attach-user-policy --user-name asha-aws --policy-arn $P
for a in s3:GetObject s3:DeleteObject; do
  printf "%s: " $a
  aws iam simulate-principal-policy --policy-source-arn $U --action-names $a --resource-arns arn:aws:s3:::my-test-bucket/room.jpg --query 'EvaluationResults[0].EvalDecision' --output text
done
```

Expected (ours): `s3:GetObject: allowed` and `s3:DeleteObject: implicitDeny` (it is not in the letter). That is the script's Policy Simulator lab.

Now the mistake the script warns about. `lab_files/objects-only.json` lists the same two actions, but only `arn:aws:s3:::only-objects/*` as the resource:

```bash
aws iam create-user --user-name tmp-user
P2=$(aws iam create-policy --policy-name objects-only --policy-document file://lab_files/objects-only.json --query Policy.Arn --output text)
aws iam attach-user-policy --user-name tmp-user --policy-arn $P2
T=arn:aws:iam::000000000000:user/tmp-user
aws iam simulate-principal-policy --policy-source-arn $T --action-names s3:GetObject --resource-arns arn:aws:s3:::only-objects/a.jpg --query 'EvaluationResults[0].EvalDecision' --output text
aws iam simulate-principal-policy --policy-source-arn $T --action-names s3:ListBucket --resource-arns arn:aws:s3:::only-objects --query 'EvaluationResults[0].EvalDecision' --output text
```

Expected (ours): `allowed` for the object, and **`implicitDeny` for listing the bucket**. With only the `/*` line, boxes open but the warehouse cannot be listed. This is "ek ko chhodoge to ya list nahi chalegi ya objects nahi khulenge", reproduced.

### B2. An explicit Deny wins

```bash
aws iam put-user-policy --user-name asha-aws --policy-name deny-get --policy-document file://lab_files/deny.json
aws iam simulate-principal-policy --policy-source-arn $U --action-names s3:GetObject --resource-arns arn:aws:s3:::my-test-bucket/room.jpg --query 'EvaluationResults[0].EvalDecision' --output text
aws iam delete-user-policy --user-name asha-aws --policy-name deny-get
```

Expected (ours): **`explicitDeny`**, even though the bucket letter allows `GetObject`. (Without the Deny it said `allowed`.) The three answers `allowed`, `implicitDeny` and `explicitDeny` are the three outcomes of the script's flowchart.

### B3. A condition: MFA

`lab_files/mfa.json` allows `ec2:StopInstances` only when `aws:MultiFactorAuthPresent` is `true`.

```bash
P3=$(aws iam create-policy --policy-name stop-with-mfa --policy-document file://lab_files/mfa.json --query Policy.Arn --output text)
aws iam attach-user-policy --user-name asha-aws --policy-arn $P3
for v in true false; do
  printf "MFA %s: " $v
  aws iam simulate-principal-policy --policy-source-arn $U --action-names ec2:StopInstances --resource-arns '*' \
    --context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=$v,ContextKeyType=boolean \
    --query 'EvaluationResults[0].EvalDecision' --output text
done
aws iam simulate-principal-policy --policy-source-arn $U --action-names ec2:StopInstances --resource-arns '*' --query 'EvaluationResults[0].EvalDecision' --output text
```

Expected (ours): `MFA true: allowed`, `MFA false: implicitDeny`, and with no MFA information at all, `implicitDeny`. The letter is sharp or loose depending on the Condition. (A mistake we made while testing: leaving out `--resource-arns '*'` gave `implicitDeny` even with MFA true.)

### B4. Not tested

The permissions boundary and service control policies (names only, in the script, and we did not try them), resource-based policies with `Principal` (the S3 session), and the five-suspect hunt for `AccessDenied` (the simulator answers "what would happen", not "which policy blocked me": `MatchedStatements` came back empty in our output, so do not rely on it with the emulator).

**Check yourself:**

- [ ] You reproduced `allowed`, `implicitDeny` and `explicitDeny`.
- [ ] You saw a missing bucket ARN stop `ListBucket`.
- [ ] You saw an MFA condition change the answer.

---

## Part C: roles and temporary credentials (Episode 3)

### C1. A role for EC2

`lab_files/trust-ec2.json` is the trust policy: "the EC2 service may wear this badge".

```bash
aws iam create-role --role-name ec2-s3-read --assume-role-policy-document file://lab_files/trust-ec2.json --query Role.Arn --output text
aws iam attach-role-policy --role-name ec2-s3-read --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam create-instance-profile --instance-profile-name ec2-s3-read
aws iam add-role-to-instance-profile --instance-profile-name ec2-s3-read --role-name ec2-s3-read
aws iam get-role --role-name ec2-s3-read --query 'Role.AssumeRolePolicyDocument.Statement[0].Principal'
```

Expected (ours): the role ARN, `{"Service": "ec2.amazonaws.com"}`, and the instance profile `arn:aws:iam::000000000000:instance-profile/ec2-s3-read`. This is the CLI view of the "wrapper" the script describes: the console makes the instance profile for you, the CLI shows it as a separate step.

### C2. Wear the badge by hand

```bash
aws sts assume-role --role-arn arn:aws:iam::000000000000:role/ec2-s3-read --role-session-name demo
```

What we saw: a `Credentials` block with exactly four keys, `AccessKeyId`, `SecretAccessKey`, `SessionToken` and `Expiration` (about **one hour** after we asked), an access key id starting **`ASIA`** (temporary keys start `ASIA`; permanent user keys start `AKIA`), and `AssumedRoleUser` `arn:aws:sts::000000000000:assumed-role/ec2-s3-read/demo`. Using them:

```bash
AWS_ACCESS_KEY_ID=ASIA... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=... aws sts get-caller-identity
```

gave `arn:aws:sts::000000000000:assumed-role/ec2-s3-read/demo`: the `assumed-role/...` the script says to look for. **The emulator let us assume a role meant for the EC2 service from a plain user. Real AWS checks the trust policy and would refuse.** Treat the trust policy lesson as untested.

### C3. The keyless EC2 lab

Putting the role on a real instance and running `aws s3 ls` without `aws configure` needs a real EC2 instance, so **we did not do it.** Do it on a real account with a short-lived instance, and terminate it after.

**Check yourself:**

- [ ] You can name the two parts of a role (trust, permissions).
- [ ] You saw the four fields of temporary credentials, and `ASIA` against `AKIA`.

---

## Part D: key hygiene (Episode 4)

### D1. Make a key, use it, switch it off

```bash
aws iam create-user --user-name leak-test
aws iam create-access-key --user-name leak-test > key.json
aws iam list-access-keys --user-name leak-test --query 'AccessKeyMetadata[].[Status]' --output text
aws iam update-access-key --user-name leak-test --access-key-id AKIA... --status Inactive
aws iam get-access-key-last-used --access-key-id AKIA...
```

(Use the key id from `key.json`. **Never** commit `key.json`.) What we saw: the key id started `AKIA`, `Status Active`, the identity call with the key worked, and then the key was set to `Inactive`. **The identity call with the Inactive key also still worked**, and "last used" said `{"ServiceName": "N/A", "Region": "N/A"}`. On real AWS the second call fails with `InvalidClientTokenId` (the script's expected result) and "last used" is filled in. We could not see either. Delete the key and the user afterwards.

### D2. The credential report

```bash
aws iam generate-credential-report
aws iam get-credential-report --query Content --output text | base64 -d
```

(Wait a moment after generating.) Expected (ours): a CSV with the header `user,arn,user_creation_time,password_enabled,password_last_used,password_last_changed,password_next_rotation,mfa_active,access_key_1_active,access_key_1_last_rotated,access_key_1_last_used_date,...` and a row per user (`<root_account>`, `asha-aws`, `leak-test`, `tmp-user`). That is the script's `base64 -d` trick, working. `access_key_1_last_used_date` was `N/A` for every user, because the emulator does not track use.

### D3. Not tested

The leak response drill with CloudTrail (the emulator has no real activity log), `aws sts decode-authorization-message`, IAM Access Analyzer, and AWS's own quarantine policy.

### D4. Clean up

```bash
for u in asha-aws leak-test tmp-user; do
  for k in $(aws iam list-access-keys --user-name $u --query 'AccessKeyMetadata[].AccessKeyId' --output text); do
    aws iam delete-access-key --user-name $u --access-key-id $k; done; done
docker rm -f floci-lab
rm -f key.json akey.json assumed.json
```

The emulator forgets everything when it is removed. On real AWS, delete the users, keys, roles, instance profiles and policies you made, and look for keys left in `~/.aws/credentials`.

**Check yourself:**

- [ ] You deactivated a key, and you know that this emulator did not stop it working.
- [ ] You read a credential report.
- [ ] No key file or `assumed.json` is left in your folder.

---

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `NoSuchEntity` from `simulate-principal-policy` | The user does not exist yet | Create it first |
| Simulator says `implicitDeny` for a condition you set | The context key was not passed | `--context-entries ...` and `--resource-arns '*'` |
| `EntityAlreadyExists` | You ran a step twice | Delete first, or restart the emulator |
| `LimitExceeded` on access keys (real AWS) | Two keys per user | Delete one |
| Policy JSON rejected | Missing `Version`, or a trailing comma | `python3 -m json.tool file.json` |

## What we did not test

- **Real enforcement:** `AccessDenied` and "not authorized" for a real call, trust policy checks, Inactive keys failing, and key "last used".
- **The console:** the sign-in URL with the alias, MFA on a user, the Policy Simulator screen, the credential report screen.
- **A real EC2 role:** `assumed-role/ec2-s3-read` seen from inside an instance, and keyless `aws s3 ls`.
- **CloudTrail,** IAM Access Analyzer, permissions boundaries, service control policies, IAM Identity Center.
