# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-16B_github-and-team-workflows

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,548 · **Episodes:** 4

---

# EPISODE 1: Vault

## Ek Laptop, Poori History

Pichhle session mein humne dekha tha ki poora register ek hi laptop ke .git folder mein hai. Ab socho us laptop par coffee gir gayi. Do hafte ki history gayi. Aur agar laptop theek bhi ho, to teen aur designers us design ko dekhenge kaise? Atithi Hotels iska hal head office mein banata hai: ek central vault, jahan har project ke register ki ek copy rehti hai aur jahan sab designers apna kaam jama karte hain. Ye vault hai GitHub. Is episode mein: apna register vault se jodna, kaam bhejna, doosron ka kaam lana, aur ek naye laptop par poora project utaarna.

## Git vs GitHub, aur origin

Pehle fark saaf kar lo. Git wo tool hai jo aapke laptop par chalta hai. GitHub ek service hai jahan registers online rehte hain; GitLab aur Bitbucket bhi aisi hi hain. Vault se judne ke liye aap ek remote banate ho: git remote add origin aur vault ka URL. origin sirf ek naam hai. Jaise phone mein number ke saath naam save karte ho taaki har baar poora number na likhna pade. git remote -v dikhata hai kaun sa naam kis pate par hai. Aur vault mein ghusne ke liye pehchaan chahiye. GitHub password se push nahi leta. Do raaste hain: HTTPS ke saath personal access token, ya SSH key. Session 4 mein jo key banayi thi, uski public key GitHub ki settings mein jodo, aur ssh -T git@github.com se jaanch lo.

## Push, Fetch, Pull, Clone

Chaar commands, chaar disha. git push -u origin main aapke revisions vault mein bhejta hai. -u ek baar ka rishta banata hai: aapka main vault ke main se juda hai, isliye agli baar sirf git push kaafi hai. Aur Git har baar poora project nahi bhejta, sirf wo revisions jo vault ke paas nahi hain. git fetch vault se naye revisions le aata hai, par aapki table ko haath nahi lagata. Wo unhe origin/main naam ke ek alag khaane mein rakh deta hai taaki aap pehle dekh sako. git pull fetch karta hai aur phir us kaam ko aapke draft mein mila bhi deta hai. Yaani fetch: laao aur dekho. Pull: laao aur lagao. Aur git clone vault se poora register ek naye laptop par utaarta hai, history aur origin ke saath. Clone ke baad git init ki zaroorat nahi.

## Lab: Register ko Vault mein Rakhna

Lab. GitHub par ek naya public repo banao, atithi-booking, bina README ke. Local folder mein git remote add origin aur URL, phir git push -u origin main. Browser refresh karo: aapki files aur poori history wahan hain. Ab ek teammate ban jao: GitHub par hi pencil icon se README mein ek line jodo aur commit karo. Wapas terminal mein git fetch. Kuch badla nahi dikhta, par git log --oneline main..origin/main batata hai ki vault mein ek revision hai jo aapke paas nahi. git diff main origin/main se dekho kya hai, aur phir git pull. Ab wo aapki table par bhi hai. Aakhir mein ek doosre folder mein git clone karo aur git log --oneline chalao: naya laptop, poori history.

## Recap aur Bridge

Recap: Git aapka tool hai, GitHub vault. origin vault ka naam, push bhejta hai, fetch laata hai, pull laakar lagata hai, aur clone poora utaarta hai. Ab vault mein paanch designers hain, aur sab seedha master mein push kar sakte hain. Ek shukravaar ki shaam koi adhoora kaam master mein daal deta hai, aur booking site band. Agle episode mein hum master par taala lagayenge aur chief architect ka review layenge: pull request.

---

# EPISODE 2: Pull Request

## Shukravaar ki Shaam ka Push

Shukravaar, shaam chhah baje. Ek designer jaldi mein apna kaam seedha main mein push kar deta hai. Kisi ne dekha nahi, kisi ne jaancha nahi. Booking page par error, aur paanch phone ek saath bajte hain. Us din Atithi ka design studio ek rule banata hai: master mein seedha kuch nahi jaayega. Har kaam apne draft par hoga, vault mein jayega, aur chief architect ke review ke baad hi master mein milega. GitHub par is review ka naam hai pull request. Is episode mein poora safar, aur wo do rukawatein jo har nayi team ko pehle hafte milti hain.

## Draft se Master tak ka Safar

Safar aise chalta hai. Hamesha taaza master se shuru karo: git switch main, git pull. Phir apna draft: git switch -c feature/offers-page. Kaam karo, commit karo, aur draft ko vault mein bhejo: git push -u origin feature/offers-page. GitHub turant ek button dikhata hai, "Compare and pull request". Title saaf likho, description mein batao kya badla aur kyun. Ab reviewer "Files changed" mein har line dekhta hai, kisi line par comment karta hai, aur ya to approve karta hai ya badlaav maangta hai. Badlaav maange gaye to naya PR nahi banta: usi draft par ek aur commit karo aur push karo, PR khud update ho jaata hai. Approve ke baad merge. Merge ke teen tareeke hain, merge commit, squash aur rebase; team ek chun leti hai. Pull request sirf merge ka button nahi, baatcheet aur jaanch hai.

## Do Rukawatein, aur Master par Taala

Pehli rukawat: aap push karte ho aur Git kehta hai "rejected, fetch first". Matlab vault ka register aage badh chuka hai, kisi ne aapse pehle push kar diya. Hal: pehle git pull, zaroorat ho to conflict suljhao, phir git push. Agar pull poochhe ki milana kaise hai, to ek baar git config --global pull.rebase false set kar do, yaani merge. Zabardasti mat karo. Agar apne hi draft par force karna pade, to git push --force-with-lease use karo: wo tabhi push karta hai jab vault par kisi aur ka naya kaam na aaya ho (par fetch karne ke baad ye jaanch bhi paas ho jaati hai, isliye pehle dekho kya fetch hua), jabki seedha --force doosre ka kaam mita sakta hai. main par force push ko to taale ne hi rok diya hai. Yaani force wahi, jahan sirf aapka apna kaam daanv par ho. Doosri rukawat: aapka draft purane master se nikla tha, aur PR par likha aata hai ki branch out-of-date hai. Hal: apne draft par git merge main karo aur push karo, ya conflict na ho to GitHub ka "Update branch" button. Aur ab taala: repo ki settings mein main par rule lagao, "Require a pull request before merging". Ab Shukravaar wali galti ho hi nahi sakti. Is chhote, seedhe tareeke ka naam GitHub Flow hai: main hamesha chalne layak, har kaam ek chhote draft par.

## Lab: Pehla Pull Request

Lab. atithi-booking mein git switch main, git pull, phir git switch -c feature/offers-page. Ek offers.html banao, commit karo, aur git push -u origin feature/offers-page. Browser mein PR kholo. Description mein teen line: kya badla, kyun, aur kaise jaancha. "Files changed" mein apni hi ek line par comment likho, jaise "heading mein hotel ka naam jodo". Terminal mein wo sudhaar karo, commit, push, aur dekho PR mein naya commit aa gaya. Merge karo aur draft hata do. Local mein git switch main, git pull, git branch -d feature/offers-page. Ab main par taala lagao, saath mein "Do not allow bypassing the above settings" bhi chuno taaki rule owner par bhi lage, aur seedha main mein push karke dekho: vault mana kar dega. Review ko zaroori banane ke liye doosra account chahiye, isliye ek dost ko collaborator bana lo.

## Recap aur Bridge

Recap: taaze master se draft, draft vault mein, PR, review, merge, aur wapas sync. Push rejected ho to pehle pull. Draft purana ho to usme main milao. Aur master par taala. Ye tareeka tab tak aaram se chalta hai jab tak koi beech mein na toke. Par asli din aise nahi hote: aap aadhe kaam mein ho aur phone aata hai, "production down hai, abhi dekho". Agle episode mein: adhoora kaam sambhalna.

---

# EPISODE 3: Adhoora Kaam

## "Sab Chhodo, Production Down Hai"

Aap ek naye feature ke beech mein ho. Teen files badli hain, ek tray mein hai, aur code abhi chalta bhi nahi. Tabhi message: booking page down hai, abhi main par fix chahiye. Commit kar nahi sakte, kyunki kaam toota hua hai. Chhod nahi sakte, kyunki do ghante ki mehnat hai. Aur pichhle session mein dekha tha ki Git aise mein draft badalne se mana bhi kar sakta hai. Is episode mein teen auzaar jo roz ke aise palon ke liye bane hain: adhoora kaam alag rakhna, purane revision ko jaa kar dekhna, aur poore draft ki jagah sirf ek revision uthana.

## Stash: Designer ki Daraaz

git stash adhoore kaam ko table aur tray dono se utha kar ek daraaz mein rakh deta hai, aur table saaf ho jaati hai. Naam ke saath rakho: git stash push -m "WIP: room filter". Ab git switch main, bug theek karo, commit karo. Wapas apne draft par aao aur git stash pop: aapka saara adhoora kaam wapas table par. Tray wali cheezein bhi tray mein hi chahiye to git stash pop --index. git stash list daraaz ki saari cheezein dikhata hai, sabse nayi stash@{0}. pop nikaal kar daraaz se hata deta hai; git stash apply nikaalta hai par ek copy daraaz mein chhod deta hai. Do baatein yaad rakho. Ek: stash nayi, untracked files ko nahi uthata jab tak -u na lagao. Do: daraaz aapki apni hai. Stash kabhi vault mein nahi jaata, isliye use lambe samay ka store mat banao.

## Detached HEAD: Archive ka Reading Room

Manager kehta hai: kal wala contact page behtar tha, zara dikhao. git log --oneline se revision number lo aur git checkout wo hash, ya naye tareeke se git switch --detach. Git ek lamba sa message deta hai: detached HEAD. Ghabrao mat. Matlab sirf itna hai ki pin ab kisi draft par nahi, seedha ek purane revision par laga hai. cat .git/HEAD mein ab branch ka naam nahi, hash hai. Ise archive ka reading room samjho: dekh sakte ho, chala kar parakh sakte ho, par yahan naya kaam mat karo. Kyunki yahan bana commit kisi draft ka nahi hota, aur wapas jaate hi lawaris ho jaata hai. Dekh liya to git switch main. Aur agar wahan kuch kaam ka ban gaya ho, to jaane se pehle git switch -c rescue-idea: ab us par ek nishaan hai aur wo surakshit hai.

## Lab: Cherry-Pick, Sirf Tayaar Panna

Lab. Ek draft banao, feature/homepage, aur us par do commits: pehla ek tayaar heading, doosra ek adhoora animation. Owner ko heading aaj hi chahiye. Poora draft merge karoge to adhoora animation bhi master mein chala jaayega. Hal: git cherry-pick. Pehle git log --oneline se heading wale commit ka hash note karo. Phir git switch main, git pull, aur ek chhota draft: git switch -c pick/offer-heading. Ab git cherry-pick aur wo hash. Sirf wahi ek badlaav yahan aa gaya. Dhyan do: ye copy hai, aur jab base alag ho, jaise team mein aksar hota hai, iska hash naya hoga. Is draft ko push karo aur PR banao, taaki ye bhi review se hi master mein jaaye. Merge poora draft laata hai; cherry-pick ek panna. Hotfix aur production patch aise hi jaate hain. Conflict aaye to suljha kar git cherry-pick --continue.

## Recap aur Bridge

Recap: git stash adhoora kaam daraaz mein rakhta hai aur pop wapas laata hai. Detached HEAD purana revision dekhne ka reading room hai; kuch banaya to branch bana kar bachao. Cherry-pick poore draft ki jagah ek revision laata hai. Ye sab rukawaton ke auzaar the. Ab galtiyon ki baari: galat file commit ho gayi, galat commit push ho gaya, galat PR merge ho gaya. Agle episode mein undo ka poora naksha, aur phir paanch logon ki team ka ek poora din.

---

# EPISODE 4: Undo ka Naksha aur Poori Team ka Ek Din

## Teesra Hafta, Ek Ghanta, Chaar Galtiyan

Naukri ka teesra hafta. Ek ghante mein chaar galtiyan: teen sahi lines mit gayi, galat file tray mein chali gayi, toota hua kaam commit ho gaya, aur wo push bhi ho gaya. Lead ka message: main ko kya hua? Sabse bada darr ye nahi ki galti hui. Darr ye hai ki theek karte hue aur bigad na jaaye. Git mein har galti ka ilaaj hai, par ilaaj is par nirbhar hai ki galti kahan tak pahunchi: table par hai, tray mein, register mein, ya vault mein. Is episode mein pehle ye naksha, phir ek aisi lab jisme is poore session ka har hissa ek saath chalta hai.

## Galti Kahan Hai? Table, Tray ya Register

Sawaal upar se neeche poochho. Sirf table par galti hai? git restore file. Tray mein chali gayi? git restore --staged file. Register mein commit ho gayi par push nahi hui? Yahan git reset aata hai, teen roop mein. git reset --soft HEAD~1: aakhri commit hat jaata hai, par saara kaam tray mein rehta hai. Tab kaam ka jab jaldi mein commit kar diya ya ek file reh gayi. git reset HEAD~1, yaani mixed: commit hata, tray khaali, par files table par surakshit. Tab kaam ka jab galat files ek saath commit ho gayi. git reset --hard HEAD~1: commit bhi gaya aur table ka kaam bhi. Ise tabhi chalao jab sach mein kuch nahi chahiye. Sirf aakhri commit ka message ya ek chhooti file sudharni ho to git commit --amend. Aur agar reset mein kuch kho jaaye, git reflog aapke pichhle saare padaav dikhata hai.

## Vault mein Pahunch Gayi: Sudhaar Parchi

Ab chautha sawaal: galti vault mein push ho chuki hai. Yahan reset mat karo. Reset aapka register chhota kar dega, phir aapko git push --force karna padega, aur jin teammates ne wo commit pull kar liya tha unke register vault se alag ho jaayenge. Share ho chuki history ko dobara likhna team ko todta hai. Sahi tareeka: git revert aur us commit ka hash; agar wo merge commit hai, to git revert -m 1 hash, warna Git mana kar deta hai. Ye kuch mitata nahi. Ye ek naya commit banata hai jo us badlaav ko ulta kar deta hai. Register mein ek sudhaar parchi lag jaati hai, panna koi nahi phatta, aur sabki history ek jaisi rehti hai. Galat PR merge ho gaya? GitHub par us PR ke neeche "Revert" button hai, jo ek revert PR bana deta hai. Aur ek khaas case: password ya API key push ho gayi. Pehla kaam history saaf karna nahi, wo chaabi turant radd karna hai. Ise session 20 mein poora dekhenge.

## Lab: Paanch Roles, Ek Repo

Lab: ek repo, paanch roles. Dost hon to baant lo, akele ho to do folders aur ek doosre account se khelo. Owner repo banata hai, main par taala lagata hai aur collaborators jodta hai. Lead designer saaf raasta chalta hai: draft, about page, PR, review, merge, cleanup. Senior designer index.html badalta hai, aur usi beech owner bhi main par wahi file badal deta hai. PR par conflict. Wo apne draft par git merge main karta hai, suljhata hai, push karta hai. Junior designer ka toota hua badlaav merge ho jaata hai; team GitHub ke Revert button se use ulta karti hai aur sab git pull karte hain. Paanchva baahar ka contractor hai, jiske paas vault ki chaabi nahi. Wo repo ko fork karta hai, yaani apni copy, use clone karta hai, git remote add upstream se asli repo jodta hai, git fetch upstream aur git merge upstream/main se taaza hota hai, aur apne fork se PR bhejta hai. Ant mein owner mohar lagata hai: git tag -a v1.0 -m "First release" aur git push origin v1.0.

## Recap aur Bridge

Recap: galti table par ho to restore, tray mein ho to restore --staged, register mein ho to reset, aur vault mein pahunch gayi ho to revert. Aur team ka tareeka: master par taala, har kaam ek draft par, har draft ek PR se, baahar wale fork se. Ab git log --oneline --graph --all chalao aur dekho: paanch logon ka poora din ek naksha mein. Atithi ke designs ab surakshit hain aur sabke saamne hain. Par har naye revision ke baad koi haath se build karta hai, jaanchta hai, pahunchata hai. Agle session mein vault ke darwaze par ek ghanti lagti hai, aur ghanti bajte hi workshop ka foreman kaam shuru kar deta hai: Jenkins.
