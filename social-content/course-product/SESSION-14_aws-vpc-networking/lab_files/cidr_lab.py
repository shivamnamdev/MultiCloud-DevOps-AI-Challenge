import ipaddress

for c in ["10.0.0.0/16", "10.0.1.0/24", "10.0.2.0/25", "10.0.3.0/28", "192.168.1.0/30"]:
    n = ipaddress.ip_network(c)
    print(f"{c:16} addresses={n.num_addresses:6} first={n[0]} last={n[-1]}  AWS usable={max(n.num_addresses - 5, 0)}")

n = ipaddress.ip_network("10.0.2.0/25")
print(n.num_addresses, n[0], n[-1])
a = ipaddress.ip_network("10.0.1.0/24")
b = ipaddress.ip_network("10.0.1.128/25")
print(a.overlaps(b))
print(list(ipaddress.ip_network("10.0.0.0/16").subnets(new_prefix=24))[:3])

print("--- a CIDR whose start is not a multiple of its block size")
try:
    ipaddress.ip_network("10.0.1.64/24")
except ValueError as e:
    print("ValueError:", e)
print(ipaddress.ip_network("10.0.1.64/24", strict=False))

print("--- the Atithi plan")
vpc = ipaddress.ip_network("10.0.0.0/16")
plan = {"public A": "10.0.1.0/24", "public B": "10.0.2.0/24", "private A": "10.0.11.0/24", "private B": "10.0.12.0/24"}
nets = {k: ipaddress.ip_network(v) for k, v in plan.items()}
print("all inside the campus:", all(n.subnet_of(vpc) for n in nets.values()))
names = list(nets)
print("any two overlap:", any(nets[x].overlaps(nets[y]) for i, x in enumerate(names) for y in names[i + 1:]))
print("campus 10.0.0.0/16 overlaps 10.0.5.0/24 of another team:", vpc.overlaps(ipaddress.ip_network("10.0.5.0/24")))
print("campus overlaps default VPC 172.31.0.0/16:", vpc.overlaps(ipaddress.ip_network("172.31.0.0/16")))
