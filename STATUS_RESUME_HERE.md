# Resume here (written 2026-11-20, before a shutdown)

Read this first when you continue. Details of every test are in `progress.md` and in each session's `03_lab_guide.md`.

## State of the world
- **AWS (account profile `atithi-lab`, region ap-south-1): nothing is running.** `_lab_tools/aws/aws_leftovers.sh` printed "NOTHING LEFT. Clean." at 20:28 IST. Credits show 99.94 USD (billing lags). The local key `~/.ssh/atithi-key.pem` is deleted.
- **GitHub: a PUBLIC practice repo is still up: https://github.com/shivamnamdev/atithi-actions-lab** (branch protection on `main`, secret `DEMO_TOKEN`, environment `production`, Dependabot). The user must delete it when Session 20 is finished (the gh token has no delete permission). It contains no real secrets.
- **GCP:** project `project-bdf7ba6f-0ee2-447a-966`, trial credit ends **2027-01-20**, budget `atithi-lab-budget` (INR 1000) exists, nothing created. The working `gcloud` login lives in a TEMPORARY folder (`.../scratchpad/gcp/config`), which a reboot may wipe. After a reboot run `gcloud auth login` again (use `/opt/homebrew/bin/gcloud`, which keeps the login in `~/.config/gcloud`).
- **Azure:** not started on purpose (create the free account only shortly before Session 30).
- Scratch work (Terraform copies, shell helpers) was in the session scratchpad and may be gone after a reboot. Everything worth keeping is already in the course repo.

## Done (tested on real AWS or GitHub, guides updated, committed and pushed)
Sessions 8, 9, 10, 11, 12, 13, 14, 15 (AWS), 27 and 28 (Terraform, incl. a new tested `envs/dev`), and Session 20 on GitHub except OIDC (see below). Earlier sessions (3 to 7, 21 to 26, 29, 31, 31B, 17 to 19) were tested in Docker / emulators.

## Waiting on the user (one action)
Attach the IAM managed policy `atithi-lab-iam-oidc` to `atithi-lab-user`: JSON is `SESSION-20_github-actions-and-devsecops/lab_files/atithi-lab-iam-oidc-policy.json` (provider `token.actions.githubusercontent.com` only; simulator-tested). Previously attached and still needed: `atithi-lab-iam`, `atithi-lab-iam-users`, plus `PowerUserAccess`.

## Next steps, in order
1. **Session 20, finish:** create the OIDC provider and role `atithi-gha-oidc` (trust: `repo:shivamnamdev/atithi-actions-lab:ref:refs/heads/main`, then try another branch and an environment to see it refused), store the role ARN as repo secret `AWS_ROLE_ARN`, run workflow `aws-oidc` (check the account id is masked in the public log), remove role + provider with the cleanup script (add IAM OIDC providers and `atithi-gha-*` roles to it first; roles are already handled). Then write `SESSION-20_github-actions-and-devsecops/03_lab_guide.md` from `progress.md` (all other parts are already tested) and ask the user to delete the repo.
2. Guides for **Sessions 16 and 16B** (Git/GitHub and team workflows; test for real on GitHub with the same account), then **01 and 02**, then **30 (Azure)**, **32 and 33 (AI, Claude API via Console with a spend limit)**.
3. **GCP / GKE (Session 24)**: re-login to gcloud, enable the GKE API quota check, cluster created and deleted the same day, extend the cleanup tooling for GCP (a `_lab_tools/gcp` pair like the AWS one).
4. Open question from the user: a recorded demo using the real console (user drives the console on camera, Claude verifies by CLI in parallel; pilot idea: the Session 8 launch wizard).
5. Housekeeping: AD-001 / AD-002 ad scripts still say "33 sessions / 132 episodes".

## Rules that still apply
Confirm before creating anything that bills; delete the same day; never print secrets; only `atithi-*` names and tag `Project=atithi-lab`; IAM names starting `atithi-lab` are protected by the cleanup script (the user's own permissions); the user's four existing S3 buckets and CloudFront distribution E2RXVOTPHG2SRH must never be touched.
