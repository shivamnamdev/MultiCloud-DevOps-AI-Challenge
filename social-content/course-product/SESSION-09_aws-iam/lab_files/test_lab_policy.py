"""Checks atithi-lab-iam-policy.json with the IAM policy simulator (works on the practice emulator or real AWS).
Usage: put the policy on a throwaway user, then:  python3 test_lab_policy.py USER_ARN [ACCOUNT_ID]"""
import json, subprocess, sys
user = sys.argv[1]
acct = sys.argv[2] if len(sys.argv) > 2 else "123456789012"
R = lambda kind, name: f"arn:aws:iam::{acct}:{kind}/{name}"
def ctx(k, v): return [f"ContextKeyName={k},ContextKeyValues={v},ContextKeyType=string"]
cases = [
 ("create a role named atithi-*",              "iam:CreateRole", R("role","atithi-ec2-s3"), [], "allowed"),
 ("create a role with another name",           "iam:CreateRole", R("role","other-role"), [], "implicitDeny"),
 ("delete an atithi-* role",                   "iam:DeleteRole", R("role","atithi-ec2-s3"), [], "allowed"),
 ("delete someone else's role",                "iam:DeleteRole", R("role","OrganizationAccountAccessRole"), [], "implicitDeny"),
 ("attach S3ReadOnly to an atithi-* role",     "iam:AttachRolePolicy", R("role","atithi-ec2-s3"), ctx("iam:PolicyARN","arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"), "allowed"),
 ("attach AdministratorAccess to atithi-*",    "iam:AttachRolePolicy", R("role","atithi-ec2-s3"), ctx("iam:PolicyARN","arn:aws:iam::aws:policy/AdministratorAccess"), "implicitDeny"),
 ("attach own atithi-* policy",                "iam:AttachRolePolicy", R("role","atithi-ec2-s3"), ctx("iam:PolicyARN",f"arn:aws:iam::{acct}:policy/atithi-stopdev"), "allowed"),
 ("attach S3ReadOnly to another role",         "iam:AttachRolePolicy", R("role","other-role"), ctx("iam:PolicyARN","arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"), "implicitDeny"),
 ("pass an atithi-* role to EC2",              "iam:PassRole", R("role","atithi-ec2-s3"), ctx("iam:PassedToService","ec2.amazonaws.com"), "allowed"),
 ("pass an atithi-* role to Lambda",           "iam:PassRole", R("role","atithi-lambda"), ctx("iam:PassedToService","lambda.amazonaws.com"), "allowed"),
 ("pass an atithi-* role to Glue",             "iam:PassRole", R("role","atithi-ec2-s3"), ctx("iam:PassedToService","glue.amazonaws.com"), "implicitDeny"),
 ("pass another role to EC2",                  "iam:PassRole", R("role","other-role"), ctx("iam:PassedToService","ec2.amazonaws.com"), "implicitDeny"),
 ("create an atithi-* instance profile",       "iam:CreateInstanceProfile", R("instance-profile","atithi-ec2-s3"), [], "allowed"),
 ("create another instance profile",           "iam:CreateInstanceProfile", R("instance-profile","prod-profile"), [], "implicitDeny"),
 ("create an atithi-* policy",                 "iam:CreatePolicy", R("policy","atithi-stopdev"), [], "allowed"),
 ("list roles (read)",                         "iam:ListRoles", "*", [], "allowed"),
 ("create a user",                             "iam:CreateUser", R("user","anyone"), [], "implicitDeny"),
 ("create an access key",                      "iam:CreateAccessKey", R("user","anyone"), [], "implicitDeny"),
 ("put an inline policy on an atithi-* role",  "iam:PutRolePolicy", R("role","atithi-ec2-s3"), [], "implicitDeny"),
 ("attach a policy to a user",                 "iam:AttachUserPolicy", R("user","anyone"), [], "implicitDeny"),
]
bad = 0
for label, action, res, ctxs, want in cases:
    cmd = ["aws","iam","simulate-principal-policy","--policy-source-arn",user,"--action-names",action,"--resource-arns",res,
           "--query","EvaluationResults[0].EvalDecision","--output","text"]
    for c in ctxs: cmd += ["--context-entries", c]
    got = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    ok = got == want; bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {label:44} {got}")
print("all as expected" if not bad else f"{bad} unexpected answers")
