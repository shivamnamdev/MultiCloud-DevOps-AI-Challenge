# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-21_docker-fundamentals

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,856 · **Episodes:** 4

---

# EPISODE 1: Truck kyun

## Wahi Code, Alag Naseeb

Atithi ka rooms-service designer ke laptop par chalta hai, Python 3.12 ke saath. Staging server par Python 3.8 hai, aur wahi code error deta hai. Code wahi, mashin alag. Isko "mere laptop par to chal raha tha" kehte hain. Jenkins aur Actions ki conveyor ne ek finished unit bana diya, par wo unit ye maanta hai ki server par sahi Python, sahi packages aur sahi settings pehle se hain. Hal: finished unit ke saath poora saaman bhi pack karo, ek sealed service truck mein, jo jis building ke courtyard mein khadi ho, wahan ek jaisi chale. Hotel ki har service, reservations, housekeeping, restaurant, billing, aisi hi apni apni truck mein jaayegi.

## Truck vs Building

VM aur container ka farq story se samjho. VM ek poori alag building hai: apna management, apna generator, apna pura operating system, jaise Session 1 mein hypervisor ne ek bade tower ko alag alag buildings mein baanta tha. Container ek truck hai. Wo building ke courtyard mein khadi hoti hai, building ki bijli, paani aur management, yaani kernel, use karti hai, par uska apna saaman, apna stock aur apni privacy hai. Isliye truck MB mein hoti hai aur seconds mein chalu, building GB mein aur minutes mein. Ek dhyaan: truck ki privacy building ki deewar jitni gehri nahi. Isolation VM se kam hai, to security ke liye ek aur soch chahiye, jo hum aage dekhenge.

## Truck Asli Mein Ek Process Hai

Truck mein koi jaadu nahi. Ye Linux ke do features ka khel hai, jo aapne Session 5 ke process ke saath dekhe hain. Namespaces tay karte hain ki process kya dekh sakta hai: sirf apne process, apna network, apni file system. Cgroups tay karte hain ki wo kitna use kar sakta hai: kitna CPU aur memory. Docker bas inhe ek aasan interface mein baandh deta hai. Isliye container sach mein ek process hai, jo building ke ps aux mein bhi dikhta hai. Aur jis din us truck ka main process khatam hota hai, container khatam hota hai. Truck ke andar ka pehla process, PID 1, aur Session 5 ke signals yahan bahut kaam aate hain, jo hum Episode 3 mein dekhenge.

## Kab Truck, Kab Building

Hamesha truck nahi, hamesha building nahi. Truck tab, jab ek app ko apni dependencies ke saath tez chalana ho, kai copies mein, aur jo kabhi bhi gir kar dobara ban sakti ho. Building tab, jab alag operating system ya alag kernel chahiye, bahut gehra isolation chahiye, ya ek lambi zindagi wali machine jisme kai cheezein saath chalti hain. Aksar dono saath hote hain: truck, building ke andar. Atithi ki EC2 buildings Session 8 se chal rahi hain, aur unke courtyards mein ab trucks khadi hongi. Aur ek baat jo Kubernetes tak jaati hai: truck ko ek aisi cheez maano jo kabhi bhi hat kar dobara ban sakti hai.

## Lab: Docker Install aur Pehla Truck

Lab. Ubuntu building par Docker Engine ko official documentation ke steps se install karo, kyunki repository ke details badalte rehte hain. Phir sudo usermod -aG docker $USER, logout aur login, taaki har command par sudo na lage. Session 4 aur 18 ka sabak yaad rakho: docker group mein hona us building par root jaisa hai. docker version mein Client aur Server dono dikhne chahiye, aur docker info mein storage driver aur containers ki ginti. Phir docker run hello-world. Output dhyaan se padho: Docker ne image dhoondhi, download ki, container chalaya aur message print kiya. Mac par Docker Desktop ek chhoti Linux VM ke andar yahi karta hai.

## Recap aur Bridge

Recap: truck kya hai, building se kaise alag, aur andar se kaise bani hai. Ab Docker ke parts: client, daemon, depot, aur truck design ke layers.

---

# EPISODE 2: Truck Design, Layers aur Depot

## Design aur Truck

Image ek truck design hai, container uske design se bani asli truck. Ek design se aap kitni bhi trucks bana sakte ho, sab ek jaisi. Design read-only hota hai aur badalta nahi. Truck uski chalti hui copy hai. Is farq ko pakka kar lo, kyunki aage ka sab kuch isi par tika hai. Ek dusre se mat milana: jab hum kehte hain "image banao", to design banta hai. Jab kehte hain "container chalao", to truck roll out hoti hai.

## Client, Daemon aur Depot

Docker teen hisson mein hai. Client, yaani docker command, jo aap type karte ho. Daemon, dockerd, jo building mein background mein asli kaam karta hai: designs aur trucks sambhalna. Aur depot, yaani registry, jahan designs rakhe jaate hain: Docker Hub public hai, ECR, GHCR aur Artifact Registry aksar private ke liye. docker pull depot se design laata hai, docker push bhejta hai, docker run truck chalata hai. Client aur daemon alag machines par bhi ho sakte hain, isliye aap door ki building ke Docker ko control kar sakte ho. Isi wajah se daemon ko kholna khatarnak hai, jaise Session 19 ke foreman ke daftar ka darwaza.

## Layers aur Cache

Image ek akhand file nahi, layers ka stack hai. Har layer ek badlaav hai: sabse neeche base operating system, phir packages, phir aapka code. Layers read-only hoti hain aur cache hoti hain, isliye jab sirf aapka code badla, to neeche ki layers dobara nahi banti. Aur kai designs ek hi base layer share karte hain, to download aur disk dono bachte hain. Jab truck chalti hai, uske upar ek patli writable layer judti hai. Truck hati, wo layer bhi gayi. Session 22 mein hum is order ka faayda uthana seekhenge.

## Tag aur Digest

Design ka poora naam hota hai registry/namespace/name:tag, jaise nginx:1.27-alpine. Tag ek label hai, jo ek design se doosre par ja sakta hai. latest sirf ek naam hai, ye zaroori nahi ki sabse naya ho, aur aaj ka latest agle mahine kuch aur ho sakta hai. Isliye production mein ek tay version tag, ya sabse pakka, digest: nginx@sha256:.... Digest design ki content ki pehchaan hai, aur wo badal nahi sakta. Ek khatra aur: Docker Hub ke public designs par bharosa mat karo bina dekhe. Official images aur bharose ke publishers ko chuno, aur Session 20 ke X-ray, yaani Trivy, se scan karo.

## Lab: Designs ko Dekho

Lab. docker pull nginx:alpine aur docker pull nginx:latest. docker images mein dono ke size dekho: alpine wala bahut chhota hai, kyunki uska base chhota hai. docker history nginx:alpine se layers ki list dekho, har layer ka size aur wo command jisse bani. docker image inspect nginx:alpine --format '{{.Id}}' se design ki pehchaan padho. Aur docker system df se dekho ki Docker disk par kitna le raha hai. Ye Session 5 ke df ka sahi saathi hai, kyunki purane designs aur band trucks chupchap disk bhar dete hain. Safai ke liye docker image rm aur, savdhani se, docker image prune.

## Recap aur Bridge

Recap: design, truck, depot, layers, tag aur digest. Ab trucks ko chalana aur sambhalna.

---

# EPISODE 3: Truck Chalana

## Ek Command, Ek Web Server

Ek command, aur ek web server chalu. Pehle ye install, config aur service start ka kaam hota tha, jaise Session 5B mein Apache ke saath hum ne kiya tha. Ab teen second. Aaj hum docker run ke zaroori flags, truck ko sambhalne ki commands, aur truck ke andar ki dikkat dhoondhna seekhenge. Aur ek dhyaan ki baat: Session 8 ke security group mein 8080 allow karna padega, warna browser tak jawab nahi aayega. Truck ka serving window aur building ka door, dono ka ek hona zaroori hai.

## docker run ke Flags

-d truck ko background mein chalata hai. --name web naam deta hai. -p 8080:80 serving window ko building ke door se jodta hai: baayein host, daayein truck. -e environment variable deta hai, jaise Session 6 mein parameter. --memory 256m aur --cpus 0.5 cgroups ki taakat se hadd lagate hain, aur memory ki hadd paar hone par truck ko kill kar diya jaata hai. --restart unless-stopped crash ya reboot par truck ko dobara chalata hai. -it interactive terminal ke liye, --rm band hote hi truck hatane ke liye. Aur ek flag jo sab bhool jaate hain: --log-opt max-size=10m, kyunki Linux Engine ke default mein log kabhi rotate nahi hote aur disk bhar sakti hai.

## Port aur Firewall ka Jaal

Session 5 mein hum ne ufw ka darwaza seekha tha. Ab ek chhupa jaal: Docker apne rules building ke firewall mein khud likh deta hai, aur wo ufw ke rules se pehle chal jaate hain. Matlab ufw deny 8080 likha ho, phir bhi -p 8080:80 wali truck internet par khuli reh sakti hai. Isliye do niyam. Ek, sirf wahi port publish karo jiski zaroorat hai. Do, agar truck sirf us building ke andar se kisi aur ko dikhani hai, to -p 127.0.0.1:8080:80 se sirf loopback par bandho. Aur asli darwaza building ka security group rakho, jo Session 8 aur 14 ne sikhaya. Database ka port kabhi publish mat karo.

## Lifecycle aur Debugging

docker ps chalte trucks dikhata hai, docker ps -a band wale bhi. docker stop, start, restart, rm. Debugging ke liye: docker logs --tail 50 -f web live log, docker exec -it web sh chalti truck ke andar ek shell, docker inspect web poori detail, docker stats live CPU aur memory, aur docker top web truck ke process. Ek rule: truck ko aisi cheez maano jo kabhi bhi mar kar dobara ban sakti hai. Andar jaake haath se settings badalna aur use yaad rakhna, ye galat tareeka hai, kyunki design se nayi truck banate hi sab gayab. Badlaav hamesha design ya parameter mein hota hai, truck ke andar nahi.

## Truck Mar Gayi: Exit Code Padho

Truck gir jaaye to pehle exit code padho. docker ps -a mein "Exited (1)" ka matlab app ne khud galti ke saath band kiya. 0 matlab theek band hui. 137 matlab use kill kiya gaya, aksar memory ki hadd paar karne par. 143 matlab SIGTERM se band hui, jo docker stop bhejta hai, aur grace period mein na rukne par SIGKILL, yaani 137. Ye Session 5 ke signals hain, aur lab mein ek ajeeb baat dikhi: truck ka pehla process, PID 1, bina apne signal handler ke SIGTERM ko andekha kar deta hai. docker run alpine sleep 1000 ko stop karo to wo poori wait ke baad 137 par girta hai, aur --init ke saath turant 143 par. Grace period kitni hai, apni machine par time docker stop se naapo, ya -t khud do. Isi liye app ko truck ka pehla process banao aur exec form mein chalao, taaki signal seedha uske paas pahunche. Phir docker logs se wajah padho, aur docker inspect --format '{{.State.OOMKilled}}' web se pata karo ki memory ne maara ya nahi.

## Docker ka AI Assistant: Gordon

Docker ka apna AI assistant hai: Gordon. Ye Docker Desktop mein side bar se, ya terminal mein docker ai se chalta hai. Wo Docker ke concepts samjhata hai, Dockerfile likhne ya sudharne mein madad karta hai, aur truck mar jaaye to logs padhkar wajah aur fix ka sujhav deta hai. Docker ke docs ke mutabik wo har kaam pehle propose karta hai aur aap approve karte ho, aur permissions har session mein dobara maangi jaati hain. Ye wahi baat hai jo Session 2 mein assistant ke liye seekhi: draft assistant ka, jaanch aapki. Isliye pehle truck ki exit code aur logs aap khud padhna seekho, jo humne abhi kiya, taaki aap jaan sako ki Gordon ka sujhav sahi hai ya nahi. Dhyaan: ise signed-in Docker account aur naya Docker Desktop chahiye, version docs mein dekho, aur uska istemaal plan ki limit mein aata hai. Isliye "approve all" bina soche mat dabana. Lab: pichhle lab ki kharab truck par Gordon se poochho "ye kyun mar gayi?", aur uska jawab apni padhi hui exit code se milao.

## Settings Truck ke Bahar se

Ek truck design, teen jagah: dev, staging aur production. Design ek hi rahega, to farq kahan jaayega? Settings truck ke bahar se aati hain. -e ENV=staging se ek-ek variable, ya --env-file prod.env se poori list, jaisa Session 15 ke Lambda mein environment variables the. Isse "twelve-factor" soch kehte hain: code ek, settings bahar se. Aur ek pakka niyam: password ya token design ke andar kabhi nahi. Design ki layers ko koi bhi depot se pull karke padh sakta hai. prod.env jaisi file .gitignore mein rahe, aur asli secrets Secrets Manager ya key cabinet se aayein, truck ke bahar se, chalne ke waqt.

## Lab: Todo, Dekho, Sudharo

Lab. docker run -d --name web -p 8080:80 nginx:alpine. Phir docker exec web sh -c 'echo changed > /usr/share/nginx/html/index.html' aur browser mein badlaav dekho. Ab docker rm -f web aur wahi docker run dobara: badlaav gayab. Sabak: writable layer asthayi hai. Doosra test: docker run --name bad alpine sh -c 'echo oops; exit 1', phir docker ps -a aur docker logs bad, aur exit code padho. Teesra: docker run --name lim --memory 32m alpine sh -c 'tail /dev/zero', phir docker inspect lim --format '{{.State.OOMKilled}}'. Aakhir mein docker rm -f se saari lab trucks hatao, aur docker system df se dekho ki kitni jagah wapas aayi.

## Recap aur Bridge

Recap: run ke flags, port aur firewall ka jaal, debugging aur exit code. Ab ek sawaal: agar truck ka data asthayi hai, to guests ke bookings kahan rakhein? Aur trucks aapas mein baat kaise karti hain?

---

# EPISODE 4: Locker Room aur Raste

## Truck Hati, Data Bhi Gaya

Ek database truck chalayi, usme bookings daali, aur kisi ne truck hata di. Saari bookings gayi. Truck asthayi hai, isliye keemti cheezein truck ke andar nahi, building ke locker room mein rakhte hain. Docker mein iska naam volume hai. Aur trucks aapas mein baat karein, iske liye network. Ek zaroori note: yahan hum lab ke liye database truck chalayenge. Production ke bookings Session 13 ke records office, yaani RDS, mein rakhte hain, jahan backup aur failover landlord sambhalta hai. Truck mein database seekhne aur testing ke liye achha hai, asli ledger ke liye nahi.

## Volume, Bind Mount aur tmpfs

Locker room ke teen roop. Volume: Docker khud sambhalta hai, docker volume create pgdata, aur -v pgdata:/var/lib/postgresql/data se truck mein lagta hai. Truck hata do, volume bacha rehta hai. Bind mount: building ka ek folder seedha truck mein lagta hai, jaise -v "$PWD/src:/app", jo development mein code ko turant dekhne ke liye achha hai, par permissions ki dikkat deta hai. Aur tmpfs: sirf memory mein, truck band to gayab, jaise temporary secrets ke liye. Production ke data ke liye volume. Ek dhyaan: volume building ki disk par rehta hai, isliye building gayi to volume bhi. Isliye volume ka backup alag lena padta hai, aur Session 10 ka EBS snapshot us disk ki photograph ban sakta hai.

## Volume ka Backup

Volume ka backup ek chhoti, tez trick se ho jaata hai. Ek temporary truck chalao jisme volume bhi lage aur building ka ek folder bhi: docker run --rm -v pgdata:/data -v "$PWD":/backup alpine tar czf /backup/pgdata.tgz -C /data . Ye Session 6 ka tar hai, bas truck ke andar. Restore ulte tareeke se. Par database ke liye ek savdhani: chalte database ka folder copy karna ek aadha-adhura photo ho sakta hai. Database ka apna dump, jaise pg_dump, ya truck band karke copy. Aur asli production mein RDS ka automated backup. Volume ka backup sirf wahan kaam aata hai jahan aap truck ko stateful ki tarah chala rahe ho.

## Raste: Docker Network

Trucks ek network par chalti hain. Default bridge par wo sirf IP se baat karti hain, aur IP badal sakta hai. Apna user-defined bridge network banao: docker network create appnet, aur usme trucks daalo, to wo ek doosre ko naam se bula sakti hain, jaise db. Isse app ke config mein DB_HOST=db likh sakte ho, jaise Session 13 mein endpoint ka naam tha. Ek aur baat: network ke andar ki trucks ko port publish karne ki zaroorat nahi. Wo sirf building ke bahar walon ke liye hota hai. Isiliye database truck ka port kabhi bahar mat kholo. Ye Session 14 ke private wing jaisa hai: andar ka raasta andar hi.

## Compose: Ek File Mein Truck Park

Do trucks, ek network, ek volume, aur kai flags: har baar itni lambi command likhna thaka deta hai aur galti bhi karwata hai. Isliye Compose: ek compose.yaml file mein app aur db service, volume, aur environment. docker compose up -d se sab ek saath, docker compose ps se halat, docker compose logs -f app se log, docker compose down se sab hat jaata hai. down -v volume bhi hata deta hai, to data ke saath savdhan. Compose ek building ke andar trucks ka chhota park chalane ke liye hai. Kai buildings ke bade park ko Kubernetes sambhalega, jo hum Session 23 se dekhenge. Aur compose file bhi vault mein, blueprint ke saath, review ke saath.

## Lab: App aur Database

Lab:

Dhyaan: database ko shuru hone mein kuch second lagte hain, isliye until docker exec db pg_isready wali line se intezaar karte hain. Uske bina psql ka pehla try aksar Connection refused deta hai. Aur -h 127.0.0.1 zaroori hai: naye volume par Postgres pehle ek chhota temporary server chalata hai jo sirf socket par sunta hai, aur bina -h ke pg_isready usi ko "accepting connections" bol deta hai. Humne teen baar bina -h ke aazmaya aur teeno baar Connection refused mila, -h 127.0.0.1 ke saath teeno baar theek. Ab docker rm -f db, wahi docker run dobara (intezaar ke saath), aur select * from t; wali command phir chalao, bina table banaye: data abhi bhi hai. Phir docker volume ls aur docker volume inspect pgdata se locker room ki jagah dekho. Password yahan sirf example ke liye hai: asli kaam mein secrets ek alag tareeke se dete hain, jaise Session 13 mein. Safai: docker rm -f db, docker volume rm pgdata, docker network rm appnet, aur building ko stop karo.

## Recap aur Bridge

Recap: Docker ka poora basic toolkit. Par abhi tak hum ne dusron ke truck designs chalaye. Atithi ki apni rooms-service ka design kaise bane? Uske liye ek fit-out sheet chahiye: ek likhi hui list ki truck mein kya kya jaayega, kis order mein. Agle session mein Dockerfile, chhoti aur surakshit designs, aur depot mein unhe rakhna.
