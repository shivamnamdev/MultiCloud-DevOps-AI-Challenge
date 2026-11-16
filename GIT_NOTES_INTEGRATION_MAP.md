# Git section: what to take from the author's Git cohort

**Status:** applied on 2026-11-14 to the DevOps course as `SESSION-16_git-and-github` (Part A) and `SESSION-16B_github-and-team-workflows` (Part B), four episodes each, in the Atithi Hotels story with the booking website as the lab project. Section 6 touch points: Session 17 (hook as the local bell, the vault rings the foreman, Jenkinsfile reviewed by pull request, deploy key) and Session 19 (required status check on the master lock, tag builds, fork trust) applied on 2026-11-17. Still to apply: 04, 20, 22 and 31. The deep version of this material is a separate dedicated course: see `courses/Github-Live-Cohort-Transcript/SYLLABUS_BLUEPRINT.md`.
**Source:** `courses/Github-Live-Cohort-Transcript` (the author's own 16-day live Git cohort).
**Target:** `social-content/course-product/SESSION-16_git-and-github/02_script.md`, plus small touch points in sessions 04, 17, 20, 22 and 31.

## 1. What the source contains

| Material | Size | What it is | How to use it |
|---|---|---|---|
| 16 class transcripts (`Git Day 1` to `Git Day 16`) | about 630,000 characters, auto-captioned Hinglish in Devanagari | The author teaching live: scenarios, spoken comparisons, learner questions | Primary source for scenarios, teaching order and spoken lines |
| 15 daily notes (`notes` in each day folder; Day 4 has none) | about 53,000 characters | Per-day summary: topics, commands, key takeaways | Checklist of what was actually taught each day |
| 11 chapter notes (`Notes/*.docx`) | about 213,000 characters | Lesson plans: scenario first, analogy, hands-on steps, cheat sheet | Lab steps and diagrams; reword, do not lift (see section 7) |

## 2. The gap

SESSION-16 today is four episodes that cover: the zip-file problem, three zones, objects and hashes, branch as a pointer, fast-forward and three-way merge, a line on rebase, remotes, pull requests, conflict markers, and an undo list (restore, amend, revert, reflog).

The cohort taught all of that and the following, none of which is in the script:

| Missing from SESSION-16 | Cohort source |
|---|---|
| A real project scenario as the reason for Git (owner, analyst, developers, customer changes their mind) | Day 1 |
| Reading history: `git diff` between commits, `git show <hash>:<file>`, how to read a diff header | Day 2, Chapter 3 |
| Why staging exists (five files changed, three belong to one feature) | Day 3, Chapters 2 and 4 |
| "Why do branch commits show in main after a merge?", merge commit with two parents | Day 7 |
| `--ours` / `--theirs` and which side is which, `git merge --abort` | Day 6, Chapter 5 |
| What happens to uncommitted work when you switch branches (carried over vs blocked) | Day 8, Chapter 6 Q&A |
| Inside `.git`: `HEAD`, `refs/heads`, `index`, `config`, hooks | Days 8 and 9, "Under the Hood" notes |
| `-u` upstream, `origin` is only a nickname, fetch vs pull in practice | Day 10, Chapter 6 |
| Push rejected because the remote moved; branch behind main before a PR; answering review comments | Day 11, Chapter 7 |
| `git stash` (push -m, list, pop, apply, -u), detached HEAD, `git cherry-pick`, cherry-pick through a PR | Days 12, 13, 14 |
| `git reset --soft / --mixed / --hard`, why `push --force` hurts teammates, the undo decision tree | Day 15, Chapter 8 |
| Five-role team simulation: owner, lead developer, conflict, bad commit reverted in the GitHub UI, fork with `upstream` | Day 16, Chapter 10 |
| `.gitignore`, commit message convention, branching strategies, tags and releases | Chapter 9 |
| Mistakes already on GitHub: leaked secret, direct push to main, PR merged by mistake, deleted branch | Chapter 8 part 5 |

## 3. The size decision

Sixteen days do not fit in four 13-minute episodes without dropping stash, cherry-pick, reset and the team simulation, which are the most practical parts of the cohort.

**Recommended:** eight episodes, packaged as two sessions of four, so the "four episodes per session" promise in Session 00 still holds and sessions 17 to 33 keep their numbers:

- **SESSION-16A, Git on your own laptop** (cohort days 1 to 9)
- **SESSION-16B, GitHub and working in a team** (cohort days 10 to 16)

Alternatives: keep four episodes and move stash, cherry-pick, reset modes and forks to a one-line mention each; or insert a new session 17 and renumber everything after it.

## 4. Episode plan

Each row names the author's scenario, then the commands, then the source.

### 16A: Git on your own laptop

| Ep | Title | Author's scenario and teaching points | Commands | Source |
|---|---|---|---|---|
| 1 | Why Git, and the three zones | The owner gives a requirement, the team builds it, the customer asks for a change and then says "go back to last week's version". Three zones. Why staging exists: five files changed, three are one feature. Habit: `git status` after every command. Lab: `my-first-website`, homepage, contact page, then the day-3 breakage that the last commit survives. Add `.gitignore` here. | `git init`, `status`, `add <file>`, `add .`, `commit -m`, `log`, `restore --staged` | Days 1 and 3; Chapters 1, 2, 4 part 1; Chapter 9 (`.gitignore`) |
| 2 | Reading history | The client calls: "the contact form worked four days ago". Investigation flow: list, compare, peek at one old file, visit, come back. Reading a diff: `a/` and `b/`, `-` and `+`, the `@@` location line, context lines. Good commit messages. | `log --oneline`, `diff`, `diff --staged`, `diff <h1> <h2>`, `show <h>`, `show <h>:<file>`, `log --name-only` | Day 2; Chapter 3; Chapter 9 (messages) |
| 3 | Branch and merge | "Make the whole site dark mode, and do not break the live site." A branch is a label on a commit, not a copy. Fast-forward vs three-way. Why branch commits stay in main after a merge (two rivers joining); a merge commit has two parents; the graph view. Conflict: keep mine, keep theirs, combine. `ours` is the branch you are standing on. `merge --abort` as the safe way out. | `branch`, `switch`, `switch -c`, `merge`, `log --oneline --graph --all`, `checkout --ours/--theirs`, `merge --abort`, `branch -d` | Days 3 to 7; Chapters 4 part 2 and 5 |
| 4 | Under the hood | Open `.git` and look. `HEAD` is the "you are here" marker; a branch is one small file holding a commit hash; `index` is the staging area; blob, tree, commit; hooks. Then the experiment: switch branches with uncommitted work, once where Git carries it over and once where Git refuses. Rule: uncommitted work belongs to no branch until it is committed. | `cat .git/HEAD`, `ls .git/refs/heads`, `cat .git/refs/heads/main`, `ls .git/objects`, `ls .git/hooks`, `cat .git/config` | Days 8 and 9; "Under the Hood" notes parts 1 and 2; Chapter 6 Q&A |

### 16B: GitHub and working in a team

| Ep | Title | Author's scenario and teaching points | Commands | Source |
|---|---|---|---|---|
| 5 | GitHub enters | Until now the whole history lived in one `.git` folder on one laptop. Remote = a saved contact (`origin` is the contact name, the URL is the number). What `-u` remembers. Fetch = download and look; pull = download and apply. Clone needs no `git init`. SSH key from Session 04. | `remote add origin`, `remote -v`, `branch -M main`, `push -u origin main`, `fetch`, `pull`, `clone` | Day 10; Chapter 6 |
| 6 | Pull request workflow | The 13-step flow from the cohort: shared repo, collaborators, branch, commit, push, PR, review, fix comments, merge, sync. A PR is a review conversation, not a merge button. Two real failures: push rejected because someone pushed first; branch behind main. Protect main. Branching strategies in one scene (GitHub Flow as the default). | `switch -c feature/...`, `push origin <branch>`, `pull origin main`, `merge main`, `branch -a`, `push origin --delete` | Day 11; Chapter 7 parts 1 to 3; Chapter 9 (strategies) |
| 7 | Interrupted work | "Production is down, drop everything": stash the half-done work, fix, come back, pop. Named stashes. "Yesterday's contact page looked better": visit an old commit (detached HEAD), look, return; if you committed there, rescue it with a branch. One ready commit and one experiment on the same branch: cherry-pick only the ready one, through its own branch and a PR. | `stash`, `stash push -m`, `stash list`, `stash pop`, `stash apply`, `stash push -u`, `checkout <hash>`, `switch -c rescue <hash>`, `cherry-pick <hash>` | Days 12, 13, 14; "Under the Hood" notes parts 3 to 5; Chapter 8 part 4 |
| 8 | Undo, then the full team run | The undo decision tree, asked top-down: pushed? committed? staged? only edited? Reset soft, mixed and hard side by side. Why `push --force` breaks teammates and `revert` does not. Then the five-role run on one repo: owner protects main; one clean PR; one conflict resolved locally; one bad commit reverted from the GitHub UI; one outside contributor through a fork and `upstream`. Tags for a release. | `restore`, `restore --staged`, `reset --soft HEAD~1`, `reset HEAD~1`, `reset --hard HEAD~1`, `revert <hash>`, `remote add upstream`, `fetch upstream`, `tag` | Days 15 and 16; Chapters 8 and 10; Chapter 9 (tags) |

## 5. The author's comparisons, and how they sit in the Atithi Hotels story

The locked story already has: code = blueprint, commit = a signed, dated revision in the blueprint register, branch = draft copy, conflict = two designers moved the same wall, GitHub = the vault, pull request = the chief architect's review. The cohort's comparisons map onto it as follows.

| Taught in the cohort | In the story | Note |
|---|---|---|
| Restaurant kitchen: table, kitchen pass, order recorded (spoken on Day 3) | Drawing table, approval tray, blueprint register | Same three steps. A kitchen sits inside one building (zoom level 1), Git sits at head office (level 3), so the tray version keeps the levels clean |
| Supermarket trolley, suitcase, Amazon cart | Approval tray | Three comparisons for one idea; use one |
| Video-game checkpoint | A signed, dated revision | "Checkpoint" can stay as a plain word; it is used all through the cohort |
| Time machine, alternate timelines (spoken on Day 1) | Draft copy of the blueprint | Locked |
| Photo album, spot the difference | Turning back the pages of the register; two revisions side by side | |
| Sticky label on a commit | A clip marking the current page; the clip moves, the pages do not | |
| Two chefs, one recipe | Two designers moved the same wall | Locked |
| Two rivers join and the water of both flows on (spoken on Day 7) | Keep as spoken | One sentence, nothing in the story competes |
| Engine room of a ship | The back room of the register, where the pages are actually filed | |
| "You are here" dot on a mall map | "You are here" pin on the head-office floor map | |
| Museum exhibit, a page pulled out of a book | The archive reading room: look, do not draw | |
| Half-cooked meal in the fridge (spoken on Day 12) | A half-drawn sheet put in the designer's drawer | The drawer is private: a stash never reaches the vault |
| Phone contact for `origin` | Keep as spoken | One sentence |
| Google Drive | The vault | Locked |
| Essay draft to the teacher | Chief architect's review | Locked |
| Google Docs without auto-sync | The vault refuses your page because the register has moved on; fetch the new pages first | |
| Photocopying a library book (fork) | An outside contractor gets their own copy of the vault and sends back a proposal | Avoid "franchise", which is Helm |
| Building with four floors of undo | Where is the mistake: on the table, in the tray, in the register, or already in the vault? | No new picture needed, and "building" stays a server |
| Newspaper correction notice (revert) | A correction slip added to the register; no page is torn out | |
| Photocopying one recipe card (cherry-pick) | Copy one page from a draft into the master | |

The scenarios carry over without change if the project is Atithi's own booking website: the owner's requirement, "dark mode but do not break the live site", "the contact page worked four days ago", "production is down", and the five team roles become Atithi's design team.

## 6. Touch points outside the Git session

| Session | What to add | Source |
|---|---|---|
| 04, Linux users, permissions, SSH | The same SSH key signs you in to GitHub. File mode in a diff (`100644`, `100755`) is the permission lesson again: a `deploy.sh` committed without the executable bit will not run for the next person | Chapter 3 (mode section), Day 10 |
| 17, Jenkins foundations | Hooks from episode 4 are the local version of the webhook; "the vault rings the foreman's bell" follows from it | Day 9 |
| 20, GitHub Actions and DevSecOps | The leaked-secret scenario: revoke the credential first, then clean history. Branch protection that requires checks. A pre-commit hook as the first security gate | Chapter 8 part 5, Chapter 9 |
| 22, Dockerfile and registries | Git tags lead to image tags | Chapter 9 |
| 31, Capstone | Start the pipeline with the team flow from episode 8: branch, PR, review, merge, and only then the bell rings | Day 16, Chapter 10 |

## 7. Do not carry over as written

- **Learner names.** The transcripts and notes name real participants. Scripts should use roles only (owner, lead developer, senior developer, junior developer, outside contributor).
- **Day 11 transcript:** "restore command is nothing but your rebase command". Not correct; restore discards or unstages changes, rebase replays commits on a new base. Likely a slip or a caption error.
- **Day 4 transcript:** revert is described as leaving no commit. Revert keeps the original commit and adds a new one that reverses it, as the Day 15 notes say correctly.
- **"Under the Hood" notes:** "that's literally all `git switch` does internally, it rewrites this one file". It also updates the files in the working folder and the index, which is exactly why a switch can be refused (Day 8).
- **Chapter 3 notes:** "without `git update-index --chmod=+x`, Git forgets the executable flag". On Linux and macOS Git records the executable bit from `chmod +x` by itself; the extra command is for Windows.
- **Chapter 5 notes:** "Working area: not shared between branches". The Day 8 finding is the accurate one: uncommitted work belongs to no branch and can travel with you.
- **Chapter notes wording.** They read as drafted lesson plans and still contain leftover chat lines ("Ready for Chapter 3, or do you want to go deeper?"). Take the structure and lab steps; take the voice from the class transcripts.
- **Promotional lines** in the daily notes (subscribe prompts, series name, hashtags).
- **Housekeeping in the source repo:** the `Git Day 15` folder holds a transcript titled `Git Day 13`; Day 4 has no notes file.

## 8. Decisions (settled by the author on 2026-11-14)

Size: two parts of four episodes, each point covered in brief. Comparisons: story words, as in the rest of the DevOps course. Lab project: Atithi's booking website. The original options were:

1. Size: two sessions of four episodes (recommended), one session of four, or a renumber.
2. Comparisons: story words everywhere with rivers and the phone contact kept as spoken (recommended), or keep more of the cohort's originals (kitchen, fridge) as spoken asides.
3. Whether the lab project becomes Atithi's booking website or stays the generic `my-first-website`.
