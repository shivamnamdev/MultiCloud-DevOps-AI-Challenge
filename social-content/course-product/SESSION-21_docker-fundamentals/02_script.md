# ✍️ 02: SCRIPT — SESSION-21: Docker Fundamentals
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S21`
- **Focus:** Containers vs VMs, Docker architecture, images/containers/layers, run flags & lifecycle commands, ports, volumes, networks
- **Episodes:**
  - Episode 1: "Mere Laptop Par Chalta Tha": Container kyun
  - Episode 2: Docker Architecture, Images aur Layers
  - Episode 3: Containers Chalana: run, ports, logs, exec
  - Episode 4: Data aur Network: Volumes aur Bridge Network

---

# 📺 EPISODE 1: Container kyun?

### [00:00 – 01:15] Scene 1: Wahi Code, Alag Naseeb
**[VISUAL: A developer's laptop with a green app (Python 3.12). A server with Python 3.8 shows an error. A moving truck packs the app with its whole environment in a sealed box, and it runs identically on both.]**

**(Voiceover):**
Developer ke laptop par Python 3.12 hai, aur server par 3.8. Code wahi hai, par server par chalta nahi. "Mere laptop par to chal raha tha" wali kahani yahi hai. Container ka idea simple hai: app ko uski saari dependencies ke saath ek sealed dabbe mein pack karo, taaki jahan bhi chalao, ek jaisa chale.

### [01:15 – 05:00] Scene 2: Container vs VM: Flat aur PG ka Farq
**[VISUAL: Left: VM stack (Hardware → Hypervisor → Guest OS ×3 → Apps). Right: Container stack (Hardware → Host OS/kernel → Container runtime → Containers). Size and startup time labels: GBs & minutes vs MBs & seconds.]**

**(Voiceover):**
VM aur container ko flat aur PG ke room se samjho. VM mein har kirayedaar ko poora alag flat milta hai, apni rasoi, apna bijli ka meter, yaani poora guest OS. Container PG ke room ki tarah hai: sab ek hi building, ek hi kitchen, yaani host ka kernel, share karte hain, par har ka apna kamra, apni cheezein aur apni privacy. Isliye container MB mein hote hain aur seconds mein start, VM GB mein aur minute mein. Dhyaan: container ka isolation VM jitna gehra nahi, to security ke liye dhyaan dena padta hai.

### [05:00 – 08:30] Scene 3: Containers andar se: Namespaces aur Cgroups
**[VISUAL: A process wrapped in a box. Two labels: Namespaces (what it can see: processes, network, filesystem) and cgroups (how much it can use: CPU, memory).]**

**(Voiceover):**
Container koi jaadu nahi, ye Linux ke do features ka khel hai. Namespaces tay karte hain ki process kya dekh sakta hai: apne processes, apna network, apni file system. Cgroups tay karte hain ki wo kitna use kar sakta hai: kitna CPU aur memory. Docker bas inhe ek aasan interface mein baandh deta hai. Isi liye container ek process hi hota hai, aur jab process khatam, container khatam.

### [08:30 – 11:30] Scene 4: Lab: Docker Install aur Pehla Container
**[VISUAL: Terminal on an Ubuntu VM: install Docker Engine from the official docs, `sudo usermod -aG docker $USER`, re-login, `docker version`, `docker run hello-world`. Output explanation lines.]**

**(Voiceover):**
Lab: Ubuntu VM par Docker Engine ko official docs ke steps se install karo. Phir `sudo usermod -aG docker $USER` aur dobara login, taaki har baar sudo na lage. Dhyaan: docker group ko access dena root access dene ke barabar hai, isliye surakshit machines par samajhdari se. `docker version` se client aur server dono dikhne chahiye. Phir `docker run hello-world`. Output padho, wo batata hai ki Docker ne kya kya kiya: image dhoondhi, download ki, container chalaya, aur message print kiya.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "container = packaged app + env · shares host kernel · namespaces + cgroups".]**

**(Voiceover):**
Recap: container kya hai aur VM se kaise alag. Ab Docker ke parts: client, daemon, registry, aur image ke layers.

---

# 📺 EPISODE 2: Docker Architecture, Images aur Layers

### [00:00 – 01:15] Scene 1: Recipe aur Dish
**[VISUAL: A recipe card (image) and a dish served from it (container). Many dishes from one recipe. Text: "Image = recipe. Container = dish."]**

**(Voiceover):**
Image ek recipe hai, container wo dish jo recipe se bani. Ek recipe se aap kitni bhi dishes bana sakte ho. Image read-only hoti hai aur badalti nahi. Container usi se bana ek chalta hua instance hai. Is farq ko pakka kar lo, kyunki aage ka sab kuch isi par tika hai.

### [01:15 – 05:00] Scene 2: Client, Daemon, Registry
**[VISUAL: `docker` CLI (client) → Docker daemon (`dockerd`) → local images/containers; daemon ↔ registry (Docker Hub, ECR, GHCR). Arrows: build, pull, push, run.]**

**(Voiceover):**
Docker teen hisson mein hai. Client, yaani `docker` command, jo aap type karte ho. Daemon, `dockerd`, jo background mein asli kaam karta hai: images aur containers sambhalna. Aur registry, jahan images store hoti hain: Docker Hub public hai, ECR, GHCR aur Artifact Registry private ke liye. `docker pull` registry se image laata hai, `docker push` bhejta hai, aur `docker run` use chalata hai. Client aur daemon alag ho sakte hain, to aap remote Docker ko bhi control kar sakte ho.

### [05:00 – 08:30] Scene 3: Layers aur Cache
**[VISUAL: An image drawn as stacked slabs: base OS, packages, app code. Each slab has a hash. When a top slab changes, only that slab is rebuilt; lower slabs reused from cache. Two images sharing base layers.]**

**(Voiceover):**
Image ek akhand file nahi, layers ka stack hai. Har layer ek badlav hai: base OS, phir packages, phir aapka code. Layers read-only hoti hain aur cache hoti hain, isliye jab sirf aapka code badla to neeche ki layers dobara nahi banti, aur kai images ek hi base layer share karti hain. Isse downloads aur builds tez hote hain. Container chalne par uske upar ek patli writable layer judti hai, jo container hatne par chali jaati hai.

### [08:30 – 11:30] Scene 4: Lab: Images ko Dekho
**[VISUAL: Terminal: `docker pull nginx:alpine`, `docker images`, `docker history nginx:alpine`, `docker image inspect nginx:alpine --format '{{.Size}}'`, comparison with `nginx:latest`.]**

**(Voiceover):**
Lab: `docker pull nginx:alpine` aur `docker pull nginx:latest`. `docker images` mein dono ka size dekho: alpine wala bahut chhota hai. `docker history nginx:alpine` se layers ki list dekho. Tag samjho: `nginx:alpine` mein `nginx` image ka naam aur `alpine` tag. `latest` ek convention hai, ye zaroori nahi ki sabse naya ho, aur production mein `latest` se bachna chahiye, specific version tag use karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "image = recipe · container = dish · client/daemon/registry · layers + cache · tags not latest".]**

**(Voiceover):**
Recap: image, container, registry, layers. Ab containers ko chalana aur sambhalna.

---

# 📺 EPISODE 3: Containers Chalana

### [00:00 – 01:15] Scene 1: Ek Command, Ek Web Server
**[VISUAL: Terminal: `docker run -d -p 8080:80 nginx:alpine`. A browser opens `localhost:8080` showing the nginx welcome page. Timer: 3 seconds.]**

**(Voiceover):**
Ek command aur ek web server chalu. Pehle ye install, config aur service start ka kaam hota tha. Ab teen second. Aaj hum `docker run` ke important flags aur container ko sambhalne ki commands seekhenge.

### [01:15 – 05:00] Scene 2: docker run ke Flags
**[VISUAL: A breakdown of `docker run -d --name web -p 8080:80 -e GREETING=hi --memory 256m --restart unless-stopped nginx:alpine` with each flag labelled.]**

**(Voiceover):**
`-d` container ko background mein chalata hai. `--name web` use naam deta hai. `-p 8080:80` host ka port 8080 container ke port 80 se jodta hai: baayein taraf host, daayein taraf container. `-e` environment variable deta hai. `--memory 256m` memory limit lagata hai, cgroups ki taakat. `--restart unless-stopped` crash ya reboot par container ko dobara chalata hai. `-it` interactive terminal ke liye, `--rm` band hote hi container hatane ke liye. Ye flags aap roz use karoge.

### [05:00 – 08:30] Scene 3: Lifecycle aur Debugging Commands
**[VISUAL: A state diagram: created → running → paused/stopped → removed. Commands: `docker ps`, `docker ps -a`, `docker stop/start/restart`, `docker rm`, `docker logs -f`, `docker exec -it web sh`, `docker inspect`, `docker stats`.]**

**(Voiceover):**
`docker ps` chalte containers dikhata hai, `docker ps -a` band wale bhi. `docker stop`, `start`, `restart`, `rm`. Debugging ke liye: `docker logs -f web` live logs, `docker exec -it web sh` chalte container ke andar shell, `docker inspect web` poori detail, aur `docker stats` live CPU aur memory. Ek rule: container ko ek aise process ki tarah socho jo kabhi bhi mar kar dobara ban sakta hai. Andar manually jaake settings badalna aur use yaad rakhna, ye galat tareeka hai.

### [08:30 – 11:30] Scene 4: Lab: Container Todo aur Jaanch Karo
**[VISUAL: Run nginx, edit the page inside with `docker exec`, remove and re-run: the change is gone. Then run a container that exits immediately and read its logs with `docker logs`. Run a container with a memory limit and check `docker stats`.]**

**(Voiceover):**
Lab: `docker run -d --name web -p 8080:80 nginx:alpine`. `docker exec web sh -c 'echo changed > /usr/share/nginx/html/index.html'`, browser mein badlav dekho. Ab `docker rm -f web` aur dobara run karo: badlav gayab. Seekh: container ka writable layer temporary hai. Ek aur test: `docker run --name bad alpine sh -c 'echo oops; exit 1'`, phir `docker ps -a` aur `docker logs bad`, exit code ke saath. Aur `docker run -d --memory 64m --name lim nginx:alpine` ke baad `docker stats --no-stream`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "-d -p -e --name --restart --memory · ps/logs/exec/inspect · writable layer is temporary".]**

**(Voiceover):**
Recap: run flags aur debugging. Ab ek sawaal: agar container ka data temporary hai, to database ka data kahan rakhein? Aur containers aapas mein baat kaise karte hain?

---

# 📺 EPISODE 4: Data aur Network — Volumes aur Bridge

### [00:00 – 01:15] Scene 1: Container Hata, Data Bhi Gaya
**[VISUAL: A database container with orders. `docker rm -f db`. The orders vanish. A second try with a volume: data survives.]**

**(Voiceover):**
Database container chalaya, usme data bhara, container hataya aur saara data gaya. Ye galti production mein bahut mehngi padti hai. Container ka data ko bachane ke liye volumes hain, aur container aapas mein baat karein iske liye networks.

### [01:15 – 05:00] Scene 2: Volume vs Bind Mount
**[VISUAL: Left: Docker-managed volume (`docker volume create`) stored under Docker's area, labelled "portable, managed". Right: bind mount of a host folder `./data:/app/data`, labelled "dev convenience". A third: tmpfs for temporary memory-only data.]**

**(Voiceover):**
Do tareeke. Volume Docker khud manage karta hai: `docker volume create pgdata`, aur `-v pgdata:/var/lib/postgresql/data` se container mein lagta hai. Container hata do, volume bacha rehta hai. Bind mount mein host ka ek folder seedha container mein lagta hai, jaise `-v $(pwd)/src:/app`, jo development mein code live dekhne ke liye achha hai. Production data ke liye volumes behtar hain. Aur volume ka backup lena mat bhoolo.

### [05:00 – 08:30] Scene 3: Docker Networks
**[VISUAL: Default bridge network with containers by IP only; a user-defined bridge network where containers resolve each other by name (`db`, `app`). Host network and none shown as alternatives.]**

**(Voiceover):**
Containers ek network par chalte hain. Default bridge par wo IP se baat karte hain, jo badal sakta hai. Apna user-defined bridge network banao: `docker network create appnet`, aur usme containers daalo, to wo ek doosre ko naam se bula sakte hain, jaise `db`. Isse app ke config mein `DB_HOST=db` likh sakte ho. Aur dhyaan: sirf wahi port bahar kholo jiski zaroorat hai. Database ka port host par publish karna aam taur par galat hai, agar sirf app ko usse baat karni hai.

### [08:30 – 11:30] Scene 4: Lab: App + Database
**[VISUAL: `docker network create appnet`; `docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16`; `docker run --rm --network appnet postgres:16 psql -h db -U postgres -c 'select 1'`. Remove and recreate the db container; data persists.]**

**(Voiceover):**
Lab:
```bash
docker network create appnet
docker run -d --name db --network appnet \
  -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
docker run --rm -e PGPASSWORD=secret --network appnet postgres:16 \
  psql -h db -U postgres -c 'create table if not exists t(x int); insert into t values (1); select * from t;'
```
Ab `docker rm -f db`, wahi `docker run` dobara chalao, aur `select * from t;` chalao: data abhi bhi hai. Lab ke baad `docker rm -f db`, `docker volume rm pgdata`, `docker network rm appnet` se safai. Password example ke liye hai, asli kaam mein secrets alag tareeke se dete hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "volumes for data · bind mounts for dev · user-defined bridge, DNS by name · publish only needed ports".]**

**(Voiceover):**
Recap: Docker ka poora basic toolkit. Ab sawaal: apni app ko khud ki image mein kaise pack karein? Agle session mein Dockerfile, aur chhoti aur surakshit images banana.
