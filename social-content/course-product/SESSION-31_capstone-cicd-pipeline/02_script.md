# ✍️ 02: SCRIPT — SESSION-31: Capstone — CI/CD Pipeline, Code to Production
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S31`
- **Focus:** End-to-end pipeline: Spring Boot app → GitHub webhook → Jenkins (build, test, scan) → Docker image → registry → deploy to a Linux server → verify, rollback, observe
- **Episodes:**
  - Episode 1: Capstone ka Design: Architecture aur Plan
  - Episode 2: App aur Container: Spring Boot, Tests, Dockerfile
  - Episode 3: Jenkins Pipeline: Build, Test, Scan, Push
  - Episode 4: Deploy, Verify, Rollback aur Observe

---

# 📺 EPISODE 1: Capstone ka Design

### [00:00 – 01:15] Scene 1: Ab Tak Ke Tukde, Ab Poori Kahani
**[VISUAL: A montage of earlier sessions as puzzle pieces: Linux, Git, Jenkins, Docker, cloud VM, monitoring. They snap together into one flow chart.]**

**(Voiceover):**
Ab tak aapne alag alag tukde seekhe: Linux, Git, Jenkins, Docker, cloud servers, monitoring. Aaj hum unhe jodkar ek asli kahani banate hain: developer ek line code badalta hai, aur kuch minute baad wo production mein chal raha hota hai, test, scan aur safety ke saath. Ye wahi Build, Ship, Fix ki poori kahani hai.

### [01:15 – 05:00] Scene 2: Architecture
**[VISUAL: A flow: Developer → GitHub (PR + main) → webhook → Jenkins controller → Jenkins agent → [Build+Test → Quality/Security scan → Docker build → Push to registry] → Deploy to Linux VM (docker run) → Health check → Slack/Email notification. Prometheus/Grafana watching the app.]**

**(Voiceover):**
Architecture: developer GitHub par push karta hai. Webhook Jenkins ko jagata hai. Jenkins agent par code build hota hai, tests chalte hain, security scan hota hai. Phir Docker image bani aur registry mein push hui. Uske baad ek Linux server par wo image naye version ke saath chalti hai, health check hota hai, aur Slack ya email par result aata hai. Aur monitoring app par nazar rakhti hai. Har tukda hum pehle seekh chuke hain.

### [05:00 – 08:30] Scene 3: Design ke Faisle aur Success Criteria
**[VISUAL: A decision table: Registry (GHCR/ECR), Deploy target (single VM with Docker), Rollback (previous tag), Secrets (Jenkins credentials), Tags (git SHA). A "Definition of Done" checklist.]**

**(Voiceover):**
Pehle faisle likh lo. Registry GHCR ya ECR. Deploy target ek Linux VM jahan Docker chal raha hai, kyunki simple rakhte hain. Image ka tag git SHA. Secrets Jenkins credentials mein. Rollback pichhle tag par. Aur Definition of Done: push se production tak automatic, tests fail hon to deploy nahi, galat version ko ek command se wapas laya ja sake, aur har deploy ka record. Ye success criteria likhne se project ke beech mein bhatakna nahi padta.

### [08:30 – 11:30] Scene 4: Lab: Infra Taiyaar Karo
**[VISUAL: Two VMs: `jenkins` (controller+agent, Java, Docker, Git) and `app-server` (Docker). Security groups: 8080 from my IP on jenkins, 22 from jenkins to app-server, 80/8081 on app-server. A checklist.]**

**(Voiceover):**
Lab: do Ubuntu VMs banao: `jenkins` aur `app-server`. Dono par Docker install karo. Jenkins VM par Jenkins aur Java 17. Security group: Jenkins ka 8080 sirf aapke IP se. App server par 22 sirf Jenkins VM se, aur app ka port, jaise 8081, jaha se test karna ho. Jenkins VM se app server par bina password SSH key setup karo, aur key ko Jenkins credentials mein SSH key type se rakho. Ye taiyaari is session ki neev hai. Terraform se ye sab bana sakte ho, bonus ke taur par.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "flow clear · decisions written · Definition of Done · infra ready".]**

**(Voiceover):**
Recap: design aur infra. Ab app aur uska container.

---

# 📺 EPISODE 2: App aur Container

### [00:00 – 01:15] Scene 1: Pipeline Kiske Liye?
**[VISUAL: A tiny Spring Boot app with a `/health` and `/hello` endpoint. A pipeline arrow pointing at it. Text: "The app can be small; the pipeline is the lesson".]**

**(Voiceover):**
Capstone mein app chhoti rakhenge, kyunki seekhne ki cheez pipeline hai. Ek Spring Boot application jisme `/hello` aur ek `/actuator/health` endpoint ho, aur kuch unit tests. Aap Python ya Node app se bhi yahi kar sakte ho, concept wahi hai.

### [01:15 – 05:00] Scene 2: App, Tests aur Health Endpoint
**[VISUAL: A Maven project: `pom.xml` with spring-boot-starter-web and actuator; a controller returning "Hello DevOps"; a JUnit test calling the controller; `mvn test`.]**

**(Voiceover):**
Spring Initializr se Maven project banao, dependencies mein Web aur Actuator. Ek controller:
```java
@RestController
class HelloController {
  @GetMapping("/hello")
  String hello() { return "Hello DevOps"; }
}
```
Aur ek test jo is endpoint ko check kare. Actuator ka `/actuator/health` load balancer aur deploy ke health check ke liye kaam aata hai. `mvn clean test` se tests chalao. Pipeline ki sabse pehli suraksha yahi tests hain, to unhe likhna chhodna mat.

### [05:00 – 08:30] Scene 3: Multi-stage Dockerfile
**[VISUAL: A Dockerfile: stage 1 `maven:3-eclipse-temurin-17` building the jar, stage 2 `eclipse-temurin:17-jre` copying the jar, non-root user, `EXPOSE 8080`, `HEALTHCHECK`, `ENTRYPOINT`.]**

**(Voiceover):**
Dockerfile mein wahi cheezein jo humne Docker session mein seekhi:
```dockerfile
FROM maven:3-eclipse-temurin-17 AS build
WORKDIR /w
COPY pom.xml .
RUN mvn -B -q dependency:go-offline
COPY src ./src
RUN mvn -B -q package -DskipTests

FROM eclipse-temurin:17-jre
RUN useradd -m app
WORKDIR /app
COPY --from=build /w/target/*.jar app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
```
Pehle pom copy karke dependencies cache hoti hain, multi-stage se image chhoti, aur non-root user. Tests pipeline mein alag stage mein chalenge, isliye yahan `-DskipTests`.

### [08:30 – 11:30] Scene 4: Lab: Local Chalao
**[VISUAL: `mvn clean test`, `docker build -t shop-api:local .`, `docker run -d -p 8081:8080 shop-api:local`, `curl localhost:8081/hello` and `/actuator/health`. Push the code to GitHub.]**

**(Voiceover):**
Lab: `mvn clean test`, phir `docker build -t shop-api:local .` aur `docker run -d -p 8081:8080 shop-api:local`. `curl localhost:8081/hello` mein "Hello DevOps", aur `curl localhost:8081/actuator/health` mein `UP`. Jab local pe sab chalta hai, tab code GitHub par push karo, ek `.gitignore` ke saath jisme `target/` ho. Ek test jaan-boojh kar tod ke dekho ki `mvn test` fail hota hai; ye wahi cheez hai jo pipeline ko rokni chahiye.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "tests · health endpoint · multi-stage Dockerfile · works locally first".]**

**(Voiceover):**
Recap: app, tests aur container. Ab Jenkins pipeline jo inhe automatic chalaye.

---

# 📺 EPISODE 3: Jenkins Pipeline — Build, Test, Scan, Push

### [00:00 – 01:15] Scene 1: Push Karo, Baaki Machine Karegi
**[VISUAL: A developer pushes. A pipeline stage view lights up stage by stage. A Slack message says "Build #42 passed".]**

**(Voiceover):**
Ab wo kaam jo aap haath se karte ho, local test, Docker build, push, wo sab Jenkins ko do. Hum ek Jenkinsfile likhenge jo build, test, scan, image banana aur registry mein push karne tak jaye. Deploy agle episode mein.

### [01:15 – 05:00] Scene 2: Jenkinsfile
**[VISUAL: A Jenkinsfile with stages: Checkout, Test, Scan (Trivy), Docker Build, Push, with environment variables for registry and image tag `${GIT_COMMIT[0..6]}`, `withCredentials` for registry login, and `post` notifications.]**

**(Voiceover):**
Jenkinsfile:
```groovy
pipeline {
  agent any
  options { timeout(time: 20, unit: 'MINUTES') }
  environment {
    REGISTRY = 'ghcr.io/YOUR_ORG'
    IMAGE    = "${REGISTRY}/shop-api"
    TAG      = "${env.GIT_COMMIT.take(7)}"
  }
  stages {
    stage('Test')   { steps { sh 'mvn -B clean test' } }
    stage('Build image') { steps { sh 'docker build -t $IMAGE:$TAG .' } }
    stage('Scan')   { steps { sh 'trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE:$TAG' } }
    stage('Push')   {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ghcr', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo "$P" | docker login ghcr.io -u "$U" --password-stdin'
          sh 'docker push $IMAGE:$TAG'
        }
      }
    }
  }
  post { failure { echo "FAILED: ${env.BUILD_URL}" } }
}
```
Tag git SHA ke pehle saat akshar.

### [05:00 – 08:30] Scene 3: Quality Gates aur Cache
**[VISUAL: A stage "Test" failing and subsequent stages skipped (grey). A Trivy report listing a HIGH vulnerability failing the build. A cache of Maven repo on the agent.]**

**(Voiceover):**
Pipeline ka asli kaam rokna bhi hai. Test fail hua to aage ke stage skip, image banegi hi nahi. Trivy ne HIGH ya CRITICAL vulnerability dekhi to build fail, jisme base image update ya dependency upgrade karni padegi. Isse kharab image production tak nahi jaati. Maven dependencies ko agent par cache karo, taaki build tez ho. Aur is lab mein Trivy ko agent par install karna padega, official guide se. Pipeline ko GitHub webhook se trigger karo, jo humne Jenkins session mein seekha.

### [08:30 – 11:30] Scene 4: Lab: Pipeline Chalao aur Todo
**[VISUAL: Multibranch pipeline on the repo. A push triggers a build: green. A failing test turns Test red. A HIGH vulnerability from an old base image turns Scan red. The GHCR Packages page shows the pushed image tagged with the SHA.]**

**(Voiceover):**
Lab: Multibranch pipeline banao, GitHub webhook lagao, aur Jenkins credentials mein `ghcr` ka token rakho. Push karke pipeline ko hara hote dekho aur GHCR mein SHA wala image. Ab teen "todo" test karo: ek unit test tod do, to Test stage laal. Dockerfile mein purana base image rakho jisme vulnerability ho, to Scan laal. Token galat kar do, to Push laal. Har fail ka kaaran log mein dhoondho. Ye wahi debugging hai jo asli team roz karti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "test → build → scan → push · fail early · SHA tags · webhook".]**

**(Voiceover):**
Recap: CI poora ho gaya. Ab CD: deploy, verify, aur rollback.

---

# 📺 EPISODE 4: Deploy, Verify, Rollback aur Observe

### [00:00 – 01:15] Scene 1: Deploy Mein Sabse Zyada Galti
**[VISUAL: A new version deployed. The health check isn't done; the app crashes silently. Customers see errors for 20 minutes. A safer version includes health check and auto rollback.]**

**(Voiceover):**
Deploy wo kadam hai jahan sabse zyada galtiyan hoti hain. Naya version chalu kiya, kisi ne check nahi kiya, aur 20 minute tak customers ko error dikha. Isliye deploy ke baad health check aur rollback ka plan zaroori hai, aur dono automatic hone chahiye.

### [01:15 – 05:00] Scene 2: Deploy Script
**[VISUAL: A `deploy.sh` run over SSH: pull the new image, remember the current image, stop old container, start new, wait for `/actuator/health`, on failure restart previous. Jenkins stage calls it with `sshagent`.]**

**(Voiceover):**
App server par ek chhoti script:
```bash
#!/usr/bin/env bash
set -euo pipefail
IMAGE="$1"; NAME=shop-api
PREV=$(docker inspect -f '{{.Config.Image}}' "$NAME" 2>/dev/null || true)
docker pull "$IMAGE"
docker rm -f "$NAME" 2>/dev/null || true
docker run -d --name "$NAME" --restart unless-stopped -p 8081:8080 "$IMAGE"
for i in $(seq 1 20); do
  curl -fsS http://localhost:8081/actuator/health | grep -q UP && { echo "deployed $IMAGE"; exit 0; }
  sleep 3
done
echo "health check failed, rolling back to ${PREV:-none}"
docker rm -f "$NAME"
[ -n "$PREV" ] && docker run -d --name "$NAME" --restart unless-stopped -p 8081:8080 "$PREV"
exit 1
```
Jenkins stage SSH se ye script chalata hai, image tag ke saath. Kuch der ke liye service ruk sakti hai, jo rolling ya blue-green deploy se bachayi jaati hai, par ye single-VM ke liye saaf aur seekhne layak hai.

### [05:00 – 08:30] Scene 3: Production Jaisa Deploy: Approval aur Observe
**[VISUAL: A Jenkins `input` step "Deploy to prod?" after a staging deploy and smoke test. Prometheus scrapes `/actuator/prometheus`; a Grafana panel shows request rate and errors after deploy. A deploy marker annotation on the graph.]**

**(Voiceover):**
Asli setup mein pehle staging par deploy, smoke test, phir `input` se manual approval, aur tab production. Deploy ke baad dashboard par nazar: request rate, errors aur latency. Spring Boot Actuator ke saath Prometheus format ke metrics bhi de sakta hai, jise Prometheus scrape karta hai, jo hum monitoring session mein seekh chuke hain. Deploy ke samay ek annotation lagao, taaki graph par dikhe ki kab version badla. Agar errors badhe, to rollback.

### [08:30 – 11:30] Scene 4: Lab: Poora Safar aur Chaos Test
**[VISUAL: A Jenkins Deploy stage with `sshagent` and the script. Push a change to `/hello` text; the page updates in minutes. Push a deliberately broken version (the app crashes at startup): health check fails, rollback keeps the old version live, build is red.]**

**(Voiceover):**
Lab: Jenkinsfile mein Deploy stage jodo, `sshagent(['app-server-key']) { sh 'ssh ubuntu@APP_IP "bash -s" < deploy.sh $IMAGE:$TAG' }`. `/hello` ka message badal kar push karo, aur kuch minute mein browser mein naya message dekho. Ab ek jaan-boojh kar toota hua version push karo, jisme app start par crash ho. Deploy stage health check par fail hoga, script purane version par rollback karegi, aur site chalti rahegi. Ye Fix wala hissa hai. Aakhir mein sab VMs aur resources delete karo, aur Jenkins ke token ko revoke karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "verify health · auto rollback · approval for prod · observe after deploy".]**

**(Voiceover):**
Recap: aapne code se production tak ek poori, surakshit pipeline banayi. Ab AI ke saath aage: cloud par AI app, aur model serving.
