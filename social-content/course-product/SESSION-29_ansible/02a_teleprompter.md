# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-29_ansible

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,857 · **Episodes:** 4

---

# EPISODE 1: Setup Crew kyun

## Chaar Buildings, Chaar Alag Kahaniyan

Session 28 ke baad Atithi ka campus ek master plan se ban jaata hai: chaar buildings, do wings, marshal aur records office. Par har building ke andar abhi khaali kamre hain. Nginx lagana hai, ek deploy user banana hai, firewall ka ek door kholna hai, aur ek page rakhna hai. Agar aap chaaron par haath se SSH karke ye karoge, to ek building mein purana version rahega, doosri mein firewall bhoolega, teesri mein page mein typo. Har building thodi alag, aur koi nahi jaanta kaun si kaisi. Isko snowflake server kehte hain: apne aap mein unique aur nazuk. Iska hal ek crew hai jo ek hi checklist har building par ek jaisi chalaye. Is session mein wo crew: Ansible.

## Terraform Banata Hai, Ansible Sajata Hai

Seedha farq: Terraform campus banata hai: network, buildings, database. Ansible building ke andar jaakar sajata hai: packages, config files, users, services. Terraform ke paas as-built register, yaani state, hota hai. Ansible ke paas by default koi register nahi hota: wo har baar building ko dekhta hai ki abhi kaisi hai, aur checklist se milata hai. Dono ek dusre ka kaam kuch had tak kar sakte hain, par aksar saath chalte hain: Terraform ke outputs se buildings ki list banti hai, aur Ansible unhe sajata hai. Ek sach bhi suno: container aur Kubernetes ke zamane mein building ke andar kaam kam hua hai, kyunki truck apna saaman saath lata hai. Par virtual machines, purane systems, Jenkins workbenches, bastion aur compliance ka kaam abhi bhi bahut hai, aur wahan Ansible roz kaam aata hai.

## Aur Kaun Se Raaste Hain

Building ko sajane ke chaar raaste hain. Haath se SSH: kam chizon ke liye theek, par yaad nahi rehta aur galti hoti hai. User data script: building pehli baar chalu hote waqt ek baar chalti hai, Session 10 mein dekha tha. Ready-made image, yaani AMI: furnished model hotel, jisse naye buildings tez ban jaate hain. Aur setup crew: checklist jo kabhi bhi dobara chal sakti hai. Ye raaste ek dusre ke dushman nahi. Aksar teams crew se model hotel banati hain, aur phir us image se buildings utaarti hain. Crew ki khaas taaqat ye hai: wo bani hui buildings par bhi chal sakti hai, aur kisi ne haath se kuch badal diya ho to use wapas theek kar deti hai. Isi ko hum drift ka ilaaj bolte hain.

## Agentless: Staff Entrance se Aana-Jaana

Ansible agentless hai. Control node, yaani jis machine se aap crew ko bhejte ho, par Ansible install hota hai. Managed nodes, yaani buildings, par kuch install nahi karna: bas SSH chalu ho aur Python maujood ho. Crew staff entrance, yaani SSH, se andar jaati hai, chhote chhote Python programs, jinhe modules kehte hain, bhejti hai, chalati hai, result wapas leti hai, aur apne tools hata kar nikal jaati hai. Isse do fayde: building par koi alag agent sambhalna ya update karna nahi, aur jis raaste se aap pehle se jaate ho, wahi raasta use hota hai. Linux session mein jo SSH key aur sudo seekha tha, wahi yahan kaam aata hai. Aur Ansible ka kaam YAML mein likha jaata hai, jo "kya hona chahiye" batata hai, "kaise karna hai" nahi.

## Lab: Control Node aur Pehla Sambandh

Lab: teen chhote Ubuntu VMs lo, ek control aur do targets: cloud par ya laptop par. Control par Ansible install karo, official docs ke tareeke se. pipx install ansible-core ek aam raasta hai, par apna version docs se dekh lo. Phir ansible --version chalao. Dhyaan: ansible-core sirf engine hai, ansible package mein community collections bhi aate hain. Isliye ansible-core ke saath ansible-galaxy collection install community.general chalao, warna ufw wala task "couldn't resolve module" error dega. Control par key banao: ssh-keygen -t ed25519, phir ssh-copy-id ubuntu@TARGET_IP dono targets ke liye. Test karo ki ssh ubuntu@TARGET_IP bina password ke chalta hai. Ye pehli ssh host key ko known_hosts mein daalti hai; wo na ho to host_key_checking = True ke saath Ansible "Host key verification failed" dega. Ek project folder banao aur usme ansible.cfg rakho, jisme inventory = inventory.ini likha ho, taaki har command mein -i na likhna pade. Target ka security group port 22 sirf control machine ke IP se khole. Agle episode mein isi setup par crew ko kaam dete hain.

## Recap aur Bridge

Recap: Terraform banata hai, Ansible sajata hai. Crew staff entrance se aati hai, kuch install nahi karti, aur drift ko wapas theek kar sakti hai. Par crew ko pehle pata hona chahiye ki kin buildings par jaana hai. Wo list agla episode.

---

# EPISODE 2: List of Buildings

## Kis Building Par Kaun Sa Kaam?

Crew ko pehle batana padta hai ki kin buildings par kaam karna hai. Is list ko inventory kehte hain. Buildings ko groups mein baanta jaata hai: web, db, agents. Isse ek hi command poore group par chalti hai, aur har group ke liye alag settings ho sakti hain, jaise web ke liye port 80 aur db ke liye port 5432. Cloud mein buildings badalti rehti hain, isliye ye list haath se bhi ho sakti hai aur automatic bhi.

## Inventory Files aur Variables

Sabse seedhi inventory:

Yahi list YAML mein bhi likh sakte ho, bas syntax alag. Settings do jagah rakhte hain: group_vars/web.yml mein poore group ki, aur host_vars/web1.yml mein ek building ki. Isse inventory file chhoti rehti hai. ansible-inventory --graph chalao to dikhega ki Ansible ne groups ko kaise samjha. Ek chhoti baat: inventory mein password mat likho. Wo key cabinet ka kaam hai, jo hum episode 4 mein dekhenge.

## Private Wing aur Dynamic List

Session 14 mein humne private wing banayi thi, jahan buildings tak seedha raasta nahi. Crew ko wahan bhi jaana hai, to gatehouse se jaayegi. Inventory mein ansible_ssh_common_args='-o ProxyJump=ubuntu@GATEHOUSE_IP' likho, wahi ssh -J jo humne tab seekha tha. Doosri samasya: buildings Auto Scaling se aati jaati hain, to IP ki list haath se kaun likhega? Iske liye dynamic inventory hai. AWS ke liye amazon.aws.aws_ec2 plugin, jo landlord se pooch kar buildings ki list nikalta hai, tags ke hisaab se filter karta hai, aur tags se groups banata hai: Role=web wali buildings ek group. Is plugin ko boto3 aur AWS ki credentials chahiye, jo role ya profile se aati hain. Config file ka naam aws_ec2.yml par khatam ho, aur group ke liye keyed_groups mein key: ec2_tags.Role. Pehle haath ki list, phir dynamic.

## Ad-hoc Commands aur Modules

Ad-hoc command ek ek kaam ke liye hai. ansible web -m ping ka matlab connection aur Python ka test, ICMP ping nahi. ansible all -a "uptime" har building par command. Module ek kaam ke liye tayyar program hai: apt, copy, file, user, service, ufw. Nginx ke liye: ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become. --become matlab sudo, yaani duty manager ki tarah, jo Linux session ka wahi idea hai. Dhyaan do state=present: ye keh raha hai "nginx maujood hona chahiye", ye nahi ki "install karo". Agar pehle se hai to crew kuch nahi karegi. Ye idempotency hai, jo agle episode ka dil hai. Aur setup module building ke facts nikalta hai: OS, IP, memory, jo checklist mein sawaal poochne ke kaam aate hain.

## Jab Module Nahi Mila: command aur shell

Kabhi kabhi koi module nahi milta. Tab command ya shell hain. Par ye idempotent nahi: har baar chalenge aur har baar "changed" bolenge, chahe kuch na badla ho. Isliye pehle module dhoondho, aur shell tabhi jab koi aur raasta na ho. Aur agar shell chalana hi pada, to Ansible ko sikhao ki kab "changed" maane: creates=/path ya changed_when. Aur shell mein pipes ya user ka text ho, to injection ka khatra, isliye command ko tarjeeh do.

## Lab: Poori Fleet par Ek Command

Lab: upar wali inventory apne targets ke IP se banao. ansible all -m ping: dono se "pong" aana chahiye. Fail ho to sabse pehle ssh haath se try karo, aur -vvv lagao. Phir ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become. Pehli baar "changed". Wahi command dobara: "ok", kyunki kuch badalna nahi tha. Phir ansible web -m ansible.builtin.service -a "name=nginx state=started enabled=yes" --become. Dono IP browser mein kholo: nginx ka welcome page. Cloud par security group ka port 80 bhi kholna padega. Ek building par haath se sudo systemctl stop nginx karo, aur wahi service wali command dobara chalao: crew use phir chalu kar degi. Ek command, poori fleet.

## Recap aur Bridge

Recap: list, groups, variables, ad-hoc. Ad-hoc command chhote kaam ke liye theek hai, par asli kaam ek likhi hui checklist hai jo Git mein rahe. Wo agla episode: playbook.

---

# EPISODE 3: Checklist

## Pandrah Command Ek File Mein

Ad-hoc commands shell history mein rah jaate hain, aur kal koi nahi jaanta ki kaun si building par kya chala tha. Asli setup, yaani nginx lagana, user banana, firewall kholna, page rakhna, ek file mein likha hona chahiye, jo Git mein jaaye aur jis par pull request mein review ho. Is file ko playbook, yaani checklist, kehte hain: ek YAML jisme kaamon ki list hoti hai, jo ek ya zyada groups par chalti hai. Ab Atithi ka setup bhi Git ke register mein hai, Session 16 jaisa.

## Checklist ka Dhancha

Checklist:

Upar play hai, yaani kin buildings par. Har task ka naam, ek module, aur uske arguments. Ufw ka rule tabhi lagao jab ufw ko sach mein use kar rahe ho, aur dhyaan rakho ki SSH ka door pehle khula ho, warna crew apne hi staff entrance par taala laga degi.

## Idempotency aur Handlers

Idempotency ka matlab: checklist jitni baar chalao, natija ek jaisa. Pehli baar changed=4, doosri baar changed=0. Crew ne dekha ki sab pehle se theek hai, to haath nahi lagaya. Isliye Ansible ko roz, ya har deploy par, chalana safe hai. Handler ek khaas task hai jo tabhi chalta hai jab usse notify karne wala task sach mein kuch badle. Page badla, to nginx reload. Page nahi badla, to reload nahi. Do baatein yaad rakho. Handler play ke aakhir mein chalte hain, beech mein nahi, aur agar beech mein koi task fail ho jaye, to handler chalne se pehle hi play ruk sakti hai. Zaroorat ho to meta: flush_handlers. Aur notify mein naam bilkul wahi likhna padta hai jo handler ka hai, ek akshar bhi alag to kuch nahi chalega.

## Variables, Conditions aur Loops

Variables kai jagah se aa sakte hain. Role ke defaults sabse kamzor, phir group_vars, phir host_vars, phir play ke vars, aur command line ka -e sabse upar. Seedha yaad rakhne ka tareeka: jo jitna specific, wo utna upar. Agar ek hi variable do jagah mila, to ladder dekho. when se task sirf tab chalta hai jab shart sach ho, jaise when: ansible_facts['os_family'] == "Debian", taaki ek hi checklist apt aur dnf dono ke liye chale. loop se ek task kai cheezon par chalta hai: do ya teen duty staff ke users ek hi task se. register se kisi task ka result variable mein rakh lo aur aage use karo. Linux session ki duty staff, user module aur authorized_key module se banti hai, aur wahi sudo group, jo hum Session 04 mein jaante hain.

## Pehle Dekho, Phir Karo: check, diff, tags

Production par seedha chalane se pehle dry run: ansible-playbook site.yml --check --diff. Ye batata hai ki kya badlega, aur file ka diff bhi dikhata hai, bina kuch badle. Ek chhoti sachchai: jo tasks command ya shell hain, wo check mode mein aksar skip hote hain, isliye dry run poori kahani nahi batata. --limit web1 se sirf ek building par chalao, jo pehle ek building par aazmane ke kaam aata hai. Tasks par tags laga do, jaise page, to --tags page se sirf wahi chalega. Aur jab checklist beech mein ruk jaye, to log mein dekho kaun sa task fail hua. Ansible ke error aksar saaf hote hain, bas upar se poora padho.

## Drift ka Ilaaj aur Galti Sambhalna

Ab drift ka ilaaj dekhte hain. Kisi ne web2 par haath se page badal diya. Checklist dobara chalao: sirf web2 par changed=2, yaani page aur nginx reload, aur page wapas theek. Jis building par kuch nahi badla, wahan kuch nahi hua. Yahi crew ki sabse badi taaqat hai. Kabhi kisi task ka fail hona normal ho sakta hai. ignore_errors har galti ko dabata hai, isliye kam use karo. Behtar hai failed_when ya changed_when se bataana ki asli naakaami kya hai. Aur block ke saath rescue se wahi try aur recover ka pattern milta hai jo Bash mein tha. Rule: crew ko aise likho ki wo kam bole aur jo bole, wo sach ho.

## Lab: Web Fleet Ko Ek Checklist se Sajao

Lab: upar wali checklist site.yml mein rakho. Pehle ansible-playbook site.yml --check --diff, dekho ki kya badlega. Taaza building par ye service wale task par ruk sakta hai: nginx abhi laga nahi. Phir asli run. Dono IP browser mein kholo: har ek par apni building ka naam. Wahi checklist dobara: changed=0. Ab web2 par haath se sudo systemctl stop nginx aur page ki file badal do. Checklist phir chalao: crew dono cheezein wapas theek karti hai, aur sirf web2 par. Ek task mein jaan-boojh kar galat package ka naam do aur dekho ki error kaisa dikhta hai. Aakhir mein site.yml aur inventory Git mein commit karo.

## Recap aur Bridge

Recap: checklist, idempotency, handler, variables, dry run. Par ek checklist agar paanch sau line ki ho jaaye, to padhna mushkil. Wahan binder aur fill-in form kaam aate hain, aur secrets ke liye sealed envelope. Agla episode.

---

# EPISODE 4: Binder aur Fill-in Form

## Paanch Sau Line ki Checklist

Atithi ki checklist badhti gayi: users, firewall, nginx, Docker, Jenkins workbench ke liye Java. Ek file mein sab milkar paanch sau line, aur koi change ek jagah chhooe to doosri toot jaye. Isliye binder, yaani role. Ek role ek kaam ka dabba hai: baseline ka role, nginx ka role, docker ka role. Har role apni jagah, aur kai checklists mein dobara use hota hai. Ye wahi soch hai jo Terraform ke standard design, yaani module, mein thi.

## Role ka Dhancha

Role ka standard dhancha: tasks/main.yml mein kaam, handlers/main.yml mein handler, templates/ mein fill-in forms, defaults/main.yml mein wo variables jo koi bhi badal sake, aur files/ mein seedhi copy hone wali files. ansible-galaxy init roles/nginx ye dhancha khud bana deta hai. Ek niyam: jo cheez badalni ho, use defaults mein rakho. vars ka variable bahut upar ki precedence rakhta hai, to use badalna mushkil hota hai. Role ka naam ek kaam batata ho, aur uska ek chhota README ho, jisme likha ho ki kaun se variables hain. Phir site.yml bas itna: hosts: web, roles: [baseline, nginx]. Ansible Galaxy aur collections se doosron ke roles bhi milte hain. Par unhe chalane se pehle padho, kyunki wo aapke buildings par root banke chalte hain.

## Fill-in Form: Jinja2 Template

Ek config file har building ke liye thodi alag hoti hai: port, server ka naam, kisse baat karni hai. Iske liye fill-in form, yaani Jinja2 template. Form mein khaali jagah {{ variable }} ki tarah likhi jaati hai, aur loops {% for %} se. Misaal:

Task:

template module form ko bharkar building par rakh deta hai. Agar file badli to handler reload karta hai. Agar kisi file ko rakhne se pehle jaanchne ka koi command ho, to task mein validate argument lagao, jisme %s temporary file ki jagah aata hai. Nginx ki ek conf.d file akeli nginx -t se nahi jaanchi ja sakti, isliye yahan hum reload ke baad curl /health se check karte hain. Isse ek galat form ko pakadna aasaan hota hai.

## Sealed Envelope: Ansible Vault

Secrets, jaise database ka password, plain YAML mein Git par nahi jaane chahiye. Ansible Vault unhe sealed envelope mein rakhta hai: ansible-vault encrypt_string 'S3cret' --name db_password, aur output ko group_vars/db.yml mein paste karo. Chalate waqt --ask-vault-pass, ya password ki file, jo khud Git mein nahi jaati. Do galtiyan jo aksar hoti hain. Pehli: password ki file .gitignore mein nahi. Doosri: log mein secret dikh jana. Isliye jis task mein secret chalta ho, uspar no_log: true. Aur ek sachchai: vault ek surakshit dabba hai, poori secrets management nahi. Production mein secrets aksar cloud ke secret manager se aate hain, jaise Session 13 mein Secrets Manager, aur Ansible unhe chalate waqt padhta hai. Vault ka password key cabinet mein, yaani Jenkins ya Actions ke credentials mein, rakho.

## Roz ka Tareeka: Lint, Test aur Pipeline

Crew ko bhi conveyor mein lagao. Jab koi checklist ya role badle, pull request par ansible-lint aur ansible-playbook --syntax-check chalein, Session 18 aur 20 wale stations ki tarah. Phir staging par --check --diff, aur approval ke baad asli run. Roles ko container mein aazmane ke liye Molecule jaisa tool hota hai, par shuru mein zaroori nahi. Kuch teams checklist ko hafte mein ek baar bhi chalati hain, taaki jo buildings drift ho gayi hon wo wapas theek ho jayein. Dhyaan: crew ko chalane wala jo key use karta hai, wo bahut taaqatwar hai, isliye use key cabinet mein rakho, aur sirf conveyor ko chalane do.

## Lab: Nginx ka Binder

Lab: ansible-galaxy init roles/nginx chalao. Pichhli checklist ke tasks tasks/main.yml mein, handler handlers/main.yml mein, aur defaults/main.yml mein app_port: 80 aur server_name: atithi.example. Phir templates/atithi.conf.j2, jo upar wala form hai. site.yml mein sirf hosts: web, become: true, roles: [nginx]. Chalao. Ab -e app_port=8080 ke saath chalao aur dekho ki config badli aur nginx reload hua. Ubuntu ki default nginx site port 80 par pehle se hai, isliye role mein ek task jodo jo /etc/nginx/sites-enabled/default hata de, tab curl /health par ok milega, warna 404. Phir ansible-vault encrypt_string se ek db_password banao, group_vars/db.yml mein rakho, aur ek task banao jisme no_log: true ho. pipx install ansible-lint karke ansible-lint chalao, aur jo cheezein wo batata hai unhe theek karo. ansible-galaxy init ki khaali meta aur tests files par bhi wo shikayat karega, aur role ke variables par nginx_ jaisa prefix maangega, isliye asli roles mein nginx_app_port likhte hain.

## Recap aur Bridge

Recap: roles, templates, vault aur pipeline. Ab Atithi ke paas ek poora campus hai, jise master plan banata hai aur setup crew sajati hai. Dono AWS par. Par Atithi ab ek doosre landlord ke saath bhi kaam karne wala hai: Azure. Wahi buildings, wahi wings, bas naam alag. Aur uske saath ek ready-made head office. Agla session.
