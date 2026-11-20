# Session 13 lab guide: AWS RDS

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Three kinds of test were used, and you should know which is which:
> - **Real, on your laptop:** the SQL (SQLite as in the script, then a real **PostgreSQL 16** in Docker), the Python `psycopg2` lab, and the three kinds of connection failure. These are real databases and real drivers.
> - **Emulator (`floci`), not AWS:** the **API calls** for a managed database: creating an instance, its endpoint, a managed password in Secrets Manager, deletion protection, a read replica. The emulator keeps these as records. **No database actually runs behind them**: connecting to the endpoint was refused.
> - **Did not work in the emulator:** `create-db-snapshot` and restoring a snapshot, so the script's snapshot-and-restore lab was **not** run.
> **Not tested at all:** the console, real RDS timing, Multi-AZ failover, point-in-time restore, a real `db-sg` doing its job, encryption, parameter groups, real costs.

> **Update, tested on real AWS (ap-south-1, PostgreSQL on `db.t4g.micro`, deleted the same day).** The database sat in the private wings of the Session 14 campus, reached only from a private building through the gatehouse:
> - **Creating it took about 10 minutes** (`creating`, `configuring-enhanced-monitoring`, `backing-up`, `available`). The endpoint is a DNS name on port **5432**, `PubliclyAccessible False`, deletion protection on, 7 days of backups. **`StorageEncrypted` was `False`** when created from the CLI with default options (the console's default is different: tick encryption yourself). The default engine was PostgreSQL 18.3.
> - **The managed secret holds only `username` and `password`**, not host, port or engine (the emulator showed more). Keep the endpoint in your app's settings. The instance's role (policy: `GetSecretValue` on that one secret) read it; `ListSecrets` was `AccessDenied`.
> - **The security group reference works:** from the private building port 5432 was open; from the gatehouse (not in the database's group) it was blocked. The connection used **TLS 1.3** (`ssl on`).
> - **SQL on real PostgreSQL** behaved as in Part D (`Asha 2`, `Ravi 1`, the unique and foreign key errors, `4 3` for the rollback, and the psycopg2 hostile-text lab: `0` matches as a parameter, all guests when glued).
> - **The three failures, against RDS:** wrong password gave `FATAL: password authentication failed`; a **wrong port (5433) gave `timeout expired`, not "refused"** (the door guard drops it); nothing listening on the machine itself (`127.0.0.1`) gave `Connection refused`.
> - **Snapshots and restore, real:** a manual snapshot took about **3 minutes**. After I added a guest, a restore of the snapshot as a **new instance with a new endpoint** took about **8 minutes** and held the older data (**3 guests, the original 4**). It had no deletion protection and no managed secret (it uses the original password). **Point-in-time restore** to a moment before my insert took about **10 minutes** and also gave **3 guests**.
> - **Deletion protection** refused `delete-db-instance` exactly as written; deleting needs it switched off first. Deleting an RDS instance took several minutes.
> - **Multi-AZ:** the first conversion attempts failed with `InsufficientDBInstanceCapacity` (no room for `db.t4g.micro` in the second zone at that time); a later try was accepted but was **still `modifying` after 27 minutes**, so **we did not see a standby or a failover**. A **read replica** of an instance that uses a managed master password was **refused** (`... where ManageMasterUserPassword is enabled is not supported`) on this engine. Test those two on your own account, with plenty of time.
> - Not tested: MySQL, Aurora, DynamoDB, parameter groups, encryption behaviour, real costs.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 25 min, Part C 25 min, Part D 35 min |
| **Cost** | Free here. A real RDS instance bills by the hour while it exists, and snapshots bill without an instance. |
| **Skill check before you start** | Session 8 (the emulator setup), Session 11 (security groups), Session 7 (Python and `venv`). Docker installed. |

## Before you start

For the SQL labs you need Docker. For the SQLite lab we used the Ubuntu practice container from Sessions 5 and 6. Files are in `lab_files/`.

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
```

(For the emulator parts: `lab_files/emulator/start.sh`, then `export PATH="$PWD/lab_files/emulator:$PATH"`, as in the Session 8 guide. Run `docker rm -f floci-lab` when you finish.)

---

## Part A: the ledger on your laptop, in SQLite (Episode 1)

`lab_files/ledger.sql` has the script's three tables and some rows. We ran it in the Ubuntu container (`apt-get update`, then `apt-get install sqlite3`; SQLite `3.45.1`):

```bash
docker cp lab_files/ledger.sql atithi-web1:/tmp/ledger.sql
docker exec -it atithi-web1 bash
cd /tmp && sqlite3 atithi.db < ledger.sql
sqlite3 atithi.db "SELECT g.name, COUNT(*) FROM bookings b JOIN guests g ON g.id=b.guest_id GROUP BY g.name;"
```

Expected (ours): `Asha|2` and `Ravi|1`.

### A1. Rules the ledger enforces, and one it does not

```bash
sqlite3 atithi.db "INSERT INTO bookings(guest_id, room_id, night) VALUES (2,1,'2026-12-01');"
sqlite3 atithi.db "INSERT INTO bookings(guest_id, room_id, night) VALUES (99,2,'2026-12-05'); SELECT COUNT(*) FROM bookings;"
sqlite3 atithi.db "PRAGMA foreign_keys=ON; INSERT INTO bookings(guest_id, room_id, night) VALUES (99,2,'2026-12-06');"
```

What we saw:

- The same room on the same night again: `Error: stepping, UNIQUE constraint failed: bookings.room_id, bookings.night (19)`. The script's `UNIQUE` guard works.
- A booking for guest `99`, who does not exist: it **went in** (the count went from 3 to 4). **SQLite does not check foreign keys unless you turn it on** in that session.
- With `PRAGMA foreign_keys=ON;` the same kind of insert failed: `FOREIGN KEY constraint failed`. (We deleted our guest-99 row afterwards.) The script now says this.

### A2. A transaction you roll back

```bash
sqlite3 atithi.db "SELECT COUNT(*) FROM bookings; BEGIN; INSERT INTO bookings(guest_id, room_id, night) VALUES (1,2,'2026-12-10'); INSERT INTO bookings(guest_id, room_id, night) VALUES (2,2,'2026-12-11'); SELECT COUNT(*) FROM bookings; ROLLBACK; SELECT COUNT(*) FROM bookings;"
```

We saw `3`, then `5` inside the transaction, then `3` after `ROLLBACK`. Two statements, both undone: the "poora ya kuch nahi" of ACID. Remove the file afterwards: `rm atithi.db`.

**Check yourself:**

- [ ] You saw `UNIQUE` refuse a double booking.
- [ ] You know why a booking for a missing guest got in, and how to stop that.
- [ ] You saw a `ROLLBACK` undo two inserts.

---

## Part B: the managed ledger, settings only (Episode 2)

This is the API view of the script's console lab. `lab_files/rds_demo.sh` runs all of it; the main commands:

```bash
VPC=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
BSG=$(aws ec2 create-security-group --group-name booking-sg --description booking --vpc-id $VPC --query GroupId --output text)
DSG=$(aws ec2 create-security-group --group-name db-sg --description "records office door" --vpc-id $VPC --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $DSG --protocol tcp --port 5432 --source-group $BSG
aws rds create-db-instance --db-instance-identifier atithi-ledger --db-instance-class db.t4g.micro --engine postgres \
  --master-username atithi_admin --manage-master-user-password --allocated-storage 20 --no-publicly-accessible \
  --vpc-security-group-ids $DSG --backup-retention-period 7 --deletion-protection
aws rds describe-db-instances --db-instance-identifier atithi-ledger --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address,Endpoint.Port,MultiAZ,StorageEncrypted]' --output text
```

Expected (ours): the inbound rule `5432 from <booking-sg>`: the script's "5432 sirf `booking-sg` se", as a group reference, not an IP list. Then `available postgres False True 7` (status, engine, publicly accessible `False`, deletion protection `True`, 7 days of backups), and `available 172.21.0.2 7001 False False`: an endpoint and a port (the emulator used `7001`; a real PostgreSQL endpoint is a DNS name and port `5432`), Multi-AZ off. **The emulator's `StorageEncrypted` was `False`.** Do not read that as real RDS's default; check your own console.

### B1. The managed password

`--manage-master-user-password` means the password is made and kept in Secrets Manager. The instance record points to it:

```bash
ARN=$(aws rds describe-db-instances --db-instance-identifier atithi-ledger --query 'DBInstances[0].MasterUserSecret.SecretArn' --output text)
aws secretsmanager get-secret-value --secret-id "$ARN" --query SecretString --output text
```

We got a JSON with `host`, `port`, `username` (`atithi_admin`), `engine`, `dbInstanceIdentifier` and a `password` (hidden in our log). Your script reads it the way the Episode 4 lab does, with `--query SecretString --output text`, and never copies it into a notes file.

### B2. Not tested here

Connecting. We tried `psql` and `pg_isready` against the emulated endpoint: **`Connection refused`**, since nothing listens there. Part D connects to a real database instead.

**Check yourself:**

- [ ] You can say why the database's security group names `booking-sg` and not an IP.
- [ ] You know where the managed password is kept.

---

## Part C: backups, replicas and protection (Episode 3)

On the emulator:

- **`create-db-snapshot` failed** (`InvalidDBInstanceState: Failed to create snapshot`), so there was nothing to restore. The script's lab (insert rows, snapshot, restore as `atithi-restored`, compare counts) is for a real account.
- **A read replica** record was accepted: `aws rds create-db-instance-read-replica --db-instance-identifier atithi-ledger-ro --source-db-instance-identifier atithi-ledger` printed `atithi-ledger-ro atithi-ledger`. It is a record, not a copy of data.
- **Multi-AZ:** `modify-db-instance --multi-az --apply-immediately` was accepted, but the instance still reported `MultiAZ False`. We could not see a standby or a failover.
- **Deletion protection** worked: `delete-db-instance` on the protected instance failed with `InvalidParameterCombination: Cannot delete protected DB Instance, please disable deletion protection and try again.` After `modify-db-instance --no-deletion-protection`, the delete went to `deleting`. This is the script's "delete protection on" advice, seen.

PITR (restoring to a chosen second), the real order of recovery, and the cost of Multi-AZ are untested here: they need a real instance.

**Check yourself:**

- [ ] You saw deletion protection stop a delete.
- [ ] You know which of the script's backup and failover claims you have not seen yet.

---

## Part D: the building meets the ledger (Episode 4)

### D1. A real Postgres to talk to

```bash
docker run -d --name atithi-pg -e POSTGRES_USER=atithi_admin -e POSTGRES_PASSWORD=practice-only postgres:16
until docker exec atithi-pg pg_isready -h 127.0.0.1 -U atithi_admin >/dev/null 2>&1; do sleep 1; done
```

(`practice-only` is a throwaway password. `-h 127.0.0.1` for the readiness check is the Session 21 lesson.) Run the ledger in it, with one change: **in PostgreSQL, `id INTEGER PRIMARY KEY` does not number rows for you.** `lab_files/ledger_pg.sql` uses `id SERIAL PRIMARY KEY`.

```bash
docker exec -i -e PGPASSWORD=practice-only atithi-pg psql -h 127.0.0.1 -U atithi_admin -d postgres -c "CREATE TABLE t1(id INTEGER PRIMARY KEY, name TEXT NOT NULL); INSERT INTO t1(name) VALUES ('x');"
docker exec -i -e PGPASSWORD=practice-only atithi-pg psql -h 127.0.0.1 -U atithi_admin -d postgres -q < lab_files/ledger_pg.sql
```

The first: `ERROR: null value in column "id" of relation "t1" violates not-null constraint`. The second created and filled the tables. The same `JOIN ... GROUP BY` as in Part A printed `Asha 2` and `Ravi 1`. In **PostgreSQL** both guards worked without any switch: the double booking gave `duplicate key value violates unique constraint "bookings_room_id_night_key"`, and the booking for guest 99 gave `violates foreign key constraint "bookings_guest_id_fkey" ... Key (guest_id)=(99) is not present in table "guests"`. A transaction with `BEGIN ... ROLLBACK` went `3`, `4` inside, `3` after.

### D2. `psycopg2`: parameters, and why

`lab_files/app_db.py` reads the host and password from environment variables and uses `%s` parameters. We ran it from the practice container in a virtual environment (`pip install psycopg2-binary`), pointing `DB_HOST` at the Postgres container's address:

```bash
DB_HOST=<postgres container ip> DB_PASSWORD=practice-only python app_db.py
```

What we saw:

```
inserted guest id 3
safe query, hostile text matches: 0 guests
glued query: SELECT count(*) FROM guests WHERE name = 'x' OR '1'='1'
glued query matches: 3 guests (all of them)
```

The same hostile text `x' OR '1'='1` matched **no one** when passed as a parameter, and **everyone** when glued into the SQL text. That is the script's "insert mein `%s` parameter ho, text jodna nahi", shown. (The glued line is the example of what **not** to write.)

### D3. The three answers when it will not connect

Against the real Postgres:

| What we did | Answer |
|---|---|
| right address, wrong password | `psycopg2.OperationalError: connection to server at "172.17.0.4", port 5432 failed: FATAL: password authentication failed for user "atithi_admin"` |
| right address, a port nobody listens on | `ConnectionRefusedError: [Errno 111] Connection refused` |
| an address that drops packets | `TimeoutError: timed out` |

This is the script's "teen sawaal": **timeout** means the road or the door guard (a security group) is blocking you; **refused** means the machine answers but no database is listening on that port; **FATAL ... password authentication failed** means you got all the way in and the credentials are wrong. We did not use `nc -vz` (the practice image has no `nc`); a Python socket did the same job.

### D4. Clean up

```bash
docker rm -f atithi-pg
docker rm -f floci-lab
```

On real AWS: delete the database (decide on the final snapshot), `atithi-restored`, the snapshots, and the secret.

**Check yourself:**

- [ ] You saw hostile text match nothing as a parameter and everything when glued.
- [ ] You can match the three connection errors to their causes.
- [ ] Your throwaway Postgres container is gone.

---

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `null value in column "id"` in Postgres | `INTEGER PRIMARY KEY` is not automatic there | `SERIAL` (or `GENERATED ... AS IDENTITY`) |
| A bad foreign key got into SQLite | Foreign key checks are off | `PRAGMA foreign_keys=ON;` each session |
| `Connection refused` | Wrong port or nothing listening | `docker ps`, the endpoint and port |
| `timed out` | Security group, route, or a dropped address | Check the door guard first (Session 11) |
| `password authentication failed` | Wrong user or password | Read the secret again, check the user name |
| `Cannot delete protected DB Instance` | Deletion protection is on | Turn it off on purpose, then delete |

## What we did not test

- **A real database on RDS:** connecting to its endpoint, SSL, the real default of encryption, parameter groups, and performance.
- **Snapshots, restore, point-in-time recovery,** Multi-AZ standby and failover, and a read replica holding data.
- **A building reading the secret with an IAM role** (the Episode 4 permission check).
- **MySQL, Aurora, DynamoDB,** and the NoSQL part of the script.
- **Real costs,** and the console.
