# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-26_prometheus-and-grafana

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,750 · **Episodes:** 4

---

# EPISODE 1: Control Room kyun

## Gaadi ka Dashboard

Gaadi chalate waqt dashboard aapko speed, tel aur engine ka temperature batata hai, aur warning light pehle se chetavani deti hai. Bina dashboard ke gaadi achanak rukti hai. Atithi ki truck park ab Kubernetes par chal rahi hai: dus services, kai wings, kai buildings. Agar kuch dheema hua, to guests ko pehle pata chalega ya hamein? Session 15 mein humne landlord ke meters aur CloudWatch dekhe. Ab head office ka apna control room banate hain, jo trucks ke andar tak dekhta hai, aur jo kisi bhi landlord par ek jaisa chalta hai.

## Teen Pillars

Observability ka matlab hai ki system ke bahar ke signals dekhkar andar ki halat samajh paao. Iske teen pillars. Metrics: samay ke saath badalte numbers, jaise requests per second. Wo batate hain kya ho raha hai. Logs: ghatnaon ke record, jo batate hain kyun. Traces: ek request ka kai services ke beech poora safar, jo batata hai kahan dheema hua. Is session mein hum metrics par dhyaan denge, kyunki Prometheus aur Grafana ki jodi sabse aam hai. Logs ke liye Loki jaise tools, aur traces ke liye OpenTelemetry, aage ki padhai hain, par wahi teen sawaal yaad rakho.

## Kya Naapein: Golden Signals

Kya naapein? Session 15 ke chaar signals yaad hain: latency, traffic, errors aur saturation. Google ke SRE ne inhe golden signals kaha hai. Latency: request kitni der leti hai. Traffic: kitni aa rahi hain. Errors: kitni fail ho rahi hain. Saturation: system kitna bhara hai. Services ke liye RED: Rate, Errors, Duration. Building jaise resources ke liye USE: Utilization, Saturation, Errors, jo Session 5 ke top, free aur df ka systematic roop hai. Chaar golden signals se zyadatar problems pakadi jaati hain, aur har dashboard inhi se shuru hona chahiye, baaki detail neeche.

## SLI, SLO aur Error Budget

Naapna kaafi nahi, ek target bhi chahiye. SLI, Service Level Indicator, wo number jo aap naapte ho: kitne percent requests successful, ya kitne percent 300 ms se tez. SLO, Service Level Objective, wo target: "tees din mein 99.5 percent requests successful." Aur error budget: baaki 0.5 percent, yaani jitni galtiyon ki chhoot hai. Ye budget team ko seedha faisla deta hai. Budget bacha hai to naya release karo, aur budget khatam ho gaya to nayi cheezein ruko aur sthirta par kaam karo. Is se "kitna achha kaafi hai" ka jhagda number mein badal jaata hai. Target ko 100 percent mat rakho: wo mehnga hai aur kabhi milta nahi.

## Lab: Paper par SLI aur SLO

Lab (paper). bookings-service aur rooms-service ke liye teen cheezein likho. Ek SLI: success rate, aur 95th percentile latency. Ek SLO, jaise "tees din mein 99.5 percent successful, aur 95 percent request 300 ms se kam." Aur error budget ko minutes mein badlo: 99.9 percent ka matlab tees din mein lagbhag 43 minute ki chhoot. Phir sochkar likho ki bookings ka SLO rooms ke SLO se zyada sakht kyun hona chahiye. Guest rooms ki list dheemi dekh kar ruk sakta hai, par booking ke beech mein error aaye to wo seedha chala jaata hai. Aur koi bhi SLO bina is jawab ke ki "isko kaun dekhega" adhoora hai.

## Recap aur Bridge

Recap: observability, golden signals aur SLO. Ab inspector se milte hain: Prometheus.

---

# EPISODE 2: Inspector

## Inspector Poochhta Hai

Prometheus ka tareeka alag hai. Trucks apne numbers inspector ko bhejti nahi. Inspector khud har kuch second mein har truck ke paas jaakar poochta hai: "tumhare numbers do." Isse pull model kehte hain. Ek bonus: agar truck jawab hi na de, to inspector ko turant pata chal jaata hai ki wo gir gayi, kyunki us ka up meter zero ho jaata hai. Session 11 ke marshal ke health check ka yahi vichar hai, bas har meter ke liye. Numbers ek time-series database mein jaate hain, aur har number ke saath samay hota hai.

## Exporter, Metric ke Types aur Labels

Truck ke paas ek /metrics page hota hai, jisme uske numbers text mein hote hain. Jo cheezein khud numbers nahi deti, unke liye exporter: building ke CPU, memory aur disk ke liye node exporter, jo Session 5 ke top aur df ko numbers mein badalta hai. Kubernetes mein service discovery se targets apne aap milte hain. Metric ke teen type. Counter: sirf badhta hai, jaise kul requests. Gauge: upar neeche hota hai, jaise memory. Histogram: values ko buckets mein ginta hai, jisse latency ke percentiles nikalte hain. Labels metric ko dimension dete hain, jaise method="GET" aur status="500". Ek dhyaan: label ki values bahut zyada hon, jaise har guest ka ID, to inspector ki memory phat jaati hai. Ise cardinality ka khatra kehte hain.

## Apni Service ko Meter Do

Apni service ke meters khud lagane padte hain. Python mein prometheus_client library: ek Counter http_requests_total labels method, path aur status ke saath, ek Histogram http_request_duration_seconds, aur ek /metrics route jo generate_latest() ka jawab de. Har request ke baad counter ek badhao, aur samay histogram mein daalo. Label mein route ka template rakho, jaise /rooms/<id>, guest ya room ki asli ID nahi. Wahi cardinality ka sabak. Ye Session 22 ki rooms-service ka chhota sa sudhaar hai, aur Session 7 ke Python ka seedha upyog.

## PromQL ki Basics

PromQL Prometheus ki query language hai. up batata hai kaun si trucks zinda hain. Counter ko seedha nahi dekhte, uski rate dekhte hain: rate(http_requests_total[5m]) pichhle paanch minute mein per second requests. sum by (status)(...) unhe status ke hisaab se jodta hai. Error ratio ke liye 5xx ki rate ko poori rate se divide karo: sum(rate(...{status=~"5.."}[5m])) / sum(rate(...[5m])). Aur latency ke liye histogram_quantile(0.95, ...). Ek aam galti: counter ko bina rate ke plot karna, jo bas ek badhti hui line dikhata hai aur kuch nahi batata. Aur [5m] ka window bahut chhota rakhoge to graph jhatke maarega. Ek aur jaal: jab koi 5xx hai hi nahi, to error ratio ki query khaali aati hai, zero nahi, aur panel mein "No data" dikhta hai. Query ke aakhir mein or vector(0) lagao.

## Recording Rule aur Yaadashta ki Seema

Do baatein jo dashboard badhne par dikhti hain. Ek: bhaari query. Agar ek dashboard har baar sau trucks par histogram_quantile chalaye, to wo dheema ho jaata hai. Recording rule us query ka natija inspector khud har minute ek naye metric mein rakh deta hai, jaise job:http_requests:rate5m, aur dashboard use seedha padhta hai. Do: yaadashta. Prometheus ka apna storage kuch hafte ke liye hota hai. Helm chart ke default mein wo emptyDir par hai, yaani pod gaya to data gaya; locker, yaani PVC, chahiye to storage khud tay karna padta hai, Session 25 jaisa. Lambi history, jaise ek saal, ya kai clusters ek jagah, ke liye alag long-term store chahiye, jaise Thanos ya Mimir ya cloud ki managed service. Aur ek dhyaan: Prometheus aapka backup system nahi hai. Wo kal ki sehat batata hai, saal bhar ki audit nahi.

## Lab: Inspector ko Service Dikhao

Lab. rooms-service mein /metrics jodo, aur truck chalao. prometheus.yml:

Dono ko ek hi Docker network par chalao, jaise Session 21 mein (Mac par port 5000 AirPlay ke paas hota hai, to -p 5050:5000 aur curl localhost:5050): docker run -d --name prom --network appnet -p 9090:9090 -v "PWD/prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus. UI mein Status, Targets dekho aur dono UP hone chahiye. Ek chhota loop for i in (seq 200); do curl -s localhost:5000/ >/dev/null; done chalao aur rate(http_requests_total[1m]) ka graph dekho. Phir truck band karo aur dekho ki up zero ho jaata hai. Safai: docker rm -f prom.

## Recap aur Bridge

Recap: pull model, exporter, metric ke types, aur PromQL. Ab Kubernetes ke liye poora control room ek franchise kit se.

---

# EPISODE 3: Franchise Kit aur Screens

## Poora Control Room, Ek Command

Kubernetes cluster ko monitor karne ke liye Prometheus, Alertmanager, Grafana, node exporter aur kube-state-metrics, sab chahiye. Haath se lagana ek din ka kaam hai, aur ek bhi jagah galti ho to adhura. Helm mein ek community franchise kit hai, kube-prometheus-stack, jo ye sab ek command mein lagata hai, Session 25 ke Helm ka seedha upyog. Atithi ke har wing aur har cluster mein wahi control room chale, ek jaisa.

## kube-prometheus-stack ke Hisse

Kit mein Prometheus Operator hota hai, jo Kubernetes ke objects se Prometheus ko chalata hai. ServiceMonitor aur PodMonitor naye objects hain jinse aap batate ho ki kaun si service ya pod scrape karni hai, bina prometheus.yml ko haath se badle. PrometheusRule se alerts. node exporter har building par, aur kube-state-metrics jo Kubernetes ke objects ke numbers deta hai: kitne pods Ready, kitne Pending. Grafana mein cluster ke liye pehle se bane dashboards aate hain. Production mein values file se retention aur storage tay karo, kyunki default mein Prometheus ka data emptyDir par hota hai, PVC tabhi banti hai jab storageSpec do, aur default admin password turant badlo.

## ServiceMonitor ka Jaal

ServiceMonitor banate waqt ek chhota jaal hai. Aap ek ServiceMonitor likhte ho, selector mein app: rooms, endpoint mein port ka naam aur /metrics, aur Prometheus ke Targets page par rooms dikhta hi nahi. Wajah: Operator sirf un monitors ko uthata hai jinke paas chart ka tay kiya hua label ho, aksar release: monitoring. Aur ye bhi dhyaan rakho ki ServiceMonitor ka selector Service ke labels dekhta hai, pod ke nahi, aur port ka naam Service mein bhi likha hona chahiye. Session 23 ka wahi label aur selector wala sabak: ek akshar ka farq aur chupchap khaali. Pehle Targets page dekho, phir labels.

## Grafana: Panel, Variable aur Dashboard

Grafana mein Prometheus data source hota hai. Panel mein ek PromQL query aur ek visualization: time series, stat, gauge, table. Variables se dashboard dynamic banta hai: dropdown se namespace ya pod chuno aur saare panels badal jaate hain. Achha dashboard ek kahani batata hai. Upar golden signals: request rate, error percent, latency, saturation. Neeche detail, jaise pod-wise CPU. Zyada panels mat daalo, kyunki raat ke do baje jab koi dekhta hai, to usse jaldi samajh aana chahiye ki guests ko dikkat hai ya nahi. Aur dashboard ko JSON ya ConfigMap mein save karo, taaki wo vault mein rahe, review ho, aur cluster dobara bane to wapas aa jaaye.

## Guest ki Nazar se: Blackbox Probe

Ab tak hum andar se dekh rahe the. Ho sakta hai ki saari trucks up = 1 dikhayen, aur phir bhi guest ko page na khule: certificate expire ho gaya, ya Ingress ka rule galat ho gaya, ya DNS toot gaya. Isliye bahar se bhi dekho. Blackbox exporter inspector ki taraf se ek probe chalata hai: public URL par HTTPS call, jawab ka code, kitna samay laga, aur certificate kitne din mein expire hoga. Alert: "certificate das din mein expire" ek ticket hai, aur "public page fail" ek page. Ye Session 11 ke marshal ke health check ka bahar wala bhai hai, aur wahi sawal: guest ko kya dikhta hai? Ek aur tareeka hai guest ki nazar ka: ek bahar ki cloud ya doosri region se probe lagao, taaki ek hi jagah ka outage dono ko ek saath na chhupa le.

## Lab: Cluster ko Dekho aur Apna Panel Banao

Lab. helm repo add prometheus-community https://prometheus-community.github.io/helm-charts, phir helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace. Pods Running hone mein kuch minute lagte hain. Phir kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80, browser mein localhost:3000, aur admin password Secret se nikalo: kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode. Chart ke naye versions install ke baad apna command bhi print karte hain, use dekh lo. Built-in dashboards kholo. Ab rooms-service ke liye ServiceMonitor lagao, label release: monitoring ke saath, aur Targets page par uska UP hona dekho. Dhyaan: label ke bina target aata hi nahi, aur label lagane ke baad bhi operator ko config reload karne mein aksar ek do minute lagte hain; humare lab mein chhappan second lage, to turant na ghabrao. Ek aur baat: Prometheus ka job label Service ke naam se banta hai, isliye alert ke job="rooms" ke liye Service ka naam rooms hona chahiye, warna query mein apna Service ka naam likho. Aur agar service gunicorn ke kai workers par chalti hai, to har worker ke apne counters hote hain; seedhe lab ke liye ek worker rakho, ya prometheus_client ka multiprocess mode docs se padho. Ek apna panel banao: sum by (status)(rate(http_requests_total{namespace="atithi"}[5m])). Aakhir mein stack hatao: helm uninstall monitoring -n monitoring. Default install mein PVC hoti hi nahi. storageSpec ke saath PVC banti hai, aur wo uninstall ke baad bhi bachi rehti hai, aur CRDs bhi, to unhe haath se hatao.

## Recap aur Bridge

Recap: franchise kit aur screens. Ab ek kadwi sachchai: deewar ki screens ko raat ko koi nahi dekhta. Alarm desk chahiye.

---

# EPISODE 4: Alarm Desk

## Do Sau Alert, Ek Raat

Do sau alerts roz raat, aur ek mahine baad aap phone silent kar dete ho. Duty manager ka phone raat bhar bajta hai, to wo uthana band kar deta hai. Phir ek asli alert aata hai aur koi nahi dekhta. Ye alert fatigue hai, aur monitoring ka sabse bada dushman. Session 15 ke alarm ka wahi niyam yahan bhi: jis alert par koi kuch nahi karta, wo shor hai. Achha alert kam hota hai, zaroori hota hai, aur uske saath runbook hota hai: phone ke bagal ki likhi procedure.

## Achhe Alert ke Niyam

Niyam. Symptom par alert do, kaaran par nahi. "Guests ko errors dikh rahe hain" ya "booking ka SLO jal raha hai" page-worthy hai. "CPU 80 percent" aksar nahi, kyunki ho sakta hai koi guest ko asar hi na ho. Har alert actionable ho: koi kuch kar sake. Severity tay karo: page jo raat ko jagaaye, aur ticket jo din mein dekha jaaye. for: duration lagao, taaki ek second ke spike par alert na aaye. Aur har alert ke saath ek runbook ka link, jisme likha ho pehle kya check karna hai. Is se naya duty manager bhi, jo us raat pehli baar aaya hai, kaam shuru kar sakta hai.

## Alert Rule aur Alertmanager

Prometheus rule mein ek expression hoti hai, jaise "5xx ratio 5 percent se upar", ek for: 5m, labels aur annotations. Condition sahi hote hi alert Pending hota hai, aur for ke baad Firing, aur wo Alertmanager ke paas jaata hai. Alarm desk teen kaam karta hai. Group: sau pods ke sau alerts ek message mein. Route: label ke hisaab se sahi jagah, jaise severity: page on-call tool ko, aur ticket chat channel ko. Inhibit: jab poori building gir gayi ho, to us par chalne wale pods ke alerts band. Aur silence: maintenance ke dauran ek tay samay ke liye band. Ek alert jo na kisi ko jagata hai na kuch kehta hai, use delete kar do.

## Dead Man's Switch aur SLO Burn

Ek chhupa sawaal: agar alarm desk hi gir jaaye, to kaun batayega? Isliye ek watchdog alert hota hai jo hamesha fire karta hai, aur jab wo aana band ho jaaye to ek bahar ka service shor machata hai. Kit mein ye pehle se hota hai. Aur ek behtar tareeka SLO par alert: burn rate. Maan lo error budget tees din ka hai. Agar pichhle ek ghante mein budget bahut tez jal raha hai, to ye page hai. Agar dheere, par chhe ghante se lagataar, to ye ticket. Isse chhoti spike par raat ko nahi jaagna padta, par lambi dheemi dikkat bhi nahi chhootti. Ye Session 15 ke "kitni readings ke liye" wale alarm ka samajhdar roop hai.

## Lab: Alert Jalao

Lab. Ek PrometheusRule likho, label release: monitoring ke saath. Lab cluster par kind mein control-plane ke kuch default alerts, jaise etcdInsufficientMembers ya TargetDown, bhi bajte hain, kyunki wo components bahar se scrape nahi hote. Ye shor hai, asli problem nahi, aur ye hi Session ke shuru wali alert-noise ki baat hai. Apna alert Watchdog ke saath Alertmanager mein dikhna chahiye:

rooms-service ko jaan boojh kar tod do, jaise ek / route jo 500 de, aur curl ke loop se traffic do. Prometheus ke Alerts page par alert Pending se Firing hota dekho, aur Alertmanager UI mein bhi. Humne todne ke teen minute baad Pending aur paanch minute baad Firing dekha, kyunki rate ki paanch minute ki window bharni padti hai, aur rollback ke baad bhi lagbhag paanch minute tak Firing raha. Phir ek chhota runbook likho: pehla kya dekhna hai, kaise rollback karna hai, Session 24 ke rollout undo ke saath. Aakhir mein Alertmanager mein ek silence lagao aur dekho ki alert chup ho gaya.

## Raat ke Baad: Seekh, Dosh nahi

Alert ne jagaya, duty manager ne rollback kiya, aur site wapas. Kaam khatam? Nahi. Agle din ek chhoti review likho. Guests ne kya dekha, kab se kab tak. Humne kya kiya. Kyun hua. Aur hum kya badlenge: ek alert, ek test, ek runbook ka hissa. Review mein koi naam nahi liya jaata, kyunki sawal "kisne galti ki" nahi, "system ne ye galti hone kyun di" hai. Isse error budget bhi samajh aata hai, aur wahi budget agle release ka faisla bhi karta hai. Aur ek aadat: har incident ke baad ek alert ya dashboard mein ek sudhaar, taaki wahi raat dobara na aaye. Monitoring tab tak poori nahi hoti jab tak wo har raat ke baad thodi behtar na ho.

## Recap aur Bridge

Recap: control room ka poora chakra: dekho, naapo, alert karo. Ab ek aur kaam: ab tak Atithi ki buildings, wings aur campus haath se, console mein click karke bane. Wahi problem, jo is poore course ki shuruaat mein thi: "staging production jaisa kyun nahi?" Agle session mein campus ka master plan document likhenge, aur ek contractor use bana dega: Terraform.
