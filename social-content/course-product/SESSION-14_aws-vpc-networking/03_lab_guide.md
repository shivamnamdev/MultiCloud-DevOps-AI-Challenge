# Session 14 lab guide: AWS VPC networking

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> We have no AWS account. Three kinds of tests were used:
> - **Real, on your laptop:** the CIDR arithmetic (Python's `ipaddress`), and the **gatehouse** idea with real SSH between three Docker containers, including `ProxyJump`.
> - **Emulator (`floci`, not AWS):** the VPC **API**: the campus, subnets, gate, route tables, NAT, security groups, peering. It answered like AWS for the rules we tried (ranges, overlaps, dependencies), but it **does not move any traffic**.
> - **Not tested at all:** whether a public building can really be reached, whether a private building can really use the NAT, ping across a peering, security groups or NACLs actually blocking, Session Manager, the console, real costs and timings.
> It was also lenient in places, and we say where.

> **Update, tested on real AWS (ap-south-1, built and deleted the same day).** A real campus: VPC `10.0.0.0/16`, two public and two private wings in two zones, internet gateway, NAT gateway, a gatehouse and a private building, and a second campus for peering.
> - **Address rules are the same as the emulator's:** a wing outside the campus (`InvalidSubnet.Range`), overlapping a wing (`InvalidSubnet.Conflict`), a `/29` (`InvalidSubnet.Range`, the smallest is `/28`), a campus `/8` or `/29` (`InvalidVpc.Range`). The new campus's main route table had only `10.0.0.0/16 local`.
> - **The NAT, real:** `available` about **1 minute** after creation, **deleting about 1.5 minutes**. From the private building (reached through the gatehouse) `curl https://example.com` gave `HTTP/2 200`, and its outside address was **exactly the NAT's Elastic IP**. With the `0.0.0.0/0` route deleted, `curl` timed out (exit 28); with the route back it worked. After deleting the NAT gateway, the route showed **`blackhole`**, and the **Elastic IP stayed allocated** with no association (release it, it bills). Without a NAT the private building could not even call the Secrets Manager API (the call hung): a private wing needs a NAT or a VPC endpoint for AWS services.
> - **The gatehouse on a real Mac (OpenSSH 10.3):** laptop to the gatehouse worked; laptop straight to the private address `Operation timed out`; **`-i key -J gatehouse private` failed on the first hop (`Permission denied (publickey)`)**, the correction already in this guide, also on macOS. A config file with `IdentityFile` and `ProxyJump` worked, and so did `-J` with an agent holding the key. Only `authorized_keys` was on the gatehouse.
> - **Security groups and NACLs, real:** the database door (port 5432 from the app's group) was open from the app and **blocked from the gatehouse**. A custom NACL starts with only deny rules. A deny rule with a lower number (`50`) beat an allow at `100`, and allowing port 22 inbound without allowing the replies outbound also timed out: **NACLs are stateless**. Restoring the rules fixed it.
> - **Peering, real:** the request went `pending-acceptance`, then `active`. **A request between overlapping ranges (`10.0.0.0/16` and `10.0.0.0/20`) was accepted into a `failed` state** (reason: overlapping CIDR range), not refused at once as the script says. Ping from the gatehouse to a building in the other campus: **100% loss** with the peering active but no routes, still lost with a route on one side only, still lost with routes both ways but **no ICMP rule in the other group**, and **0% loss only with all of them**.
> - **Deleting in order, real:** `delete-vpc` with parts left: `DependencyViolation`. Deleting an **attached** internet gateway: `DependencyViolation` (the emulator allowed it). Detaching it while a public address was still mapped: `Network ... has some mapped public address(es)`.
> - Not tested: Session Manager, `ssh -A`, VPN, Transit Gateway, VPC endpoints.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 35 min, Part C 30 min, Part D 35 min |
| **Cost** | Free here. A real NAT gateway bills by the hour plus data, and an Elastic IP that is not in use bills too; delete them first. |
| **Skill check before you start** | Sessions 4, 5 (SSH, ports), 8 (the emulator setup, security groups). Docker installed. |

## Before you start

```bash
chmod +x lab_files/emulator/* lab_files/*.sh
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
```

(See the Session 8 guide. Run `docker rm -f floci-lab` when you finish.) `lab_files/vpc_demo.sh` runs Parts B and C by API in one go.

---

## Part A: addresses by hand (Episode 1)

Write the answers for the script's five blocks on paper first. Then check with `lab_files/cidr_lab.py` (it runs with plain Python 3, no install):

```bash
python3 lab_files/cidr_lab.py
```

Expected (ours):

```
10.0.0.0/16      addresses= 65536 first=10.0.0.0 last=10.0.255.255  AWS usable=65531
10.0.1.0/24      addresses=   256 first=10.0.1.0 last=10.0.1.255  AWS usable=251
10.0.2.0/25      addresses=   128 first=10.0.2.0 last=10.0.2.127  AWS usable=123
10.0.3.0/28      addresses=    16 first=10.0.3.0 last=10.0.3.15  AWS usable=11
192.168.1.0/30   addresses=     4 first=192.168.1.0 last=192.168.1.3  AWS usable=0
```

`AWS usable` subtracts the five addresses AWS keeps in every subnet. And the script's own checks: `10.0.2.0/25` gives `128 10.0.2.0 10.0.2.127`; `10.0.1.0/24` and `10.0.1.128/25` **overlap** (`True`); and `/16` split into `/24`s starts `10.0.0.0/24`, `10.0.1.0/24`, `10.0.2.0/24`.

The "start must be a multiple of the block size" rule, shown: `ipaddress.ip_network("10.0.1.64/24")` raises `ValueError: 10.0.1.64/24 has host bits set`, and with `strict=False` it quietly becomes `10.0.1.0/24`. The plan of the script (campus `10.0.0.0/16`, four wings) checked out: all four inside the campus, none overlapping. Overlap with a team that picked `10.0.5.0/24` is `True`, with the default VPC `172.31.0.0/16` it is `False`.

**A thing to notice:** `192.168.1.0/30` has four addresses, so AWS would have zero usable ones. It is a good answer to "how big is it", and a bad subnet (Part B shows the emulator refusing a `/29` and `/30`).

**Check yourself:**

- [ ] You can turn `/24`, `/25`, `/28` into an address count without a tool.
- [ ] You know why `10.0.1.64/24` is not a valid network address.

---

## Part B: the campus, wings and gate (Episodes 2 and 3)

### B1. The campus and its wings

```bash
V=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=atithi-vpc}]' --query Vpc.VpcId --output text)
mk() { aws ec2 create-subnet --vpc-id $V --cidr-block $1 --availability-zone $2 --query Subnet.SubnetId --output text; }
PA=$(mk 10.0.1.0/24 us-east-1a); PB=$(mk 10.0.2.0/24 us-east-1b); RA=$(mk 10.0.11.0/24 us-east-1a); RB=$(mk 10.0.12.0/24 us-east-1b)
aws ec2 describe-subnets --filters Name=vpc-id,Values=$V --query 'Subnets[].[CidrBlock,AvailabilityZone,AvailableIpAddressCount]' --output text
```

(The script uses Mumbai; the emulator's zones are `us-east-1a`, `b`, `c`.) Expected (ours): the four wings, each `251` available (256 minus the 5 kept by AWS). **The emulator knew the AWS rules and refused:**

| Request | Answer |
|---|---|
| a wing `192.168.1.0/24` outside the campus | `InvalidSubnet.Range ... The CIDR '192.168.1.0/24' is invalid.` |
| a wing `10.0.1.128/25` inside an existing wing | `InvalidSubnet.Conflict ... conflicts with another subnet` |
| a wing `10.0.3.0/29` or `/30` | `InvalidSubnet.Range` (we got `/28` accepted: **the smallest is `/28`**) |
| a campus `10.0.0.0/8` or `10.5.0.0/29` | `InvalidVpc.Range` (a campus must be between `/16` and `/28`) |

The `/16`-to-`/28` limits are AWS's rules as we remember them from its documentation, and the emulator matched them; check your region's quotas.

### B2. The main gate and the public direction board

```bash
aws ec2 describe-route-tables --filters Name=vpc-id,Values=$V --query 'RouteTables[].[Associations[0].Main,Routes[].[DestinationCidrBlock,GatewayId]]'
IGW=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text)
aws ec2 attach-internet-gateway --internet-gateway-id $IGW --vpc-id $V
PUB=$(aws ec2 create-route-table --vpc-id $V --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PUB --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW
for s in $PA $PB; do aws ec2 associate-route-table --route-table-id $PUB --subnet-id $s; aws ec2 modify-subnet-attribute --subnet-id $s --map-public-ip-on-launch; done
aws ec2 describe-route-tables --route-table-ids $PUB --query 'RouteTables[0].[Routes[].[DestinationCidrBlock,GatewayId],length(Associations)]'
```

Expected (ours): the new campus's **main route table has only `10.0.0.0/16 local`**: everything inside the campus, nothing outside. After the steps, `public-rt` has `10.0.0.0/16 local` and `0.0.0.0/0 igw-...`, with `2` wings associated, and both public wings have `MapPublicIpOnLaunch True` while the private ones stay `False`. That is the script's definition made visible: **a "public" wing is just a wing whose route table has a road to the gate**, plus a rule to give new buildings a public address. Whether a building there can really be reached from the internet, we could not test.

### B3. The dispatch desk (NAT) and the private board

```bash
EIP=$(aws ec2 allocate-address --query AllocationId --output text)
NAT=$(aws ec2 create-nat-gateway --subnet-id $PA --allocation-id $EIP --query NatGateway.NatGatewayId --output text)
PRV=$(aws ec2 create-route-table --vpc-id $V --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PRV --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT
for s in $RA $RB; do aws ec2 associate-route-table --route-table-id $PRV --subnet-id $s; done
```

Expected (ours): the NAT was `available` quickly (real ones take a minute or more), and `private-rt` got `0.0.0.0/0` pointing at it. Note that the NAT sits in a **public** wing (`$PA`) and the private wings point **at it**. We could not run the script's `curl -sI https://example.com` from a private building, because the emulator has no traffic.

**What the emulator got wrong.** The script says that if you remove the NAT row, `curl` hangs. We deleted the NAT gateway itself instead, and the route to it still showed as `active`. On real AWS such a route becomes a **`blackhole`** route. So do not use this emulator to learn that failure.

Also after deleting the NAT, the **Elastic IP was still allocated** (`203.0.113.1`, no association): release it, or on real AWS it bills.

### B4. The door guards

```bash
BSG=$(aws ec2 create-security-group --group-name bastion-sg --description gatehouse --vpc-id $V --query GroupId --output text)
ASG=$(aws ec2 create-security-group --group-name app-sg --description app --vpc-id $V --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $BSG --protocol tcp --port 22 --cidr 203.0.113.7/32
aws ec2 authorize-security-group-ingress --group-id $ASG --protocol tcp --port 22 --source-group $BSG
```

Both rules were accepted: the gatehouse allows port 22 from one address, the private building allows port 22 **only from the gatehouse's group** (a group reference, not an address list). Security group versus NACL (stateful versus stateless, the numbered rules) is the script's reading: we did not test any of it, and we did not create a NACL.

**Check yourself:**

- [ ] You can say what makes a wing "public".
- [ ] You saw the emulator refuse an overlapping and a too-small wing.
- [ ] You know what you did not see: a packet crossing the NAT.

---

## Part C: the gatehouse for real (Episode 4)

`lab_files/gatehouse_demo.sh` builds three machines in Docker and does real SSH. It needs the practice image from Session 6 (`atithi-ubuntu:lab`). The three: `laptop` (public network only), `bastion` (public **and** private network), `app` (private network only).

```bash
docker build -t atithi-ubuntu:lab -f ../SESSION-06_bash-scripting/lab_files/Dockerfile.ubuntu ../SESSION-06_bash-scripting/lab_files   # once
cd lab_files && ./gatehouse_demo.sh
```

What we saw:

```
1) laptop to the gatehouse:                       in the gatehouse: bastion
2) laptop straight to the private building:       ssh: Could not resolve hostname app: Name or service not known
3a) the script's command (-i key plus -J):        ubuntu@bastion: Permission denied (publickey,password).
3b) config file with IdentityFile and ProxyJump:  in the private building: app
3c) -J with an agent that holds the key:          in the private building: app
4) is the key on the gatehouse?                   only authorized_keys, no .pem
5) stop the gatehouse, try again:                 ssh: Could not resolve hostname bastion: Name or service not known
```

What it teaches:

- **2:** the private building cannot be reached directly. (In real AWS it would simply have no route from the internet.)
- **3a, a correction to the script:** `ssh -i atithi.pem -J ubuntu@GATEHOUSE ubuntu@PRIVATE` **failed** on the first hop. With OpenSSH `9.6` (Ubuntu 24.04), `-i` is used for the final building, **not** for the jump host. Either put the key in `~/.ssh/config` for both (3b), or load it into an agent with `ssh-add atithi.pem` first (3c). We did not test on macOS's or Windows's `ssh`; your results may differ. The script now says this.
- **4:** the private key never reached the gatehouse: the script's "chaabi kabhi gatehouse par nahi jaati", checked. (We did **not** test `ssh -A` agent forwarding, which the script warns about.)
- **5:** the gatehouse is the only road. Keep it small and watched.

The `~/.ssh/config` we used:

```
Host bastion app
  User ubuntu
  IdentityFile ~/atithi.pem
  IdentitiesOnly yes
Host app
  ProxyJump bastion
```

### C2. Peering

```bash
V2=$(aws ec2 create-vpc --cidr-block 10.1.0.0/16 --query Vpc.VpcId --output text)
PCX=$(aws ec2 create-vpc-peering-connection --vpc-id $V --peer-vpc-id $V2 --query VpcPeeringConnection.VpcPeeringConnectionId --output text)
aws ec2 describe-vpc-peering-connections --vpc-peering-connection-ids $PCX --query 'VpcPeeringConnections[0].Status.Code' --output text
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PCX
aws ec2 create-route --route-table-id $PRV --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PCX
aws ec2 create-route --route-table-id $R2 --destination-cidr-block 10.0.0.0/16 --vpc-peering-connection-id $PCX
```

(`$R2` is the second campus's route table.) Expected (ours): `pending-acceptance`, then `active`, and a route in **each** direction board: the script's "dono direction boards mein doosre ka CIDR". **Ping across it was not tested.** We also tried to peer with a campus using an **overlapping** range (`10.0.0.0/20` against `10.0.0.0/16`): **the emulator accepted it.** Real AWS refuses peering between overlapping ranges (the script's "overlap = future pain"). Do not trust this emulator on that rule.

### C3. Deleting in the right order

`aws ec2 delete-vpc` failed with `DependencyViolation ... has dependencies and cannot be deleted.` while subnets and gateways remained. The script's order is: peering, NAT and Elastic IP, buildings, subnets, gateway, then the campus. The emulator also let us delete an attached internet gateway without detaching it first, which real AWS would not: detach first.

**Check yourself:**

- [ ] You saw the private building unreachable except through the gatehouse.
- [ ] You know the two ways to give the key to both hops.
- [ ] You know the emulator's two blind spots: the blackhole route, and overlapping peering.

---

## Clean up

```bash
docker rm -f floci-lab bastion app laptop 2>/dev/null
docker network rm awslab pubnet privnet 2>/dev/null
```

(`gatehouse_demo.sh` removes its own containers and networks at the end.) On real AWS, release the Elastic IP, delete the NAT gateway **first** (it bills hourly), then everything in the script's order.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `host bits set` in Python | The block does not start at a multiple of its size | Use the network address, or `strict=False` |
| `InvalidSubnet.Conflict` | Two wings overlap | Re-plan the ranges |
| `Permission denied` on the gatehouse hop only | `-i` does not apply to the jump host | `IdentityFile` in `~/.ssh/config`, or `ssh-add` |
| `DependencyViolation` deleting the campus | Something still lives in it | Delete the parts first, in order |
| Private building cannot reach the internet (real AWS) | Missing route to the NAT, NAT in a private wing, or NAT without an Elastic IP | Check the three, in that order |
| `Connection timed out` over a peering | A direction board or a security group is missing a CIDR | Check both sides |

## What we did not test

- **Any real traffic through the campus:** internet to a public building, a private building through the NAT, ping over a peering, security groups and NACLs blocking.
- **A `blackhole` route,** AWS refusing overlapping peering, and AWS refusing to delete an attached gateway (the emulator was lenient).
- **Session Manager** (the gatehouse-free way), `ssh -A`, NACL rules, VPN, Transit Gateway.
- **macOS and Windows `ssh`** behaviour with `-J`, and **the console.**
