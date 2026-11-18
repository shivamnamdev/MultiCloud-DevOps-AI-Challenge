# ✍️ 02: SCRIPT — SESSION-29: Ansible
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S29`
- **Focus:** Configuration management and where Ansible sits next to Terraform, images and containers; agentless design (control node, SSH, Python, modules); `ansible.cfg`; inventory (INI, YAML, groups, `group_vars`, `host_vars`, bastion with `ProxyJump`, dynamic inventory); ad-hoc commands and facts; playbooks, idempotency, `changed`, handlers, variables and precedence, `when`, `loop`, `register`, `--check --diff`, tags, error handling; roles; Jinja2 templates; Ansible Vault and `no_log`; `ansible-lint`; Ansible in a pipeline
- **Builds on:** Session 04 (users, groups, `sudo`, SSH keys), Session 05 and 05B (`systemctl`, `ufw`, ports), Session 10 (instances, user data), Session 14 (private wing, gatehouse, `ssh -J`), Session 17 to 19 (Jenkins credentials and agents), Session 20 (Actions), Session 27 and 28 (Terraform outputs, drift, modules)
- **Story position:** Zoom level 2, the rented campus. Campus Terraform ne bana diya, par har building ke kamre khaali hain. Setup crew list ke saath aati hai, staff entrance (SSH) se andar jaati hai, checklist ke hisaab se kaam karti hai, aur nikal jaati hai. Terraform banata hai, Ansible sajata hai.
- **Story words used:** setup crew (Ansible), checklist (playbook), binder (role), fill-in form (Jinja2 template), list of buildings (inventory), staff entrance (SSH), master plan (Terraform code), as-built register (state), drift, buildings (servers), campus (VPC), wing (subnet), gatehouse (bastion), duty manager (sudo user), key cabinet (credentials), sealed envelope (secret), foreman (Jenkins), conveyor (pipeline), staff (admin), guest (end user)
- **Lab project:** Atithi's web buildings: a control machine and two target buildings get nginx, a deploy user, a firewall rule and a page that says which building served the guest. First as ad-hoc commands, then as a checklist, then as a binder with a fill-in form.
- **Cost rule:** two or three small instances (or local VMs) for a few hours. Stop or destroy them after the lab. Targets in a private wing need the gatehouse path from Session 14, so for the first run keep targets in a public wing or use local VMs.
- **Episodes:**
  - Episode 1: Setup Crew kyun: Terraform se Farq aur Agentless Design
  - Episode 2: List of Buildings: Inventory aur Ad-hoc Commands
  - Episode 3: Checklist: Playbook, Idempotency aur Handlers
  - Episode 4: Binder aur Fill-in Form: Roles, Templates aur Vault

---

# 📺 EPISODE 1: Setup Crew kyun

### [00:00 – 02:20] Scene 1: Chaar Buildings, Chaar Alag Kahaniyan
**[VISUAL: Four buildings, four engineers' hands typing over SSH. Building 1 has nginx 1.18 and a custom config, building 2 has a newer nginx, building 3 has no firewall rule, building 4 has a typo in the page. A red label: "snowflake". Then a single list and a single checklist applied to all four.]**

**(Voiceover):**
Session 28 ke baad Atithi ka campus ek master plan se ban jaata hai: chaar buildings, do wings, marshal aur records office. Par har building ke andar abhi khaali kamre hain. Nginx lagana hai, ek deploy user banana hai, firewall ka ek door kholna hai, aur ek page rakhna hai. Agar aap chaaron par haath se SSH karke ye karoge, to ek building mein purana version rahega, doosri mein firewall bhoolega, teesri mein page mein typo. Har building thodi alag, aur koi nahi jaanta kaun si kaisi. Isko snowflake server kehte hain: apne aap mein unique aur nazuk. Iska hal ek crew hai jo ek hi checklist har building par ek jaisi chalaye. Is session mein wo crew: Ansible.

### [02:20 – 04:55] Scene 2: Terraform Banata Hai, Ansible Sajata Hai
**[VISUAL: Two lanes. Terraform: "build the campus" (VPC, subnets, instances, ALB, RDS), master plan, as-built register. Ansible: "furnish the buildings" (packages, files, users, services), checklist, no register. A thin overlap marked "user data". An arrow: Terraform output (IP list) → Ansible list of buildings.]**

**(Voiceover):**
Seedha farq: Terraform campus banata hai: network, buildings, database. Ansible building ke andar jaakar sajata hai: packages, config files, users, services. Terraform ke paas as-built register, yaani state, hota hai. Ansible ke paas by default koi register nahi hota: wo har baar building ko dekhta hai ki abhi kaisi hai, aur checklist se milata hai. Dono ek dusre ka kaam kuch had tak kar sakte hain, par aksar saath chalte hain: Terraform ke outputs se buildings ki list banti hai, aur Ansible unhe sajata hai. Ek sach bhi suno: container aur Kubernetes ke zamane mein building ke andar kaam kam hua hai, kyunki truck apna saaman saath lata hai. Par virtual machines, purane systems, Jenkins workbenches, bastion aur compliance ka kaam abhi bhi bahut hai, aur wahan Ansible roz kaam aata hai.

### [04:55 – 07:25] Scene 3: Aur Kaun Se Raaste Hain
**[VISUAL: Four ways to furnish a building. 1. Hand over SSH (fragile). 2. Instance user data: a script at first boot (runs once). 3. A ready-made image: furnished model hotel, AMI (Session 10). 4. A setup crew with a checklist, run any time. A small table: runs once vs repeatable, good for first boot vs ongoing.]**

**(Voiceover):**
Building ko sajane ke chaar raaste hain. Haath se SSH: kam chizon ke liye theek, par yaad nahi rehta aur galti hoti hai. User data script: building pehli baar chalu hote waqt ek baar chalti hai, Session 10 mein dekha tha. Ready-made image, yaani AMI: furnished model hotel, jisse naye buildings tez ban jaate hain. Aur setup crew: checklist jo kabhi bhi dobara chal sakti hai. Ye raaste ek dusre ke dushman nahi. Aksar teams crew se model hotel banati hain, aur phir us image se buildings utaarti hain. Crew ki khaas taaqat ye hai: wo bani hui buildings par bhi chal sakti hai, aur kisi ne haath se kuch badal diya ho to use wapas theek kar deti hai. Isi ko hum drift ka ilaaj bolte hain.

### [07:25 – 10:00] Scene 4: Agentless: Staff Entrance se Aana-Jaana
**[VISUAL: A control node with Ansible installed. SSH arrows to three managed nodes with nothing installed. A small Python script (module) travels over SSH, runs, returns a JSON result, and is deleted. Tags: "control node: Ansible + Python", "managed node: SSH + Python only".]**

**(Voiceover):**
Ansible agentless hai. Control node, yaani jis machine se aap crew ko bhejte ho, par Ansible install hota hai. Managed nodes, yaani buildings, par kuch install nahi karna: bas SSH chalu ho aur Python maujood ho. Crew staff entrance, yaani SSH, se andar jaati hai, chhote chhote Python programs, jinhe modules kehte hain, bhejti hai, chalati hai, result wapas leti hai, aur apne tools hata kar nikal jaati hai. Isse do fayde: building par koi alag agent sambhalna ya update karna nahi, aur jis raaste se aap pehle se jaate ho, wahi raasta use hota hai. Linux session mein jo SSH key aur `sudo` seekha tha, wahi yahan kaam aata hai. Aur Ansible ka kaam YAML mein likha jaata hai, jo "kya hona chahiye" batata hai, "kaise karna hai" nahi.

### [10:00 – 13:20] Scene 5: Lab: Control Node aur Pehla Sambandh
**[VISUAL: A control VM and two target VMs. `pipx install ansible-core`, or the distribution package. `ansible --version`. `ssh-keygen -t ed25519` on control; `ssh-copy-id ubuntu@TARGET_IP`. An `ansible.cfg` with `inventory = inventory.ini` and `host_key_checking = True`. Reminder: security group allows port 22 from control only.]**

**(Voiceover):**
Lab: teen chhote Ubuntu VMs lo, ek control aur do targets: cloud par ya laptop par. Control par Ansible install karo, official docs ke tareeke se. `pipx install ansible-core` ek aam raasta hai, par apna version docs se dekh lo. Phir `ansible --version` chalao. Dhyaan: `ansible-core` sirf engine hai, `ansible` package mein community collections bhi aate hain. Isliye `ansible-core` ke saath `ansible-galaxy collection install community.general` chalao, warna `ufw` wala task "couldn't resolve module" error dega. Control par key banao: `ssh-keygen -t ed25519`, phir `ssh-copy-id ubuntu@TARGET_IP` dono targets ke liye. Test karo ki `ssh ubuntu@TARGET_IP` bina password ke chalta hai. Ye pehli ssh host key ko `known_hosts` mein daalti hai; wo na ho to `host_key_checking = True` ke saath Ansible "Host key verification failed" dega. Ek project folder banao aur usme `ansible.cfg` rakho, jisme `inventory = inventory.ini` likha ho, taaki har command mein `-i` na likhna pade. Target ka security group port 22 sirf control machine ke IP se khole. Agle episode mein isi setup par crew ko kaam dete hain.

### [13:20 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "Terraform builds · Ansible furnishes · agentless over SSH · module = small Python program · no register, always compares · ansible.cfg".]**

**(Voiceover):**
Recap: Terraform banata hai, Ansible sajata hai. Crew staff entrance se aati hai, kuch install nahi karti, aur drift ko wapas theek kar sakti hai. Par crew ko pehle pata hona chahiye ki kin buildings par jaana hai. Wo list agla episode.

---

# 📺 EPISODE 2: List of Buildings

### [00:00 – 01:55] Scene 1: Kis Building Par Kaun Sa Kaam?
**[VISUAL: A list: web1 and web2 under group `web`, db1 under `db`, jenkins-agent1 under `agents`. A command aimed at `web` reaches two buildings; a command aimed at `all` reaches four.]**

**(Voiceover):**
Crew ko pehle batana padta hai ki kin buildings par kaam karna hai. Is list ko inventory kehte hain. Buildings ko groups mein baanta jaata hai: `web`, `db`, `agents`. Isse ek hi command poore group par chalti hai, aur har group ke liye alag settings ho sakti hain, jaise web ke liye port 80 aur db ke liye port 5432. Cloud mein buildings badalti rehti hain, isliye ye list haath se bhi ho sakti hai aur automatic bhi.

### [01:55 – 03:55] Scene 2: Inventory Files aur Variables
**[VISUAL: An `inventory.ini` with `[web]`, `[db]`, `[all:vars]`. Beside it the same in YAML. A folder layout: `inventory.ini`, `group_vars/web.yml`, `host_vars/web1.yml`. A command `ansible-inventory --graph`.]**

**(Voiceover):**
Sabse seedhi inventory:
```ini
[web]
web1 ansible_host=10.0.1.10
web2 ansible_host=10.0.1.11

[db]
db1 ansible_host=10.0.2.10

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_ed25519
```
Yahi list YAML mein bhi likh sakte ho, bas syntax alag. Settings do jagah rakhte hain: `group_vars/web.yml` mein poore group ki, aur `host_vars/web1.yml` mein ek building ki. Isse inventory file chhoti rehti hai. `ansible-inventory --graph` chalao to dikhega ki Ansible ne groups ko kaise samjha. Ek chhoti baat: inventory mein password mat likho. Wo key cabinet ka kaam hai, jo hum episode 4 mein dekhenge.

### [03:55 – 07:05] Scene 3: Private Wing aur Dynamic List
**[VISUAL: Left: control node reaching the private wing through the gatehouse. `ansible_ssh_common_args='-o ProxyJump=ubuntu@GATEHOUSE_IP'`. Right: an `aws_ec2.yml` inventory plugin config filtering by tag `Env=dev` and grouping by tag `Role`. A terminal showing `ansible-inventory --graph` with groups `role_web`, `role_db`.]**

**(Voiceover):**
Session 14 mein humne private wing banayi thi, jahan buildings tak seedha raasta nahi. Crew ko wahan bhi jaana hai, to gatehouse se jaayegi. Inventory mein `ansible_ssh_common_args='-o ProxyJump=ubuntu@GATEHOUSE_IP'` likho, wahi `ssh -J` jo humne tab seekha tha. Doosri samasya: buildings Auto Scaling se aati jaati hain, to IP ki list haath se kaun likhega? Iske liye dynamic inventory hai. AWS ke liye `amazon.aws.aws_ec2` plugin, jo landlord se pooch kar buildings ki list nikalta hai, tags ke hisaab se filter karta hai, aur tags se groups banata hai: `Role=web` wali buildings ek group. Is plugin ko `boto3` aur AWS ki credentials chahiye, jo role ya profile se aati hain. Config file ka naam `aws_ec2.yml` par khatam ho, aur group ke liye `keyed_groups` mein `key: ec2_tags.Role`. Pehle haath ki list, phir dynamic.

### [07:05 – 10:10] Scene 4: Ad-hoc Commands aur Modules
**[VISUAL: `ansible web -m ping`, `ansible all -a "uptime"`, `ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become`. A module catalogue: apt, dnf, copy, file, user, service, template, lineinfile, ufw. `ansible web -m setup -a "filter=ansible_distribution*"`.]**

**(Voiceover):**
Ad-hoc command ek ek kaam ke liye hai. `ansible web -m ping` ka matlab connection aur Python ka test, ICMP ping nahi. `ansible all -a "uptime"` har building par command. Module ek kaam ke liye tayyar program hai: `apt`, `copy`, `file`, `user`, `service`, `ufw`. Nginx ke liye: `ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become`. `--become` matlab `sudo`, yaani duty manager ki tarah, jo Linux session ka wahi idea hai. Dhyaan do `state=present`: ye keh raha hai "nginx maujood hona chahiye", ye nahi ki "install karo". Agar pehle se hai to crew kuch nahi karegi. Ye idempotency hai, jo agle episode ka dil hai. Aur `setup` module building ke facts nikalta hai: OS, IP, memory, jo checklist mein sawaal poochne ke kaam aate hain.

### [10:10 – 12:00] Scene 5: Jab Module Nahi Mila: command aur shell
**[VISUAL: A side-by-side. Left: `ansible web -m ansible.builtin.service -a "name=nginx state=started"` result "ok" the second time. Right: `ansible web -m ansible.builtin.shell -a "systemctl start nginx"` always shows "changed". A small note: `creates=` or `changed_when` to teach it.]**

**(Voiceover):**
Kabhi kabhi koi module nahi milta. Tab `command` ya `shell` hain. Par ye idempotent nahi: har baar chalenge aur har baar "changed" bolenge, chahe kuch na badla ho. Isliye pehle module dhoondho, aur shell tabhi jab koi aur raasta na ho. Aur agar shell chalana hi pada, to Ansible ko sikhao ki kab "changed" maane: `creates=/path` ya `changed_when`. Aur `shell` mein pipes ya user ka text ho, to injection ka khatra, isliye `command` ko tarjeeh do.

### [12:00 – 14:45] Scene 6: Lab: Poori Fleet par Ek Command
**[VISUAL: Create `inventory.ini` and `group_vars/web.yml`. Run `ansible all -m ping`: "pong" from both. Run the nginx command once: "changed". Run it again: "ok". `ansible web -m ansible.builtin.service -a "name=nginx state=started enabled=yes" --become`. Browser to both IPs shows the nginx welcome page. A third command opens port 80 with `ufw`.]**

**(Voiceover):**
Lab: upar wali inventory apne targets ke IP se banao. `ansible all -m ping`: dono se "pong" aana chahiye. Fail ho to sabse pehle `ssh` haath se try karo, aur `-vvv` lagao. Phir `ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become`. Pehli baar "changed". Wahi command dobara: "ok", kyunki kuch badalna nahi tha. Phir `ansible web -m ansible.builtin.service -a "name=nginx state=started enabled=yes" --become`. Dono IP browser mein kholo: nginx ka welcome page. Cloud par security group ka port 80 bhi kholna padega. Ek building par haath se `sudo systemctl stop nginx` karo, aur wahi service wali command dobara chalao: crew use phir chalu kar degi. Ek command, poori fleet.

### [14:45 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "inventory = list + groups · group_vars / host_vars · ProxyJump for private wing · dynamic plugin from tags · ad-hoc for quick checks · state= not 'do this' · avoid shell".]**

**(Voiceover):**
Recap: list, groups, variables, ad-hoc. Ad-hoc command chhote kaam ke liye theek hai, par asli kaam ek likhi hui checklist hai jo Git mein rahe. Wo agla episode: playbook.

---

# 📺 EPISODE 3: Checklist

### [00:00 – 01:40] Scene 1: Pandrah Command Ek File Mein
**[VISUAL: A scroll of fifteen ad-hoc commands in a shell history. They become one YAML file with named tasks. The file is committed to the Atithi repo; a Git log shows who changed what.]**

**(Voiceover):**
Ad-hoc commands shell history mein rah jaate hain, aur kal koi nahi jaanta ki kaun si building par kya chala tha. Asli setup, yaani nginx lagana, user banana, firewall kholna, page rakhna, ek file mein likha hona chahiye, jo Git mein jaaye aur jis par pull request mein review ho. Is file ko playbook, yaani checklist, kehte hain: ek YAML jisme kaamon ki list hoti hai, jo ek ya zyada groups par chalti hai. Ab Atithi ka setup bhi Git ke register mein hai, Session 16 jaisa.

### [01:40 – 04:25] Scene 2: Checklist ka Dhancha
**[VISUAL: An annotated playbook. `- name`, `hosts: web`, `become: true`, `vars`, `tasks` each with a name, module and arguments; a `notify`; a `handlers` section. Callouts: "play = which buildings", "task = one step", "module = how".]**

**(Voiceover):**
Checklist:
```yaml
- name: Furnish the web buildings
  hosts: web
  become: true
  vars:
    app_port: 80
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true
        cache_valid_time: 3600

    - name: Deploy the welcome page
      ansible.builtin.copy:
        content: "Atithi Hotels, served by {{ inventory_hostname }}\n"
        dest: /var/www/html/index.html
        mode: "0644"
      notify: Reload nginx

    - name: Allow the public door
      community.general.ufw:
        rule: allow
        port: "{{ app_port }}"
        proto: tcp

    - name: Keep nginx running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```
Upar play hai, yaani kin buildings par. Har task ka naam, ek module, aur uske arguments. Ufw ka rule tabhi lagao jab `ufw` ko sach mein use kar rahe ho, aur dhyaan rakho ki SSH ka door pehle khula ho, warna crew apne hi staff entrance par taala laga degi.

### [04:25 – 06:55] Scene 3: Idempotency aur Handlers
**[VISUAL: First run summary: `changed=4`. Second run: `changed=0`. A handler box that lights up only when the page task shows "changed". A caution: handlers run at the end of the play; `meta: flush_handlers` runs them earlier.]**

**(Voiceover):**
Idempotency ka matlab: checklist jitni baar chalao, natija ek jaisa. Pehli baar `changed=4`, doosri baar `changed=0`. Crew ne dekha ki sab pehle se theek hai, to haath nahi lagaya. Isliye Ansible ko roz, ya har deploy par, chalana safe hai. Handler ek khaas task hai jo tabhi chalta hai jab usse notify karne wala task sach mein kuch badle. Page badla, to nginx reload. Page nahi badla, to reload nahi. Do baatein yaad rakho. Handler play ke aakhir mein chalte hain, beech mein nahi, aur agar beech mein koi task fail ho jaye, to handler chalne se pehle hi play ruk sakti hai. Zaroorat ho to `meta: flush_handlers`. Aur `notify` mein naam bilkul wahi likhna padta hai jo handler ka hai, ek akshar bhi alag to kuch nahi chalega.

### [06:55 – 09:30] Scene 4: Variables, Conditions aur Loops
**[VISUAL: A precedence ladder from weakest to strongest: role defaults, group_vars, host_vars, play vars, `-e` extra vars. Code: `when: ansible_facts['os_family'] == "Debian"`; `loop: [ops1, ops2]` creating users; `register: result` then `debug: var=result.stdout`.]**

**(Voiceover):**
Variables kai jagah se aa sakte hain. Role ke defaults sabse kamzor, phir `group_vars`, phir `host_vars`, phir play ke `vars`, aur command line ka `-e` sabse upar. Seedha yaad rakhne ka tareeka: jo jitna specific, wo utna upar. Agar ek hi variable do jagah mila, to ladder dekho. `when` se task sirf tab chalta hai jab shart sach ho, jaise `when: ansible_facts['os_family'] == "Debian"`, taaki ek hi checklist `apt` aur `dnf` dono ke liye chale. `loop` se ek task kai cheezon par chalta hai: do ya teen duty staff ke users ek hi task se. `register` se kisi task ka result variable mein rakh lo aur aage use karo. Linux session ki duty staff, `user` module aur `authorized_key` module se banti hai, aur wahi `sudo` group, jo hum Session 04 mein jaante hain.

### [09:30 – 11:40] Scene 5: Pehle Dekho, Phir Karo: check, diff, tags
**[VISUAL: `ansible-playbook site.yml --check --diff`: lines removed in red, added in green, tasks marked "changed". `--limit web1`. `--tags page`. `--start-at-task`. A warning: check mode can skip `command` tasks.]**

**(Voiceover):**
Production par seedha chalane se pehle dry run: `ansible-playbook site.yml --check --diff`. Ye batata hai ki kya badlega, aur file ka diff bhi dikhata hai, bina kuch badle. Ek chhoti sachchai: jo tasks `command` ya `shell` hain, wo check mode mein aksar skip hote hain, isliye dry run poori kahani nahi batata. `--limit web1` se sirf ek building par chalao, jo pehle ek building par aazmane ke kaam aata hai. Tasks par `tags` laga do, jaise `page`, to `--tags page` se sirf wahi chalega. Aur jab checklist beech mein ruk jaye, to log mein dekho kaun sa task fail hua. Ansible ke error aksar saaf hote hain, bas upar se poora padho.

### [11:40 – 13:55] Scene 6: Drift ka Ilaaj aur Galti Sambhalna
**[VISUAL: Someone edits `/var/www/html/index.html` by hand on web2. The next run shows `changed=2` on web2 only (the page and the nginx reload), with the diff restoring the page. Then `ignore_errors`, `failed_when`, `block` and `rescue` shown briefly.]**

**(Voiceover):**
Ab drift ka ilaaj dekhte hain. Kisi ne web2 par haath se page badal diya. Checklist dobara chalao: sirf web2 par `changed=2`, yaani page aur nginx reload, aur page wapas theek. Jis building par kuch nahi badla, wahan kuch nahi hua. Yahi crew ki sabse badi taaqat hai. Kabhi kisi task ka fail hona normal ho sakta hai. `ignore_errors` har galti ko dabata hai, isliye kam use karo. Behtar hai `failed_when` ya `changed_when` se bataana ki asli naakaami kya hai. Aur `block` ke saath `rescue` se wahi try aur recover ka pattern milta hai jo Bash mein tha. Rule: crew ko aise likho ki wo kam bole aur jo bole, wo sach ho.

### [13:55 – 16:00] Scene 7: Lab: Web Fleet Ko Ek Checklist se Sajao
**[VISUAL: `ansible-playbook site.yml --check --diff`, then a real run with `changed=4` on both buildings, then a second run with `changed=0`. Browser shows each building's name on its page. A manual stop of nginx on web2 fixed by the next run. The playbook committed to Git.]**

**(Voiceover):**
Lab: upar wali checklist `site.yml` mein rakho. Pehle `ansible-playbook site.yml --check --diff`, dekho ki kya badlega. Taaza building par ye service wale task par ruk sakta hai: nginx abhi laga nahi. Phir asli run. Dono IP browser mein kholo: har ek par apni building ka naam. Wahi checklist dobara: `changed=0`. Ab web2 par haath se `sudo systemctl stop nginx` aur page ki file badal do. Checklist phir chalao: crew dono cheezein wapas theek karti hai, aur sirf web2 par. Ek task mein jaan-boojh kar galat package ka naam do aur dekho ki error kaisa dikhta hai. Aakhir mein `site.yml` aur inventory Git mein commit karo.

### [16:00 – 16:40] Scene 8: Recap aur Bridge
**[VISUAL: A card: "playbook = play + tasks + handlers · idempotent: second run changed=0 · handlers on change · vars precedence · when / loop / register · --check --diff · --limit and tags".]**

**(Voiceover):**
Recap: checklist, idempotency, handler, variables, dry run. Par ek checklist agar paanch sau line ki ho jaaye, to padhna mushkil. Wahan binder aur fill-in form kaam aate hain, aur secrets ke liye sealed envelope. Agla episode.

---

# 📺 EPISODE 4: Binder aur Fill-in Form

### [00:00 – 01:30] Scene 1: Paanch Sau Line ki Checklist
**[VISUAL: One giant playbook scrolls past: nginx, users, firewall, monitoring, Java, Docker all mixed. A tidy set of binders replaces it: `baseline`, `nginx`, `docker`. Two different playbooks use the same `baseline` binder.]**

**(Voiceover):**
Atithi ki checklist badhti gayi: users, firewall, nginx, Docker, Jenkins workbench ke liye Java. Ek file mein sab milkar paanch sau line, aur koi change ek jagah chhooe to doosri toot jaye. Isliye binder, yaani role. Ek role ek kaam ka dabba hai: baseline ka role, nginx ka role, docker ka role. Har role apni jagah, aur kai checklists mein dobara use hota hai. Ye wahi soch hai jo Terraform ke standard design, yaani module, mein thi.

### [01:30 – 03:50] Scene 2: Role ka Dhancha
**[VISUAL: `ansible-galaxy init roles/nginx` produces `tasks/`, `handlers/`, `templates/`, `defaults/`, `files/`, `vars/`, `meta/`. Callouts: "defaults = weakest, easy to override", "vars = hard to override". A site playbook calling `roles: [baseline, nginx]`.]**

**(Voiceover):**
Role ka standard dhancha: `tasks/main.yml` mein kaam, `handlers/main.yml` mein handler, `templates/` mein fill-in forms, `defaults/main.yml` mein wo variables jo koi bhi badal sake, aur `files/` mein seedhi copy hone wali files. `ansible-galaxy init roles/nginx` ye dhancha khud bana deta hai. Ek niyam: jo cheez badalni ho, use `defaults` mein rakho. `vars` ka variable bahut upar ki precedence rakhta hai, to use badalna mushkil hota hai. Role ka naam ek kaam batata ho, aur uska ek chhota README ho, jisme likha ho ki kaun se variables hain. Phir `site.yml` bas itna: `hosts: web`, `roles: [baseline, nginx]`. Ansible Galaxy aur collections se doosron ke roles bhi milte hain. Par unhe chalane se pehle padho, kyunki wo aapke buildings par `root` banke chalte hain.

### [03:50 – 07:00] Scene 3: Fill-in Form: Jinja2 Template
**[VISUAL: `templates/atithi.conf.j2` with `listen {{ app_port }};` and `server_name {{ server_name }};`, plus a `{% for %}` loop over upstream backends. A task `ansible.builtin.template` with `src`, `dest`, `mode`, `notify`. Output shows the rendered file on web1 and web2 differ in the server name.]**

**(Voiceover):**
Ek config file har building ke liye thodi alag hoti hai: port, server ka naam, kisse baat karni hai. Iske liye fill-in form, yaani Jinja2 template. Form mein khaali jagah `{{ variable }}` ki tarah likhi jaati hai, aur loops `{% for %}` se. Misaal:
```jinja
server {
    listen {{ app_port }};
    server_name {{ server_name }};
    root /var/www/html;
    location /health { return 200 "ok\n"; }
}
```
Task:
```yaml
- name: Render the site config
  ansible.builtin.template:
    src: atithi.conf.j2
    dest: /etc/nginx/conf.d/atithi.conf
    mode: "0644"
  notify: Reload nginx
```
`template` module form ko bharkar building par rakh deta hai. Agar file badli to handler reload karta hai. Agar kisi file ko rakhne se pehle jaanchne ka koi command ho, to task mein `validate` argument lagao, jisme `%s` temporary file ki jagah aata hai. Nginx ki ek `conf.d` file akeli `nginx -t` se nahi jaanchi ja sakti, isliye yahan hum reload ke baad `curl /health` se check karte hain. Isse ek galat form ko pakadna aasaan hota hai.

### [07:00 – 09:25] Scene 4: Sealed Envelope: Ansible Vault
**[VISUAL: `ansible-vault encrypt_string 'S3cret' --name db_password` produces an encrypted block pasted into `group_vars/db.yml`. `ansible-playbook site.yml --ask-vault-pass`, or `--vault-password-file ~/.vault_pass` (not in Git). A task with `no_log: true`. A line: "Production: cloud secret manager".]**

**(Voiceover):**
Secrets, jaise database ka password, plain YAML mein Git par nahi jaane chahiye. Ansible Vault unhe sealed envelope mein rakhta hai: `ansible-vault encrypt_string 'S3cret' --name db_password`, aur output ko `group_vars/db.yml` mein paste karo. Chalate waqt `--ask-vault-pass`, ya password ki file, jo khud Git mein nahi jaati. Do galtiyan jo aksar hoti hain. Pehli: password ki file `.gitignore` mein nahi. Doosri: log mein secret dikh jana. Isliye jis task mein secret chalta ho, uspar `no_log: true`. Aur ek sachchai: vault ek surakshit dabba hai, poori secrets management nahi. Production mein secrets aksar cloud ke secret manager se aate hain, jaise Session 13 mein Secrets Manager, aur Ansible unhe chalate waqt padhta hai. Vault ka password key cabinet mein, yaani Jenkins ya Actions ke credentials mein, rakho.

### [09:25 – 11:30] Scene 5: Roz ka Tareeka: Lint, Test aur Pipeline
**[VISUAL: A Jenkins or Actions stage: `ansible-lint`, `ansible-playbook --syntax-check`, `--check --diff` against staging, then a run on approval. A small box: "Molecule: test a role in a container". A calendar: weekly run to catch drift.]**

**(Voiceover):**
Crew ko bhi conveyor mein lagao. Jab koi checklist ya role badle, pull request par `ansible-lint` aur `ansible-playbook --syntax-check` chalein, Session 18 aur 20 wale stations ki tarah. Phir staging par `--check --diff`, aur approval ke baad asli run. Roles ko container mein aazmane ke liye Molecule jaisa tool hota hai, par shuru mein zaroori nahi. Kuch teams checklist ko hafte mein ek baar bhi chalati hain, taaki jo buildings drift ho gayi hon wo wapas theek ho jayein. Dhyaan: crew ko chalane wala jo key use karta hai, wo bahut taaqatwar hai, isliye use key cabinet mein rakho, aur sirf conveyor ko chalane do.

### [11:30 – 14:20] Scene 6: Lab: Nginx ka Binder
**[VISUAL: `ansible-galaxy init roles/nginx`. Tasks, handlers and defaults moved in; `templates/atithi.conf.j2` added. `site.yml` shrinks to `roles: [nginx]`. A run with `-e app_port=8080` re-renders the config and reloads. An encrypted `db_password` in `group_vars/db.yml`. `ansible-lint` output.]**

**(Voiceover):**
Lab: `ansible-galaxy init roles/nginx` chalao. Pichhli checklist ke tasks `tasks/main.yml` mein, handler `handlers/main.yml` mein, aur `defaults/main.yml` mein `app_port: 80` aur `server_name: atithi.example`. Phir `templates/atithi.conf.j2`, jo upar wala form hai. `site.yml` mein sirf `hosts: web`, `become: true`, `roles: [nginx]`. Chalao. Ab `-e app_port=8080` ke saath chalao aur dekho ki config badli aur nginx reload hua. Ubuntu ki default nginx site port 80 par pehle se hai, isliye role mein ek task jodo jo `/etc/nginx/sites-enabled/default` hata de, tab `curl /health` par `ok` milega, warna 404. Phir `ansible-vault encrypt_string` se ek `db_password` banao, `group_vars/db.yml` mein rakho, aur ek task banao jisme `no_log: true` ho. `pipx install ansible-lint` karke `ansible-lint` chalao, aur jo cheezein wo batata hai unhe theek karo. `ansible-galaxy init` ki khaali meta aur tests files par bhi wo shikayat karega, aur role ke variables par `nginx_` jaisa prefix maangega, isliye asli roles mein `nginx_app_port` likhte hain.

### [14:20 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "role = binder · defaults for what changes · template = fill-in form · vault + no_log · lint + syntax-check + check in pipeline · Terraform builds, Ansible furnishes".]**

**(Voiceover):**
Recap: roles, templates, vault aur pipeline. Ab Atithi ke paas ek poora campus hai, jise master plan banata hai aur setup crew sajati hai. Dono AWS par. Par Atithi ab ek doosre landlord ke saath bhi kaam karne wala hai: Azure. Wahi buildings, wahi wings, bas naam alag. Aur uske saath ek ready-made head office. Agla session.

---

# 📎 Student handout: Session 29 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Terraform vs Ansible | Terraform banata hai (state hai); Ansible sajata hai (state nahi, har baar compare) |
| Agentless | Control node par Ansible; buildings par sirf SSH aur Python |
| `ansible.cfg` | `inventory`, `host_key_checking`; har command mein `-i` nahi |
| Inventory | Groups, `group_vars/`, `host_vars/`; password nahi |
| Private wing | `ansible_ssh_common_args='-o ProxyJump=...'` |
| Dynamic inventory | `amazon.aws.aws_ec2` plugin, tags se groups |
| Ad-hoc | `ansible web -m MODULE -a "..." --become`; `ping` = connection test |
| `state=` | "aisa hona chahiye", "karo" nahi |
| `command`/`shell` | Idempotent nahi; `creates` ya `changed_when`; pehle module dhoondho |
| Playbook | `hosts` + `become` + `vars` + `tasks` + `handlers` |
| Idempotency | Dusri run: `changed=0` |
| Handler | Sirf tab jab notify karne wala task `changed`; play ke aakhir mein |
| Variable precedence | defaults < group_vars < host_vars < play vars < `-e` |
| `when`, `loop`, `register` | Shart, dohrana, result rakhna |
| Dry run | `--check --diff`; `command` tasks skip ho sakte hain |
| Chhota daayra | `--limit web1`, `--tags page` |
| Role | `ansible-galaxy init`; defaults mein badalne wali cheezein |
| Template | Jinja2 `{{ }}`, `{% for %}`; `template` module; `validate` |
| Vault | `ansible-vault encrypt_string`; password Git mein nahi; `no_log: true` |
| Pipeline | `ansible-lint`, `--syntax-check`, `--check --diff`, approval, phir run |
| Safai | Lab VMs stop ya destroy |
