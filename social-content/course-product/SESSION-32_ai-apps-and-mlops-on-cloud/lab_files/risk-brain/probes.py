import numpy as np, subprocess, sys, re
src = open("train.py").read()
# 1. accuracy of a brain that always says "no cancel"
rng = np.random.default_rng(42); n = 4000
X = np.column_stack([rng.integers(0,120,n), rng.normal(5000,1500,n), rng.integers(0,2,n), rng.integers(0,4,n)])
y = ((X[:,0] > 60) & (X[:,2] == 0) & (rng.random(n) < 0.7)).astype(int)
print("cancel share in data:", round(y.mean(), 3), "| accuracy of 'always no cancel':", round(1 - y.mean(), 3))
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
m = RandomForestClassifier(n_estimators=100, random_state=42).fit(Xtr, ytr)
print("real brain accuracy:", round(accuracy_score(yte, m.predict(Xte)), 3))
# 2. a broken brain: labels shuffled -> the gate must stop the station
broken = src.replace("y = ((X", "y = np.random.default_rng(1).permutation(((X").replace(").astype(int)", ").astype(int))", 1)
open("/tmp/train_broken.py", "w").write(broken)
r = subprocess.run([sys.executable, "/tmp/train_broken.py"], capture_output=True, text=True, cwd="/tmp")
print("broken brain: exit code", r.returncode, "|", (r.stdout.strip() or "") , "|", r.stderr.strip().splitlines()[-1])
# 3. seeds removed
nos = src.replace("default_rng(42)", "default_rng()").replace("random_state=42", "random_state=None")
open("/tmp/train_noseed.py", "w").write(nos)
for i in range(3):
    r = subprocess.run([sys.executable, "/tmp/train_noseed.py"], capture_output=True, text=True, cwd="/tmp"); print("no seed run", i + 1, r.stdout.strip())
for i in range(2):
    r = subprocess.run([sys.executable, "train.py"], capture_output=True, text=True, cwd="/tmp" if False else "."); print("seeded run", i + 1, r.stdout.strip())
