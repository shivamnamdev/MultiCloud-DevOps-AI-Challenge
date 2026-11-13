# ✍️ 02: SCRIPT — SESSION-05: Linux SysAdmin & Troubleshooting
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S05`
- **Focus:** Processes & resource monitoring, services (systemd), networking commands, a troubleshooting method, health-check script
- **Episodes:**
  - Episode 1: Server ki Sehat: CPU, Memory, Disk aur Processes
  - Episode 2: Services ko Sambhalna: systemctl aur journalctl
  - Episode 3: Network ke Sawaal: ip, ss, curl, DNS
  - Episode 4: Troubleshooting ka Tareeka aur Health-Check Script

---

# 📺 EPISODE 1: Server ki Sehat

### [00:00 – 01:15] Scene 1: "Server Slow Hai"
**[VISUAL: A Slack message: "Website bahut slow hai!!". A dev terminal opens. A stethoscope icon overlays on a server image.]**

**(Voiceover):**
Subah subah message aaya: website slow hai. Ab aap kya karoge? Server ko restart karna sabse aasaan lagta hai, par wo ilaaj nahi, wo bas doctor ke bina goli dena hai. Doctor pehle nabz dekhta hai. Server ki nabz hain: CPU, memory, disk aur network. Is episode mein inhe dekhna seekhte hain.

### [01:15 – 05:00] Scene 2: top, uptime, free, df
**[VISUAL: Terminal dashboards: `uptime` with load average, `top` with process list, `free -h` memory table, `df -h` disk table. Highlight key columns.]**

**(Voiceover):**
`uptime` batata hai server kitni der se chal raha hai aur load average, yaani kitne processes CPU ka intezaar kar rahe hain. `top` ya `htop` mein dekho kaun sa process sabse zyada CPU ya memory kha raha hai. `free -h` memory ka hisaab dikhata hai, aur dhyaan rakho ki "available" asli aankda hai, sirf "free" nahi. `df -h` har disk ka use batata hai. Aur `du -sh *` dikhata hai kaun sa folder bhaari hai. Disk 100% bhar jaye to bahut saari cheezein ek saath toot jaati hain.

### [05:00 – 08:30] Scene 3: Processes, PID aur Signals
**[VISUAL: A process tree: init/systemd → sshd → bash → python app. A kill command sends signals: SIGTERM (polite), SIGKILL (forced).]**

**(Voiceover):**
Har chalti cheez ek process hai, jiska ek PID hota hai. `ps aux` sabhi processes dikhata hai, aur `ps aux | grep nginx` filter karta hai. Process rokne ke liye `kill PID`, jo SIGTERM bhejta hai, yaani vinamrata se bolna ki band ho jao, taaki wo saaf-safai kar sake. Agar na maane to `kill -9 PID`, SIGKILL, jo zabardasti band karta hai aur kaam adhoora chhod sakta hai. Pehle polite, phir force, ye order yaad rakho.

### [08:30 – 11:30] Scene 4: Lab: CPU Chadhao, Pakdo, Roko
**[VISUAL: Terminal 1 runs `yes > /dev/null &`. Terminal 2 shows `top` with `yes` at ~100% CPU. User runs `kill <PID>`; CPU drops.]**

**(Voiceover):**
Lab. Ek terminal mein `yes > /dev/null &` chalao, ye ek process background mein CPU khaata rahega. Doosre terminal mein `top` kholo aur `yes` ko upar dekho. PID note karo aur `kill PID` chalao. Dekho CPU wapas neeche aa gaya. Ab aapne ek load ko dekha, pehchana aur roka, ye ek mini incident hai. Dhyaan rahe: production par kisi bhi process ko kill karne se pehle pata karo wo kya hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A health card: uptime/load · top · free -h · df -h · ps · kill.]**

**(Voiceover):**
Recap: nabz dekhne ki commands aur process control. Ab services: jo programs background mein hamesha chalte rehte hain, unhe kaise sambhalte hain.

---

# 📺 EPISODE 2: Services ko Sambhalna

### [00:00 – 01:15] Scene 1: Reboot ke Baad Website Gayab
**[VISUAL: A server reboots. After boot, the website returns 502. Text: "Service not enabled at boot".]**

**(Voiceover):**
Server reboot hua aur website wapas nahi aayi. Wajah: service start to hui thi haath se, par boot par apne aap chalne ke liye enable nahi thi. Services ka poora management systemd karta hai, aur uska remote control hai `systemctl`.

### [01:15 – 05:00] Scene 2: systemctl ki Commands
**[VISUAL: Terminal: `systemctl status nginx`, `start`, `stop`, `restart`, `reload`, `enable`, `disable`, `is-active`. Status shows "active (running)" in green.]**

**(Voiceover):**
`systemctl status nginx` batata hai service chal rahi hai ya nahi. `start` aur `stop` chalu aur band. `restart` band karke chalu, `reload` bina band kiye nayi config padhta hai, jo production ke liye behtar hai. Aur do alag cheezein yaad rakho: `start` abhi chalata hai, `enable` boot par chalne ke liye likhta hai. Dono alag hain, isliye aksar `systemctl enable --now nginx` ek saath use hota hai.

### [05:00 – 08:30] Scene 3: Logs: journalctl aur /var/log
**[VISUAL: Terminal: `journalctl -u nginx -n 50`, `journalctl -u nginx -f`, `journalctl -p err --since "1 hour ago"`, and `/var/log/nginx/error.log`.]**

**(Voiceover):**
Service kharab ho to uske logs padho. systemd wali services ke logs `journalctl` se milte hain: `journalctl -u nginx -n 50` aakhri pachaas lines, `-f` live follow, `-p err` sirf errors, aur `--since "1 hour ago"` samay ka filter. Kai apps apni alag log files bhi rakhte hain, jaise `/var/log/nginx/error.log`. Pehle service ka status, phir uska log: ye jodi aapko 80% problems ka jawab degi.

### [08:30 – 11:30] Scene 4: Lab: Service ko Todo aur Theek Karo
**[VISUAL: Config edited to include a typo. `sudo nginx -t` reports syntax error. `systemctl restart nginx` fails; `journalctl` shows the error; the typo is fixed; service starts.]**

**(Voiceover):**
Lab: nginx ki config mein jaan-boojh kar ek galti karo, jaise ek `;` hatao. `sudo nginx -t` se config test karo, wo error batayega. `sudo systemctl restart nginx` fail hoga. `journalctl -u nginx -n 20` mein wajah dikhegi. Galti theek karo, `nginx -t` pass hoga, aur restart chalega. Seekh: pehle config test, phir restart, aur production mein `reload` ko prefer karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "status → logs → fix → test config → reload".]**

**(Voiceover):**
Recap: systemctl se control, journalctl se jaanch, aur config test se bachav. Ab network: jab service chal rahi ho par bahar se na pahunche.

---

# 📺 EPISODE 3: Network ke Sawaal

### [00:00 – 01:15] Scene 1: Service Chal Rahi Hai, Phir Bhi Nahi Khulti
**[VISUAL: A browser "This site can't be reached". A funnel diagram: App → Port → Firewall → Network → DNS → Client, with a question mark on each.]**

**(Voiceover):**
Service active hai, phir bhi browser mein site nahi khul rahi. Ab problem kahin raaste mein hai: app sahi port par sun raha hai? Firewall roke hue hai? Network ka route theek hai? DNS sahi IP de raha hai? In sawaalon ko ek ek karke todna hi networking troubleshooting hai.

### [01:15 – 05:00] Scene 2: ip, ss aur ping
**[VISUAL: Terminal: `ip a`, `ip route`, `ss -tulpn` with a LISTEN column, `ping -c 3 8.8.8.8`.]**

**(Voiceover):**
`ip a` aapke interfaces aur IP addresses dikhata hai. `ip route` batata hai traffic kis raaste se jayega. `ss -tulpn` dikhata hai kaun sa process kis port par sun raha hai, yaani LISTEN. Agar aapka app 8080 par sunna chahiye aur `ss` mein wo dikh hi nahi raha, to app ki problem hai, network ki nahi. `ping` batata hai ki doosri machine tak pahunch hai ya nahi, lekin kai servers ping band rakhte hain, to ping na chale iska matlab hamesha down nahi hota.

### [05:00 – 08:30] Scene 3: curl, DNS aur Ports
**[VISUAL: Terminal: `curl -I https://example.com`, `curl -v http://localhost:8080`, `dig example.com +short`, `nslookup`.]**

**(Voiceover):**
`curl` HTTP ka swiss army knife hai. `curl -I` sirf headers lata hai, `curl -v` poori baat-cheet dikhata hai. Agar app localhost par curl se chal raha hai par bahar se nahi, to firewall ya security group dekho. DNS ke liye `dig example.com +short` domain ka IP batata hai. Agar IP galat ya khaali hai, to problem DNS ki hai. Common ports yaad rakho: 22 SSH, 80 HTTP, 443 HTTPS.

### [08:30 – 11:30] Scene 4: Lab: Layer by Layer Debug
**[VISUAL: A checklist drawn while terminal commands run: 1 app listening? `ss` ✔ 2 local curl? ✔ 3 firewall? `sudo ufw status` 4 remote curl? ✘ → open port 80.]**

**(Voiceover):**
Lab: nginx chalu rakho. Pehle `ss -tulpn | grep :80` se dekho ki wo sun raha hai. Phir `curl localhost`. Phir firewall: `sudo ufw status`. Agar ufw active hai aur 80 band hai, `sudo ufw allow 80/tcp`. Ab doosri machine ya apne laptop se `curl http://SERVER_IP`. Isi tarah, andar se bahar, har layer par ek check. Agar cloud par ho, to security group bhi ek layer hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "app → port → firewall → route → DNS".]**

**(Voiceover):**
Recap: ip, ss, curl, dig aur ek systematic order. Ab in sabko ek method mein baandhte hain, aur apni pehli health-check script likhte hain.

---

# 📺 EPISODE 4: Troubleshooting ka Tareeka aur Health-Check Script

### [00:00 – 01:15] Scene 1: Ghabrahat vs Method
**[VISUAL: Two engineers. One types random commands rapidly. The other writes steps in a notebook. The second finds the cause first.]**

**(Voiceover):**
Ghabrahat mein hum random commands chalate hain, aur ek aur galti kar dete hain. Achha engineer pehle method lagata hai. Ye method itna simple hai ki aap ise kisi bhi problem par laga sakte ho: kya badla, kya dikh raha hai, kahan se shuru karein.

### [01:15 – 05:00] Scene 2: 5-Step Troubleshooting Method
**[VISUAL: Five steps appear: 1 Define the symptom, 2 Check what changed, 3 Look at logs and metrics, 4 Form one hypothesis and test it, 5 Fix, verify and document.]**

**(Voiceover):**
Ek, symptom ko saaf shabdon mein likho: "kya kab se, kis par asar". Do, pata karo kya badla: deploy, config, traffic, certificate expiry. Teen, logs aur metrics dekho. Chaar, ek hi hypothesis chuno aur ek hi cheez badalkar test karo, ek saath kai cheezein nahi. Paanch, fix ke baad verify karo ki problem sach mein gayi, aur kya hua wo likh lo. Yahi likhi hui baat agli baar ka runbook ban jaati hai.

### [05:00 – 08:30] Scene 3: Health-Check Script ka Design
**[VISUAL: A script outline: header, checks (disk %, memory %, service status, port open), output as OK/WARN/FAIL, exit code.]**

**(Voiceover):**
Jo checks aap roz haath se karte ho, unhe script bana do. Ek health-check script ye dekhegi: disk kitna bhara hai, memory kitni bachi hai, zaroori service chal rahi hai ya nahi, aur port khula hai ya nahi. Output saaf hona chahiye: OK, WARN ya FAIL. Aur exit code bhi, taaki monitoring ya cron ise automatically samajh sake: sab theek hai to 0, warna non-zero.

### [08:30 – 11:30] Scene 4: Lab: Pehli Health-Check Script
**[VISUAL: An editor with `healthcheck.sh`. Terminal runs it and prints coloured lines.]**

**(Voiceover):**
Lab. Ye script likho:
```bash
#!/usr/bin/env bash
disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge 90 ]; then echo "FAIL disk ${disk}%"; fail=1; else echo "OK   disk ${disk}%"; fi
if systemctl is-active --quiet nginx; then echo "OK   nginx"; else echo "FAIL nginx"; fail=1; fi
exit ${fail:-0}
```
`chmod +x healthcheck.sh` karke chalao. Phir nginx band karke dobara chalao, ek FAIL dikhega aur exit code 1 hoga, `echo $?` se dekho. Aap Session 6 mein is script ko Bash ki poori taakat ke saath sudharoge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "method · logs · one change at a time · script it".]**

**(Voiceover):**
Recap: Linux ka kaam nabz, services, network aur ek tareeka. Aur jo roz karo wo script mein daalo. Ab Bash ko poori tarah seekhte hain, taaki ye script ek asli automation tool ban sake.
