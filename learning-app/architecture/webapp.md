# SOP: Web app (local)

## Goal
A local study UI: browse units, read each concept as text beside its Mermaid diagram, practise questions, track progress. Works with no internet except the Mermaid CDN script (diagram source is shown as fallback) and no Ollama.

## Stack
- Backend: Python stdlib `http.server` (`tools/server.py`), JSON API, binds to 127.0.0.1 only.
- Storage: SQLite `data/progress.sqlite` (gitignored): `progress(item_id PRIMARY KEY, status, updated_at)`.
- Frontend: `web/index.html`, `web/app.js`, `web/style.css`. No framework, no build step. Text is HTML-escaped before formatting. Mermaid loaded from jsDelivr, pinned major 11, `securityLevel: 'strict'`.

## API
- `GET /api/units` -> units with item counts and progress counts.
- `GET /api/units/<id>` -> unit JSON with diagram source inlined.
- `GET /api/progress` -> `{item_id: status}`.
- `POST /api/progress` `{item_id, status}` -> validates the item exists and the status is allowed.

## Statuses
- Concepts: `not_started | read | lab_done | mastered`.
- Questions: `not_started | known | review`.

## Not built yet (later steps)
Quizzes (MCQ + SM-2 review), Ollama mock interview + scoring, settings page.

## Learnings
(append when something fails)
