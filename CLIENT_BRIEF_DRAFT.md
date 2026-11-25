# Client brief and sample ticket (DRAFT for review)

Status: **approved by the author on 2026-11-25 and applied** to Session 00 (brief, ticket/handover explanation, client sheet) and, as a pilot, tickets and handover notes in Sessions 8, 13, 22, 25 and 31 (script and lab guide). Other sessions get tickets later, only where they fit. Story rule: `ANALOGY_STORY.md` rule 3.
Companion to `ANALOGY_STORY.md`. The spoken and on-screen lines are in the same Roman-script Hinglish as the scripts; the notes are English.

## The one rule that keeps the story from confusing the technical parts

1. **Story for the why, real names for the what.** A story word is always followed by (or paired with) the real term the first time: "building, yaani EC2 instance". Commands, settings, errors and numbers never use story words.
2. **The client voice is the only place the story speaks in a ticket.** The ticket's asks, "done when" checks and the handover note are plain technical English.
3. **Optional per session.** A session with no natural client need (for example a pure concept episode) simply has no ticket. Nothing is forced.

---

## Part 1: The client brief (goes in Session 00, Episode 1 or 4)

**Client:** Atithi Hotels, owned by **Mrs. Mehta** (a hotel owner, not a techie). **You** are the DevOps / cloud engineer she hired.

### Her message (on screen, then read aloud)

> "Namaste. Humare paas ek booking website hai, par wo hamare ek purane computer par chalti hai. Sale ke din hamara site baith jaata hai aur guests phone kaat dete hain. Mujhe nahi pata ye sab kaise hota hai, mujhe bas ye chahiye:"

### The six needs (her words, then the engineer's translation)

| # | What Mrs. Mehta says | What you hear (real term) | Where the course delivers it |
|---|---|---|---|
| 1 | "Sale wale din bhi site chalni chahiye." | Scaling, load balancing, high availability | Sessions 10, 11, 24, 25 |
| 2 | "Koi booking kabhi gum nahi honi chahiye." | Database backups, snapshots, persistent storage | Sessions 10, 13, 25 |
| 3 | "Bill mere haath se bahar na jaye." | Budgets, tagging, cleanup, right-sizing | Sessions 1, 8, 12 |
| 4 | "Sirf meri team andar aaye, guest ka data safe rahe." | IAM, SSH keys, security groups, secrets | Sessions 4, 9, 14, 20 |
| 5 | "Naya feature jaldi aaye, par site tootay nahi." | Git, CI/CD, containers, GitOps | Sessions 16 to 22, 31, 31B |
| 6 | "Guest ko problem dikhne se pehle mujhe pata chal jaye." | Monitoring, alerts, logs, AIOps | Sessions 15, 26, 33 |

(Multi-cloud and the AI sessions fit as a bonus request: "kal ko hum doosre cloud par bhi ja sakte hain" and "ek smart assistant chahiye". They need no separate need line.)

### Her promise to you, as the "contract" (on screen, three lines)

- Aap kaam ek-ek **ticket** mein karoge. Har ticket ke ant mein ek **handover note** likhoge.
- Ticket tabhi poora, jab "Done when" ke saare checks pass ho.
- Sab kuch temporary lab account mein: kaam ke baad delete.

### Where it fits in Session 00

- **Episode 1, Scene 2** (the story) gets the message above (about 30 seconds).
- **Episode 4, Scene 5** (the Day 0 activity) gets the contract and one extra task: "Mrs. Mehta ke six needs apni copy mein likho, aur har need ke saamne Session number likhte jao jaise course aage badhe."
- This **adds** about 250 words and **removes** none.

---

## Part 2: Sample ticket (Session 8, AWS and EC2 basics)

This reuses what we really tested on 24 November 2026, so every "Done when" check is a real command we ran.

### TICKET ATITHI-008: First server for the booking site

**Client says (Mrs. Mehta):** "Pehla server aaj hi live ho jaye. Bas ek simple page dikhna chahiye, aur sirf meri team andar ja sake."

**Constraints**
- Region: `ap-south-1` (Mumbai). Instance type `t3.micro`.
- SSH only from **your own IP** (`/32`), never `0.0.0.0/0`. Web (port 80) open to everyone.
- IMDSv2 only (token required).
- Tag everything `Project=atithi-lab` and name it `atithi-demo-web`.
- Everything deleted at the end of the lab.

**Deliver**
1. A running Ubuntu server with nginx, set up through **user data** (`lab_files/userdata.sh`).
2. The page text `Atithi Hotels: Book Now` visible in a browser at `http://PUBLIC-IP`.

**Done when** (each is checked with a command; "expected" is what we really saw)

| Check | How | Expected |
|---|---|---|
| Page is live | `curl -s http://PUBLIC-IP` | `<h1>Atithi Hotels: Book Now</h1>...` |
| SSH works from your IP | `ssh -i key.pem ubuntu@PUBLIC-IP` | login succeeds |
| SSH is not open to the world | `aws ec2 describe-security-groups ...` | port 22 source is your `/32` only |
| IMDSv2 enforced | `curl` to the metadata address without a token | `401`; with a token it answers |
| Tags present | `aws ec2 describe-instances` | `Name` and `Project` tags |

**Common trap (real, from our test):** the user data was saved with the last line wrong, so nginx showed the default welcome page. User data runs **only on first boot**; editing it later does not rerun it. Read it back with `describe-instance-attribute --attribute userData` before you blame nginx.

### HANDOVER NOTE (what the student writes at the end; plain technical English)

```
Ticket:        ATITHI-008 First server
Built:         1 x t3.micro (Ubuntu), nginx via user data, security group atithi-demo-sg
Reach it:      http://<public-ip> (web), SSH from <my-ip>/32 only
Changes on stop/start:  public IP changes (tested); private IP and disk stay
Cost while running:     <price per hour from the pricing page> + 8 GiB gp3 disk; ours ran about 1 hour: cents
Undo:          terminate instance (volume goes with it), delete security group and key pair, delete .pem
Known gaps:    single server (no failover), HTTP only (no TLS), manual setup (Terraform comes in Session 27)
Next ticket:   ATITHI-009 (staff access with IAM)
```

The **"Known gaps"** line is the thread that joins one session to the next: it names what a later session fixes.

---

## Part 3: How this changes the work, if you approve

| Piece | Change | Size |
|---|---|---|
| Session 00 script | Add the brief (Episode 1, Scene 2) and the contract and activity (Episode 4, Scene 5) | about 250 words |
| Other sessions | **Optional** one ticket per session, shown at the start of the lab and a handover note at the end | about 100 words each, only where it fits |
| Lab guides | A "Ticket" box at the top and a "Handover note" box at the end | small, no technical change |
| Teleprompter | Only Session 00 and the sessions you choose are re-extracted and re-rendered (Session 01 stays as is) | small |

**A suggestion on order:** if you like this, add the brief to Session 00 and tickets to a **handful** of sessions first (for example 8, 13, 22, 25, 31), render and upload those, and add more tickets later without redoing everything.

## Questions for you

1. Is **Mrs. Mehta** (a non-technical owner) the right client voice, or do you want someone else (a manager, an investor)?
2. The six needs: any to add, drop, or reword?
3. Is the **handover note** too much for students, or is it the valuable part?
