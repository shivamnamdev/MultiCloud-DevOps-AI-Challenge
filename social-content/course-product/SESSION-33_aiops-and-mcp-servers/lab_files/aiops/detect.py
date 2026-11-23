import requests, statistics as st


def series(prom, query, start, end, step=60):
    r = requests.get(f"{prom}/api/v1/query_range", timeout=10,
                     params={"query": query, "start": start, "end": end, "step": step})
    r.raise_for_status()
    result = r.json()["data"]["result"]
    return {tuple(sorted(s["metric"].items())): [float(v) for _, v in s["values"]] for s in result}


def anomalies(values, window=30, z=3.0, need=3):
    run, hits = 0, []
    for i in range(window, len(values)):
        w = values[i - window:i]
        mu, sd = st.mean(w), st.pstdev(w)
        if sd < 1e-9:
            run = 0
            continue
        run = run + 1 if abs(values[i] - mu) / sd > z else 0
        if run >= need:
            hits.append((i, values[i]))
    return hits
