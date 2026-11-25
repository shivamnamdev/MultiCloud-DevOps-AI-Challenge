# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-12_aws-s3

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,997 · **Episodes:** 4

---

# EPISODE 1: Anant Godown

## Building ka Storeroom Bhar Gaya

Atithi ki booking site chal padi hai, aur ab har room ki das das photos, har booking ki PDF invoice, aur har raat ka database backup aa raha hai. Session 10 mein humne buildings ke storeroom, yaani EBS, dekhe the. Wo ek building se juda hota hai, aur uski jagah tay hoti hai. Landlord ke paas iska ek aur jawab hai: campus ke bahar ek anant godown. Ismein aap kisi bhi cheez ko ek label ke saath rakh dete ho, aur kahin se bhi wapas maang lete ho. Is godown ka naam Simple Storage Service hai, yaani S3.

## Warehouse, Box aur Label

S3 mein teen shabd yaad rakho. Bucket matlab warehouse, jiska naam poori duniya mein sirf ek ka ho sakta hai, kyunki naam address ka hissa banta hai. Object matlab box: aapki file aur uske saath kuch jankari, jaise uska type aur kab bana. Aur key matlab box ka label, jaise rooms/101/front.jpg. Dhyaan do: ye slash asli folder nahi hain. Pura rooms/101/front.jpg ek hi naam hai, aur rooms/101/ sirf us naam ka shuruaati hissa, jise prefix kehte hain. Console aapko folders dikhata hai, kyunki wo prefix ke hisaab se dikhata hai, par godown mein koi almari nahi hoti, sirf label wale box hote hain.

## File System Nahi, Box Store

S3 aur Linux ke disk mein ek bada fark hai. Disk par aap file kholte ho, beech ki ek line badalte ho, aur save karte ho. S3 mein aisa nahi hota. Aap poora box daalte ho, ya poora box nikalte ho. Badalna ho, to naya box wahi label lagakar rakh do, jo purane ko badal deta hai. Ek box paanch terabyte tak bada ho sakta hai, par ek hi baar mein daalne ki seema paanch gigabyte hai. Isliye bade box tukdon mein bheje jaate hain, jise multipart upload kehte hain, aur AWS CLI ye khud kar leta hai. Isi wajah se S3 par database ya wo files nahi rakhte jo har second badalti hain. Wahan EBS sahi hai. S3 un cheezon ke liye hai jo ek baar likhi jaati hain aur baar baar padhi jaati hain.

## Durability, Availability aur Backup: Teen Alag Cheezein

S3 ke baare mein ek line sunoge: "gyarah nau ki durability." Matlab landlord aapke box ki copy ek city ke kai towers mein rakhta hai, aur box ke kho jaane ka khatra bahut hi kam hai. Teen alag baatein: Durability: box khoya nahi. Availability: godown ka darwaza abhi khula hai ya nahi. Backup: agar aapne galti se box phenk diya, to kya wapas milega. S3 Standard pehli baat ka vaada karta hai. Teesri baat aapko khud banani padti hai, versioning se, jo hum agle episode mein dekhenge. Ek aur rule: aapka data usi region mein rehta hai jo aapne chuna, jab tak aap khud use kahin aur na bhejo. Aur ab S3 mein naya box likhte hi turant padha ja sakta hai.

## Teen Tarah ka Kharcha

S3 ka bill teen hisson mein aata hai. Ek, storage: kitne box kitne din rakhe. Do, requests: har daalna aur har padhna, jiska rate bahut kam hai par lakhon baar mein ginti ban jaata hai. Teen, data out: box godown se bahar internet par jaaye to uska paisa. Box andar daalna aam taur par free hai. Isi wajah se bada bill aksar teesre hisse se aata hai, jab koi bada video lakhon bar download hota hai. Isiliye brochure aur photos ke liye aage CloudFront aayega. Rates aur free tier badalte rehte hain, to live pricing page dekhna.

## Lab: Pehla Warehouse

Lab. Console mein ek bucket banao. Naam unique rakho, jaise atithi-photos- ke baad apna naam aur ek number. Region wahi jo aapki lab buildings ka hai. Block Public Access on rehne do. Terminal mein echo "room 101" > front.txt, phir aws s3 cp front.txt s3://YOUR-BUCKET/rooms/101/front.txt, aur aws s3 ls s3://YOUR-BUCKET/ --recursive se check karo. Ab ek folder ki kuch photos banao aur aws s3 sync ./photos s3://YOUR-BUCKET/rooms/ chalao. Sync sirf wo cheezein bhejta hai jo naye ya badli hui hain. Ek box ki jankari, bina use utaare, aws s3api head-object --bucket YOUR-BUCKET --key rooms/101/front.txt se dekho: aws s3 roz ka aasaan aujaar hai, aur s3api S3 ki har call seedhi chalata hai. Aakhir mein console se ek object ka URL browser mein kholo. AccessDenied aayega, aur wahi sahi hai: S3 ka default jawab "nahi" hai, aur hum use jaan boojh kar badalenge.

## Recap aur Bridge

Recap: bucket, object aur key. Box poora daalte hain, poora nikalte hain. Aur durability ka matlab backup nahi hota. Ab ek sawaal: teen saal purane boxes, jinhe kisi ne nahi khola, kya wo bhi utna hi mehnga paisa lete rehenge? Agle episode mein godown ki alag alag manzilein.

---

# EPISODE 2: Storage Classes, Lifecycle aur Versioning

## Teen Saal Purane Boxes ka Bill

Atithi ke godown mein teen saal ki invoices aur logs pade hain. Kisi ko unki zaroorat saal mein ek baar padti hai, jab hisaab ka audit aata hai. Phir bhi wo godown ke us hisse mein hain jo roz ke boxes ke liye bana hai, aur wahi rate de rahe hain. S3 mein godown ki kai manzilein hain. Jitni kam zaroorat, utni sasti manzil, par wapas laane mein utna zyada samay ya kharcha. Samajhna sirf itna hai ki kaun sa box kis manzil par jaana chahiye, aur ye hamesha haath se nahi, nuskhe se hota hai.

## Godown ki Manzilein

Standard roz ke boxes ke liye hai. Standard-IA matlab infrequent access: rakhna sasta, par har baar nikalne par fee. One Zone-IA wahi hai par sirf ek tower mein, aur bhi sasta, isliye ek tower ke girne par data ka khatra rehta hai. Glacier family archive ke liye hai. Instant Retrieval mein box millisecond mein mil jaata hai, Flexible Retrieval mein minute se ghante lagte hain, aur Deep Archive sabse sasta aur sabse dheema hai. Ye sab ek hi warehouse ke andar hota hai: box ka label wahi rehta hai, sirf manzil badalti hai. Sidha rule: jitni kam zaroorat, utna thanda aur sasta, par har manzil par wapas laane ki shart yaad rakho.

## Intelligent-Tiering aur Chhupe Kharche

Agar aapko pata hi nahi ki kaun sa box kitna khulega, to Intelligent-Tiering hai. Landlord khud dekhta rehta hai ki box kab khola gaya, aur use upar ya neeche karta rehta hai, bina retrieval fee ke, bas ek chhoti monitoring fee ke saath. Thande classes mein teen chhupe kharche yaad rakho. Ek, minimum storage days: agar box ko jaldi hata diya, to bhi un dinon ka paisa lagta hai. Do, retrieval fee: box nikaalne par alag kharcha. Teen, bahut chhote boxes: unke liye minimum size ka hisaab hota hai, isliye lakhon chhoti files ko thande class mein bhejna kabhi kabhi mehnga padta hai. Exact numbers pricing page par dekho.

## Lifecycle: Boxes ka Apne Aap Safar

Lifecycle rule ek likha hua nuskha hai, jo godown ka supervisor roz chalata hai. Aap ek prefix ya tag chunte ho, aur likhte ho: tees din baad Standard-IA mein, nabbe din baad Glacier mein, ek saal baad delete. Alag alag prefix ke alag nuskhe ho sakte hain: invoices/ ke liye lamba, tmp/ ke liye sirf saat din. Ek chhoti magar zaroori rule aur hai: adhoore multipart uploads ko kuch din baad hata do, kyunki wo dikhte nahi par paisa lete hain. Aur ek dhyaan: lifecycle sirf aage badhne wali manzilein jaanta hai, upar wapas nahi aata. Sasti manzil se wapas laana ho, to box ko restore karke naya copy banao.

## Versioning: Undo ka Button

Versioning godown ka undo button hai. Bucket par on karo, to har overwrite ek naya version banata hai, aur purana version bhi rakha jaata hai. Ab agar koi box delete kare, to wo sach mein nahi hatta. Uske upar sirf ek delete marker lag jaata hai, jiski wajah se box saamne ki list mein gayab dikhta hai. Marker hata do to box wapas. Par yaad rakho: agar koi version ID ke saath delete kare, to wo version hamesha ke liye jaata hai. Isiliye versioning ke saath MFA delete jaisi extra suraksha ya IAM ki sakht ijaazat rakhte hain. Aur ek kharcha: har purana version paisa leta hai, isliye lifecycle mein purane versions ki meyaad bhi likho.

## Lab: Undo aur Nuskha

Lab. Bucket par versioning on karo. note.txt mein v1 likho aur upload karo, phir v2 likho aur dobara upload karo. aws s3api list-object-versions --bucket YOUR-BUCKET --prefix note.txt do versions dikhayega, alag version ID ke saath. Ab aws s3 rm s3://YOUR-BUCKET/note.txt chalao. Normal list mein file gayab, par list-object-versions mein ek delete marker. Marker ki version ID ko aws s3api delete-object --bucket YOUR-BUCKET --key note.txt --version-id MARKER-ID se hatao, aur file wapas aa jaayegi. Aakhir mein Management tab mein ek lifecycle rule likho: tees din baad Standard-IA, aur purane versions saath din baad expire. Safai ke waqt dhyaan: versioning on ho to bucket khaali karne mein saare versions bhi hatane padte hain.

## Recap aur Bridge

Recap: classes, lifecycle aur versioning. Ab sabse badi galti jo godown mein hoti hai: darwaza galti se sab ke liye khul jaana. Agle episode mein.

---

# EPISODE 3: Access Control

## Kisi Ne Hack Nahi Kiya

Kai bade data leaks mein koi hacker tha hi nahi. Kisi ne ek bucket ko public kar diya, ek galat checkbox se, aur poori duniya ne andar jhaanka. Ye wahi shared responsibility model hai jo humne Session 8 mein padha: godown ka dhancha landlord ka hai, par darwaze par kaun kis shart par andar aa sakta hai, ye faisla aapka hai. Aaj hum dekhenge ki S3 mein kaun andar jaa sakta hai, ye kaise tay hota hai, aur is galti ko rokne wali sabse upar ki chaabi kya hai.

## Teen Chaabiyan, Ek Safety Switch

Godown mein andar jaane ke raaste ginte hain. Sabse upar Block Public Access, ek bada safety switch, jo account par bhi lagta hai aur bucket par bhi. Isse koi galti se bhi kisi box ko public nahi bana sakta, chahe uski policy kuch bhi kahe. Uske neeche IAM policy: wo permission letter jo kisi staff ya duty badge ke saath chalta hai. Aur bucket policy: wo letter jo godown ke darwaze par khud chipka hota hai. ACL purane kaagzi passes hain. Naye buckets mein wo by default band hote hain, aur unhe band hi rehne dena behtar hai. Session 9 yaad hai? Pehli do chaabiyan wahi identity policy aur resource policy hain.

## Faisla Kaun Karta Hai

Jab koi box maangta hai, to faisla ek kram mein hota hai, aur Session 9 ka wahi order yahan bhi hai. Pehle: kahin koi saaf Deny hai? Agar hai, to baat khatam. Phir Block Public Access: kya ye request public banane jaisi hai? Phir dekha jaata hai ki Allow kahin se mila ya nahi. Apne hi account ke andar, identity policy ya bucket policy, dono mein se ek ka Allow kaafi hai. Doosre account ka koi aaye, to dono taraf se ijaazat chahiye. Isliye "Allow hai par phir bhi AccessDenied" aaye, to dekho: bucket policy ka Deny, Block Public Access, aur kya box doosre account ya KMS key se bandha hai.

## Bucket Policy Padhna aur Likhna

Bucket policy padhna Session 9 ke policy jaisa hai, bas ek naya hissa hai: Principal, yaani ye letter kis par laagu hai. Pehla udaharan: HTTPS ke bina aane wale har request ko Deny, condition aws:SecureTransport false. Doosra: sirf ek role ko rooms/* ke boxes padhne do, aur kuch nahi. Ye least privilege hai. Teesra: aisi baat jo sirf aapke organization ke accounts ko ijaazat de. Resource ke ARN mein dhyaan do: arn:aws:s3:::BUCKET pura warehouse hai, aur arn:aws:s3:::BUCKET/* uske andar ke boxes. Dono ki alag alag jagah zaroorat padti hai, jaise listing ke liye pehla aur box padhne ke liye doosra. Ye chhoti galti bahut baar hoti hai.

## Tala Lagana: Encryption aur Nigrani

Box par tala bhi lagta hai. Aaj naye boxes by default landlord ki chaabi se, yaani SSE-S3 se, tale mein rakhe jaate hain, aapko kuch karna nahi padta. Agar aapko chaabi par apna control aur audit chahiye ki kis ne chaabi use ki, to SSE-KMS chuno. Teesra tareeka: box bhejne se pehle aap hi tala laga do. Ye sab "at rest" hai, yaani godown mein rakhne ke samay. Raaste mein, yaani in transit, HTTPS hota hai, aur use hum bucket policy se zaroori bana sakte hain. Aur nigrani: server access logs aur CloudTrail ke data events se pata chalta hai ki kis ne kaun sa box maanga.

## Box Dikhana: Presigned URL aur Role

Private box kisi ko dikhana ho to do tareeke hain, aur dono mein bucket private hi rehta hai. Pehla: presigned URL, ek lamba link jisme signature aur samay-seema chhupi hoti hai. aws s3 presign s3://BUCKET/rooms/101/front.jpg --expires-in 300, aur paanch minute baad wahi link expire. Dhyaan rakho: link usi ki ijaazat ke saath chalta hai jisne use banaya, aur agar wo ijaazat badli ya khatam hui, to link bhi band. Doosra tareeka: building ko duty badge pehna do. Session 9 ka instance profile, jisme sirf s3:GetObject aur s3:PutObject ek prefix par hon. Ab building ki parchi mein koi access key nahi hogi, aur boto3 ya CLI khud badge utha lega.

## Lab: Private Rakho aur Phir Bhi Dikhao

Lab. Pehle presigned URL: aws s3 presign s3://YOUR-BUCKET/rooms/101/front.txt --expires-in 300, link browser mein kholo, file dikhegi. Paanch minute baad dobara kholo, to "Request has expired". Phir bucket ki Permissions tab mein dekho ki Block Public Access ke chaaron options on hain. Ab HTTPS-only wala Deny statement bucket policy mein jodo, aur curl http:// se box ka URL maango: ab bhi jawab nahi milega. Aakhir mein Session 9 ka ek role banao jisme sirf rooms/* par s3:GetObject ho, use ek EC2 building par lagao, aur building ke andar aws s3 ls s3://YOUR-BUCKET/rooms/ chalao, bina aws configure ke.

## Recap aur Bridge

Recap: Block Public Access sabse upar, phir policies, tale aur nigrani, aur dikhane ke do surakshit tareeke. Ab ek mazedaar upyog: ek poori website bina kisi building ke.

---

# EPISODE 4: Display Window aur Brochure Stand

## Bina Staff ki Website

Atithi ka brochure page sirf HTML, CSS aur JavaScript hai: kamre ki photos, rate ki list, aur ek "Book now" button jo booking site par le jaata hai. Is page ko chalane ke liye building ki zaroorat nahi, kyunki isme koi guest ka data nahi badalta, aur koi staff kaam nahi karta. Landlord ke godown mein ek display window hai: boxes ko is tarah rakho ki raaste se guest unhe dekh sakein, bina andar aaye. Landing page, portfolio, documentation, sab ke liye ye sasta aur sahi hai. Par ye window bina kisi suraksha ke khulti hai, aur yahan se kahani mod leti hai.

## S3 Static Hosting aur uski Seema

Bucket par static website hosting on karo, aur do naam batao: index document, jo index.html hai, aur error document. Landlord ek website endpoint deta hai. Is raaste mein do kamzoriyan hain. Ek, ye endpoint sirf HTTP deta hai, HTTPS nahi, to guest ka browser "not secure" dikhayega. Do, ise chalane ke liye bucket ke box public padhne ke liye kholne padte hain, matlab Block Public Access band karna padta hai. Pichhle episode ke baad ye khatarnak lagna chahiye. Isliye aaj ka sahi tareeka ye hai: bucket private rakho, aur uske saamne ek brochure stand lagao.

## Brochure Stand: CloudFront

CloudFront ek brochure stand hai. Landlord ke duniya bhar mein chhote chhote stands hain, jinhe edge location kehte hain. Aapka original warehouse origin kehlata hai. Pehli baar koi guest brochure maangta hai, to stand warehouse se copy mangata hai, aur apne paas rakh leta hai. Agle guests ko wahin se mil jaata hai: tez, paas se, aur origin par kam bojh. Isi ko cache kehte hain. Stand HTTPS bhi deta hai, aur aapka apna domain naam bhi.

## Stand aur Godown ke Beech ka Pass: OAC

Ab sawaal: bucket private hai, to stand box kaise padhe? Isliye Origin Access Control, OAC. Stand ko ek khaas pass milta hai, aur bucket policy kehti hai: "sirf CloudFront, aur sirf ye distribution, mere boxes padh sakta hai." Console aapko ye policy ka text khud deta hai, aur aapko use bucket par lagana hota hai. Ab guest seedha godown ka URL maange to AccessDenied, aur stand ka URL maange to brochure dikhta hai. Aur ek chhota jaal: console ya CLI se "S3 bucket" ko origin banana hai, "static website endpoint" ko nahi, jab OAC use kar rahe ho.

## HTTPS aur Apna Naam

Stand ko apna naam aur sealed envelope, yaani HTTPS, dena ho to teen kaam hote hain. Ek, AWS Certificate Manager mein ek certificate, aur CloudFront ke liye wo certificate hamesha us-east-1 region mein banta hai. Do, distribution mein alternate domain name likho, jaise brochure.atithi.example. Teen, DNS mein us naam ko stand ke dxxxx.cloudfront.net par point karo. Route 53 mein ise alias record kehte hain, kisi aur DNS mein CNAME. Domain khareedna zaroori nahi hai: bina domain ke bhi dxxxx.cloudfront.net par HTTPS chalta hai, aur lab ke liye wahi kaafi hai. Domain wali baat optional hai.

## Purani Copy aur Achanak 403

Stand par kuch cheezein sabko pareshan karti hain. Pehli: aapne warehouse mein naya brochure rakha, par guest ko kal wala dikh raha hai. Wajah cache hai: stand purani copy tab tak deta hai jab tak uski meyaad, TTL, khatam na ho. Do upaay hain. Ek, invalidation: aws cloudfront create-invalidation --distribution-id ID --paths "/*", jo stand ko purani copy phenkne ko kehta hai. Doosra aur behtar: file ke naam mein version rakho, jaise app.3f2a.js, taaki naya naam naya box ho. Dusri pareshani: koi box maango jo hai hi nahi, aur 404 ki jagah 403 aaye. Private bucket par jab stand ko list karne ki ijaazat nahi hoti, to landlord "nahi mila" aur "ijaazat nahi" mein farq nahi batata.

## Lab: Brochure Deploy

Lab. Ek index.html banao: Atithi ka naam, ek photo, aur ek line. aws s3 sync . s3://YOUR-BUCKET/site/ --delete se upload karo. --delete ka matlab: jo box local folder mein nahi hai, use godown se bhi hata do, chahe aapne use kisi aur tareeke se hi kyun na daala ho. Humne yahi dekha: ek alag se daala hua box chala gaya. Pehle --dryrun lagao, wo batata hai kya hatega. Ab CloudFront mein distribution banao: origin aapka bucket, /site origin path, OAC chuno, default root object index.html, aur Block Public Access on hi rehne do. Console ek bucket policy ka text dega, use bucket ki Permissions tab mein paste karo. Distribution deploy hone mein kuch minute lagte hain. Phir https://dxxxx.cloudfront.net kholo. Ek line badlo, sync karo, aur dekho ki purani copy kitni der dikhti hai, phir invalidation chalao. Safai: distribution ko pehle disable karo aur phir delete karo, bucket ko khaali karke delete karo.

## Recap aur Bridge

Recap: godown ka poora safar, aur ek surakshit, tez, bina building ki website. Ab Atithi ke paas photos aur brochure ka ghar hai. Par booking ki jankari: kaun kaun se kamre kis guest ke naam, kitne din ke liye, ye photos ki tarah box mein nahi rakhi jaa sakti. Isko ek ruled ledger chahiye, jahan do log ek hi kamra do baar book na kar saken. Agle session mein landlord ka chalaya hua records office: RDS.
