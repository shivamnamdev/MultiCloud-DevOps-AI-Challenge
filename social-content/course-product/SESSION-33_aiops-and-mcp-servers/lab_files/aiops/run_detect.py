import time
from detect import series, anomalies
q = 'sum(rate(http_requests_total{status="500"}[10s]))'
end = time.time(); start = end - 150
for key, vals in series("http://det-prom:9090", q, start, end, step=2).items():
    h = anomalies(vals, window=30)
    print(f"{len(vals)} points; mean of first 100 = {sum(vals[:100])/100:.2f}; last values {[round(v,2) for v in vals[-4:]]}; first hit index = {h[0][0] if h else None} of {len(vals)}; hits={len(h)}")
