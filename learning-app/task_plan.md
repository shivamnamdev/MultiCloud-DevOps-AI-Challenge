# task_plan.md

## Phase 0 — Initialization
- [x] Create task_plan.md, findings.md, progress.md, gemini.md
- [x] Discovery questions answered (see below)
- [x] Data schema approved in gemini.md (user: "Let's begin", 2026-10-23)
- [x] Blueprint approved

## Discovery (B.L.A.S.T. — 5 questions) — all answered
1. North Star: text + diagram learning app with progress tracking, quizzes, Ollama mock interviews.
2. Integrations: Ollama only (llama3.2:latest, codellama:latest). No keys. Not installed on this machine; user tests on another machine.
3. Source of truth: repo Markdown (class notes + projects primary; Interview-QnA for question bank).
4. Delivery: local web app (Python backend + browser UI), SQLite progress, run script instead of cloud Trigger.
5. Behavioral rules: see gemini.md (strict/friendly toggle, hints toggle, 2–3 follow-ups, score /10 with study suggestions).

## Build order (content)
1. `FREE Workshop's/22Aug2026.md` (Terraform interview workshop) — pilot
2. `Session-00-Program-Kickoff` (mostly roadmap/logistics; light diagrams only)
3. Then Session-01 onward, one session at a time.

## Blueprint (approved 2026-10-23; research done, see findings.md)
- B Blueprint: approve schemas + this plan.
- L Link: `tools/ollama_handshake.py` that lists models and sends one prompt. Cannot run here (no Ollama); user runs it on the other machine. Local tests use a fake client.
- A Architect (per session, repeated):
  1. SOP in architecture/ — ingest, diagram, quiz, interview, scoring.
  2. `tools/ingest.py`: Markdown -> Concept JSON (deterministic).
  3. Diagrams: Claude generates `.mmd` per concept using mermaid-expert/diagram-generator guidance; user reviews.
  4. Quiz bank: MCQs + interview questions from Interview-QnA question lists and class notes.
  5. `tools/score.py`: deterministic concept-coverage scoring; Ollama only for feedback.
  6. Progress store (SQLite) + API.
- S Stylize: UI with text and diagram side by side, progress bars, settings toggles.
- T Trigger: `run.sh`/`run.bat` local start, README with Ollama setup (`ollama pull llama3.2`, `ollama pull codellama`).

## Open items
- mermaid-cli (`mmdc`) is not installed; diagrams can render client-side in the browser, mmdc only needed for offline syntax validation (requires npm install — needs user approval).

## Blueprint additions from research
- Add optional `format` (JSON schema) to `OllamaClient.generate`; every LLM reply is parsed and validated, with a safe fallback if invalid.
- Mermaid rendered client-side with `securityLevel: 'strict'`, major version pinned (11).
- Spaced repetition for quiz review uses SM-2 (deterministic, in code).
- Next action: Architect step 1 for the Free Workshop — SOP `architecture/ingest.md`, then `tools/ingest.py`.

## Status 2026-10-23
- [x] L Link (Ollama client + handshake; real handshake still to run on user's machine)
- [x] A Architect step 1: ingest + web app for unit fw1 (Learn + Practice, progress tracking)
- [ ] A Architect step 2: MCQ quizzes + SM-2 review
- [ ] A Architect step 3: Ollama mock interview (settings toggles, hybrid /10 scoring, 3 follow-ups, study suggestions) — add `format` to OllamaClient.generate
- [ ] Review/fix diagrams after user checks them in the browser
- [ ] Next unit: Session-00-Program-Kickoff
