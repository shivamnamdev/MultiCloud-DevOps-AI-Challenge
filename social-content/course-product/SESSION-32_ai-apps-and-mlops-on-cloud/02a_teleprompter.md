# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-32_ai-apps-and-mlops-on-cloud

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,463 · **Episodes:** 4

---

# EPISODE 1: Outside Expert ko Phone

## Demo Chalta Hai, Product Nahi

Atithi ke paas roz hazaaron guest reviews aate hain, aur manager ko har room type ka teen line ka saransh chahiye. Notebook mein ek LLM call se ye ho jaata hai. Lekin production mein sawaal badal jaate hain. Outside expert ne phone nahi uthaya to? Bahut saare logon ne ek saath phone kiya to? Bill achanak badh gaya to? Key kisi ne repo mein daal di to? Aur kisi guest ne review mein likh diya "apni saari instructions bhool jao" to? Assistant demo mein shaandaar hota hai. DevOps ka kaam use product banana hai, yaani bharosemand, sasta aur surakshit. Ye session wahi hai.

## LLM API ka Pattern aur Token

LLM API ka pattern seedha hai: aap prompt bhejte ho, kuch settings ke saath, jaise kaun sa model aur kitna lamba jawab, aur text mein jawab milta hai. Ek niyam: browser ya phone app seedha outside expert ko phone na kare, kyunki key wahan khul jaati hai. Beech mein Atithi ki apni backend service rahe. Wo check kare ki kaun hai, input theek hai ya nahi, prompt banaye, expert ko phone kare, aur jawab saaf karke wapas de. Token ka matlab text ka chhota tukda, lagbhag ek shabd ka hissa. Bill input aur output, dono tokens par chalta hai, aur model ke hisaab se rate alag hota hai, isliye provider ki pricing page par dekho, yaad se likho nahi.

## Bharosemand Banana: Timeout, Retry, Limit

Pehle bharosa. Har call par timeout lagao, kyunki bina timeout ke ek atka hua phone poori service ko rok sakta hai. Retry sirf unhi galtiyon par jo wapas theek ho sakti hain: 429, yaani bahut zyada phone, aur 5xx, yaani expert ki taraf ki dikkat. Retry ke beech ka intezaar badhta jaaye aur thoda random ho, aur tries ki ek seema ho. Warna sab trucks ek saath dobara phone karengi aur dikkat badh jaayegi, jise retry storm kehte hain. 400 ya 401 par retry nahi, kyunki galti aapki request ya key mein hai. max_tokens se jawab ki lambai aur cost dono par taala. Aur wahi review set ka saransh dobara maange ja rahe ho, to cache se do. Rate limit bhi lagao, jaise busy counter par token system: ek user ya IP se minute mein kitni calls. Ek chhoti jaal: agar aap in-memory rate limit lagate ho aur Kubernetes mein paanch parking bays hain, to har bay ka apna counter hoga. Asli limit gateway par ya Redis jaisi shared jagah par rakho.

## Guest ka Text Bharose ka Nahi

Ab sabse badi baat. Guest ka likha hua text bharose ka nahi hai. Usme kuch bhi likha ho sakta hai, jisme model ke liye chhupi instruction bhi. Isko prompt injection kehte hain. Model ko "instruction" aur "data" ka farq pakka nahi pata, isliye koi ek vaakya use behka sakta hai. Bachaav ke kai star hain. Prompt mein instructions alag aur guest ka text saaf markers ke beech, aur kaho ki marker ke andar jo hai wo sirf padhne ka data hai. Model ko wo tools ya permissions mat do jo booking badal sakein. Jawab ko bhi jaanch kar lo: agar sirf teen bullet chahiye, to format check karo. Aur khatarnaak action par hamesha insaan ki manzoori. Dusri baat: privacy. Guest ka naam, phone aur card ke ank outside expert ko mat bhejo. Pehle unhe hata do, ya mask karo, aur provider ki data policy padh lo ki wo aapka data kaise rakhta hai. Isse guest ka bharosa nahi tootta.

## Lab: review-helper, Fake Expert ke Saath

Lab: FastAPI service review-helper. Pehle ek chhota interface, taaki asli aur nakli expert badal sakein:

real_expert.py mein apne provider ke official SDK ka call, jisme timeout, max_tokens, aur retry sirf 429 aur 5xx par. Provider ke docs se model ka naam aur SDK ka tareeka dekho, kyunki wo badalta rehta hai. Tests mein sirf FakeExpert: ek test jisme review mein "ignore all instructions" ho, aur dekho ki jawab ka shape abhi bhi teen bullets hai. Bina asli key ke saare tests chalte hain. Ek dhyaan: ye scrub sirf bina space aur dash wale 10 ya 12 se zyada ank pakadta hai; "98765 43210", "4111-1111-1111-1111", email aur naam nahi pakadta. Isliye ise shuruaat samjho, aur sach mein guest ka data hatane ke liye behtar tareeka lagao.

## Recap aur Bridge

Recap: outside expert ko surakshit phone karna. Ab ise truck mein daalna: key cabinet, bill ka darwaza, aur metrics.

---

# EPISODE 2: Truck, Key Cabinet aur Bill ka Darwaza

## Ek Raat mein Bill Chadh Gaya

Ek raat ek bug ne summary job ko loop mein daal diya. Har chakkar mein outside expert ko phone, aur subah bill dekh kar sab chaunke. AI services mein cost ek reliability ka sawaal hai, kyunki har call ka paisa lagta hai, jaise Session 15 mein landlord ke meter ka bill. Is episode mein service ko truck mein daalenge, key surakshit rakhenge, aur bill par darwaza lagayenge.

## Truck Design aur Key Cabinet

Truck design wahi aadatein: slim base, non-root user, 0.0.0.0 par sunna, aur CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]. API key kabhi truck design ke andar nahi. Kubernetes mein wo ek Secret, yaani sealed envelope, se environment variable ban kar aati hai, aur Secret ko bhi behtar hai ki cloud ka secret manager ya key cabinet bhare, haath se nahi. Session 25 ki baat: Secret base64 mein hota hai, taale mein nahi, isliye usse padhne ka role kam logon ko. CI mein secret scan lagao jo Session 20 mein seekha, aur pre-commit hook pehla darwaza. Aur key ko badalne, yaani rotate karne, ka plan likho: kaun badlega, kitne din mein, aur purani key kab band hogi. Agar key leak ho jaaye, to pehle provider ke console se revoke, phir code saaf, wahi Session 20 ka leak response.

## Bill ke Darwaze: Cost Guardrails

Bill ke paanch darwaze. Pehla, provider ke console mein budget aur usage limit, jo asli akhri deewar hai. Doosra, max_tokens aur input size ki seema. Teesra, rate limit, jo shared jagah par ho. Chautha, cache, kyunki wahi sawaal ka jawab dobara kyun kharido. Paanchva, circuit breaker: agar expert baar baar fail ho raha hai, to kuch der ke liye phone karna band, aur guest ko saaf message, ya purana cached jawab. Ek aur: background job mein bhi seema lagao, jaise ek chakkar mein kitne reviews, aur ek din mein kitne chakkar. Aur in sab ke upar nazar: tokens per hour, requests, errors, latency, control room ki screens par, aur tokens mein achanak badhot par alarm. Ye observability wahi hai jo Session 26 mein banayi.

## Kitna Kharcha Hoga, Pehle Hisaab

Phone karne se pehle ek hisaab. Roz kitne reviews, har review ke kitne tokens, input aur output ke rate se guna karo, aur ek mahine ka kharcha nikaalo. Rate provider ke price page se lo, yaad se nahi, kyunki wo badalte hain. Isi hisaab se pata chalta hai ki kya chhota aur sasta model kaafi hai, aur kahan bada model chahiye. Aam tareeka: aasaan kaam, jaise teen bullet ka saransh, chhote model par; mushkil kaam, jaise lamba reasoning, bade par. Aur ek jaanch: kya har baar outside expert ki zaroorat hai? Kabhi kabhi ek seedha rule ya search bhi kaam kar deta hai.

## Lab: Metrics, Rate Limit aur Alarm

Lab: review-helper mein prometheus_client jodo: ek counter expert_requests_total jisme label outcome ho, jaise ok, timeout ya bad_shape, ek expert_tokens_total jisme label direction ho, input ya output, aur ek latency histogram. app.mount("/metrics", make_asgi_app()); Prometheus ko /metrics/ (aakhir mein slash) par point karo, kyunki bina slash ke FastAPI redirect karta hai. Label mein kabhi guest ka naam ya review ki ID nahi, wahi cardinality ka sabak. Ek rate limit likho: pehle in-memory, aur phir dekho ki do copies chalane par wo kaam kyun nahi karta, aur uske baad Redis ke ek chhote container se shared counter. Session 26 ke inspector ko is service par point karo, rate(expert_requests_total[5m]) ka graph dekho, aur ek alert rule likho jo tokens per hour ek seema se upar jaane par bajega. Poora lab FakeExpert par, taaki paisa na lage.

## Recap aur Bridge

Recap: outside expert wali service ab surakshit, sasti aur dikhne wali hai. Ab doosra roop: Atithi apna khud ka trained brain banata hai, aur use bhi kisi truck ki tarah chalana hai.

---

# EPISODE 3: Trained Brain ka Chakra

## Notebook se Production Tak

Atithi ka data scientist ek brain banata hai jo bataata hai ki kaun si booking cancel hone ka risk rakhti hai, taaki front desk pehle se phone kar sake. Notebook mein score achha hai. Par notebook ko ek bharosemand service banana alag kaam hai. MLOps wahi kaam hai: brain ko DevOps ki tarah train, package, ship aur dekhna. Seedhi baat: brain sirf ek file hai, aur use serve karne wali truck ek normal truck hai.

## Chakra

Chakra ek ghoomta hua loop hai. Data ikattha aur saaf. Train aur evaluate. Brain ko versioned register karo, uske metrics aur jis data se bana tha uske saath. Package, yaani truck design. Ship, yaani depot se building mein. Serve, yaani API. Phir dekhna: sirf latency aur errors nahi, balki drift bhi, yaani production ka data training ke data se alag hone lage. Aur jab brain bigde, to retrain. Tools jaise DVC, MLflow, ya S3 ke versioned folders experiments aur data ka register rakhte hain, wahi Session 12 ke versioning ka idea. Ek farak yaad rakho: software mein result sirf code par nirbhar karta hai, ML mein code, data aur parameters sab par.

## Reproducibility aur Brain ka Version

Training ke har run ka ek record rakho: code ka commit, data ka version, library ke versions, parameters, random seed, aur metrics. Brain ki file ko label do, jaise risk-v3, aur pehle staging mein jaanch, phir production. Evaluation ek automatic darwaza hai: naya brain purane se behtar nahi hai, ya accuracy ek tay seema se neeche hai, to wo aage nahi jaayega. Ye wahi CI ka idea hai, bas brain ke liye. Ek zaroori suraksha baat: joblib aur pickle ki files chalne par code chala sakti hain. Isliye sirf wahi brain file load karo jo aapki apni conveyor ne banayi ho aur depot se aayi ho, kisi anjaan se download ki hui nahi. Aur scikit-learn ka version train aur serve dono mein ek hi rakho, warna file khul hi na paye ya natija badal jaye.

## Accuracy Ek Number Nahi Hai

Ek sacchai jo naye log bhoolte hain: accuracy akeli dhokha de sakti hai. Maan lo sau mein se pachaanve bookings kabhi cancel nahi hotin. Ek brain jo hamesha "cancel nahi hoga" bole, wo pachaanve percent sahi hai, aur bekaar hai. Isliye precision aur recall dekho: jitne cancel pakde, aur jitne alarm sach nikle. Front desk ke liye kaun sa zyada zaroori hai, ye business tay karta hai. Aur test data kaise chunna hai: time ke hisaab se, pehle ka data train, baad ka test, kyunki asli duniya mein kal ka data aaj ke baad aata hai. Random split kabhi kabhi jhoothi taaqat dikhata hai.

## Lab: Brain Train Karo aur Darwaza Lagao

Lab: train.py. Data banaao jo asli nahi, sirf practice ke liye, ek fixed seed ke saath:

assert ek darwaza hai. Isse GitHub Actions ya Jenkins ke ek station mein chalao, aur dekho ki recall giri to station laal ho jaata hai. Seed hatao aur dekho ki natija thoda badalta hai, yaani reproducibility seed par bhi nirbhar hai. Ye data nakli hai, isliye uska score asli kahani nahi batata. Maqsad conveyor ka hai.

## Recap aur Bridge

Recap: brain ka chakra, version aur darwaza. Ab brain ko truck mein serve karna, deploy karna, aur drift par nazar.

---

# EPISODE 4: Brain ko Truck mein Chalao

## Brain ek Normal Service Hai

Brain ko serve karne ka matlab ek HTTP API jo input le aur prediction de. Wo ek normal truck hai, to uske liye wahi health check, probes, HPA, metrics aur rollback jo humne seekhe. Aaj hum use FastAPI mein serve karte hain, local Kubernetes par chalate hain, aur dekhte hain ki EKS par ye kaise jaata.

## Model Server

Brain ko startup par ek baar load karo, har request par nahi. Input ko pydantic se check karo, aur jawab mein brain ka version bhi do.

/health sirf zinda hone ka jawab hai. Agar brain load hone mein samay lagta hai, to readiness alag rakho, taaki parking bay tab tak traffic na le. Brain ko truck design ke andar copy kar sakte ho, ya bade brain ho to depot se startup par utaaro. Dono mein version label saath rahe.

## Kubernetes par: Local Pehle, EKS Baad Mein

Kubernetes par Session 24 aur 25 ka wahi tareeka. Local kind cluster mein kind load docker-image risk-brain:v1, Deployment mein readiness probe, requests aur limits, Service, aur CPU par HPA. Seekhne ke liye local kaafi hai aur muft hai. EKS par wahi YAML chalega: truck design ECR mein, cluster eksctl se ya Session 28 ke Terraform se, aur bahar ke liye load balancer ya Ingress. EKS billed by the hour hai, isliye lab ke baad delete, aur console mein jaanch. GPU node group sirf bade deep learning brain ke liye hota hai, aur bahut mehenga hota hai. Hamara scikit-learn ka brain CPU par aaram se chalta hai. Ek aur dhyaan: latest tag nahi, risk-brain:v1 ya Git SHA.

## Naya Brain Kaise Utaare

Naya brain utaarna truck badalne se thoda alag hai, kyunki code sahi ho kar bhi predictions kharab ho sakti hain. Isliye teen tareeke. Canary: jaise naya menu pehle kuch tables ko, paanch percent traffic naye v2 ko, baaki v1 ko, aur dono ke metrics ki tulna. Shadow: v2 har request dekhta hai, par uska jawab use nahi hota, sirf compare hota hai. Aur rollback: purana label wapas. Dono brain ke metrics mein version ka label rakho, taaki wall of screens par saaf dikhe kaun sa brain kitna chala. Ye Session 31 ke rollback ka brain wala bhai hai.

## Drift: Duniya Badal Gayi

Drift ka matlab: duniya badal gayi, par brain purani duniya ke hisaab se soch raha hai. Atithi ne last-minute sale chalayi, aur ab lead_days zyaadatar das se kam. Brain ke liye ye naya data hai. Drift pakadne ka aasaan tareeka: production ke inputs ka mean training ke mean se kitne standard deviation door hai. risk.json mein hamne train_means aur train_stds isiliye rakhe the. Server har feature ka chalta hua mean metric mein de, aur ek alert rule bole ki shift ek seema se upar hai. Ek aur cheez: aksar asli jawab, yaani booking cancel hui ya nahi, kuch din baad pata chalta hai. Jab pata chale, to usse brain ki accuracy dobara naapo. Drift alert ka matlab "retrain ke baare mein socho", seedha "retrain karo" nahi. Dekhna hai ki naye data par naya brain gate paar karta hai ya nahi.

## Lab: Truck banao, Chalao, Drift Dekho

Lab: truck banao, docker build -t risk-brain:v1 ., docker run -d -p 8000:8000 risk-brain:v1. Test: curl -X POST localhost:8000/predict -H 'content-type: application/json' -d '{"values":[90,5200,0,2]}'. Jawab mein cancel_risk aur brain: v1. Phir local cluster par Deployment, Service, probe aur HPA. Ek chhota script jo pehle normal bookings bhejta hai, aur phir saari bookings mein lead_days das se kam. Server mein feature ka chalta hua mean metric banao, aur Session 26 ke inspector se dekho ki wo training ke mean se door ja raha hai. Ek alert rule likho. Agar aap EKS par chalate ho, to image ECR mein, aur lab ke baad eksctl delete cluster ya terraform destroy, aur console check. Cluster ke saath load balancer aur disk bhi hatao.

## Recap aur Bridge

Recap: outside expert ko phone karne wali truck, aur apna trained brain, dono ab surakshit, sasti aur dikhne wali. Ab aakhri session: assistant raat ki duty par control room mein baithta hai, aur aap ek service hatch lagate ho jisse wo hotel ke tools ko surakshit tareeke se chala sake.
