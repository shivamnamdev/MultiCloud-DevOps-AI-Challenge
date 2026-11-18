import platform
import shutil

total, used, free = shutil.disk_usage("/")
pct = used / total * 100
print(f"Building: {platform.node()}  OS: {platform.system()}")
print(f"Disk used: {pct:.1f}%")
if pct > 90:
    raise SystemExit("FAIL: disk almost full")
