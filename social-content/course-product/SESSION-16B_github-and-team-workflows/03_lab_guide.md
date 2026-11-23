# Session 16B lab guide: GitHub and team workflows

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **What was tested, and what was not.**
> Everything below ran for real on GitHub (a free personal account, a **public** repo, SSH, `gh` CLI, Git 2.54 on macOS). The messages are copied from those runs. Where the browser has a button, we used the `gh` command or API call that does the same thing, so the **screens** themselves were not tested.
> **Not tested:** a second human account. Requiring **approvals** (a reviewer other than you), a real **fork to a different owner's repo and a pull request from it** (GitHub does not let you fork your own repo, see Part E), and `git rebase`.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 40 min, Part C 30 min, Part D 30 min, Part E 20 min |
| **Cost** | Free. A public repo costs nothing and its Actions minutes are free. |
| **Skill check before you start** | Session 16 (the `atithi-booking` folder with commits), an SSH key added on GitHub (`ssh -T git@github.com` greets you by name), `gh auth status` logged in. |

Starter files in `lab_files/`:

```
.github/workflows/html-check.yml   a tiny required check: every page needs an <h1>
branch-protection.json             the rule used with the API (same as the Settings screen)
```

## Before you start: do not leak your email

A public repo shows the email on every commit. Use GitHub's private "noreply" address in this practice repo:

```bash
ID=$(gh api user --jq .id); LOGIN=$(gh api user --jq .login)
git config user.name  "$LOGIN"
git config user.email "${ID}+${LOGIN}@users.noreply.github.com"   # repo-local, not --global
```

(The script says to use the email on your GitHub account. Both work; the noreply one is safer on a public repo, and you can turn on "Keep my email addresses private" in GitHub settings.)

---

## Part A: the vault and the four arrows (Episode 1)

```bash
cd atithi-booking                 # the folder from Session 16
gh repo create atithi-booking --public --source=. --remote=origin
git remote -v                     # origin  git@github.com:YOU/atithi-booking.git
git push -u origin main
```

Expected: `new branch main -> main` and `branch 'main' set up to track 'origin/main'`. Refresh the repo page: files and the whole history are there.

**Be the teammate.** On github.com click the pencil on a file, or use the same API call the pencil uses:

```bash
gh api -X PUT repos/YOU/atithi-booking/contents/README.md \
  -f message="Add README from GitHub" -f content="$(printf '# Atithi booking\n' | base64)"
```

Back in the terminal (all tested):

```bash
git fetch                               # new line:  9bed0d1..b636fc4  main -> origin/main
git status -sb                          # ## main...origin/main [behind 1]
git log --oneline main..origin/main     # the one commit you do not have
git diff main origin/main --stat
git pull                                # "Fast-forward"
git clone git@github.com:YOU/atithi-booking.git second     # the new laptop
cd second && git log --oneline          # the full history, no git init needed
```

---

## Part B: pull requests, rejections, the lock (Episode 2)

### B1. Push rejected, and the divergent-pull hint (both reproduced)

In `second/`, edit `README.md`, commit and push. In your first folder, edit `index.html`, commit, then:

```bash
git push
#  ! [rejected]  main -> main (fetch first)
git pull
#  hint: You have divergent branches and need to specify how to reconcile them.
```

Choose once: `git config pull.rebase false` (merge) and `git pull` again; Git makes a merge commit; then `git push` works. Do not use `--force` here.

### B2. A pull request, start to finish

```bash
git switch main && git pull
git switch -c feature/offers-page
printf '<h1>Offers</h1>\n<p>Stay 3 nights, pay for 2</p>\n' > offers.html
git add offers.html && git commit -m "Add offers page"
git push -u origin feature/offers-page
gh pr create --base main --head feature/offers-page --title "Add offers page" \
  --body $'What: new offers.html\nWhy: owner wants a 3-for-2 offer\nTested: opened it locally'
```

Review comment on one line (the "Files changed" comment). Review requests can only be **comments** from you:

```bash
gh api -X POST repos/YOU/atithi-booking/pulls/1/reviews -f event=COMMENT -f body="Needs hotel name" \
  -f 'comments[][path]=offers.html' -F 'comments[][line]=1' -f 'comments[][body]=Add the hotel name'
gh pr review 1 --approve
#  failed to create review: Review Can not approve your own pull request
```

That last error is expected and real: **you cannot approve your own PR**. To practise approvals you need a second account (a friend as collaborator). We did not test that.

Fix, push, merge, clean up:

```bash
sed -i '' 's#<h1>Offers</h1>#<h1>Atithi Hotels Offers</h1>#' offers.html    # on Linux: sed -i
git commit -am "Add hotel name" && git push           # the PR updates itself
gh pr merge 1 --merge --delete-branch                 # deletes the remote AND local branch
git switch main && git pull
git fetch --prune                                     # see the tip below
```

**Tip (tested):** after a merge, `git branch -r` still lists `origin/feature/offers-page` until you run `git fetch --prune` (or `git remote prune origin`). `git pull` does not prune. Also, `gh pr merge --delete-branch` already deleted your local branch, so `git branch -d` afterwards says `not found`. Not an error.

### B3. The lock on `main`

Settings, Branches (or the API, same rule): require a pull request, require the check to pass, require the branch to be up to date, and apply the rule to admins too.

First add the check, **through a pull request**, because it is the thing the rule will wait for:

```bash
mkdir -p .github/workflows && cp /path/to/lab_files/.github/workflows/html-check.yml .github/workflows/
git switch -c chore/add-check && git add -A && git commit -m "Add html-check" && git push -u origin chore/add-check
gh pr create --base main --head chore/add-check --title "Add html-check" --body "Required check"
gh pr checks 3        # html-check  pass   (about 6 seconds)
gh pr merge 3 --merge --delete-branch
```

Then lock:

```bash
gh api -X PUT repos/YOU/atithi-booking/branches/main/protection --input /path/to/lab_files/branch-protection.json
```

Now try to cheat (tested; the rule applies to you, the owner):

```bash
git switch main && echo "<p>sneaky</p>" >> index.html && git commit -am "Direct push"
git push          # remote: error: GH006: Protected branch update failed ... Changes must be made through a pull request.
git push --force  # the same error: the lock stops force-push too
git reset --hard origin/main      # take your sneaky commit back
```

`required_approving_review_count` is `0` in our file, so one person can still merge their own PR. Raise it to `1` once you have a second account.

### B4. "This branch is out-of-date" and the Update branch button (tested)

Open two PRs from `main` (say `feature/bar` and `feature/garden`), wait for both checks to pass, then merge the first. The second changes state:

```bash
gh pr view 8 --json mergeStateStatus --jq .mergeStateStatus     # BEHIND
gh pr merge 8 --merge
#  X Pull request ... is not mergeable: the head branch is not up to date with the base branch.
gh api -X PUT repos/YOU/atithi-booking/pulls/8/update-branch    # = the "Update branch" button
#  Updating pull request branch.
gh pr checks 8        # the check runs again on the updated branch; merge when it passes
```

**Two things we learned the hard way:**

1. The `BEHIND` state appears **only** when the rule has "require branches to be up to date" **and** at least one required check. With the rule but no required check (our first attempt) GitHub let the stale PR merge without complaint.
2. Right after a push or merge GitHub shows `UNKNOWN` for a few seconds while it works things out. We got a bogus `merge conflict` from `update-branch` when we asked too early. Wait until the state is not `UNKNOWN`, then act.

The terminal alternative: `git switch feature/garden && git merge main && git push`.

---

## Part C: unfinished work, old revisions, one page (Episode 3)

### C1. Stash (tested)

```bash
git switch -c feature/room-filter
echo "<h1>Rooms</h1>" > rooms.html && git add rooms.html     # new file, in the tray
echo "<p>half done</p>" >> index.html                         # edit
echo "notes" > scratch.txt                                    # untracked
git stash push -m "WIP: room filter"
git status -s        # ?? scratch.txt   <- the untracked file did NOT go in the drawer
git stash list       # stash@{0}: On feature/room-filter: WIP: room filter
git stash pop        # everything comes back
```

What we saw:

| Command | Result |
|---|---|
| `git stash push` | tracked edits and tray go in; **untracked files stay** on the table |
| `git stash push -u` | untracked files go in the drawer too |
| `git stash pop` | restores and removes the stash. A **modified** tracked file comes back **unstaged** (` M`); a **brand-new** staged file stays staged |
| `git stash pop --index` | a modified file comes back **staged** (`M `) as it was |
| `git stash apply` | restores and **keeps** the stash (`git stash list` still shows it) |
| `git stash drop` | throws one away |

### C2. Detached HEAD (tested)

```bash
git log --oneline
git checkout 9c464e3          # or: git switch --detach 9c464e3
#  You are in 'detached HEAD' state ...
cat .git/HEAD                 # a raw 40-character hash, no "ref:"
echo y > lost.txt && git add lost.txt && git commit -m "made in reading room"
git switch main
#  Warning: you are leaving 1 commit behind, not connected to any of your branches: a270b54 ...
git branch rescue-idea a270b54      # saved. Without this the commit is findable only through git reflog
```

The warning prints the hash of your orphan commit. Copy it **before** you do anything else.

### C3. Cherry-pick (tested), with a surprise

```bash
git switch -c feature/homepage
echo "<h2>Winter offer</h2>" > offer-heading.html && git add . && git commit -m "Add offer heading"
echo "anim" > anim.js && git add . && git commit -m "Try homepage animation"
git log --oneline                          # note the hash of "Add offer heading"
git switch main && git pull
git switch -c pick/offer-heading
git cherry-pick 7b62dba                    # only that one commit arrives; anim.js does not
```

**Surprise 1 (hash):** in our first try the new hash was **identical** to the old one (`7b62dba`). That happens when both commits have the **same parent and are made in the same second**, which is true when you branch twice from an unchanged `main`. Pick onto a different base (`git switch -c other main~1`) and the hash changes (`6ba194c`). In a real team `main` has moved on, so you will normally see a new hash.

**Surprise 2 (the lock works):** we pushed this branch and opened a PR. The required `html-check` **failed**, because our file used `<h2>` and the check wants an `<h1>`. The merge button stayed blocked: `the base branch policy prohibits the merge`. Fix it on the same branch (`<h1>`), push, wait for green, merge. This is exactly the lock doing its job.

```bash
git push -u origin pick/offer-heading
gh pr create --base main --head pick/offer-heading --title "Offer heading" --body "Only the ready commit"
gh pr checks 9        # fail -> fix -> pass
```

---

## Part D: undo ladder, and the team day (Episode 4)

### D1. The ladder (every step tested)

| Where is the mistake? | Command | Test result |
|---|---|---|
| table only | `git restore FILE` | file back to last commit |
| in the tray | `git restore --staged FILE` | file stays on the table |
| committed, not pushed, keep the work staged | `git reset --soft HEAD~1` | status: `A  u1.txt` |
| committed, not pushed, keep the files | `git reset HEAD~1` (mixed) | status: `?? u2.txt` |
| committed, not pushed, throw it all away | `git reset --hard HEAD~1` | file and commit gone |
| wrong message on last commit | `git commit --amend -m "Right message"` | one commit, new text |
| `reset --hard` was a mistake | `git reflog`, then `git reset --hard HASH` | the file came back |

The reflog test: commit "precious", `git reset --hard HEAD~1` (file gone), `git reflog` shows `d430f5e HEAD@{1}: commit: precious`, `git reset --hard d430f5e` brings it back. The reflog only exists on **your** machine and entries expire (about 90 days).

### D2. After the push: revert, never reset (tested)

```bash
git revert d567733                 # a normal commit: fine
git revert HASH_OF_A_MERGE
#  error: commit 80eba0a is a merge but no -m option was given.
git revert -m 1 HASH_OF_A_MERGE    # -m 1 = "keep the main line (parent 1)"
```

**This one catches everyone.** A merged pull request is a merge commit, so reverting a PR from the terminal needs `-m 1`. Because `main` is locked, put the revert on a branch and send it through a PR:

```bash
git switch -c revert/bar && git revert --no-edit -m 1 80eba0a && git push -u origin revert/bar
gh pr create --base main --head revert/bar --title "Revert bar page" --body "Undo PR 7"
```

**The button's twin (tested):** GitHub's "Revert" button on a merged PR is a GraphQL mutation, which makes the revert branch and PR for you:

```bash
PRID=$(gh pr view 8 --json id --jq .id)
gh api graphql -f query='mutation($id:ID!){revertPullRequest(input:{pullRequestId:$id,title:"Revert garden page"}){revertPullRequest{number url}}}' -f id=$PRID
```

When we reverted two PRs at the same time, the second PR went `BEHIND` and needed **Update branch** (Part B4) before it could merge. Expected.

### D3. `--force-with-lease` (tested, with a catch)

On a feature branch where a teammate pushed after you:

```bash
git commit --amend -m "lease 1 (amended)"      # you rewrote your own commit
git push                    # ! [rejected] (fetch first)
git push --force-with-lease # ! [rejected] (stale info)   <- safe: it noticed the teammate
git fetch
git push --force-with-lease # + 1df3c6e...58935b7 (forced update)
```

**The catch:** after `git fetch` Git believes you have *seen* the teammate's commit, so the lease passes and **the teammate's commit is overwritten**. `--force-with-lease` protects you from the blind overwrite, not from a fetch you did not read. Run `git log origin/BRANCH` after fetching and decide on purpose.

### D4. The five-role day, in one repo

Run it with a friend, or with two folders and a second GitHub account. We tested the parts a single account can do: lock, lead-designer PR, conflict-free update, revert, tag. Parts that need another human: reviewer approvals, the contractor's fork.

Owner seals the release (tested; tags are not covered by the branch lock):

```bash
git switch main && git pull
git tag -a v1.0 -m "First release"
git push origin v1.0              # * [new tag] v1.0 -> v1.0
git ls-remote --tags origin       # refs/tags/v1.0  and  refs/tags/v1.0^{}   (the second is the commit it points to)
git tag -n1                       # v1.0   First release
```

Finish with the whole picture:

```bash
git log --oneline --graph --all
```

---

## Part E: the outside contractor (fork and upstream)

**What GitHub says if you try it on your own repo (tested):**

```
failed to fork: YOU/atithi-booking cannot be forked. A single user account cannot own both a parent and fork.
```

So for a real fork you need a repo that belongs to **someone else** (a friend's, or GitHub's public practice repo `octocat/Spoon-Knife`).

```bash
gh repo fork OWNER/REPO --clone=false          # creates YOU/REPO on GitHub
git clone git@github.com:YOU/REPO.git && cd REPO
git remote add upstream git@github.com:OWNER/REPO.git
git remote -v                                  # origin = your fork, upstream = the real one
git fetch upstream
git branch -r                                  # CHECK the branch name: some repos use main, some master
git merge upstream/main                        # use the name you saw ("Already up to date" if nothing new)
gh repo sync YOU/REPO                          # one-line alternative that syncs the fork on GitHub
```

Then branch, push to **your fork**, and open the PR to the upstream owner. We did **not** open a PR into someone else's repo, so that last step is untested.

---

## Clean up (do not skip)

```bash
gh repo delete YOU/atithi-booking --yes         # needs:  gh auth refresh -s delete_repo   (once)
```

Delete the practice folders too. If you forked someone else's repo only for this lab, delete the fork the same way. Do not delete a fork that you were already using for something else. (Ours existed since 2017, so we left it alone.)

## If something goes wrong

| You see | Cause | Fix |
|---|---|---|
| `Permission denied (publickey)` | SSH key not on GitHub | Session 4 key, GitHub Settings, SSH keys; `ssh -T git@github.com` |
| `rejected ... fetch first` | vault is ahead | `git pull`, then `git push` |
| `You have divergent branches` | no `pull.rebase` choice | `git config pull.rebase false` |
| `GH006: Protected branch update failed` | the lock works | make a branch and a PR |
| PR stuck on `BLOCKED` | a required check failed or is missing | `gh pr checks N`, fix, push |
| PR `BEHIND` | base moved on | **Update branch** (API above) or `git merge main` |
| `update-branch` says `merge conflict` right away | GitHub still computing (`UNKNOWN`) | wait 10 seconds, ask again |
| `a merge but no -m option was given` | reverting a merge commit | `git revert -m 1 HASH` |
| `Can not approve your own pull request` | GitHub rule | use a second account |
| `origin/feature/x` still listed after merge | stale tracking ref | `git fetch --prune` |
| Commit lost after detached HEAD | no branch points at it | `git branch rescue HASH` (hash from the warning or `git reflog`) |

## What we did not test

Requiring approvals and CODEOWNERS (needs a second person), a PR from a fork into another owner's repo, merge **queue**, squash and rebase merge buttons (we used merge commits only), `git rebase`, GitLab and Bitbucket, signed commits, and every browser screen (we used `gh` and the API for the same actions).
