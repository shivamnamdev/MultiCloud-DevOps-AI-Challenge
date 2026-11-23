# Answer key for alerts_sample.csv (one defensible reading; yours may differ in details)

**Dependency map used:** frontend -> load-balancer -> bookings-service and rooms-service -> records-office-db; bookings-service -> payments-queue.

| Group | Alerts (ids) | Why they belong together |
|---|---|---|
| **A. The incident** | 2, 3, 16, 5, 4, 10, 15, 11, 6, 18, 7, 12, 9, 8, 14, 17, 19, 20 | They start at the records office (02:58) and travel **up** the dependency map in time order: db connections and latency, then the services that read it, then the queue, then the frontend. |
| **B. Old noise** | 1, 13 | Disk alerts that have been firing for **5 and 9 days**: older than the incident, different services, nothing changed at 03:00. Keep them on the list, but not in this incident. |
| **C. Repeats** | 19, 20 | Same alert as 9 and 4 firing again. Collapse, do not count. |

**First alert of the incident:** id **2** (ConnectionsHigh on the records office at 02:58). Id 1 is older but is old noise (group B).

**Likely root cause (a hypothesis, not a fact):** the records-office database ran out of connections or got slow, so every service that waits on it slowed down, timed out and failed its readiness checks. **Evidence to fetch next:** connection count and slow queries on the db around 02:58, what changed at about 02:55 (a deploy? a batch job?), whether the 5-day-old disk alert is related to growth.

**Out of 20 alerts the manager should see ONE incident** with: first alert, the chain, two noise items, three checks to run.

**Runbook lines you should look for in Session 26's runbook:** database connections and slow queries; a service whose readiness fails (do not restart it blindly, it will fail again while the db is slow); queue lag follows its consumers; the frontend errors are a symptom, not a cause.

**The trap to notice:** pods are restarting (ids 10, 18). A restart helper could "fix" this and make it worse, because the cause is the database. That is why the ladder keeps restart at "suggest with evidence" first.
