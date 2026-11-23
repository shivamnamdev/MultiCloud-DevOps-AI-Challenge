import json, joblib
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from prometheus_client import Counter, Gauge, make_asgi_app

FEATURES = ["lead_days", "price", "repeat_guest", "season"]

app = FastAPI()
app.mount("/metrics", make_asgi_app())

READY = False
model = joblib.load("risk.joblib")          # load ONCE at startup, only a file our own conveyor made
meta = json.load(open("risk.json"))
READY = True

BRAIN = meta["version"]
PRED = Counter("risk_predictions_total", "Predictions served", ["brain"])
MEAN = Gauge("risk_feature_mean", "Running mean of each input feature", ["brain", "feature"])
TRAIN_MEAN = Gauge("risk_feature_train_mean", "Mean of the feature in the training data", ["brain", "feature"])
TRAIN_STD = Gauge("risk_feature_train_std", "Std deviation of the feature in the training data", ["brain", "feature"])
for name, m, sd in zip(FEATURES, meta["train_means"], meta["train_stds"]):
    TRAIN_MEAN.labels(BRAIN, name).set(m)
    TRAIN_STD.labels(BRAIN, name).set(sd)

_n = 0
_sum = [0.0] * len(FEATURES)


class Booking(BaseModel):
    values: list[float] = Field(min_length=4, max_length=4)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response):
    if not READY:
        response.status_code = 503
    return {"ready": READY}


@app.post("/predict")
def predict(b: Booking):
    global _n
    p = float(model.predict_proba([b.values])[0][1])
    _n += 1
    PRED.labels(BRAIN).inc()
    for i, name in enumerate(FEATURES):
        _sum[i] += b.values[i]
        MEAN.labels(BRAIN, name).set(_sum[i] / _n)
    return {"cancel_risk": round(p, 3), "brain": BRAIN}
