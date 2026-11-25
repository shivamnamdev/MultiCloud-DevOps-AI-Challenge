# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-06_bash-scripting

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,677 · **Episodes:** 4

---

# EPISODE 1: Pehli Slip

## Wahi Paanch Commands, Roz

Pichhle session mein manager ka daily round seekha: uptime, free, df, service ka status, aur logbook. Manager roz subah wahi paanch instructions desk par bolta hai. Kisi din ek bhool jaaye to round adhoora rehta hai. Ab socho wo ek parchi par likh de, aur assistant parchi padh kar sab kar de. Linux mein wo parchi bash script hai: ek file jisme commands likhi hain, aur wo ek saath chal jaati hain. Desk, yaani jahan aap instruction bolte ho, shell hai, aur is session mein hum us desk ke liye parchiyan likhna seekhenge. Parchi mein sirf commands nahi hoti. Usme variables, faisle aur dohrav bhi hote hain, aur wahi use ek chhote program mein badal dete hain. Is episode mein: pehli slip.

## Shebang, Chalana aur Variables

Slip ki pehli line shebang hoti hai: #!/usr/bin/env bash. Ye batati hai ki is parchi ko padhne wala assistant bash hai. Phir wahi cheez jo Session 4 mein seekhi thi: parchi par execute ka haq do, chmod u+x hello.sh, aur chalao ./hello.sh. Variable ek naam wala dabba hai. name="Asha" mein = ke dono taraf space nahi hota. Space daala to bash socha ki name koi command hai. Dabba kholne ke liye name. Double quotes ke andar dabba khul jaata hai, single quotes mein nahi, wahan jo likha hai wahi print hota hai. Aur ek aadat abhi se: variable ko hamesha double quotes mein likho, "name". Warna agar uski value mein space ho, jaise ek folder ka naam booking site, to bash use do tukdon mein tod deta hai aur command galat chal jaati hai.

## Arguments, Output aur Input

Parchi ko bahar se kuch dena ho to arguments. ./greet.sh Asha 25 mein 0 parchi ka apna naam hai, 1 Asha, 2 25. # batata hai kitne arguments aaye, aur @ sabhi arguments ek saath. Kisi command ka jawab dabbe mein rakhna ho to ( ) lagao: today=(date +%F) aaj ki tareekh ek variable mein rakh deta hai. Purane scripts mein aap ulte quote, yaani backticks, bhi dekhoge, wahi kaam karte hain, par ( ) padhna aasaan hai aur uske andar $( ) bhi aa sakta hai. Aur agar parchi chalate waqt insaan se kuch poochna ho to read -p "Name: " name. In teen cheezon, argument, command ka output aur input, se ek hi parchi alag alag kaam ke liye chal jaati hai. Har baar usse badalna nahi padta.

## Jawab ka Raasta: Redirect aur Pipe

Parchi jo bhi kare, uska jawab kahin na kahin jaata hai, aur ye raaste samajhna zaroori hai. Normal jawab ek raaste se aata hai, aur galtiyan ek alag raaste se, jise error stream kehte hain. > jawab ko ek file mein likhta hai, aur purani file mita deta hai. >> purani file ke aakhir mein jodta hai, jo logbook ke liye sahi hai. Galtiyon ko alag file mein bhejna ho to 2>. Aur > out.txt 2>&1 ka matlab hai: normal jawab bhi aur galtiyan bhi, dono ek hi file mein. Pipe, yaani |, jo Session 3 mein dekha tha, ek command ka jawab seedha doosri command ko haath mein de deta hai: ls | wc -l folder ki files ginta hai. Aur /dev/null ek nali hai jisme jo bhi dalo gayab ho jaata hai. Cron wale episode mein >> log 2>&1 isi ka seedha upyog hoga: parchi ka har jawab, galtiyon ke saath, ek logbook mein.

## Lab: Building ki Report Slip

Lab. Ye slip likho aur info.sh naam se save karo:

chmod u+x info.sh karo aur ./info.sh chalao. Ab ek badlaav: parchi ko ek folder ka naam argument mein do, aur wo us folder ka size bhi print kare. Isliye aakhir mein ek line jodo: du -sh "1". Chalao ./info.sh ~/atithi-booking. Agar abhi Session 16 nahi hua to koi bhi folder chalega. Ek parchi, do tarah ke kaam, aur is baar "1" quotes mein hai, to space wale folder ke naam par bhi chalegi. Bina argument chalaoge to du: invalid zero-length file name aayega; uska ilaaj Episode 3 mein hai.

## Recap aur Bridge

Recap: shebang, variables, quotes, arguments, command ka output aur input. Abhi hamari parchi sirf seedhi line mein chalti hai. Ab use faisle lena sikhate hain: agar ye ho to wo, warna kuch aur.

---

# EPISODE 2: Faisle aur Doharav

## Slip Soch Sake To?

Ek parchi jo bina dekhe chale, chhoti galti par bada nuksaan karti hai. Parchi kehti hai guest register archive mein copy karo, aur register hai hi nahi. Assistant bina dekhe khaali folder thama deta hai, aur kisi ko pata bhi nahi chalta. Achhi parchi pehle poochhti hai: file hai? Building jawab de rahi hai? Disk bhari to nahi? Faisle ke liye conditions hain, aur ek kaam baar baar karne ke liye loops.

## if, test aur case

Faisle ka dhaancha hai if [ condition ]; then ... fi. Square brackets ke andar spaces zaroori hain. Ek [ bhi darasal ek chhoti command hai, isliye uske baad space chahiye. File hai ya nahi, ye -f se. Folder ke liye -d, khaali string ke liye -z. Numbers ki tulna -eq, -gt, -lt se, aur strings ki == se. Ye dono alag hain, aur isi mein aksar galti hoti hai. [[ 95 > 100 ]] bhi sach nikalta hai, kyunki > akshar ke kram se tulna karta hai; numbers ke liye -gt. Aur [ -ff ] bina space ke chupchap sach ho jaata hai, jabki [-f seedha "command not found" deta hai. Ab wo galti: [ "disk" -gt 90 ] number ki tulna hai, [ "$cmd" == "start" ] string ki. Agar kai alag raaste hon, jaise start, stop, restart, to lambi if ki chain ki jagah case saaf padhta hai. Har raaste ke aakhir mein do semicolon, aur sabse neeche *), yaani jo kisi mein na aaye uska default jawab.

## for aur while

for f in *.log; do echo "$f"; done har log file par ek ek kaam karta hai. Ginti ke liye for i in {1..5}. Aur ek file ki har line par kaam ho, jaise building ki list, to while read -r line; do ...; done < list.txt. -r ka matlab hai ki backslash ko jaisa hai waisa rehne do. Ek chhoti sachchai: us loop ke andar agar koi command, jaise ssh, bhi input padhne lage to wo file ki baaki lines nigal leta hai, aur loop do line mein hi khatam ho jaata hai. Us command par -n lagao, ssh -n, aur kaam chalega. Loop ke andar conditions bhi laga sakte ho, jaise sirf bade files pakadna. Aur DevOps ki roz ki sachchai: building ki list par ek loop chalana, har ek ko jaanchna, yahi automation ki shuruaat hai.

## && aur ||, aur Double Bracket

Do chhote jodne wale nishaan bahut kaam aate hain. && ka matlab: pehli command theek chali to hi doosri chalao. mkdir releases && cd releases: folder bana to andar jao. || ka matlab: pehli command fail hui to hi doosri chalao. ping -c1 8.8.8.8 || echo "no network". Dono ko ek lambi parchi ki jagah ek line mein likha ja sakta hai, par line lambi ho to saaf if hi behtar hai. Ab ek aur hissa. Bash mein [ ] ke alawa double bracket [[ ]] bhi hai. Wo sirf bash mein chalta hai, par uske do faayde hain: isme pattern milaye ja sakte hain, jaise [[ name == a* ]], aur isme variable ke quotes ki utni chinta nahi. Wo ek hi line mein && bhi samajhta hai: [[ -f f && -r $f ]]. Seedhi baat: agar parchi sirf bash par chalegi, to [[ ]] use karo. Agar sab shells par chalani ho, to [ ].

## Lab: Buildings ka Roll Call

Lab. Maan lo Atithi ki kai buildings hain. Ek file servers.txt mein unke naam likho: localhost, 8.8.8.8 aur ek galat naam. Phir ye slip:

Chalao aur UP aur DOWN dekho. >/dev/null 2>&1 ka matlab: ping ka apna shor chhupao, taaki sirf humara message dikhe. Aakhir mein jo ginti aati hai, wo agle episode mein kaam aayegi. Dhyaan rahe: kuch buildings ping ka jawab hi nahi deti, to DOWN ka matlab pakka band hona nahi, "ping ka jawab nahi" hai.

## Recap aur Bridge

Recap: faisle aur dohrav. Par ek sawaal baaki hai. Ye parchi agar beech mein kisi kadam par fail ho jaaye, to kya wo aage chalti rahegi? Agla episode isi ke baare mein hai: parchi ko surakshit kaise banate hain.

---

# EPISODE 3: Safe Slip

## Slip Jo Galti ke Baad Bhi Chalti Rahi

Ek release ki parchi mein teen kadam hain: nayi website ki files rakho, unhe jaancho, aur purana release hata do. Kadam do fail ho gaya, par parchi ruki nahi. Teen chalu hua aur purana release bhi chala gaya. Ab na naya hai, na purana, aur guests ko khaali page dikh raha hai. Bash by default galti par rukta nahi, wo agli line par badh jaata hai. Isliye bash ki sabse zaroori seekh: parchi ko safe mode mein likho.

## set -euo pipefail aur Exit Code

Parchi ki shuruaat mein ek line likho: set -euo pipefail. -e ka matlab: koi command fail ho to parchi wahin ruk jaaye. -u ka matlab: jo variable kabhi bana hi nahi, use chhoo to error do. Ye rm -rf "DIR/" jaisi bhayanak galti se bachata hai, jahan DIR khaali ho aur command seedhi jad par chal jaaye. pipefail ka matlab: pipe ke beech ka koi hissa fail ho to bhi poora pipe fail maano. Har command ke baad uska status ? mein hota hai, aur zero ka matlab sab theek. echo $? se khud dekh lo. Ek chhoti sachchai: -e ki ek seema hai. if ke andar ya || ke saath chalayi gayi command ke fail hone par wo parchi nahi rokta, kyunki wahan fail hona ek jawab hai, galti nahi. Aur safai ke liye trap 'echo cleanup' EXIT ek aisa kaam hai jo parchi ke har tarah se khatam hone par chalta hai, chahe sab theek ho ya na ho.

## Functions: Ek Baar Likho, Baar Baar Use Karo

Jo kaam parchi mein baar baar likhna pade, use function bana do: log() { echo "[(date +%T)] *"; }. Ab har jagah sirf log "disk check" likho. Function ke arguments bhi 1, 2 hote hain, parchi ke apne arguments ki tarah. local lagane se variable function ke andar tak rehta hai aur bahar ki cheezein kharab nahi karta. return ek status code deta hai, yaani zero ya non-zero, text nahi. Text wapas chahiye to function usse echo kare aur bahar ( ) use karo. Ek jaal: jis function ka jawab ( ) se pakadna ho, uske andar ka log agar stdout par likhe, to wo bhi pakda jaata hai; humne pct=(check_disk) mein log ki line aur number dono ek saath paaye. log ko >&2 par bhejo, to sirf number aata hai. Aur ek achha dhancha: poori parchi main() function mein rakho, aur sabse neeche ek line main "@". Padhne wale ko upar se hi pata chal jaata hai ki parchi kya kya karti hai.

## Parchi Galat Chale to: bash -x aur shellcheck

Parchi galat chale to ghabrane ki zaroorat nahi, bash khud batata hai ki wo kya kar raha hai. bash -n script.sh parchi ko chalaye bina sirf uska vyakaran jaanchta hai. bash -x script.sh har command ko chalane se pehle ek plus ke saath dikha deta hai, aur variable ki asli value bhi. Isse turant dikh jaata hai ki kaun si line mein galat value aayi. Poori parchi nahi, sirf teen lines ko dekhna ho to un se pehle set -x aur baad mein set +x likho. Doosra aujaar hai shellcheck. sudo apt install shellcheck, phir shellcheck script.sh, aur wo parchi padh kar bata deta hai ki kahan quotes chhoot gaye, kahan variable galat hai. Ye parchi ka grammar-checker hai, aur ek achhi aadat hai ki har naye script par ek baar chalao.

## Lab: Session 05 ki Health-Check Parchi ko Sudharo

Lab. Session 5 ki healthcheck.sh yaad hai? Aaj use asli parchi banate hain.

Bina argument chalao: saaf usage message aata hai. ./healthcheck.sh nginx chalao: dono OK. Ab ./healthcheck.sh nginx 1 chalao, disk ki limit ek percent, to FAIL aayega aur echo ? mein 1. Ek nayi cheez dekho: {2:-90} ka matlab hai doosra argument diya ho to wo, warna 90. Ek ek jagah ek hi kaam, aur parchi ka aakhri jawab exit code mein. Isi tarah ki parchi ko cron aur monitoring bina insaan ke padh sakte hain.

## Recap aur Bridge

Recap: safe mode, functions, default values aur exit codes. Ab ek parchi ban gayi jo bharosemand hai. Par wo abhi bhi tabhi chalti hai jab aap desk par ho. Agla episode: parchi ko timetable par rakhna, aur ek asli backup.

---

# EPISODE 4: Timetable

## Raat Do Baje Kaun Jaage?

Booking website ka backup raat do baje lena hai, jab guests kam hote hain. Aap to so rahe honge. Linux ke paas ek timetable hai jo aapke bina parchiyan chalata hai, aur uska naam cron hai. Aaj ke episode ka maksad: ek parchi likhna jo booking website ka backup le, purane backups hataye, aur timetable se khud chale.

## cron ka Syntax

crontab -e se aap apna timetable likhte ho, aur crontab -l use dikhata hai. Har line mein paanch time ke khaane aate hain, aur uske baad command. Khaane hain: minute, ghanta, mahine ka din, mahina, aur hafte ka din. Sitara matlab "har". To 0 2 * * * matlab har din ke do baje, zero minute par. /15 * * * har paandrah minute mein. 0 9 * * 1 har somvaar subah nau baje. Ek zaroori baat: cron ka apna environment bahut chhota hota hai. Aapka login wala PATH wahan nahi hota. Isliye parchi ka poora path likho, jaise /home/ubuntu/backup.sh, aur uska jawab ek log file mein bhejo: >> /var/log/backup.log 2>&1. Warna agar kuch toota to kahin likha hi nahi milega.

## Backup Slip ka Design

Achhi backup parchi paanch kaam karti hai. Pehla, source folder hai ya nahi, ye jaanchna. Doosra, tar.gz banana, jisme naam mein tareekh aur samay ho, taaki har baar alag file bane. Teesra, jaanchna ki archive sahi bani hai: tar -tzf uske andar ki files ki list deta hai, aur list na aaye to archive kharab hai. Chautha, purane backups hatana, jaise find /backups -name "backup-*.tar.gz" -mtime +7 -delete, yaani saat din se purane. Paanchwa, ek line log mein likhna. Aur ek rule jo is parchi se bhi bada hai: backup kabhi usi disk par mat rakho jahan asli data hai. Disk gayi to dono gaye.

## Lab: Booking Site ka Backup aur cron

Lab. Ye parchi backup.sh mein likho:

chmod u+x backup.sh karo aur chalao ./backup.sh ~/atithi-booking. Ek .tar.gz banegi. Ab timetable: crontab -e mein ye line jodo, apna poora path likh kar: /2 * * * /home/aap/backup.sh /home/aap/atithi-booking >> /tmp/backup.log 2>&1. Do minute baad doosra backup aur log mein nayi line dikhegi. Dhyaan rahe, /tmp sirf abhyas ke liye hai, asli backup kisi doosri jagah, jaise cloud storage mein jaana chahiye, jo hum S3 ke session mein karenge. Test ke baad timetable se do-minute wali line zaroor hata do, warna folder bharta jayega. Ek kami humne pakdi: isi minute dobara chalane par agar source galat ho, to tar -czf pehle se bani achhi file ko 20 byte ki khaali file bana deta hai, aur tar -tzf use bhi theek maanta hai. Ilaaj: pehle file.part naam par banao, jaancho, aur tabhi mv se asli naam do.

## Timetable Gadbad Kare to

Timetable ki line daal di, aur kuch chala hi nahi. Pehle dekho cron ne parchi uthayi ya nahi. Ubuntu par grep CRON /var/log/syslog ya journalctl -u cron uska logbook hai. Red Hat family mein wahi service crond hai aur uska log /var/log/cron mein. Agar cron ne parchi uthayi par wo fail hui, to teen aam wajah hain. Ek, relative path: parchi ke andar ./data likha hai, par cron ka kaam karne ka folder alag hota hai. Poora path do. Do, PATH: cron ke paas aapka login wala PATH nahi hota. Timetable ke upar PATH= aur SHELL=/bin/bash likh sakte ho. Teen, percent ka nishaan. Crontab ki line ke andar % ka matlab nayi line hota hai, isliye date +%F seedha crontab mein likhna ho to \%F likhna padta hai. Isliye date wali cheezein parchi ke andar rakho, timetable mein nahi. Ek aur khatra: agar ek backup abhi chal raha hai aur timetable doosra shuru kar de, to dono bhidte hain. flock -n /tmp/backup.lock ./backup.sh ... doosre ko chalne hi nahi deta. Aur @reboot ya @daily jaise chhote naam bhi hote hain, jo aam mauqon par saaf padhe jaate hain.

## Recap aur Bridge

Recap: bash se aap Linux ke roz ke kaam ko automate kar sakte ho. Parchi likhna, use surakshit banana, aur timetable par chadhana. Par jab parchi mein JSON padhna ho, landlord ke office ko phone karna ho, ya logic bada ho jaaye, to bash thakane lagta hai. Agle session mein ek trained operations officer aata hai: Python, aur uska landlord ke office tak ka phone, boto3.
