# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-14_aws-vpc-networking

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,563 · **Episodes:** 4

---

# EPISODE 1: Campus ke Number

## Society ke Flat Number

Ek badi society mein flats ke number kuch aise hote hain: block A ke 101 se 110, block B ke 201 se 210. Delivery wala pehle block dekhta hai, phir flat. IP address bhi aisa hi hai: ek hissa batata hai ki kaun si network, aur doosra hissa kaun si machine. Ab tak humne IP address ko ek number samjha tha, jaise Session 3 mein. Aaj hum use todenge, kyunki Atithi ka campus khud banane ke liye ye hisaab zaroori hai: kitne kamre, kitne wing, aur kitne guests ko jagah. Isi hisaab ka naam CIDR hai.

## IPv4, Bits aur Slash

IPv4 address chaar numbers ka hota hai, jaise 10.0.1.25, aur har number ek octet, yaani aath bit. Kul battees bit. CIDR mein 10.0.1.0/24 ka matlab: pehle chaubees bit network ke liye tay, baaki aath bit machines ke liye. Aath bit ka matlab do ki ghaat aath, yaani 256 addresses. /16 mein 65,536, /28 mein sirf 16, aur /32 mein sirf ek. Yaad rakhne ka tareeka: slash ke baad jitna bada number, network utna chhota. Aur AWS har subnet mein paanch addresses apne liye rakh leta hai: pehle chaar aur aakhri ek. Isliye /28 mein sirf gyarah use ho paate hain.

## Haath se Hisaab: Block Size

Haath se hisaab karna seekh lo, kyunki baad mein tool ke bharose chalna mushkil padta hai. Block size ka formula: do ki ghaat battees minus slash. 10.0.2.0/25 ka matlab ek sau atthaaees addresses: 10.0.2.0 se 10.0.2.127 tak. Agla /25 wahin shuru hota hai jahan pehla khatam hua, yaani 10.0.2.128. Isi tarah /26 mein chaunsath, /27 mein battees. Ek aur niyam: subnet ka shuru ka address hamesha apne block size ka guna hona chahiye. 10.0.2.64/25 galat hai, kyunki chaunsath, ek sau atthaaees ka guna nahi hai. Ye ek hi cheez hai jo exam mein aur asli campus mein dono jagah kaam aati hai.

## Private Ranges aur Campus ki Yojana

Private networks ke liye teen range alag rakhi gayi hain: 10.0.0.0/8, 172.16.0.0/12 aur 192.168.0.0/16. Inhe internet par koi nahi dekhta. Atithi ke campus ke liye 10.0.0.0/16, yaani chaunsath hazaar se zyada addresses. Usme chaar wing: do public, do private, har type ka ek ek tower mein. Isliye 10.0.1.0/24 aur 10.0.2.0/24 public, aur 10.0.11.0/24 aur 10.0.12.0/24 private. Number sochkar rakho, taaki dekhte hi pata chale ki wo kis type ka wing hai. Ek rule: jinhe aap kabhi jodoge, jaise doosra campus, ya aapka purana office, unke ranges overlap nahi hone chahiye. Overlap ho gaya to baad mein badalna bahut dukhdayi hai, kyunki VPC ka main range badla nahi jaata. Haan, baad mein ek aur range jod sakte ho.

## Lab: Subnet Calculator Haath se

Lab. Paanch CIDR haath se likho: 10.0.0.0/16, 10.0.1.0/24, 10.0.2.0/25, 10.0.3.0/28, 192.168.1.0/30. Har ek ke addresses ki ginti aur pehla aur aakhri address. Phir Python se check:

Ye batata hai ki 10.0.1.128/25 poora 10.0.1.0/24 ke andar hai, isliye overlap hai. Aakhri line se /16 ko /24 mein todne ka tareeka dikhta hai. Isi tarah ek chhoti parchi likh sakte ho jo Atithi ke saare wing ki list bana de.

## Recap aur Bridge

Recap: IP, CIDR, block ka hisaab aur campus ki yojana. Ab naksha banane ka waqt: VPC.

---

# EPISODE 2: Campus ka Naksha

## Default Campus se Apne Campus tak

Ab tak Atithi ki buildings landlord ke bane banaye default campus mein rahi hain. Wo default VPC hai, 172.31.0.0/16, jisme har tower mein ek public wing pehle se bana hota hai. Seekhne ke liye theek, par asli hotel chain ke liye kaafi nahi: na private wing, na apna number plan, aur sab kuch ek jaisa. Is episode mein hum apna VPC, yaani Virtual Private Cloud, banate hain: ek region mein, ek number range ke saath, aur har cheez apni jagah par. VPC ke andar aap tay karte ho ki kaun kisse baat karega, aur bahar se kaun andar aayega.

## VPC, Subnet aur Tower

VPC ek region mein rehta hai, aur uska main CIDR aap tay karte ho, jaise 10.0.0.0/16. Subnet VPC ka ek chhota hissa hai, yaani ek wing. Ek subnet sirf ek tower mein hota hai, kabhi do mein nahi. Isliye high availability ke liye har tier ke wing do towers mein banate hain, jaise Session 11 ka marshal do towers ki buildings ko jodta tha. Ek aur baat: subnet ko public ya private naam uska nahi, uske direction board ka milta hai. Naam mein public likhne se kuch nahi hota. Ab dekhte hain wo direction board kya hai.

## Direction Boards: Route Table

Route table wo direction board hai jo har wing ke bahar lagta hai. Har row bolti hai: is address ki taraf jaana ho to is darwaze se jaao. Har VPC mein ek local row hoti hai, jo campus ke andar sab ko ek doosre tak pahunchne deti hai. 0.0.0.0/0 ka matlab "baaki sab kuch", yaani default raasta. Agar kai rows ek address se milti hon, to sabse specific wali jeetti hai, matlab sabse bada slash. Isliye 10.0.2.7 local row se jaayega, aur 8.8.8.8 default row se. Ek chhota jaal: console mein Main route table hoti hai jo har naye subnet ko by default mil jaati hai. Use badalne ke bajaye apni alag route table banao.

## Main Gate: Internet Gateway

Internet gateway, IGW, campus ka main gate hai. Wo VPC se attach hota hai, aur akela kuch nahi karta. Public wing wo hai jiske direction board mein 0.0.0.0/0 ka raasta IGW ki taraf jaata hai. Par ek aur cheez zaroori hai: building ke paas public IP hona chahiye. IGW building ke private address ko uske public address se ek-ek karke badalta hai, jo ek simple NAT hai. Bina public IP ke building gate tak aati hai par bahar nahi jaa paati. Aur public IPv4 address ka ab alag kharcha hai, jo live pricing page par hai. Isliye public wing mein sirf wahi cheezein rakho jinhe sach mein public hona hai: marshal aur gatehouse. Booking buildings aur database private wing mein.

## Lab: Campus Zero se

Lab. VPC banao, 10.0.0.0/16, naam atithi-vpc. Chaar subnets: do public, 10.0.1.0/24 aur 10.0.2.0/24, do alag towers mein, aur do private, 10.0.11.0/24 aur 10.0.12.0/24, wahi do towers. Internet gateway banao aur VPC se attach karo. Phir ek nayi route table public-rt banao, usme 0.0.0.0/0 ko IGW par point karo, aur use dono public subnets se jodo. Public subnets par auto-assign public IPv4 on karo. Ab public subnet mein ek chhoti building launch karo aur SSH karo: kaam karega. Private subnet mein ek building daalo, aur dekho ki wo internet tak nahi pahunch sakti. Ye abhi bilkul sahi hai, kyunki hum ne uske liye koi raasta banaya hi nahi.

## Recap aur Bridge

Recap: VPC, subnet, route table aur IGW. Ab sawaal: private wing ki buildings ko kabhi kabhi bahar bhi jaana hai, updates ke liye. Bina darwaza khole kaise?

---

# EPISODE 3: Dispatch Desk aur Do Tarah ke Guard

## Bahar Jaana Hai, Andar Aane Dena Nahi

Private wing ki booking building ko kabhi kabhi bahar jaana padta hai: security updates download karne, ya kisi payment API se baat karne. Par koi bahar wala andar nahi aana chahiye. Session 05B yaad hai? Hum ne ek Rocky building ko dispatch desk banaya tha: andar ki buildings ke saare khat us desk ke ek public address se jaate the, aur desk yaad rakhta tha ki kis khat ka jawab kisko dena hai. Ye wahi masquerade tha. Landlord ke paas iska ek taiyar, har waqt chalne wala desk hai, jise NAT gateway kehte hain.

## NAT Gateway

NAT gateway public wing mein rehta hai, aur uske paas ek Elastic IP hota hai, wahi permanent address jo Session 10 mein dekha tha. Private wing ke direction board mein 0.0.0.0/0 ko NAT gateway par point karte hain. Private building ka khat desk se guzarta hai, desk apna public address lagata hai, aur IGW se bahar jaata hai. Jawab wapas usi raaste aata hai. Bahar se koi naya connection khud shuru nahi kar sakta, kyunki desk ko pata hi nahi ki use kise bhejna hai. Wahi cheez Session 05B ke port forwarding se ulti hai: wahan humne jaan boojh kar ek darwaza andar khola tha. Yahan koi darwaza nahi khulta.

## Desk ka Kharcha aur Sasta Raasta

NAT gateway ghante ke hisaab se chalta hai, aur uske upar jitna data guzarta hai uska bhi kharcha hota hai. Isliye lab ke baad hata dena. Ek NAT gateway ek hi tower mein hota hai. Do towers mein high availability chahiye to har tower mein ek desk lagta hai, aur har private wing apne tower ke desk ki taraf jaata hai. Ek sasta raasta bhi hai: S3 aur DynamoDB ke liye gateway endpoint. Session 12 ka warehouse private wing se seedha ek pipe se mil jaata hai, desk ke bina, aur is pipe ka koi kharcha nahi. Atithi ki booking building rooms ki photos S3 se padhti hai, to ye pipe bahut paisa bachayegi.

## Do Tarah ke Guard: SG aur NACL

Ab do tarah ke guard. Door guard, yaani security group, building ke darwaze par khada hai. Wo yaad rakhta hai ki kisne bahar ka khat bheja, isliye jawab apne aap andar aane deta hai. Ise stateful kehte hain. Uski list mein sirf allow hote hain, aur jo likha nahi wo band hai. Wing guard, yaani NACL, poore wing ke darwaze par khada hai. Wo kuch yaad nahi rakhta, stateless hai. Isliye andar aur bahar ke rule alag alag likhne padte hain, khaaskar jawab wale ports, jo 1024 se 65535 ke beech hote hain. Isme allow bhi hote hain aur deny bhi, aur rules number ke kram mein check hote hain, sabse chhota number pehle. Default NACL sab kuch allow karta hai, aur nayi banayi hui NACL sab kuch deny karti hai.

## Kab Kaun Sa Guard

Roz ka zyadatar kaam door guard se chalta hai. Booking buildings ko database tak aane dena: database ke security group mein booking-sg ko source likho, jaise Session 13 mein. Kisi ek abusive IP range ko poore wing ke liye rokna ho: NACL mein ek deny rule, jiska number allow rule se chhota ho, jaise 90 aur allow 100, kyunki chhota number pehle check hota hai. NACL mein ek aam galti: andar ka rule likha, par jawab wale ports ke liye bahar ka rule bhool gaye. Tab connection aadha bana aur latak jaata hai. Isliye jab tak zaroorat na ho, NACL default par chhod do, aur security group ki zanjeer se kaam chalao.

## Lab: Private Building ko Bahar Ka Raasta

Lab. Public wing mein NAT gateway banao, ek nayi Elastic IP ke saath. Phir ek alag private-rt banao, usme 0.0.0.0/0 ko us NAT par point karo, aur use dono private subnets se jodo. Ab private building ke andar, jisse hum agle episode mein gatehouse ke raaste pahunchenge, curl -sI https://example.com chalao: jawab aayega. Ab ulta test: internet se us private building ke IP par SSH ya ping karne ki koshish karo. Wo kabhi pahunchega nahi, kyunki wahan koi public address hai hi nahi. Ek check aur: private-rt se NAT wali row hata do aur dekho ki curl latak jaata hai. Ye wahi "timeout" hai jo humne Session 13 mein dekha tha. Lab ke baad NAT gateway hatao aur Elastic IP release karo.

## Recap aur Bridge

Recap: NAT, endpoint, SG aur NACL. Ab sab ko jodkar ek poora campus banate hain, aur dekhte hain ki andar jaaye kaise.

---

# EPISODE 4: Poora Campus

## Ek Hi Gatehouse

Private building ka koi public address nahi. To admin uske andar jaaye kaise? Ek tareeka gatehouse hai, jise bastion host kehte hain: public wing mein ek chhoti, bahut surakshit building, jiske through staff andar ke buildings tak pahunchta hai. Ek hi darwaza, ek hi jagah jahan nigrani rakhi jaati hai, aur wahi jagah jahan har andar aane ki entry logbook mein likhi jaati hai. Ye wahi SSH key wali baat hai jo Session 4 mein humne sikhi thi: chaabi laptop par rahegi, gatehouse par copy nahi hogi.

## Gatehouse ke Rules aur ProxyJump

Gatehouse ke door guard ki list mein port 22 sirf aapke apne IP se. Private building ke door guard mein port 22 sirf bastion-sg se, kisi IP list se nahi. Ab ek hi command mein andar: ssh -i atithi.pem -J ubuntu@GATEHOUSE_PUBLIC_IP ubuntu@PRIVATE_IP. -J ka matlab hai ProxyJump: aapka laptop gatehouse ke through ek surakshit raasta kholta hai aur aapki chaabi kabhi gatehouse par nahi jaati. Ek jaal: -i atithi.pem sirf aakhri building ke liye lagta hai, gatehouse wale pehle hop ko bhi chaabi chahiye. Humne sirf -i aur -J chalaya to gatehouse par Permission denied mila. Do tareeke kaam kiye: ~/.ssh/config mein dono hosts par IdentityFile aur ProxyJump, ya pehle ssh-add atithi.pem. Isliye chaabi ki copy scp se gatehouse par daalna galat hai, aur ek aur khatarnak tareeka ssh -A agent forwarding hai, jise bhi bachana behtar hai. Gatehouse ko chhota rakho, usme kuch aur mat chalao, aur uska logbook dhyaan se dekho.

## Gatehouse ke Bina: Session Manager

Ek aur tareeka hai, jo aajkal aur behtar maana jaata hai: Systems Manager ka Session Manager. Isme gatehouse hi nahi, port 22 bhi nahi kholna padta. Staff landlord ki service se shell maangta hai, aur landlord uske badle private building ke andar ek surakshit raasta kholta hai. Iske liye teen cheezein chahiye. Ek, building par SSM agent, jo kai AMIs mein pehle se hota hai. Do, building par Session 9 ka ek duty badge, yaani role, jisme AmazonSSMManagedInstanceCore policy ho. Teen, building ko landlord ki SSM service tak pahunchne ka raasta: NAT desk ya VPC endpoints se. Isse har session ka logbook aur kaun andar gaya, ye sab landlord ke paas rehta hai. Hum gatehouse isliye sikha rahe hain ki bahut jagah aaj bhi wahi chalta hai.

## Skywalk: VPC Peering

Maan lo Atithi ek doosra campus banata hai, 10.1.0.0/16, analytics ke liye. Dono campuses ko seedha private raaste se jodna ho to skywalk lagta hai: VPC peering. Isme internet ka koi hissa nahi, aur dono ke number range alag hone chahiye, nahi to raasta kahan jaayega ye tay nahi hoga. Peering banane ke baad teen kaam: request accept karo, dono taraf ke direction boards mein doosre campus ke CIDR ki row jodo, aur dono taraf ke door guards mein doosri taraf ko allow karo. Ek hi kaam chhoot jaaye, to skywalk dikhta hai par kaam nahi karta. Aur peering transitive nahi: A se B aur B se C jude hon, to A se C apne aap nahi. Bahut saare campuses ho to Transit Gateway ek hub ki tarah kaam karta hai.

## "Time Out Ho Raha Hai": Khoj ka Kram

Jab kuch connect nahi hota, to Session 5 ka tarika yahan bhi chalta hai: ek ek kadi se raasta dekho. Pehle, kya destination par service sun rahi hai aur sahi port par? Phir destination ka door guard. Phir source ka door guard, jo aam taur par sab bahar jaane deta hai. Phir NACL, dono taraf. Phir dono taraf ke direction boards. Phir public IP aur IGW, ya private wing ke liye NAT. Aur peering ke liye dono taraf ki routes. Landlord do madadgaar bhi deta hai: Reachability Analyzer, jo bina packet bheje batata hai ki raasta kahan atakta hai, aur Flow Logs, jo har accept aur reject ka record rakhte hain. Isse "kahin kuch band hai" ka andaza nahi, jawab milta hai.

## Lab: Poora Campus

Lab. Public wing mein ek chhoti building launch karo, naam gatehouse, bastion-sg ke saath. Private wing mein ek building, app-sg ke saath. ssh -i atithi.pem -J ubuntu@GATEHOUSE_IP ubuntu@PRIVATE_IP se andar jaao, aur check karo ki wahan se curl -sI https://example.com NAT ke raaste chalta hai. Ab doosra VPC 10.1.0.0/16 banao, usme ek building daalo. Peering request banao aur accept karo. Dono direction boards mein doosre ka CIDR jodo, dono door guards mein ICMP allow karo, aur ek building se doosri ka private IP ping karo. Phir ek row hata kar dekho ki ping rukti hai ya nahi. Safai ka kram: peering, NAT gateway aur Elastic IP, buildings, subnets, IGW, aur aakhir mein VPCs.

## Recap aur Bridge

Recap: ek poora campus: wing, direction boards, main gate, dispatch desk, do guard, gatehouse aur skywalk. Ab sab kuch chal raha hai, par ek sawaal baaki hai: agar koi building raat ko dheemi hone lage, ya NAT desk par bill achanak badh jaaye, to pata kaise chalega? Agle session mein landlord ke meters, alarm aur chhote on-call freelancers: CloudWatch aur Lambda.
