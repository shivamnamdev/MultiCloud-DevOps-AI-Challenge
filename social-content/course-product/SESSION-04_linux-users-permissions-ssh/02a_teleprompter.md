# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-04_linux-users-permissions-ssh

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,796 · **Episodes:** 4

---

# EPISODE 1: Users, Groups aur sudo

## Sabke Paas Master Key Ho To?

Pichhle session mein Atithi Hotels ko apni pehli building mili thi. Ab socho is building mein dus staff hain, aur sabke paas master key hai. Ek ne galti se records room khaali kar diya. Ab pata nahi kisne kiya, aur rok bhi koi nahi sakta tha. Server par bilkul yahi hota hai jab dus developers root se login karte hain aur ek galti se zaroori folder hata deta hai. Linux ka user system isi problem ke liye hai: har staff ki apni pehchaan, aur utni hi power jitni kaam ke liye zaroori hai. Is session mein hum building mein staff rakhenge aur kamron par taale lagayenge. Is episode mein: users, groups aur sudo.

## Chaar Tarah ka Staff, UID aur Staff Register

Pehle ek rule yaad rakho: Linux ke users hotel ka staff hain, guests nahi. Guest yaani website ka end user, aur use kabhi staff ID card nahi milta. Staff chaar tarah ka hota hai. Root is building ka general manager hai, jiske paas master key hai. Uska UID, yaani ID card ka number, 0 hota hai, aur wo kuch bhi kar sakta hai. Local user aam staff hai, jise root ne rakha hai: uska apna quarter, yaani home directory, aur limited rights. Inke UID aam taur par 1000 se shuru hote hain. System user insaan hota hi nahi. Wo ek hi kaam wala service staff hai, jaise web server ka user, aur wo login nahi karta. Aur sudo user wo local user hai jise zaroorat par master key udhaar milti hai. Isiliye rule ye hai: roz ka kaam normal user se, aur zaroorat padne par hi power uthao. Staff ki jaankari staff register mein hoti hai, yaani /etc/passwd. Uski har line mein saat khaane hote hain: naam, password ki jagah ek x, UID, group ka ID, ek comment, home directory aur default shell. Wo x batata hai ki password yahan nahi hai. Uska hash ek band tijori mein rehta hai, yaani /etc/shadow, jise aam staff padh nahi sakta.

## Naya Staff, Home Department aur Extra Cards

Naya staff rakhte hain. sudo useradd -m -s /bin/bash asha ek naya user banata hai. -m uska quarter yaani home directory banata hai, aur -s uska shell tay karta hai. Do aur options kaam ke hain: -u se UID aap khud dete ho, aur -c se comment, jaise poora naam. UID na do to Linux pichhle user ke baad wala number de deta hai. tail -1 /etc/passwd se register ki aakhri line dekho, asha wahin milegi. sudo passwd asha password set karta hai. Ab departments. Group ek department ki tarah hota hai. Har staff ka ek home department hota hai, yaani primary group, aur ye sirf ek ho sakta hai. Uske upar kitne bhi extra department cards mil sakte hain, yaani secondary groups. useradd mein chhota -g primary group deta hai aur bada -G secondary. sudo groupadd devs department banata hai, aur sudo usermod -aG devs asha asha ko us department ka card deta hai. Yahan -a ka matlab append hai, aur use bhoolna khatarnaak hai, kyunki tab asha ke baaki department cards chhin jaate hain, yaani baaki secondary groups hat jaate hain. Card wapas lena ho to sudo gpasswd -d asha devs. id asha batata hai ki user kis kis group mein hai.

## ID Card ki Expiry: Password Policy

Atithi mein ID card hamesha ke liye nahi banta. Uski expiry hoti hai aur renewal ke rules hote hain. Linux mein yahi password policy hai. sudo chage -l asha asha ki policy dikhata hai. sudo chage -M 90 asha ka matlab: nabbe din mein password badalna hi hoga. Chhota -m do badlaav ke beech kam se kam din tay karta hai, aur -W batata hai expiry se kitne din pehle warning shuru ho. Naye users ke liye default numbers /etc/login.defs file mein likhe hote hain. Ek shabd aur: inactive period. Password expire hone ke baad itne din tak user purane password se login karke naya bana sakta hai. Uske baad account band, aur admin ko beech mein aana padta hai. Ab maan lo ravi naam ka staff lambi chhutti par hai. sudo usermod -L ravi uska password lock karta hai, aur -U kholta hai. Tijori mein lock hua password ek ! se shuru hota hai. Dhyaan: jis user ka password kabhi set hi nahi hua, use -U se kholne par Ubuntu mana kar deta hai, "passwordless account" ke darr se, isliye pehle passwd se password do. Dhyaan rahe, ye sirf password ko rokta hai. SSH key se login tab bhi chal sakta hai. Aur jab staff company chhod de, sudo userdel -r ravi user ko hata deta hai, aur -r uska quarter bhi khaali kar deta hai.

## Lab: sudo ka Sahi Use

Hotel mein duty manager general manager nahi hota. Par zaroorat padne par wo master key udhaar le sakta hai, aur har baar register mein entry hoti hai. Linux mein yahi sudo hai. Lab: asha ko sudo group mein jodo, Ubuntu par sudo usermod -aG sudo asha. Red Hat family mein isi group ka naam wheel hota hai. Ab asha ke naam se login karo, su - asha se. Bina sudo ke apt update chalao, error milegi. Phir sudo apt update chalao, kaam karega. Sudo aapka password maangta hai aur har command ka log rakhta hai, isliye ye root login se behtar hai: pata rehta hai kisne kya kiya. Aur sudo rules badalne ho to seedha file mat kholo, sudo visudo use karo, kyunki wo syntax check karta hai aur aapko lock hone se bachata hai. Us file ki ek line aisi dikhti hai: asha ALL=(ALL) ALL, yaani asha har command chala sakti hai. Aakhri ALL ki jagah ek command ka poora path likho to sirf wahi command milti hai. Aur naam se pehle % lagao to rule poore group par lagta hai.

## Recap aur Bridge

Recap: aam staff yaani normal user, general manager yaani root, home department aur extra cards yaani primary aur secondary groups, ID card ki expiry yaani password policy, aur duty manager ki udhaar wali master key yaani sudo. Ab sawaal: kis staff ko kis kamre mein kya karne diya jaye, ye kaun tay karta hai? Wo hain kamron ke taale, yaani file permissions, agle episode mein.

---

# EPISODE 2: File Permissions

## Ek Taala, Teen Ring

Atithi ki building mein har kamre aur har almari par ek teen-ring taala laga hai. Kamra yaani directory, almari yaani file. Pehli ring owner ke liye hai, jisne file banayi. Doosri ring uske department ke liye, yaani group. Teesri ring baaki sab staff ke liye, yaani others. Aur har ring par teen haq hote hain: dekhna yaani read, badalna yaani write, aur chalana yaani execute. Ye 3 gune 3 ka hisaab hi Linux permissions ka poora khel hai.

## ls -l Padhna aur Octal Numbers

ls -l ki pehli column dekho: -rwxr-xr--. Pehla akshar file ka type hai, phir teen teen ke group, yaani hamari teen rings: owner rwx, group r-x, others r--. Number se bhi likha jaa sakta hai: read ka 4, write ka 2, execute ka 1. To rwx yaani 7, r-x yaani 5, r-- yaani 4. Is file ki permission 754 hai. Aur ek baat yaad rakhna: kamre par, yaani directory par, x ka matlab hota hai us kamre ke andar ja sakna.

## chmod aur chown

Taale ki rings ghumane ke liye chmod. Number se: chmod 640 secret.txt owner ko read-write, group ko read, others ko kuch nahi. Symbolic tareeke se: chmod u+x deploy.sh owner ko execute deta hai, aur minus se haq wapas liya jaata hai. Barabar ka nishaan, jaise chmod g=rx deploy.sh, purani setting mita kar nayi likhta hai, aur a ka matlab teeno rings ek saath. Kamre ki nameplate badalne ke liye, yaani owner badalne ke liye, chown: sudo chown asha:devs app.log owner asha aur group devs kar deta hai. Aur ek khatarnaak aadat: chmod 777 kabhi mat lagao. Ye taala hata kar darwaza khula chhod dene jaisa hai, sab ko sab kuch mil jaata hai, aur security audits mein pehli galti yahi pakdi jaati hai.

## Default Taala aur Teen Khaas Nishaan

Naya kamra bante hi uspar taala kis setting mein lagta hai? Ye umask tay karta hai, yaani default taala. umask chalao: root par 0022 dikhega, aam user par 0002 ya 0022. umask wo haq hain jo hata diye jaate hain. Directory 777 se shuru hoti hai, 022 hatao to 755. File 666 se shuru hoti hai, kyunki nayi file ko execute apne aap kabhi nahi milta, to 644 banta hai. Ab teen khaas nishaan, jo ls -l mein kabhi kabhi x ki jagah dikhte hain. Pehla SUID, owner ki ring mein chhota s. Ye ek aisi machine hai jo chalane wale ko us ek kaam ke liye owner ki power de deti hai. ls -l /usr/bin/passwd dekho. Password badalne par tijori, yaani /etc/shadow, badalti hai, jise sirf root likh sakta hai. passwd par SUID hai, isliye aam staff bhi apna password badal paata hai. Doosra SGID, group ki ring mein s. Directory par lage to uske andar bani har nayi file us directory ke group ki ho jaati hai, yaani department ke kamre mein rakha saaman department ka. Team ke shared folder par chmod g+s isi kaam aata hai. Teesra sticky bit, others ki ring mein t. ls -ld /tmp dekho. /tmp building ka lost-and-found hai: koi bhi saaman rakh sakta hai, par hata sirf wahi sakta hai jiska wo saaman hai.

## Lab: Script Chalao aur Secret Chhupao

Lab. echo 'echo hello devops' > hello.sh se script banao, ./hello.sh chalao, "Permission denied" aayega kyunki execute ka haq nahi hai. chmod u+x hello.sh ke baad chalega. Ab ek secret.txt banao, chmod 600 secret.txt lagao, yaani sirf owner ki ring khuli hai, aur doosre user se cat karke dekho, access nahi milega. Aakhir mein umask chalao, ek nayi file aur ek naya folder banao, aur ls -l se dekho ki default taale ka hisaab mila ya nahi. Ye principle of least privilege ka pehla abhyas hai: har staff ko utna hi haq jitna uske kaam ke liye chahiye. Ek baat aage ke liye yaad rakho: jab hum Git seekhenge, to git diff mein file ke mode ki line, jaise 100644 aur 100755, dikhegi. 755 mein execute ki ring khuli hai. Agar deploy.sh vault mein bina execute ring ke gayi, to agle designer ke laptop par wo Permission denied degi, aur ilaaj wahi chmod u+x hai.

## Recap aur Bridge

Recap: teen ring, teen haq, number ka hisaab, chmod aur chown, default taala yaani umask, aur teen khaas nishaan: SUID, SGID aur sticky bit. Ab kamre to safe hain, par staff building ke andar aata kaise hai? Staff entrance se, yaani SSH se. Aur us darwaze ka sabse safe tareeka hai SSH keys. Agle episode mein.

---

# EPISODE 3: SSH Keys

## Password ki Problem

Hamari building public road par hai, aur uska staff entrance, yaani SSH ka darwaza number 22, road se dikhta hai. Road se guzarne wala koi bhi keypad par code try kar sakta hai. Internet par jo bhi server khula hai, uspar kuch hi minute mein anjaan logon ke password guess karne ke attempts shuru ho jaate hain. Password kitna bhi accha ho, guess ya leak ho sakta hai. SSH keys is problem ka ek bahut behtar jawab hain: ek lambi jodi jise guess karna lagbhag namumkin hai, aur jiska ek hissa kabhi network par jaata hi nahi.

## Public aur Private Key: Taala aur Chaabi

Ise taale aur chaabi se samjho. Public key ek taala hai, jo aap building ke staff entrance par lagwa dete ho. Wahi taala aap kitni bhi buildings par laga sakte ho, yaani kitne bhi servers par, aur use sabko dikhane mein koi dikkat nahi. Private key wo chaabi hai, jo sirf aapke paas rehti hai. Jab aap login karte ho, server ek chunauti bhejta hai, aapka laptop private key se use hal karta hai, aur server public key se verify kar leta hai. Chaabi kabhi network par nahi jaati. Isliye private key ko kabhi share mat karo, aur uspar ek passphrase bhi lagao.

## Key Banana aur Server par Lagana

ssh-keygen -t ed25519 -C "asha@laptop" ek modern key jodi banata hai: id_ed25519 private hai aur id_ed25519.pub public. Public key server par ~/.ssh/authorized_keys file mein jaati hai. Ye staff entrance par lage taalon ki list hai. ssh-copy-id user@server ye kaam aapke liye kar deta hai. Uske baad ssh user@server bina password ke login karta hai. Yahi key jodi aage Git wale session mein GitHub par bhi kaam aayegi: aap cat ~/.ssh/id_ed25519.pub ka text GitHub ke settings mein rakhoge, aur head office ka vault aapko is chaabi se pehchanega. Public hissa hi jaata hai, private kabhi nahi. Aur pichhle episode ke taale yahan bhi kaam aate hain: ~/.ssh folder 700 aur private key 600 honi chahiye, warna SSH khud mana kar deta hai.

## Lab: Password Login Band Karo

Ab keypad hi hata dete hain, taaki staff entrance sirf chaabi se khule. Lab: pehle key se login kaam karta hai ye pakka karo. Phir /etc/ssh/sshd_config mein PasswordAuthentication no aur PermitRootLogin no karo, aur sudo systemctl reload ssh chalao. Phir sudo sshd -T | grep -i passwordauthentication se asli value dekho. /etc/ssh/sshd_config.d/ ke chhote files pehle padhe jaate hain aur pehli value jeet jaati hai, aur kai cloud images wahan PasswordAuthentication yes rakhte hain. Humne ek aisi file banakar dekha: main file mein no hote hue bhi password login chalta raha. Doosri setting ka matlab: general manager seedha staff entrance se nahi aata. Har koi apne naam se aata hai, aur zaroorat par sudo se master key udhaar leta hai. Bahut zaroori: ek SSH session khula rakho, aur doosre terminal se naya login test karo. Agar kuch galat hua to aap bahar nahi hoge. Ye chhoti si setting server ko brute-force se kaafi bacha leti hai.

## Recap aur Bridge

Recap: key jodi, public server par, private aapke paas, permissions sahi, password login band. Staff andar aa gaya aur kamre safe hain. Ab building mein naya saaman kaise aata hai, aur subah building khulti kaise hai? Yaani software kaise install hota hai aur system boot kaise hota hai, ye dekhte hain.

---

# EPISODE 4: Packages aur Boot Process

## Software Kahan se Aata Hai?

Atithi ki building mein koi staff bazaar se apni marzi ka saaman utha kar nahi laata. Sab kuch purchase department se aata hai, approved vendor catalogue se, aur saath mein uski zaroori fittings bhi. Linux mein yahi kaam package manager karta hai. Catalogue yaani repository, fittings yaani dependencies. Wo software ko dhoondhta hai, dependencies ke saath download karta hai, aur install, update, remove sab sambhalta hai. Server par kabhi kisi website se installer download karke nahi chalate. Hamesha package manager se.

## apt aur dnf

Ubuntu aur Debian mein apt. sudo apt update catalogue ki taaza copy laata hai, yaani package list ka naya version. sudo apt install nginx software install karta hai, apt search dhoondhta hai, sudo apt remove hatata hai. Red Hat family mein dnf, yaani sudo dnf install nginx. Wahan purana naam yum tha, aur aaj bhi yum likho to wo dnf hi chalata hai. Tool alag hai, idea ek. Security ke liye regular updates zaroori hain, aur production par update karne se pehle test environment mein try karo.

## Linux Boot Process

Computer ON kaise hota hai? Hotel ke subah ke opening routine ki tarah, ek tay kram mein. Pehle bijli aur building ki jaanch: firmware, BIOS ya UEFI, hardware check karta hai. Phir bootloader, GRUB, tay karta hai kaun sa kernel uthana hai aur use memory mein load karta hai. Kernel ke saath ek chhota temporary root bhi load hota hai, initramfs, jisme disk tak pahunchne ke drivers hote hain. Phir management office jaagta hai: kernel hardware chalu karta hai aur pehla process, systemd, start karta hai. systemd hamara shift supervisor hai, jo baaki departments ko sahi kram mein kholta hai, yaani services, jaise networking aur SSH. Aakhir mein staff entrance khulta hai, yaani login aata hai. Purane systems mein supervisor ka naam init tha, aur wo run levels se kaam karta tha: 3 yaani bina graphics ke poora multi-user mode, 5 yaani graphical. systemd mein inhe targets kehte hain: multi-user.target aur graphical.target. systemctl get-default batata hai ki aapka server kis target tak boot hota hai. Jab server boot nahi hota, to is routine ka kaun sa kadam atka hai ye pehchaan kar hi aap sahi jagah dekh paate ho.

## Lab: nginx Install aur Check

Lab: purchase department se ek naya department mangwate hain. sudo apt update && sudo apt install -y nginx chalao. nginx building ka front desk hai, jo darwaza number 80 par guests ko jawab deta hai. systemctl status nginx se shift supervisor se poochho ki ye service chal rahi hai ya nahi. curl -I localhost se HTTP response header aayega, 200 OK. systemctl get-default bhi chala kar dekho: Ubuntu par aksar graphical.target dikhta hai, humare test mein wahi tha, aur multi-user.target bhi aam hai; dono mein server bina screen ke bhi chalta hai. Agar aapka VM cloud mein hai to uska public IP browser mein kholo aur nginx ka welcome page dekho. Agar na dikhe to gate ka guard rok raha ho sakta hai, yaani firewall ya security group, jo hum cloud sessions mein detail se dekhenge.

## Recap aur Bridge

Recap: saaman purchase department se, yaani packages package manager se. Subah ka opening routine, yaani boot ki chain. Aur ek chalti nginx service. Ab Atithi ki building mein staff hai, taale hain, aur pehla guest serve ho sakta hai. Agle session mein manager ka daily round: jab server dheema ho, bhar jaye ya toote, to use kaise dekhein aur theek karein.
