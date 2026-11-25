# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-05_linux-sysadmin-and-troubleshooting

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,501 · **Episodes:** 4

---

# EPISODE 1: Server ki Sehat

## "Server Slow Hai"

Pichhle session mein Atithi ki building mein staff aaya, taale lage aur pehla guest serve hua. Aaj subah subah message aaya: website slow hai. Sabse aasaan lagta hai poori building ki bijli band karke dobara chalu kar dena, yaani server restart. Par isse wajah kabhi pata nahi chalti, aur kal wahi problem phir aayegi. Achha manager pehle round lagata hai: kitna staff kaam mein laga hai, desks bhari hain ya khaali, jagah bachi hai ya nahi. Server par yahi round chaar cheezon ka hai: CPU, memory, disk aur network. Is session mein hum ye round seekhenge, aur phir ek kharab din ko sambhalna. Is episode mein: server ki sehat aur processes.

## Round ki Chaar Commands: uptime, top, free, df

Round ki pehli command uptime. Ye batati hai server kitni der se chal raha hai, aur load average, yaani kitna kaam workforce ka intezaar kar raha hai. Workforce yaani CPU. top ek live board hai: kaun sa kaam sabse zyada CPU ya memory kha raha hai, wo sabse upar dikhta hai. free -h desks ka hisaab hai, yaani RAM. Yahan "available" asli aankda hai, sirf "free" nahi. Usi mein swap ki line bhi hai: swap wo dheema overflow room hai jahan kaam tab bheja jaata hai jab saari desks bhar jaayein. Swap bharne lage to samjho RAM kam pad rahi hai. df -h batata hai building mein jagah kitni bachi hai, yaani disk. Aur du -sh * dikhata hai kaun sa folder bhaari hai. nproc batata hai kitne CPU hain: load average ko isse milao, kyunki chaar CPU par load chaar ka matlab poora bhara, par ek CPU par wahi load chaar ka matlab teen kaam intezaar mein. Disk 100% bhar jaye to bahut saari cheezein ek saath toot jaati hain.

## Process: Work Order, Token Number aur Uski Zindagi

Server par har chalti cheez ek process hai. Hotel ki bhasha mein, ek work order jo abhi chal raha hai. Har work order ka ek token number hota hai, yaani PID, aur us supervisor ka token bhi, jisne ye kaam diya, yaani PPID, parent process ID. ps -ef mein dono columns dikhte hain. Aapka bash bhi ek process hai, aur usme chalayi har command uska child banti hai. Zindagi aisi chalti hai: parent ek child banata hai, child kaam karta hai, khatm hone par apna nateeja parent ko deta hai, aur parent use register se hata deta hai. ps aux mein STAT column haalat batata hai: R yaani chal raha hai, S yaani so raha hai aur kisi cheez ka intezaar kar raha hai, T yaani roka gaya hai, aur Z yaani zombie. Zombie wo work order hai jo poora ho chuka hai, par supervisor ne abhi uska nateeja uthaya nahi. Wo CPU ya memory nahi khaata, bas register mein ek line ghere rehta hai. Use kill nahi kar sakte, kyunki wo pehle hi khatm ho chuka hai; theek uske parent ko karna padta hai. Aur agar parent pehle khatm ho jaye to child anaath nahi rehta: use shift supervisor, yaani PID 1 wala systemd, god le leta hai. Ye saari jaankari kernel /proc folder mein rakhta hai.

## Kaam Rokna: Signals

Kisi kaam ko rokna ho to use signal bheja jaata hai. ps aux | grep nginx se process dhoondho aur PID lo. kill PID SIGTERM bhejta hai, yaani kandhe par haath rakh kar kehna ki kaam samet lo, taaki wo saaf-safai karke band ho. Agar na maane to kill -9 PID, SIGKILL, yaani machine ka plug kheench dena. Isme kaam adhoora chhoot sakta hai. Pehle polite, phir force, ye order yaad rakho. PID ki jagah naam se rokna ho to killall aur command ka naam. Aur ps ki TTY column batati hai kaam kis terminal se juda hai. Wahan sawaaliya nishaan ho to wo background ka kaam hai, jiska koi terminal nahi.

## Lab: CPU Chadhao, Pakdo, Roko

Lab. Ek terminal mein yes > /dev/null & chalao. Ye ek process background mein CPU khaata rahega. Doosre terminal mein top kholo aur yes ko sabse upar dekho. Ab ps -o pid,ppid,stat,cmd -C yes chalao: token number, supervisor ka token aur haalat, teeno ek line mein. Haalat R hogi. kill -STOP PID chalao aur wahi ps dobara dekho, ab T hai, kaam ruka hua hai aur CPU neeche aa gaya. kill -CONT PID se wo phir chal padta hai. Aakhir mein kill PID se use band karo. Ab aapne ek load ko dekha, pehchana, roka aur khatm kiya. Ye ek mini incident hai. Dhyaan rahe: production par kisi bhi process ko kill karne se pehle pata karo wo kya hai aur uska parent kaun hai.

## Recap aur Bridge

Recap: round ki chaar commands, work order yaani process, token yaani PID, uski haalat, aur signals se control. Ab un departments ki baat jo kabhi band nahi hote: services, aur unki logbooks.

---

# EPISODE 2: Services aur Logs

## Reboot ke Baad Website Gayab

Raat ko bijli gayi, subah building dobara khuli, par front desk band pada hai. Wajah: kal kisi ne use haath se khola tha, par shift supervisor ki subah wali list mein uska naam likha hi nahi. Server par yahi hota hai: reboot hua aur website wapas nahi aayi, kyunki service haath se start hui thi, boot par chalne ke liye enable nahi thi. Service wo department hai jo hamesha khula rehta hai. Unhe shift supervisor sambhalta hai, yaani systemd, aur usse baat karne ka tareeka hai systemctl.

## systemctl ki Commands

systemctl status nginx batata hai service chal rahi hai ya nahi, uska main PID kya hai, aur neeche uske aakhri kuch log lines. start aur stop chalu aur band. restart band karke chalu karta hai. reload bina band kiye nayi config padhwata hai, jo production ke liye behtar hai kyunki guests ka connection nahi tootta. Aur do alag cheezein yaad rakho: start department ko abhi kholta hai, enable uska naam subah ki list mein likhta hai. Dono alag hain, isliye aksar sudo systemctl enable --now nginx ek saath use hota hai. Yahi tareeka har service par chalta hai: sudo systemctl restart ssh staff entrance wali service ko dobara chalata hai. Red Hat family mein usi service ka naam sshd hai.

## Logbook Room: journalctl, /var/log aur logrotate

Har department apni logbook likhta hai, aur saari logbooks ek hi kamre mein rakhi hain: /var/log. Yahan do clerk kaam karte hain. Pehla rsyslog, jo seedhi text files likhta hai. Kaun si baat kis file mein jaati hai, ye /etc/rsyslog.conf mein likha hai. Ubuntu par login ki entries auth.log mein milti hain, Red Hat family mein secure mein. Doosra clerk systemd-journald hai. Uska register text nahi hota, isliye use cat se nahi, journalctl se padhte hain. journalctl -u nginx -n 50 us service ki aakhri pachaas lines dikhata hai, -f live follow karta hai, -p err sirf errors, aur --since "1 hour ago" samay ka filter hai. Ek baat aur: journal agar /run/log/journal mein likha ja raha hai to reboot par chala jaata hai. /var/log/journal folder ho to disk par bachta hai, aur Ubuntu par aam taur par aisa hi hota hai. Ab sawaal: logbooks bharti rahin to kamra bhar jayega. Isliye purane register archive hote hain, yaani logrotate. Uski config /etc/logrotate.conf mein do lines dekho: weekly, yaani har hafte naya register, aur rotate 4, yaani chaar purane rakho. Paanchwa bante hi sabse purana hat jaata hai. Pehle service ka status, phir uska log: ye jodi aapko zyadatar problems ka jawab degi.

## Lab: Service ko Todo aur Theek Karo

Lab: nginx ki config mein jaan-boojh kar ek galti karo, jaise /etc/nginx/nginx.conf mein ek line ke aakhir ka ; hata do. sudo nginx -t se config test karo, wo file aur line number ke saath error batayega. Dhyaan: line number aksar us line ke agli line ka hota hai jahan ; chhoota; humare test mein doosri line toot-i to error teesri line par aaya. Ab sudo systemctl restart nginx chalao, fail hoga. systemctl status nginx mein laal "failed" dikhega, aur journalctl -u nginx -n 20 mein wajah. Galti theek karo, nginx -t pass hoga, aur restart chalega. Seekh: pehle config test, phir restart, aur production mein reload ko prefer karo. Aur systemctl is-enabled nginx se pakka kar lo ki ye department subah ki list mein hai.

## Recap aur Bridge

Recap: systemctl se control, start aur enable ka farq, journalctl aur /var/log se jaanch, logrotate se archive, aur config test se bachav. Ab network: jab service chal rahi ho par bahar se koi pahunch na paaye.

---

# EPISODE 3: Network ke Sawaal

## Service Chal Rahi Hai, Phir Bhi Nahi Khulti

Front desk khula hai, staff baitha hai, phir bhi guest nahi pahunch raha. Ab problem building ke andar nahi, raaste mein hai. Guest ne directory mein sahi address paaya? Yaani DNS sahi IP de raha hai? Sadak us address tak jaati hai? Yaani route theek hai? Gate ka guard rok to nahi raha? Yaani firewall? Aur front desk sahi darwaze par baitha hai? Yaani app sahi port par sun raha hai? In sawaalon ko ek ek karke todna hi networking troubleshooting hai, aur hum andar se bahar ki taraf chalenge.

## ip, ss aur ping

ip a aapke interfaces aur unke IP addresses dikhata hai. IP address building ka street address hai. ip route batata hai traffic kis raaste se bahar jayega. Usme default via wali line aapka default gateway hai, yaani colony se bahar nikalne wala mod. ss -tulpn dikhata hai kaun sa process kis darwaze par sun raha hai, yaani kis port par LISTEN kar raha hai. Agar aapka app 8080 par sunna chahiye aur ss mein wo dikh hi nahi raha, to app ki problem hai, network ki nahi. ping batata hai ki doosri machine tak pahunch hai ya nahi. Lekin kai servers ping band rakhte hain, to ping na chale iska matlab hamesha down nahi hota.

## Pakka Address: Static IP

Aam taur par machine ko address apne aap milta hai, DHCP se, aur wo badal bhi sakta hai. Server ka address badalta rahe to guest use dhoondhega kaise? Isliye server ko pakka address dete hain, yaani static IP. Iske liye teen cheezein chahiye: address, gateway, jo ip route se milta hai, aur DNS server. Ubuntu server par ye /etc/netplan ke andar ek YAML file mein likha jaata hai, aur sudo netplan try use lagata hai. try ki khoobi ye hai ki agar aapka connection toot jaye to wo kuch der mein purani setting wapas le aata hai. Red Hat family mein ye kaam NetworkManager karta hai, aur uske teen raaste hain: nmtui, jo ek menu wala screen hai; nmcli, jo command line hai; ya seedha connection ki config file badalna. Teeno ke baad connection ko dobara uthana padta hai, tabhi nayi setting lagti hai. Ek chetavni: ye abhyas sirf apne laptop ki local VM par karo. Cloud ki VM ka address landlord deta hai, yaani cloud provider. Wahan andar se address badla to aap khud bahar ho jaoge.

## curl aur DNS

curl se aap khud guest ban kar darwaza khatkhata sakte ho. curl -I sirf headers lata hai, curl -v poori baat-cheet dikhata hai. Agar app localhost par curl se chal raha hai par bahar se nahi, to gate ka guard dekho. DNS wo directory hai jo hotel ke naam ko address mein badalti hai. dig example.com +short domain ka IP batata hai. Agar IP galat ya khaali hai, to problem DNS ki hai, server ki nahi. Common darwaze yaad rakho: 22 staff entrance yaani SSH, 80 public entrance yaani HTTP, 443 secured public entrance yaani HTTPS.

## Lab: Gate ka Guard aur Layer by Layer Debug

Firewall gate ka guard hai, jiske paas list hai ki kaun se darwaze tak aane ki ijaazat hai. Ubuntu par ye guard ufw hai. Lab: sabse pehle apna raasta bachao. sudo ufw allow OpenSSH chalao, phir sudo ufw enable, warna aap staff entrance se hi bahar ho sakte ho. Ab nginx chalu rakho aur andar se bahar chalo. Ek: ss -tulpn | grep :80, front desk darwaze par hai? Do: curl localhost, andar se jawab aata hai? Teen: sudo ufw status, guard ki list mein 80 hai? Chaar: apne laptop se curl http://SERVER_IP. Ye fail hoga. Ab sudo ufw allow 80/tcp chalao aur chautha kadam dobara karo, is baar chalega. Red Hat family mein yahi guard firewalld hai, aur uski command firewall-cmd. Wo gates ko zones mein baant-ta hai, yaani alag gate ke liye alag suraksha star. Aur wahan ek aadat chahiye: --permanent ke saath rule likho, phir --reload karo, warna rule reload ya reboot par chala jaata hai. Use hum agle session, 05B, mein haath se chalayenge. Aur cloud par ek guard aur hota hai, security group, jo building ke bahar landlord ka guard hai.

## Recap aur Bridge

Recap: ip se address aur gateway, ss se darwaze, static IP se pakka address, curl aur dig se bahar ki jaanch, aur guard ki list. Hamesha ek hi order: andar se bahar. Ab in sabko ek method mein baandhte hain, aur apni pehli health-check script likhte hain.

---

# EPISODE 4: Troubleshooting ka Tareeka aur Health-Check Script

## Ghabrahat vs Method

Aaj Atithi ka kharab din hai: guests shikayat kar rahe hain aur teen phone ek saath baj rahe hain. Ghabrahat mein hum random switch dabate hain, yaani random commands chalate hain, aur ek aur galti kar dete hain. Achha engineer pehle method lagata hai. Ye method itna simple hai ki aap ise kisi bhi problem par laga sakte ho: kya dikh raha hai, kya badla, aur kahan se shuru karein.

## 5-Step Troubleshooting Method

Ek, symptom ko saaf shabdon mein likho: kya ho raha hai, kab se, aur kis par asar hai. "Site down hai" kaafi nahi; "checkout page do baje se 502 de raha hai" kaam ki baat hai. Do, pata karo kya badla: naya deploy, config, traffic, ya koi certificate jo expire ho gaya. Teen, logbooks aur board dekho, yaani logs aur metrics. Yahan is session ka poora round kaam aata hai: top aur df -h se sehat, systemctl status aur journalctl se service, ss aur curl se network. Chaar, ek hi hypothesis chuno aur ek hi cheez badal kar test karo, ek saath kai cheezein nahi, warna pata nahi chalega kisse theek hua. Paanch, fix ke baad verify karo ki problem sach mein gayi, aur kya hua wo likh lo. Yahi likhi hui baat agli baar ka runbook ban jaati hai. Aur AI assistant yahan madad kar sakta hai: use log ki lines do aur poochho ki inka matlab kya ho sakta hai. Par command chalane se pehle use khud samjho.

## Health-Check Script ka Design

Manager roz wahi round lagata hai. Jo checks aap roz haath se karte ho, unhe ek slip par likh do, yaani script bana do. Ek health-check script ye dekhegi: disk kitna bhara hai, memory kitni bachi hai, zaroori service chal rahi hai ya nahi, aur port khula hai ya nahi. Output saaf hona chahiye: OK, WARN ya FAIL. Aur exit code bhi, taaki monitoring ya cron ise apne aap samajh sake: sab theek hai to 0, warna non-zero.

## Lab: Pehli Health-Check Script

Lab. Ye script likho:

chmod +x healthcheck.sh karke ./healthcheck.sh chalao. Phir sudo systemctl stop nginx karke dobara chalao, ek FAIL dikhega aur exit code 1 hoga, echo $? se dekho. Aakhir mein nginx ko wapas start kar do. Aap Session 6 mein is script ko Bash ki poori taakat ke saath sudharoge.

## Recap aur Bridge

Recap: manager ka round, yaani sehat, services, logbooks aur network, aur kharab din ke liye paanch kadam ka tareeka. Aur jo roz karo wo script mein daalo. Ab ek building chalana aapko aata hai. Par abhi teen cheezein baaki hain: nayi khaali jagah ko kamron mein kaise badalte hain, yaani disks aur LVM; guests ke liye front-of-house kaise khulta hai, yaani Apache web server; aur chaabi ke upar ki doosri suraksha, yaani SELinux. Ye sab agle session, 05B, mein.
