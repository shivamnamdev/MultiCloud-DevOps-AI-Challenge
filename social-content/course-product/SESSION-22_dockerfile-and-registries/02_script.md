# ✍️ 02: SCRIPT — SESSION-22: Dockerfile & Registries
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S22`
- **Focus:** Dockerfile instructions, build context & cache, small/secure images (multi-stage, non-root), tagging, registries, CI build & push
- **Episodes:**
  - Episode 1: Dockerfile: App ka Nuskha
  - Episode 2: Build Cache aur .dockerignore: Tez Builds
  - Episode 3: Chhoti aur Surakshit Image: Multi-stage, Non-root
  - Episode 4: Tags, Registry aur CI mein Push

---

# 📺 EPISODE 1: Dockerfile — App ka Nuskha

### [00:00 – 01:15] Scene 1: Docker Hub par Image Nahi, Apni App
**[VISUAL: A small Flask app folder. A question mark over "How do I run this anywhere?" A Dockerfile appears and a container with the app starts.]**

**(Voiceover):**
Ab tak aapne dusron ki banayi images chalayi. Ab apni app ko pack karna hai. Iske liye Dockerfile hai: ek text file jisme likha hota hai ki image kaise banegi. Ye wahi nuskha hai jo kisi bhi machine par ek jaisi app deta hai.

### [01:15 – 05:00] Scene 2: Zaroori Instructions
**[VISUAL: A Dockerfile with each instruction highlighted: FROM, WORKDIR, COPY, RUN, ENV, EXPOSE, CMD/ENTRYPOINT. Side labels for build-time vs run-time.]**

**(Voiceover):**
`FROM` batata hai kis base image se shuru karna, jaise `python:3.12-slim`. `WORKDIR` andar ka kaam ka folder. `COPY` host ki files image mein. `RUN` build ke time par command chalata hai, jaise `pip install`. `ENV` environment variable. `EXPOSE` sirf documentation hai ki app kaun sa port sunti hai, wo port khud nahi kholta. `CMD` container start hone par default command. `ENTRYPOINT` ek fixed command, jisme CMD uske arguments ban sakte hain. Hamesha exec form, yaani JSON list `["python","app.py"]`, use karo, jisse signals sahi pahunchte hain.

### [05:00 – 08:30] Scene 3: Pehli Dockerfile
**[VISUAL: A sample app: `app.py` with Flask returning "Hello DevOps", `requirements.txt`, and the Dockerfile. Build and run output.]**

**(Voiceover):**
Ek chhoti Flask app ki Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```
`docker build -t hello:1.0 .` image banata hai, aur `docker run -d -p 5000:5000 hello:1.0` chalata hai. Dhyaan do ki Flask ko `host="0.0.0.0"` par sunna chahiye, nahi to container ke bahar se nahi dikhega.

### [08:30 – 11:30] Scene 4: Lab: Apni App ko Container Karo
**[VISUAL: Create `app.py` and `requirements.txt` (flask). Build, run, `curl localhost:5000`. Then show a wrong host binding (127.0.0.1) failing and the fix.]**

**(Voiceover):**
Lab: `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return "Hello DevOps"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
`requirements.txt` mein `flask`. Upar wali Dockerfile se build karo aur `curl localhost:5000` se test. Ab `host` ko `127.0.0.1` kar do, dobara build karo, aur dekho ki bahar se connect nahi hota. Ye bahut aam galti hai, aur isse samajhna networking ka ek zaroori sabak hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "FROM · WORKDIR · COPY · RUN · CMD (exec form) · bind 0.0.0.0".]**

**(Voiceover):**
Recap: Dockerfile ke basic instructions. Ab ek sawaal: baar baar build karne par itna samay kyun lagta hai? Cache.

---

# 📺 EPISODE 2: Build Cache aur .dockerignore

### [00:00 – 01:15] Scene 1: Ek Line Badli, Poora Build Dobara
**[VISUAL: A developer changes one line of code. The build log shows "pip install" running again for 3 minutes. Frustration.]**

**(Voiceover):**
Aapne sirf ek line code badli, aur Docker ne dobara saare packages install kar diye, teen minute lage. Ye Dockerfile ke order ki galti hai. Layers ka cache samajh gaye to aap builds ko seconds mein la sakte ho.

### [01:15 – 05:00] Scene 2: Cache ka Niyam
**[VISUAL: Two Dockerfiles. Bad: `COPY . .` then `RUN pip install`. Good: `COPY requirements.txt .` then `RUN pip install` then `COPY . .`. A cache indicator "CACHED" appears on the good one's install step.]**

**(Voiceover):**
Niyam: Docker har instruction ek layer banata hai, aur agar us instruction ya uske input files nahi badle, to cache se uthata hai. Lekin ek layer badli to uske baad ki saari layers dobara banti hain. Isliye jo cheez kam badalti hai, jaise dependencies, use pehle rakho, aur jo roz badalti hai, jaise aapka code, use baad mein. Pehle `requirements.txt` copy karke install, aur uske baad `COPY . .`. Ab code badalne par install wali layer CACHED rahegi.

### [05:00 – 08:30] Scene 3: .dockerignore aur Build Context
**[VISUAL: A folder with `.git`, `node_modules`, `.env`, `__pycache__`. A `.dockerignore` listing them. A "Sending build context: 1.2GB → 12KB" message.]**

**(Voiceover):**
`docker build .` ka dot build context hai, yaani jo folder Docker ko bhejta hai. Agar usme `.git`, `node_modules`, ya bade datasets hain, to wo sab daemon ko bhejta hai, build dheema hota hai. `.dockerignore` file mein inhe likho. Aur ek bahut zaroori baat: `.env` aur secret files ko kabhi image mein mat jaane do. Image ke layers mein ek baar gaya hua secret baad mein hata dene par bhi history mein reh sakta hai. Isliye `.dockerignore` mein `.env`, aur build-time secrets ke liye BuildKit ke secret mount jaise surakshit tareeke use karo.

### [08:30 – 11:30] Scene 4: Lab: Build Time Naapo
**[VISUAL: Terminal: `time docker build -t hello:1.0 .` (cold), change `app.py`, build again (fast with CACHED lines). Reorder the Dockerfile to the bad version and rebuild to see the difference.]**

**(Voiceover):**
Lab: upar wali sahi Dockerfile ko `time docker build -t hello:cache .` se build karo. Phir `app.py` mein ek line badlo aur dobara build karo, install step par CACHED likha aayega aur build second mein khatam. Ab Dockerfile mein `COPY . .` ko install se pehle rakh do aur wahi karo, to install dobara chalega. Time ka farq note karo. `.dockerignore` mein `.git`, `__pycache__`, `.env` likho aur `docker build` ke context size ka farq dekho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "deps first, code last · CACHED · .dockerignore · no secrets in layers".]**

**(Voiceover):**
Recap: cache aur ignore. Ab image ko chhota aur surakshit banate hain.

---

# 📺 EPISODE 3: Chhoti aur Surakshit Image

### [00:00 – 01:15] Scene 1: 1.2 GB ki Hello World App
**[VISUAL: An image size bar: `python:3.12` full → 1.0 GB; `slim` → 150 MB; multi-stage with distroless/slim → 60 MB. A vulnerability scan count shrinking alongside.]**

**(Voiceover):**
Ek chhoti si app ki image 1.2 GB? Wo slow download, zyada storage, aur zyada vulnerabilities, yaani hamlon ke zyada raaste. Chhoti image tez, sasti aur surakshit hoti hai. Teen tareeke: chhota base, multi-stage build, aur non-root user.

### [01:15 – 05:00] Scene 2: Multi-stage Build
**[VISUAL: A Dockerfile with two stages: `FROM golang:1.22 AS build` compiling a binary, and `FROM gcr.io/distroless/static` or `alpine` copying only the binary with `COPY --from=build`. Size shrinks from 800MB to 15MB.]**

**(Voiceover):**
Multi-stage build mein pehle stage mein saare build tools hote hain, compiler aur dependencies. Dusre stage mein sirf wo cheez jo chalane ke liye chahiye. `COPY --from=build` se sirf binary ya built files le aate ho. Compiler aur tools final image mein nahi jaate, to image chhoti aur kam attack surface ke saath. Python ke liye bhi wahi idea: pehle stage mein packages build, dusre stage mein sirf installed packages aur code.

### [05:00 – 08:30] Scene 3: Non-root aur Base Image ke Choices
**[VISUAL: A Dockerfile with `RUN adduser ... && USER app`. A comparison of base images: full, slim, alpine, distroless. Notes: "alpine uses musl, may break some wheels", "pin the digest or version".]**

**(Voiceover):**
Container ko by default root se chalana khatarnaak hai. `RUN useradd -m app` aur `USER app` se non-root user par chalao, taaki agar app hack ho jaye to nuksaan kam ho. Base image mein slim aam taur par achha balance hai. Alpine bahut chhota hai par musl libc ki wajah se kabhi kabhi Python packages mein dikkat deta hai. Distroless mein shell tak nahi hota, jo security ke liye achha hai par debugging mushkil. Base image ko specific version par pin karo aur regularly update karo, aur Trivy se scan karo.

### [08:30 – 11:30] Scene 4: Lab: Multi-stage aur Non-root
**[VISUAL: A Python Dockerfile with a builder stage making wheels and a runtime stage installing from wheels with a non-root user. `docker images` shows sizes; `docker run --rm hello:slim id` prints uid=1000.]**

**(Voiceover):**
Lab:
```dockerfile
FROM python:3.12-slim AS build
WORKDIR /w
COPY requirements.txt .
RUN pip wheel --no-cache-dir -w /wheels -r requirements.txt

FROM python:3.12-slim
RUN useradd -m app
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels
COPY --chown=app:app . .
USER app
EXPOSE 5000
CMD ["python", "app.py"]
```
Build karo, `docker images` se size dekho, aur `docker run --rm hello:slim id` se confirm karo ki user root nahi hai. Agar Trivy install hai, to `trivy image hello:slim` chalao aur findings ki sankhya note karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "multi-stage · non-root · slim base · pin versions · scan".]**

**(Voiceover):**
Recap: chhoti aur surakshit image. Ab image ko share karna: tags, registry aur CI.

---

# 📺 EPISODE 4: Tags, Registry aur CI mein Push

### [00:00 – 01:15] Scene 1: Kaun Sa Version Production Mein Hai?
**[VISUAL: A production server runs `myapp:latest`. Nobody knows which commit it is. A bug appears; a team scrambles. Next: `myapp:1.4.2-a1b2c3d` clearly traceable.]**

**(Voiceover):**
Production mein `myapp:latest` chal raha hai, aur bug aaya. Ab kaun sa code chal raha hai? Koi nahi jaanta. `latest` ek kharab tag hai kyunki wo badalta rehta hai. Aachi tagging se aap kisi bhi image ko ek commit se jod sakte ho, aur rollback bhi aasaan hota hai.

### [01:15 – 05:00] Scene 2: Tagging Strategy
**[VISUAL: Tag examples: semantic version `1.4.2`, git SHA `a1b2c3d`, branch `main`, and an immutable digest `sha256:...`. A guide: "Deploy by version or digest, never by latest".]**

**(Voiceover):**
Teen tareeke jo saath chalte hain. Semantic version, jaise `1.4.2`, jo logon ke liye. Git commit SHA, jaise `a1b2c3d`, jo exact code se jodta hai. Aur digest, `sha256:...`, jo content ka asli, na badalne wala pehchaan hai. Deploy karte waqt version ya SHA se, `latest` se nahi. Image ka naam hota hai `registry/namespace/name:tag`, jaise `ghcr.io/aapkaorg/hello:1.0.0`.

### [05:00 – 08:30] Scene 3: Registry aur Login
**[VISUAL: Registries: Docker Hub, GHCR, AWS ECR, Google Artifact Registry, Azure ACR. A flow: `docker login`, `docker tag`, `docker push`, `docker pull`. A note on private repos and access tokens.]**

**(Voiceover):**
Registry images ka ghar hai. Docker Hub public aur private dono, GHCR GitHub ke saath, ECR AWS ke liye, Artifact Registry GCP ke liye, ACR Azure ke liye. Flow: `docker login`, `docker tag hello:1.0 REGISTRY/hello:1.0`, `docker push REGISTRY/hello:1.0`. Login ke liye password ki jagah access token ya cloud ka role, aur CI mein secrets se. Private registry mein vulnerability scanning aur immutable tags jaise features bhi hote hain.

### [08:30 – 11:30] Scene 4: Lab: GitHub Actions se Build aur Push
**[VISUAL: A workflow using `docker/login-action`, `docker/metadata-action`, `docker/build-push-action` pushing to GHCR with tags from the commit SHA. The Packages tab shows the image.]**

**(Voiceover):**
Lab: GitHub Actions mein ek workflow:
```yaml
name: image
on: { push: { branches: [main] } }
permissions: { contents: read, packages: write }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```
Push karo, aur repo ke Packages mein image dikhegi. Action versions ke liye docs dekh lena. Ab koi bhi machine `docker pull` karke wahi image chala sakti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "version + SHA tags · digest · registry · CI build/push · never deploy latest".]**

**(Voiceover):**
Recap: Docker ka poora safar: image banana, chhota karna, tag karna aur share karna. Ab ek sawaal: sau containers ko kaun sambhalega, restart, scale, update? Kubernetes.
