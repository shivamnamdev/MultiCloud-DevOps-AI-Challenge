# Resume here (updated 2026-11-24, after Sessions 01, 02, 16, 16B, 24, 30, 32 and 33)

Read this first when you continue. Details of every test are in `progress.md` and in each session's `03_lab_guide.md`.

## State of the world
- **AWS (profile `atithi-lab`, ap-south-1): nothing is running.** `_lab_tools/aws/aws_leftovers.sh` was clean at the end of the Session 20 test. The OIDC provider and role were created and deleted. Credits 99.67 USD (billing lags).
- **GitHub: TWO PUBLIC practice repos (atithi-booking also got a PR template, k8s/rooms.yaml and html-check from S02) are still up: https://github.com/shivamnamdev/atithi-actions-lab (S20) and https://github.com/shivamnamdev/atithi-booking (S16B, branch protection + required check `html-check`).** (Do NOT delete `shivamnamdev/Spoon-Knife`: it is the user's own old fork from 2017.)  (branch protection on `main`, secret `DEMO_TOKEN`, environment `production`). It has no real secrets and no account number in any log (we deleted the one run that exposed it). The user now has the `delete_repo` scope; ask before deleting (`gh repo delete shivamnamdev/atithi-actions-lab --yes`, same for atithi-booking).
- **Docker Desktop was NOT running after the restart** (start it before any Docker-based lab).
- **GCP:** project `project-bdf7ba6f-0ee2-447a-966`, trial credit ends **2027-01-20**, budget `atithi-lab-budget` (INR 1000). gcloud is logged in; `gke-gcloud-auth-plugin` installed (add `/opt/homebrew/share/google-cloud-sdk/bin` to PATH). Session 24 Part D done and cleaned up; nothing of ours runs. The stray 10 GB `vm-securehost` snapshot (default snapshot schedule, 2026-11-02) was deleted on the user's request on 2026-11-24; the empty schedule `default-schedule-1` remains and is free...` (from the default snapshot schedule, 2026-11-02) is not ours and was left alone. Check with `_lab_tools/gcp/gcp_leftovers.sh`.
- **Azure:** account created and Session 30 tested; nothing billable is running (only the DevOps-created `VisualStudioOnline-*` group and free `NetworkWatcherRG`). **No Azure budget exists yet** (user to create one). Azure DevOps org `shivam-atithi-lab-org`, private project `atithi-booking` (repo, pipeline `rooms-service`, envs dev/prod, branch policy) are kept. The user must revoke the 7-day PAT in the portal.

## Done (tested on real AWS or GitHub, guides updated, committed and pushed)
Sessions 1 and 2 (guides + lab files; no hypervisor installed, no AI product tested), 8 to 15, 32 and 33 (local Docker + kind; NO real LLM call, no EKS; fake provider for SDK retries; MCP hatch tested with the SDK client) (AWS), 16 and 16B (Git and GitHub: guides + self-check script), 20 (GitHub Actions, OIDC to AWS: guide written), 27 and 28 (Terraform, incl. a tested `envs/dev`). Earlier sessions (3 to 7, 17 to 19, 21 to 26, 29, 31, 31B) were tested in Docker / emulators.
Key corrections found by real runs are recorded inside each guide (for example, GitHub's OIDC `sub` now contains owner and repo IDs; the S20 script was fixed).

## Next steps, in order
0. Docker-only audit (2026-11-24): done so far = Session 05B on a real Rocky VM. Remaining plan: (2) one GKE run for Sessions 23, 25, 26; (3) GitHub + AWS pass for 17, 18, 19, 22, 31; (4) recorded console demo. Groups 1 also still has Ubuntu-VM-only bits of Sessions 3, 4, 5, 6 (real boot, netplan, swap pressure, logrotate, passphrase key).
1. **Skipped by the user's choice (2026-11-24); do it only if a demo video needs it:** one real Claude API call for Session 32 Part F (needs the user's Console key with a spend limit; nothing real was called so far).
2. ~~GCP / GKE (Session 24)~~ done 2026-11-24 (with `_lab_tools/gcp` pair). Remaining ideas: other sessions that touch GCP, and the open recorded-demo idea below.
3. Open idea from the user: a recorded demo using the real console (user drives the console on camera, Claude verifies by CLI in parallel; pilot: the Session 8 launch wizard).
4. ~~Housekeeping: ad scripts~~ done 2026-11-24: AD-001 now says 35 sessions + 1 optional bonus / 140 episodes / ~35 h (still planned figures, verify against final recordings); AD-002 has no counts.

## Rules that still apply
Confirm before creating anything that bills; delete the same day; never print secrets; only `atithi-*` names and tag `Project=atithi-lab`; IAM names starting `atithi-lab` are protected by the cleanup script (the user's own permissions); the user's four existing S3 buckets and CloudFront distribution E2RXVOTPHG2SRH must never be touched.
