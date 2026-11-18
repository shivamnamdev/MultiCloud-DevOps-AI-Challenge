# Session 29 lab guide: Ansible

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal. Commands and outputs below come from real runs (ansible-core 2.21.6, ansible-lint 26.11.0, Ubuntu 24.04 targets, nginx from the Ubuntu repository). Your timings and IDs will differ.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 25 min, Part C 35 min, Part D 45 min |
| **Cost** | Practice with **Docker** on your laptop: free. With three **cloud VMs** (one control, two targets, a database target if you want `db`): a few cents per hour for small instances. Stop or delete them afterwards. |
| **Skill check** | You can use SSH keys (Session 4), and you did Session 27 (so you know why "agentless" and "idempotent" matter). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  docker/      compose.yml  Dockerfile.control  Dockerfile.target     <- the practice buildings
  project/     ansible.cfg  inventory.ini  group_vars/web.yml  site.yml  .gitignore   <- your starting point
  solution/    the finished role, vault and lint-clean files, to compare with yours
```

## Before you start: get three or four machines

**Option 1: Docker (free, recommended for practice).** From `lab_files/docker/`:

```bash
docker compose -f compose.yml up -d --build
docker compose -f compose.yml exec control bash      # you are now on the control node, in ~/atithi-ansible
```

You get a control node plus three target buildings named `web1`, `web2` and `db1`, each with SSH, systemd and `ufw`. The targets' practice password is `ubuntu`, and the control node's `~/atithi-ansible` folder is your `lab_files/project` folder, so files you create there appear on your laptop.

Docker limits: the targets are containers, not real servers (they are `privileged` so systemd works), and there is no browser step. Use `curl` from the control node where the script says to open a browser. The firewall (`ufw`) is installed but left inactive, so the "open port 80" task proves the module works without actually filtering.

**Option 2: real VMs.** Three small Ubuntu VMs (one control, two targets), as in the script. In `inventory.ini` replace `web1` and `web2` with the targets' IPs, and open port 22 only from the control machine's IP and port 80 to the world.

When you finish, tear Docker down with `docker compose -f compose.yml down` (from `lab_files/docker/`).

---

## Part A: control node and first connection (Episode 1)

**Goal:** install Ansible, get passwordless SSH to every target, and write the small config file.

On the control node:

```bash
ansible --version
```

Expected: `ansible [core 2.21.6]` (yours may be newer) and the path of your config file. In the Docker option it is already installed with `pipx install ansible-core`. On your own VM install it from the official docs (`pipx install ansible-core` is common).

Note: `ansible-core` is only the engine. Many modules (including the `ufw` one used later) live in the **community.general collection**, which is not bundled with `ansible-core`. Install it now:

```bash
ansible-galaxy collection install community.general
```

Expected: `... was installed successfully`. Skip this and the firewall task later fails with `couldn't resolve module/action`.

### The project files

In `~/atithi-ansible` (Docker: already filled in from `lab_files/project/`):

`ansible.cfg`:

```ini
[defaults]
inventory = inventory.ini
host_key_checking = True
```

`inventory.ini` (Docker version; on VMs use the IPs):

```ini
[web]
web1
web2

[db]
db1

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_ed25519
ansible_python_interpreter=/usr/bin/python3
```

(`ansible_python_interpreter` stops a harmless warning about the discovered Python.)

### Deliberate break: connect before you have trusted the host

`host_key_checking = True` is the safe setting. Try Ansible before you have ever used SSH to the target:

```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
ansible web1 -m ping
```

Expected:

```
[ERROR]: Task failed: Failed to connect to the host via ssh: Host key verification failed.
```

Ansible does not silently trust an unknown machine. SSH to it once by hand first. That also gives you the passwordless key. For each target (password `ubuntu` in the Docker option; on VMs, your own method):

```bash
ssh-copy-id ubuntu@web1
ssh-copy-id ubuntu@web2
ssh-copy-id ubuntu@db1
ssh ubuntu@web1 hostname          # must print web1 with no password prompt
```

(`ssh-copy-id` asks "Are you sure you want to continue connecting" the first time. Answer `yes`, that is what puts the host key into `known_hosts`.)

```bash
ansible all -m ping
```

Expected: three `SUCCESS` blocks each ending in `"ping": "pong"`.

### Check yourself

- [ ] `ansible --version` shows your config file path.
- [ ] You saw the `Host key verification failed` error, and you can say why it is a good thing.
- [ ] `ansible all -m ping` returns `pong` three times.

---

## Part B: the list of buildings and one command for the fleet (Episode 2)

**Goal:** use groups and group variables, and see that the same command run twice reports `changed: false` the second time.

```bash
ansible-inventory --graph
```

Expected:

```
@all:
  |--@ungrouped:
  |--@web:
  |  |--web1
  |  |--web2
  |--@db:
  |  |--db1
```

Create `group_vars/web.yml` (already in the Docker project):

```yaml
app_port: 80
server_name: atithi.example
```

Now install nginx on the web group, twice:

```bash
ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become
ansible web -m ansible.builtin.apt -a "name=nginx state=present update_cache=yes" --become
```

Expected: the first run says `CHANGED` / `"changed": true` for each web host. The second says `SUCCESS` / `"changed": false`, because nothing needed to change. That is idempotency, the same idea as Terraform's second plan.

```bash
ansible web -m ansible.builtin.service -a "name=nginx state=started enabled=yes" --become
curl -s http://web1 | head -4
```

Expected: the nginx welcome page (`<title>Welcome to nginx!</title>`). On the very first service run you may see `changed: true` or `false`, depending on whether the package already started nginx.

### Deliberate break: someone stops nginx by hand

```bash
ssh ubuntu@web2 'sudo systemctl stop nginx'
ansible web -m ansible.builtin.service -a "name=nginx state=started enabled=yes" --become
```

Expected: `web1 | SUCCESS ... "changed": false` and `web2 | CHANGED ... "changed": true`. One command for the whole fleet, and only the broken building was fixed.

### Check yourself

- [ ] `changed` was true once and false the second time.
- [ ] Only web2 changed after you stopped nginx there.
- [ ] You can say why `state=present` is better than a shell command that runs `apt install`.

---

## Part C: one checklist for the web fleet (Episode 3)

**Goal:** turn the commands into a playbook, preview with `--check --diff`, run it, and watch it repair drift.

Look at `site.yml` (already in `lab_files/project/`). It installs nginx, writes a page that names its own building, opens port `app_port` with `ufw`, makes sure nginx runs, and has one handler that reloads nginx when the page changes.

First, start from clean web buildings so you can see a full run:

```bash
ansible web -m ansible.builtin.apt -a "name=nginx state=absent purge=yes autoremove=yes" --become
ansible-playbook site.yml --syntax-check
```

Expected: `playbook: site.yml`.

### Preview with `--check --diff`

```bash
ansible-playbook site.yml --check --diff
```

Expected: `changed` for "Install nginx", a diff showing the new page (`+Atithi Hotels, served by web1`), `changed` for the firewall task, and then:

```
TASK [Keep nginx running]
[ERROR]: Task failed: Module failed: Could not find the requested service nginx: host
```

Read this carefully: it is **not a mistake in your playbook**. Check mode does not install anything, so on a building with no nginx at all, the service task cannot find the service. `--check` is most useful on buildings that are already furnished. Run the real thing:

```bash
ansible-playbook site.yml
```

Expected play recap:

```
web1 : ok=6  changed=4  unreachable=0  failed=0
web2 : ok=6  changed=4  unreachable=0  failed=0
```

The four changes: install, page, firewall rule, and the handler's reload. Prove each building says its own name:

```bash
curl -s http://web1; curl -s http://web2
```

Expected: `Atithi Hotels, served by web1` and `... web2`.

```bash
ansible-playbook site.yml
```

Expected: `changed=0` for both. A checklist you can run all day without side effects.

### Deliberate break 1: drift on one building

```bash
ssh ubuntu@web2 'sudo systemctl stop nginx; echo hacked | sudo tee /var/www/html/index.html'
ansible-playbook site.yml --check --diff       # shows -hacked and +Atithi Hotels, served by web2
ansible-playbook site.yml
curl -s http://web2
```

Expected: web1 `changed=0`, web2 `changed=3` (nginx started, page restored, handler reload), and the page says `Atithi Hotels, served by web2` again. If you only edit the page and leave nginx running, you get `changed=2` (page plus reload).

### Deliberate break 2: a wrong package name

Copy `site.yml` to `bad.yml`, change `name: nginx` to `name: nginxx`, and run `ansible-playbook bad.yml`. Expected:

```
fatal: [web1]: FAILED! => {"changed": false, "msg": "No package matching 'nginxx' is available"}
```

Read the message, fix the name and delete `bad.yml`.

### `--limit` and tags

```bash
ansible-playbook site.yml --limit web1
```

Expected: only web1 appears in the recap. To run just the page task, add `tags: page` under the "Deploy the welcome page" task and run `ansible-playbook site.yml --tags page`. Expected: only that task (plus its reload handler if the page changed) runs.

### Save your work

```bash
git init && git add ansible.cfg inventory.ini group_vars site.yml .gitignore && git commit -m "Atithi web fleet checklist"
```

### Check yourself

- [ ] You saw `changed=4` then `changed=0`.
- [ ] You understand why `--check` stopped at the service task on empty buildings.
- [ ] You saw drift repaired on web2 only.

---

## Part D: a binder (role), a fill-in form, a sealed envelope (Episode 4)

**Goal:** move the checklist into a role, change the port from the command line, protect a password with Vault, and clean up what `ansible-lint` finds.

### D1. Build the role

```bash
mkdir solution-mine && cd solution-mine        # work here; compare with lab_files/solution later
cp ../ansible.cfg ../inventory.ini . && cp -R ../group_vars .
ansible-galaxy init roles/nginx
```

Expected: `- Role roles/nginx was created successfully`. Fill the role in as the script says. Where each piece goes:

`roles/nginx/defaults/main.yml`:

```yaml
app_port: 80
server_name: atithi.example
```

`roles/nginx/tasks/main.yml`: the tasks from `site.yml`, plus two new ones, in this order: install nginx; **remove `/etc/nginx/sites-enabled/default`** (`ansible.builtin.file` with `state: absent`, notify the handler); render the config from the template (`ansible.builtin.template`, `src: atithi.conf.j2`, `dest: /etc/nginx/conf.d/atithi.conf`, notify the handler); deploy the page; open the port; keep nginx running.

`roles/nginx/handlers/main.yml`: the "Reload nginx" handler.

`roles/nginx/templates/atithi.conf.j2`, the fill-in form:

```
server {
    listen {{ app_port }};
    server_name {{ server_name }};
    root /var/www/html;
    location /health { return 200 "ok\n"; }
}
```

`site.yml` shrinks to:

```yaml
- name: Furnish the web buildings
  hosts: web
  become: true
  roles:
    - nginx
```

Stuck? The finished version is in `lab_files/solution/`.

```bash
ansible-playbook site.yml
sleep 3; curl -s http://web1/health
```

Expected: `ok`. Without the "remove the default site" task you would get a **404**: Ubuntu's default nginx site already owns port 80 and wins. (Do not try to fix this with `default_server` in your template: it conflicts with the default site and nginx refuses to reload.)

### D2. Change the port from the command line

```bash
ansible-playbook site.yml -e app_port=8080
sleep 3
curl -s http://web1:8080/health
```

Expected: `ok` on port 8080, and a play recap with `changed=2` or `3` (config re-rendered, handler reload). Note the `sleep 3`: after a reload nginx can keep answering on the old port for a second or two, so check a moment later, not instantly. Then put it back with `ansible-playbook site.yml` and `curl -s http://web1/health`.

### D3. A sealed envelope: Vault and `no_log`

```bash
echo 'practice-vault-password' > .vault_pass && chmod 600 .vault_pass
ansible-vault encrypt_string --vault-password-file .vault_pass 'S3cret-db-pass' --name db_password
```

Expected: a block starting `db_password: !vault |` followed by `$ANSIBLE_VAULT;1.1;AES256` and hex lines. Put it in `group_vars/db.yml`, starting the file with a line `---`. (`.vault_pass` is in `.gitignore`. In real life the vault password is a secret you do not commit.)

Create `db.yml`:

```yaml
- name: Set up the database building
  hosts: db
  become: true
  tasks:
    - name: Write the database password file
      ansible.builtin.copy:
        content: "{{ db_password }}\n"
        dest: /etc/atithi-db-password
        mode: "0600"
      no_log: true
```

Run it without and with the password:

```bash
ansible-playbook db.yml
ansible-playbook db.yml --vault-password-file .vault_pass
```

Expected without it: `Attempt to use undecryptable variable: Attempting to decrypt but no vault secrets found.` With it: `db1 ... changed=1`. A missing password stops the run clearly, it never sends garbage.

### Deliberate break: show that Vault does not hide a printed secret

Vault protects the secret **at rest** (in Git), not in the output. `leak_demo.yml` (in `lab_files/solution/`) has two tasks that echo the decrypted value, one without `no_log`:

```bash
ansible-playbook leak_demo.yml --vault-password-file .vault_pass -v
```

Expected: the first task prints `"stdout": "S3cret-db-pass"` in plain text; the second prints `"censored": "the output has been hidden due to the fact that 'no_log: true' was specified"`. Any task that echoes a secret needs `no_log: true`.

### D4. Lint

```bash
ansible-lint site.yml
```

On the skeleton that `ansible-galaxy init` made, expect **8 failures**, in these families:

```
var-naming[no-role-prefix]: Variables names from within roles should use nginx_ as a prefix. (vars: app_port)
var-naming[no-role-prefix]: ... (vars: server_name)
schema[meta]: $.galaxy_info.min_ansible_version 2.2 is not of type 'string'
yaml[comments]: Missing starting space in comment     (two files)
meta-incorrect: Should change default metadata: author / company / license
```

Fix them: rename `app_port` to `nginx_app_port` and `server_name` to `nginx_server_name` everywhere in the role (defaults, tasks, template) and in `group_vars/web.yml`; write a real `roles/nginx/meta/main.yml` (author, company, license, `min_ansible_version: "2.14"` as a string); and replace the comment line in `roles/nginx/vars/main.yml`. Run `ansible-lint site.yml` again. Expected: `Passed: 0 failure(s), 0 warning(s)`.

After the rename, an old override such as `-e app_port=8080` is silently ignored (no error, no change). Use `-e nginx_app_port=8080` from now on. This is exactly why the prefix rule exists: roles must not share bare variable names.

### Cleanup

- Docker: `docker compose -f compose.yml down` from `lab_files/docker/`.
- Real VMs: stop or delete them. Check that no extra volumes or public IPs remain.
- Delete `.vault_pass` and any `*.retry` files; never commit them.

### Check yourself

- [ ] `curl http://web1/health` returns `ok`, and you know why it returned 404 before the default site was removed.
- [ ] You changed the port with `-e` and saw nginx listen on the new port.
- [ ] A decrypted secret appeared in output without `no_log`, and was hidden with it.
- [ ] `ansible-lint` passes.

---

## Final checklist for Session 29

- [ ] Part A: passwordless SSH to all targets and `pong` from `ansible all -m ping`
- [ ] Part B: same command twice gives `changed: false`; only the broken building changed
- [ ] Part C: `changed=4`, then `changed=0`; drift repaired on one building
- [ ] Part D: role works, port changed from the command line, vault and `no_log` used, lint passes
- [ ] `site.yml` and the inventory are in Git, but no vault password

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `Host key verification failed` | You have not used SSH to that host yet | `ssh` to it once, or `ssh-copy-id` |
| `couldn't resolve module/action 'community.general.ufw'` | The collection is not installed | `ansible-galaxy collection install community.general` |
| `Permission denied (publickey)` | Key not copied, or wrong user | `ssh-copy-id`, check `ansible_user` |
| `ping` works, apt fails with a permission error | Missing `--become` (or `become: true`) | Add it |
| `curl /health` returns 404 | Ubuntu's default nginx site wins | Add the task that removes `/etc/nginx/sites-enabled/default` |
| Port still answers right after you change it | nginx reload takes a moment | Wait 2 to 3 seconds and check again |
| `--check` fails at the service task | Package not installed on a fresh host | Run it for real once; use `--check` on furnished hosts |
| `Attempting to decrypt but no vault secrets found` | No vault password given | `--vault-password-file .vault_pass` |

## What we did not test

All parts ran in Docker (Ubuntu 24.04 containers with systemd, ansible-core 2.21.6). We did not run: real cloud VMs, a real firewall (`ufw` was installed but left inactive), a browser, `ssh-copy-id` with a real password prompt from a person (we supplied the password with a helper), the `amazon.aws.aws_ec2` dynamic inventory in this guide (it was tested separately against an emulator), Ansible inside a Jenkins or GitHub Actions pipeline, Molecule, third-party Galaxy roles, or Windows targets.
