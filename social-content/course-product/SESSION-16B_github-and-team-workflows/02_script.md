# ✍️ 02: SCRIPT — SESSION-16 (Part B): GitHub and Team Workflows
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Teaching order and scenarios: the author's own Git cohort, days 10 to 16 (`GIT_NOTES_INTEGRATION_MAP.md`).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S16B`
- **Focus:** Remotes (push/fetch/pull/clone), pull request workflow, push rejected and stale branches, branch protection, stash, detached HEAD, cherry-pick, undo (restore/reset/revert), forks, tags
- **Continues from:** `SESSION-16_git-and-github` (Part A)
- **Story position:** Zoom level 3, head office. Atithi Hotels ek central vault banata hai jahan saare designers milte hain, aur master mein kuch bhi chief architect ke review ke bina nahi jaata.
- **Lab project:** `atithi-booking`, Atithi ki booking website (same repo as Part A)
- **Story words used:** vault (GitHub, remote), chief architect ka review (pull request), master par taala (branch protection), designer ki daraaz (stash), archive ka reading room (detached HEAD), ek panna utha kar lagana (cherry-pick), sudhaar parchi (revert), baahar ka contractor aur uski apni copy (fork), release ki mohar (tag)
- **Episodes:**
  - Episode 1: Vault: Remote, Push, Fetch, Pull, Clone
  - Episode 2: Pull Request: Chief Architect ka Review
  - Episode 3: Adhoora Kaam: Stash, Detached HEAD, Cherry-Pick
  - Episode 4: Undo ka Naksha aur Poori Team ka Ek Din

---

# 📺 EPISODE 1: Vault

### [00:00 – 01:15] Scene 1: Ek Laptop, Poori History
**[VISUAL: A designer's laptop with the `atithi-booking` register inside it. Coffee spills; the screen goes black. Three other designers stand around with nothing to work on. Then a vault door opens at head office, with shelves for every project.]**

**(Voiceover):**
Pichhle session mein humne dekha tha ki poora register ek hi laptop ke `.git` folder mein hai. Ab socho us laptop par coffee gir gayi. Do hafte ki history gayi. Aur agar laptop theek bhi ho, to teen aur designers us design ko dekhenge kaise? Atithi Hotels iska hal head office mein banata hai: ek central vault, jahan har project ke register ki ek copy rehti hai aur jahan sab designers apna kaam jama karte hain. Ye vault hai GitHub. Is episode mein: apna register vault se jodna, kaam bhejna, doosron ka kaam lana, aur ek naye laptop par poora project utaarna.

### [01:15 – 04:30] Scene 2: Git vs GitHub, aur `origin`
**[VISUAL: Left: a laptop labelled "Git = tool". Right: the vault labelled "GitHub = hosting". A phone contact card: name `origin`, number `git@github.com:you/atithi-booking.git`. Terminal: `git remote add origin ...`, `git remote -v`. A small card: "SSH key (Session 4) → GitHub Settings → SSH and GPG keys → `ssh -T git@github.com`".]**

**(Voiceover):**
Pehle fark saaf kar lo. Git wo tool hai jo aapke laptop par chalta hai. GitHub ek service hai jahan registers online rehte hain; GitLab aur Bitbucket bhi aisi hi hain. Vault se judne ke liye aap ek remote banate ho: `git remote add origin` aur vault ka URL. `origin` sirf ek naam hai. Jaise phone mein number ke saath naam save karte ho taaki har baar poora number na likhna pade. `git remote -v` dikhata hai kaun sa naam kis pate par hai. Aur vault mein ghusne ke liye pehchaan chahiye. GitHub password se push nahi leta. Do raaste hain: HTTPS ke saath personal access token, ya SSH key. Session 4 mein jo key banayi thi, uski public key GitHub ki settings mein jodo, aur `ssh -T git@github.com` se jaanch lo.

### [04:30 – 08:00] Scene 3: Push, Fetch, Pull, Clone
**[VISUAL: Four arrows between laptop and vault. `git push -u origin main` (laptop → vault). `git fetch` (vault → a side shelf labelled `origin/main`, table untouched). `git pull` (fetch + merge into the table). `git clone` (vault → a brand-new laptop, complete with history).]**

**(Voiceover):**
Chaar commands, chaar disha. `git push -u origin main` aapke revisions vault mein bhejta hai. `-u` ek baar ka rishta banata hai: aapka `main` vault ke `main` se juda hai, isliye agli baar sirf `git push` kaafi hai. Aur Git har baar poora project nahi bhejta, sirf wo revisions jo vault ke paas nahi hain. `git fetch` vault se naye revisions le aata hai, par aapki table ko haath nahi lagata. Wo unhe `origin/main` naam ke ek alag khaane mein rakh deta hai taaki aap pehle dekh sako. `git pull` fetch karta hai aur phir us kaam ko aapke draft mein mila bhi deta hai. Yaani fetch: laao aur dekho. Pull: laao aur lagao. Aur `git clone` vault se poora register ek naye laptop par utaarta hai, history aur `origin` ke saath. Clone ke baad `git init` ki zaroorat nahi.

### [08:00 – 11:30] Scene 4: Lab: Register ko Vault mein Rakhna
**[VISUAL: GitHub: New repository `atithi-booking`, public, no README. Terminal: `git remote add origin`, `git push -u origin main`. Browser: the pencil icon edits `README.md` and commits on GitHub. Terminal: `git fetch`, `git log --oneline main..origin/main`, `git diff main origin/main`, `git pull`. Then `git clone` into a second folder and `git log --oneline` there.]**

**(Voiceover):**
Lab. GitHub par ek naya public repo banao, `atithi-booking`, bina README ke. Local folder mein `git remote add origin` aur URL, phir `git push -u origin main`. Browser refresh karo: aapki files aur poori history wahan hain. Ab ek teammate ban jao: GitHub par hi pencil icon se README mein ek line jodo aur commit karo. Wapas terminal mein `git fetch`. Kuch badla nahi dikhta, par `git log --oneline main..origin/main` batata hai ki vault mein ek revision hai jo aapke paas nahi. `git diff main origin/main` se dekho kya hai, aur phir `git pull`. Ab wo aapki table par bhi hai. Aakhir mein ek doosre folder mein `git clone` karo aur `git log --oneline` chalao: naya laptop, poori history.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "`origin` = vault ka naam · push = bhejo · fetch = laao aur dekho · pull = laao aur lagao · clone = poora utaaro".]**

**(Voiceover):**
Recap: Git aapka tool hai, GitHub vault. `origin` vault ka naam, push bhejta hai, fetch laata hai, pull laakar lagata hai, aur clone poora utaarta hai. Ab vault mein paanch designers hain, aur sab seedha master mein push kar sakte hain. Ek shukravaar ki shaam koi adhoora kaam master mein daal deta hai, aur booking site band. Agle episode mein hum master par taala lagayenge aur chief architect ka review layenge: pull request.

---

# 📺 EPISODE 2: Pull Request

### [00:00 – 01:15] Scene 1: Shukravaar ki Shaam ka Push
**[VISUAL: Friday 6 PM. A designer pushes straight to `main`. The live booking page shows an error. Five phones ring. Then a rule goes up on the vault door: "Master mein seedha kuch nahi. Pehle review."]**

**(Voiceover):**
Shukravaar, shaam chhah baje. Ek designer jaldi mein apna kaam seedha `main` mein push kar deta hai. Kisi ne dekha nahi, kisi ne jaancha nahi. Booking page par error, aur paanch phone ek saath bajte hain. Us din Atithi ka design studio ek rule banata hai: master mein seedha kuch nahi jaayega. Har kaam apne draft par hoga, vault mein jayega, aur chief architect ke review ke baad hi master mein milega. GitHub par is review ka naam hai pull request. Is episode mein poora safar, aur wo do rukawatein jo har nayi team ko pehle hafte milti hain.

### [01:15 – 04:30] Scene 2: Draft se Master tak ka Safar
**[VISUAL: A flow strip: `git switch main` + `git pull` → `git switch -c feature/offers-page` → commits → `git push -u origin feature/offers-page` → "Compare & pull request" → Files changed (red/green) → review comment → new commit pushed to the same branch → Approve → Merge → `git switch main`, `git pull`, `git branch -d`.]**

**(Voiceover):**
Safar aise chalta hai. Hamesha taaza master se shuru karo: `git switch main`, `git pull`. Phir apna draft: `git switch -c feature/offers-page`. Kaam karo, commit karo, aur draft ko vault mein bhejo: `git push -u origin feature/offers-page`. GitHub turant ek button dikhata hai, "Compare and pull request". Title saaf likho, description mein batao kya badla aur kyun. Ab reviewer "Files changed" mein har line dekhta hai, kisi line par comment karta hai, aur ya to approve karta hai ya badlaav maangta hai. Badlaav maange gaye to naya PR nahi banta: usi draft par ek aur commit karo aur push karo, PR khud update ho jaata hai. Approve ke baad merge. Merge ke teen tareeke hain, merge commit, squash aur rebase; team ek chun leti hai. Pull request sirf merge ka button nahi, baatcheet aur jaanch hai.

### [04:30 – 08:00] Scene 3: Do Rukawatein, aur Master par Taala
**[VISUAL: Terminal 1: `git push` → "rejected ... fetch first". Fix: `git pull`, then `git push`. Screen 2: a PR page saying "This branch is out-of-date with the base branch" with an "Update branch" button; terminal alternative `git switch feature/...`, `git merge main`, `git push`. Screen 3: Settings → Branches → rule on `main`: "Require a pull request before merging".]**

**(Voiceover):**
Pehli rukawat: aap push karte ho aur Git kehta hai "rejected, fetch first". Matlab vault ka register aage badh chuka hai, kisi ne aapse pehle push kar diya. Hal: pehle `git pull`, zaroorat ho to conflict suljhao, phir `git push`. Agar pull poochhe ki milana kaise hai, to ek baar `git config --global pull.rebase false` set kar do, yaani merge. Zabardasti mat karo. Doosri rukawat: aapka draft purane master se nikla tha, aur PR par likha aata hai ki branch out-of-date hai. Hal: apne draft par `git merge main` karo aur push karo, ya conflict na ho to GitHub ka "Update branch" button. Aur ab taala: repo ki settings mein `main` par rule lagao, "Require a pull request before merging". Ab Shukravaar wali galti ho hi nahi sakti. Is chhote, seedhe tareeke ka naam GitHub Flow hai: `main` hamesha chalne layak, har kaam ek chhote draft par.

### [08:00 – 11:30] Scene 4: Lab: Pehla Pull Request
**[VISUAL: Terminal: `git switch main`, `git pull`, `git switch -c feature/offers-page`, create `offers.html`, commit, `git push -u origin feature/offers-page`. Browser: open PR, write description, add a review comment on one line, push a fix commit, merge, delete branch. Terminal: `git switch main`, `git pull`, `git branch -d feature/offers-page`. Then a direct `git push` to `main` is refused by the rule.]**

**(Voiceover):**
Lab. `atithi-booking` mein `git switch main`, `git pull`, phir `git switch -c feature/offers-page`. Ek `offers.html` banao, commit karo, aur `git push -u origin feature/offers-page`. Browser mein PR kholo. Description mein teen line: kya badla, kyun, aur kaise jaancha. "Files changed" mein apni hi ek line par comment likho, jaise "heading mein hotel ka naam jodo". Terminal mein wo sudhaar karo, commit, push, aur dekho PR mein naya commit aa gaya. Merge karo aur draft hata do. Local mein `git switch main`, `git pull`, `git branch -d feature/offers-page`. Ab `main` par taala lagao, saath mein "Do not allow bypassing the above settings" bhi chuno taaki rule owner par bhi lage, aur seedha `main` mein push karke dekho: vault mana kar dega. Review ko zaroori banane ke liye doosra account chahiye, isliye ek dost ko collaborator bana lo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "taaza main → draft → push → PR → review → merge → sync · rejected? pehle pull · out-of-date? `merge main`".]**

**(Voiceover):**
Recap: taaze master se draft, draft vault mein, PR, review, merge, aur wapas sync. Push rejected ho to pehle pull. Draft purana ho to usme `main` milao. Aur master par taala. Ye tareeka tab tak aaram se chalta hai jab tak koi beech mein na toke. Par asli din aise nahi hote: aap aadhe kaam mein ho aur phone aata hai, "production down hai, abhi dekho". Agle episode mein: adhoora kaam sambhalna.

---

# 📺 EPISODE 3: Adhoora Kaam

### [00:00 – 01:15] Scene 1: "Sab Chhodo, Production Down Hai"
**[VISUAL: A designer mid-work: three sheets on the table, one in the tray, the design half drawn. A message pops up: "Booking page down. Abhi main par fix chahiye." The designer looks at the table, then at a desk drawer.]**

**(Voiceover):**
Aap ek naye feature ke beech mein ho. Teen files badli hain, ek tray mein hai, aur code abhi chalta bhi nahi. Tabhi message: booking page down hai, abhi `main` par fix chahiye. Commit kar nahi sakte, kyunki kaam toota hua hai. Chhod nahi sakte, kyunki do ghante ki mehnat hai. Aur pichhle session mein dekha tha ki Git aise mein draft badalne se mana bhi kar sakta hai. Is episode mein teen auzaar jo roz ke aise palon ke liye bane hain: adhoora kaam alag rakhna, purane revision ko jaa kar dekhna, aur poore draft ki jagah sirf ek revision uthana.

### [01:15 – 04:30] Scene 2: Stash: Designer ki Daraaz
**[VISUAL: The designer sweeps the half-drawn sheets into a desk drawer; the table is clean. Terminal: `git stash push -m "WIP: room filter"`, `git status` (clean), `git switch main`, fix, commit, `git switch feature/room-filter`, `git stash list`, `git stash pop`. A note: "`-u` = nayi files bhi".]**

**(Voiceover):**
`git stash` adhoore kaam ko table aur tray dono se utha kar ek daraaz mein rakh deta hai, aur table saaf ho jaati hai. Naam ke saath rakho: `git stash push -m "WIP: room filter"`. Ab `git switch main`, bug theek karo, commit karo. Wapas apne draft par aao aur `git stash pop`: aapka saara adhoora kaam wapas table par. Tray wali cheezein bhi tray mein hi chahiye to `git stash pop --index`. `git stash list` daraaz ki saari cheezein dikhata hai, sabse nayi `stash@{0}`. `pop` nikaal kar daraaz se hata deta hai; `git stash apply` nikaalta hai par ek copy daraaz mein chhod deta hai. Do baatein yaad rakho. Ek: stash nayi, untracked files ko nahi uthata jab tak `-u` na lagao. Do: daraaz aapki apni hai. Stash kabhi vault mein nahi jaata, isliye use lambe samay ka store mat banao.

### [04:30 – 08:00] Scene 3: Detached HEAD: Archive ka Reading Room
**[VISUAL: The manager: "Kal wala contact page behtar tha, zara dikhao." Terminal: `git log --oneline`, `git checkout <hash>` prints "You are in 'detached HEAD' state". `cat .git/HEAD` shows a raw hash. The designer in an archive reading room with a sign: "Dekho, yahan draw mat karo". Then `git switch main`. A rescue path: `git switch -c rescue-idea`.]**

**(Voiceover):**
Manager kehta hai: kal wala contact page behtar tha, zara dikhao. `git log --oneline` se revision number lo aur `git checkout` wo hash, ya naye tareeke se `git switch --detach`. Git ek lamba sa message deta hai: detached HEAD. Ghabrao mat. Matlab sirf itna hai ki pin ab kisi draft par nahi, seedha ek purane revision par laga hai. `cat .git/HEAD` mein ab branch ka naam nahi, hash hai. Ise archive ka reading room samjho: dekh sakte ho, chala kar parakh sakte ho, par yahan naya kaam mat karo. Kyunki yahan bana commit kisi draft ka nahi hota, aur wapas jaate hi lawaris ho jaata hai. Dekh liya to `git switch main`. Aur agar wahan kuch kaam ka ban gaya ho, to jaane se pehle `git switch -c rescue-idea`: ab us par ek nishaan hai aur wo surakshit hai.

### [08:00 – 11:30] Scene 4: Lab: Cherry-Pick, Sirf Tayaar Panna
**[VISUAL: Branch `feature/homepage` with two commits: "Add offer heading" (ticked, ready) and "Try homepage animation" (experimental). Terminal: `git log --oneline`, `git switch main`, `git pull`, `git switch -c pick/offer-heading`, `git cherry-pick <hash>`, `git push -u origin pick/offer-heading`, PR opened. A note: "naya hash, wahi badlaav".]**

**(Voiceover):**
Lab. Ek draft banao, `feature/homepage`, aur us par do commits: pehla ek tayaar heading, doosra ek adhoora animation. Owner ko heading aaj hi chahiye. Poora draft merge karoge to adhoora animation bhi master mein chala jaayega. Hal: `git cherry-pick`. Pehle `git log --oneline` se heading wale commit ka hash note karo. Phir `git switch main`, `git pull`, aur ek chhota draft: `git switch -c pick/offer-heading`. Ab `git cherry-pick` aur wo hash. Sirf wahi ek badlaav yahan aa gaya. Dhyan do: ye copy hai, isliye iska hash naya hoga. Is draft ko push karo aur PR banao, taaki ye bhi review se hi master mein jaaye. Merge poora draft laata hai; cherry-pick ek panna. Hotfix aur production patch aise hi jaate hain. Conflict aaye to suljha kar `git cherry-pick --continue`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "stash = daraaz (sirf aapki) · detached HEAD = reading room · cherry-pick = ek panna, naya hash".]**

**(Voiceover):**
Recap: `git stash` adhoora kaam daraaz mein rakhta hai aur `pop` wapas laata hai. Detached HEAD purana revision dekhne ka reading room hai; kuch banaya to branch bana kar bachao. Cherry-pick poore draft ki jagah ek revision laata hai. Ye sab rukawaton ke auzaar the. Ab galtiyon ki baari: galat file commit ho gayi, galat commit push ho gaya, galat PR merge ho gaya. Agle episode mein undo ka poora naksha, aur phir paanch logon ki team ka ek poora din.

---

# 📺 EPISODE 4: Undo ka Naksha aur Poori Team ka Ek Din

### [00:00 – 01:15] Scene 1: Teesra Hafta, Ek Ghanta, Chaar Galtiyan
**[VISUAL: A new designer, week three. In one hour: deletes three good lines, stages the wrong file, commits something broken, pushes it. A message from the lead: "Main ko kya hua?" The designer's hands hover over the keyboard, frozen.]**

**(Voiceover):**
Naukri ka teesra hafta. Ek ghante mein chaar galtiyan: teen sahi lines mit gayi, galat file tray mein chali gayi, toota hua kaam commit ho gaya, aur wo push bhi ho gaya. Lead ka message: main ko kya hua? Sabse bada darr ye nahi ki galti hui. Darr ye hai ki theek karte hue aur bigad na jaaye. Git mein har galti ka ilaaj hai, par ilaaj is par nirbhar hai ki galti kahan tak pahunchi: table par hai, tray mein, register mein, ya vault mein. Is episode mein pehle ye naksha, phir ek aisi lab jisme is poore session ka har hissa ek saath chalta hai.

### [01:15 – 04:30] Scene 2: Galti Kahan Hai? Table, Tray ya Register
**[VISUAL: A decision ladder, read top-down. "Vault mein push ho gayi?" → next scene. "Register mein commit hui?" → `git reset` with three columns: `--soft` (commit hata, tray bhara), `--mixed` (commit hata, tray khaali, table surakshit), `--hard` (sab hata). "Tray mein hai?" → `git restore --staged`. "Sirf table par?" → `git restore`. Side note: `git commit --amend`, `git reflog`.]**

**(Voiceover):**
Sawaal upar se neeche poochho. Sirf table par galti hai? `git restore file`. Tray mein chali gayi? `git restore --staged file`. Register mein commit ho gayi par push nahi hui? Yahan `git reset` aata hai, teen roop mein. `git reset --soft HEAD~1`: aakhri commit hat jaata hai, par saara kaam tray mein rehta hai. Tab kaam ka jab jaldi mein commit kar diya ya ek file reh gayi. `git reset HEAD~1`, yaani mixed: commit hata, tray khaali, par files table par surakshit. Tab kaam ka jab galat files ek saath commit ho gayi. `git reset --hard HEAD~1`: commit bhi gaya aur table ka kaam bhi. Ise tabhi chalao jab sach mein kuch nahi chahiye. Sirf aakhri commit ka message ya ek chhooti file sudharni ho to `git commit --amend`. Aur agar reset mein kuch kho jaaye, `git reflog` aapke pichhle saare padaav dikhata hai.

### [04:30 – 08:00] Scene 3: Vault mein Pahunch Gayi: Sudhaar Parchi
**[VISUAL: Three registers side by side after a local reset + force push: yours (C1-C2-C3), vault (forced to C1-C2-C3), teammate (C1-C2-C3-C4, now out of line, red). Then the safe way: `git revert <hash>` adds C5 "Revert ..." and all three registers agree. A correction slip stapled into the register. GitHub: a merged PR with a "Revert" button. A red card: "Secret push ho gaya? Pehle chaabi badlo."]**

**(Voiceover):**
Ab chautha sawaal: galti vault mein push ho chuki hai. Yahan reset mat karo. Reset aapka register chhota kar dega, phir aapko `git push --force` karna padega, aur jin teammates ne wo commit pull kar liya tha unke register vault se alag ho jaayenge. Share ho chuki history ko dobara likhna team ko todta hai. Sahi tareeka: `git revert` aur us commit ka hash. Ye kuch mitata nahi. Ye ek naya commit banata hai jo us badlaav ko ulta kar deta hai. Register mein ek sudhaar parchi lag jaati hai, panna koi nahi phatta, aur sabki history ek jaisi rehti hai. Galat PR merge ho gaya? GitHub par us PR ke neeche "Revert" button hai, jo ek revert PR bana deta hai. Aur ek khaas case: password ya API key push ho gayi. Pehla kaam history saaf karna nahi, wo chaabi turant radd karna hai. Ise session 20 mein poora dekhenge.

### [08:00 – 11:30] Scene 4: Lab: Paanch Roles, Ek Repo
**[VISUAL: One repo `atithi-team-site`, five lanes. Owner: creates repo, protects `main`, adds collaborators, later `git tag -a v1.0`. Lead designer: `feature/about-page` → PR → merged. Senior designer: edits `index.html` while the owner also changes it on `main` → conflict → `git merge main` locally → resolved → push. Junior designer: bad change merged → "Revert" on GitHub → `git pull`. Outside contractor: Fork → `git clone` → `git remote add upstream` → `git fetch upstream` → `git merge upstream/main` → branch → PR from fork.]**

**(Voiceover):**
Lab: ek repo, paanch roles. Dost hon to baant lo, akele ho to do folders aur ek doosre account se khelo. Owner repo banata hai, `main` par taala lagata hai aur collaborators jodta hai. Lead designer saaf raasta chalta hai: draft, about page, PR, review, merge, cleanup. Senior designer `index.html` badalta hai, aur usi beech owner bhi `main` par wahi file badal deta hai. PR par conflict. Wo apne draft par `git merge main` karta hai, suljhata hai, push karta hai. Junior designer ka toota hua badlaav merge ho jaata hai; team GitHub ke Revert button se use ulta karti hai aur sab `git pull` karte hain. Paanchva baahar ka contractor hai, jiske paas vault ki chaabi nahi. Wo repo ko fork karta hai, yaani apni copy, use clone karta hai, `git remote add upstream` se asli repo jodta hai, `git fetch upstream` aur `git merge upstream/main` se taaza hota hai, aur apne fork se PR bhejta hai. Ant mein owner mohar lagata hai: `git tag -a v1.0 -m "First release"` aur `git push origin v1.0`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "table → `restore` · tray → `restore --staged` · register → `reset` · vault → `revert`". Then the full graph of the team repo from `git log --oneline --graph --all`. Finally the vault with a bell hanging beside its door, and a workshop visible down the corridor.]**

**(Voiceover):**
Recap: galti table par ho to `restore`, tray mein ho to `restore --staged`, register mein ho to `reset`, aur vault mein pahunch gayi ho to `revert`. Aur team ka tareeka: master par taala, har kaam ek draft par, har draft ek PR se, baahar wale fork se. Ab `git log --oneline --graph --all` chalao aur dekho: paanch logon ka poora din ek naksha mein. Atithi ke designs ab surakshit hain aur sabke saamne hain. Par har naye revision ke baad koi haath se build karta hai, jaanchta hai, pahunchata hai. Agle session mein vault ke darwaze par ek ghanti lagti hai, aur ghanti bajte hi workshop ka foreman kaam shuru kar deta hai: Jenkins.
