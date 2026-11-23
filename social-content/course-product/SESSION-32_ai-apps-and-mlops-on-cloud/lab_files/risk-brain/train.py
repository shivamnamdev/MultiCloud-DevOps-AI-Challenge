import json, os, hashlib, joblib, numpy as np, sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
n = 4000
X = np.column_stack([
    rng.integers(0, 120, n),        # lead_days
    rng.normal(5000, 1500, n),      # price
    rng.integers(0, 2, n),          # repeat_guest
    rng.integers(0, 4, n),          # season
])
y = ((X[:, 0] > 60) & (X[:, 2] == 0) & (rng.random(n) < 0.7)).astype(int)

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=100, random_state=int(os.getenv("SEED", "42"))).fit(Xtr, ytr)
pred = model.predict(Xte)
p, r = precision_score(yte, pred), recall_score(yte, pred)
joblib.dump(model, "risk.joblib")
json.dump({"version": os.getenv("BRAIN_VERSION", "v1"), "precision": p, "recall": r, "sklearn": sklearn.__version__,
           "data_hash": hashlib.sha256(X.tobytes()).hexdigest()[:12],
           "train_means": X.mean(axis=0).tolist(),
           "train_stds": X.std(axis=0).tolist()}, open("risk.json", "w"))
print("precision", p, "recall", r)
assert r >= 0.6 and p >= 0.6, "brain below the quality gate"
