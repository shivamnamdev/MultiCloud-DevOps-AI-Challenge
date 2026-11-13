# ✍️ 02: SCRIPT — SESSION-29: Ansible
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S29`
- **Focus:** Configuration management & Terraform-vs-Ansible, inventory & ad-hoc commands, playbooks/idempotency/handlers, roles & Jinja2 templates, vault
- **Episodes:**
  - Episode 1: Ansible kyun: Terraform se Farq, Agentless Design
  - Episode 2: Inventory aur Ad-hoc Commands
  - Episode 3: Playbooks: Idempotency, Handlers aur Variables
  - Episode 4: Roles, Templates aur Vault

---

# 📺 EPISODE 1: Ansible kyun?

### [00:00 – 01:15] Scene 1: Dus Servers, Dus Alag Setup
**[VISUAL: Ten servers configured by hand over SSH. They drift: different nginx versions, different config files. A red "snowflake servers" label. Next, a single playbook applying identical config to all ten.]**

**(Voiceover):**
Terraform ne aapko dus servers bana kar de diye. Ab unke andar nginx install karna hai, config rakhni hai, aur users banane hain. Dus servers par SSH karke haath se karoge to har server thoda alag ban jayega. Isse snowflake servers kehte hain, jo apne aap mein unique aur fragile hote hain. Configuration management ka tool, Ansible, ye kaam ek jaisa aur repeatable banata hai.

### [01:15 – 05:00] Scene 2: Terraform vs Ansible
**[VISUAL: Two lanes. Terraform: "Build the house" (VPC, VM, DB, load balancer) — provisioning, state. Ansible: "Furnish the house" (packages, files, services, users) — configuration, no state file. Overlap area shown small.]**

**(Voiceover):**
Seedha farq: Terraform ghar banata hai: network, servers, database. Ansible ghar mein furniture lagata hai: packages, config files, services, users. Terraform state rakhta hai, Ansible by default state file nahi rakhta. Dono kuch cheezein kar sakte hain jo doosre ka kaam hai, par aksar saath chalte hain: Terraform se servers, aur Ansible se unka setup. Container aur Kubernetes ke zamane mein machine configuration kam hui hai, par VMs aur legacy systems mein Ansible bahut kaam aata hai.

### [05:00 – 08:30] Scene 3: Agentless Architecture
**[VISUAL: A control node with Ansible installed, SSH to managed nodes (no agent installed). Modules (Python scripts) copied to nodes, executed, results returned, then removed.]**

**(Voiceover):**
Ansible agentless hai. Control node par Ansible install hota hai, aur managed nodes par kuch nahi, sirf SSH aur Python chahiye. Ansible SSH se jaata hai, chhote Python programs, jinhe modules kehte hain, bhejta hai, chalata hai, aur result wapas leta hai. Isse setup aasaan hai: koi agent update ya sambhalne ki zaroorat nahi. Aur Ansible YAML mein likha jaata hai, to padhna aasaan hai, aur ye "kya hona chahiye" batata hai, "kaise" nahi.

### [08:30 – 11:30] Scene 4: Lab: Ansible Install aur Connection Test
**[VISUAL: A control VM and two target VMs. `pipx install ansible` or `sudo apt install ansible`. Passwordless SSH set up with `ssh-copy-id`. `ansible --version`.]**

**(Voiceover):**
Lab: do-teen Ubuntu VMs lo, ek control, baaki targets. Control par Ansible install karo, official docs ke tareeke se, aur `ansible --version` chalao. Control se targets par SSH key ke saath login set karo, jo hum Linux session mein seekh chuke hain: `ssh-copy-id ubuntu@TARGET_IP`. Test karo ki bina password ke `ssh ubuntu@TARGET_IP` chalta hai. Agle episode mein isi setup par Ansible chalayenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Terraform builds · Ansible configures · agentless via SSH · YAML".]**

**(Voiceover):**
Recap: Ansible ka maksad aur design. Ab inventory aur ad-hoc commands.

---

# 📺 EPISODE 2: Inventory aur Ad-hoc Commands

### [00:00 – 01:15] Scene 1: Kis Server Par Kya Chalana Hai?
**[VISUAL: A list of servers grouped: web1, web2 under `web`; db1 under `db`. A command targeting `web` runs on both.]**

**(Voiceover):**
Ansible ko pehle pata hona chahiye ki kin servers par kaam karna hai. Is list ko inventory kehte hain. Servers ko groups mein baanta jaata hai, jaise web aur db, taaki aap ek command se pura group target kar sako.

### [01:15 – 05:00] Scene 2: Inventory Files
**[VISUAL: An `inventory.ini` and an equivalent `inventory.yml`. Group variables: `[web:vars] ansible_user=ubuntu`. `ansible-inventory --list`. A mention of dynamic inventory for AWS/GCP.]**

**(Voiceover):**
Simple inventory:
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
Groups, aur unke variables. `ansible-inventory --list` se dekho Ansible ise kaise samajhta hai. Cloud mein servers badalte rehte hain, to dynamic inventory plugins AWS ya GCP se list khud nikaalte hain, tags ke hisaab se groups banakar.

### [05:00 – 08:30] Scene 3: Ad-hoc Commands aur Modules
**[VISUAL: `ansible web -m ping`, `ansible all -a "uptime"`, `ansible web -m apt -a "name=nginx state=present" --become`, `ansible all -m setup -a "filter=ansible_distribution*"`. A module catalogue: apt, copy, file, service, user, template.]**

**(Voiceover):**
Ad-hoc command ek ek kaam ke liye hai. `ansible web -m ping` connection test karta hai, `ansible all -a "uptime"` har server par command. Module ka matlab ek kaam ke liye tayyar program: `-m apt -a "name=nginx state=present"` nginx ko present karta hai, aur `--become` sudo ke liye. Dhyaan do `state=present`: ye "nginx hona chahiye" kehta hai, "install karo" nahi. Ye hi idempotency hai, jo hum agle episode mein detail se dekhenge. `setup` module server ke facts nikalta hai: OS, IP, memory.

### [08:30 – 11:30] Scene 4: Lab: Fleet par Kaam
**[VISUAL: Create the inventory, run ping, install nginx on `web`, check `systemctl` via `-m service`, and gather facts. Run the same `apt` command twice: the second says "ok" (no change).]**

**(Voiceover):**
Lab: upar wala inventory apne VMs ke IPs se banao. `ansible all -i inventory.ini -m ping`, sab par "pong". `ansible web -i inventory.ini -m apt -a "name=nginx state=present update_cache=yes" --become`. Pehli baar output "changed" dikhayega. Wahi command dobara chalao: ab "ok", yaani kuch nahi badla, kyunki nginx pehle se present hai. Phir `ansible web -m service -a "name=nginx state=started enabled=yes" --become`. Ek command se poori fleet par kaam.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "inventory groups · ad-hoc for quick tasks · modules · state= not 'do this'".]**

**(Voiceover):**
Recap: inventory, ad-hoc, modules. Ab asli taakat: playbooks.

---

# 📺 EPISODE 3: Playbooks

### [00:00 – 01:15] Scene 1: Ad-hoc se Playbook Tak
**[VISUAL: A scroll of 15 ad-hoc commands become a single YAML file with tasks. Version controlled in Git.]**

**(Voiceover):**
Ad-hoc commands choti cheezon ke liye hain. Asli setup, jaise nginx install, config rakhna, firewall khulna, service chalana, ek file mein likhna chahiye jo Git mein rakhi ja sake. Ise playbook kehte hain: ek YAML file jisme tasks ki list hoti hai, jo ek ya zyada groups par chalti hai.

### [01:15 – 05:00] Scene 2: Playbook ka Dhancha
**[VISUAL: A playbook: `- hosts: web`, `become: true`, `vars:`, `tasks:` with `name`, module, args; `handlers:` with `notify`. Annotated.]**

**(Voiceover):**
Playbook:
```yaml
- name: Configure web servers
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
    - name: Deploy index page
      ansible.builtin.copy:
        content: "Hello from {{ inventory_hostname }}\n"
        dest: /var/www/html/index.html
      notify: Reload nginx
    - name: Ensure nginx is running
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
Har task ka ek naam, ek module aur uske arguments.

### [05:00 – 08:30] Scene 3: Idempotency, Handlers aur Variables
**[VISUAL: A first run: "changed=3". A second run: "changed=0". A handler runs only when its notifying task changed. Variable precedence ladder: defaults → group_vars → host_vars → play vars → extra vars (`-e`).]**

**(Voiceover):**
Idempotency matlab playbook ko jitni baar chalao, natija ek hi: pehli baar changes, dusri baar `changed=0`. Isiliye Ansible safe hai. Handler sirf tab chalta hai jab usse notify karne wala task `changed` ho, jaise config badli to nginx reload. Variables kai jagah se aa sakte hain: role defaults sabse kamzor, phir group_vars, host_vars, play vars, aur command line ke `-e` sabse upar. Precedence yaad rakhna zaroori hai. Aur `command` ya `shell` module idempotent nahi hote, to unhe tab hi use karo jab koi proper module na ho.

### [08:30 – 11:30] Scene 4: Lab: Web Fleet Configure Karo
**[VISUAL: `ansible-playbook -i inventory.ini site.yml`, `--check --diff` dry run, then a real run. Browser shows each server's hostname page. Second run shows `changed=0`.]**

**(Voiceover):**
Lab: upar wala playbook `site.yml` mein save karo. Pehle `ansible-playbook -i inventory.ini site.yml --check --diff`, jo dry run hai aur batata hai kya badlega. Phir asli run. Dono servers ke IP browser mein kholo, alag hostname dikhega. Ab wahi playbook dobara chalao: `changed=0`. Ek server par index file haath se badal do aur playbook chalao: Ansible use wapas theek kar dega. Ye configuration drift ka ilaaj hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "playbook · idempotent · handlers on change · --check --diff · variable precedence".]**

**(Voiceover):**
Recap: playbooks. Ab bade projects ke liye structure: roles, templates aur secrets ke liye vault.

---

# 📺 EPISODE 4: Roles, Templates aur Vault

### [00:00 – 01:15] Scene 1: 500 Line ka Playbook
**[VISUAL: A single giant playbook file scrolling endlessly with nginx, users, firewall, monitoring tasks mixed together. A tidy folder structure replaces it.]**

**(Voiceover):**
Ek playbook jab 500 lines ka ho jaye, to padhna aur dobara use karna mushkil. Roles Ansible ka tareeka hai kaam ko saaf folders mein baantne ka: nginx ka role, users ka role, monitoring ka role. Har role ek jagah, aur kai playbooks mein reuse.

### [01:15 – 05:00] Scene 2: Role Structure aur Jinja2 Templates
**[VISUAL: `roles/nginx/{tasks,handlers,templates,defaults,files,vars,meta}`. A template `nginx.conf.j2` with `{{ app_port }}` and a `{% for %}` loop. A task using `ansible.builtin.template`.]**

**(Voiceover):**
Role ka standard structure: `tasks/main.yml`, `handlers/main.yml`, `templates/`, `defaults/main.yml` for default variables, aur `files/`. `ansible-galaxy init nginx` ye structure bana deta hai. Template Jinja2 mein hota hai: `server { listen {{ app_port }}; server_name {{ server_name }}; }`. Variables aur loops se config server ke hisaab se badalti hai. `template` module use render karke server par rakhta hai. Ansible Galaxy aur collections se community roles bhi milte hain, par unhe use karne se pehle review karo.

### [05:00 – 08:30] Scene 3: Ansible Vault aur Best Practices
**[VISUAL: `ansible-vault encrypt_string 's3cret' --name db_password`, an encrypted block in `group_vars/db.yml`, running with `--ask-vault-pass`. A checklist: roles small, tags, `ansible-lint`, never commit plain secrets.]**

**(Voiceover):**
Secrets, jaise database password, plain YAML mein Git mein nahi jaane chahiye. Ansible Vault unhe encrypt karta hai: `ansible-vault encrypt_string 's3cret' --name db_password`, aur playbook chalate waqt `--ask-vault-pass` ya password file. Production mein vault ki jagah cloud secret manager ya HashiCorp Vault bhi use hote hain. Best practices: roles chhote rakho, `tags` se partial run, `ansible-lint` se code check, aur `--check` pehle. Aur playbook ko CI mein lint karo.

### [08:30 – 11:30] Scene 4: Lab: Nginx Role
**[VISUAL: `ansible-galaxy init roles/nginx`. Move tasks and handlers into the role; add `templates/index.html.j2` using `{{ ansible_hostname }}`; set defaults. `site.yml` just calls `roles: [nginx]`. Run with `ansible-lint`.]**

**(Voiceover):**
Lab: `ansible-galaxy init roles/nginx` chalao. Pichle playbook ke tasks `tasks/main.yml` mein, handler `handlers/main.yml` mein, aur `templates/index.html.j2` mein `Hello from {{ ansible_hostname }} on port {{ app_port }}`. `defaults/main.yml` mein `app_port: 80`. Ab `site.yml` sirf itna: `- hosts: web  become: true  roles: [nginx]`. Chalao, aur `-e app_port=8080` se port badlo, aur template se config badalti dekho. `pipx install ansible-lint` karke `ansible-lint` bhi chalao.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "roles = reusable units · Jinja2 templates · vault for secrets · lint + check".]**

**(Voiceover):**
Recap: Ansible ka poora toolkit. Hum ek hi cloud, AWS, ke saath chal rahe the. Ab dusre bade cloud ko dekhte hain: Azure, aur uska DevOps platform.
