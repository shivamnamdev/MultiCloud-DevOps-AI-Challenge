# Session 20 lab guide: GitHub Actions and DevSecOps

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **What was tested, and what was not.**
> Everything below ran for real on GitHub (a free personal account, a **public** practice repo, GitHub-hosted runners) and, for OIDC, on a real AWS account. The numbers and messages are from those runs.
> **Not tested:** self-hosted runners, GitLab CI (`.gitlab-ci.yml` is a paper exercise), a reusable workflow in a second repo, `schedule`, `pull_request_target`, CodeQL and SonarQube, an OIDC role limited to an **environment** instead of a branch, and the console screens (we used the browser-equivalent `gh` commands and the API).

| | |
|---|---|
| **Time** | Part A 30 min, Part B 25 min, Part C 40 min, Part D 30 min |
| **Cost** | GitHub: free. A public repo has no Actions minute charge; a private repo uses your plan's minutes (check the live billing page). AWS: the OIDC provider and role are free; delete them after. |
| **Skill check before you start** | Sessions 16, 16B and 19 (Git, pull requests, required checks) and Session 9 (roles, trust policies). Docker installed (for the local hook test). `gh auth status` must be logged in. |

Starter files are in `lab_files/atithi-actions-lab/` (the exact repo we tested):

```
atithi-actions-lab/
  app.py  test_app.py  requirements.txt  README.md  .gitignore
  .github/dependabot.yml
  .github/workflows/ci.yml         tests (matrix, cache, artifact) + security job
  .github/workflows/deploy.yml     build artifact, then a deploy job behind an approval
  .github/workflows/pr-title.yml   the injection-safe way to use a pull request title
  .github/workflows/aws-oidc.yml   sign in to AWS with no stored key
lab_files/oidc-debug.yml.example   prints the claims of the identity token
lab_files/trust-policy.json.example
lab_files/atithi-lab-iam-oidc-policy.json   lets a restricted lab user create GitHub's OIDC provider only
```

## Before you start

```bash
gh auth status
mkdir atithi-actions-lab && cd atithi-actions-lab
cp -R /path/to/lab_files/atithi-actions-lab/. .
git init -b main && git add -A && git commit -m "practice repo"
gh repo create YOUR-NAME/atithi-actions-lab --public --source=. --push
```

**Public or private?** We used **public**, because *required reviewers on an environment* (Part C) work on a free account only for public repos. A public repo's logs are readable by everyone, so **never print secrets or your AWS account number** (Part C shows how that nearly happened). Delete the repo when you finish.

---

## Part A: the conveyor in the vault (Episode 1)

### A1. The first run

`.github/workflows/ci.yml` is the script's workflow, with the actions **pinned by full commit SHA** (the comment keeps the version):

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
- uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
```

(The script's `@v7` tags exist: checkout v7.0.1, setup-python v7.1.0, upload-artifact v7.0.2, configure-aws-credentials v6.3.0 on the day we tested. Look up the current ones yourself, and let Dependabot, `.github/dependabot.yml`, keep them fresh.)

```bash
gh run list
gh run watch                 # pick the run
gh run view RUN_ID --log
```

What we saw: the push started two runs, `ci` and a **Dependabot** run (that is the `dependabot.yml` file being read, not your code). `ci` finished green: `test (3.11)` in 12 s, `test (3.12)` in 11 s, `security` in 49 s (it downloads tools).

### A2. Break a test on a branch, and make the check required

```bash
git checkout -b break-a-test
sed -i 's/== 3$/== 4/' test_app.py        # on macOS: sed -i '' ...
git commit -am "break a test" && git push -u origin break-a-test
gh pr create --title "Deliberately broken test" --body "check must go red" --base main
gh pr checks
```

We saw `test (3.11)=FAILURE`, **`test (3.12)=CANCELLED`** (the matrix's `fail-fast` stopped the other job as soon as one failed, the script's `fail-fast` line) and `security=SUCCESS`.

Make the checks required (the same as Settings, Branches, Branch protection rule, "Require status checks"):

```bash
cat > protect.json <<'EOF'
{"required_status_checks":{"strict":false,"contexts":["test (3.11)","test (3.12)","security"]},
 "enforce_admins":true,"required_pull_request_reviews":null,"restrictions":null}
EOF
gh api -X PUT repos/YOU/atithi-actions-lab/branches/main/protection --input protect.json
gh pr view 1 --json mergeStateStatus --jq .mergeStateStatus
gh pr merge 1 --squash
```

Expected: `BLOCKED`, and `gh pr merge` refuses (`To use administrator privileges ... add the --admin flag`). The merge button is grey. (We set `enforce_admins` so that even the repo owner is blocked; a check name is **exactly** the job name, including the matrix part.) Fix the test, push, wait for green, then `gh pr merge 1 --squash --delete-branch`: `mergeStateStatus` becomes `CLEAN`.

(A `git revert` we tried silently did nothing: check `git log` before you trust it.)

### A3. GitLab CI, on paper

Translate `ci.yml` into a `.gitlab-ci.yml` with `stages`, `image: python:3.12`, `script`, and `rules:`. We did not run GitLab. The ideas map one to one (`workflow` to pipeline, `steps` to `script`, `on:` to `rules:`).

**Check yourself:**

- [ ] You read the per-step log of a green run.
- [ ] You saw a red check block a merge, and know why the second matrix job said `cancelled`.
- [ ] You can say what pinning a SHA protects you from.

---

## Part B: fast and clever (Episode 2)

### B1. Cache, concurrency, artifacts

`ci.yml` already has `cache: pip`, a `concurrency` group with `cancel-in-progress`, and `upload-artifact` named `report-${{ matrix.python }}`. Push a harmless change twice, then:

```bash
echo "" >> README.md && git commit -qam "touch" && git push -q       # the second run
gh run view RUN_ID --log | grep -i "cache"
```

Expected: first run, no cache; the second says **`Cache hit for: setup-python-...`** and **`Cache restored successfully`**, and the `test (3.12)` job took 7 s. Now push twice quickly:

```bash
echo a >> README.md; git commit -qam "quick 1"; git push -q
echo b >> README.md; git commit -qam "quick 2"; git push -q
gh run list --workflow ci --limit 3
```

We saw the older run as **`completed cancelled`** and the newer one running: the script's `cancel-in-progress` lab.

Artifacts:

```bash
gh api repos/YOU/atithi-actions-lab/actions/runs/RUN_ID/artifacts --jq '.artifacts[] | "\(.name) \(.size_in_bytes)B expires \(.expires_at)"'
```

Expected: `report-3.11` and `report-3.12` (about 350 bytes each, `retention-days: 3` expires in three days) and also `gitleaks-results.sarif`, which the Gitleaks action uploads on its own (kept 90 days: costs storage, so look at your own settings).

### B2. `needs` and `if`

`deploy.yml` has a `build` job that uploads `dist/` and a `deploy` job with `needs: build` and `if: github.ref == 'refs/heads/main'`. It runs from the **Run workflow** button (`workflow_dispatch`); Part C uses it.

### B3. Not tested

A reusable workflow in a second repo (`workflow_call`), `schedule` (its cron is **UTC**: `30 20 * * *` is 02:00 in India), and a bigger matrix with `include` and `exclude`.

**Check yourself:**

- [ ] You saw `Cache restored` on the second run.
- [ ] You saw an older run cancelled by a newer push.
- [ ] You downloaded or listed an artifact.

---

## Part C: secrets, injection and a key-free deploy (Episode 3)

### C1. A secret, an environment and an approval

```bash
LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 32 | gh secret set DEMO_TOKEN --repo YOU/atithi-actions-lab --body -
UID_=$(gh api user --jq .id)
echo "{\"reviewers\":[{\"type\":\"User\",\"id\":$UID_}]}" > env.json
gh api -X PUT repos/YOU/atithi-actions-lab/environments/production --input env.json
gh workflow run deploy.yml -f note=practice
gh run list --workflow deploy --limit 1
```

Expected: the environment answers `production required_reviewers`. The run shows **`waiting`**: the `build` job is done and the `deploy` job is paused for you. Approve it (the console shows a **Review deployments** button; by API):

```bash
gh api repos/YOU/atithi-actions-lab/actions/runs/RUN_ID/pending_deployments --jq '.[0].environment.id'
echo '{"environment_ids":[ENV_ID],"state":"approved","comment":"practice"}' > approve.json
gh api -X POST repos/YOU/atithi-actions-lab/actions/runs/RUN_ID/pending_deployments --input approve.json
```

After the approval the `deploy` job ran and finished `success`. The step printed only `token length=32`, never the value. (Private repos on a free plan do not get required reviewers; check your plan.)

### C2. Script injection: a title becomes a command

Put this in `.github/workflows/pr-title.yml` on a **branch**, never on `main` (a public repo accepts other people's pull requests):

```yaml
jobs:
  unsafe:     # DO NOT COPY
    runs-on: ubuntu-latest
    steps:
      - run: echo "title is ${{ github.event.pull_request.title }}"
  safe:
    runs-on: ubuntu-latest
    steps:
      - env:
          TITLE: ${{ github.event.pull_request.title }}
        run: echo "title is $TITLE"
```

Open a pull request titled exactly: `fix"; echo INJECTED-BY-THE-TITLE; "` (the payload only echoes a word). In the log:

```
unsafe:  Run echo "title is fix"; echo INJECTED-BY-THE-TITLE; ""      <- the title became commands (and the empty "" at the end made the job fail)
safe:    title is fix"; echo INJECTED-BY-THE-TITLE; "                   <- plain data
```

Then **delete the `unsafe` job** and merge only the safe one (`lab_files/atithi-actions-lab/.github/workflows/pr-title.yml` is the safe version).

### C3. OIDC: AWS without a stored key

Prerequisite for a restricted lab user: it needs permission to create GitHub's OIDC provider (`lab_files/atithi-lab-iam-oidc-policy.json`, as a managed policy). A normal admin does not.

1. **Make the provider** (once per account):

```bash
aws iam create-open-id-connect-provider --url https://token.actions.githubusercontent.com --client-id-list sts.amazonaws.com
```

2. **Find the real `sub` of your runs.** This is the step the script now insists on. Put `lab_files/oidc-debug.yml.example` on a branch called `oidc-debug`, push, and read the log. Our run printed:

```
"iss": "https://token.actions.githubusercontent.com",
"aud": "sts.amazonaws.com",
"sub": "repo:shivamnamdev@20036175/atithi-actions-lab@1465414609:ref:refs/heads/oidc-debug",
```

**Correction to the script's example:** the `sub` of a new repo contains the **owner and repository IDs** (`repo:OWNER@ID/REPO@ID:ref:...`), not `repo:OWNER/REPO:ref:...`. Our first role, with the plain form, failed on every one of 12 retries with **`Could not assume role with OIDC: Not authorized to perform sts:AssumeRoleWithWebIdentity`**. Copy the `sub` you see, with your own IDs.

3. **Make the role** with that exact `sub` for the `main` branch (see `trust-policy.json.example`), and store its ARN as a repository **secret** `AWS_ROLE_ARN` (it contains your account number, so a secret gets masked; a plain variable would not):

```bash
aws iam create-role --role-name atithi-gha-oidc --assume-role-policy-document file://trust.json
printf '%s' "$ROLE_ARN" | gh secret set AWS_ROLE_ARN --repo YOU/atithi-actions-lab
gh workflow run aws-oidc.yml --ref main
```

Result: **success**, `Authenticated as assumedRoleId AROA...`, with no AWS key anywhere in the repo. The same workflow started from another branch (`--ref oidc-debug`) **failed** with the same `Not authorized` message: the trust policy's `sub` condition did its job. (We did not test an environment-limited role.)

4. **Do not print the account number.** Our first working run used `aws sts get-caller-identity`, and its output has `"Account": "..."` and the role ARN: **the account number was readable in the public log** (it was not masked). We deleted that run, checked that no other run contained it, and changed the step to `aws sts get-caller-identity --query UserId --output text`, as in `aws-oidc.yml` now. The rule: in a public repo print nothing you would not post on a notice board.

### C4. Clean up this part

```bash
aws iam delete-role --role-name atithi-gha-oidc          # after detaching any policies
aws iam delete-open-id-connect-provider --open-id-connect-provider-arn arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com
gh secret delete AWS_ROLE_ARN --repo YOU/atithi-actions-lab
gh secret delete DEMO_TOKEN   --repo YOU/atithi-actions-lab
```

(Our course scripts do the AWS part: `_lab_tools/aws/aws_cleanup_atithi.sh`.) Revoking comes first for a real leak: the script's order, **revoke, check logs, clean history, add a guard**.

**Check yourself:**

- [ ] The deploy job waited for you, and the log showed the secret's length, not the secret.
- [ ] You saw the unsafe job run the title as a command, and the safe job print it as text.
- [ ] You can say why the `sub` must be copied from a real run, and why a wrong or missing `sub` condition is dangerous.
- [ ] No account number is visible in any public log.

---

## Part D: inspection in the conveyor (Episode 4)

### D1. The `security` job

`ci.yml` has three scanners: **Gitleaks** (secrets, the official action; it is free for a personal repo, an organisation needs a licence key), **pip-audit** (known-vulnerable Python packages) and **Trivy** (`scan-type: fs`, `severity: HIGH,CRITICAL`, `ignore-unfixed: true`, `exit-code: '1'`). On the clean repo all three passed.

Now pin a famous old package on a branch:

```bash
git checkout -b old-package
sed -i 's/requests>=2.32.4/requests==2.19.1/' requirements.txt
git commit -qam "old package on purpose" && git push -u origin old-package
gh pr create --title "Old package (do not merge)" --body practice --base main
gh run view RUN_ID --log-failed | tail -25
```

We saw `test (3.11)` and `test (3.12)` stay green and **`security=FAILURE`**. The pip-audit step printed a table of **package, version, vulnerability ID and the version that fixes it** (for example `urllib3  1.23  PYSEC-2019-133  1.24.2`), then `Process completed with exit code 1`. **The Trivy step never ran**, because a failed step stops the job: give each scanner its own job (or `if: always()`) if you want all three reports every time. Close the pull request without merging.

### D2. The first gate: a pre-commit hook

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/bash
docker run --rm -v "$PWD":/repo -w /repo zricethezav/gitleaks:latest git --staged --redact --no-banner -v .
exit ${PIPESTATUS[0]}
EOF
chmod +x .git/hooks/pre-commit
```

Test with a random, made-up key (never a real one):

```bash
FAKE="AKIA$(LC_ALL=C tr -dc 'A-Z2-7' </dev/urandom | head -c16)"
printf 'aws_access_key_id = %s\naws_secret_access_key = %s\n' "$FAKE" "$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c40)" > settings.py
git add settings.py && git commit -m "add settings"
```

Expected: the commit is **refused**, with `Finding:`, `RuleID: aws-access-token` (and `generic-api-key`), the **file and line**, and the secret shown as `REDACTED`. Then `git commit --no-verify` goes through: the hook can be skipped, which is why the conveyor (`security` as a required check) is the second gate. (Note: the older `gitleaks protect --staged` is now `gitleaks git --staged`.)

### D3. Not tested

CodeQL and SonarQube, `.trivyignore` with an expiry, and a Docker image scan (Session 22).

**Check yourself:**

- [ ] The `security` job went red for an old package, and you read the fix version.
- [ ] The hook refused a fake key, and you know how to skip it and why that is not enough.
- [ ] `security` is a required check on `main`.

---

## Clean up (do not skip)

- [ ] Delete the repo when you are done: `gh repo delete YOU/atithi-actions-lab --yes` (this needs `gh auth refresh -s delete_repo`), or Settings, Danger Zone.
- [ ] AWS: the role, the OIDC provider and the secret (Part C4), then your leftovers check.
- [ ] Remove `.git/hooks/pre-commit` from any repo where you do not want it.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | The role's `sub` does not match the real one (note the owner and repo IDs), or the wrong branch or environment | Print the real claims with the debug workflow and copy the `sub` |
| Account number visible in a public log | You printed `aws sts get-caller-identity` | Delete the run (`gh run delete`), print `--query UserId` only |
| `mergeStateStatus: BLOCKED` | Required checks are red or pending | Read `gh pr checks` |
| Required check never appears | The name must match the job name exactly, including `(3.12)` | Use the names from `gh pr checks` |
| Second matrix job `cancelled` | `fail-fast` stopped it after the first failure | Expected; `fail-fast: false` to see all |
| `Environment` approval never asked | Private repo on a free plan | Use a public practice repo, or check your plan |
| The Trivy step did not run | The step before it failed | Separate jobs, or `if: always()` |
| `git revert` made no commit | An error was hidden by `-q` | Run it without `-q` and read the message |

## What we did not test

- **Self-hosted runners, GitLab CI, reusable workflows in another repo, `schedule`, `pull_request_target`, CodeQL, SonarQube.**
- **OIDC restricted to an environment** (`sub` ending `environment:production`), and permissions boundaries for the role.
- **Real costs for a private repo** (minutes), and the browser screens (we used `gh` and the API).
