# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-25_microservices-on-kubernetes

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~3,102 · **Episodes:** 4

---

# EPISODE 1: Ek Truck se Truck Park Tak

## Ek Bug, Poori Dukaan Band

Atithi ki booking site ab ek hi bade program mein hai: rooms, bookings, payments, photos, notifications. Payment ke code mein ek memory leak aaya aur poori site gir gayi, rooms ki list bhi, photos bhi. Hotel mein reservations, housekeeping, restaurant aur billing alag services hoti hain: billing counter band ho to bhi kamre bukk hote hain. Microservices ka vichar wahi hai: site ko aise todo ki ek gire to baaki chalein. Har service ek alag truck, apna design, apna standing order, apna extension number. Mil kar ye ek truck park banta hai. Par pehle ek sachchi baat: ye vichar mushkil bhi hai, aur ye episode utna hi us mushkil ke baare mein hai jitna faayde ke baare mein.

## Faayde aur Keemat

Faayde. Har service alag release hoti hai. Jo zyada busy hai use alag scale karo: shaadi ke season mein sirf bookings-service. Ek team, ek service, aur ek ki galti chhoti rehti hai. Keemat. Jo function call tha, ab network call hai: dheema, aur fail ho sakta hai. Request kai services se guzarti hai, to debugging kai jagah, aur data kai databases mein. Chalane ko bahut zyada cheezein. Isliye chhoti team ke liye pehle ek achha monolith bhi theek hai. Microservices tab lo jab team aur scale ki zaroorat ho, "kyunki sab karte hain" isliye nahi.

## Kahan Todo: Business ke Hisaab se

Kahan todein? Hotel ki tarah, business ke hisaab se: rooms (housekeeping), bookings (reservations), payments (billing), photos, notifications. Technical layers ke hisaab se nahi, jaise ek UI service, ek logic, ek database. Har service apna data khud rakhti hai, aur doosre ka database seedha nahi padhti: baat service ke raaste hoti hai. Ek ka schema badle to doosre nahi tootte.

## Atithi ka Truck Park

Is session ka project: Atithi ka truck park, atithi wing mein. web, lobby ki screen, jo guests ko page dikhata hai. rooms-service, yaani housekeeping, jo kamron ki list deta hai, aur photos Session 12 ke warehouse se. bookings-service, yaani reservations desk, jo bookings likhta hai, aur records ke liye Postgres. Har ek apna Deployment aur apna Service. Kuch trucks stateless hain, jaise web aur rooms. Ek stateful hai: records, jinhe locker room chahiye. Production mein records Session 13 ke RDS mein hote hain; seekhne ke liye hum ek chhoti Postgres truck cluster ke andar chalayenge, taaki locker room dikhe. Sabke upar concierge, yaani Ingress.

## 12-Factor ke Teen Niyam

Trucks Kubernetes par achhi tarah tab chalti hain jab teen niyam pakke hon, jinhe 12-factor soch kehte hain. Ek: config environment se aaye, design ke andar nahi. Do: logs stdout par jaayein, kisi file mein nahi, taaki kubectl logs aur logging tools unhe utha sakein. Teen: process stateless ho, yaani koi bhi truck mar kar dobara ban sake bina kuch khoye. Ab Kubernetes unka poora faayda uthata hai: ek pod hatao, dusra aa jaata hai, aur guest ko pata bhi nahi chalta.

## Lab: Services ko Pehchano

Is session ka ticket, ATITHI-025. Mrs. Mehta kehti hain: "Sale wale din bhi site chalni chahiye, aur koi booking gum nahi honi chahiye." Done when: web, rooms aur bookings ek saath chalein aur naam se ek doosre ko dhundhein, database ka data pod delete ke baad bhi rahe, ek galat service poore cluster ko na khaye, aur sirf bookings hi database tak pahunche. Lab (design ka exercise). Paanch services ke liye ek table banao: naam, port, kis par nirbhar, stateful ya nahi, aur ye gir jaaye to kya tootega. Jaise bookings-service ko Postgres chahiye aur wo stateful hai. Payments gire to bookings ko "baad mein payment" ka rasta chahiye. Phir har service par 12-factor ke teen niyam check karo.

## Recap aur Bridge

Recap: microservices ka vichar aur uski keemat. Ab asli kaam: har truck ko config, secrets aur budget dena.

---

# EPISODE 2: Notice Board, Envelope aur Budget

## Ek Design, Teen Wing

Agar dev, staging aur production ke liye alag alag design banane pade, to wo galat tareeka hai. Ek hi design, aur settings bahar se. Kubernetes mein iske liye notice board, yaani ConfigMap, aur sealed envelope, yaani Secret. Aur har truck ko ek sahi allowance ki zaroorat hai: kitna CPU aur memory. Aur har wing ko ek budget. Aaj ye sab, aur uske baad trucks aapas mein baat kaise karein.

## ConfigMap aur Secret

ConfigMap mein aam settings: APP_MODE, ya page par kitne rooms. Secret mein sensitive cheezein, jaise database password. Bahut zaroori: Secret ki value base64 mein hoti hai, jo sirf encoding hai, encryption nahi. Isliye RBAC se access seemit karo, cluster mein secrets ka encryption on rakho, aur bade systems mein cloud ka secret manager, jaise Session 13 mein Secrets Manager. Aur Secret ka YAML kabhi vault mein plain mat daalo, jaise Session 20 ke leak ki kahani.

## Config Badla, Pod ko Pata Nahi

Ek jaal: ConfigMap badal diya, par chalti truck ko wahi purani value dikhti hai. Environment variable truck ke start hote waqt padhe jaate hain, isliye un mein badlaav tab tak nahi dikhta jab tak pod dobara na bane. Mounted file ke roop mein diya ho to kuch der mein file badal jaati hai, par app ko use phir se padhna aana chahiye. Roz ka hal: kubectl rollout restart deployment/rooms, jo rolling update ki tarah pods ko ek ek karke dobara banata hai.

## Requests, Limits aur Budget

Har truck ke do aankde. Request: kam se kam kitna chahiye, aur allocation officer isi ke hisaab se building chunta hai. Limit: upar ki hadd. CPU limit paar karne par truck ko dheema kiya jaata hai, throttle. Memory limit paar karne par truck ko maar diya jaata hai, OOMKilled, exit code 137, jo hum ne Session 24 mein dekha. CPU ki ikai milli-core hai: 100m ka matlab ek core ka dasva hissa. Request na ho to HPA ko kuch pata nahi chalta, aur building ki planning bhi andhi. Isliye har truck par request zaroor likho.

## LimitRange aur ResourceQuota

Do object, jinhe log mila dete hain. ResourceQuota poori wing ka total budget hai: sab pods milakar kitna CPU, memory aur kitne pods. Notes ki misaal: ek team ko sau rupaye ka budget mila hai, poori team mil kar usse zyada kharch nahi kar sakti. LimitRange har truck ka allowance hai: default request, default limit, aur minimum aur maximum. Ek zaroori jodi: agar wing mein ResourceQuota ho jisme CPU aur memory hain, to har pod ko request aur limit deni hi padti hai, aur LimitRange unhe default de sakta hai. Quota paar hone par pod Pending nahi hota. Pod banta hi nahi: ReplicaSet ke Events mein FailedCreate... exceeded quota likha aata hai.

## Probes: Truck Taiyaar Hai?

Probes truck ki sehat ki jaanch hain. Readiness: jaise housekeeping jab tak kamra "ready" mark na kare, guest ko upar nahi bhejte; taiyaar na ho to Service us truck ko endpoints se hata deti hai. Liveness: duty manager ka round, jo jawab na de use badal do. Startup: dheere start hone wali truck ke liye. Ye Session 22 ke HEALTHCHECK aur Session 11 ke marshal ke health check ka Kubernetes roop hai. Probe halka rakho: /health jo sirf 200 de. Liveness database tak gayi aur database dheema hua, to saari trucks ek saath restart hongi. Readiness rolling update ko bhi bachata hai: Deployment purana pod tab tak nahi hatata jab tak naya taiyaar na ho.

## Service se Service ki Baat

Services ek doosre ko DNS naam se bulati hain. Same wing mein http://rooms-service:5000, alag wing se rooms-service.atithi.svc.cluster.local. Ye URL code mein hardcode nahi, ConfigMap se. Ab network par bharosa nahi: har call par timeout lagao, thoda retry karo, ruk ruk ke, aur fail ho to saaf, chhota jawab do. Laundry band ho to front desk "same-day laundry" ka wada rok deta hai, har guest ko intezaar nahi karwata: yahi timeout hai. Bina timeout ke ek dheemi service poori chain ko latka sakti hai, jise cascading failure kehte hain. Retry sirf wahi karo jo do baar chalne par bhi nuksaan na kare, yaani idempotent: do clerk ek hi booking daalein, to reservation number se doosri kuch nahi badalti, jaise Session 15 mein Lambda ke saath.

## Lab: Truck Park ko Budget ke Saath Chalao

Lab. kubectl create namespace atithi. Phir kubectl create configmap rooms-config -n atithi --from-literal=APP_MODE=demo aur ek Secret. rooms-service ke Deployment mein Session 22 ka design, envFrom se ConfigMap, resources mein request aur limit, aur readinessProbe /health par. Pehle ek LimitRange lagao, phir ek chhoti ResourceQuota, jaise pods: "4". Ek test pod se wget -qO- http://rooms-service:5000/health karo. Ab Deployment ko paanch tak scale karo: paanchva pod nahi banega. kubectl describe rs -n atithi ke Events mein FailedCreate aur "exceeded quota" padho. Phir do replicas par wapas lao: bhari quota rollout rok deti hai. Ab ConfigMap badlo, kubectl rollout restart se naya value dikhao.

## Recap aur Bridge

Recap: config, envelope, budget, probes aur service-to-service calls. Ab ek sawaal jo abhi baaki hai: records truck mar gayi to records bhi gaye?

---

# EPISODE 3: Locker Room

## Truck Mari, Records Gaye

Records truck mar gayi, aur uske saath saari bookings. Truck asthayi hai, aur Session 21 mein humne yahi dekha: volume ke bina data truck ke saath jaata hai. Par ek aur kamzori: agar volume sirf ek building ke disk par hai, to us building ke girte hi data tak pahunch nahi. Kubernetes ka jawab Persistent Volume hai: cluster ka ek central locker, jo kisi bhi building se jud sakta hai, aur jo kisi bhi pod ki zindagi se alag hai. Truck badle, locker wahi.

## PV, PVC aur StorageClass: Teen Cheezein

Teen cheezein, aur teeno ke naam alag. PersistentVolume, PV, locker khud: kitna bada, kahan, kaise. PersistentVolumeClaim, PVC, truck ki request slip: "mujhe paanch GiB chahiye, ek time par ek likhne wala." Aur StorageClass landlord ka catalogue: kaun se locker types milte hain, jaise tez SSD ya sasta HDD. Pod seedha PV se nahi judta. Pod PVC se judta hai, aur Kubernetes PVC ke liye ek PV dhoondhta hai. Agar StorageClass diya ho, to PV khud ban jaata hai, jise dynamic provisioning kehte hain. Cloud par PV asli mein ek EBS ya Persistent Disk hota hai, jo Session 10 ka storeroom hai, ab Kubernetes ke naam se.

## PV ka YAML aur Access Modes

PV ka YAML: capacity mein size, accessModes mein kaun kaise use kar sakta hai, persistentVolumeReclaimPolicy mein PVC hatne par kya ho, aur ek backend, jaise hostPath: /tmp/data, jo sirf ek building ka folder hai aur sirf seekhne ke liye. Access modes. ReadOnlyMany: bahut sare padh sakte hain. ReadWriteOnce: ek building ek time par padh aur likh sakti hai. ReadWriteMany: bahut sare ek saath padh aur likh sakte hain. Ek sudhaar: ReadWriteOnce ek pod nahi, ek node, yaani ek building par lagta hai, to ek hi building ke kai pods usse share kar sakte hain. Sirf ek pod tak rokne ke liye ReadWriteOncePod hai.

## Binding ke Niyam aur PVC

PVC ka YAML: accessModes aur resources.requests.storage, jaise 5Gi. Binding ke niyam. Access mode match hona chahiye: PV ReadWriteMany ka ho aur PVC ReadWriteOnce ka, to bind nahi hoga. Size ke liye Kubernetes kam se kam utna bada PV dhoondhta hai, kabhi chhota nahi. Agar sirf saat GiB ka PV mila, to poora PV us claim ke naam ho jaata hai, aur extra jagah bekaar rakhi rehti hai chahe pod use kare ya nahi. Ek PV sirf ek PVC se bandhta hai, par ek PVC ko kai pods use kar sakte hain, agar access mode ijaazat de. Koi PV nahi mila to PVC Pending rehta hai. Khaas PV se jodna ho to PVC ke spec mein volumeName: my-pv.

## Reclaim Policy aur Statuses

PVC hata do, to locker ka kya hoga? Reclaim policy tay karti hai. Retain: PV aur uska data bache rehte hain, aur aapko haath se saaf ya dobara use karna padta hai. Delete: PV aur peeche ka disk dono hat jaate hain. Recycle purani aur deprecated hai. Jab PVC hata, PV ka status Bound se Released ho jaata hai. PVC ke statuses: Pending, jab tak PV na mile. Bound, jab mil gaya. Lost, jab jis PV se bandha tha wo ab nahi raha. Ek zaroori baat: pod ko locker se alag karne par data nahi jaata. Data tabhi jaata hai jab policy Delete ho aur PVC hata diya jaaye. Isliye production ke data par Retain, aur backup alag.

## PVC ke Jaal aur Badhana

PVC ke kuch jaal. Pehla: PVC banne ke baad uska access mode badal nahi sakte, hatao aur nayi banao. Do: jis PVC ko koi pod use kar raha ho, use hatane par wo Terminating mein atak jaata hai, jab tak pod na hate. Teen: storageClassName ek baar set hone ke baad badalta nahi, doosri class ke liye nayi PVC banao. Locker bada karna ho to kubectl patch pvc my-pvc -p '{"spec":{"resources":{"requests":{"storage":"10Gi"}}}}'. Dhyaan: field requests hai, request nahi. Ye tabhi chalta hai jab StorageClass allowVolumeExpansion de. Kind ki default class allowVolumeExpansion nahi deti, to wahan patch Forbidden aata hai. Bada karna aasaan hai, chhota karna nahi.

## StorageClass aur StatefulSet

StorageClass landlord ka catalogue hai: locker ka type, jaise SSD ya HDD, aur kaun sa provisioner usse banayega. kubectl get storageclass mein default class par (default) likha hota hai. PVC mein class na likho to wahi mil jaati hai, aur PV khud ban jaata hai, bina kisi ke haath se banaye. Database jaisi stateful trucks ke liye StatefulSet hota hai: pods ke naam tay, pg-0, pg-1, aur har pod ka apna PVC. Par ek honest salah: asli production mein database ko Kubernetes ke andar khud chalana mushkil hai, backup, upgrade aur failover sab aapke zimme. Session 13 ka RDS aksar behtar hai. Truck park mein stateless trucks, aur records landlord ke records office mein.

## Lab: Locker aur Truck

Lab. Ek PV banao: 1Gi, ReadWriteOnce, Retain, hostPath: /tmp/data, aur storageClassName: manual. Phir ek PVC: ReadWriteOnce, 500Mi, wahi storageClassName: manual. Class likhna zaroori hai: bina class ka PVC cluster ki default class le leta hai, Pending rehta hai, aur hamara PV Available hi pada rehta hai. kubectl get pv,pvc mein dono Bound dikhne chahiye, aur dekho ki PVC ne chhota maanga par poora PV mila. Ab ek pod jisme PVC /data par mount ho. kubectl exec se echo hi > /data/a. Pod hatao, naya pod banao, aur cat /data/a: data bacha hai. Phir PVC hatao aur dekho ki PV Released ho gaya aur data abhi bhi disk par hai. Doosra part: kubectl get storageclass dekho, ek PVC bina PV ke banao, aur dekho ki PV khud ban gaya. Kind mein wo tabhi banta hai jab koi pod PVC ko use kare. kubectl describe pvc aur kubectl get events mein poori kahani. Safai: PVC, PV, aur pods.

## Recap aur Bridge

Recap: PV, PVC, StorageClass aur reclaim policy. Ab truck park ke entrance par concierge, aur production ke taale.

---

# EPISODE 4: Concierge aur Production ke Taale

## Har Service ka Alag Load Balancer?

Agar har service ke liye alag LoadBalancer banao, to har ek ka alag IP aur alag bill. Ingress ek hi concierge deta hai, jo HTTP rules se tay karta hai ki kaun si request kaun si service ko jaaye. Ek darwaza, kai kamre. Rule host aur path par chalte hain: atithi.example ka / web ko, /api/rooms rooms-service ko, /api/bookings bookings-service ko.

## Ingress aur uska Controller

Ingress sirf ek rule ka object hai. Rule ko asli mein chalane ke liye Ingress controller chahiye: Traefik jaisa koi controller, ya cloud ka apna. Ek zaroori khabar: community ka ingress-nginx March 2026 mein retire ho gaya, isliye naye kaam mein use mat chuno; Gateway API ya kisi maintained controller ki taraf jao. Controller ke bina Ingress likha rehta hai, kaam nahi karta. GKE mein built-in controller ek Google load balancer banata hai. Ingress mein ingressClassName se controller chuna jaata hai, aur TLS ke liye Secret mein certificate jodte hain, jaise Session 11 ke marshal par HTTPS.

## Pod Ek Doosre se Baat Kar Sakte Hain

By default Kubernetes mein koi bhi pod kisi bhi pod se baat kar sakta hai, kisi bhi wing mein. Agar web truck hack ho jaaye, to hamlavar seedha records tak pahunch sakta hai. NetworkPolicy ek allow-list hai: kaun kisse baat kare. Pehle default-deny lagao: wing ka sab traffic band. Phir sirf zaroori raaste kholo: postgres ke pods sirf bookings-service ke pods se port 5432 par traffic lein. Dhyaan: policy tab kaam karti hai jab cluster ka network plugin use enforce kare. Apne cluster mein check karo, kyunki kuch local clusters mein policy likhne par bhi asar nahi hota. Aur agar egress bhi deny karo, to DNS ke liye raasta kholna mat bhoolo.

## Kaun Kya Kar Sakta Hai: RBAC

NetworkPolicy bataati hai ki pods aapas mein kaun baat karein. RBAC alag hai: kaun Kubernetes API par kya kar sakta hai. Har service ko apni ServiceAccount do, yaani duty badge, aur ek Role jisme sirf zaroori ijaazat hon, jaise apni wing ke ConfigMap padhna. Role ko RoleBinding se jodo. Check karne ke liye kubectl auth can-i list secrets --as=system:serviceaccount:atithi:bookings-sa -n atithi. Jawab no hona chahiye. Aur pod ko khud bhi kasna: non-root user, read-only filesystem, aur kam capabilities, jaise Session 22 mein docker run ke flags the, bas ab pod ke YAML ke securityContext mein.

## Helm: Franchise Kit

Teen services ke liye teen YAML theek hain. Par das services aur teen wings ke liye copy paste ka jungle ban jaata hai. Helm Kubernetes ka package manager hai, ek franchise kit: ek chart mein templates aur values.yaml hota hai, aur har wing ke liye alag values file. helm lint chart ko jaanchta hai, helm template bina lagaye final YAML dikhata hai. helm install atithi ./atithi -f values-prod.yaml poori app lagata hai, helm upgrade update karta hai, aur helm rollback atithi 1 pichhle release par wapas. Chart bhi vault mein rehta hai, pull request ke saath.

## Khoj ka Kram

Ab ek table jo apne paas rakho. Pod Pending: kubectl describe pod ke Events: jagah, quota ya storage. CrashLoopBackOff: kubectl logs --previous, aur exit code. ImagePullBackOff: image ka naam ya registry ki ijaazat. Service ke endpoints khaali: label aur selector ka mismatch. Ingress se 502 ya 404: backend pod Ready nahi, port galat, ya path galat. PVC Pending: koi matching PV ya StorageClass nahi. Aur sabka pehla kadam wahi: kubectl get events --sort-by=.lastTimestamp aur describe. Session 5 ka seedha sawaal: pehle jaano kya toota, phir badlo.

## Lab: Concierge aur Taale

Lab. Ek Ingress YAML likho: / web ko, /api/rooms rooms-service ko, /api/bookings bookings-service ko. Local cluster mein Helm se Traefik jaisa maintained controller lagao, jaise helm install traefik traefik/traefik -n traefik --create-namespace, aur GKE mein built-in. Ek jaal: Ingress path ko jyon ka tyon service tak bhejta hai. /api/rooms rooms-service ko jaaye to wo /api/rooms/health dekhega aur 404 dega. Isliye service ko wahi prefix do, ya controller ka strip-prefix rule lagao. Apply karke teeno raaste curl se test karo. Phir atithi wing mein ek default-deny NetworkPolicy lagao: pods aapas mein baat nahi kar paate. Ab sirf zaroori allow policies jodo: web se rooms aur bookings, bookings se rooms aur postgres, aur concierge ke wing se web, rooms aur bookings. Concierge wali policy bhoolne par default-deny ke baad Ingress bhi pods tak nahi pahunchta. Test pod se web se postgres tak koshish karo: nahi pahunchta. Ek ServiceAccount banao aur kubectl auth can-i se check karo. Aakhir mein helm template chalao. Safai: wing hatao, PVC hatao. Ab handover note likho: kaun si services chal rahi hain, kaise pahunchenge, data kahan rehta hai, kitna kharcha, undo kaise, aur known gaps. Yahan gaps ye hain: database ek hi hai bina replica aur backup ke, aur abhi koi TLS nahi.

## Recap aur Bridge

Recap: ek poora truck park: concierge, locker, taale aur franchise kit. Ab ek sawaal jo har raat poocha jaayega: ye sab theek chal raha hai, ye hum kaise jaanenge? Agle session mein control room: Prometheus aur Grafana.
