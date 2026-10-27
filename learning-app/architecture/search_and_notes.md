# SOP: Search, notes, bookmarks, cheat sheet (Phase 1)

## Goal
Find anything across all units fast, keep personal notes and bookmarks per concept/question, and print a one-column cheat sheet per unit.

## Search (`tools/search.py`)
- In-memory SQLite FTS5 index built by the server from `content/*/unit.json`; rebuilt automatically when any `unit.json` changes (same mtime signature the server already uses for `item_kinds`). Deviation from the plan: built at server start, not by ingest, so there is no extra artifact to keep in sync.
- One row per concept (title, text_md) and per question (title + prompt, reference answer). Columns `item_id`, `unit_id`, `unit_title`, `kind` are stored unindexed.
- User text is never passed to FTS5 as syntax. Query = every `\w+` token as a quoted prefix term, ANDed: `"tf"* "state"*`. Empty/no tokens -> no results. Limit 1..50 (default 25).
- Ranking: `bm25`, title weighted above body. Snippet uses `[[` `]]` markers; the UI HTML-escapes first and then turns the markers into `<mark>`.
- If FTS5 is unavailable the module falls back to a case-insensitive substring scan (same result shape).

## Notes and bookmarks (server `Store`)
- Tables in the existing progress DB: `notes(item_id PK, text, updated_at)` and `bookmarks(item_id PK, created_at)`.
- `item_id` must exist in the content; note text max 5000 chars; empty note text deletes the note.
- API: `GET /api/search?q=&limit=`, `GET/POST /api/notes`, `GET/POST /api/bookmarks` (`{item_id, on}`), `GET /api/mine` (items with a note or bookmark, with unit/title for linking).

## Cheat sheet
- Client route `#/u/<id>/print` renders the unit's concepts in a single printable column (diagrams included, own notes included). Print with the browser (`Cmd/Ctrl+P`); `@media print` hides navigation. Deviation from plan: client route instead of `GET /print/<unit>`, so the Markdown renderer is not duplicated server-side.

## Edge cases / learnings
(append when something fails)
