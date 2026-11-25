# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-31B_gitops-with-argo-cd

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,433 · **Episodes:** 4

---

# EPISODE 1: Vault hi Sach Hai

## Raat ke Teen Baje, Ek kubectl edit

Raat ke teen baje, rooms-service par load badha. Ek engineer ne jaldi mein kubectl edit kiya aur replicas badha diye. Kaam ho gaya. Par vault mein ab bhi purana number hai. Agle hafte pipeline chali, number wapas ghat gaya, aur kisi ko samajh nahi aaya ki guests ki line kyun lambi ho gayi. Ye wahi drift hai jo Session 27 mein Terraform ke saath dekha tha, ab Kubernetes ke andar. Sawaal seedha hai: agar vault hi sach hai, to campus apne aap vault jaisa kyun nahi rehta? Is session ka jawab GitOps hai.

## GitOps ke Chaar Niyam

GitOps ke chaar niyam. Ek: jo campus mein hona chahiye, wo files mein likha ho, yaani manifests, jaise Session 24 ke Deployment aur Service. Do: wo files vault mein rahein, to har badlaav ka naam, tareekh aur review ho. Teen: koi agent unhe khud khinchkar lagaye. Chaar: wo agent baar baar milaye ki asli campus vault jaisa hai ya nahi, aur farq ho to theek kare. Chaar niyam milkar ek simple baat banate hain: vault mein change karo, campus apne aap badal jaata hai, aur campus mein haath se change karo to wo wapas ho jaata hai. Story mein is agent ka naam hai site supervisor.

## Foreman Dhakelta Hai, Supervisor Kheenchta Hai

Session 31 mein foreman ne deploy.sh ke saath truck ko building tak dhakela. Isse push kehte hain, aur uske liye foreman ke paas campus ki chaabi chahiye, yaani CI ke key cabinet mein cluster ke credentials. Agar CI par koi daaka dale, to campus ki chaabi bhi gayi. Pull ulta hai: supervisor campus ke andar rehta hai, aur bahar vault ko padhta hai. Chaabi andar hi rehti hai, aur CI ko sirf vault mein likhne ka haq chahiye. Isliye do vault rakhte hain. Ek app vault, jisme code hai, jis par foreman test aur truck design banata hai. Aur ek config vault, jisme sirf manifests hain, jo supervisor padhta hai. Foreman ka kaam banta hai: nayi truck design depot mein rakho, aur config vault mein edition label badlo. Ek aur fayda: "prod mein ye kisne badla?" ka jawab git log mein hota hai, kisi ke terminal history mein nahi. Har badlaav ka naam, tareekh aur review.

## Argo CD Ke Hisse aur Install

Argo CD site supervisor ka asli naam hai, aur wo campus ke andar apne ek wing argocd mein chalta hai. Uske hisse: application controller, jo vault aur campus ko milata hai. Repo server, jo vault padhkar manifests banata hai. API server aur UI. Redis cache ke liye, Dex login ke liye, aur notifications aur ApplicationSet ke controller. Install ek manifest se hota hai, par ek jaal hai. Seedha kubectl apply karo to ApplicationSet ki CRD par error aata hai: Too long: may not be more than 262144 bytes, kyunki client-side apply ek bada annotation likhta hai. Hal: kubectl apply --server-side --force-conflicts. Aur URL mein stable ki jagah ek pakka version likho, taaki aaj aur kal ka install ek jaisa ho. Hamare test mein sab pods ek minute mein Running ho gaye.

## Lab: kind par Argo CD

Lab. Session 23 ka kind cluster banao: kind create cluster --name argo. Phir:

Jab sab Running ho, pehla password nikalo: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d, ya argocd admin initial-password -n argocd. Phir kubectl port-forward svc/argocd-server -n argocd 8080:443 aur browser mein https://localhost:8080. Certificate ki chetavani local test mein normal hai. User admin, wahi password. Terminal ke liye argocd CLI bhi lagao aur argocd login localhost:8080 --username admin --insecure se login karo. Pehli cheez: password badlo, aur initial secret hata do, kyunki wo ek khula taala hai. Ek GitHub repo atithi-config banao, aur usme rooms/deployment.yaml aur rooms/service.yaml rakho, jaise Session 24 mein likhe the, jisme CPU request ho.

## Recap aur Bridge

Recap: GitOps ka matlab hai vault hi sach. Supervisor khinchta hai, chaabi andar rehti hai, aur do vault. Install server-side, aur version pakka. Ab supervisor ko pehla kaam do: ek Application.

---

# EPISODE 2: Application

## Ek Application, Teen Sawaal

Supervisor ko teen sawaal ka jawab chahiye. Standing order kahan rakha hai: repo, branch aur folder. Kahan lagana hai: kaun sa cluster aur kaun sa wing. Aur kis ijaazat ke saath: project. Ye teen jawab ek Application object mein likhte hain:

https://kubernetes.default.svc ka matlab wahi cluster jisme Argo CD khud chal raha hai. CreateNamespace=true se wing khud ban jaata hai.

## Do Alag Sawaal: Synced Hai Ya Healthy?

Application par do alag badge dikhte hain, aur inhe mila dena sabse aam galti hai. Sync Status poochta hai: campus vault se milta hai ya nahi, yaani Synced ya OutOfSync. Health Status poochta hai: jo chal raha hai wo theek chal raha hai ya nahi: Healthy, Progressing, Degraded ya Missing. Pehle sync se pehle Application OutOfSync aur Missing dikhta hai, kyunki vault mein order hai par campus mein kuch nahi. Sync ke baad Synced aur Progressing, aur pods ready hote hi Healthy. Aage dekhenge: ek kharab release Synced bhi ho sakta hai aur Healthy nahi.

## Sync: Haath Se, Phir Apne Aap

Sync ka matlab hai vault ke order ko campus par lagana. Haath se: UI ka Sync button, ya argocd app sync rooms. Argo CD har object par ek annotation argocd.argoproj.io/tracking-id lagata hai, taaki jaane ki kaun si cheez uski hai. Automatic ke liye syncPolicy mein automated likhte hain. Do switch ka dhyaan: prune: true ka matlab hai ki jo cheez vault se hat gayi, wo campus se bhi hat jaaye. selfHeal: true ka matlab hai ki campus mein haath se kuch badla to wapas vault jaisa ho. Dono default mein band hain, yaani sirf automated likhna kaafi nahi.

## Kitni Jaldi Pata Chalta Hai, aur Drift ka Ilaaj

Vault mein badlaav karo to Argo CD ko kitni der mein pata chalta hai? Default mein wo har teen minute ke aas paas vault ko dekhta hai, jitter ke saath. Hamare test mein ek commit ko campus tak pahunchne mein lagbhag paanch minute lage. Usse pehle chahiye to UI mein refresh dabao, ya vault mein webhook lagao, jo seconds mein bata deta hai. Ab drift. selfHeal band ho aur aap kubectl scale se replicas paanch kar do, to Application OutOfSync dikhata hai, par campus ko wahin chhod deta hai. selfHeal chalu karo, to kuch seconds mein replicas wapas vault wale number par aa jaate hain. Hamare test mein haath se hataya hua Service bhi kuch seconds mein wapas aa gaya.

## Lab: Pehla Sync aur Drift

Lab. Upar wala Application apne repo ke URL ke saath kubectl apply -f karo. Tile OutOfSync aur Missing dikhegi. Sync dabao: Synced, phir Healthy, aur kubectl -n atithi get pods mein do pods. Ab vault mein replicas ko teen karo, commit karo, aur refresh dabao ya intezaar karo. Phir syncPolicy mein automated: {prune: true} jodo. kubectl -n atithi scale deploy rooms --replicas=5 karo: OutOfSync, par number wahin atka rehta hai. Ab selfHeal: true jodo, aur dekho ki number kuch seconds mein teen par wapas. Aakhir mein kubectl -n atithi delete svc rooms karo aur dekho ki Service wapas aa jaati hai.

## Recap aur Bridge

Recap: Application, do alag badge, auto-sync ke do switch, aur drift ka ilaaj. Ab ek asli sawaal: naya version dev se prod tak kaise jaaye, aur kuch kharab ho to wapas kaise aayein.

---

# EPISODE 3: Naya Version

## Naya Edition Label Kahan Se Aata Hai

GitOps mein naya version aise chalta hai. App vault mein badlaav, foreman ki conveyor test karti hai, truck design banati hai, scan karti hai, aur depot mein edition label ke saath rakhti hai, bilkul Session 31 jaisa. Aakhri station alag hai: wo config vault mein sirf ek line badalta hai, naya edition label, aur ek pull request kholta hai. Chief architect use review karta hai, jaise Session 16B mein. Merge hote hi site supervisor naya label campus par lagata hai. Conveyor ko cluster ki chaabi kabhi nahi chahiye.

## Base aur Overlay: Dev aur Prod

Dev aur prod mein zyada tar cheezein ek jaisi hoti hain, bas replicas, wing aur edition label alag. Isliye Kustomize: ek base folder mein common manifests, aur har environment ka ek chhota overlay. Argo CD Kustomize aur Helm dono ko seedha samajhta hai, kuch extra install nahi karna.

overlays/dev mein wahi, par count: 1 aur namespace: atithi-dev. Phir do Application, ek overlays/dev par aur ek overlays/prod par. Edition label sirf images mein badalta hai.

## Promotion: Pehle Dev, Phir Prod, Diff ke Saath

Promotion ka matlab hai wahi edition label pehle dev mein, aur jab dev theek ho, prod mein. Har step ek pull request: dev ki file badlo, supervisor dev par lagata hai, tum dekhte ho. Phir prod ki file mein wahi ek line, review ke saath. Merge se pehle argocd app diff rooms-prod --refresh chalao: wo bilkul batata hai ki campus mein kya badlega, hamare test mein sirf image: rooms:s22 se rooms:s31. Yaani prod mein kya jaa raha hai, ye deploy se pehle review mein dikh jaata hai.

## Kharab Release aur Rollback: Git Revert

Ab jaan-boojh kar kharab release: edition label jo depot mein hai hi nahi. Application dikhata hai Synced, kyunki campus vault jaisa hi hai, par Health Progressing, kyunki naya pod ImagePullBackOff mein hai. Rolling update ki wajah se purane pods abhi guests ko serve kar rahe hain. Synced ka matlab sahi nahi hota, vault jaisa hota hai. Rollback ka natural tareeka vault mein hai: git revert aur push. Hamare test mein revert ke kuch seconds baad Application wapas Healthy tha. Ek jaal: argocd app rollback rooms 1 auto-sync ke saath mana hai, error aata hai ki rollback cannot be initiated when auto-sync is enabled, kyunki supervisor use turant undo kar deta. Isliye rollback hamesha vault ka badlaav hai. argocd app history rooms purane syncs ki list dikhata hai.

## Secrets Vault Mein Nahi

Ek sawaal turant uthta hai: secrets ka kya? Secret ka manifest vault mein plain mat daalo, base64 sirf encoding hai, Session 25 aur Session 20 ki wahi baat. Teen raaste hain, aur teeno alag tool hain jo Argo CD ke saath chalte hain. Encrypted Secret jise sirf cluster khol sake, cloud ke secret manager se padhne wala tool, ya ek encrypted file jo team ki chaabi se khulti hai. Tool ka naam apni team ke saath chuno, aur uska doc padho. Sabka niyam ek hai: config vault mein jo bhi hai, wo public hone par bhi nuksaan na kare.

## Lab: Overlay, Promotion aur Revert

Lab. Config vault ko base aur overlays/dev, overlays/prod mein baanto, jaise upar. Do Application banao. Dono Synced aur Healthy: dev mein ek pod, prod mein teen. Dev ki newTag badlo aur dekho ki sirf dev badalta hai. Phir prod ke liye pehle argocd app diff rooms-prod --refresh, phir badlao. Ab jaan-boojh kar prod mein newTag mein aisa label likho jo depot mein nahi hai. Dekho Synced aur Progressing, kubectl -n atithi-prod get pods mein ImagePullBackOff. argocd app rollback try karke error padho. Phir git revert HEAD aur push, aur Healthy wapas aate dekho.

## Recap aur Bridge

Recap: conveyor sirf label likhti hai. Base aur overlay, promotion pull request se, diff pehle, rollback git revert se, aur secrets vault mein plain nahi. Ab supervisor ko kuch limit chahiye: wo kis vault se, kis wing mein, kya laga sakta hai.

---

# EPISODE 4: Guard Rails

## AppProject: Supervisor ki Hadd

Supervisor bahut taaqatwar hai, wo campus mein kuch bhi laga sakta hai. Isliye har Application ek project ke andar chalta hai, aur project batata hai: kaun se vault, kaun se wing, aur kaun se object allowed hain. Ye Session 9 ka least privilege hai, Argo CD ke andar.

Is project mein koi Application kube-system mein lagana chahe, to Argo CD mana karta hai: application destination ... do not match any of the allowed destinations in project 'atithi'. Default project sab kuch allow karta hai, isliye asli kaam ke liye apna project banao.

## ApplicationSet: Ek Template, Kai Application

Dev aur prod ke liye do alag Application likhna theek hai. Par das services aur teen environments ho jaayein, to tees file. ApplicationSet ek template aur ek list se Applications khud banata hai:

Hamare test mein rooms-dev aur rooms-prod is ek file se khud ban gaye. List ke alawa folders ya clusters par bhi generator hota hai.

## Kaun Andar Aa Sakta Hai, aur Private Vault

Argo CD ka apna darwaza bhi surakshit rakho. admin account sirf shuruat ke liye hai: SSO se login, role ke hisaab se access, aur admin ko band karo. UI aur API ko seedha internet par mat kholo; ingress aur HTTPS ke peeche, jaise Session 25 ke concierge mein. Agar config vault private hai, to supervisor ko ek read-only deploy key do, wahi Session 17 ka sabak: sirf padhne ki chaabi, aur wo Argo CD ke repository credential mein. Instant sync chahiye to vault ka webhook Argo CD ke API ko bhejo. Exact steps apne version ke docs mein dekho, kyunki settings badalti rehti hain. Aur Argo CD ki apni settings aur Applications bhi config vault mein rakho, taaki supervisor par bhi wahi review lage jo trucks par lagta hai.

## Capstone Mein Kahan Baithta Hai

Session 31 mein aakhir ka station deploy.sh tha: SSH se building par jaao, truck badlo, health check karo. Kubernetes par wahi station config vault ka update ban jaata hai. Conveyor config vault ko clone karta hai, overlays/dev/kustomization.yaml mein newTag ko naye edition label se badalta hai, commit aur push karta hai. Baaki kaam supervisor ka: naya label lagana, aur health batana. Health check aur rollback ab Argo CD ke Health aur git revert mein hain. Control room, yaani Prometheus aur Grafana, jaise the waise rehte hain. Pehle dev par aazmao, aur prod ke liye pull request zaroori rakho.

## Kab Nahi, aur Kya Alag Hai

Argo CD sab kaam ka tool nahi hai. Wo Kubernetes ke manifests lagane mein achha hai, kai environments ke saath, aur har badlaav Git mein record hota hai. Wo truck banata nahi, wo foreman ka kaam hai. Wo campus ki infrastructure, yaani Terraform ka kaam, nahi karta. Aur pull ka matlab hai thodi der: webhook ke bina kuch minute. Do naam jo aap sunoge: Flux, ek aur GitOps tool jo isi vichar par chalta hai, aur Argo Rollouts, jo dheere dheere ya canary rollout deta hai, jaise Session 11 ke weighted target groups, par Kubernetes ke andar. Pehle Argo CD ke yeh basics seekho, phir aage ke tools dekhna.

## Lab: Project aur ApplicationSet

Lab. Upar wala AppProject apply karo. Ek Application banao jo kube-system mein lagana chahe, aur dekho ki wo InvalidSpecError ke saath ruk jaata hai. Phir do haath se banaye Application hata do, ApplicationSet apply karo, aur dekho ki rooms-dev aur rooms-prod khud ban gaye, dono Synced aur Healthy. Ek aakhri sawaal: prod mein selfHeal ke saath aap emergency mein kubectl edit karo to kya hoga? Aazma kar dekho, kyunki asli raat ke teen baje yahi sawaal aayega. Hamare test mein hath ka badlaav do second mein wapas ho gaya, aur ApplicationSet wale Application par argocd app set --sync-policy none bhi kaam nahi karta, kyunki set use wapas likh deta hai. Emergency ka rasta Git commit hai. Safai: kind delete cluster --name argo.

## Recap aur Bridge

Recap: vault hi sach hai. Supervisor khinchta hai, Sync aur Health alag hain, rollback git revert hai, project supervisor ki hadd tay karta hai, aur ApplicationSet ek template se kai Application banata hai. Ab Atithi ke head office mein ek naya sadasya aata hai: ek bahut padha-likha assistant. Pehle wo ek bahari expert ki tarah phone par jawab dega. Phir ek trained brain ki tarah, jo kisi bhi truck ki tarah chalta hai. Agla session: AI apps aur MLOps.
