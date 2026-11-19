# ✍️ 02: SCRIPT — SESSION-12: Amazon S3
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S12`
- **Focus:** Object storage concepts (bucket, object, key, prefix), durability vs availability vs backup, storage classes, lifecycle rules, versioning and delete markers, Block Public Access, bucket policies, encryption, presigned URLs, instance roles for S3 access, static website hosting, CloudFront with Origin Access Control, cache invalidation
- **Builds on:** Session 09 (IAM policies, roles, instance profile), Session 10 (EBS and snapshots, to contrast with object storage), Session 11 (the booking site behind a marshal)
- **Story position:** Zoom level 2, the rented campus. Campus ke bahar ek anant godown hai (the warehouse): labelled boxes, purane boxes sasti godown mein, aur ek display window jahan brochures bina staff ke dikhte hain.
- **Story words used:** warehouse (bucket), box (object), label (key), godown (cold storage class), display window (static website), brochure stand (CloudFront edge location), duty badge (role), permission letter (policy), photograph (snapshot, from Session 10), guest (end user)
- **Lab project:** the Atithi booking site gets its room photos and brochure page out of the buildings and into a warehouse, and a brochure stand in front of it.
- **Cost rule (AWS):** S3 charges for storage, requests and data going out; CloudFront charges for data going out and requests. Free-tier terms change, so check the live pricing page before the lab. Every lab ends with emptying and deleting the buckets and deleting the distribution.
- **Episodes:**
  - Episode 1: Anant Godown: Bucket, Object aur Key
  - Episode 2: Storage Classes, Lifecycle aur Versioning
  - Episode 3: Access Control: Ek Setting se Leak kaise Hota Hai
  - Episode 4: Display Window aur Brochure Stand: Static Website aur CloudFront

---

# 📺 EPISODE 1: Anant Godown

### [00:00 – 02:00] Scene 1: Building ka Storeroom Bhar Gaya
**[VISUAL: Atithi's booking building with a small storeroom (EBS volume) filling with room photos until the door will not close. A manager points beyond the campus wall to an endless warehouse with labelled boxes, and a dotted line from the building to it.]**

**(Voiceover):**
Atithi ki booking site chal padi hai, aur ab har room ki das das photos, har booking ki PDF invoice, aur har raat ka database backup aa raha hai. Session 10 mein humne buildings ke storeroom, yaani EBS, dekhe the. Wo ek building se juda hota hai, aur uski jagah tay hoti hai. Landlord ke paas iska ek aur jawab hai: campus ke bahar ek anant godown. Ismein aap kisi bhi cheez ko ek label ke saath rakh dete ho, aur kahin se bhi wapas maang lete ho. Is godown ka naam Simple Storage Service hai, yaani S3.

### [02:00 – 04:10] Scene 2: Warehouse, Box aur Label
**[VISUAL: A warehouse sign `atithi-room-photos-2026`. Inside, boxes. Each box carries a label: `rooms/101/front.jpg`. The slashes in the label glow as part of the text, while a drawing of folders is crossed out.]**

**(Voiceover):**
S3 mein teen shabd yaad rakho. Bucket matlab warehouse, jiska naam poori duniya mein sirf ek ka ho sakta hai, kyunki naam address ka hissa banta hai. Object matlab box: aapki file aur uske saath kuch jankari, jaise uska type aur kab bana. Aur key matlab box ka label, jaise `rooms/101/front.jpg`. Dhyaan do: ye slash asli folder nahi hain. Pura `rooms/101/front.jpg` ek hi naam hai, aur `rooms/101/` sirf us naam ka shuruaati hissa, jise prefix kehte hain. Console aapko folders dikhata hai, kyunki wo prefix ke hisaab se dikhata hai, par godown mein koi almari nahi hoti, sirf label wale box hote hain.

### [04:10 – 07:00] Scene 3: File System Nahi, Box Store
**[VISUAL: A split card. Left, Linux disk: open a file, change one line in the middle, save. Right, S3: the whole box is taken out and a whole new box with the same label is put back. A small ruler shows a single box can be huge.]**

**(Voiceover):**
S3 aur Linux ke disk mein ek bada fark hai. Disk par aap file kholte ho, beech ki ek line badalte ho, aur save karte ho. S3 mein aisa nahi hota. Aap poora box daalte ho, ya poora box nikalte ho. Badalna ho, to naya box wahi label lagakar rakh do, jo purane ko badal deta hai. Ek box paanch terabyte tak bada ho sakta hai, par ek hi baar mein daalne ki seema paanch gigabyte hai. Isliye bade box tukdon mein bheje jaate hain, jise multipart upload kehte hain, aur AWS CLI ye khud kar leta hai. Isi wajah se S3 par database ya wo files nahi rakhte jo har second badalti hain. Wahan EBS sahi hai. S3 un cheezon ke liye hai jo ek baar likhi jaati hain aur baar baar padhi jaati hain.

### [07:00 – 09:30] Scene 4: Durability, Availability aur Backup: Teen Alag Cheezein
**[VISUAL: A box being copied automatically into three towers (AZs) of one city. Three labels beneath: "Durability: box does not get lost", "Availability: warehouse door open right now", "Backup: someone can bring back what I deleted". Only the first is lit for plain S3 Standard.]**

**(Voiceover):**
S3 ke baare mein ek line sunoge: "gyarah nau ki durability." Matlab landlord aapke box ki copy ek city ke kai towers mein rakhta hai, aur box ke kho jaane ka khatra bahut hi kam hai. Teen alag baatein: Durability: box khoya nahi. Availability: godown ka darwaza abhi khula hai ya nahi. Backup: agar aapne galti se box phenk diya, to kya wapas milega. S3 Standard pehli baat ka vaada karta hai. Teesri baat aapko khud banani padti hai, versioning se, jo hum agle episode mein dekhenge. Ek aur rule: aapka data usi region mein rehta hai jo aapne chuna, jab tak aap khud use kahin aur na bhejo. Aur ab S3 mein naya box likhte hi turant padha ja sakta hai.

### [09:30 – 11:30] Scene 5: Teen Tarah ka Kharcha
**[VISUAL: A bill with three lines: "Storage: boxes sitting in the godown, per GB per month", "Requests: every put and get, per thousand", "Data out: boxes leaving the godown to the internet, per GB". Data coming in is marked free, and a small arrow shows traffic to a building in the same region as cheap.]**

**(Voiceover):**
S3 ka bill teen hisson mein aata hai. Ek, storage: kitne box kitne din rakhe. Do, requests: har daalna aur har padhna, jiska rate bahut kam hai par lakhon baar mein ginti ban jaata hai. Teen, data out: box godown se bahar internet par jaaye to uska paisa. Box andar daalna aam taur par free hai. Isi wajah se bada bill aksar teesre hisse se aata hai, jab koi bada video lakhon bar download hota hai. Isiliye brochure aur photos ke liye aage CloudFront aayega. Rates aur free tier badalte rehte hain, to live pricing page dekhna.

### [11:30 – 14:25] Scene 6: Lab: Pehla Warehouse
**[VISUAL: Console: Create bucket, unique name, region matching the lab building, Block Public Access ON. Terminal: `echo "room 101" > front.txt`, `aws s3 cp front.txt s3://YOUR-BUCKET/rooms/101/front.txt`, `aws s3 ls s3://YOUR-BUCKET/ --recursive`, `aws s3 sync ./photos s3://YOUR-BUCKET/rooms/ `. Then the object URL opened in a browser: "AccessDenied".]**

**(Voiceover):**
Lab. Console mein ek bucket banao. Naam unique rakho, jaise `atithi-photos-` ke baad apna naam aur ek number. Region wahi jo aapki lab buildings ka hai. Block Public Access on rehne do. Terminal mein `echo "room 101" > front.txt`, phir `aws s3 cp front.txt s3://YOUR-BUCKET/rooms/101/front.txt`, aur `aws s3 ls s3://YOUR-BUCKET/ --recursive` se check karo. Ab ek folder ki kuch photos banao aur `aws s3 sync ./photos s3://YOUR-BUCKET/rooms/` chalao. Sync sirf wo cheezein bhejta hai jo naye ya badli hui hain. Ek box ki jankari, bina use utaare, `aws s3api head-object --bucket YOUR-BUCKET --key rooms/101/front.txt` se dekho: `aws s3` roz ka aasaan aujaar hai, aur `s3api` S3 ki har call seedhi chalata hai. Aakhir mein console se ek object ka URL browser mein kholo. AccessDenied aayega, aur wahi sahi hai: S3 ka default jawab "nahi" hai, aur hum use jaan boojh kar badalenge.

### [14:25 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "bucket = unique name · object = file + info · key = label, not folder · put whole box · durability ≠ availability ≠ backup · bill = storage + requests + data out".]**

**(Voiceover):**
Recap: bucket, object aur key. Box poora daalte hain, poora nikalte hain. Aur durability ka matlab backup nahi hota. Ab ek sawaal: teen saal purane boxes, jinhe kisi ne nahi khola, kya wo bhi utna hi mehnga paisa lete rehenge? Agle episode mein godown ki alag alag manzilein.

---

# 📺 EPISODE 2: Storage Classes, Lifecycle aur Versioning

### [00:00 – 02:10] Scene 1: Teen Saal Purane Boxes ka Bill
**[VISUAL: A bill bar growing every month because three years of logs and invoices sit in the front rows of the warehouse. A hand moves old boxes to the back godown, and the bar drops.]**

**(Voiceover):**
Atithi ke godown mein teen saal ki invoices aur logs pade hain. Kisi ko unki zaroorat saal mein ek baar padti hai, jab hisaab ka audit aata hai. Phir bhi wo godown ke us hisse mein hain jo roz ke boxes ke liye bana hai, aur wahi rate de rahe hain. S3 mein godown ki kai manzilein hain. Jitni kam zaroorat, utni sasti manzil, par wapas laane mein utna zyada samay ya kharcha. Samajhna sirf itna hai ki kaun sa box kis manzil par jaana chahiye, aur ye hamesha haath se nahi, nuskhe se hota hai.

### [02:10 – 04:45] Scene 2: Godown ki Manzilein
**[VISUAL: A ladder. Top rung "Standard: front row, roz ka kaam". Then "Standard-IA: kabhi kabhi", "One Zone-IA: ek hi tower mein, sasta", "Glacier Instant Retrieval: saal mein ek baar, turant", "Glacier Flexible Retrieval: minutes to hours", "Glacier Deep Archive: aakhri godown". An arrow shows storage price going down, retrieval effort going up.]**

**(Voiceover):**
Standard roz ke boxes ke liye hai. Standard-IA matlab infrequent access: rakhna sasta, par har baar nikalne par fee. One Zone-IA wahi hai par sirf ek tower mein, aur bhi sasta, isliye ek tower ke girne par data ka khatra rehta hai. Glacier family archive ke liye hai. Instant Retrieval mein box millisecond mein mil jaata hai, Flexible Retrieval mein minute se ghante lagte hain, aur Deep Archive sabse sasta aur sabse dheema hai. Ye sab ek hi warehouse ke andar hota hai: box ka label wahi rehta hai, sirf manzil badalti hai. Sidha rule: jitni kam zaroorat, utna thanda aur sasta, par har manzil par wapas laane ki shart yaad rakho.

### [04:45 – 07:15] Scene 3: Intelligent-Tiering aur Chhupe Kharche
**[VISUAL: A box moving itself up and down the ladder by an unseen hand labelled "Intelligent-Tiering", with a small monitoring fee tag. Beside it three warning tags on the cold classes: "minimum storage days", "retrieval fee", "tiny files cost extra".]**

**(Voiceover):**
Agar aapko pata hi nahi ki kaun sa box kitna khulega, to Intelligent-Tiering hai. Landlord khud dekhta rehta hai ki box kab khola gaya, aur use upar ya neeche karta rehta hai, bina retrieval fee ke, bas ek chhoti monitoring fee ke saath. Thande classes mein teen chhupe kharche yaad rakho. Ek, minimum storage days: agar box ko jaldi hata diya, to bhi un dinon ka paisa lagta hai. Do, retrieval fee: box nikaalne par alag kharcha. Teen, bahut chhote boxes: unke liye minimum size ka hisaab hota hai, isliye lakhon chhoti files ko thande class mein bhejna kabhi kabhi mehnga padta hai. Exact numbers pricing page par dekho.

### [07:15 – 09:45] Scene 4: Lifecycle: Boxes ka Apne Aap Safar
**[VISUAL: A timeline for prefix `invoices/`: Day 0 Standard → Day 30 Standard-IA → Day 90 Glacier Flexible Retrieval → Day 365 expire. A second rule: `tmp/` expires in 7 days. A third: "abort incomplete multipart uploads after 7 days".]**

**(Voiceover):**
Lifecycle rule ek likha hua nuskha hai, jo godown ka supervisor roz chalata hai. Aap ek prefix ya tag chunte ho, aur likhte ho: tees din baad Standard-IA mein, nabbe din baad Glacier mein, ek saal baad delete. Alag alag prefix ke alag nuskhe ho sakte hain: `invoices/` ke liye lamba, `tmp/` ke liye sirf saat din. Ek chhoti magar zaroori rule aur hai: adhoore multipart uploads ko kuch din baad hata do, kyunki wo dikhte nahi par paisa lete hain. Aur ek dhyaan: lifecycle sirf aage badhne wali manzilein jaanta hai, upar wapas nahi aata. Sasti manzil se wapas laana ho, to box ko restore karke naya copy banao.

### [09:45 – 12:25] Scene 5: Versioning: Undo ka Button
**[VISUAL: A versioning stack for `note.txt`: v3 current, v2, v1. A normal delete adds a "delete marker" on top and the box vanishes from the normal view. Removing the marker brings v3 back. A deletion of a specific version id permanently removes that version, shown in red.]**

**(Voiceover):**
Versioning godown ka undo button hai. Bucket par on karo, to har overwrite ek naya version banata hai, aur purana version bhi rakha jaata hai. Ab agar koi box delete kare, to wo sach mein nahi hatta. Uske upar sirf ek delete marker lag jaata hai, jiski wajah se box saamne ki list mein gayab dikhta hai. Marker hata do to box wapas. Par yaad rakho: agar koi version ID ke saath delete kare, to wo version hamesha ke liye jaata hai. Isiliye versioning ke saath MFA delete jaisi extra suraksha ya IAM ki sakht ijaazat rakhte hain. Aur ek kharcha: har purana version paisa leta hai, isliye lifecycle mein purane versions ki meyaad bhi likho.

### [12:25 – 14:55] Scene 6: Lab: Undo aur Nuskha
**[VISUAL: Console: enable versioning. Terminal: `echo v1 > note.txt`, `aws s3 cp note.txt s3://BUCKET/`, `echo v2 > note.txt`, `aws s3 cp note.txt s3://BUCKET/`, `aws s3api list-object-versions --bucket BUCKET --prefix note.txt`, `aws s3 rm s3://BUCKET/note.txt`, then removing the delete marker with `aws s3api delete-object --version-id`. Then Management tab: lifecycle rule.]**

**(Voiceover):**
Lab. Bucket par versioning on karo. `note.txt` mein v1 likho aur upload karo, phir v2 likho aur dobara upload karo. `aws s3api list-object-versions --bucket YOUR-BUCKET --prefix note.txt` do versions dikhayega, alag version ID ke saath. Ab `aws s3 rm s3://YOUR-BUCKET/note.txt` chalao. Normal list mein file gayab, par list-object-versions mein ek delete marker. Marker ki version ID ko `aws s3api delete-object --bucket YOUR-BUCKET --key note.txt --version-id MARKER-ID` se hatao, aur file wapas aa jaayegi. Aakhir mein Management tab mein ek lifecycle rule likho: tees din baad Standard-IA, aur purane versions saath din baad expire. Safai ke waqt dhyaan: versioning on ho to bucket khaali karne mein saare versions bhi hatane padte hain.

### [14:55 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "class by how often you open · lifecycle = written recipe, by prefix · versioning = undo, delete marker · expire old versions too".]**

**(Voiceover):**
Recap: classes, lifecycle aur versioning. Ab sabse badi galti jo godown mein hoti hai: darwaza galti se sab ke liye khul jaana. Agle episode mein.

---

# 📺 EPISODE 3: Access Control

### [00:00 – 02:00] Scene 1: Kisi Ne Hack Nahi Kiya
**[VISUAL: A news-style headline: "Customer records found in an open storage bucket". A warehouse with the door open and a wrongly ticked checkbox glowing. A tiny caption: "no hacker was involved".]**

**(Voiceover):**
Kai bade data leaks mein koi hacker tha hi nahi. Kisi ne ek bucket ko public kar diya, ek galat checkbox se, aur poori duniya ne andar jhaanka. Ye wahi shared responsibility model hai jo humne Session 8 mein padha: godown ka dhancha landlord ka hai, par darwaze par kaun kis shart par andar aa sakta hai, ye faisla aapka hai. Aaj hum dekhenge ki S3 mein kaun andar jaa sakta hai, ye kaise tay hota hai, aur is galti ko rokne wali sabse upar ki chaabi kya hai.

### [02:00 – 04:30] Scene 2: Teen Chaabiyan, Ek Safety Switch
**[VISUAL: A stack. Top: a big red "Block Public Access" lever (account level and bucket level). Below: "Permission letter on the person (IAM policy)", "Letter pinned on the warehouse door (bucket policy)", "Old paper passes (ACLs): switched off by default". A line from each to the box.]**

**(Voiceover):**
Godown mein andar jaane ke raaste ginte hain. Sabse upar Block Public Access, ek bada safety switch, jo account par bhi lagta hai aur bucket par bhi. Isse koi galti se bhi kisi box ko public nahi bana sakta, chahe uski policy kuch bhi kahe. Uske neeche IAM policy: wo permission letter jo kisi staff ya duty badge ke saath chalta hai. Aur bucket policy: wo letter jo godown ke darwaze par khud chipka hota hai. ACL purane kaagzi passes hain. Naye buckets mein wo by default band hote hain, aur unhe band hi rehne dena behtar hai. Session 9 yaad hai? Pehli do chaabiyan wahi identity policy aur resource policy hain.

### [04:30 – 06:55] Scene 3: Faisla Kaun Karta Hai
**[VISUAL: A flow. A request arrives. Step 1: any explicit Deny? stop. Step 2: Block Public Access? Step 3: in the same account, an Allow from either the identity side or the bucket side is enough. For another account both sides must allow. A small table of two examples.]**

**(Voiceover):**
Jab koi box maangta hai, to faisla ek kram mein hota hai, aur Session 9 ka wahi order yahan bhi hai. Pehle: kahin koi saaf Deny hai? Agar hai, to baat khatam. Phir Block Public Access: kya ye request public banane jaisi hai? Phir dekha jaata hai ki Allow kahin se mila ya nahi. Apne hi account ke andar, identity policy ya bucket policy, dono mein se ek ka Allow kaafi hai. Doosre account ka koi aaye, to dono taraf se ijaazat chahiye. Isliye "Allow hai par phir bhi AccessDenied" aaye, to dekho: bucket policy ka Deny, Block Public Access, aur kya box doosre account ya KMS key se bandha hai.

### [06:55 – 09:15] Scene 4: Bucket Policy Padhna aur Likhna
**[VISUAL: JSON on screen, three short policies. 1: Deny with `"Condition": {"Bool": {"aws:SecureTransport": "false"}}`. 2: Allow `s3:GetObject` on `arn:aws:s3:::BUCKET/rooms/*` to a role ARN. 3: Deny `s3:*` unless `aws:PrincipalOrgID` matches. Arrows mark Effect, Principal, Action, Resource, Condition.]**

**(Voiceover):**
Bucket policy padhna Session 9 ke policy jaisa hai, bas ek naya hissa hai: Principal, yaani ye letter kis par laagu hai. Pehla udaharan: HTTPS ke bina aane wale har request ko Deny, condition `aws:SecureTransport` false. Doosra: sirf ek role ko `rooms/*` ke boxes padhne do, aur kuch nahi. Ye least privilege hai. Teesra: aisi baat jo sirf aapke organization ke accounts ko ijaazat de. Resource ke ARN mein dhyaan do: `arn:aws:s3:::BUCKET` pura warehouse hai, aur `arn:aws:s3:::BUCKET/*` uske andar ke boxes. Dono ki alag alag jagah zaroorat padti hai, jaise listing ke liye pehla aur box padhne ke liye doosra. Ye chhoti galti bahut baar hoti hai.

### [09:15 – 11:35] Scene 5: Tala Lagana: Encryption aur Nigrani
**[VISUAL: A box sealed with a lock. Three lock types: "Landlord's key (SSE-S3, default)", "Key you control, with audit log (SSE-KMS)", "You lock before sending (client side)". Beside it, a CCTV tag for server access logs and CloudTrail data events.]**

**(Voiceover):**
Box par tala bhi lagta hai. Aaj naye boxes by default landlord ki chaabi se, yaani SSE-S3 se, tale mein rakhe jaate hain, aapko kuch karna nahi padta. Agar aapko chaabi par apna control aur audit chahiye ki kis ne chaabi use ki, to SSE-KMS chuno. Teesra tareeka: box bhejne se pehle aap hi tala laga do. Ye sab "at rest" hai, yaani godown mein rakhne ke samay. Raaste mein, yaani in transit, HTTPS hota hai, aur use hum bucket policy se zaroori bana sakte hain. Aur nigrani: server access logs aur CloudTrail ke data events se pata chalta hai ki kis ne kaun sa box maanga.

### [11:35 – 14:00] Scene 6: Box Dikhana: Presigned URL aur Role
**[VISUAL: Two paths. Path 1: a long link with signature and expiry, valid for five minutes, then "Request has expired". Path 2: a booking building wearing a duty badge, reading `rooms/101/front.jpg` with no keys on disk. Both leave the bucket private.]**

**(Voiceover):**
Private box kisi ko dikhana ho to do tareeke hain, aur dono mein bucket private hi rehta hai. Pehla: presigned URL, ek lamba link jisme signature aur samay-seema chhupi hoti hai. `aws s3 presign s3://BUCKET/rooms/101/front.jpg --expires-in 300`, aur paanch minute baad wahi link expire. Dhyaan rakho: link usi ki ijaazat ke saath chalta hai jisne use banaya, aur agar wo ijaazat badli ya khatam hui, to link bhi band. Doosra tareeka: building ko duty badge pehna do. Session 9 ka instance profile, jisme sirf `s3:GetObject` aur `s3:PutObject` ek prefix par hon. Ab building ki parchi mein koi access key nahi hogi, aur boto3 ya CLI khud badge utha lega.

### [14:00 – 16:05] Scene 7: Lab: Private Rakho aur Phir Bhi Dikhao
**[VISUAL: Terminal: `aws s3 presign` output opened in a browser, then a "Request has expired" page. Console: Permissions tab, Block Public Access with all four boxes ticked, a bucket policy with the HTTPS-only Deny. On an EC2 building with a role, `aws s3 ls s3://BUCKET/rooms/` works without `aws configure`.]**

**(Voiceover):**
Lab. Pehle presigned URL: `aws s3 presign s3://YOUR-BUCKET/rooms/101/front.txt --expires-in 300`, link browser mein kholo, file dikhegi. Paanch minute baad dobara kholo, to "Request has expired". Phir bucket ki Permissions tab mein dekho ki Block Public Access ke chaaron options on hain. Ab HTTPS-only wala Deny statement bucket policy mein jodo, aur `curl http://` se box ka URL maango: ab bhi jawab nahi milega. Aakhir mein Session 9 ka ek role banao jisme sirf `rooms/*` par `s3:GetObject` ho, use ek EC2 building par lagao, aur building ke andar `aws s3 ls s3://YOUR-BUCKET/rooms/` chalao, bina `aws configure` ke.

### [16:05 – 16:40] Scene 8: Recap aur Bridge
**[VISUAL: A card: "Block Public Access ON · Deny wins · same account: one Allow is enough · /* vs bucket ARN · SSE-S3 default · presigned or role, never public".]**

**(Voiceover):**
Recap: Block Public Access sabse upar, phir policies, tale aur nigrani, aur dikhane ke do surakshit tareeke. Ab ek mazedaar upyog: ek poori website bina kisi building ke.

---

# 📺 EPISODE 4: Display Window aur Brochure Stand

### [00:00 – 02:05] Scene 1: Bina Staff ki Website
**[VISUAL: Atithi's brochure page with a hero photo, a rooms list and a "Book now" button, built from `index.html`, `style.css`, `app.js`. No building in the picture, just the warehouse with a glass display window facing the road.]**

**(Voiceover):**
Atithi ka brochure page sirf HTML, CSS aur JavaScript hai: kamre ki photos, rate ki list, aur ek "Book now" button jo booking site par le jaata hai. Is page ko chalane ke liye building ki zaroorat nahi, kyunki isme koi guest ka data nahi badalta, aur koi staff kaam nahi karta. Landlord ke godown mein ek display window hai: boxes ko is tarah rakho ki raaste se guest unhe dekh sakein, bina andar aaye. Landing page, portfolio, documentation, sab ke liye ye sasta aur sahi hai. Par ye window bina kisi suraksha ke khulti hai, aur yahan se kahani mod leti hai.

### [02:05 – 04:00] Scene 2: S3 Static Hosting aur uski Seema
**[VISUAL: Console: Properties → Static website hosting → index document `index.html`, error document `error.html`. The generated endpoint `http://BUCKET.s3-website-REGION.amazonaws.com`. Beside it, two red marks: "HTTP only" and "bucket must be public".]**

**(Voiceover):**
Bucket par static website hosting on karo, aur do naam batao: index document, jo `index.html` hai, aur error document. Landlord ek website endpoint deta hai. Is raaste mein do kamzoriyan hain. Ek, ye endpoint sirf HTTP deta hai, HTTPS nahi, to guest ka browser "not secure" dikhayega. Do, ise chalane ke liye bucket ke box public padhne ke liye kholne padte hain, matlab Block Public Access band karna padta hai. Pichhle episode ke baad ye khatarnak lagna chahiye. Isliye aaj ka sahi tareeka ye hai: bucket private rakho, aur uske saamne ek brochure stand lagao.

### [04:00 – 05:35] Scene 3: Brochure Stand: CloudFront
**[VISUAL: A world map. Without a stand: every guest drives to the single warehouse city. With a stand: copies of the brochure sit at stands in many cities, and guests pick up the nearest one. A line from the stand back to the warehouse marked "only on a miss".]**

**(Voiceover):**
CloudFront ek brochure stand hai. Landlord ke duniya bhar mein chhote chhote stands hain, jinhe edge location kehte hain. Aapka original warehouse origin kehlata hai. Pehli baar koi guest brochure maangta hai, to stand warehouse se copy mangata hai, aur apne paas rakh leta hai. Agle guests ko wahin se mil jaata hai: tez, paas se, aur origin par kam bojh. Isi ko cache kehte hain. Stand HTTPS bhi deta hai, aur aapka apna domain naam bhi.

### [05:35 – 07:35] Scene 4: Stand aur Godown ke Beech ka Pass: OAC
**[VISUAL: A private warehouse with a bucket policy that allows only the principal `cloudfront.amazonaws.com` when the request comes from distribution `d-xxxx`. A guest tries the warehouse's direct URL and gets AccessDenied, but the stand's URL works.]**

**(Voiceover):**
Ab sawaal: bucket private hai, to stand box kaise padhe? Isliye Origin Access Control, OAC. Stand ko ek khaas pass milta hai, aur bucket policy kehti hai: "sirf CloudFront, aur sirf ye distribution, mere boxes padh sakta hai." Console aapko ye policy ka text khud deta hai, aur aapko use bucket par lagana hota hai. Ab guest seedha godown ka URL maange to AccessDenied, aur stand ka URL maange to brochure dikhta hai. Aur ek chhota jaal: console ya CLI se "S3 bucket" ko origin banana hai, "static website endpoint" ko nahi, jab OAC use kar rahe ho.

### [07:35 – 09:30] Scene 5: HTTPS aur Apna Naam
**[VISUAL: Left, a padlock icon with "ACM certificate" and a label "region: us-east-1 for CloudFront". Middle, an alternate domain name `brochure.atithi.example` attached to the distribution. Right, a DNS box with an alias record pointing to `dxxxx.cloudfront.net`.]**

**(Voiceover):**
Stand ko apna naam aur sealed envelope, yaani HTTPS, dena ho to teen kaam hote hain. Ek, AWS Certificate Manager mein ek certificate, aur CloudFront ke liye wo certificate hamesha us-east-1 region mein banta hai. Do, distribution mein alternate domain name likho, jaise `brochure.atithi.example`. Teen, DNS mein us naam ko stand ke `dxxxx.cloudfront.net` par point karo. Route 53 mein ise alias record kehte hain, kisi aur DNS mein CNAME. Domain khareedna zaroori nahi hai: bina domain ke bhi `dxxxx.cloudfront.net` par HTTPS chalta hai, aur lab ke liye wahi kaafi hai. Domain wali baat optional hai.

### [09:30 – 11:55] Scene 6: Purani Copy aur Achanak 403
**[VISUAL: A guest's browser shows yesterday's brochure while the warehouse has today's. A clock with "TTL". Beside it, a terminal: `aws cloudfront create-invalidation --distribution-id ID --paths "/*"`. A second panel: a missing file gives a 403 page instead of 404, with a note "no list permission".]**

**(Voiceover):**
Stand par kuch cheezein sabko pareshan karti hain. Pehli: aapne warehouse mein naya brochure rakha, par guest ko kal wala dikh raha hai. Wajah cache hai: stand purani copy tab tak deta hai jab tak uski meyaad, TTL, khatam na ho. Do upaay hain. Ek, invalidation: `aws cloudfront create-invalidation --distribution-id ID --paths "/*"`, jo stand ko purani copy phenkne ko kehta hai. Doosra aur behtar: file ke naam mein version rakho, jaise `app.3f2a.js`, taaki naya naam naya box ho. Dusri pareshani: koi box maango jo hai hi nahi, aur 404 ki jagah 403 aaye. Private bucket par jab stand ko list karne ki ijaazat nahi hoti, to landlord "nahi mila" aur "ijaazat nahi" mein farq nahi batata.

### [11:55 – 15:05] Scene 7: Lab: Brochure Deploy
**[VISUAL: A simple `index.html` with the hotel name and one photo. Terminal: `aws s3 sync . s3://YOUR-BUCKET/site/ --delete`. Console: Create distribution, origin = bucket, OAC created, default root object `index.html`, Block Public Access still ON, bucket policy pasted. The page opens at `https://dxxxx.cloudfront.net`.]**

**(Voiceover):**
Lab. Ek `index.html` banao: Atithi ka naam, ek photo, aur ek line. `aws s3 sync . s3://YOUR-BUCKET/site/ --delete` se upload karo. `--delete` ka matlab: jo box local folder mein nahi hai, use godown se bhi hata do, chahe aapne use kisi aur tareeke se hi kyun na daala ho. Humne yahi dekha: ek alag se daala hua box chala gaya. Pehle `--dryrun` lagao, wo batata hai kya hatega. Ab CloudFront mein distribution banao: origin aapka bucket, `/site` origin path, OAC chuno, default root object `index.html`, aur Block Public Access on hi rehne do. Console ek bucket policy ka text dega, use bucket ki Permissions tab mein paste karo. Distribution deploy hone mein kuch minute lagte hain. Phir `https://dxxxx.cloudfront.net` kholo. Ek line badlo, sync karo, aur dekho ki purani copy kitni der dikhti hai, phir invalidation chalao. Safai: distribution ko pehle disable karo aur phir delete karo, bucket ko khaali karke delete karo.

### [15:05 – 16:40] Scene 8: Recap aur Bridge
**[VISUAL: A card: "private bucket + CloudFront + OAC · HTTPS from ACM (us-east-1) · TTL, invalidate or version names · 403 on a missing key · clean up". Then a thick ledger book with ruled columns fades in over the warehouse.]**

**(Voiceover):**
Recap: godown ka poora safar, aur ek surakshit, tez, bina building ki website. Ab Atithi ke paas photos aur brochure ka ghar hai. Par booking ki jankari: kaun kaun se kamre kis guest ke naam, kitne din ke liye, ye photos ki tarah box mein nahi rakhi jaa sakti. Isko ek ruled ledger chahiye, jahan do log ek hi kamra do baar book na kar saken. Agle session mein landlord ka chalaya hua records office: RDS.

---

# 📎 Student handout: Session 12 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Bucket, object, key | Unique naam; file + info; label (slash folder nahi, prefix hai) |
| Limits | Ek baar mein 5 GB tak, multipart se bade; object 5 TB tak |
| Teen alag baatein | Durability (kho nahi) ≠ availability (khula hai) ≠ backup (undo) |
| Bill | Storage + requests + data out |
| Classes | Standard, Standard-IA, One Zone-IA, Intelligent-Tiering, Glacier IR / FR / Deep Archive |
| Chhupe kharche | Minimum storage days, retrieval fee, bahut chhoti files |
| Lifecycle | Prefix ya tag ke hisaab se transition aur expire; adhoore multipart hatao |
| Versioning | Overwrite = naya version; delete = delete marker; version ID delete = hamesha ke liye |
| Block Public Access | Sabse upar ka safety switch, account aur bucket dono par |
| Faisla | Deny jeetta hai; apne account mein ek Allow kaafi; doosre account ko dono taraf se |
| ARN | `arn:aws:s3:::BUCKET` aur `arn:aws:s3:::BUCKET/*` alag cheezein |
| Encryption | SSE-S3 default; SSE-KMS control ke liye; HTTPS bucket policy se zaroori |
| Dikhana | Presigned URL (expiry) ya role (duty badge), kabhi public nahi |
| Static site | S3 endpoint HTTP only; private bucket + CloudFront + OAC |
| HTTPS | ACM certificate, CloudFront ke liye us-east-1 |
| Cache | TTL, invalidation, versioned file names |
| Safai | Distribution disable → delete; bucket ke saare versions hatao → delete |
