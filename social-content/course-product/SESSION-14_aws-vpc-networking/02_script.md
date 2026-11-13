# ✍️ 02: SCRIPT — SESSION-14: AWS VPC Networking
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S14`
- **Focus:** CIDR & subnetting, VPC/subnets/route tables/IGW, NAT, security groups vs NACLs, bastion + private app lab, peering
- **Episodes:**
  - Episode 1: IP aur CIDR: Network ka Hisaab
  - Episode 2: VPC, Subnets, Route Table aur Internet Gateway
  - Episode 3: Private Subnet, NAT aur Security: SG vs NACL
  - Episode 4: Poora VPC Lab: Bastion, Private Server aur Peering

---

# 📺 EPISODE 1: IP aur CIDR

### [00:00 – 01:15] Scene 1: Society ke Flat Numbers
**[VISUAL: An apartment complex with blocks A, B, C, flat numbers 101-110 in each. A delivery person reads addresses and routes by the block first.]**

**(Voiceover):**
Ek badi society mein flats ke numbers kuch aise hote hain: block A ke 101 se 110, block B ke 201 se 210. Delivery wala pehle block dekhta hai, phir flat. IP networking bhi aisi hi hai: address ka ek hissa network batata hai aur doosra hissa device. CIDR wo notation hai jisse hum ye batate hain, aur VPC ko samajhne ke liye ye pehla kadam hai.

### [01:15 – 05:00] Scene 2: IPv4 aur Subnet Mask
**[VISUAL: An IP `10.0.1.25` broken into four octets with binary underneath. A slash `/24` shown colouring the first 24 bits as "network" and the last 8 as "host".]**

**(Voiceover):**
IPv4 address chaar numbers ka hota hai, jaise `10.0.1.25`, jo kul 32 bits hai. CIDR notation mein `10.0.1.0/24` ka matlab hai pehle 24 bits network ke liye, bache 8 bits devices ke liye. 8 bit ka matlab 2 ki ghaat 8, yaani 256 addresses. `/16` mein 65,536, `/28` mein sirf 16. Slash ke baad ka number jitna bada, network utna chhota. AWS har subnet mein paanch addresses apne liye rakh leta hai, isliye `/28` mein 11 hi use hote hain.

### [05:00 – 08:30] Scene 3: Private IP Ranges aur Planning
**[VISUAL: Three private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. A VPC plan: VPC 10.0.0.0/16 split into four /24 subnets.]**

**(Voiceover):**
Private networks ke liye teen range reserve hain: `10.0.0.0/8`, `172.16.0.0/12` aur `192.168.0.0/16`. VPC ke liye aam choice `10.0.0.0/16`, jise aap chhote subnets mein baantte ho, jaise `10.0.1.0/24`, `10.0.2.0/24`. Planning ka ek rule: jo networks aap kabhi aapas mein jodoge, jaise VPC peering ya VPN se, unki ranges overlap nahi honi chahiye. Overlap ho gaya to baad mein badalna bahut dukhdayi hota hai.

### [08:30 – 11:30] Scene 4: Lab: Subnet Calculator Haath se
**[VISUAL: A table with 5 CIDR blocks. The learner fills the number of addresses, first and last address. A Python snippet with `ipaddress` confirms.]**

**(Voiceover):**
Lab: paanch CIDR likho aur haath se nikalo: `10.0.0.0/16`, `10.0.1.0/24`, `10.0.2.0/25`, `10.0.3.0/28`, `192.168.1.0/30`. Har ek ke addresses ki sankhya. Phir Python se check:
```python
import ipaddress
n = ipaddress.ip_network("10.0.2.0/25")
print(n.num_addresses, n[0], n[-1])
```
Aur ye bhi dekho ki `10.0.1.0/24` aur `10.0.1.128/25` overlap karte hain ya nahi, `ipaddress` ke `overlaps` se. Ye sab VPC design ki neev hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "/24 = 256 · bigger slash = smaller net · AWS reserves 5 · avoid overlap".]**

**(Voiceover):**
Recap: IP, CIDR, aur planning. Ab apna private network banate hain: VPC.

---

# 📺 EPISODE 2: VPC, Subnets, Route Table aur IGW

### [00:00 – 01:15] Scene 1: Apna Private Campus
**[VISUAL: A gated campus on a map with buildings (subnets), internal roads (routes), and a main gate to the public road (internet gateway).]**

**(Voiceover):**
VPC, Virtual Private Cloud, AWS ke andar aapka apna private network hai, jaise ek gated campus. Uske andar buildings yaani subnets, raaste yaani route tables, aur ek main gate yaani internet gateway. Ab tak aapne default VPC use kiya tha. Aaj hum apna banate hain, aur har hissa samajhte hain.

### [01:15 – 05:00] Scene 2: VPC, Subnet aur AZ
**[VISUAL: A VPC rectangle across a region. Inside, two AZs; each with a public and a private subnet. A tag on each subnet: CIDR + AZ.]**

**(Voiceover):**
VPC ek region mein hota hai, aur uska CIDR aap tay karte ho. Subnet VPC ka ek chhota hissa hai, aur ek subnet sirf ek AZ mein rehta hai. High availability ke liye har tier ke subnets do AZ mein banate ho. Subnet ko public ya private ka naam us ke naam se nahi, uske route table se milta hai. Chaliye dekhte hain ye route table kya hai.

### [05:00 – 08:30] Scene 3: Route Table aur Internet Gateway
**[VISUAL: A route table: `10.0.0.0/16 → local`, `0.0.0.0/0 → igw-xxxx`. Next to it a private route table with only `local`. An Internet Gateway attached to the VPC.]**

**(Voiceover):**
Route table batati hai ki traffic kidhar jayega. Har VPC mein `local` route hota hai, jisse VPC ke andar sab baat kar sakte hain. Internet gateway, IGW, VPC ko internet se jodta hai. Subnet public tab hai jab uski route table mein `0.0.0.0/0` ka rasta IGW ki taraf ho, aur instance ke paas public IP ho. Agar ye route nahi hai, to subnet private hai. Yaad rakho: IGW sirf gate hai, route aapko khud likhna padta hai.

### [08:30 – 11:30] Scene 4: Lab: VPC from Scratch
**[VISUAL: Console steps: Create VPC 10.0.0.0/16 → Create two subnets (public 10.0.1.0/24, private 10.0.2.0/24) → Create IGW and attach → Create route table with 0.0.0.0/0 → IGW; associate with public subnet → enable auto-assign public IP on public subnet.]**

**(Voiceover):**
Lab: VPC banao `10.0.0.0/16`. Do subnets: public `10.0.1.0/24` aur private `10.0.2.0/24`. Internet gateway banao aur VPC se attach karo. Ek nayi route table banao, usme `0.0.0.0/0` ko IGW par point karo, aur use public subnet se associate karo. Public subnet par auto-assign public IPv4 on karo. Ab public subnet mein ek EC2 launch karo aur SSH karo: kaam karega. Private subnet ka koi bhi instance abhi internet tak nahi pahunch sakta.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "VPC → subnets → route tables → IGW · public = route to IGW".]**

**(Voiceover):**
Recap: VPC, subnet, route table, IGW. Ab private subnet ko safe tareeke se internet dena, aur security ke do layers.

---

# 📺 EPISODE 3: Private Subnet, NAT aur Security

### [00:00 – 01:15] Scene 1: Database ko Updates Chahiye, Par Internet Nahi
**[VISUAL: A private database server needs a software update. A red line "Do not expose!" vs a dotted outbound-only path through a "NAT" box.]**

**(Voiceover):**
Private subnet mein aapka app server aur database baithe hain. Unhe internet se koi access nahi karna chahiye, par unhe khud kabhi kabhi internet jana padta hai: updates download karne, ya kisi API se baat karne. Ye "bahar jaa sakte ho, andar koi nahi aa sakta" wali suvidha NAT deta hai.

### [01:15 – 05:00] Scene 2: NAT Gateway
**[VISUAL: A NAT Gateway in the public subnet with an Elastic IP. Private route table: `0.0.0.0/0 → nat-xxxx`. Arrows: private instance → NAT → IGW → internet; return traffic comes back only on the same flow.]**

**(Voiceover):**
NAT Gateway public subnet mein rehta hai aur uske paas ek Elastic IP hota hai. Private subnet ki route table mein `0.0.0.0/0` ko NAT Gateway par point karte hain. Private instance ki request NAT se guzarti hai, IGW se internet jaati hai, aur jawab wapas usi raaste aata hai. Bahar se naye connection andar nahi aa sakte. Dhyaan: NAT Gateway ka ghante ka aur data ka charge hai, aur isliye lab ke baad delete karna chahiye. Kam kharch ke liye S3 aur DynamoDB ke liye gateway endpoints bhi hote hain.

### [05:00 – 08:30] Scene 3: Security Group vs NACL
**[VISUAL: A comparison table. SG: instance level, stateful, allow rules only. NACL: subnet level, stateless, allow and deny, numbered rules. A packet passes NACL (in) → SG → instance → SG → NACL (out).]**

**(Voiceover):**
Security group instance ke level par hota hai, stateful hai: agar request andar aane di, jawab apne aap bahar jaayega. Isme sirf allow rules hote hain. NACL subnet ke level par hota hai, stateless hai: andar aur bahar dono ke rules alag likhne padte hain, aur isme deny rules bhi hote hain, rules number ke order mein check hote hain. Zyadatar kaam security groups se hi chal jaata hai, aur NACL ek extra layer ya kisi khaas IP ko block karne ke liye use hota hai.

### [08:30 – 11:30] Scene 4: Lab: Private Instance ko Internet Do
**[VISUAL: Create a NAT Gateway in the public subnet with a new EIP. Edit the private route table: 0.0.0.0/0 → NAT. A private instance (reached via bastion) runs `curl -I https://example.com` successfully.]**

**(Voiceover):**
Lab: public subnet mein NAT Gateway banao, nayi Elastic IP ke saath. Private subnet ki route table mein `0.0.0.0/0` ko us NAT par point karo. Ab private instance mein, jisse hum agle episode mein bastion ke through pahunchenge, `curl -I https://example.com` chalao, jawab aayega. Aur ek test: internet se us private instance ke IP par ping ya SSH karne ki koshish karo, wo kaam nahi karega. Lab ke baad NAT Gateway aur uski Elastic IP delete karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "NAT = outbound only · SG stateful · NACL stateless + deny".]**

**(Voiceover):**
Recap: NAT, SG vs NACL. Ab sab ko jodkar ek poora, surakshit architecture banate hain.

---

# 📺 EPISODE 4: Poora VPC Lab — Bastion, Private Server aur Peering

### [00:00 – 01:15] Scene 1: Ek Hi Darwaza Andar Jaane ka
**[VISUAL: A building with a single guarded entrance (bastion). Inside, private rooms. Staff go through the guard to reach rooms.]**

**(Voiceover):**
Private servers par SSH kaise karein jab unka public IP hi nahi? Ek tareeka bastion host hai: ek chhota, surakshit server public subnet mein, jiske through aap andar ke servers tak pahunchte ho. Ek hi darwaza, ek hi jagah jisse hum nigrani rakhte hain.

### [01:15 – 05:00] Scene 2: Bastion Pattern aur SSH Agent Forwarding
**[VISUAL: Laptop → (SSH, port 22 from my IP) → Bastion in public subnet → (SSH, port 22 from bastion SG) → App server in private subnet. A ProxyJump command shown.]**

**(Voiceover):**
Bastion ke security group mein port 22 sirf aapke IP se. Private server ke security group mein port 22 sirf bastion ke security group se. Aap bastion ke through ek hi command mein jaa sakte ho: `ssh -J ubuntu@BASTION_IP ubuntu@PRIVATE_IP`. Private key apne laptop par hi rehne do, bastion par copy mat karo. Aur aajkal AWS Systems Manager Session Manager se bina bastion aur bina SSH port khole bhi shell mil sakta hai, jo aur surakshit hai.

### [05:00 – 08:30] Scene 3: VPC Peering
**[VISUAL: Two VPCs, 10.0.0.0/16 and 10.1.0.0/16, connected by a peering link. Each VPC's route table has a route to the other CIDR. A warning symbol: "No transitive routing, no overlapping CIDRs".]**

**(Voiceover):**
VPC peering do VPCs ke beech private connection hai, bina internet ke. Zaroori: dono ki CIDR ranges overlap na karein. Peering banane ke baad dono taraf ki route tables mein doosre ki CIDR ka rasta jodna padta hai, aur security groups mein bhi allow dena padta hai. Peering transitive nahi hai: A se B aur B se C ho to A se C apne aap nahi chalta. Bahut saare VPCs ho to Transit Gateway use hota hai.

### [08:30 – 11:30] Scene 4: Lab: End-to-End
**[VISUAL: Launch a bastion in the public subnet and an app server in the private subnet. SSH via ProxyJump works. In the private server, `curl` goes through NAT. Then a second VPC and a peering connection; ping works across private IPs.]**

**(Voiceover):**
Lab: public subnet mein bastion aur private subnet mein ek app server launch karo, security groups upar jaise. `ssh -J` se private server tak pahuncho. Wahan `curl` internet tak NAT se jaa raha hai ye check karo. Ab dusra VPC `10.1.0.0/16` banao, ek instance daalo, peering request banao aur accept karo, dono route tables update karo, aur security group mein ICMP allow karke ek instance se doosre ka private IP ping karo. Cleanup: peering, NAT Gateway, instances, aur VPCs hata do.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "bastion · private SGs · NAT out · peering needs routes + no overlap".]**

**(Voiceover):**
Recap: ek poora VPC, surakshit access, aur peering. Ab sab kuch chal raha hai, par kaise pata chalega ki kab kuch kharab hua? Agla session: CloudWatch aur serverless automation.
