# ✍️ 02: SCRIPT — SESSION-05: Linux SysAdmin & Troubleshooting
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S05`
- **Focus:** Resource monitoring, process lifecycle and states, signals, services (systemd), logs (`journalctl`, `/var/log`, `logrotate`), networking commands, static IP, firewall basics, a troubleshooting method, health-check script
- **Author's notes woven in:** `Linux-Handwritten-Notes.md` sections 7 to 10 (map: `NOTES_INTEGRATION_MAP_LINUX_K8S.md`)
- **Distribution:** Ubuntu is the main line (`ufw`, netplan); the Red Hat family equivalent (`firewalld`, `nmcli`, `nmtui`) is named here and practised in Session 05B
- **Story position:** Zoom level 1, inside one building. Atithi Hotels ke manager ka daily round, aur phir ek kharab din.
- **Story words used:** workforce, desks aur overflow room (CPU, RAM, swap), work order (process), token number (PID), supervisor (parent process), shift supervisor (systemd), always-on department (service), logbook room (`/var/log`), purane register ka archive (`logrotate`), street address (IP address), numbered door (port), gate ka guard (firewall), directory (DNS)
- **Episodes:**
  - Episode 1: Server ki Sehat: Manager ka Daily Round, Work Orders aur Token Numbers
  - Episode 2: Services aur Logs: Always-On Departments aur Logbook Room
  - Episode 3: Network ke Sawaal: Address, Darwaze aur Gate ka Guard
  - Episode 4: Troubleshooting ka Tareeka aur Health-Check Script

---

# 📺 EPISODE 1: Server ki Sehat

### [00:00 – 02:05] Scene 1: "Server Slow Hai"
**[VISUAL: The Atithi Hotels building at 9 am. A phone buzzes: "Website bahut slow hai!!". A panicked hand reaches for the building's main power switch. The manager stops the hand, picks up a clipboard and starts walking the floors. Cut to a terminal opening on a server.]**

**(Voiceover):**
Pichhle session mein Atithi ki building mein staff aaya, taale lage aur pehla guest serve hua. Aaj subah subah message aaya: website slow hai. Sabse aasaan lagta hai poori building ki bijli band karke dobara chalu kar dena, yaani server restart. Par isse wajah kabhi pata nahi chalti, aur kal wahi problem phir aayegi. Achha manager pehle round lagata hai: kitna staff kaam mein laga hai, desks bhari hain ya khaali, jagah bachi hai ya nahi. Server par yahi round chaar cheezon ka hai: CPU, memory, disk aur network. Is session mein hum ye round seekhenge, aur phir ek kharab din ko sambhalna. Is episode mein: server ki sehat aur processes.

### [02:05 – 05:15] Scene 2: Round ki Chaar Commands: uptime, top, free, df
**[VISUAL: The manager's clipboard with four rows: workforce (CPU), work desks (RAM), overflow room (swap), floor space (disk). Each row turns into a terminal panel: `uptime` with load average, `top` with the process list, `free -h` with the "available" column highlighted, `df -h` with one line at 96%.]**

**(Voiceover):**
Round ki pehli command `uptime`. Ye batati hai server kitni der se chal raha hai, aur load average, yaani kitna kaam workforce ka intezaar kar raha hai. Workforce yaani CPU. `top` ek live board hai: kaun sa kaam sabse zyada CPU ya memory kha raha hai, wo sabse upar dikhta hai. `free -h` desks ka hisaab hai, yaani RAM. Yahan "available" asli aankda hai, sirf "free" nahi. Usi mein swap ki line bhi hai: swap wo dheema overflow room hai jahan kaam tab bheja jaata hai jab saari desks bhar jaayein. Swap bharne lage to samjho RAM kam pad rahi hai. `df -h` batata hai building mein jagah kitni bachi hai, yaani disk. Aur `du -sh *` dikhata hai kaun sa folder bhaari hai. `nproc` batata hai kitne CPU hain: load average ko isse milao, kyunki chaar CPU par load chaar ka matlab poora bhara, par ek CPU par wahi load chaar ka matlab teen kaam intezaar mein. Disk 100% bhar jaye to bahut saari cheezein ek saath toot jaati hain.

### [05:15 – 09:15] Scene 3: Process: Work Order, Token Number aur Uski Zindagi
**[VISUAL: A work-order slip with a token number (PID) and the token of the supervisor who issued it (PPID). A tree: systemd (1) → sshd → bash → python app. Terminal: `ps -ef` with the PID and PPID columns highlighted, then `ps aux` with the STAT column highlighted. A small legend: R running, S sleeping, T stopped, Z zombie. One slip stamped "done" still lying on the supervisor's desk, labelled "zombie".]**

**(Voiceover):**
Server par har chalti cheez ek process hai. Hotel ki bhasha mein, ek work order jo abhi chal raha hai. Har work order ka ek token number hota hai, yaani PID, aur us supervisor ka token bhi, jisne ye kaam diya, yaani PPID, parent process ID. `ps -ef` mein dono columns dikhte hain. Aapka `bash` bhi ek process hai, aur usme chalayi har command uska child banti hai. Zindagi aisi chalti hai: parent ek child banata hai, child kaam karta hai, khatm hone par apna nateeja parent ko deta hai, aur parent use register se hata deta hai. `ps aux` mein `STAT` column haalat batata hai: `R` yaani chal raha hai, `S` yaani so raha hai aur kisi cheez ka intezaar kar raha hai, `T` yaani roka gaya hai, aur `Z` yaani zombie. Zombie wo work order hai jo poora ho chuka hai, par supervisor ne abhi uska nateeja uthaya nahi. Wo CPU ya memory nahi khaata, bas register mein ek line ghere rehta hai. Use kill nahi kar sakte, kyunki wo pehle hi khatm ho chuka hai; theek uske parent ko karna padta hai. Aur agar parent pehle khatm ho jaye to child anaath nahi rehta: use shift supervisor, yaani PID 1 wala systemd, god le leta hai. Ye saari jaankari kernel `/proc` folder mein rakhta hai.

### [09:15 – 11:20] Scene 4: Kaam Rokna: Signals
**[VISUAL: The manager first taps a worker on the shoulder (SIGTERM, 15), and only if ignored, pulls the plug on the machine (SIGKILL, 9). Terminal: `ps aux | grep nginx`, `kill 4321`, `kill -9 4321`, `killall yes`.]**

**(Voiceover):**
Kisi kaam ko rokna ho to use signal bheja jaata hai. `ps aux | grep nginx` se process dhoondho aur PID lo. `kill PID` SIGTERM bhejta hai, yaani kandhe par haath rakh kar kehna ki kaam samet lo, taaki wo saaf-safai karke band ho. Agar na maane to `kill -9 PID`, SIGKILL, yaani machine ka plug kheench dena. Isme kaam adhoora chhoot sakta hai. Pehle polite, phir force, ye order yaad rakho. PID ki jagah naam se rokna ho to `killall` aur command ka naam. Aur `ps` ki `TTY` column batati hai kaam kis terminal se juda hai. Wahan sawaaliya nishaan ho to wo background ka kaam hai, jiska koi terminal nahi.

### [11:20 – 13:40] Scene 5: Lab: CPU Chadhao, Pakdo, Roko
**[VISUAL: Terminal 1 runs `yes > /dev/null &`. Terminal 2 shows `top` with `yes` at ~100% CPU, then `ps -o pid,ppid,stat,cmd -C yes`. User runs `kill -STOP <PID>` (STAT becomes T), `kill -CONT <PID>` (R again), then `kill <PID>`; CPU drops.]**

**(Voiceover):**
Lab. Ek terminal mein `yes > /dev/null &` chalao. Ye ek process background mein CPU khaata rahega. Doosre terminal mein `top` kholo aur `yes` ko sabse upar dekho. Ab `ps -o pid,ppid,stat,cmd -C yes` chalao: token number, supervisor ka token aur haalat, teeno ek line mein. Haalat `R` hogi. `kill -STOP PID` chalao aur wahi `ps` dobara dekho, ab `T` hai, kaam ruka hua hai aur CPU neeche aa gaya. `kill -CONT PID` se wo phir chal padta hai. Aakhir mein `kill PID` se use band karo. Ab aapne ek load ko dekha, pehchana, roka aur khatm kiya. Ye ek mini incident hai. Dhyaan rahe: production par kisi bhi process ko kill karne se pehle pata karo wo kya hai aur uska parent kaun hai.

### [13:40 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A health card: uptime/load · top · free -h · df -h · ps (PID, PPID, STAT) · kill. Under it, small: "workforce · desks · overflow room · work order · token".]**

**(Voiceover):**
Recap: round ki chaar commands, work order yaani process, token yaani PID, uski haalat, aur signals se control. Ab un departments ki baat jo kabhi band nahi hote: services, aur unki logbooks.

---

# 📺 EPISODE 2: Services aur Logs

### [00:00 – 02:00] Scene 1: Reboot ke Baad Website Gayab
**[VISUAL: The hotel reopens after a power cut. Every department lights up except the front desk, which stays dark. The shift supervisor's morning list is shown: the front desk is not on it. Cut to a server after reboot: the website returns "connection refused". Text: "Service not enabled at boot".]**

**(Voiceover):**
Raat ko bijli gayi, subah building dobara khuli, par front desk band pada hai. Wajah: kal kisi ne use haath se khola tha, par shift supervisor ki subah wali list mein uska naam likha hi nahi. Server par yahi hota hai: reboot hua aur website wapas nahi aayi, kyunki service haath se start hui thi, boot par chalne ke liye enable nahi thi. Service wo department hai jo hamesha khula rehta hai. Unhe shift supervisor sambhalta hai, yaani systemd, aur usse baat karne ka tareeka hai `systemctl`.

### [02:00 – 04:45] Scene 2: systemctl ki Commands
**[VISUAL: Terminal: `systemctl status nginx`, `start`, `stop`, `restart`, `reload`, `enable`, `disable`, `is-active`. Status shows "active (running)" in green and "enabled" highlighted on the Loaded line. A side note: "start = open now · enable = on the morning list".]**

**(Voiceover):**
`systemctl status nginx` batata hai service chal rahi hai ya nahi, uska main PID kya hai, aur neeche uske aakhri kuch log lines. `start` aur `stop` chalu aur band. `restart` band karke chalu karta hai. `reload` bina band kiye nayi config padhwata hai, jo production ke liye behtar hai kyunki guests ka connection nahi tootta. Aur do alag cheezein yaad rakho: `start` department ko abhi kholta hai, `enable` uska naam subah ki list mein likhta hai. Dono alag hain, isliye aksar `sudo systemctl enable --now nginx` ek saath use hota hai. Yahi tareeka har service par chalta hai: `sudo systemctl restart ssh` staff entrance wali service ko dobara chalata hai. Red Hat family mein usi service ka naam `sshd` hai.

### [04:45 – 09:20] Scene 3: Logbook Room: journalctl, /var/log aur logrotate
**[VISUAL: A room full of logbooks labelled `/var/log`. One shelf: `syslog`, `auth.log`, `nginx/error.log`. A clerk (rsyslog) writing in books; a second clerk (journald) writing in a sealed binder that only opens through a window labelled `journalctl`. On the top shelf, four dated old registers; a fifth arrives and the oldest goes to the bin. Terminal: `journalctl -u nginx -n 50`, `journalctl -u nginx -f`, `journalctl -p err --since "1 hour ago"`, `ls /var/log`, `cat /etc/logrotate.conf`.]**

**(Voiceover):**
Har department apni logbook likhta hai, aur saari logbooks ek hi kamre mein rakhi hain: `/var/log`. Yahan do clerk kaam karte hain. Pehla `rsyslog`, jo seedhi text files likhta hai. Kaun si baat kis file mein jaati hai, ye `/etc/rsyslog.conf` mein likha hai. Ubuntu par login ki entries `auth.log` mein milti hain, Red Hat family mein `secure` mein. Doosra clerk `systemd-journald` hai. Uska register text nahi hota, isliye use `cat` se nahi, `journalctl` se padhte hain. `journalctl -u nginx -n 50` us service ki aakhri pachaas lines dikhata hai, `-f` live follow karta hai, `-p err` sirf errors, aur `--since "1 hour ago"` samay ka filter hai. Ek baat aur: journal agar `/run/log/journal` mein likha ja raha hai to reboot par chala jaata hai. `/var/log/journal` folder ho to disk par bachta hai, aur Ubuntu par aam taur par aisa hi hota hai. Ab sawaal: logbooks bharti rahin to kamra bhar jayega. Isliye purane register archive hote hain, yaani `logrotate`. Uski config `/etc/logrotate.conf` mein do lines dekho: `weekly`, yaani har hafte naya register, aur `rotate 4`, yaani chaar purane rakho. Paanchwa bante hi sabse purana hat jaata hai. Pehle service ka status, phir uska log: ye jodi aapko zyadatar problems ka jawab degi.

### [09:20 – 12:10] Scene 4: Lab: Service ko Todo aur Theek Karo
**[VISUAL: Config edited to remove a `;`. `sudo nginx -t` reports a syntax error with a line number. `sudo systemctl restart nginx` fails; `systemctl status nginx` shows "failed" in red; `journalctl -u nginx -n 20` shows the same error; the typo is fixed; `nginx -t` passes; the service starts.]**

**(Voiceover):**
Lab: nginx ki config mein jaan-boojh kar ek galti karo, jaise `/etc/nginx/nginx.conf` mein ek line ke aakhir ka `;` hata do. `sudo nginx -t` se config test karo, wo file aur line number ke saath error batayega. Dhyaan: line number aksar us line ke agli line ka hota hai jahan `;` chhoota; humare test mein doosri line toot-i to error teesri line par aaya. Ab `sudo systemctl restart nginx` chalao, fail hoga. `systemctl status nginx` mein laal "failed" dikhega, aur `journalctl -u nginx -n 20` mein wajah. Galti theek karo, `nginx -t` pass hoga, aur restart chalega. Seekh: pehle config test, phir restart, aur production mein `reload` ko prefer karo. Aur `systemctl is-enabled nginx` se pakka kar lo ki ye department subah ki list mein hai.

### [12:10 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "status → logs → fix → test config → reload · enable for boot · logrotate keeps the room from filling".]**

**(Voiceover):**
Recap: systemctl se control, `start` aur `enable` ka farq, journalctl aur `/var/log` se jaanch, logrotate se archive, aur config test se bachav. Ab network: jab service chal rahi ho par bahar se koi pahunch na paaye.

---

# 📺 EPISODE 3: Network ke Sawaal

### [00:00 – 01:50] Scene 1: Service Chal Rahi Hai, Phir Bhi Nahi Khulti
**[VISUAL: A guest's car on the road, unable to reach the hotel. The route drawn as stops: directory lookup (DNS) → road (route) → gate guard (firewall) → door 80 (port) → front desk (app). A question mark on each stop. Cut to a browser: "This site can't be reached".]**

**(Voiceover):**
Front desk khula hai, staff baitha hai, phir bhi guest nahi pahunch raha. Ab problem building ke andar nahi, raaste mein hai. Guest ne directory mein sahi address paaya? Yaani DNS sahi IP de raha hai? Sadak us address tak jaati hai? Yaani route theek hai? Gate ka guard rok to nahi raha? Yaani firewall? Aur front desk sahi darwaze par baitha hai? Yaani app sahi port par sun raha hai? In sawaalon ko ek ek karke todna hi networking troubleshooting hai, aur hum andar se bahar ki taraf chalenge.

### [01:50 – 04:10] Scene 2: ip, ss aur ping
**[VISUAL: Terminal: `ip a` with the interface name and IP highlighted, `ip route` with the "default via" line highlighted, `ss -tulpn` with the LISTEN column, `ping -c 3 8.8.8.8`.]**

**(Voiceover):**
`ip a` aapke interfaces aur unke IP addresses dikhata hai. IP address building ka street address hai. `ip route` batata hai traffic kis raaste se bahar jayega. Usme `default via` wali line aapka default gateway hai, yaani colony se bahar nikalne wala mod. `ss -tulpn` dikhata hai kaun sa process kis darwaze par sun raha hai, yaani kis port par LISTEN kar raha hai. Agar aapka app 8080 par sunna chahiye aur `ss` mein wo dikh hi nahi raha, to app ki problem hai, network ki nahi. `ping` batata hai ki doosri machine tak pahunch hai ya nahi. Lekin kai servers ping band rakhte hain, to ping na chale iska matlab hamesha down nahi hota.

### [04:10 – 07:45] Scene 3: Pakka Address: Static IP
**[VISUAL: A building whose street number keeps changing on the signboard (DHCP), then a fixed engraved number plate (static). Two columns. Ubuntu: a file `/etc/netplan/01-config.yaml` with `addresses`, `routes`, `nameservers`, then `sudo netplan try`. Red Hat family: `nmtui` menu (Edit a connection → IPv4 → Manual), `nmcli con mod ...`, `nmcli con up ...`. A red banner: "Cloud VM par mat badlo".]**

**(Voiceover):**
Aam taur par machine ko address apne aap milta hai, DHCP se, aur wo badal bhi sakta hai. Server ka address badalta rahe to guest use dhoondhega kaise? Isliye server ko pakka address dete hain, yaani static IP. Iske liye teen cheezein chahiye: address, gateway, jo `ip route` se milta hai, aur DNS server. Ubuntu server par ye `/etc/netplan` ke andar ek YAML file mein likha jaata hai, aur `sudo netplan try` use lagata hai. `try` ki khoobi ye hai ki agar aapka connection toot jaye to wo kuch der mein purani setting wapas le aata hai. Red Hat family mein ye kaam NetworkManager karta hai, aur uske teen raaste hain: `nmtui`, jo ek menu wala screen hai; `nmcli`, jo command line hai; ya seedha connection ki config file badalna. Teeno ke baad connection ko dobara uthana padta hai, tabhi nayi setting lagti hai. Ek chetavni: ye abhyas sirf apne laptop ki local VM par karo. Cloud ki VM ka address landlord deta hai, yaani cloud provider. Wahan andar se address badla to aap khud bahar ho jaoge.

### [07:45 – 09:40] Scene 4: curl aur DNS
**[VISUAL: Terminal: `curl -I https://example.com`, `curl -v http://localhost:8080`, `dig example.com +short`. A side card: "22 SSH · 80 HTTP · 443 HTTPS".]**

**(Voiceover):**
`curl` se aap khud guest ban kar darwaza khatkhata sakte ho. `curl -I` sirf headers lata hai, `curl -v` poori baat-cheet dikhata hai. Agar app `localhost` par curl se chal raha hai par bahar se nahi, to gate ka guard dekho. DNS wo directory hai jo hotel ke naam ko address mein badalti hai. `dig example.com +short` domain ka IP batata hai. Agar IP galat ya khaali hai, to problem DNS ki hai, server ki nahi. Common darwaze yaad rakho: 22 staff entrance yaani SSH, 80 public entrance yaani HTTP, 443 secured public entrance yaani HTTPS.

### [09:40 – 13:25] Scene 5: Lab: Gate ka Guard aur Layer by Layer Debug
**[VISUAL: A guard at the gate with a list of allowed doors. A checklist drawn while terminal commands run: 1 app listening? `ss` ✔ 2 local curl? ✔ 3 firewall? `sudo ufw status` 4 remote curl? ✘ → allow door 80 → ✔. A side card: "Ubuntu: ufw · Red Hat family: firewalld (`firewall-cmd`), zones, `--permanent` + `--reload`".]**

**(Voiceover):**
Firewall gate ka guard hai, jiske paas list hai ki kaun se darwaze tak aane ki ijaazat hai. Ubuntu par ye guard `ufw` hai. Lab: sabse pehle apna raasta bachao. `sudo ufw allow OpenSSH` chalao, phir `sudo ufw enable`, warna aap staff entrance se hi bahar ho sakte ho. Ab nginx chalu rakho aur andar se bahar chalo. Ek: `ss -tulpn | grep :80`, front desk darwaze par hai? Do: `curl localhost`, andar se jawab aata hai? Teen: `sudo ufw status`, guard ki list mein 80 hai? Chaar: apne laptop se `curl http://SERVER_IP`. Ye fail hoga. Ab `sudo ufw allow 80/tcp` chalao aur chautha kadam dobara karo, is baar chalega. Red Hat family mein yahi guard `firewalld` hai, aur uski command `firewall-cmd`. Wo gates ko zones mein baant-ta hai, yaani alag gate ke liye alag suraksha star. Aur wahan ek aadat chahiye: `--permanent` ke saath rule likho, phir `--reload` karo, warna rule reload ya reboot par chala jaata hai. Use hum agle session, 05B, mein haath se chalayenge. Aur cloud par ek guard aur hota hai, security group, jo building ke bahar landlord ka guard hai.

### [13:25 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "app → port → firewall → route → DNS". Under it, small: "front desk · door · gate guard · road · directory".]**

**(Voiceover):**
Recap: `ip` se address aur gateway, `ss` se darwaze, static IP se pakka address, `curl` aur `dig` se bahar ki jaanch, aur guard ki list. Hamesha ek hi order: andar se bahar. Ab in sabko ek method mein baandhte hain, aur apni pehli health-check script likhte hain.

---

# 📺 EPISODE 4: Troubleshooting ka Tareeka aur Health-Check Script

### [00:00 – 01:50] Scene 1: Ghabrahat vs Method
**[VISUAL: A bad day at the hotel: three phones ringing. Two duty managers. One runs between floors flipping random switches. The other opens a notebook and writes: "What changed?". The second finds the cause first. Cut to two terminals side by side, one full of random commands, one with a short ordered list.]**

**(Voiceover):**
Aaj Atithi ka kharab din hai: guests shikayat kar rahe hain aur teen phone ek saath baj rahe hain. Ghabrahat mein hum random switch dabate hain, yaani random commands chalate hain, aur ek aur galti kar dete hain. Achha engineer pehle method lagata hai. Ye method itna simple hai ki aap ise kisi bhi problem par laga sakte ho: kya dikh raha hai, kya badla, aur kahan se shuru karein.

### [01:50 – 06:15] Scene 2: 5-Step Troubleshooting Method
**[VISUAL: Five steps appear in the notebook: 1 Define the symptom, 2 Check what changed, 3 Look at logs and metrics, 4 Form one hypothesis and test it, 5 Fix, verify and document. Beside step 3, the commands from this session: `top`, `df -h`, `systemctl status`, `journalctl`, `ss`, `curl`.]**

**(Voiceover):**
Ek, symptom ko saaf shabdon mein likho: kya ho raha hai, kab se, aur kis par asar hai. "Site down hai" kaafi nahi; "checkout page do baje se 502 de raha hai" kaam ki baat hai. Do, pata karo kya badla: naya deploy, config, traffic, ya koi certificate jo expire ho gaya. Teen, logbooks aur board dekho, yaani logs aur metrics. Yahan is session ka poora round kaam aata hai: `top` aur `df -h` se sehat, `systemctl status` aur `journalctl` se service, `ss` aur `curl` se network. Chaar, ek hi hypothesis chuno aur ek hi cheez badal kar test karo, ek saath kai cheezein nahi, warna pata nahi chalega kisse theek hua. Paanch, fix ke baad verify karo ki problem sach mein gayi, aur kya hua wo likh lo. Yahi likhi hui baat agli baar ka runbook ban jaati hai. Aur AI assistant yahan madad kar sakta hai: use log ki lines do aur poochho ki inka matlab kya ho sakta hai. Par command chalane se pehle use khud samjho.

### [06:15 – 08:15] Scene 3: Health-Check Script ka Design
**[VISUAL: The manager's clipboard from episode 1 turns into a script outline: header, checks (disk %, memory, service status, port open), output as OK/WARN/FAIL, exit code 0 or 1.]**

**(Voiceover):**
Manager roz wahi round lagata hai. Jo checks aap roz haath se karte ho, unhe ek slip par likh do, yaani script bana do. Ek health-check script ye dekhegi: disk kitna bhara hai, memory kitni bachi hai, zaroori service chal rahi hai ya nahi, aur port khula hai ya nahi. Output saaf hona chahiye: OK, WARN ya FAIL. Aur exit code bhi, taaki monitoring ya cron ise apne aap samajh sake: sab theek hai to 0, warna non-zero.

### [08:15 – 10:55] Scene 4: Lab: Pehli Health-Check Script
**[VISUAL: An editor with `healthcheck.sh`. Terminal runs it and prints OK lines; nginx is stopped; the second run prints a FAIL line and `echo $?` prints 1.]**

**(Voiceover):**
Lab. Ye script likho:
```bash
#!/usr/bin/env bash
disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge 90 ]; then echo "FAIL disk ${disk}%"; fail=1; else echo "OK   disk ${disk}%"; fi
if systemctl is-active --quiet nginx; then echo "OK   nginx"; else echo "FAIL nginx"; fail=1; fi
exit ${fail:-0}
```
`chmod +x healthcheck.sh` karke `./healthcheck.sh` chalao. Phir `sudo systemctl stop nginx` karke dobara chalao, ek FAIL dikhega aur exit code 1 hoga, `echo $?` se dekho. Aakhir mein nginx ko wapas start kar do. Aap Session 6 mein is script ko Bash ki poori taakat ke saath sudharoge.

### [10:55 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "method · logs · one change at a time · script it". Then a teaser: an empty rented floor with no walls, a front-of-house counter, and a second guard checking badges.]**

**(Voiceover):**
Recap: manager ka round, yaani sehat, services, logbooks aur network, aur kharab din ke liye paanch kadam ka tareeka. Aur jo roz karo wo script mein daalo. Ab ek building chalana aapko aata hai. Par abhi teen cheezein baaki hain: nayi khaali jagah ko kamron mein kaise badalte hain, yaani disks aur LVM; guests ke liye front-of-house kaise khulta hai, yaani Apache web server; aur chaabi ke upar ki doosri suraksha, yaani SELinux. Ye sab agle session, 05B, mein.

---

# 📎 Student handout: Session 05 command sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Kaam | Command |
|---|---|
| Load aur uptime | `uptime` |
| Live process board | `top` |
| Memory aur swap | `free -h` |
| Disk aur bhaari folders | `df -h`, `du -sh *` |
| Processes (PID, PPID) | `ps -ef` |
| Processes (CPU, memory, STAT) | `ps aux` |
| STAT codes | `R` running, `S` sleeping, `D` uninterruptible sleep, `T` stopped, `Z` zombie |
| Process rokna | `kill PID` (SIGTERM), `kill -9 PID` (SIGKILL), `killall name` |
| Service control | `sudo systemctl status/start/stop/restart/reload svc` |
| Boot par chalana | `sudo systemctl enable --now svc`, `systemctl is-enabled svc` |
| Journal padhna | `journalctl -u svc -n 50`, `-f`, `-p err`, `--since "1 hour ago"` |
| Log files | `ls /var/log`, `/etc/rsyslog.conf`, `/etc/logrotate.conf` |
| Address aur gateway | `ip a`, `ip route` |
| Sunte hue ports | `ss -tulpn` |
| HTTP aur DNS jaanch | `curl -I URL`, `curl -v URL`, `dig name +short` |
| Static IP (Ubuntu) | `/etc/netplan/*.yaml`, `sudo netplan try` |
| Static IP (Red Hat family) | `nmtui`, ya `nmcli con mod NAME ipv4.method manual ipv4.addresses IP/24 ipv4.gateway GW`, phir `nmcli con up NAME` |
| Firewall (Ubuntu) | `sudo ufw allow OpenSSH`, `sudo ufw enable`, `sudo ufw allow 80/tcp`, `sudo ufw status` |
| Firewall (Red Hat family) | `sudo firewall-cmd --add-service=http --permanent && sudo firewall-cmd --reload` |
