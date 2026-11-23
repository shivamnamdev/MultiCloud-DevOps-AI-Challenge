# Session 16 lab guide: Git on your own laptop

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **What was tested, and what was not.**
> Every command below was run for real, in a throwaway folder with its own Git config, on **macOS with Git 2.54 (Apple Git)**, and again as an automated self-check (`lab_files/session16_selfcheck.sh`, 39 checks, all passed). The script itself was written against Git 2.43 on Ubuntu 24.04; the commands are the same, only a few messages differ (see "Mac versus Ubuntu" below).
> **Not tested:** Windows (Git Bash), `git rebase` (the script only mentions it), and the interactive editor screens (`nano`/`vim` on a commit without `-m`).

| | |
|---|---|
| **Time** | Part A 25 min, Part B 25 min, Part C 30 min, Part D 20 min |
| **Cost** | Nothing. Everything is local; no account is needed until Session 16B. |
| **Skill check before you start** | Session 3 (terminal, files, a text editor). `git --version` prints a version. |

Starter files: `lab_files/session16_selfcheck.sh`. Run `bash session16_selfcheck.sh` any time to prove your Git behaves as this guide says. It uses its own temporary config and folder, so it cannot touch your real settings.

## Mac versus Ubuntu (what you may see differently)

| Step | Ubuntu 24.04 (script) | macOS (tested here) |
|---|---|---|
| Commit with no name set | `Author identity unknown, Please tell me who you are` and the commit is refused | The commit **works**: Git guesses a name from your username and a fake email from the hostname, and prints a warning. That guessed email will **not** match your GitHub account, so still set your own. |
| `git init` with no setting | branch is `master` plus a hint | same: `master` plus a long hint (it says the default becomes `main` in Git 3.0) |
| Running `git init -b main` in a folder that is **already** a repo | n/a | `warning: re-init: ignored --initial-branch=main`. The branch name does not change. Use `git branch -m main` to rename. |

---

## Part A: the register and the three places (Episode 1)

### A1. Tell Git who you are, once

```bash
git --version
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"   # use the SAME email as your GitHub account
git config --global init.defaultBranch main
git config --global core.editor nano
git config --list
```

You should see `user.name`, `user.email`, `init.defaultbranch=main` and `core.editor=nano` in the list (Git prints the key names in lower case). Settings live in `~/.gitconfig`.

### A2. First register

```bash
mkdir atithi-booking && cd atithi-booking
git init -b main
echo "<h1>Atithi Hotels: Book Now</h1>" > index.html
git status -s            # ?? index.html   (untracked: on the table, not in the register)
git add index.html
git status -s            # A  index.html   (in the tray)
git commit -m "Add booking homepage"
echo "<h1>Contact</h1><p>stay@atithi.example</p>" > contact.html
git add .
git commit -m "Add contact page"
git log --oneline
```

Expected: two lines in the log, newest first. `git add .` stages every changed file in the current folder at once.

**What `git status -s` letters mean** (two columns: tray, table): `??` untracked, `A ` staged new file, ` M` modified but not staged, `M ` modified and staged, `R ` renamed, `UU` conflict.

### A3. The two undo moves for the table and the tray

```bash
echo BROKEN > index.html
git status -s                   #  M index.html
git restore index.html          # table goes back to the last commit
cat index.html                  # the real heading is back

echo x > experiment.html
git add experiment.html
git restore --staged experiment.html   # out of the tray, still on the table
git status -s                   # ?? experiment.html
```

`git restore FILE` **cannot be undone**: uncommitted work is gone. `git restore --staged` loses nothing.

### A4. `.gitignore`, and the trap

```bash
printf '.env\nnode_modules/\n*.log\n' > .gitignore
git add .gitignore && git commit -m "Add .gitignore"
```

**The trap (tested):** if a file was committed *before* you ignored it, ignoring does nothing.

```bash
echo "SECRET=1" > .env && git add .env && git commit -m "Oops: add env"
echo ".env" >> .gitignore && echo "SECRET=2" > .env
git status -s            #  M .env   <- still tracked, still shows changes
git rm --cached .env     # forget it, keep the file on disk
git commit -am "Stop tracking .env"
git status -s            # clean
git log -p --all | grep SECRET     # the old secret is STILL in history
```

The last line is the lesson: removing a file does not remove it from the past. If it held a real secret, treat it as leaked and replace it (Session 20).

### A5. Remove and rename

```bash
echo hi > a.txt && git add a.txt && git commit -m "add a"
git mv a.txt b.txt
git status -s                     # R  a.txt -> b.txt
git commit -m "Rename a to b"
git log --follow --oneline b.txt  # shows the history from before the rename too
```

---

## Part B: reading the register (Episode 2)

Build the scenario, with a deliberate typo in the last commit:

```bash
echo "<h1>Atithi Hotels Welcome</h1>" > index.html
git commit -am "Update heading"
echo "<h1>Contact</h1><p>stya@atithi.example</p>" > contact.html     # typo: stya
git commit -am "Update contact email"
```

Then investigate, in this order:

```bash
git log --oneline                       # 1. find the suspects
git log --name-only --oneline           #    which commits touched contact.html
git diff GOOD_HASH BAD_HASH             # 2. what changed (replace with real hashes)
git show BAD_HASH                       # 3. one commit in full, with its message
git show GOOD_HASH:contact.html         # 4. the file exactly as it was that day
git blame contact.html                  #    who wrote each line
git blame -L 2,2 contact.html           #    only line 2
```

In the `diff` output, the line starting with `-` is what was there before and `+` is what is there now. The `index ... 100644` line ends with the file mode: `100644` is a normal file, `100755` an executable one.

Fix it with a **new** commit (history is never edited):

```bash
echo "<h1>Contact</h1><p>stay@atithi.example</p>" > contact.html
git commit -am "Fix contact email typo"
```

`git diff` alone compares table and tray; `git diff --staged` compares tray and last commit.

---

## Part C: drafts, merges and conflicts (Episode 3)

### C1. A branch is a pointer

```bash
echo "background: white;" > style.css
git add style.css && git commit -m "Add style"
git switch -c dark-mode
git branch                               # * dark-mode, main
git rev-parse main dark-mode             # the same hash twice: nothing was copied
cat .git/HEAD                            # ref: refs/heads/dark-mode
echo "background: black;" > style.css
git commit -am "Dark"
git log --oneline --graph --all          # only dark-mode moved forward
```

### C2. The conflict

```bash
git switch main
echo "background: #f5f0e6;" > style.css
git commit -am "Cream"
git merge dark-mode
```

Expected (tested): `CONFLICT (content): Merge conflict in style.css` and `git status -s` shows `UU style.css`. Open the file:

```
<<<<<<< HEAD
background: #f5f0e6;
=======
background: black;
>>>>>>> dark-mode
```

Three ways out:

```bash
git merge --abort                  # panic button: back to exactly before the merge
# or, after running git merge dark-mode again:
git checkout --ours   style.css    # keep the branch you stand on (main)
git checkout --theirs style.css    # keep the incoming one (dark-mode)
# or edit the file by hand, delete the three marker lines
git add style.css
git commit                          # or: git commit -m "Merge dark-mode"
```

`--ours` is always the branch **you are standing on**, not "mine" in the everyday sense. After the commit, `git rev-list --parents -n1 HEAD` shows three hashes: the merge commit and its **two parents**.

### C3. Fast-forward and clean-up

```bash
git switch -c quick && echo x > quick.txt && git add quick.txt && git commit -m quick
git switch main
git merge quick                    # "Fast-forward": main simply moved
git branch -d quick dark-mode      # delete finished drafts
```

`-d` refuses to delete an unmerged branch (good); `-D` forces it.

---

## Part D: inside `.git` (Episode 4)

```bash
ls -la
cat .git/HEAD                          # ref: refs/heads/main
ls .git/refs/heads                     # one small file per branch
cat .git/refs/heads/main               # a 40-character hash, nothing else
ls -la .git/index                      # the approval tray
git cat-file -t HEAD                   # commit
git cat-file -t 'HEAD^{tree}'          # tree
git cat-file -t HEAD:index.html        # blob
ls .git/hooks                          # *.sample files; remove .sample to enable one
```

### Switching drafts with unfinished work (two experiments, both tested)

```bash
echo "same" > notes.txt && git add notes.txt && git commit -m notes
git branch branch-a                       # same notes.txt as main
echo "vA" > contact.html && git commit -am "contact on main"
git switch -c branch-b HEAD~1             # a different contact.html
echo "vB" > contact.html && git commit -am "contact on branch-b"
git switch main
```

**Experiment A** (file is identical on both branches):

```bash
echo "more" >> notes.txt
git switch branch-a       # works; the edit travels with you
git restore notes.txt && git switch main
```

**Experiment B** (file differs between branches):

```bash
echo "wip" >> contact.html
git switch branch-b
```

Expected (tested): refused, with `error: Your local changes to the following files would be overwritten by checkout`. Your three options: commit it, `git restore` it, or park it:

```bash
git stash push -m "WIP"
git switch branch-b
git switch main
git stash pop                 # your unfinished edit is back
```

(Stash is taught properly in Session 16B.)

---

## Clean up

Nothing to delete in the cloud. To remove the practice folder, `cd ..` and delete `atithi-booking` yourself. Keep it: Session 16B pushes this same repo to GitHub.

## If something goes wrong

| You see | Cause | Fix |
|---|---|---|
| `Author identity unknown` | no name or email set (Ubuntu) | `git config --global user.name ...` and `user.email ...` |
| Branch is `master` | `init.defaultBranch` not set | `git branch -m main` now; set the config for next time |
| `.gitignore` does nothing for a file | file is already tracked | `git rm --cached FILE`, commit |
| `nothing to commit, working tree clean` after `git add` | you forgot to save the file in the editor, or you committed already | `git status`, `git log --oneline` |
| `error: ... would be overwritten by checkout` | uncommitted work in the way | commit, `restore`, or `stash` |
| Stuck mid-merge | unresolved conflict | resolve, `git add`, `git commit`; or `git merge --abort` |
| Vim opened and you cannot leave | commit without `-m` and no `core.editor` | press `Esc`, type `:q!` and Enter (cancels), then set `core.editor nano` |

## What we did not test

Windows Git Bash, `git rebase`, the editor-based commit message screen, `git config --global pull.rebase` (that belongs to Session 16B), and signed commits.
