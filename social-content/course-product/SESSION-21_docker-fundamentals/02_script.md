# ✍️ 02: SCRIPT — SESSION-21: Docker Fundamentals
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S21`
- **Focus:** Why containers, container vs VM, what a container really is (process, namespaces, cgroups), Docker client, daemon and registry, images, layers, tags and digests, `docker run` flags, lifecycle and debugging commands, exit codes, logs and their disk cost, published ports and the firewall, volumes and bind mounts, user-defined networks, a first look at Compose
- **Builds on:** Session 03 and 05 (processes, signals, `ufw`, disk), Session 04 (groups), Session 10 (EBS, snapshot), Session 13 (why production databases go to RDS), Session 14 (private wing, doors), Session 17 to 20 (the conveyor that delivers a finished unit)
- **Story position:** Zoom level 3, head office. Finished unit ab ek sealed service truck mein pack hota hai, jise koi bhi building apne courtyard mein park karke apni bijli aur paani se jod sakti hai.
- **Story words used:** truck (container), truck design (image), serving window (port mapping), locker room (volume), depot (registry), fit-out sheet (Dockerfile, preview), building (server), courtyard (the host's space for trucks), guest (end user), foreman and conveyor (callbacks)
- **Lab project:** Atithi's `rooms-service` truck design (an `nginx` page first, then a database truck with a locker room), run, inspected, broken and repaired.
- **Cost rule:** Docker Engine is free; the lab building is billed while it runs. Stop it after the lab. Remove lab containers, volumes and images at the end so the disk does not fill.
- **Episodes:**
  - Episode 1: "Mere Laptop Par Chalta Tha": Truck kyun
  - Episode 2: Truck Design, Layers aur Depot
  - Episode 3: Truck Chalana: run, Ports, Logs aur Debugging
  - Episode 4: Locker Room aur Raste: Volumes, Networks aur Compose

---

# 📺 EPISODE 1: Truck kyun

### [00:00 – 02:25] Scene 1: Wahi Code, Alag Naseeb
**[VISUAL: A designer's laptop shows the rooms-service running with Python 3.12. The staging server shows an error: "SyntaxError, Python 3.8". A moving truck loads the app with its whole equipment and runs identically on both machines.]**

**(Voiceover):**
Atithi ka rooms-service designer ke laptop par chalta hai, Python 3.12 ke saath. Staging server par Python 3.8 hai, aur wahi code error deta hai. Code wahi, mashin alag. Isko "mere laptop par to chal raha tha" kehte hain. Jenkins aur Actions ki conveyor ne ek finished unit bana diya, par wo unit ye maanta hai ki server par sahi Python, sahi packages aur sahi settings pehle se hain. Hal: finished unit ke saath poora saaman bhi pack karo, ek sealed service truck mein, jo jis building ke courtyard mein khadi ho, wahan ek jaisi chale.

### [02:25 – 05:15] Scene 2: Truck vs Building
**[VISUAL: Left: a building stack. Hardware → hypervisor → three full buildings (each with its own management and generator) → apps. Right: a courtyard stack. Hardware → one building with its management → three trucks parked in the courtyard sharing its power and water. Labels: "GB, minutes" and "MB, seconds".]**

**(Voiceover):**
VM aur container ka farq story se samjho. VM ek poori alag building hai: apna management, apna generator, apna pura operating system, jaise Session 1 mein hypervisor ne ek bade tower ko alag alag buildings mein baanta tha. Container ek truck hai. Wo building ke courtyard mein khadi hoti hai, building ki bijli, paani aur management, yaani kernel, use karti hai, par uska apna saaman, apna stock aur apni privacy hai. Isliye truck MB mein hoti hai aur seconds mein chalu, building GB mein aur minutes mein. Ek dhyaan: truck ki privacy building ki deewar jitni gehri nahi. Isolation VM se kam hai, to security ke liye ek aur soch chahiye, jo hum aage dekhenge.

### [05:15 – 08:15] Scene 3: Truck Asli Mein Ek Process Hai
**[VISUAL: A host's `ps aux` output with a `python app.py` process, highlighted. A box drawn around it with two labels: "namespaces: what it can see (processes, network, file system)" and "cgroups: how much it can use (CPU, memory)". A caption: "container ends when its main process ends".]**

**(Voiceover):**
Truck mein koi jaadu nahi. Ye Linux ke do features ka khel hai, jo aapne Session 5 ke process ke saath dekhe hain. Namespaces tay karte hain ki process kya dekh sakta hai: sirf apne process, apna network, apni file system. Cgroups tay karte hain ki wo kitna use kar sakta hai: kitna CPU aur memory. Docker bas inhe ek aasan interface mein baandh deta hai. Isliye container sach mein ek process hai, jo building ke `ps aux` mein bhi dikhta hai. Aur jis din us truck ka main process khatam hota hai, container khatam hota hai. Truck ke andar ka pehla process, PID 1, aur Session 5 ke signals yahan bahut kaam aate hain, jo hum Episode 3 mein dekhenge.

### [08:15 – 10:55] Scene 4: Kab Truck, Kab Building
**[VISUAL: A decision card. "Truck: one app, quick start, same everywhere, scale by copies, short life". "Building (VM): different operating system or kernel, strong isolation, long-lived, many services together". A third row: "Often both: trucks inside buildings".]**

**(Voiceover):**
Hamesha truck nahi, hamesha building nahi. Truck tab, jab ek app ko apni dependencies ke saath tez chalana ho, kai copies mein, aur jo kabhi bhi gir kar dobara ban sakti ho. Building tab, jab alag operating system ya alag kernel chahiye, bahut gehra isolation chahiye, ya ek lambi zindagi wali machine jisme kai cheezein saath chalti hain. Aksar dono saath hote hain: truck, building ke andar. Atithi ki EC2 buildings Session 8 se chal rahi hain, aur unke courtyards mein ab trucks khadi hongi. Aur ek baat jo Kubernetes tak jaati hai: truck ko ek aisi cheez maano jo kabhi bhi hat kar dobara ban sakti hai.

### [10:55 – 13:35] Scene 5: Lab: Docker Install aur Pehla Truck
**[VISUAL: Terminal on an Ubuntu building. Install Docker Engine from the official docs. `sudo usermod -aG docker $USER`, log out and in, `docker version` showing Client and Server, `docker run hello-world`, then `docker info | head`.]**

**(Voiceover):**
Lab. Ubuntu building par Docker Engine ko official documentation ke steps se install karo, kyunki repository ke details badalte rehte hain. Phir `sudo usermod -aG docker $USER`, logout aur login, taaki har command par sudo na lage. Session 4 aur 18 ka sabak yaad rakho: docker group mein hona us building par root jaisa hai. `docker version` mein Client aur Server dono dikhne chahiye, aur `docker info` mein storage driver aur containers ki ginti. Phir `docker run hello-world`. Output dhyaan se padho: Docker ne image dhoondhi, download ki, container chalaya aur message print kiya. Mac par Docker Desktop ek chhoti Linux VM ke andar yahi karta hai.

### [13:35 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "truck = app + its equipment · shares the building's kernel · namespaces + cgroups · it is a process · docker group = root".]**

**(Voiceover):**
Recap: truck kya hai, building se kaise alag, aur andar se kaise bani hai. Ab Docker ke parts: client, daemon, depot, aur truck design ke layers.

---

# 📺 EPISODE 2: Truck Design, Layers aur Depot

### [00:00 – 02:20] Scene 1: Design aur Truck
**[VISUAL: A master truck design (image). Many identical trucks rolling out from it (containers). A label "design is read-only; trucks are running copies".]**

**(Voiceover):**
Image ek truck design hai, container uske design se bani asli truck. Ek design se aap kitni bhi trucks bana sakte ho, sab ek jaisi. Design read-only hota hai aur badalta nahi. Truck uski chalti hui copy hai. Is farq ko pakka kar lo, kyunki aage ka sab kuch isi par tika hai. Ek dusre se mat milana: jab hum kehte hain "image banao", to design banta hai. Jab kehte hain "container chalao", to truck roll out hoti hai.

### [02:20 – 05:25] Scene 2: Client, Daemon aur Depot
**[VISUAL: The `docker` CLI (client) sends commands to the daemon `dockerd` on the building. The daemon holds local images and containers, and talks to a registry (Docker Hub, GHCR, ECR). Arrows: build, push, pull, run. The client and daemon can be on different machines.]**

**(Voiceover):**
Docker teen hisson mein hai. Client, yaani `docker` command, jo aap type karte ho. Daemon, `dockerd`, jo building mein background mein asli kaam karta hai: designs aur trucks sambhalna. Aur depot, yaani registry, jahan designs rakhe jaate hain: Docker Hub public hai, ECR, GHCR aur Artifact Registry aksar private ke liye. `docker pull` depot se design laata hai, `docker push` bhejta hai, `docker run` truck chalata hai. Client aur daemon alag machines par bhi ho sakte hain, isliye aap door ki building ke Docker ko control kar sakte ho. Isi wajah se daemon ko kholna khatarnak hai, jaise Session 19 ke foreman ke daftar ka darwaza.

### [05:25 – 08:00] Scene 3: Layers aur Cache
**[VISUAL: An image drawn as stacked slabs with hashes: base OS, system packages, Python packages, app code. A change to the top slab rebuilds only that slab. Two designs share the same lower slabs. A thin writable slab on top of a running truck.]**

**(Voiceover):**
Image ek akhand file nahi, layers ka stack hai. Har layer ek badlaav hai: sabse neeche base operating system, phir packages, phir aapka code. Layers read-only hoti hain aur cache hoti hain, isliye jab sirf aapka code badla, to neeche ki layers dobara nahi banti. Aur kai designs ek hi base layer share karte hain, to download aur disk dono bachte hain. Jab truck chalti hai, uske upar ek patli writable layer judti hai. Truck hati, wo layer bhi gayi. Session 22 mein hum is order ka faayda uthana seekhenge.

### [08:00 – 10:55] Scene 4: Tag aur Digest
**[VISUAL: An image reference broken into parts: `registry/namespace/name:tag`, with `nginx:1.27-alpine` highlighted. Beside it, a digest `nginx@sha256:...`. A warning on `latest`: "a label that moves". A line: "same tag, different design next month".]**

**(Voiceover):**
Design ka poora naam hota hai `registry/namespace/name:tag`, jaise `nginx:1.27-alpine`. Tag ek label hai, jo ek design se doosre par ja sakta hai. `latest` sirf ek naam hai, ye zaroori nahi ki sabse naya ho, aur aaj ka `latest` agle mahine kuch aur ho sakta hai. Isliye production mein ek tay version tag, ya sabse pakka, digest: `nginx@sha256:...`. Digest design ki content ki pehchaan hai, aur wo badal nahi sakta. Ek khatra aur: Docker Hub ke public designs par bharosa mat karo bina dekhe. Official images aur bharose ke publishers ko chuno, aur Session 20 ke X-ray, yaani Trivy, se scan karo.

### [10:55 – 13:50] Scene 5: Lab: Designs ko Dekho
**[VISUAL: Terminal: `docker pull nginx:alpine`, `docker pull nginx:latest`, `docker images`, `docker history nginx:alpine`, `docker image inspect nginx:alpine --format '{{.Id}} {{.Size}}'`, `docker system df`. Two image sizes side by side.]**

**(Voiceover):**
Lab. `docker pull nginx:alpine` aur `docker pull nginx:latest`. `docker images` mein dono ke size dekho: alpine wala bahut chhota hai, kyunki uska base chhota hai. `docker history nginx:alpine` se layers ki list dekho, har layer ka size aur wo command jisse bani. `docker image inspect nginx:alpine --format '{{.Id}}'` se design ki pehchaan padho. Aur `docker system df` se dekho ki Docker disk par kitna le raha hai. Ye Session 5 ke `df` ka sahi saathi hai, kyunki purane designs aur band trucks chupchap disk bhar dete hain. Safai ke liye `docker image rm` aur, savdhani se, `docker image prune`.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "image = design · container = truck · client / daemon / depot · layers + cache · tag moves, digest does not · scan what you pull".]**

**(Voiceover):**
Recap: design, truck, depot, layers, tag aur digest. Ab trucks ko chalana aur sambhalna.

---

# 📺 EPISODE 3: Truck Chalana

### [00:00 – 01:55] Scene 1: Ek Command, Ek Web Server
**[VISUAL: Terminal: `docker run -d --name web -p 8080:80 nginx:alpine`. A browser opens `http://BUILDING_IP:8080` and shows the nginx welcome page. A timer reads 3 seconds.]**

**(Voiceover):**
Ek command, aur ek web server chalu. Pehle ye install, config aur service start ka kaam hota tha, jaise Session 5B mein Apache ke saath hum ne kiya tha. Ab teen second. Aaj hum `docker run` ke zaroori flags, truck ko sambhalne ki commands, aur truck ke andar ki dikkat dhoondhna seekhenge. Aur ek dhyaan ki baat: Session 8 ke security group mein 8080 allow karna padega, warna browser tak jawab nahi aayega. Truck ka serving window aur building ka door, dono ka ek hona zaroori hai.

### [01:55 – 04:20] Scene 2: docker run ke Flags
**[VISUAL: A breakdown of `docker run -d --name web -p 8080:80 -e GREETING=hi --memory 256m --cpus 0.5 --restart unless-stopped --log-opt max-size=10m --log-opt max-file=3 nginx:alpine` with each flag labelled.]**

**(Voiceover):**
`-d` truck ko background mein chalata hai. `--name web` naam deta hai. `-p 8080:80` serving window ko building ke door se jodta hai: baayein host, daayein truck. `-e` environment variable deta hai, jaise Session 6 mein parameter. `--memory 256m` aur `--cpus 0.5` cgroups ki taakat se hadd lagate hain, aur memory ki hadd paar hone par truck ko kill kar diya jaata hai. `--restart unless-stopped` crash ya reboot par truck ko dobara chalata hai. `-it` interactive terminal ke liye, `--rm` band hote hi truck hatane ke liye. Aur ek flag jo sab bhool jaate hain: `--log-opt max-size=10m`, kyunki default mein log kabhi rotate nahi hote aur disk bhar sakti hai.

### [04:20 – 06:45] Scene 3: Port aur Firewall ka Jaal
**[VISUAL: A building with a `ufw` rule "deny 8080". A truck started with `-p 8080:80` still answers from the internet. An arrow shows Docker writing its own rule ahead of `ufw`. A fix: `-p 127.0.0.1:8080:80` binds only to the loopback.]**

**(Voiceover):**
Session 5 mein hum ne `ufw` ka darwaza seekha tha. Ab ek chhupa jaal: Docker apne rules building ke firewall mein khud likh deta hai, aur wo `ufw` ke rules se pehle chal jaate hain. Matlab `ufw deny 8080` likha ho, phir bhi `-p 8080:80` wali truck internet par khuli reh sakti hai. Isliye do niyam. Ek, sirf wahi port publish karo jiski zaroorat hai. Do, agar truck sirf us building ke andar se kisi aur ko dikhani hai, to `-p 127.0.0.1:8080:80` se sirf loopback par bandho. Aur asli darwaza building ka security group rakho, jo Session 8 aur 14 ne sikhaya. Database ka port kabhi publish mat karo.

### [06:45 – 09:05] Scene 4: Lifecycle aur Debugging
**[VISUAL: A state diagram: created → running → paused or exited → removed. Commands listed: `docker ps`, `docker ps -a`, `docker stop`, `start`, `restart`, `rm`, `logs --tail 50 -f`, `exec -it web sh`, `inspect --format`, `stats`, `top`, `cp`.]**

**(Voiceover):**
`docker ps` chalte trucks dikhata hai, `docker ps -a` band wale bhi. `docker stop`, `start`, `restart`, `rm`. Debugging ke liye: `docker logs --tail 50 -f web` live log, `docker exec -it web sh` chalti truck ke andar ek shell, `docker inspect web` poori detail, `docker stats` live CPU aur memory, aur `docker top web` truck ke process. Ek rule: truck ko aisi cheez maano jo kabhi bhi mar kar dobara ban sakti hai. Andar jaake haath se settings badalna aur use yaad rakhna, ye galat tareeka hai, kyunki design se nayi truck banate hi sab gayab. Badlaav hamesha design ya parameter mein hota hai, truck ke andar nahi.

### [09:05 – 11:25] Scene 5: Truck Mar Gayi: Exit Code Padho
**[VISUAL: `docker ps -a` showing a status "Exited (137)", "Exited (1)", "Exited (143)". A decode table: 0 normal, 1 app error, 137 killed (often out of memory), 143 stopped by SIGTERM. A line "docker stop = SIGTERM, 10 seconds, then SIGKILL".]**

**(Voiceover):**
Truck gir jaaye to pehle exit code padho. `docker ps -a` mein "Exited (1)" ka matlab app ne khud galti ke saath band kiya. 0 matlab theek band hui. 137 matlab use kill kiya gaya, aksar memory ki hadd paar karne par. 143 matlab SIGTERM se band hui, jo `docker stop` bhejta hai, aur dus second mein na rukne par SIGKILL. Ye Session 5 ke signals hain. Isi liye app ko truck ka pehla process banao aur exec form mein chalao, taaki signal seedha uske paas pahunche. Phir `docker logs` se wajah padho, aur `docker inspect --format '{{.State.OOMKilled}}' web` se pata karo ki memory ne maara ya nahi.

### [11:25 – 13:40] Scene 6: Settings Truck ke Bahar se
**[VISUAL: One truck design started three times with different `-e ENV=dev`, `-e ENV=staging`, `-e ENV=prod` and an `--env-file prod.env` that is listed in `.gitignore`. A red cross over a design with a password baked into a layer.]**

**(Voiceover):**
Ek truck design, teen jagah: dev, staging aur production. Design ek hi rahega, to farq kahan jaayega? Settings truck ke bahar se aati hain. `-e ENV=staging` se ek-ek variable, ya `--env-file prod.env` se poori list, jaisa Session 15 ke Lambda mein environment variables the. Isse "twelve-factor" soch kehte hain: code ek, settings bahar se. Aur ek pakka niyam: password ya token design ke andar kabhi nahi. Design ki layers ko koi bhi depot se pull karke padh sakta hai. `prod.env` jaisi file `.gitignore` mein rahe, aur asli secrets Secrets Manager ya key cabinet se aayein, truck ke bahar se, chalne ke waqt.

### [13:40 – 16:00] Scene 7: Lab: Todo, Dekho, Sudharo
**[VISUAL: Run nginx, edit the page inside with `docker exec`, remove and re-run: the change is gone. A truck that exits at once, read with `docker logs`. A memory-limited truck killed by an allocation, `OOMKilled` true. `docker system df`, prune.]**

**(Voiceover):**
Lab. `docker run -d --name web -p 8080:80 nginx:alpine`. Phir `docker exec web sh -c 'echo changed > /usr/share/nginx/html/index.html'` aur browser mein badlaav dekho. Ab `docker rm -f web` aur wahi `docker run` dobara: badlaav gayab. Sabak: writable layer asthayi hai. Doosra test: `docker run --name bad alpine sh -c 'echo oops; exit 1'`, phir `docker ps -a` aur `docker logs bad`, aur exit code padho. Teesra: `docker run --name lim --memory 32m alpine sh -c 'tail /dev/zero'`, phir `docker inspect lim --format '{{.State.OOMKilled}}'`. Aakhir mein `docker rm -f` se saari lab trucks hatao, aur `docker system df` se dekho ki kitni jagah wapas aayi.

### [16:00 – 16:45] Scene 8: Recap aur Bridge
**[VISUAL: A card: "-d -p -e --name --restart --memory --cpus --log-opt · docker adds its own firewall rules · logs, exec, inspect, stats · read the exit code · the writable layer is temporary".]**

**(Voiceover):**
Recap: run ke flags, port aur firewall ka jaal, debugging aur exit code. Ab ek sawaal: agar truck ka data asthayi hai, to guests ke bookings kahan rakhein? Aur trucks aapas mein baat kaise karti hain?

---

# 📺 EPISODE 4: Locker Room aur Raste

### [00:00 – 01:55] Scene 1: Truck Hati, Data Bhi Gaya
**[VISUAL: A database truck holding twenty bookings. `docker rm -f db`. The bookings vanish. A second take with a locker room attached to the building: the new truck opens the same bookings.]**

**(Voiceover):**
Ek database truck chalayi, usme bookings daali, aur kisi ne truck hata di. Saari bookings gayi. Truck asthayi hai, isliye keemti cheezein truck ke andar nahi, building ke locker room mein rakhte hain. Docker mein iska naam volume hai. Aur trucks aapas mein baat karein, iske liye network. Ek zaroori note: yahan hum lab ke liye database truck chalayenge. Production ke bookings Session 13 ke records office, yaani RDS, mein rakhte hain, jahan backup aur failover landlord sambhalta hai. Truck mein database seekhne aur testing ke liye achha hai, asli ledger ke liye nahi.

### [01:55 – 04:15] Scene 2: Volume, Bind Mount aur tmpfs
**[VISUAL: Three panels. 1: named volume `pgdata` managed by Docker, stored under `/var/lib/docker/volumes`, label "portable, managed". 2: bind mount of a host folder `./src:/app`, label "dev convenience". 3: tmpfs, memory only, label "gone when the truck stops".]**

**(Voiceover):**
Locker room ke teen roop. Volume: Docker khud sambhalta hai, `docker volume create pgdata`, aur `-v pgdata:/var/lib/postgresql/data` se truck mein lagta hai. Truck hata do, volume bacha rehta hai. Bind mount: building ka ek folder seedha truck mein lagta hai, jaise `-v "$PWD/src:/app"`, jo development mein code ko turant dekhne ke liye achha hai, par permissions ki dikkat deta hai. Aur tmpfs: sirf memory mein, truck band to gayab, jaise temporary secrets ke liye. Production ke data ke liye volume. Ek dhyaan: volume building ki disk par rehta hai, isliye building gayi to volume bhi. Isliye volume ka backup alag lena padta hai, aur Session 10 ka EBS snapshot us disk ki photograph ban sakta hai.

### [04:15 – 06:25] Scene 3: Volume ka Backup
**[VISUAL: A command: `docker run --rm -v pgdata:/data -v "$PWD":/backup alpine tar czf /backup/pgdata-$(date +%Y%m%d).tgz -C /data .` creating a tarball on the host. A restore command in the other direction. A caution: "a copy of a live database folder may be inconsistent; for databases use the database's own dump".]**

**(Voiceover):**
Volume ka backup ek chhoti, tez trick se ho jaata hai. Ek temporary truck chalao jisme volume bhi lage aur building ka ek folder bhi: `docker run --rm -v pgdata:/data -v "$PWD":/backup alpine tar czf /backup/pgdata.tgz -C /data .` Ye Session 6 ka `tar` hai, bas truck ke andar. Restore ulte tareeke se. Par database ke liye ek savdhani: chalte database ka folder copy karna ek aadha-adhura photo ho sakta hai. Database ka apna dump, jaise `pg_dump`, ya truck band karke copy. Aur asli production mein RDS ka automated backup. Volume ka backup sirf wahan kaam aata hai jahan aap truck ko stateful ki tarah chala rahe ho.

### [06:25 – 08:35] Scene 4: Raste: Docker Network
**[VISUAL: Two panels. Default bridge: containers reachable by IP only, IPs change. A user-defined bridge `appnet`: containers resolve each other by name, `db` and `app`. Beside them, host and none as options. A line: "published ports = doors to the outside; internal trucks need none".]**

**(Voiceover):**
Trucks ek network par chalti hain. Default bridge par wo sirf IP se baat karti hain, aur IP badal sakta hai. Apna user-defined bridge network banao: `docker network create appnet`, aur usme trucks daalo, to wo ek doosre ko naam se bula sakti hain, jaise `db`. Isse app ke config mein `DB_HOST=db` likh sakte ho, jaise Session 13 mein endpoint ka naam tha. Ek aur baat: network ke andar ki trucks ko port publish karne ki zaroorat nahi. Wo sirf building ke bahar walon ke liye hota hai. Isiliye database truck ka port kabhi bahar mat kholo. Ye Session 14 ke private wing jaisa hai: andar ka raasta andar hi.

### [08:35 – 10:55] Scene 5: Compose: Ek File Mein Truck Park
**[VISUAL: A `compose.yaml` with services `app` and `db`, a volume `pgdata`, a network, and an `environment` block. Commands: `docker compose up -d`, `docker compose ps`, `docker compose logs -f app`, `docker compose down`. A caution on `down -v`.]**

**(Voiceover):**
Do trucks, ek network, ek volume, aur kai flags: har baar itni lambi command likhna thaka deta hai aur galti bhi karwata hai. Isliye Compose: ek `compose.yaml` file mein `app` aur `db` service, volume, aur environment. `docker compose up -d` se sab ek saath, `docker compose ps` se halat, `docker compose logs -f app` se log, `docker compose down` se sab hat jaata hai. `down -v` volume bhi hata deta hai, to data ke saath savdhan. Compose ek building ke andar trucks ka chhota park chalane ke liye hai. Kai buildings ke bade park ko Kubernetes sambhalega, jo hum Session 23 se dekhenge. Aur compose file bhi vault mein, blueprint ke saath, review ke saath.

### [10:55 – 14:25] Scene 6: Lab: App aur Database
**[VISUAL: `docker network create appnet`; `docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16`; a one-off truck with `psql` creating a table and inserting a row; `docker rm -f db`; the same `docker run` again; `select * from t` shows the row.]**

**(Voiceover):**
Lab:
```bash
docker network create appnet
docker run -d --name db --network appnet \
  -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec db pg_isready -U postgres; do sleep 1; done
docker run --rm -e PGPASSWORD=secret --network appnet postgres:16 \
  psql -h db -U postgres -c 'create table if not exists t(x int); insert into t values (1); select * from t;'
```
Dhyaan: database ko shuru hone mein kuch second lagte hain, isliye `until docker exec db pg_isready` wali line se intezaar karte hain. Uske bina `psql` ka pehla try aksar `Connection refused` deta hai. Ab `docker rm -f db`, wahi `docker run` dobara (intezaar ke saath), aur `select * from t;` wali command phir chalao, bina table banaye: data abhi bhi hai. Phir `docker volume ls` aur `docker volume inspect pgdata` se locker room ki jagah dekho. Password yahan sirf example ke liye hai: asli kaam mein secrets ek alag tareeke se dete hain, jaise Session 13 mein. Safai: `docker rm -f db`, `docker volume rm pgdata`, `docker network rm appnet`, aur building ko stop karo.

### [14:25 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "volume = locker room, survives the truck · backup it separately · user-defined network, names not IPs · do not publish the database port · compose = a small park in one building". Then a blank sheet titled "fit-out sheet" appears on a desk.]**

**(Voiceover):**
Recap: Docker ka poora basic toolkit. Par abhi tak hum ne dusron ke truck designs chalaye. Atithi ki apni rooms-service ka design kaise bane? Uske liye ek fit-out sheet chahiye: ek likhi hui list ki truck mein kya kya jaayega, kis order mein. Agle session mein Dockerfile, chhoti aur surakshit designs, aur depot mein unhe rakhna.

---

# 📎 Student handout: Session 21 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Truck vs building | Truck building ka kernel share karti hai; MB aur seconds; isolation kam |
| Andar se | Ek process + namespaces (kya dikhe) + cgroups (kitna mile) |
| Docker parts | Client, daemon (`dockerd`), depot (registry) |
| Image vs container | Design read-only; truck uski chalti copy; upar patli writable layer |
| Tag | Label hai, badal sakta hai; `latest` par nahi; digest pakka |
| `docker run` | `-d --name -p -e --memory --cpus --restart --rm -it` |
| Log | `--log-opt max-size` lagao, nahi to disk bharti hai |
| Port | `-p host:truck`; Docker ufw se pehle rules likhta hai; `-p 127.0.0.1:...` |
| Debug | `ps -a`, `logs`, `exec -it`, `inspect`, `stats`, `top` |
| Exit code | 0 theek, 1 app error, 137 kill (aksar memory), 143 SIGTERM |
| Volume | `-v name:/path`; truck hati, data bacha; building gayi to volume bhi |
| Bind mount | Dev ke liye; tmpfs sirf memory mein |
| Backup | `tar` wali temporary truck; database ke liye dump |
| Network | User-defined bridge, naam se baat; database port publish nahi |
| Compose | `compose.yaml`; `up -d`, `ps`, `logs`, `down` (`-v` savdhani) |
| Safai | `rm`, `volume rm`, `network rm`, `system df`, `prune` savdhani se |
