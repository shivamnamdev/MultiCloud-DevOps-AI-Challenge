# Resume here (updated 2026-11-23)

Read this first when you continue. Details of every test are in `progress.md` and in each session's `03_lab_guide.md`.

## State of the world
- **AWS (profile `atithi-lab`, ap-south-1): nothing is running.** `_lab_tools/aws/aws_leftovers.sh` was clean at the end of the Session 20 test. The OIDC provider and role were created and deleted. Credits 99.67 USD (billing lags).
- **GitHub: a PUBLIC practice repo is still up: https://github.com/shivamnamdev/atithi-actions-lab** (branch protection on `main`, secret `DEMO_TOKEN`, environment `production`). It has no real secrets and no account number in any log (we deleted the one run that exposed it). The user must delete it when finished with Sessions 16/16B too (`gh auth refresh -s delete_repo`, then `gh repo delete`).
- **Docker Desktop was NOT running after the restart** (start it before any Docker-based lab).
- **GCP:** project `project-bdf7ba6f-0ee2-447a-966`, trial credit ends **2027-01-20**, budget `atithi-lab-budget` (INR 1000), nothing created. Homebrew `gcloud` has no login yet: run `/opt/homebrew/bin/gcloud auth login` in the user's own Terminal.
- **Azure:** not started on purpose (create the free account only shortly before Session 30).

## Done (tested on real AWS or GitHub, guides updated, committed and pushed)
Sessions 8 to 15 (AWS), 20 (GitHub Actions, OIDC to AWS: guide written), 27 and 28 (Terraform, incl. a tested `envs/dev`). Earlier sessions (3 to 7, 17 to 19, 21 to 26, 29, 31, 31B) were tested in Docker / emulators.
Key corrections found by real runs are recorded inside each guide (for example, GitHub's OIDC `sub` now contains owner and repo IDs; the S20 script was fixed).

## Next steps, in order
1. Guides for **Sessions 16 and 16B** (Git/GitHub and team workflows): test for real on GitHub with the same practice repo or a new one (branch protection, PR reviews, CODEOWNERS, issues, Dependabot). Then **01 and 02**, then **30 (Azure)**, **32 and 33 (AI, Claude API via Console with a spend limit)**.
2. **GCP / GKE (Session 24)**: re-login to gcloud, cluster created and deleted the same day, and a `_lab_tools/gcp` cleanup pair like the AWS one.
3. Open idea from the user: a recorded demo using the real console (user drives the console on camera, Claude verifies by CLI in parallel; pilot: the Session 8 launch wizard).
4. Housekeeping: AD-001 / AD-002 ad scripts still say "33 sessions / 132 episodes".

## Rules that still apply
Confirm before creating anything that bills; delete the same day; never print secrets; only `atithi-*` names and tag `Project=atithi-lab`; IAM names starting `atithi-lab` are protected by the cleanup script (the user's own permissions); the user's four existing S3 buckets and CloudFront distribution E2RXVOTPHG2SRH must never be touched.
