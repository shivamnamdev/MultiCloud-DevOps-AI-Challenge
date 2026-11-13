# ✍️ 02: SCRIPT — SESSION-32: AI Apps & MLOps on Cloud
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S32`
- **Focus:** Calling an LLM API safely from an app, serving it behind a service, packaging and deploying on Kubernetes (EKS), model serving with FastAPI, the MLOps lifecycle, monitoring and drift
- **Episodes:**
  - Episode 1: LLM API ko App mein Jodna: Design aur Safety
  - Episode 2: AI Service ko Deploy Karna: Container, Secrets, Cost Control
  - Episode 3: MLOps ka Chakra: Train, Package, Serve
  - Episode 4: Model ko EKS par Chalana aur Monitor Karna

---

# 📺 EPISODE 1: LLM API ko App mein Jodna

### [00:00 – 01:15] Scene 1: Demo Chalta Hai, Product Nahi
**[VISUAL: A notebook demo calling an LLM gets a nice reply. Then production issues pile up: rate-limit errors, a 60-second timeout, a huge bill, the API key leaked in a repo.]**

**(Voiceover):**
Notebook mein LLM ka demo bahut aasaan hai: ek call, ek jawab. Lekin production mein sawal alag hote hain. API fail ho to? Rate limit lage to? Bill achanak badh jaye to? Key leak ho jaye to? DevOps engineer ka kaam AI ko demo se product banana hai, aur isi mein hum kaam aate hain.

### [01:15 – 05:00] Scene 2: LLM API ka Pattern
**[VISUAL: A request flow: Client → your API (auth, validation) → LLM provider API (prompt + params) → response → your API (filter, log) → client. A "never call the provider from the browser" warning.]**

**(Voiceover):**
LLM API ka pattern simple hai: aap prompt bhejte ho, parameters jaise model aur max tokens ke saath, aur text jawab milta hai. Ek rule: client ya browser se seedha provider ko mat bulao, kyunki key khul jaati hai. Aapki apni backend service beech mein rahe: wo user ko authenticate kare, input check kare, prompt banaye, provider ko bulaye, aur jawab filter karke wapas de. Token ka matlab text ka chhota tukda, aur bill input aur output tokens par chalta hai.

### [05:00 – 08:30] Scene 3: Reliability aur Safety Patterns
**[VISUAL: A checklist: timeouts, retries with backoff for 429/5xx, max tokens, cache repeated prompts, per-user rate limits, input size limits, log metadata not secrets, prompt injection awareness, human review for risky actions.]**

**(Voiceover):**
Reliability ke patterns. Timeout lagao. 429 aur 5xx par retry with backoff, par 4xx galat request par nahi. `max_tokens` se jawab ki seema aur cost control. Same prompt ka jawab cache karo. Har user par rate limit. Safety ke patterns: user ka input ek untrusted cheez hai, aur prompt injection ek asli khatra hai: user text mein chhupi instruction model ko behka sakti hai. To model ko jo tools ya permissions do, wo kam rakho, aur khatarnaak action par insaan ki manzoori. Logs mein metadata rakho, sensitive data nahi.

### [08:30 – 11:30] Scene 4: Lab: Chhota AI Service
**[VISUAL: A FastAPI endpoint `POST /summarize` that validates input length, calls an LLM SDK with timeout and `max_tokens`, handles exceptions, and returns JSON. The API key is read from an environment variable.]**

**(Voiceover):**
Lab: FastAPI service jo text summarize kare. Provider ka official SDK use karo, model ka naam environment variable `MODEL_NAME` se, aur key `API_KEY` se, code mein nahi.
```python
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Req(BaseModel):
    text: str = Field(min_length=1, max_length=8000)

def call_llm(prompt: str) -> str:
    # Use your provider's official SDK here. Read MODEL_NAME and the API key from env.
    # Set a client timeout and max_tokens. Return the text of the reply.
    raise NotImplementedError

@app.post("/summarize")
def summarize(req: Req):
    try:
        return {"summary": call_llm(f"Summarize in 3 bullets:\n\n{req.text}")}
    except TimeoutError:
        raise HTTPException(504, "model timeout")
```
`call_llm` mein apne provider ke docs se call jodo. Input length ki seema, timeout aur error mapping dekho, ye hi production ke asli hisse hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "backend proxy · timeouts + retries · max_tokens · rate limits · injection-aware".]**

**(Voiceover):**
Recap: LLM ko surakshit tareeke se app mein jodna. Ab is service ko cloud par chalana: container, secrets aur cost control.

---

# 📺 EPISODE 2: AI Service ko Deploy Karna

### [00:00 – 01:15] Scene 1: Ek Raat mein Bill Chadh Gaya
**[VISUAL: A script bug loops LLM calls overnight. A billing chart spikes. An alert fires too late. A budget cap prevents a repeat.]**

**(Voiceover):**
Ek bug se loop mein LLM calls chalti rahi, aur subah ka bill chaunka gaya. AI services mein cost ek reliability problem hai, kyunki har call ka paisa lagta hai. Is episode mein hum service ko container mein daalenge, secrets surakshit rakhenge, aur cost par control lagayenge.

### [01:15 – 05:00] Scene 2: Container aur Secrets
**[VISUAL: A Dockerfile for the FastAPI service with uvicorn, non-root. A Kubernetes Secret (or external secrets manager) injecting `API_KEY` as an env var. A diagram: Secret Manager → External Secrets/CSI → Pod.]**

**(Voiceover):**
Service ko Docker image mein pack karo, wahi aadatein: slim base, non-root, `CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]`. API key ko Kubernetes Secret ya, behtar, cloud secret manager se pod mein environment variable ke roop mein do. Image mein kabhi key mat daalo. CI/CD pipeline mein secret scan lagao, jo humne DevSecOps session mein dekha, taaki koi galti se key commit na kar de. Aur key ko rotate karne ka plan rakho.

### [05:00 – 08:30] Scene 3: Cost aur Reliability Guardrails
**[VISUAL: A control panel: provider-side budget/limits, per-user and global rate limits, `max_tokens`, cache, request-size limits, a circuit breaker, alerts on tokens/day. A dashboard panel for "tokens per hour".]**

**(Voiceover):**
Cost guardrails. Provider ke console mein budget aur usage limits lagao. Apni service mein user aur global rate limits, `max_tokens`, aur request size ki seema. Cache se dohraye prompts par paisa bachta hai. Circuit breaker se provider fail hone par service baar baar uske peeche nahi bhagti. Aur metrics: tokens per hour, requests, errors, latency, jinhe Prometheus aur Grafana mein dikhao, aur tokens ke spike par alert lagao. Ye sab usi observability ki kahani hai jo humne pichhle sessions mein seekhi.

### [08:30 – 11:30] Scene 4: Lab: Metrics aur Rate Limit
**[VISUAL: The FastAPI app exposes `/metrics` using `prometheus-client` with counters `llm_requests_total` and `llm_tokens_total`. A simple in-memory per-IP rate limiter returns 429. A Grafana panel shows request rate.]**

**(Voiceover):**
Lab: apni service mein `prometheus-client` jodo: `from prometheus_client import Counter, make_asgi_app`, ek counter `llm_requests_total`, aur `app.mount("/metrics", make_asgi_app())`. Ek simple rate limit likho jo ek IP se ek minute mein, jaise 10 se zyada requests par 429 de. Local Prometheus ke `prometheus.yml` mein is service ko scrape karo, aur `rate(llm_requests_total[1m])` ka graph dekho. Test ke liye provider ki jagah ek fake `call_llm` use karo, taaki lab mein paisa na lage.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "image + secrets from manager · budgets · rate limits · metrics on tokens · fake LLM in tests".]**

**(Voiceover):**
Recap: AI service ko surakshit aur sasta chalana. Ab dusra roop: apna khud ka ML model, aur MLOps.

---

# 📺 EPISODE 3: MLOps ka Chakra

### [00:00 – 01:15] Scene 1: Model Notebook Mein, Production Mein Nahi
**[VISUAL: A data scientist's notebook with a great accuracy score. A question mark between the notebook and "production". A pipeline icon fills the gap.]**

**(Voiceover):**
Data scientist ka model notebook mein 95% accuracy deta hai. Lekin us notebook ko production service banana alag kaam hai. MLOps wo practice hai jo ML models ko DevOps ki tarah reliable tareeke se train, package, deploy aur monitor karta hai. Aur seedhi baat: model sirf ek file hai, aur use serve karne wali service ek normal service hai.

### [01:15 – 05:00] Scene 2: MLOps Lifecycle
**[VISUAL: A loop: Data → Train → Evaluate → Register (versioned model + metrics) → Package → Deploy → Serve → Monitor (latency, errors, data drift, accuracy) → Retrain. Tools: MLflow/DVC, Docker, Kubernetes.]**

**(Voiceover):**
Lifecycle ek loop hai. Data ikattha aur saaf. Train aur evaluate. Model ko versioned register karo, uske metrics aur use bane data ke saath, taaki baad mein reproduce ho sake. Package, yaani container. Deploy. Serve, yaani API. Monitor: sirf latency aur errors nahi, balki data drift bhi, yaani production ka data training data se alag hone lage. Aur jab model bigde, to retrain. Tools jaise MLflow aur DVC experiments aur data ka version rakhte hain.

### [05:00 – 08:30] Scene 3: Reproducibility aur Model Versioning
**[VISUAL: A training run record: code commit, data version hash, parameters, metrics, model artifact stored with a version tag `model-v3`. A promotion flow: staging → production after evaluation.]**

**(Voiceover):**
Ek hi cheez jo ML ko normal software se alag banati hai: result sirf code par nahi, data par bhi nirbhar karta hai. Isliye training ke saath code ka commit, data ka version, parameters aur metrics sab record karo. Model artifact ko version do, jaise `model-v3`, aur pehle staging par jaanch, phir production. Evaluation ek automatic gate hai: naya model purane se behtar na ho to promote nahi hoga. Ye wahi CI/CD ka idea hai, bas model ke liye.

### [08:30 – 11:30] Scene 4: Lab: Model Train Karo aur Save Karo
**[VISUAL: A Python script training a small scikit-learn classifier on the Iris dataset, printing accuracy, saving `model.joblib` with metadata JSON (version, accuracy, data hash). A GitHub Actions job that fails if accuracy < 0.9.]**

**(Voiceover):**
Lab: ek chhota model train karo:
```python
import json, joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42).fit(Xtr, ytr)
acc = accuracy_score(yte, model.predict(Xte))
joblib.dump(model, "model.joblib")
json.dump({"version": "v1", "accuracy": acc}, open("model.json", "w"))
print("accuracy", acc)
assert acc >= 0.9, "model below quality gate"
```
`assert` quality gate hai. Isse CI mein chalao, aur dekho ki accuracy girne par pipeline fail hoti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "train → register → package → serve → monitor · version code + data + model · quality gate".]**

**(Voiceover):**
Recap: MLOps lifecycle aur model versioning. Ab model ko serve karna, aur use EKS par chalana.

---

# 📺 EPISODE 4: Model ko EKS par Chalana aur Monitor Karna

### [00:00 – 01:15] Scene 1: Model ek Normal Service Hai
**[VISUAL: A FastAPI service wrapping `model.joblib` at `/predict`. A container icon, then EKS pods, then an ALB, then a monitoring dashboard.]**

**(Voiceover):**
Model serving ka matlab: ek HTTP API jo input leta hai aur prediction deti hai. Wo ek normal service hai, to uske liye wahi Docker, Kubernetes, health checks, autoscaling aur monitoring, jo humne seekha. Aaj hum model ko FastAPI mein serve karenge, aur AWS ke EKS cluster par chalayenge.

### [01:15 – 05:00] Scene 2: FastAPI Model Server
**[VISUAL: `app.py` loading the model at startup, `/predict` with pydantic input validation, `/health`, and `/metrics`. A Dockerfile copying `model.joblib`.]**

**(Voiceover):**
Model ko startup par ek baar load karo, har request par nahi. Input ko pydantic se validate karo.
```python
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, conlist

app = FastAPI()
model = joblib.load("model.joblib")

class Features(BaseModel):
    values: conlist(float, min_length=4, max_length=4)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(f: Features):
    return {"class": int(model.predict([f.values])[0])}
```
`/health` Kubernetes probes ke liye. Dockerfile mein model file image ke andar, ya bade models ke liye registry se startup par download.

### [05:00 – 08:30] Scene 3: EKS aur Autoscaling
**[VISUAL: `eksctl create cluster`, `kubectl apply`, a Service + Ingress/ALB. HPA on CPU. A note: GPU node group for deep learning models; cost banner.]**

**(Voiceover):**
EKS AWS ka managed Kubernetes hai. Seekhne ke liye `eksctl create cluster --name ml-demo --region YOUR_REGION --nodes 2` kaafi hai, aur ye kuch minute leta hai aur paisa bhi. Image ko ECR mein push karo, Deployment mein readiness probe `/health` par, resource requests aur limits, aur Service. Bahar ke liye Service type LoadBalancer ya ALB Ingress. CPU par HPA. Deep learning models ke liye GPU node group chahiye, jo bahut mehenga hota hai, to chhote experiments se shuruaat. Aur cluster ke saath saath sab resources ki safai.

### [08:30 – 11:30] Scene 4: Lab: Serve, Deploy aur Drift Socho
**[VISUAL: Build and run locally, `curl -X POST /predict -d '{"values":[5.1,3.5,1.4,0.2]}'`. Push to ECR. Deploy to EKS. Grafana shows request rate and latency. A histogram of feature values in production vs training shows drift.]**

**(Voiceover):**
Lab: model server ko local Docker mein chalao aur `curl -X POST localhost:8000/predict -H 'content-type: application/json' -d '{"values":[5.1,3.5,1.4,0.2]}'` se test. Phir ECR par push, EKS par Deployment, Service aur HPA. `prometheus-fastapi-instrumentator` jaisi library se latency aur request metrics lo. Drift ka experiment: production ke inputs ka mean aur training ka mean compare karo. Agar kisi feature ka mean bahut khisak jaye, to alert, aur retrain ki soch. Lab ke ant mein `eksctl delete cluster --name ml-demo --region YOUR_REGION` chalao aur confirm karo ki sab hat gaya.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "load once · validate input · probes · ECR + EKS · metrics + drift · delete cluster".]**

**(Voiceover):**
Recap: AI apps aur ML models ko production mein chalana, DevOps ke tareeke se. Ab aakhri session: AI aur operations ka milan. AIOps, aur apna MCP server, jahan AI sach mein tools ko chalata hai.
