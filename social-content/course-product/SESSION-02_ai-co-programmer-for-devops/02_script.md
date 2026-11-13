# ✍️ 02: SCRIPT — SESSION-02: AI Co-Programmer for DevOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S02`
- **Focus:** How LLMs work (just enough), prompting for DevOps, AI on logs/IaC/review, verification habits, agents
- **Episodes:**
  - Episode 1: AI andar se kaise sochta hai: tokens, context aur hallucination
  - Episode 2: Prompt Engineering: DevOps ke liye RTCF framework
  - Episode 3: AI se kaam: code, config, logs aur code review
  - Episode 4: Agents, Guardrails aur "Trust but Verify" ki aadat

---

# 📺 EPISODE 1: AI andar se kaise sochta hai

### [00:00 – 01:15] Scene 1: Confident Galat Jawab
**[VISUAL: A chat window. User: "Command to list EC2 instances older than 7 days?" AI answers with a smooth command. The terminal runs it: red "Unknown option". Stamp: "SOUNDS RIGHT ≠ IS RIGHT".]**

**(Voiceover):**
Aapne AI se command maangi. Jawab itna confident tha ki aapne bina padhe terminal mein chala diya, aur error. Ye galti AI ki bhi hai, aur ek had tak aapki bhi. Is episode ka maksad AI ko jaadu se hata kar ek tool ki tarah samajhna hai. Jab aap jaante ho ki wo andar se kaise kaam karta hai, tab aapko pata hota hai kab uspar bharosa karna hai aur kab nahi.

### [01:15 – 04:30] Scene 2: LLM = Agla Shabd Predict Karne wali Machine
**[VISUAL: A sentence typed word by word: "Kubernetes is a container ___" with a probability bar: "orchestration 62%, platform 21%, system 9%...". The top word is picked.]**

**(Voiceover):**
Large Language Model, yaani LLM, ka basic kaam hai agla shabd predict karna. Usne internet ka bahut saara text padha hai, aur ab wo har baar poochta hai: is context ke baad sabse sambhavit agla tukda kya hai. Is tukde ko token kehte hain, jo ek shabd, shabd ka hissa ya symbol ho sakta hai. Isse do cheezein samajh aati hain. Ek, AI ko "pata" nahi hota, wo sambhavit likhta hai. Do, jab context mein sahi jaankari na ho, wo bhi kuch sambhavit sa likh deta hai. Wahi hallucination hai.

### [04:30 – 08:00] Scene 3: Context Window, Training Cutoff aur Tool Versions
**[VISUAL: A window frame holding a chat. Old messages scroll out of the left side and fade. A calendar marked "Training cutoff" with newer tool logos beyond it greyed.]**

**(Voiceover):**
Do limits yaad rakho. Pehli, context window: AI ek baar mein sirf utna text dekh sakta hai. Lambi chat mein shuru ki baatein bhoolne lagti hain, isliye important cheezein baar baar yaad dilao. Doosri, training cutoff: model ne ek tareekh tak ka hi data dekha hota hai. Naye tool versions, naye flags, naye cloud features, wo galat ya purane de sakta hai. DevOps mein ye bahut kaata hai, kyunki tools har mahine badalte hain. Isliye official docs hi final authority hain.

### [08:00 – 11:30] Scene 4: Lab: Hallucination Pakdo
**[VISUAL: Split terminal and chat. User asks for "docker run flags to limit memory and cpu". AI answers. The user opens `docker run --help` and ticks each flag green or red.]**

**(Voiceover):**
Lab: AI se poochho "docker run mein memory aur CPU limit kaise lagate hain". Jo command aaye, usse chalane se pehle `docker run --help` ya official docs se har flag tick karo. Dhyaan se dekho ki kaun sa flag sach mein exist karta hai. Agar sab sahi nikla to bhi aadat banao: har AI command ke liye ek verification step. Ye aadat aapko us raat bachayegi jab AI ne `rm -rf` jaisi koi cheez bina context ke suggest ki ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: Two-column card: "AI is good at: drafts, boilerplate, explanations" / "AI is risky at: versions, your environment, secrets".]**

**(Voiceover):**
Recap: LLM sambhavit text banata hai, context limited hai, data purana ho sakta hai. Isliye AI draft ke liye ek great tool hai, final decision ke liye nahi. Agla sawaal: AI se behtar jawab kaise nikalein? Wo hai prompt engineering, aur DevOps ke liye uska ek seedha framework.

---

# 📺 EPISODE 2: Prompt Engineering — RTCF Framework

### [00:00 – 01:15] Scene 1: Do Prompt, Do Natije
**[VISUAL: Two prompts side by side. Left: "Make a Dockerfile". Right: a detailed prompt with stack, constraints, and output format. The right output is a clean multi-stage Dockerfile; the left is generic.]**

**(Voiceover):**
"Ek Dockerfile bana do." Aur doosra: "Node 20 ki Express app ke liye multi-stage Dockerfile, non-root user, aur chhoti image." Pehle ka jawab generic, doosre ka jawab kaam ka. Fark AI mein nahi, prompt mein hai. AI ek bahut samajhdar intern ki tarah hai: jitna saaf kaam doge, utna accha dega. Aaj ka framework yaad karna aasaan hai: R, T, C, F.

### [01:15 – 05:00] Scene 2: R-T-C-F: Role, Task, Context, Format
**[VISUAL: Four blocks light up in sequence with an example for each: Role: "Senior SRE". Task: "Find why the pod restarts". Context: "Logs, K8s 1.29, 512Mi limit". Format: "3 likely causes, then commands".]**

**(Voiceover):**
Role: AI ko batao wo kaun hai, jaise "tum ek senior SRE ho". Task: kaam ek line mein, jaise "ye pod baar baar restart kyun ho raha hai". Context: jo aapko pata hai, wo sab: logs, versions, limits, kya try kiya. Format: jawab kaise chahiye, jaise "teen sambhavit wajah, har ek ke liye ek command". Context sabse zaroori hai, kyunki AI aapka environment dekh nahi sakta. Aur ek baat: secrets, passwords aur private keys kabhi prompt mein mat daalna.

### [05:00 – 08:30] Scene 3: Iterate, Examples aur Step-by-Step Reasoning
**[VISUAL: A chat conversation where the user refines: "Shorter", "Use alpine", "Explain each line". Each reply improves. A side note: "Show 1 example of the style you want".]**

**(Voiceover):**
Pehle jawab par ruko mat. Chhote changes maango: "image aur chhoti karo", "har line samjhao", "ye non-root ke saath dikhao". Agar ek khaas style chahiye, ek example de do, AI usko follow karta hai. Aur jab problem jatil ho, bolo "step by step socho aur pehle plan batao". Isse AI jaldi jawab dene ki jagah rasta banata hai. Lekin ek rule: lambe plan ke baad bhi har command aap khud check karoge.

### [08:30 – 11:30] Scene 4: Lab: Ek Kharab Prompt ko Sudhaaro
**[VISUAL: A scorecard: Role ✔/✘, Task ✔/✘, Context ✔/✘, Format ✔/✘. The prompt "fix my pipeline" scores 0/4, then rewritten scores 4/4.]**

**(Voiceover):**
Lab: ek kharab prompt lo, jaise "mera pipeline fail ho raha hai, fix karo". Ab RTCF ke saath dobara likho: role SRE, task failing stage ka root cause, context mein Jenkins ka error log aur kya badla, format mein "teen kaaran aur check karne ki commands". Dono prompts chalao aur jawab compare karo. Ye 5 minute ka exercise aapki roz ki productivity badal dega.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A sticky note on a monitor: "R·T·C·F + Verify".]**

**(Voiceover):**
Recap: Role, Task, Context, Format, aur aakhir mein verify. Ab dekhte hain ki AI ko DevOps ke asli kaam mein kaise lagayein: code, config, logs aur review. Episode 3 mein.

---

# 📺 EPISODE 3: AI se DevOps ka Kaam

### [00:00 – 01:15] Scene 1: Raat ke 2 Baje ka Log
**[VISUAL: A wall of 3,000 log lines scrolling. One red line is buried inside. A magnifying glass drops onto it.]**

**(Voiceover):**
Production mein error aaya, aur aapke saamne teen hazaar log lines hain. Insaan ke liye ye dhoondhna thakane wala hai. AI is jagah kamal ka sahayak ho sakta hai, kyunki wo lambe text ko jaldi padh kar patterns nikal deta hai. Aaj hum teen kaam dekhenge: logs ka analysis, config ka draft, aur code review.

### [01:15 – 05:00] Scene 2: Logs ka Analysis
**[VISUAL: A screen showing a log excerpt pasted into the chat with a prompt: "Group these errors, tell the first failure, suggest 3 checks." AI response highlights the first error line.]**

**(Voiceover):**
Logs paste karte waqt pehle secrets hata do: tokens, passwords, internal IPs. Phir bolo: "sabse pehla failure kaun sa hai, baaki errors uske result to nahi, aur teen checks batao." Dhyaan rahe ki pehla error aksar asli wajah hota hai, aur uske baad ke zyadatar errors uske natije. AI ko ye bataoge to wo noise ke beech se signal nikalta hai. Phir bhi, jo check wo suggest kare, wo aap khud chalaoge.

### [05:00 – 08:30] Scene 3: Config aur IaC ka Draft
**[VISUAL: An editor with a YAML draft generated by AI. Reviewer annotations: "pin version", "add resource limits", "no hardcoded secret".]**

**(Voiceover):**
Kubernetes YAML, Terraform, GitHub Actions workflow: AI inka pehla draft kaafi tez de deta hai. Lekin draft ko hamesha review checklist se guzaaro: image version pinned hai ya `latest`? Resource limits hain? Secret hardcoded to nahi? Permissions zaroorat se zyada to nahi? Ye sawaal aap poochhoge, AI nahi. Aur ek tip: AI se bolo "is config mein kya galat ho sakta hai" aur wo apna hi draft criticize karke achhe points nikalta hai.

### [08:30 – 11:30] Scene 4: Lab: AI Code Review
**[VISUAL: A small Bash script with a risky line `rm -rf $DIR/*` where DIR may be empty. The AI flags it; the user fixes with `set -u` and a check.]**

**(Voiceover):**
Lab: ek chhoti Bash script lo jisme `rm -rf $DIR/*` jaisi line ho, aur AI se review karwao. Dekho kya wo is khatre ko pakadta hai ki agar DIR khaali hai to command root ke andar delete kar sakta hai. Phir fix karo: `set -u` lagao aur check karo ki DIR khaali na ho. Is tarah aap AI ko reviewer ki tarah istemaal karte ho, aur final approve aap karte ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: Three-step loop: "Draft by AI → Check by you → Test in a safe place".]**

**(Voiceover):**
Recap: logs mein AI shuruaat ka rasta dikhata hai, config mein draft deta hai, review mein dusri aankh banta hai. Hamesha: draft AI ka, check aapka, test safe jagah par. Ab last episode: agents. Jab AI sirf bolta nahi, kaam bhi karta hai, tab guardrails kitne zaroori ho jaate hain.

---

# 📺 EPISODE 4: Agents, Guardrails aur Trust but Verify

### [00:00 – 01:15] Scene 1: Jab AI Khud Commands Chalane Lage
**[VISUAL: A terminal where an AI agent proposes a series of commands and runs them: `git checkout`, `terraform apply`. A big red "Approve?" dialog hovers.]**

**(Voiceover):**
Ab tak AI sirf jawab deta tha. Agent ek aisa AI hai jo tools use karke kaam kar sakta hai: files padhna, commands chalana, API call karna. Ye bahut powerful hai, aur isiliye khatarnaak bhi. Agar AI ko aapke production ki permission mil gayi aur usne ek galat command chala di, to nuksaan seedha asli hoga. Isliye is episode ka mool mantra: pehle guardrails, phir autonomy.

### [01:15 – 05:00] Scene 2: Chatbot, Copilot, Agent: Farq
**[VISUAL: Three tiers: Chatbot (talks), Copilot (suggests in your editor), Agent (plans and acts with tools). Each tier lists "what it can touch".]**

**(Voiceover):**
Chatbot sirf baat karta hai. Copilot aapke editor mein code suggest karta hai, aur aap accept ya reject karte ho. Agent plan banata hai aur tools ke through kaam bhi karta hai. Jaise jaise AI ko zyada kaam milta hai, uske paas utni hi zyada power hoti hai, aur utni hi zyada galti ki keemat. Isliye har step par poochho: ye AI kya touch kar sakta hai?

### [05:00 – 08:30] Scene 3: Guardrails ki Checklist
**[VISUAL: A shield with five labels: Least privilege, Read-only first, Human approval, Sandbox, Audit log.]**

**(Voiceover):**
Paanch guardrails yaad rakho. Least privilege: AI ko sirf zaroori permission do. Read-only pehle: pehle dekhne do, badalne baad mein. Human approval: production badalne wale step par insaan ki haan zaroori. Sandbox: test environment mein hi experiment. Aur audit log: har action ka record, taaki baad mein pata chale kisne kya kiya. Ye wahi principles hain jo hum insaano ke liye bhi lagate hain, bas AI par bhi lagani hain.

### [08:30 – 11:30] Scene 4: Lab: Safe Agent Workflow
**[VISUAL: A repo with a branch `ai/fix-yaml`. The agent opens a pull request. A reviewer comments, runs the pipeline, and merges.]**

**(Voiceover):**
Lab: ek test repo banao. AI se ek chhota change maango, jaise YAML mein resource limit add karna, aur use main par nahi, ek alag branch par karwao. Fir ek pull request kholo, pipeline chalao, khud diff padho aur tab merge karo. Ye safe workflow hai: AI draft karta hai, git history record karti hai, pipeline test karti hai, aur insaan final haan deta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A closing card: "AI = autopilot. You = pilot." with the Build → Ship → Fix arrow.]**

**(Voiceover):**
Recap: agent ko tab tak power mat do jab tak guardrails na ho. Draft AI ka, jaanch aapki, final haan insaan ki. Ye soch poore course mein saath chalegi, har tool ke saath. Ab ek solid neev banate hain: Linux. Kyunki cloud ka zyadatar hissa Linux par hi chalta hai.
