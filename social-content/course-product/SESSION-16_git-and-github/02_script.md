# ✍️ 02: SCRIPT — SESSION-16: Git & GitHub
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S16`
- **Focus:** Version control idea, Git internals (working tree/index/repo), branching & merging, remotes/PRs, conflict resolution, team workflows
- **Episodes:**
  - Episode 1: Version Control kyun: Git ke Teen Zone
  - Episode 2: Branch aur Merge: Parallel Duniya
  - Episode 3: GitHub, Pull Request aur Code Review
  - Episode 4: Conflicts, Undo aur Team Workflow

---

# 📺 EPISODE 1: Version Control kyun?

### [00:00 – 01:15] Scene 1: final_v2_REAL_final.zip
**[VISUAL: A folder full of files: `project_final.zip`, `project_final_v2.zip`, `project_final_v2_REAL.zip`. A confused developer. Then a clean timeline with commits.]**

**(Voiceover):**
Aapne kabhi `project_final_v2_REAL_final.zip` jaisa naam rakha hai? Agar team mein paanch log aise files email se bhejein, to kaun sa version asli hai? Version control is pagalpan ka ilaaj hai: har badlav ka record, kisne kiya, kab kiya, kyun kiya, aur zaroorat par purane version par wapas jaana. Git duniya ka sabse popular version control system hai.

### [01:15 – 05:00] Scene 2: Git ke Teen Zone
**[VISUAL: Three boxes in a row: Working Directory → Staging Area (index) → Repository (commits). Arrows labelled `git add` and `git commit`. A shopping analogy: trolley then billing counter then receipt.]**

**(Voiceover):**
Git mein teen jagahein hoti hain. Working directory, jahan aap files badalte ho. Staging area, jahan aap chunte ho ki agle snapshot mein kya jayega. Aur repository, jahan snapshots, yaani commits, hamesha ke liye save hote hain. Isse shopping se samjho. Saaman uthana working directory, trolley mein daalna `git add`, aur billing counter par receipt banana `git commit`. Commit ek snapshot hai, aur har commit ka ek unique hash aur ek message hota hai.

### [05:00 – 08:30] Scene 3: Git Andar se: Objects aur Hash
**[VISUAL: Four object types: blob (file content), tree (folder), commit (snapshot + parent + message), tag. A chain of commits linked by parent hashes.]**

**(Voiceover):**
Git ke andar sab kuch objects hain. Blob file ka content hai, tree ek folder ki list, commit ek tree ka snapshot plus uska parent plus message. Har object ka naam uske content ka hash hota hai, isliye content badla to hash badal jata hai. Commits ek chain banate hain, har commit apne parent ko point karta hai. Isi wajah se Git history ko chupke se badalna mushkil hai, aur wo itna tez aur bharosemand hai.

### [08:30 – 11:30] Scene 4: Lab: Pehla Repo
**[VISUAL: Terminal: `git config --global user.name`, `git init`, create `app.py`, `git status`, `git add`, `git commit -m`, `git log --oneline`, edit and `git diff`.]**

**(Voiceover):**
Lab. Pehle identity: `git config --global user.name "Aapka Naam"` aur `user.email`. Phir `mkdir hello && cd hello && git init`. `echo "print('hi')" > app.py`, `git status` mein untracked file dikhegi. `git add app.py`, `git commit -m "Add first script"`, `git log --oneline` mein commit dikhega. Ab file badlo, `git diff` se badlav dekho, aur ek aur commit karo. Commit message hamesha batata hai kyun badla, sirf "update" nahi.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "working dir → add → staging → commit → repo · commit = snapshot".]**

**(Voiceover):**
Recap: teen zone, commits, hash. Ab Git ki asli shakti: branches, yani parallel duniya mein kaam karna.

---

# 📺 EPISODE 2: Branch aur Merge

### [00:00 – 01:15] Scene 1: Do Log, Ek File, Ek Raat
**[VISUAL: Two developers edit the same project simultaneously. Without branches, the edits collide; with branches, each works in their own lane and merges later.]**

**(Voiceover):**
Do developers ko alag alag feature banane hain, ek hi code par. Agar dono seedha main mein likhein, to ek doosre ka kaam tod denge. Branch ek alag lane hai: aap apna kaam apni lane mein karte ho, aur jab taiyaar ho to main mein milate ho.

### [01:15 – 05:00] Scene 2: Branch Sirf ek Pointer Hai
**[VISUAL: A commit chain C1-C2-C3 with `main` label on C3. A new label `feature/login` also on C3, then a new commit C4 appears only for `feature/login`. HEAD arrow points to the current branch.]**

**(Voiceover):**
Git mein branch ek commit ko point karne wala ek chhota label hai, koi copy nahi. Isliye banana aur badalna bahut sasta hai. `HEAD` batata hai ki aap abhi kaun si branch par ho. `git switch -c feature/login` nayi branch banata hai aur use par le jata hai. Ab naye commits sirf us branch ko aage badhate hain, main ko nahi. Ye aasani hi wajah hai ki Git mein feature branch workflow itna aam hai.

### [05:00 – 08:30] Scene 3: Merge: Fast-forward aur Merge Commit
**[VISUAL: Two diagrams. Fast-forward: main simply moves forward. Three-way merge: a merge commit with two parents. A short note on rebase as rewriting commits onto a new base.]**

**(Voiceover):**
Kaam khatam hone par `git switch main` aur `git merge feature/login`. Agar main ke peeche koi naya commit nahi aaya, to Git bas main ko aage khisaka deta hai, ise fast-forward kehte hain. Agar main bhi aage badh chuka ho, to ek merge commit banta hai jisme do parents hote hain. Rebase ek alag tareeka hai jo apne commits ko naye base par dobara chalata hai, jisse history seedhi dikhti hai. Rule: jo commits aap share kar chuke ho, unhe rebase mat karo.

### [08:30 – 11:30] Scene 4: Lab: Feature Branch
**[VISUAL: Terminal: `git switch -c feature/greeting`, edit, commit, `git switch main`, `git merge feature/greeting`, `git branch -d`, `git log --oneline --graph --all`.]**

**(Voiceover):**
Lab: pehle wale repo mein `git switch -c feature/greeting` karo, `app.py` mein ek line jodo, commit karo. `git switch main` karo, dekho ki line gayab hai. Ab `git merge feature/greeting`, line wapas aa gayi. `git branch -d feature/greeting` se branch hatao. Aur `git log --oneline --graph --all` se poori kahani ek picture mein dekho. Ab aap branching ke baadshah ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "branch = pointer · switch -c · merge ff vs 3-way · don't rebase shared".]**

**(Voiceover):**
Recap: branch, merge, rebase. Ab team ke saath: GitHub, jahan code online rehta hai aur review hota hai.

---

# 📺 EPISODE 3: GitHub, Pull Request aur Code Review

### [00:00 – 01:15] Scene 1: Git vs GitHub
**[VISUAL: A laptop with a local repo (Git) and a cloud box labelled GitHub, connected by arrows `push` and `pull`. A caption: "Git is the tool, GitHub is the hosting".]**

**(Voiceover):**
Git aur GitHub ek hi cheez nahi. Git wo tool hai jo aapke laptop par chalta hai. GitHub ek website hai jahan aapke repos online rehte hain, jahan team collaborate karti hai, review karti hai, aur CI chalata hai. Aur GitLab, Bitbucket jaisi aur bhi aise services hain.

### [01:15 – 05:00] Scene 2: Remote, Push, Pull, Clone
**[VISUAL: `git remote add origin ...`, `git push -u origin main`, `git clone`, `git fetch`, `git pull`. A diagram: local ↔ origin. A mini card on SSH key auth for GitHub.]**

**(Voiceover):**
Remote ek online copy ka naam hai, jisko aam taur par `origin` kehte hain. `git push` aapke commits online bhejta hai, `git clone` poora repo laata hai, `git fetch` naye commits laata hai bina aapki files badle, aur `git pull` fetch plus merge hai. GitHub se login ke liye ya to HTTPS ke saath personal access token, ya SSH key, jo hum Linux session mein bana chuke hain. Password se push ab nahi chalta, aur token ko ek password ki tarah surakshit rakhna padta hai.

### [05:00 – 08:30] Scene 3: Pull Request ka Poora Safar
**[VISUAL: A PR page: title, description, diff view, reviewers, checks passing, comments, "Approve", "Squash and merge". Branch protection rules shown on main.]**

**(Voiceover):**
Pull request, PR, ek request hai ki "meri branch ko main mein milao". Isme diff dikhta hai, teammates comments karte hain, aur CI checks chalte hain. Achhe PR ki pehchaan: chhota, ek hi kaam, saaf description. Reviewer ke liye: logic, security, tests aur readability dekho, aur vyakti nahi, code par comment karo. Main branch par protection lagao: seedha push band, review zaroori, aur checks pass hone par hi merge. Merge ke tareeke: merge commit, squash ya rebase, team ek chun leti hai.

### [08:30 – 11:30] Scene 4: Lab: Apna PR Banao
**[VISUAL: A new GitHub repo. Local: clone, create a branch, commit, `git push -u origin feature/readme`, open a PR in the browser, review own PR, merge, delete branch, `git pull`.]**

**(Voiceover):**
Lab: GitHub par ek naya repo banao, usse clone karo. `git switch -c feature/readme`, README mein ek line jodo, commit karo, `git push -u origin feature/readme`. Browser mein "Compare & pull request" par click karo, ek acchi description likho, aur merge karo. Phir local mein `git switch main && git pull` aur dekho ki badlav aa gaya. Repo settings mein main branch par ek protection rule lagao jisme review zaroori ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "origin · push/pull · PR = review + checks · protect main".]**

**(Voiceover):**
Recap: GitHub, PR, aur code review. Ab sabse darr wali cheez: merge conflict, aur galti hone par undo.

---

# 📺 EPISODE 4: Conflicts, Undo aur Team Workflow

### [00:00 – 01:15] Scene 1: <<<<<<< HEAD
**[VISUAL: A file with conflict markers `<<<<<<<`, `=======`, `>>>>>>>`. The developer panics. A calm hand resolves it.]**

**(Voiceover):**
Aapne kabhi file mein `<<<<<<< HEAD` jaise ajeeb symbol dekhe? Ye merge conflict hai, aur ye galti nahi, ek sawaal hai: do logon ne ek hi line badli, to Git poochh raha hai ki kaun sa rakhna hai. Darne ki zaroorat nahi, bas tareeka samajhna hai.

### [01:15 – 05:00] Scene 2: Conflict Resolve Karna
**[VISUAL: A file showing: `<<<<<<< HEAD` our version, `=======`, their version, `>>>>>>> feature`. The user edits to the final text, removes markers, `git add`, `git commit`.]**

**(Voiceover):**
Conflict mein `<<<<<<< HEAD` aur `=======` ke beech aapka version hota hai, aur `=======` aur `>>>>>>>` ke beech doosra. Aap file ko edit karke wo final version rakhte ho jo sahi hai, kabhi dono ka mix, aur markers hata dete ho. Phir `git add` aur `git commit`. VS Code ya koi merge tool ye dekhne mein madad karta hai. Aur conflict kam karne ka tareeka: chhote branches, baar baar main ko pull karna, aur aapas mein baat karna.

### [05:00 – 08:30] Scene 3: Undo ke Tareeke
**[VISUAL: A decision tree: Unstaged change → `git restore file`. Staged → `git restore --staged`. Last commit wrong → `git commit --amend`. Pushed commit wrong → `git revert`. Lost work → `git reflog`.]**

**(Voiceover):**
Galti ke hisaab se undo. File ke badlav hatane ho to `git restore file`. Staging se hatana ho to `git restore --staged file`. Last commit ka message ya content sudharna ho aur abhi push nahi kiya, to `git commit --amend`. Jo commit push ho chuka, uske liye `git revert`, jo ek naya commit bana kar badlav ko ulat deta hai, history ko nahi chhedta. `git reset --hard` khatarnaak hai, kyunki wo kaam hata deta hai. Aur kuch kho jaye to `git reflog` aapki aakhri halaton ki list dikha deta hai.

### [08:30 – 11:30] Scene 4: Lab: Conflict Banao aur Hal Karo
**[VISUAL: Two branches change the same line in `app.py`. Merge produces a conflict. Resolve in VS Code, commit. Then `git revert HEAD` on a bad commit.]**

**(Voiceover):**
Lab: `app.py` mein ek line likho aur commit karo. Do branches banao, `a` aur `b`, dono mein wahi line alag alag tarah badlo aur commit karo. `a` ko main mein merge karo, phir `b` ko merge karo: conflict. File kholo, sahi version rakho, markers hatao, `git add app.py && git commit`. Ab ek galat commit banao aur `git revert HEAD` se use ulat do. Ye lab aapko conflicts se aur undo se bhaybheet nahi, sahaj bana dega.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "conflict = a question · restore/amend/revert · reflog saves · small PRs".]**

**(Voiceover):**
Recap: Git ka poora toolkit: commits, branches, PRs, conflicts aur undo. Ab hum isse ek automation machine se jodte hain: CI/CD. Aap commit karoge aur ek machine khud build, test aur deploy karegi. Pehla tool: Jenkins.
