# ✍️ 02: SCRIPT — SESSION-26: Prometheus & Grafana
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S26`
- **Focus:** Observability pillars & golden signals, Prometheus pull model, PromQL, kube-prometheus-stack via Helm, Grafana dashboards, alerting
- **Episodes:**
  - Episode 1: Observability: Metrics, Logs, Traces aur Golden Signals
  - Episode 2: Prometheus: Pull Model aur PromQL
  - Episode 3: Helm se Monitoring Stack aur Grafana Dashboard
  - Episode 4: Alerts: Alertmanager aur Runbook

---

# 📺 EPISODE 1: Observability aur Golden Signals

### [00:00 – 01:15] Scene 1: Gaadi ka Dashboard
**[VISUAL: A car dashboard with speed, fuel, temperature, and a warning light. Next, a car with no dashboard rolling to a stop on a highway.]**

**(Voiceover):**
Gaadi chalate waqt dashboard aapko speed, tel aur engine ka temperature batata hai, aur warning light pehle se chetavani deti hai. Bina dashboard ke gaadi achanak rukti hai. Software mein bhi yahi hai. Observability ka matlab hai ki aap system ke bahar ke signals dekhkar andar ki halat samajh sakein.

### [01:15 – 05:00] Scene 2: Teen Pillars
**[VISUAL: Three pillars: Metrics (numbers over time), Logs (event records), Traces (a request's journey across services). Each with an example question it answers.]**

**(Voiceover):**
Teen pillars. Metrics numbers hain jo samay ke saath badalte hain, jaise requests per second. Wo batate hain "kya ho raha hai". Logs ghatnaon ke record hain, jo batate hain "kyun". Traces ek request ka poora safar dikhate hain kai services ke beech, jo batate hain "kahan dheema hua". Is session mein hum metrics par dhyaan denge, jisme Prometheus aur Grafana sabse popular jodi hai. Logs aur traces ke tools, jaise Loki aur OpenTelemetry, aage ki padhai hain.

### [05:00 – 08:30] Scene 3: Golden Signals aur RED/USE
**[VISUAL: Four gauges: Latency, Traffic, Errors, Saturation. Beneath: RED (Rate, Errors, Duration) for services; USE (Utilization, Saturation, Errors) for resources.]**

**(Voiceover):**
Kya naapein? Google ke SRE ne chaar golden signals batayen. Latency: request kitni der leti hai. Traffic: kitni requests aa rahi hain. Errors: kitni fail ho rahi hain. Aur saturation: system kitna bhara hua hai. Services ke liye RED yaad rakho: Rate, Errors, Duration. Machines ke liye USE: Utilization, Saturation, Errors. Ye chaar signals aapko 80% problems ke liye kaafi hain, aur har dashboard inhi se shuru hona chahiye.

### [08:30 – 11:30] Scene 4: Lab: Apna SLI Socho
**[VISUAL: A worksheet for the `catalog` service: "Success rate = good requests / total", "Latency: 95% under 300 ms". A sample SLO: "99% success over 30 days".]**

**(Voiceover):**
Lab (paper): apni Mini Shop ki catalog service ke liye teen cheezein likho. SLI, yaani measure: successful requests ka percent, aur 95th percentile latency. SLO, yaani target: "30 din mein 99% requests successful, aur 95% 300 ms se kam." Aur error budget: 1% jitni galtiyon ki chhoot. Ye target tay karne se team ko pata hota hai ki kab release rokna hai aur kab tez chalna hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "metrics = what · logs = why · traces = where · golden signals · SLI/SLO".]**

**(Voiceover):**
Recap: observability, golden signals, SLO. Ab hands-on: Prometheus.

---

# 📺 EPISODE 2: Prometheus — Pull Model aur PromQL

### [00:00 – 01:15] Scene 1: Prometheus Poochhta Hai
**[VISUAL: A Prometheus server asking apps "give me your numbers" every 15 seconds via HTTP `/metrics`, and storing them in a time-series database.]**

**(Voiceover):**
Prometheus ka tareeka alag hai. Apps apne numbers Prometheus ko bhejte nahi. Prometheus khud har kuch second mein apps ke paas jaakar poochta hai: "tumhare numbers do." Isse pull model kehte hain. Isse pata bhi chal jaata hai ki app zinda hai ya nahi: agar jawab na mile, to wo down hai.

### [01:15 – 05:00] Scene 2: Architecture aur Metric Types
**[VISUAL: Components: Prometheus server (scrape + TSDB + PromQL), exporters (node_exporter), app `/metrics`, service discovery, Alertmanager, Grafana. Metric types: Counter, Gauge, Histogram.]**

**(Voiceover):**
Prometheus server targets ko scrape karta hai aur time-series database mein rakhta hai. Targets ke paas `/metrics` endpoint hota hai. Exporters un cheezon ke liye hain jo khud metrics nahi dete, jaise node exporter machine ke CPU aur memory ke liye. Kubernetes mein service discovery se targets apne aap milte hain. Metric ke type: counter, jo sirf badhta hai, jaise total requests. Gauge, jo upar neeche hota hai, jaise memory. Histogram, jisse latency ke percentiles nikalte hain. Labels metrics ko dimension dete hain, jaise `method="GET"`.

### [05:00 – 08:30] Scene 3: PromQL ki Basics
**[VISUAL: Queries and results: `up`, `rate(http_requests_total[5m])`, `sum by (status)(rate(http_requests_total[5m]))`, `histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket[5m])))`.]**

**(Voiceover):**
PromQL Prometheus ki query language hai. `up` batata hai kaun se targets zinda hain. Counter ko seedha nahi dekhte, uski rate dekhte hain: `rate(http_requests_total[5m])` pichle paanch minute mein per second requests. `sum by (status)(...)` unhe status ke hisaab se jodta hai. Error ratio ke liye 5xx ki rate ko total rate se divide karo. Aur latency ke liye `histogram_quantile(0.95, ...)`. Ek aam galti: counter ko bina `rate` ke plot karna, jo sirf ek badhti hui line dikhata hai.

### [08:30 – 11:30] Scene 4: Lab: Prometheus Local Chalao
**[VISUAL: A `prometheus.yml` scraping `localhost:9090` and `node_exporter:9100`. `docker run -p 9090:9090 -v ... prom/prometheus`. The UI shows targets UP; a query on `node_cpu_seconds_total` rate.]**

**(Voiceover):**
Lab: Docker se Prometheus chalao. `prometheus.yml`:
```yaml
global: { scrape_interval: 15s }
scrape_configs:
  - job_name: prometheus
    static_configs: [{ targets: ['localhost:9090'] }]
  - job_name: node
    static_configs: [{ targets: ['host.docker.internal:9100'] }]
```
Node exporter ko bhi ek container ya binary se chalao. `docker run -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus`. UI mein Status, Targets dekho aur query chalao: `up`, aur `rate(node_cpu_seconds_total{mode!="idle"}[1m])`. Linux par host networking ke options alag hote hain, jo docs mein dekh sakte ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "pull /metrics · counter/gauge/histogram · rate() · labels".]**

**(Voiceover):**
Recap: Prometheus aur PromQL. Ab Kubernetes mein poora monitoring stack ek hi command mein, aur Grafana par sundar dashboards.

---

# 📺 EPISODE 3: Helm se Monitoring Stack aur Grafana Dashboard

### [00:00 – 01:15] Scene 1: Poora Stack, Ek Command
**[VISUAL: A helm install command and a flurry of pods starting: prometheus, alertmanager, grafana, node-exporter, kube-state-metrics.]**

**(Voiceover):**
Kubernetes cluster ko monitor karne ke liye Prometheus, Alertmanager, Grafana, node exporter aur kube-state-metrics sab chahiye. Haath se lagana ek din ka kaam hai. Helm mein ek community chart, `kube-prometheus-stack`, ye sab ek command mein laga deta hai.

### [01:15 – 05:00] Scene 2: kube-prometheus-stack
**[VISUAL: `helm repo add prometheus-community ...`, `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`. A components diagram: Prometheus Operator, ServiceMonitor/PodMonitor CRDs, Grafana with pre-built dashboards.]**

**(Voiceover):**
Chart ka naam `kube-prometheus-stack`. Isme Prometheus Operator hota hai, jo Prometheus ko Kubernetes ke objects se chalata hai. ServiceMonitor aur PodMonitor naye objects hain jinse aap batate ho ki kaun si service scrape karni hai. Grafana mein cluster ke liye pehle se bane dashboards aate hain: nodes, pods, namespaces. Production mein values file se retention, storage aur passwords set karte hain, aur default admin password ko turant badalna chahiye.

### [05:00 – 08:30] Scene 3: Grafana: Data Source, Panel, Dashboard
**[VISUAL: Grafana UI. Data source Prometheus. A new dashboard with panels: Time series (request rate), Stat (error %), Gauge (CPU), Table. Variables `namespace`, `pod` as dropdowns.]**

**(Voiceover):**
Grafana mein Prometheus data source hota hai. Panel mein ek PromQL query aur ek visualization: time series, stat, gauge, table. Variables se dashboard dynamic banta hai: dropdown se namespace ya pod chuno aur sab panels badal jaate hain. Achha dashboard ek kahani batata hai: upar golden signals, neeche detail. Zyada panels mat daalo. Dashboard ko JSON ya code mein save karo taaki Git mein rakh sako.

### [08:30 – 11:30] Scene 4: Lab: Cluster Monitor aur Apna Panel
**[VISUAL: Helm install, `kubectl get pods -n monitoring`, `kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring`, login, open "Kubernetes / Compute Resources / Namespace (Pods)". Create a panel with the query `sum(rate(container_cpu_usage_seconds_total{namespace="shop"}[5m])) by (pod)`.]**

**(Voiceover):**
Lab: `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`, phir `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`. Pods Running hone par `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80`. Browser mein `localhost:3000`, aur admin password chart ke docs ke hisaab se secret se nikalo. Built-in dashboards dekho, aur ek apna panel banao jo Mini Shop ke namespace ka pod-wise CPU dikhaye. Test ke baad cluster ya stack hata do, kyunki ye kaafi resources leta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "helm chart · ServiceMonitor · Grafana variables · dashboards as code".]**

**(Voiceover):**
Recap: stack aur dashboards. Ab asli kaam: dashboard roz koi nahi dekhta. Alert chahiye, jo aapko jagaye jab zaroori ho.

---

# 📺 EPISODE 4: Alerts — Alertmanager aur Runbook

### [00:00 – 01:15] Scene 1: Alert Fatigue
**[VISUAL: A phone buzzing 200 times a night with low-importance alerts. The engineer silences the phone. A real critical alert arrives and is missed.]**

**(Voiceover):**
Do sau alerts roz raat, aur ek mahine baad aap phone silent kar dete ho. Phir ek asli alert aata hai aur koi nahi dekhta. Ye alert fatigue hai, aur monitoring ka sabse bada dushman. Achha alert kam hota hai, zaroori hota hai, aur usme batata hai ki kya karna hai.

### [01:15 – 05:00] Scene 2: Achhe Alert ke Niyam
**[VISUAL: A checklist: Symptom over cause, actionable, with a severity, with a `for:` duration, linked runbook. Examples: page on "users see errors", ticket on "disk 80%".]**

**(Voiceover):**
Niyam. Symptom par alert do, kaaran par nahi: "users ko errors dikh rahe hain" page-worthy hai, "CPU 80%" aksar nahi. Har alert actionable ho: koi kuch kar sake. Severity tay karo: page jo raat ko jagaaye, aur ticket jo din mein dekha jaye. `for:` duration lagao, taaki ek second ke spike par alert na aaye. Aur har alert ke saath ek runbook ka link, jisme likha ho pehle kya check karna hai.

### [05:00 – 08:30] Scene 3: Alert Rule aur Alertmanager
**[VISUAL: A PrometheusRule YAML with expr, for, labels (severity), annotations (summary, runbook_url). Flow: Prometheus evaluates rule → firing → Alertmanager groups, deduplicates, routes to Slack/Email/PagerDuty; silences and inhibition.]**

**(Voiceover):**
Prometheus rule mein ek expression hoti hai, jaise "5xx ratio 5% se upar", ek `for: 5m`, labels aur annotations. Jab condition lagataar sahi rahe to alert firing ho jata hai aur Alertmanager ko jaata hai. Alertmanager alerts ko group karta hai, duplicate hatata hai, aur sahi jagah bhejta hai: Slack, email, ya on-call tool. Silence se maintenance mein alerts band kar sakte ho. Aur ek alert jo na kisi ko jagata hai na kuch kehta hai, use delete kar do.

### [08:30 – 11:30] Scene 4: Lab: Ek Alert Banao aur Chalao
**[VISUAL: A PrometheusRule `HighErrorRate` on `catalog` with `for: 2m`. A broken deployment causes 5xx; the alert appears in Prometheus (Pending → Firing) and in Alertmanager UI.]**

**(Voiceover):**
Lab: ek PrometheusRule likho jisme expression kuch aisi ho: `sum(rate(http_requests_total{job="catalog",status=~"5.."}[5m])) / sum(rate(http_requests_total{job="catalog"}[5m])) > 0.05`, `for: 2m`, label `severity: page`. Catalog service ko jaan-boojh kar tod do, jaise galat config se 500 dene wala version, aur Prometheus ke Alerts page par state Pending se Firing hoti dekho. Alertmanager UI mein alert dikhega. Phir ek runbook ka chhota page likho: pehle kya dekhna hai, kaise rollback karna hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "symptom-based · actionable · for: duration · routing · runbook link".]**

**(Voiceover):**
Recap: monitoring ka poora chakra: dekho, naapo, alert karo. Ab infrastructure ko bhi code mein likhne ka waqt: Terraform.
