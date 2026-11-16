# ✍️ 02: SCRIPT — SESSION-14: AWS VPC Networking
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S14`
- **Focus:** IP addresses and CIDR arithmetic, planning a VPC, subnets and Availability Zones, route tables (longest match, main vs custom), internet gateway, public vs private subnet, NAT gateway (and the Session 05B callback), gateway endpoints, security groups vs NACLs, bastion host and Session Manager, VPC peering, troubleshooting "it times out"
- **Builds on:** Session 03 (IP, ports, DNS), Session 05B (masquerade NAT and port forwarding on a Linux gateway), Session 08 (security groups), Session 09 (roles for Session Manager), Session 11 (security group chain), Session 12 (S3), Session 13 (the private wing for the database)
- **Story position:** Zoom level 2, the rented campus, from the architect's side. Pehle ke sessions mein hum campus mein rehte rahe. Aaj hum campus ka naksha khud banate hain: number range, do wing, main gate, direction boards, dispatch desk, do tarah ke guard, gatehouse aur skywalk.
- **Story words used:** campus (VPC), wing (subnet), main gate (internet gateway), direction boards (route table), dispatch desk (NAT gateway), door guard (security group), wing guard (NACL), gatehouse (bastion), skywalk (peering), tower (Availability Zone), duty badge (role), guest (end user), staff (admin)
- **Lab project:** the Atithi campus: one public wing (marshal, gatehouse), one private wing (booking buildings, database), a dispatch desk, and a skywalk to a second campus.
- **Cost rule (AWS):** a NAT gateway is billed by the hour and per GB, and an Elastic IP or a public IPv4 address can be billed too. Check the live pricing page before the lab. Every lab ends with deleting the NAT gateway, releasing the Elastic IP, terminating instances, deleting the peering and the VPCs.
- **Episodes:**
  - Episode 1: Campus ke Number: IP aur CIDR
  - Episode 2: Campus ka Naksha: VPC, Wing, Direction Boards aur Main Gate
  - Episode 3: Dispatch Desk aur Do Tarah ke Guard: NAT, SG aur NACL
  - Episode 4: Poora Campus: Gatehouse, Private Wing aur Skywalk

---

# 📺 EPISODE 1: Campus ke Number

### [00:00 – 02:40] Scene 1: Society ke Flat Number
**[VISUAL: A housing society with blocks A, B, C. Block A has flats 101 to 110, block B flats 201 to 210. A delivery person reads the block first, then the flat. Beside it, the IP `10.0.1.25` split into a network part and a host part.]**

**(Voiceover):**
Ek badi society mein flats ke number kuch aise hote hain: block A ke 101 se 110, block B ke 201 se 210. Delivery wala pehle block dekhta hai, phir flat. IP address bhi aisa hi hai: ek hissa batata hai ki kaun si network, aur doosra hissa kaun si machine. Ab tak humne IP address ko ek number samjha tha, jaise Session 3 mein. Aaj hum use todenge, kyunki Atithi ka campus khud banane ke liye ye hisaab zaroori hai: kitne kamre, kitne wing, aur kitne guests ko jagah. Isi hisaab ka naam CIDR hai.

### [02:40 – 05:25] Scene 2: IPv4, Bits aur Slash
**[VISUAL: `10.0.1.0/24` with four octets and 32 bits drawn underneath. The first 24 bits shaded "network", the last 8 "hosts". A table: /16 = 65,536, /24 = 256, /28 = 16, /32 = 1.]**

**(Voiceover):**
IPv4 address chaar numbers ka hota hai, jaise `10.0.1.25`, aur har number ek octet, yaani aath bit. Kul battees bit. CIDR mein `10.0.1.0/24` ka matlab: pehle chaubees bit network ke liye tay, baaki aath bit machines ke liye. Aath bit ka matlab do ki ghaat aath, yaani 256 addresses. `/16` mein 65,536, `/28` mein sirf 16, aur `/32` mein sirf ek. Yaad rakhne ka tareeka: slash ke baad jitna bada number, network utna chhota. Aur AWS har subnet mein paanch addresses apne liye rakh leta hai: pehle chaar aur aakhri ek. Isliye `/28` mein sirf gyarah use ho paate hain.

### [05:25 – 08:15] Scene 3: Haath se Hisaab: Block Size
**[VISUAL: A subnet `10.0.2.0/25` worked out on a whiteboard: 128 addresses, range `10.0.2.0` to `10.0.2.127`. The next /25 starts at `10.0.2.128`. A line "block size = 2^(32 − slash)" and a ruler that shows blocks of 256, 128, 64, 32.]**

**(Voiceover):**
Haath se hisaab karna seekh lo, kyunki baad mein tool ke bharose chalna mushkil padta hai. Block size ka formula: do ki ghaat battees minus slash. `10.0.2.0/25` ka matlab ek sau atthaaees addresses: `10.0.2.0` se `10.0.2.127` tak. Agla `/25` wahin shuru hota hai jahan pehla khatam hua, yaani `10.0.2.128`. Isi tarah `/26` mein chaunsath, `/27` mein battees. Ek aur niyam: subnet ka shuru ka address hamesha apne block size ka guna hona chahiye. `10.0.2.64/25` galat hai, kyunki chaunsath, ek sau atthaaees ka guna nahi hai. Ye ek hi cheez hai jo exam mein aur asli campus mein dono jagah kaam aati hai.

### [08:15 – 11:30] Scene 4: Private Ranges aur Campus ki Yojana
**[VISUAL: Three private ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. A plan: Atithi campus `10.0.0.0/16`. Four wings carved out: `10.0.1.0/24` public tower A, `10.0.2.0/24` public tower B, `10.0.11.0/24` private tower A, `10.0.12.0/24` private tower B. A red stamp on an overlapping pair.]**

**(Voiceover):**
Private networks ke liye teen range alag rakhi gayi hain: `10.0.0.0/8`, `172.16.0.0/12` aur `192.168.0.0/16`. Inhe internet par koi nahi dekhta. Atithi ke campus ke liye `10.0.0.0/16`, yaani chaunsath hazaar se zyada addresses. Usme chaar wing: do public, do private, har type ka ek ek tower mein. Isliye `10.0.1.0/24` aur `10.0.2.0/24` public, aur `10.0.11.0/24` aur `10.0.12.0/24` private. Number sochkar rakho, taaki dekhte hi pata chale ki wo kis type ka wing hai. Ek rule: jinhe aap kabhi jodoge, jaise doosra campus, ya aapka purana office, unke ranges overlap nahi hone chahiye. Overlap ho gaya to baad mein badalna bahut dukhdayi hai, kyunki VPC ka main range badla nahi jaata. Haan, baad mein ek aur range jod sakte ho.

### [11:30 – 13:50] Scene 5: Lab: Subnet Calculator Haath se
**[VISUAL: A worksheet with five CIDRs and empty boxes for addresses, first and last. A Python panel: `import ipaddress`, `n = ipaddress.ip_network("10.0.2.0/25")`, `print(n.num_addresses, n[0], n[-1])`, `a.overlaps(b)`, and `list(net.subnets(new_prefix=24))`.]**

**(Voiceover):**
Lab. Paanch CIDR haath se likho: `10.0.0.0/16`, `10.0.1.0/24`, `10.0.2.0/25`, `10.0.3.0/28`, `192.168.1.0/30`. Har ek ke addresses ki ginti aur pehla aur aakhri address. Phir Python se check:
```python
import ipaddress
n = ipaddress.ip_network("10.0.2.0/25")
print(n.num_addresses, n[0], n[-1])
a = ipaddress.ip_network("10.0.1.0/24")
b = ipaddress.ip_network("10.0.1.128/25")
print(a.overlaps(b))
print(list(ipaddress.ip_network("10.0.0.0/16").subnets(new_prefix=24))[:3])
```
Ye batata hai ki `10.0.1.128/25` poora `10.0.1.0/24` ke andar hai, isliye overlap hai. Aakhri line se `/16` ko `/24` mein todne ka tareeka dikhta hai. Isi tarah ek chhoti parchi likh sakte ho jo Atithi ke saare wing ki list bana de.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "/24 = 256 · 2^(32−slash) · AWS keeps 5 · start must be a multiple of block size · overlap = future pain".]**

**(Voiceover):**
Recap: IP, CIDR, block ka hisaab aur campus ki yojana. Ab naksha banane ka waqt: VPC.

---

# 📺 EPISODE 2: Campus ka Naksha

### [00:00 – 02:30] Scene 1: Default Campus se Apne Campus tak
**[VISUAL: The default VPC `172.31.0.0/16` with identical public subnets in every tower, drawn as a prefabricated campus. Beside it, a blank plot with the Atithi plan drawn on it.]**

**(Voiceover):**
Ab tak Atithi ki buildings landlord ke bane banaye default campus mein rahi hain. Wo default VPC hai, `172.31.0.0/16`, jisme har tower mein ek public wing pehle se bana hota hai. Seekhne ke liye theek, par asli hotel chain ke liye kaafi nahi: na private wing, na apna number plan, aur sab kuch ek jaisa. Is episode mein hum apna VPC, yaani Virtual Private Cloud, banate hain: ek region mein, ek number range ke saath, aur har cheez apni jagah par. VPC ke andar aap tay karte ho ki kaun kisse baat karega, aur bahar se kaun andar aayega.

### [02:30 – 04:55] Scene 2: VPC, Subnet aur Tower
**[VISUAL: A VPC rectangle across a region. Two towers (AZs) each containing a public and a private subnet, with a CIDR tag and a tower tag on each subnet. A note: "one subnet lives in one tower only".]**

**(Voiceover):**
VPC ek region mein rehta hai, aur uska main CIDR aap tay karte ho, jaise `10.0.0.0/16`. Subnet VPC ka ek chhota hissa hai, yaani ek wing. Ek subnet sirf ek tower mein hota hai, kabhi do mein nahi. Isliye high availability ke liye har tier ke wing do towers mein banate hain, jaise Session 11 ka marshal do towers ki buildings ko jodta tha. Ek aur baat: subnet ko public ya private naam uska nahi, uske direction board ka milta hai. Naam mein `public` likhne se kuch nahi hota. Ab dekhte hain wo direction board kya hai.

### [04:55 – 07:50] Scene 3: Direction Boards: Route Table
**[VISUAL: A route table with two rows: `10.0.0.0/16 → local` and `0.0.0.0/0 → igw-xxxx`. An arrow shows a packet to `10.0.2.7` taking the local row and a packet to `8.8.8.8` taking the default row. A label "most specific match wins".]**

**(Voiceover):**
Route table wo direction board hai jo har wing ke bahar lagta hai. Har row bolti hai: is address ki taraf jaana ho to is darwaze se jaao. Har VPC mein ek `local` row hoti hai, jo campus ke andar sab ko ek doosre tak pahunchne deti hai. `0.0.0.0/0` ka matlab "baaki sab kuch", yaani default raasta. Agar kai rows ek address se milti hon, to sabse specific wali jeetti hai, matlab sabse bada slash. Isliye `10.0.2.7` local row se jaayega, aur `8.8.8.8` default row se. Ek chhota jaal: console mein `Main` route table hoti hai jo har naye subnet ko by default mil jaati hai. Use badalne ke bajaye apni alag route table banao.

### [07:50 – 10:50] Scene 4: Main Gate: Internet Gateway
**[VISUAL: An internet gateway icon attached to the VPC edge. A public wing's route table has `0.0.0.0/0 → igw`. A building inside has a public IP shown to the gateway as a one-to-one tag: private `10.0.1.25 ↔ public 13.x.x.x`. A building without a public IP is shown stuck at the gate.]**

**(Voiceover):**
Internet gateway, IGW, campus ka main gate hai. Wo VPC se attach hota hai, aur akela kuch nahi karta. Public wing wo hai jiske direction board mein `0.0.0.0/0` ka raasta IGW ki taraf jaata hai. Par ek aur cheez zaroori hai: building ke paas public IP hona chahiye. IGW building ke private address ko uske public address se ek-ek karke badalta hai, jo ek simple NAT hai. Bina public IP ke building gate tak aati hai par bahar nahi jaa paati. Aur public IPv4 address ka ab alag kharcha hai, jo live pricing page par hai. Isliye public wing mein sirf wahi cheezein rakho jinhe sach mein public hona hai: marshal aur gatehouse. Booking buildings aur database private wing mein.

### [10:50 – 13:30] Scene 5: Lab: Campus Zero se
**[VISUAL: Console: Create VPC `10.0.0.0/16` → two public subnets `10.0.1.0/24`, `10.0.2.0/24` → two private subnets `10.0.11.0/24`, `10.0.12.0/24` → Create IGW, attach → route table `public-rt` with `0.0.0.0/0 → igw`, associated with both public subnets → enable auto-assign public IPv4 on the public subnets.]**

**(Voiceover):**
Lab. VPC banao, `10.0.0.0/16`, naam `atithi-vpc`. Chaar subnets: do public, `10.0.1.0/24` aur `10.0.2.0/24`, do alag towers mein, aur do private, `10.0.11.0/24` aur `10.0.12.0/24`, wahi do towers. Internet gateway banao aur VPC se attach karo. Phir ek nayi route table `public-rt` banao, usme `0.0.0.0/0` ko IGW par point karo, aur use dono public subnets se jodo. Public subnets par auto-assign public IPv4 on karo. Ab public subnet mein ek chhoti building launch karo aur SSH karo: kaam karega. Private subnet mein ek building daalo, aur dekho ki wo internet tak nahi pahunch sakti. Ye abhi bilkul sahi hai, kyunki hum ne uske liye koi raasta banaya hi nahi.

### [13:30 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "VPC → subnets (one tower each) → route tables → IGW · public = route to IGW + public IP · custom route table, not main".]**

**(Voiceover):**
Recap: VPC, subnet, route table aur IGW. Ab sawaal: private wing ki buildings ko kabhi kabhi bahar bhi jaana hai, updates ke liye. Bina darwaza khole kaise?

---

# 📺 EPISODE 3: Dispatch Desk aur Do Tarah ke Guard

### [00:00 – 02:05] Scene 1: Bahar Jaana Hai, Andar Aane Dena Nahi
**[VISUAL: A private-wing booking building needs a security update from the internet. A red line "do not let guests in" and a dotted outbound-only path through a small desk at the main gate. Past session: the Rocky gateway from Session 05B with its masquerade line.]**

**(Voiceover):**
Private wing ki booking building ko kabhi kabhi bahar jaana padta hai: security updates download karne, ya kisi payment API se baat karne. Par koi bahar wala andar nahi aana chahiye. Session 05B yaad hai? Hum ne ek Rocky building ko dispatch desk banaya tha: andar ki buildings ke saare khat us desk ke ek public address se jaate the, aur desk yaad rakhta tha ki kis khat ka jawab kisko dena hai. Ye wahi masquerade tha. Landlord ke paas iska ek taiyar, har waqt chalne wala desk hai, jise NAT gateway kehte hain.

### [02:05 – 04:30] Scene 2: NAT Gateway
**[VISUAL: A NAT gateway in the public wing with an Elastic IP. The private route table has `0.0.0.0/0 → nat-xxxx`. Arrows: private building → NAT → IGW → internet, and the reply returning on the same path. A new connection from the internet is stopped.]**

**(Voiceover):**
NAT gateway public wing mein rehta hai, aur uske paas ek Elastic IP hota hai, wahi permanent address jo Session 10 mein dekha tha. Private wing ke direction board mein `0.0.0.0/0` ko NAT gateway par point karte hain. Private building ka khat desk se guzarta hai, desk apna public address lagata hai, aur IGW se bahar jaata hai. Jawab wapas usi raaste aata hai. Bahar se koi naya connection khud shuru nahi kar sakta, kyunki desk ko pata hi nahi ki use kise bhejna hai. Wahi cheez Session 05B ke port forwarding se ulti hai: wahan humne jaan boojh kar ek darwaza andar khola tha. Yahan koi darwaza nahi khulta.

### [04:30 – 07:00] Scene 3: Desk ka Kharcha aur Sasta Raasta
**[VISUAL: A bill with a per-hour line and a per-GB line for the NAT gateway. Beside it, a "gateway endpoint" for S3 drawn as a private pipe from the private wing to the warehouse, bypassing the desk. A second desk in the other tower.]**

**(Voiceover):**
NAT gateway ghante ke hisaab se chalta hai, aur uske upar jitna data guzarta hai uska bhi kharcha hota hai. Isliye lab ke baad hata dena. Ek NAT gateway ek hi tower mein hota hai. Do towers mein high availability chahiye to har tower mein ek desk lagta hai, aur har private wing apne tower ke desk ki taraf jaata hai. Ek sasta raasta bhi hai: S3 aur DynamoDB ke liye gateway endpoint. Session 12 ka warehouse private wing se seedha ek pipe se mil jaata hai, desk ke bina, aur is pipe ka koi kharcha nahi. Atithi ki booking building rooms ki photos S3 se padhti hai, to ye pipe bahut paisa bachayegi.

### [07:00 – 09:55] Scene 4: Do Tarah ke Guard: SG aur NACL
**[VISUAL: A comparison table with two columns. Door guard (security group): at the building door, remembers who went out so the reply is allowed, only allow rules. Wing guard (NACL): at the wing entrance, remembers nothing, checks both directions, numbered allow and deny rules. A packet path: wing guard in → door guard → building → door guard → wing guard out.]**

**(Voiceover):**
Ab do tarah ke guard. Door guard, yaani security group, building ke darwaze par khada hai. Wo yaad rakhta hai ki kisne bahar ka khat bheja, isliye jawab apne aap andar aane deta hai. Ise stateful kehte hain. Uski list mein sirf allow hote hain, aur jo likha nahi wo band hai. Wing guard, yaani NACL, poore wing ke darwaze par khada hai. Wo kuch yaad nahi rakhta, stateless hai. Isliye andar aur bahar ke rule alag alag likhne padte hain, khaaskar jawab wale ports, jo 1024 se 65535 ke beech hote hain. Isme allow bhi hote hain aur deny bhi, aur rules number ke kram mein check hote hain, sabse chhota number pehle. Default NACL sab kuch allow karta hai, aur nayi banayi hui NACL sab kuch deny karti hai.

### [09:55 – 12:25] Scene 5: Kab Kaun Sa Guard
**[VISUAL: Three cases. Case 1: allow booking buildings to reach the database → security group referencing `booking-sg`. Case 2: block one abusive IP range for all buildings in a wing → NACL deny rule 90 before an allow 100. Case 3: a broken NACL with only an inbound rule, causing a hang.]**

**(Voiceover):**
Roz ka zyadatar kaam door guard se chalta hai. Booking buildings ko database tak aane dena: database ke security group mein `booking-sg` ko source likho, jaise Session 13 mein. Kisi ek abusive IP range ko poore wing ke liye rokna ho: NACL mein ek deny rule, jiska number allow rule se chhota ho, jaise 90 aur allow 100, kyunki chhota number pehle check hota hai. NACL mein ek aam galti: andar ka rule likha, par jawab wale ports ke liye bahar ka rule bhool gaye. Tab connection aadha bana aur latak jaata hai. Isliye jab tak zaroorat na ho, NACL default par chhod do, aur security group ki zanjeer se kaam chalao.

### [12:25 – 15:05] Scene 6: Lab: Private Building ko Bahar Ka Raasta
**[VISUAL: Create a NAT gateway in a public subnet with a new Elastic IP. Edit `private-rt`: `0.0.0.0/0 → nat`. A private building (reached via the gatehouse, next episode) runs `curl -sI https://example.com` and gets a 200 or 301. From the internet, a ping and SSH to the private IP fail.]**

**(Voiceover):**
Lab. Public wing mein NAT gateway banao, ek nayi Elastic IP ke saath. Phir ek alag `private-rt` banao, usme `0.0.0.0/0` ko us NAT par point karo, aur use dono private subnets se jodo. Ab private building ke andar, jisse hum agle episode mein gatehouse ke raaste pahunchenge, `curl -sI https://example.com` chalao: jawab aayega. Ab ulta test: internet se us private building ke IP par SSH ya ping karne ki koshish karo. Wo kabhi pahunchega nahi, kyunki wahan koi public address hai hi nahi. Ek check aur: `private-rt` se NAT wali row hata do aur dekho ki `curl` latak jaata hai. Ye wahi "timeout" hai jo humne Session 13 mein dekha tha. Lab ke baad NAT gateway hatao aur Elastic IP release karo.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "NAT = out only, ek tower, ghante ka kharcha · endpoint for S3 and DynamoDB · SG stateful, allow only · NACL stateless, allow + deny, numbered".]**

**(Voiceover):**
Recap: NAT, endpoint, SG aur NACL. Ab sab ko jodkar ek poora campus banate hain, aur dekhte hain ki andar jaaye kaise.

---

# 📺 EPISODE 4: Poora Campus

### [00:00 – 01:50] Scene 1: Ek Hi Gatehouse
**[VISUAL: A campus with one small guarded gatehouse in the public wing. Staff walk through it to reach private rooms. The private building has no public address. A guard checks a list at the gatehouse.]**

**(Voiceover):**
Private building ka koi public address nahi. To admin uske andar jaaye kaise? Ek tareeka gatehouse hai, jise bastion host kehte hain: public wing mein ek chhoti, bahut surakshit building, jiske through staff andar ke buildings tak pahunchta hai. Ek hi darwaza, ek hi jagah jahan nigrani rakhi jaati hai, aur wahi jagah jahan har andar aane ki entry logbook mein likhi jaati hai. Ye wahi SSH key wali baat hai jo Session 4 mein humne sikhi thi: chaabi laptop par rahegi, gatehouse par copy nahi hogi.

### [01:50 – 04:00] Scene 2: Gatehouse ke Rules aur ProxyJump
**[VISUAL: Laptop → (port 22 from my IP) → gatehouse `bastion-sg` → (port 22 from `bastion-sg`) → private building `app-sg`. A command: `ssh -i atithi.pem -J ubuntu@GATEHOUSE_PUBLIC_IP ubuntu@PRIVATE_IP`. A cross over `scp key.pem bastion:`.]**

**(Voiceover):**
Gatehouse ke door guard ki list mein port 22 sirf aapke apne IP se. Private building ke door guard mein port 22 sirf `bastion-sg` se, kisi IP list se nahi. Ab ek hi command mein andar: `ssh -i atithi.pem -J ubuntu@GATEHOUSE_PUBLIC_IP ubuntu@PRIVATE_IP`. `-J` ka matlab hai ProxyJump: aapka laptop gatehouse ke through ek surakshit raasta kholta hai aur aapki chaabi kabhi gatehouse par nahi jaati. Isliye chaabi ki copy `scp` se gatehouse par daalna galat hai, aur ek aur khatarnak tareeka `ssh -A` agent forwarding hai, jise bhi bachana behtar hai. Gatehouse ko chhota rakho, usme kuch aur mat chalao, aur uska logbook dhyaan se dekho.

### [04:00 – 06:40] Scene 3: Gatehouse ke Bina: Session Manager
**[VISUAL: A staff laptop talking to the landlord's Systems Manager service, which opens a shell on the private building. The building wears a duty badge `AmazonSSMManagedInstanceCore`. No port 22 anywhere. A line from the building to the service through the NAT desk or interface endpoints.]**

**(Voiceover):**
Ek aur tareeka hai, jo aajkal aur behtar maana jaata hai: Systems Manager ka Session Manager. Isme gatehouse hi nahi, port 22 bhi nahi kholna padta. Staff landlord ki service se shell maangta hai, aur landlord uske badle private building ke andar ek surakshit raasta kholta hai. Iske liye teen cheezein chahiye. Ek, building par SSM agent, jo kai AMIs mein pehle se hota hai. Do, building par Session 9 ka ek duty badge, yaani role, jisme `AmazonSSMManagedInstanceCore` policy ho. Teen, building ko landlord ki SSM service tak pahunchne ka raasta: NAT desk ya VPC endpoints se. Isse har session ka logbook aur kaun andar gaya, ye sab landlord ke paas rehta hai. Hum gatehouse isliye sikha rahe hain ki bahut jagah aaj bhi wahi chalta hai.

### [06:40 – 09:25] Scene 4: Skywalk: VPC Peering
**[VISUAL: Two campuses, `10.0.0.0/16` and `10.1.0.0/16`, joined by a covered skywalk. Each side's direction board gets a row to the other campus. A warning: "A to B and B to C does not give A to C" and a second warning "overlapping numbers cannot be joined".]**

**(Voiceover):**
Maan lo Atithi ek doosra campus banata hai, `10.1.0.0/16`, analytics ke liye. Dono campuses ko seedha private raaste se jodna ho to skywalk lagta hai: VPC peering. Isme internet ka koi hissa nahi, aur dono ke number range alag hone chahiye, nahi to raasta kahan jaayega ye tay nahi hoga. Peering banane ke baad teen kaam: request accept karo, dono taraf ke direction boards mein doosre campus ke CIDR ki row jodo, aur dono taraf ke door guards mein doosri taraf ko allow karo. Ek hi kaam chhoot jaaye, to skywalk dikhta hai par kaam nahi karta. Aur peering transitive nahi: A se B aur B se C jude hon, to A se C apne aap nahi. Bahut saare campuses ho to Transit Gateway ek hub ki tarah kaam karta hai.

### [09:25 – 11:55] Scene 5: "Time Out Ho Raha Hai": Khoj ka Kram
**[VISUAL: A checklist drawn as a path from source to destination: "1 Destination listening? (service, port) 2 Door guard at destination 3 Door guard outbound at source 4 Wing guard (NACL) both directions 5 Direction boards on both sides 6 Public IP and IGW, or NAT 7 Peering routes". A tool tag: Reachability Analyzer and Flow Logs.]**

**(Voiceover):**
Jab kuch connect nahi hota, to Session 5 ka tarika yahan bhi chalta hai: ek ek kadi se raasta dekho. Pehle, kya destination par service sun rahi hai aur sahi port par? Phir destination ka door guard. Phir source ka door guard, jo aam taur par sab bahar jaane deta hai. Phir NACL, dono taraf. Phir dono taraf ke direction boards. Phir public IP aur IGW, ya private wing ke liye NAT. Aur peering ke liye dono taraf ki routes. Landlord do madadgaar bhi deta hai: Reachability Analyzer, jo bina packet bheje batata hai ki raasta kahan atakta hai, aur Flow Logs, jo har accept aur reject ka record rakhte hain. Isse "kahin kuch band hai" ka andaza nahi, jawab milta hai.

### [11:55 – 14:15] Scene 6: Lab: Poora Campus
**[VISUAL: Launch a gatehouse in a public subnet and an app building in a private subnet with the security groups described. `ssh -J` into the private building. `curl` through NAT. A second VPC `10.1.0.0/16` with one building. A peering connection, accept, routes added on both sides, `ping` between private IPs.]**

**(Voiceover):**
Lab. Public wing mein ek chhoti building launch karo, naam gatehouse, `bastion-sg` ke saath. Private wing mein ek building, `app-sg` ke saath. `ssh -i atithi.pem -J ubuntu@GATEHOUSE_IP ubuntu@PRIVATE_IP` se andar jaao, aur check karo ki wahan se `curl -sI https://example.com` NAT ke raaste chalta hai. Ab doosra VPC `10.1.0.0/16` banao, usme ek building daalo. Peering request banao aur accept karo. Dono direction boards mein doosre ka CIDR jodo, dono door guards mein ICMP allow karo, aur ek building se doosri ka private IP ping karo. Phir ek row hata kar dekho ki ping rukti hai ya nahi. Safai ka kram: peering, NAT gateway aur Elastic IP, buildings, subnets, IGW, aur aakhir mein VPCs.

### [14:15 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "gatehouse: 22 from my IP, then 22 from bastion-sg · -J, never copy the key · Session Manager needs role + agent + path · peering: accept, two routes, two SGs, no overlap · debug one link at a time". Then a control room with meters and alarms fades in over the campus map.]**

**(Voiceover):**
Recap: ek poora campus: wing, direction boards, main gate, dispatch desk, do guard, gatehouse aur skywalk. Ab sab kuch chal raha hai, par ek sawaal baaki hai: agar koi building raat ko dheemi hone lage, ya NAT desk par bill achanak badh jaaye, to pata kaise chalega? Agle session mein landlord ke meters, alarm aur chhote on-call freelancers: CloudWatch aur Lambda.

---

# 📎 Student handout: Session 14 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| CIDR | `/n` = pehle n bit network; addresses = 2^(32 − n); AWS 5 rakhta hai |
| Block start | Subnet ka shuru block size ka guna hona chahiye |
| Private ranges | `10/8`, `172.16/12`, `192.168/16` |
| Planning | Overlap nahi; wing ke number se type dikhe |
| VPC | Region mein; subnet ek tower mein |
| Public subnet | Route `0.0.0.0/0 → IGW` + public IP |
| Route table | Sabse specific row jeetti hai; main table mat badlo |
| IGW | Main gate; public IP ko private se ek-ek badalta hai |
| NAT gateway | Bahar jaane ke liye; ek tower mein; ghante + GB kharcha; Elastic IP |
| Endpoint | S3 aur DynamoDB ke liye gateway endpoint, free |
| SG | Building ka darwaza; stateful; sirf allow |
| NACL | Wing ka darwaza; stateless; allow + deny; number kram; return ports 1024 se 65535 |
| Gatehouse | `22` laptop IP se, phir `22` `bastion-sg` se; `ssh -J` |
| Session Manager | Role + SSM agent + service tak raasta; port 22 nahi |
| Peering | Accept + dono routes + dono SG; no overlap; no transitive |
| Time out ka kram | Service, SG, NACL, route, IGW ya NAT, peering; Reachability Analyzer, Flow Logs |
| Safai | Peering, NAT + Elastic IP, buildings, subnets, IGW, VPC |
