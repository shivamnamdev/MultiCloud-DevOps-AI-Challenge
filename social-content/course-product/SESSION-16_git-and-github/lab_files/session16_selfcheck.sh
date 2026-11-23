#!/usr/bin/env bash
# Session 16 (Part A) self-check: runs the whole lab in a throwaway folder and
# prints PASS/FAIL for each claim made in the script. Safe: uses its own Git
# config, never touches your real ~/.gitconfig, creates nothing outside $WORK.
# Run:  bash session16_selfcheck.sh
set -u
WORK=$(mktemp -d)
export GIT_CONFIG_GLOBAL="$WORK/gitconfig" GIT_CONFIG_NOSYSTEM=1 HOME="$WORK/home"
mkdir -p "$HOME"; : > "$GIT_CONFIG_GLOBAL"
pass=0; fail=0
check(){ if eval "$2" >/dev/null 2>&1; then echo "PASS  $1"; pass=$((pass+1)); else echo "FAIL  $1"; fail=$((fail+1)); fi; }
g(){ git "$@" >/dev/null 2>&1; }

git config --global user.name "Asha"; git config --global user.email "asha@example.com"
git config --global init.defaultBranch main; git config --global core.editor nano
cd "$WORK" && mkdir atithi-booking && cd atithi-booking && git init -q -b main
check "Episode 1: init -b main gives branch main" '[ "$(git symbolic-ref --short HEAD)" = main ]'

echo "<h1>Atithi Hotels: Book Now</h1>" > index.html
check "untracked file shows ??" 'git status -s | grep -q "^?? index.html"'
git add index.html
check "after add the file is staged (A)" 'git status -s | grep -q "^A  index.html"'
g commit -m "Add booking homepage"
echo "<p>stay@atithi.example</p>" > contact.html; git add .; g commit -m "Add contact page"

echo BROKEN > index.html
check "modified file shows ' M'" 'git status -s | grep -q "^ M index.html"'
g restore index.html
check "restore brings the page back" 'grep -q "Book Now" index.html'
echo x > experiment.html; git add experiment.html; g restore --staged experiment.html
check "restore --staged moves file back to untracked, content kept" 'git status -s | grep -q "^?? experiment.html" && [ -s experiment.html ]'
rm experiment.html

# .gitignore trap
echo "SECRET=1" > .env; git add .env; g commit -m "Oops add env"
printf '.env\n*.log\n' > .gitignore; echo "SECRET=2" > .env
check "TRAP: ignoring an already-tracked file does NOT hide changes" 'git status -s | grep -q "^ M .env"'
g rm --cached .env
check "git rm --cached keeps the file on disk" '[ -f .env ]'
g add .gitignore; g commit -m "Stop tracking .env"
check "after rm --cached + commit, .env is ignored" '[ -z "$(git status -s)" ]'
check "old history still contains the secret (leak lesson)" 'git log -p --all | grep -q "SECRET=1"'
echo hi > a.txt; git add a.txt; g commit -m "add a"
git mv a.txt b.txt
check "git mv shows as rename (R)" 'git status -s | grep -q "^R  a.txt -> b.txt"'
g commit -m "rename a to b"
check "log --follow shows pre-rename history" '[ "$(git log --follow --oneline b.txt | wc -l)" -ge 2 ]'

# Episode 2: history
g mv b.txt b2.txt 2>/dev/null
echo "<h1>Contact</h1><p>stay@atithi.example</p>" > contact.html; g add contact.html; g commit -m "Contact email"
echo "<h1>Atithi Hotels Welcome</h1>" > index.html; g add index.html; g commit -m "Update heading"
echo "<h1>Contact</h1><p>stya@atithi.example</p>" > contact.html; g add contact.html; g commit -m "Update contact email"
BAD=$(git rev-parse --short HEAD); GOOD=$(git log --format=%h --grep="Contact email" | tail -1)
check "log --name-only lists contact.html" 'git log --name-only --oneline | grep -q contact.html'
check "diff GOOD BAD shows - good email, + typo" 'git diff $GOOD $BAD | grep -q "^-.*stay@" && git diff $GOOD $BAD | grep -q "^+.*stya@"'
check "diff header has index line with mode 100644" 'git diff $GOOD $BAD | grep -q "^index .*100644"'
check "show REV:file prints the file as of that day" 'git show $GOOD:contact.html | grep -q "stay@"'
check "blame names the author of the bad line" 'git blame contact.html | grep -q Asha'
check "blame -L limits lines" '[ "$(git blame -L 1,1 contact.html | wc -l)" -eq 1 ]'
echo "<h1>Contact</h1><p>stay@atithi.example</p>" > contact.html; g commit -am "Fix contact email typo"
check "plain diff vs --staged differ" 'echo z >> index.html; [ -n "$(git diff)" ] && [ -z "$(git diff --staged)" ]'
g restore index.html

# Episode 3: branches, merge, conflict
echo "background: white;" > style.css; g add style.css; g commit -m "Add style"
g switch -c dark-mode
check "branch is just a pointer: same commit as main" '[ "$(git rev-parse dark-mode)" = "$(git rev-parse main)" ]'
check "HEAD now points to dark-mode" 'grep -q "refs/heads/dark-mode" .git/HEAD'
echo "background: black;" > style.css; g commit -am "Dark"
check "only dark-mode moved" '[ "$(git rev-parse dark-mode)" != "$(git rev-parse main)" ]'
g switch main
echo "background: #f5f0e6;" > style.css; g commit -am "Cream"
git merge dark-mode >/dev/null 2>&1
check "conflicting merge reports unmerged file (UU)" 'git status -s | grep -q "^UU style.css"'
check "conflict markers are present" 'grep -q "<<<<<<< HEAD" style.css && grep -q ">>>>>>> dark-mode" style.css'
git merge --abort >/dev/null 2>&1
check "merge --abort restores a clean tree" '[ -z "$(git status -s)" ] && grep -q "f5f0e6" style.css'
git merge dark-mode >/dev/null 2>&1; git checkout --ours style.css >/dev/null 2>&1
check "--ours keeps the branch you stand on (main)" 'grep -q "f5f0e6" style.css'
g add style.css; g commit -m "Merge dark-mode (kept cream)"
check "merge commit has two parents" '[ "$(git rev-list --parents -n1 HEAD | wc -w)" -eq 3 ]'
g branch -d dark-mode
check "branch -d removes the draft" '! git rev-parse --verify dark-mode'
# fast-forward
g switch -c ff; echo "x" > ff.txt; g add ff.txt; g commit -m ff; g switch main; git merge ff 2>&1 | grep -q "Fast-forward"
check "fast-forward happens when main has not moved" '[ "$(git rev-parse main)" = "$(git rev-parse ff)" ]'

# Episode 4: inside .git
check "HEAD file reads ref: refs/heads/main" 'grep -q "ref: refs/heads/main" .git/HEAD'
check "branch file holds a 40-char hash" '[ "$(wc -c < .git/refs/heads/main | tr -d " ")" -eq 41 ]'
check ".git/index exists" '[ -f .git/index ]'
check "objects types are blob, tree, commit" 'T=$(git cat-file -t HEAD); [ "$T" = commit ] && [ "$(git cat-file -t HEAD^{tree})" = tree ] && [ "$(git cat-file -t HEAD:index.html)" = blob ]'
check "hooks folder has pre-commit.sample" 'ls .git/hooks | grep -q "^pre-commit.sample$"'
# switching with unfinished work
echo "same" > notes.txt; g add notes.txt; g commit -m notes; g branch branch-a
echo "vA" > contact.html; g commit -am "contact on main"; g switch -c branch-b HEAD~1; echo "vB" > contact.html; g commit -am "contact on branch-b"; g switch main
echo "same+" >> notes.txt
g switch branch-a
check "A: unchanged-on-both file travels with you" 'grep -q "same+" notes.txt'
g restore notes.txt; g switch main
echo "wip" >> contact.html
git switch branch-b >/dev/null 2>&1
check "B: switch refused when work is in the way" '[ "$(git symbolic-ref --short HEAD)" = main ]'
git switch branch-b 2>&1 | grep -q "would be overwritten" && echo "PASS  message says 'would be overwritten'" && pass=$((pass+1)) || { echo "FAIL  message"; fail=$((fail+1)); }
g stash push -m "WIP"; g switch branch-b
check "stash lets you switch" '[ "$(git symbolic-ref --short HEAD)" = branch-b ]'
g switch main; g stash pop
check "stash pop brings work back" 'grep -q wip contact.html'

echo; echo "Passed: $pass   Failed: $fail   (work folder: $WORK)"
[ "$fail" -eq 0 ]
