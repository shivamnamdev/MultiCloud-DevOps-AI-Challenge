# ✍️ 02: SCRIPT — SESSION-16 (Part A): Git on Your Own Laptop
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Teaching order and scenarios: the author's own Git cohort, days 1 to 9 (`GIT_NOTES_INTEGRATION_MAP.md`).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S16A`
- **Focus:** Why version control, three zones, first-time setup (`git config`, name, email, default branch, editor), reading history (log/diff/show/blame), `.gitignore` and its tracked-file trap, `git rm` and `git mv`, branches and merges, conflicts, inside `.git`, switching branches with unfinished work
- **Builds on:** Session 03 (terminal, files, editors), Session 02 (check what the assistant tells you, here with `git help` and the docs)
- **Tested with:** every Git command in the new scenes was run on Git 2.43 (Ubuntu 24.04) in November 2026
- **Continues in:** `SESSION-16B_github-and-team-workflows` (remotes, pull requests, stash, cherry-pick, undo, team run)
- **Story position:** Zoom level 3, head office. Atithi Hotels ka design studio khulta hai, aur har design ka hisaab ek register mein rakha jaata hai.
- **Lab project:** `atithi-booking`, Atithi ki booking website (`index.html`, `contact.html`, `style.css`)
- **Story words used:** design (code), drawing table (working directory), approval tray (staging area), register (Git repository), revision (commit), revision number (hash), draft (branch), master (main), "aap yahan ho" pin (HEAD), register ka pichla kamra (`.git`), do designers ne ek hi deewar khiskayi (merge conflict)
- **Episodes:**
  - Episode 1: Git kyun: Drawing Table, Tray aur Register
  - Episode 2: History Padhna: Kya Badla, Kab Badla
  - Episode 3: Draft aur Merge: Dark Mode, Bina Live Site Tode
  - Episode 4: Register ke Andar: `.git`, HEAD aur Adhoora Kaam

---

# 📺 EPISODE 1: Git kyun?

### [00:00 – 01:50] Scene 1: "Pichhle Hafte Jaisa Kar Do"
**[VISUAL: Atithi Hotels head office, design studio. The owner points at the booking website: "Offer banner lagao." A week later, same owner: "Hata do, pichhle hafte jaisa kar do." The designer opens a folder: `booking_final.zip`, `booking_final_v2.zip`, `booking_final_v2_REAL.zip`.]**

**(Voiceover):**
Atithi Hotels ka campus ban chuka hai. Ab hum head office mein hain, jahan hotel ki services ke design bante hain, yaani code. Owner kehta hai: booking page par offer banner lagao. Team laga deti hai. Ek hafte baad wahi owner: hata do, pichhle hafte jaisa kar do. Ab sawaal ye hai ki pichhle hafte kaisa tha? Kisne kya badla tha? Agar jawab `booking_final_v2_REAL.zip` mein hai, to aap mushkil mein ho. Is session mein hum design ka register banayenge, yaani Git: har badlaav ka hisaab, kisne kiya, kab kiya, kyun kiya, aur zaroorat par purane revision par wapas jaana.

### [01:50 – 04:20] Scene 2: Teen Jagah: Table, Tray, Register
**[VISUAL: Three areas in a row. A drawing table with loose sheets (Working Directory). An approval tray holding selected sheets (Staging Area). A bound register with dated, signed pages (Repository). Arrows: `git add` from table to tray, `git commit` from tray to register.]**

**(Voiceover):**
Studio mein design teen jagah se guzarta hai. Pehli: drawing table, jahan aap kaam karte ho, kaat-peet karte ho. Ye working directory hai, yaani aapka folder. Doosri: approval tray, jahan aap wahi sheets rakhte ho jo agle revision mein jaani hain. Ye staging area hai, aur `git add` sheet ko tray mein rakhta hai. Teesri: register, jahan revision tareekh aur dastakhat ke saath hamesha ke liye darj hota hai. Ye repository hai, aur `git commit` tray ki sheets ko register mein chadha deta hai. Ek revision yaani ek commit: us pal ka poora snapshot. Ab tray ki zaroorat kyun? Socho aapne paanch files badli. Teen ek feature ki hain, do sirf experiment. Tray ke bina sab ya kuch nahi. Tray ke saath aap chunte ho ki is revision mein kya jayega.

### [04:20 – 06:45] Scene 3: Pehle Setup: Naam, Email aur Pehla Branch
**[VISUAL: A terminal: `git --version`, then `git config --global user.name "Asha"`, `git config --global user.email`, `git config --global init.defaultBranch main`, `git config --global core.editor nano`, and `git config --list`. A red message "Author identity unknown" on a commit without a name, and a yellow hint about the branch called master.]**

**(Voiceover):**
Register shuru karne se pehle ek chhota setup. `git --version` se dekho ki Git hai ya nahi. Phir apni pehchaan: `git config --global user.name "Asha"` aur `git config --global user.email "asha@example.com"`. Ye zaroori hai, kyunki har revision par likhne wale ka naam jaata hai. Na ho to pehle commit par Git rok deta hai: `Author identity unknown`, `Please tell me who you are`. Email wahi rakho jo aapke GitHub account mein hai, jo Session 16B mein kaam aayega. Ek aur setting: `git config --global init.defaultBranch main`. Iske bina Ubuntu par naye repo ka pehla branch `master` hota hai, aur Git ek hint bhi deta hai. Editor ke liye `git config --global core.editor nano`, taaki commit message ke liye vim mein na phanso. `git config --list` mein sab setting dikhti hai.

### [06:45 – 09:05] Scene 4: Lab: Pehla Register
**[VISUAL: Terminal: `git config --global user.name`, `user.email`, `mkdir atithi-booking`, `git init -b main`, create `index.html`, `git status`, `git add index.html`, `git status`, `git commit -m "Add booking homepage"`, then `contact.html`, `git log`. A `.gitignore` file with `.env` and `node_modules/`.]**

**(Voiceover):**
Lab. Pehle dastakhat: `git config --global user.name "Aapka Naam"` aur `user.email`. Phir `mkdir atithi-booking`, andar jao, aur `git init -b main`. Isse ek chhupa hua `.git` folder banta hai, wahi register hai. `echo "<h1>Atithi Hotels: Book Now</h1>" > index.html`. Ab `git status`: file untracked hai, yaani table par padi hai aur Git ne abhi use apnaya nahi. `git add index.html`, phir `git status`: ab wo tray mein hai. `git commit -m "Add booking homepage"`: pehla revision darj. Isi tarah `contact.html` banao aur commit karo. `git add .` table ki saari badli hui files ek saath tray mein rakhta hai. Aur ek file abhi bana lo, `.gitignore`: isme wo naam likho jo register mein kabhi nahi jaane chahiye, jaise `.env`, passwords wali files aur `node_modules/`.

### [09:05 – 11:20] Scene 5: Lab: Galti, aur Status ki Aadat
**[VISUAL: `echo "BROKEN" > index.html`, `git status` shows "modified". `git restore index.html` brings the page back. Then `git add experiment.html`, `git restore --staged experiment.html`. Two commit messages side by side: "update" (crossed out) and "Fix wrong phone number on contact page" (ticked).]**

**(Voiceover):**
Ab jaan-boojh kar todo. `echo "BROKEN" > index.html`. Homepage gaya. `git status` kehta hai modified. Par register ka aakhri revision bilkul surakshit hai, kyunki aapne ye gadbad na tray mein rakhi, na darj ki. `git restore index.html` table ki sheet ko aakhri revision jaisa kar deta hai. Dhyan rahe, ye wapas nahi aata: jo commit nahi hua, wo gaya. Doosra case: galat file tray mein rakh di. `git restore --staged experiment.html` use tray se wapas table par le aata hai, kaam nahi khota. Do aadatein yahin se pakdo. Ek: har command ke baad `git status`, jab tak teen jagahein aankh band karke na dikhne lagein. Do: commit message batata hai kyun badla. "update" nahi, "Fix wrong phone number on contact page".

### [11:20 – 14:10] Scene 6: `.gitignore` aur File Hatana, Naam Badalna
**[VISUAL: A project folder with `.env`, `app.log` and `index.html`. A `.gitignore` file with `*.log` and `.env`. A trap: `.env` already tracked, still showing ` M .env` after being ignored; then `git rm --cached .env` and a clean status with the file still on disk. Then `git mv a.txt b.txt` showing `R  a.txt -> b.txt`.]**

**(Voiceover):**
Har file register mein nahi jaani chahiye: password ki file `.env`, log files, `node_modules` jaise bhaari folders. Inke liye ek file `.gitignore`, jisme pattern likho, jaise `*.log` aur `.env`, aur Git unhe tray mein nahi lega. Ek jaal, jo hamare test mein dikha: agar file pehle hi register mein aa chuki hai, to `.gitignore` mein naam likhne se wo hat nahi jaati, aur Git uske badlaav dikhata rehta hai. Tab `git rm --cached .env`: register se hatao, par kamre mein file rehne do. Aur yaad rakho, purani history mein wo file ab bhi hai, to agar usme secret tha, use leak maano aur badlo, jaise Session 20 mein. File ka naam badalna ho to `git mv a.txt b.txt`, jo rename ko ek hi badlaav ki tarah likhta hai, aur `git log --follow b.txt` purana itihaas bhi dikhata hai. `git rm` file ko hatata hai aur hatane ko tray mein daal deta hai.

### [14:10 – 15:20] Scene 7: Recap aur Bridge
**[VISUAL: A card: "table → `git add` → tray → `git commit` → register · status after every step". Under it, small: "working directory · staging area · repository".]**

**(Voiceover):**
Recap: drawing table yaani working directory, approval tray yaani staging area, register yaani repository, aur har revision ek commit. `restore` table ki galti hatata hai, `restore --staged` tray se wapas laata hai. Ab register mein revisions jama ho rahe hain. Par jis din kuch toot-ta hai, us din sawaal hota hai: kya badla tha, aur kab? Agle episode mein hum register ko padhna seekhenge.

---

# 📺 EPISODE 2: History Padhna

### [00:00 – 02:05] Scene 1: "Chaar Din Pehle Theek Tha"
**[VISUAL: A phone rings in the studio. Hotel manager on the line: "Contact page par email galat hai. Chaar din pehle theek tha." The designer stares at eight revisions and cannot remember which one changed it.]**

**(Voiceover):**
Do hafte ho gaye, register mein aath revisions hain. Tabhi hotel manager ka phone aata hai: contact page par email galat hai, guests ki mail kahin aur ja rahi hai, aur chaar din pehle sab theek tha. Aapko yaad nahi ki chaar din pehle page kaisa tha, na ye ki kis revision ne use badla. Andaza lagane ki zaroorat nahi. Register sab jaanta hai, bas use padhna aana chahiye. Is episode mein teen sawaal: kya kya hua, kya badla, aur us din file kaisi thi.

### [02:05 – 04:55] Scene 2: `git log`: Register ke Panne
**[VISUAL: Terminal: `git log` with full entries (hash, author, date, message). Then `git log --oneline` as a compact list. Then `git log --name-only` listing files under each commit. A label on the hash: "revision number".]**

**(Voiceover):**
`git log` register ke panne ulta kholta hai, sabse naya upar. Har entry mein chaar cheezein: revision number, yaani commit hash, kisne kiya, kab kiya, aur message. Hash ek lamba unique ID hai, par kaam ke liye uske pehle saat akshar kaafi hote hain. Poori detail zyada lage to `git log --oneline`: har revision ek line mein. Aur `git log --name-only` ye bhi dikhata hai ki kis revision mein kaun si files badli. Hamare case mein yahi kaam ka hai: contact page kis kis revision mein chhua gaya, turant dikh jaata hai. Yahan samajh aata hai ki achha commit message kyun zaroori tha. "Update contact email" padh kar aap seedha sahi panne par pahunch jaate ho.

### [04:55 – 07:50] Scene 3: `git diff`: Do Revisions Aamne-Saamne
**[VISUAL: Terminal: `git diff b2c3d4a d4e5f6a`. Output annotated line by line: `diff --git a/contact.html b/contact.html` ("a = before, b = after"), `index ..100644` ("file version IDs, mode"), `@@ -1 +1 @@` ("where in the file"), a red `-` line with the right email and a green `+` line with the wrong one.]**

**(Voiceover):**
`git diff` do revisions ko aamne-saamne rakhta hai. `git diff purana-hash naya-hash`. Output darawna dikhta hai, par ise chaar hisson mein padho. Pehli line: `a/contact.html` pehle wali file hai, `b/contact.html` baad wali. Doosri line `index` se shuru hoti hai: dono versions ke ID, aur ant mein `100644`, yaani normal file. Agar wahan `100755` ho to file executable hai, wahi permission jo Linux session mein dekhi thi. Teesra hissa `@@` wali line: badlaav file mein kahan hai. Aur phir asli cheez: minus wali line pehle thi aur hat gayi, plus wali line nayi aayi. Bina sign wali lines sirf context hain. Akela `git diff` table aur tray ka fark dikhata hai, aur `git diff --staged` tray aur aakhri revision ka.

### [07:50 – 09:45] Scene 4: `git blame`: Ye Line Kisne Likhi
**[VISUAL: A file with two lines. Beside each line a short revision id, an author name and a date. One line is highlighted; its id is passed to `git show` and the commit message appears.]**

**(Voiceover):**
Kabhi kabhi sawaal ye hota hai: is line ko kisne badla, aur kab? `git blame f.txt` har line ke aage dikhata hai ki use aakhri baar kis revision ne, kis ne, aur kab badla. Naam blame hai, par maksad doshi dhoondhna nahi, wajah samajhna hai: us line ke revision ka hash lekar `git show` chalao aur commit message padho. Isi liye achhe commit message ki keemat yahin pata chalti hai. `git blame -L 10,20 f.txt` sirf kuch lines dikhata hai.

### [09:45 – 12:25] Scene 5: Lab: Galat Email ki Jaanch
**[VISUAL: Terminal builds four commits in `atithi-booking`: homepage, contact page with `stay@atithi.example`, heading update, contact email changed to `stya@atithi.example`. Then `git log --oneline`, `git diff <day2> <day4>`, `git show <day4>`, `git show <day2>:contact.html`.]**

**(Voiceover):**
Lab: `atithi-booking` mein chaar revisions banao. Homepage, phir contact page jisme email `stay@atithi.example` ho, phir homepage ki heading badlo, aur chauthe mein contact email mein jaan-boojh kar typo daalo. Ab jaanch, isi kram mein. Ek: `git log --oneline`, shaq wale revisions dhoondho. Do: `git diff` doosre aur chauthe hash ke beech: minus mein sahi email, plus mein galat. Mil gaya. Teen: `git show chautha-hash` us ek revision ka poora badlaav aur message dikhata hai. Chaar: `git show doosra-hash:contact.html` aapko wo file bilkul waisi dikhata hai jaisi us din thi, bina kahin gaye. Ab sahi email wapas likho aur ek naya revision banao. Aapne kuch yaad nahi kiya, sirf register padha.

### [12:25 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "`log --oneline` → `diff A B` → `show A` → `show A:file`". Under it: "minus = pehle tha · plus = ab hai".]**

**(Voiceover):**
Recap: `git log` batata hai kya kya hua, `git diff` batata hai kya badla, aur `git show` batata hai us din file kaisi thi. Ye jaanch ka kram interview mein bhi kaam aata hai aur production mein bhi. Ab agla sawaal owner ki taraf se aa raha hai: poori website ka naya roop chahiye, par chalti hui site tootni nahi chahiye. Ek hi register mein do kaam saath saath kaise? Agle episode mein: draft.

---

# 📺 EPISODE 3: Draft aur Merge

### [00:00 – 02:20] Scene 1: "Dark Mode Banao, Live Site Mat Todna"
**[VISUAL: The owner at the studio door: "Poori booking site dark mode mein chahiye." Pause. "Aur live site mat todna, guests abhi booking kar rahe hain." Two paths appear: editing the master sheet directly (red), or a separate draft sheet (green).]**

**(Voiceover):**
Owner ka naya hukm: poori booking site dark mode mein chahiye. Aur saath mein shart: live site mat todna, guests abhi booking kar rahe hain. Aapke paas do raaste hain. Seedha master design par kaam karo, aur agar dark mode ne kuch toda to live site tooti. Ya ek alag draft banao, wahan khul kar experiment karo, aur jab sab theek ho tabhi master mein milao. Git mein ye draft hai branch, aur master hai `main`. Is episode mein: draft banana, use master mein milana, aur us din ka hal jab do logon ne ek hi line badal di.

### [02:20 – 05:05] Scene 2: Draft Sirf ek Nishaan Hai
**[VISUAL: A chain of revisions C1-C2-C3 in the register. A clip labelled `main` sits on C3. A second clip `dark-mode` is placed on the same C3. A pin "aap yahan ho" (HEAD) moves from `main` to `dark-mode`. A new revision C4 appears and only the `dark-mode` clip moves. Terminal: `git branch`, `git switch -c dark-mode`, `git log --oneline --graph --all`.]**

**(Voiceover):**
Sabse pehle ek galatfehmi hatao: draft poore design ki photocopy nahi hai. Branch register ke ek panne par laga ek chhota nishaan hai, jo kehta hai "ye draft abhi is revision par hai". Isliye branch banana pal bhar ka kaam hai. `git switch -c dark-mode` naya nishaan lagata hai aur aapko us par le jaata hai. Shuru mein `main` aur `dark-mode` dono ek hi revision par hote hain. Aur ek pin hota hai, `HEAD`, jo batata hai aap abhi kahan khade ho. Ab aap jo naya revision banaoge, sirf wahi nishaan aage badhega jis par aap khade ho. `main` wahin rahega. `git branch` saare drafts dikhata hai, aur `git log --oneline --graph --all` poora naksha.

### [05:05 – 08:35] Scene 3: Merge: Milana, aur Do Nadiyan
**[VISUAL: Diagram 1, fast-forward: the `main` clip slides forward to where `dark-mode` is. Diagram 2, three-way: both lines have moved; a merge commit joins them with two parent arrows. Two rivers joining into one. Terminal: `git switch main`, `git merge dark-mode`, graph view, `git branch -d dark-mode`.]**

**(Voiceover):**
Dark mode tayaar hai. `git switch main`, phir `git merge dark-mode`. Do tarah se mil sakta hai. Agar is beech `main` par koi naya revision nahi aaya, to Git bas `main` ka nishaan aage khiska deta hai. Ise fast-forward kehte hain. Agar `main` bhi aage badh chuka hai, to Git ek naya revision banata hai jiske do parents hote hain. Ye merge commit hai. Ab ek sawaal jo sabko uljhata hai: merge ke baad draft ke commits `main` ke log mein kyun dikhte hain? Do nadiyan milti hain to chhoti nadi ka paani gayab nahi hota, wo badi nadi ka hissa ban jaata hai. Draft ke revisions bhi `main` ki history ka pakka hissa ban jaate hain. Kaam ho gaya to `git branch -d dark-mode`. Rebase ek alag tareeka hai jo history seedhi rakhta hai; rule bas itna: jo commits share ho chuke, unhe rebase mat karo.

### [08:35 – 11:30] Scene 4: Lab: Ek hi Deewar, Do Designers
**[VISUAL: `style.css` with `background: white;`. On `dark-mode` it becomes `background: black;`, on `main` it becomes `background: #f5f0e6;`. `git merge dark-mode` prints CONFLICT. The file shows `<<<<<<< HEAD`, `=======`, `>>>>>>> dark-mode`. Three resolutions shown, then `git add`, `git commit`. A side note: "`--ours` = jahan aap khade ho".]**

**(Voiceover):**
Lab. `style.css` mein ek line likho, `background: white;`, aur commit karo. `git switch -c dark-mode`, use `black` karo, commit. Wapas `main` par, wahi line cream rang karo, commit. Ab `git merge dark-mode`: CONFLICT. Do designers ne ek hi deewar khiska di, aur Git andaza nahi lagata, wo poochhta hai. File kholo. `<<<<<<< HEAD` ke neeche aapka version hai, `=======` ke neeche aane wala. Teen raaste hain. `main` wala rakho: `git checkout --ours style.css`. Draft wala rakho: `git checkout --theirs style.css`. Ya dono ko haath se milao aur markers hata do. `ours` hamesha wo branch hai jis par aap khade ho. Phir `git add style.css` aur `git commit`. Aur agar beech mein ghabrahat ho, `git merge --abort` sab kuch merge se pehle jaisa kar deta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "branch = nishaan · `switch -c` · fast-forward ya merge commit · conflict = sawaal · `merge --abort`".]**

**(Voiceover):**
Recap: draft yaani branch ek nishaan hai, copy nahi. Merge ya to nishaan khiskata hai ya do parents wala revision banata hai. Conflict galti nahi, ek sawaal hai, aur uske teen jawab hain. Ab tak hum register ko upar se chala rahe the. Agle episode mein hum uske pichle kamre mein jaayenge aur dekhenge ki ye nishaan aur pin asal mein kahan rakhe hain.

---

# 📺 EPISODE 4: Register ke Andar

### [00:00 – 02:10] Scene 1: Pichla Kamra
**[VISUAL: The designer opens a small door behind the register shelf marked `.git`. Inside: a pin board labelled HEAD, a rack of clips labelled refs, a tray log labelled index, shelves of numbered boxes labelled objects. Terminal: `ls -la`, `ls .git`.]**

**(Voiceover):**
Aap hafton se `git add` aur `git commit` chala rahe ho. Par ye sab jaata kahan hai? `ls -la` chalao: ek chhupa hua folder dikhega, `.git`. Yahi asli register hai. Aapka project folder sirf drawing table hai; history, drafts aur settings sab is pichle kamre mein hain. Is folder ko hatana yaani poori history hatana. Aaj hum ise khol kar dekhenge, kyunki jo ye samajh leta hai use phir koi Git command jaadu nahi lagta. Aur isi se ek aisa sawaal suljhega jo sabko pareshan karta hai: draft badalte waqt adhoora kaam kahan jaata hai?

### [02:10 – 04:40] Scene 2: Pin, Nishaan aur Tray ki Soochi
**[VISUAL: Terminal: `cat .git/HEAD` prints `ref: refs/heads/main`. `git switch dark-mode`, `cat .git/HEAD` prints `ref: refs/heads/dark-mode`. `ls .git/refs/heads`, `cat .git/refs/heads/main` prints a 40-character hash. `ls -la .git/index`. `cat .git/config`.]**

**(Voiceover):**
`cat .git/HEAD`. Andar ek line: `ref: refs/heads/main`. Ye wahi pin hai, "aap yahan ho". `git switch dark-mode` karo aur dobara dekho: ab wahan `dark-mode` likha hai. Ab `ls .git/refs/heads`: har branch ke naam ki ek chhoti file. `cat .git/refs/heads/main`: andar sirf ek commit hash. Bas. Branch ek file hai jisme ek revision number likha hai. Naya commit banta hai to isi file ka number badal jaata hai. Isiliye branch sasti hai. Teesri cheez: `.git/index`. Ye approval tray ki soochi hai. `git add` isi file ko badalta hai. Aur `.git/config` is register ki settings hain. Naam aur email wali global settings aapke home folder ki `~/.gitconfig` mein rehti hain.

### [04:40 – 07:50] Scene 3: Dabbe: Blob, Tree, Commit, aur Hooks
**[VISUAL: `ls .git/objects`. A diagram: COMMIT (author, date, message, parent) points to a TREE (file names) which points to BLOBs (file contents). A chain of commits linked by parent arrows. Then `ls .git/hooks` showing `pre-commit.sample`, `pre-push.sample`, `commit-msg.sample`.]**

**(Voiceover):**
`ls .git/objects`: yahan Git ka saara maal rakha hai, teen tarah ke dabbon mein. Blob: ek file ka content. Tree: ek folder ki soochi, kaun sa naam kis blob ka hai. Commit: ek tree ki taraf ishaara, saath mein kisne, kab, kyun, aur pichhla commit kaun sa tha. Har dabbe ka naam uske content ka hash hai, isliye content badla to naam badla. Aur har commit apne parent ko point karta hai, isi se chain banti hai. Isi wajah se history ko chupke se badalna mushkil hai. Ek aur folder: `.git/hooks`. Ye wo scripts hain jo Git ke kisi kaam se pehle ya baad apne aap chalti hain. `pre-commit` commit se pehle jaanch chala sakta hai, `pre-push` push rok sakta hai. Ise yaad rakho: agle session mein vault ki ghanti isi soch ka bada roop hai.

### [07:50 – 11:05] Scene 4: Lab: Adhoora Kaam aur Draft Badalna
**[VISUAL: Two experiments. A: on `main`, edit `notes.txt` (same content on both branches), `git switch branch-a` succeeds and the change travels along. B: `contact.html` differs between `main` and `branch-b`; edit it on `main`, `git switch branch-b` is refused: "Your local changes would be overwritten". Three options card: commit · stash · restore.]**

**(Voiceover):**
Lab, do prayog. Pehla: ek file jo dono drafts mein ek jaisi hai, use `main` par badlo, commit mat karo, aur `git switch branch-a`. Git jaane deta hai, aur aapka badlaav saath chala aata hai. Doosra: ek file jo dono drafts mein alag alag commit hui hai, use `main` par badlo aur switch karo. Git mana kar deta hai: "your local changes would be overwritten". Kyun? Kyunki draft badalte waqt Git table ki sheets ko us draft ke revision se badalta hai. Jahan aapka adhoora kaam us badlaav ke raaste mein aata hai, wahan wo rukta hai taaki kuch khoye nahi. Asli rule: adhoora kaam kisi draft ka nahi hota jab tak commit na ho. Aur aapke paas teen raaste hain: commit kar do, `git restore` se hata do, ya `git stash` se alag rakh do, jo hum agle session mein seekhenge.

### [11:05 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "`.git` = register · HEAD = aap yahan ho · branch = ek file, ek hash · index = tray · blob → tree → commit". Then the laptop alone on a desk, with a question mark above it.]**

**(Voiceover):**
Recap: `.git` hi register hai. `HEAD` pin hai, branch ek file jisme ek hash hai, `index` tray ki soochi, aur blob, tree, commit teen dabbe. Adhoora kaam kisi draft ka nahi jab tak commit na ho. Ab ek darr wali baat: ye poora register sirf ek laptop ke ek folder mein hai. Laptop gaya to sab gaya, aur team ke baaki log ise dekh bhi nahi sakte. Agle session mein Atithi ek central vault banata hai jahan sab designers milte hain: GitHub.


---

# 📎 Student handout: Session 16 (Part A) cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Setup | `git config --global user.name`, `user.email`, `init.defaultBranch main`, `core.editor nano`; na ho to "Author identity unknown" |
| Teen jagah | Drawing table (working folder), approval tray (staging), register (commits) |
| Roz ka chakkar | `git status` har kadam par; `add`; `commit -m`; `log --oneline` |
| Padhna | `git log`, `git diff` (teen roop), `git show`, `git blame -L a,b FILE` |
| Galti sudharna | `git restore FILE`, `git restore --staged FILE` |
| `.gitignore` | Patterns; pehle se tracked file par asar nahi; `git rm --cached FILE`; history mein purani file rehti hai |
| Hatana aur naam | `git rm FILE`, `git mv OLD NEW`, `git log --follow NEW` |
| Branch | Ek nishaan, copy nahi; `git switch -c NAME`; `git branch -d` |
| Merge | Fast-forward ya merge commit; conflict markers; `git merge --abort` |
| `.git` ke andar | `HEAD`, `refs`, objects: blob, tree, commit; hooks |
