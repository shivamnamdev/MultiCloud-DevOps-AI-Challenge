# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-24_kubernetes-workloads-on-gke

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,998 · **Episodes:** 4

---

# EPISODE 1: Parking Bay ki Sehat

## Pod Chal Nahi Raha, Ab Kya?

Session 23 mein humne pod chalaya aur woh Running tha. Asli kaam mein pods aise nahi hote. Subah kisi ne bataya ki rooms-service sust hai. kubectl get pods ki list mein paanch pods paanch alag status dikhate hain. Kaun sa pehle dekhein? Is episode mein ek hi seedhi aadat banegi: status padho, exit code padho, describe ke Events padho. Session 5 ka troubleshooting method wahi hai, bas ab bays aur trucks ke naam se. Asli seekh tab hoti hai jab cheezein tootein, isliye lab mein hum jaan boojh kar pods ko todenge.

## Pod ke States

Pod ke paanch asli phases hain. Pending: pod ban gaya par abhi chalu nahi hua, aksar kyunki kisi building mein itna CPU ya memory nahi, ya jis storage ki zaroorat hai wo nahi mila. Running: pod ek building par laga hai aur kam se kam ek truck chal rahi hai, doosri abhi start ho rahi ho sakti hai. Succeeded: saari trucks ne kaam poora karke theek tareeke se band hui, jobs ke liye normal. Failed: ek ya zyada truck non-zero exit code ke saath band hui. Unknown: building tak pahunch nahi paa rahe. Ek zaroori sudhaar: CrashLoopBackOff aur Terminating phases nahi hain. Ye woh status hain jo kubectl get pods ke STATUS column mein dikhte hain, jaise ImagePullBackOff aur ContainerCreating. Roz dikhte yahi hain, isliye inhe jaanna zaroori hai.

## Exit Code: Truck Ne Kya Kaha

Truck ka exit code uski aakhri baat hai. Zero: theek se khatam. Ek: aam error, jaise web server config na milne se start nahi hua. 126: permission denied, yaani file executable nahi, chmod ki dikkat, jo Session 4 ka sabak hai. 127: command mili hi nahi, jaise truck ne aisi command chalayi jo design mein hai hi nahi. 137: kill kar di gayi, aur sabse aam wajah memory ki hadd paar karna, yaani OOMKilled. Ye 128 plus 9 hai, yaani signal 9, SIGKILL. 143 ek aur: 128 plus 15, SIGTERM, jo tab aata hai jab command ne use band hone ko kaha. Ye Session 5 aur 21 ke signals hain. Exit code ka matlab jaan liya to aadha debugging ho gaya.

## describe, Events aur logs --previous

Pod ki kahani kubectl describe pod ke sabse neeche Events table mein hai: kab schedule hua, kab image khichi, kab fail hua, aur kyun. Upar Containers section mein har truck ki State aur Last State hai: usme Reason aur Exit Code hota hai, jaise OOMKilled aur 137. Ab ek sawaal jo har engineer ko milta hai: "raat ke barah baje pod restart hua, par ab naya truck chal raha hai, to purane ke logs kahan?" kubectl logs POD -c TRUCK --previous pichhli truck ke logs deta hai, wahi jo crash hui thi. Jab pod mein ek se zyada trucks hon, to -c se naam batao. Aur agar pod mein ek hi truck hai, to bhi --previous crash ke baad sabse pehla command hai.

## Pending aur CrashLoopBackOff

Do status sabse zyada rulate hain. Pending: describe ke Events mein likha aata hai jaise "teen mein se koi building nahi jisme itna CPU ho." Wajah: pod ne zyada resources maange, ya jis disk ki zaroorat hai wo nahi mili, ya node ka koi niyam match nahi hua. Hal: request kam karo ya building jodo. CrashLoopBackOff: truck start hoti hai, mar jaati hai, command use phir chalata hai, aur har baar ruk ruk ke, kuch second se badhte badhte kuch minute tak. Wajah aksar app ki apni galti: database tak abhi pahunch nahi paayi, koi environment variable, ConfigMap ya Secret nahi mila, ya galat command. Hal: logs --previous, phir exit code. Pehle logs, phir change.

## Lab: Paanch Beemar Pods

Lab. Paanch beemar pods banao, ek ek kubectl run ya YAML se. Ek: image nginx:doesnotexist. Do: --command -- sh -c 'exit 1'. Teen: ek truck jo tail /dev/zero chalaye aur uski memory limit 32Mi ho. Chaar: ek pod jiski CPU request sau ho. Paanch: sh -c nosuchcmd. Ab har ek ke liye kubectl get pods, phir kubectl describe pod, aur likho: status, exit code, event ka sabse zaroori shabd. Ek hafta aap yahi order dohrao: status se shuru, describe ke Events, logs --previous agar crash ho, aur exit code se wajah. Dhyaan: ek pod mein dusra truck jodkar READY ko 1/2 dikha kar dekho, aur samjho ki ye truck ginti hai, pod ginti nahi. Safai: kubectl delete pod --all.

## Recap aur Bridge

Recap: pod ke states, exit code, describe aur --previous. Par ab bhi ek pod mara to koi wapas nahi laata. Agle episode mein standing order.

---

# EPISODE 2: Standing Order

## Pod Mara, Koi Wapas Nahi Laya

Bare pod ko kubectl delete pod karo, to wo gaya, aur koi use wapas nahi laata, kyunki kisi ne "hamesha teen" kaha hi nahi. Isliye pods ko hum seedha nahi chalate. Standing order dete hain, jaise "har floor par hamesha teen housekeeping staff". Pehla level hai ReplicaSet: ek order jo kehta hai "is label ke teen pods hamesha rahein." Doosra level Deployment hai, jo ReplicaSet ko sambhalta hai aur release ka kaam bhi. Dono ka status dekhna padta hai jab kuch galat ho.

## ReplicaSet ka YAML aur Columns

ReplicaSet ka YAML: apiVersion: apps/v1, kind: ReplicaSet. spec mein replicas, ek selector jo bataata hai kaun se pods apne hain, aur template, jisme pod ka nuskha hai. Template ke labels selector se match hone chahiye, nahi to ReplicaSet banta hi nahi. kubectl get rs ke columns: DESIRED, CURRENT aur READY. DESIRED matlab kitne pods hone chahiye. CURRENT jitne bane hain. READY jitne taiyaar hain. kubectl describe rs NAME mein Containers ke neeche image dikhta hai, aur pods ready kyun nahi, ye kisi pod ka describe dekhne se pata chalta hai. Pehle ye commands yaad karo: kubectl get rs, aur resource ka type hamesha likho, kyunki kubectl get new-replica-set nahi, kubectl get rs new-replica-set chalta hai.

## Scale, Replace aur Delete

ReplicaSet banane ke liye kubectl create -f, update ke baad kubectl apply -f, ya kubectl replace -f. Paanch pods tak le jaane ke do tareeke. kubectl scale rs rooms-rs --replicas=5. Ya kubectl edit rs rooms-rs, jahan spec mein replicas badal kar save karo. Hatane ke liye kubectl delete rs rooms-rs, ya kubectl delete -f rs.yaml. Ek naya sawaal: ek pod hata diya, phir bhi chaar hi kyun dikhte hain? Kyunki ReplicaSet dekhta hai ki desired paanch aur current chaar hai, aur turant ek naya bana deta hai. Ek hairan karne wali baat: agar aapne haath se ek pod banaya jiska label ReplicaSet ke selector se milta hai, to ReplicaSet use apna maan leta hai, aur ginti poori hone par use hata bhi sakta hai. Isliye labels sochkar rakho.

## Deployment: Release ka Maalik

Deployment ReplicaSet ke upar ka standing order hai. Aap Deployment likhte ho, wo ek ReplicaSet banata hai, aur ReplicaSet pods. Image badalne par Deployment ek naya ReplicaSet banata hai, aur purane ko dheere dheere kam karta hai. Isi ko rolling update kehte hain, floor by floor renovation jab hotel khula ho. maxSurge batata hai ki ek saath kitne extra pods ban sakte hain, aur maxUnavailable ki kitne kam ho sakte hain. Dono ka default pachchees percent hai. Purana ReplicaSet kuch samay bacha rehta hai, aur isi se rollback ho paata hai. Deployment ka READY column 3/3 hota hai, yaani teen mein se teen taiyaar. Dhyaan: pod ke READY mein trucks gine jaate hain, Deployment ke READY mein pods. 0/4 ka matlab chaar pods chahiye aur ek bhi taiyaar nahi.

## Release, Galat Release aur Rollback

Naya design chalane ke liye YAML mein tag badal kar kubectl apply, ya kubectl set image deploy/rooms rooms=ghcr.io/atithi/rooms-service:1.0.1. kubectl rollout status deploy/rooms progress dikhata hai. rollout history purane revisions, aur rollout undo pichhle par wapas, ya --to-revision se kisi tay par. Agar naya design galat ho, jaise tag ka naam galat, to naye pods ImagePullBackOff mein atak jaate hain, par purane pods chalte rehte hain, kyunki Deployment tab tak purane nahi hatata jab tak naye taiyaar na hon. Guests tak asar nahi. Ye tab hi sachhi suraksha hai jab pod mein readiness check bhi ho, jise hum agle session mein dekhenge. Aur har release par change-cause ka note rakho.

## Lab: Order, Galat Release, Wapas

Lab. Deployment ka YAML kubectl create deployment rooms --image=nginx:1.26-alpine --replicas=3 --dry-run=client -o yaml > rooms.yaml se banao, aur kubectl apply -f rooms.yaml. Phir kubectl delete pod karke dekho ki replacement turant aata hai. Ab kubectl set image deploy/rooms nginx=nginx:doesnotexist, kyunki create deployment ne truck ka naam nginx rakha hai. kubectl get pods mein naye pod ImagePullBackOff mein hain par purane Running. kubectl rollout status atka rahega. Phir kubectl rollout undo deploy/rooms. Ab sahi tag, nginx:1.27-alpine, set karo aur dekho ki pods ek ek karke badalte hain, aur kubectl rollout history mein revisions. Safai: kubectl delete deploy rooms.

## Recap aur Bridge

Recap: ReplicaSet, Deployment, rollout aur rollback. Ab sawaal: pods badalte rehte hain, to guests ko kaun sa address milega? Aur ek hi cluster mein dev, staging aur production ko kaise alag rakhein?

---

# EPISODE 3: Wings aur Extension Number

## Ek Cluster, Teen Team

Ek cluster mein dev, staging aur production, aur kai teams. Agar sab ek hi jagah ho, to naam takrate hain: dono jagah frontend aur backend hain. Ek ki galti doosre ko tod sakti hai. Namespace cluster ke andar ek alag wing hai: alag naam, alag access, alag resource ki hadd. Dev wing mein backend aur staging wing mein bhi backend aaram se chalte hain, aur ek doosre se takrate nahi. Notes ki ek achhi misaal: cluster ek library hai aur namespace alag alag bookshelf. Do shelf par ek hi naam ki kitaab ho sakti hai, aur koi confusion nahi.

## Namespace ke Commands

Namespace ka YAML: apiVersion: v1, kind: Namespace, aur metadata mein name aur labels. Naam mein underscore nahi chalta, isliye dev-wing, dev_wing nahi. Bina YAML ke kubectl create namespace dev. kubectl get namespaces list, describe detail. Kisi wing mein kaam ke liye -n dev: kubectl get pods -n dev, kubectl run redis --image=redis -n dev, kubectl create -f x.yaml -n dev. Ek pod kis wing mein hai ye bhoolo to kubectl get pods -A | grep blue. Flag -A ya --all-namespaces hai. Ek khatra: kubectl delete namespace dev us wing ki saari cheezein hata deta hai. Aur kuch cheezein wing ki hoti hi nahi, jaise nodes aur persistent volumes. Cluster ke default wing: default, kube-system, kube-public aur kube-node-lease.

## Wing Badalna aur Wing Paar Baat

Har command ke saath -n dev thakane wala hai. Isliye kubectl config set-context --current --namespace=dev: ab bina -n ke har command dev wing mein chalega. Isme bhi khatra: bhool jao ki ab dev mein ho. Isliye prompt mein namespace dikhao. Kya ek wing ka pod doosre wing ke pod se baat kar sakta hai? Haan, service ke poore naam se: <service>.<namespace>.svc.cluster.local, jaise backend.dev.svc.cluster.local. Apni wing mein sirf backend kaafi hai. Ye dhyaan rakho ki wing akeli suraksha ki deewar nahi: bina network policy ke koi bhi pod kisi bhi wing se baat kar sakta hai. Network policy hum Session 25 mein dekhenge.

## Service: Permanent Extension Number

Pod ka IP naya pod banne par badal jaata hai. Jo client usi IP se baat karta rahe, wo tootega. Service ek permanent extension number hai: ek tay IP aur DNS naam, jo peeche ke pods ko label ke zariye dhoondhti hai aur traffic baantti hai. Cluster mein ek Service pehle se hoti hai: kubernetes. kubectl get services mein uska TYPE dikhta hai, aur kubectl describe service kubernetes mein TargetPort, Labels aur Endpoints. Endpoints wahi pods hain jinhe Service abhi traffic bhej rahi hai. Aur sirf Ready pods hi endpoints mein aate hain. Ye Session 11 ke marshal ka health check hai, bas cluster ke andar.

## Service ke Types aur YAML

Service ke teen mukhya types. ClusterIP default hai: sirf cluster ke andar. NodePort har building par 30000 se 32767 ke beech ek port kholta hai. LoadBalancer cloud ka load balancer banata hai aur ek external IP deta hai, jo Session 11 ke marshal ka Kubernetes roop hai. YAML mein selector batata hai kaun se pods, port Service ka darwaza, aur targetPort truck ka port. Ek chhoti command: kubectl expose pod redis --port=6379 --name redis-service, jo ek chalte pod ke liye ek Service bana deti hai, jo cluster ke andar redis ko 6379 par dikhaye. Aur ek hi pehchaan wali galti: Service ka selector aur pod ka label mile nahi, to kubectl get endpoints rooms khaali aayega. Wahi Session 23 ka label jaal.

## Lab: Dev Wing, Staging Wing, Ek Naam

Lab. kubectl create namespace dev aur kubectl create namespace staging. Dono mein kubectl create deployment rooms --image=nginx:alpine --replicas=2 -n dev aur wahi staging mein, aur kubectl expose deployment rooms --port=80 -n dev, staging mein bhi. kubectl get pods -A | grep rooms se dono wing ke pods dekho. Ab staging mein ek test pod: kubectl run tmp -n staging --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- rooms.dev.svc.cluster.local. Nginx ka page aayega. Phir kubectl get endpoints rooms -n dev mein do IP. Naye Kubernetes mein ye command deprecated ka warning deti hai, kyunki ab EndpointSlice use hota hai, to kubectl get endpointslices -n dev bhi aazma lo. Ab kubectl edit svc rooms -n dev se selector galat kar do aur get endpoints dobara: khaali. Aakhir mein kubectl delete namespace dev staging aur dekho ki sab saath hat gaya.

## Recap aur Bridge

Recap: wings aur extension numbers. Ab sawaal: guests ki line badhe to kya karein? Aur ye sab cloud par kaise chalayein?

---

# EPISODE 4: Zyada Trucks ya Bada Truck

## Shaadi ka Season

Shaadi ke season mein Atithi ki booking site par line badh jaati hai. Do hi raaste hain. Ya zyada trucks kholo, ya ek truck ko bada karo. Pehle ko horizontal scaling kehte hain, out aur in. Doosre ko vertical scaling, up aur down. Session 10 mein humne Auto Scaling mein buildings badhai thi, aur Session 13 mein records office ka size badhaya tha. Wahi do vichar yahan trucks par hain.

## Kab Kaun Sa

Horizontal tab, jab app ke independent copies ban sakte hon: web server, microservices. Badi sale mein zyada log aate hain, aur har pod thoda traffic sambhalta hai. Vertical tab, jab ek hi strong instance chahiye. Maan lo Atithi ke database mein peak ghanton mein complex queries chalte hain. Copies banane se data sync ki dikkat aati hai, to ek ko zyada CPU aur memory do. Session 13 ka wahi sabak: instance class badalna vertical hai, aur read replica horizontal. Seedha rule: web ko phailao, database ko mazboot karo, aur database ko phailana ho to uska poora alag tareeka hai.

## HPA: Apne Aap Zyada Trucks

HPA, Horizontal Pod Autoscaler, ek supervisor hai jo pods ka average CPU dekhta hai aur replicas badhata ya ghatata hai. kubectl autoscale deployment rooms --cpu=50% --min=2 --max=5. Iske do shart hain. Metrics ka source chahiye, yaani metrics-server, jo GKE mein pehle se hota hai aur local cluster mein alag lagana padta hai. Aur pod ke container mein CPU request likha hona chahiye, kyunki percent usi request ka hota hai. Scale up tez hota hai, par scale down jaan boojh kar dheere: kuch minute ka intezaar, taaki line ek second ke liye ghat jaaye to trucks hat na jaayein.

## Vertical, aur Buildings ka Sawaal

Vertical ke liye Kubernetes mein Vertical Pod Autoscaler jaisa ek alag tool hai, jo dekhta hai ki pod ko asli mein kitna chahiye, aur request badalne ki salah deta hai. Aur ek aur baat: HPA ne pods badha diye, par buildings mein jagah nahi hui to naye pods Pending ho jaayenge. Wahan building ka scaling aata hai: node autoscaler. Autopilot jaise mode mein landlord ye khud karta hai. Ek HPA aur VPA ek hi resource par saath mat chalao.

## GKE: Landlord Command Chalaye

Control plane khud chalana mehnat ka kaam hai: upgrades, etcd ka backup, security patches. GKE, Google Kubernetes Engine, ye kaam landlord ko de deta hai. Iske do mode. Autopilot mein buildings bhi Google sambhalta hai, aur bill pods ke maange hue resources par aata hai, isliye resource requests likhna zaroori ho jaata hai. Request na likho to Autopilot khud default laga deta hai, aadha vCPU aur do GiB, aur bahut chhoti request ko minimum tak badha deta hai, jaise CPU ke liye 250 milli. Standard mein aap node pools khud chalate ho: machine type, autoscaling, aur zyada control. AWS par wahi kaam EKS karta hai, aur Azure par AKS. Cluster se judne ke liye gcloud container clusters get-credentials, jo kubeconfig mein ek naya context jod deta hai. kubectl ko GKE se baat karne ke liye gke-gcloud-auth-plugin chahiye: gcloud components install gke-gcloud-auth-plugin. Docs mein ab --region ki jagah --location likha hota hai, dono chalte hain.

## Depot se Image aur Bahar ka Darwaza

Pehle depot banao: gcloud artifacts repositories create REPO --repository-format=docker --location=REGION, aur gcloud auth configure-docker REGION-docker.pkg.dev se Docker ko login sikhao. Phir apni design ko Artifact Registry mein push karo: docker tag, docker push REGION-docker.pkg.dev/PROJECT/REPO/rooms-service:1.0.0. Cluster ko use khichne ki ijaazat chahiye: nodes ki service account ko registry padhne ka role. Naye project mein ye service account ke paas koi role hota hi nahi, to pehli baar pods ImagePullBackOff mein aate hain, aur kubectl get events mein 403 Forbidden dikhta hai. Hal: gcloud artifacts repositories add-iam-policy-binding REPO --location=REGION --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader. Session 9 ka wahi sabak: kaun kya kar sakta hai. Service ko type: LoadBalancer karo, to GKE ek Google load balancer banata hai aur kuch der mein EXTERNAL-IP dikhata hai. Load balancer aur uski IP bhi paisa leti hain, isliye lab ke baad sab hatao.

## Lab: GKE par Poora Deploy

Lab. GCP project mein billing on karo, aur gcloud services enable container.googleapis.com artifactregistry.googleapis.com se Kubernetes Engine aur Artifact Registry API chalu karo. gcloud container clusters create-auto atithi-lab --region=YOUR_REGION, jisme saat-aath minute lagte hain, aur cluster shuru mein bina kisi node ke hota hai. Phir gcloud container clusters get-credentials atithi-lab --region=YOUR_REGION aur kubectl config current-context se pakka karo ki aap sahi cluster par ho. Deployment aur type: LoadBalancer Service ke YAML kubectl apply -f karo, jisme container ki CPU request zaroor ho. kubectl get svc -w mein EXTERNAL-IP aaye to browser mein kholo. Pehli baar pods kareeb teen minute Pending rehte hain, kyunki Autopilot pehle building kholta hai. Ek rolling update karo aur rollback bhi. Phir kubectl autoscale deployment rooms --cpu=50% --min=2 --max=5, ek chhote load generator se line badhao, aur kubectl get hpa -w dekho. Hamare test mein replicas do se paanch kareeb ek minute mein ho gaye, aur wapas do hone mein das se pandrah minute lage. Scale down jaan boojh kar dheere hai. Sabse aakhir mein gcloud container clusters delete atithi-lab --region=YOUR_REGION, aur console mein dekho ki koi load balancer, forwarding rule, disk ya image nahi bacha.

## Recap aur Bridge

Recap: Kubernetes ke asli workloads: pod ki sehat, standing order, wings, extension numbers, scaling, aur GKE. Ab Atithi ka poora truck park: kai chhoti services, jo ek doosre ko extension se bulati hain, ek concierge jo guests ko sahi truck tak le jaaye, aur ek locker room jisme records bachein. Agle session mein microservices.
