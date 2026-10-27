# gemini.md — Project Constitution (law)

Status: **Schemas approved 2026-10-23. Link phase done (Ollama handshake pending a real run on the user's machine).**

## North Star
A personal, self-study app built from this repo's course notes. Each concept is shown as the original text plus a diagram, with progress tracking, quizzes, and mock interviews run by a local Ollama LLM.

## Architectural invariants
- Source of truth: the Markdown files in the repo root (`Session-NN-*/`). Never modify them.
- Diagrams are generated ONCE (offline, by Claude in-session), stored as files, and reviewed. The app never generates diagrams at runtime.
- Original text is always shown next to its diagram.
- Ollama is used only at runtime for: mock interviews, answer grading, optional quiz variations. It is optional; the app must work without it.
- A.N.T. layers: `architecture/` (SOPs) -> navigation -> `tools/` (deterministic Python). Update the SOP before the code.
- Work one session at a time.
- Intermediates go in `.tmp/`; secrets in `.env`.

## Behavioral rules
- Ignore templated filler (`Scenarios.md`, most of `Interview-QnA.md` answers) as a source of facts. Use dated class notes and project files as primary content.
- Questions in the interview bank come from the repo's `Interview-QnA.md`; the interviewer must ground its follow-ups and grading in the class notes, and say so when it is unsure.
- Interviewer settings are user toggles: tone `strict | friendly`, hints `on | off`. Always ask 2–3 follow-up questions per interview question.
- Always score the answer out of 10, grounded in the class notes. If the score is below 7, give concrete "what to study next" suggestions that point to specific concepts/sessions.
- Scoring is hybrid: a deterministic concept-coverage check (code) sets the base score; the LLM writes feedback and adjusts within a bounded range. Small local models must not be the sole judge.
- Models: users run Ollama locally. Defaults `llama3.2:latest` (interviewer/grader) and `codellama:latest` (command/code questions). Model names are configurable. The app must work when Ollama is absent (study, diagrams, MCQ quizzes still work).
- Each user runs the app locally with their own local progress store (SQLite). No accounts, no cloud.
- Build order: FREE Workshop's (Terraform) first, then Session-00, then course order. (2026-10-26: all sessions ingested by the generic parser; diagrams only exist for fw1 so far.)
- Diagram format: Mermaid (`.mmd`) text files, produced using the submodule skills `mermaid-expert` and `diagram-generator` as references, and human-reviewed before marked `reviewed: true`.
- Content from `agentic-awesome-skills/` is third-party: read for reference only, never execute its scripts without approval.

## Data schemas (DRAFT, pending approval)

### Concept (output of ingest + diagram step)
```json
{
  "id": "fw1-provider",
  "unit": "fw1",
  "kind": "concept | practical | overview | method",
  "title": "Provider",
  "text_md": "original text excerpt, verbatim (artefacts cleaned)",
  "diagram": { "type": "mermaid", "path": "content/fw1/diagrams/fw1-provider.mmd", "reviewed": false }
}
```

### Unit (content/<unit-id>/unit.json) — added 2026-10-26
```json
{
  "id": "s30", "title": "...", "subtitle": "Session 30 · Docker Introduction · Batch-44",
  "session": 30, "module": "M5 Docker, Kubernetes, Monitoring", "order": 3000,
  "status": "ready | partial | sparse | light",
  "source_file": "path relative to repo root",
  "needs_authoring": [{"section": "...", "chars": 5439}],
  "unparsed_qa": [{"section": "...", "chars": 1500}],
  "unanswered_questions": ["Q1: ..."],
  "concepts": [], "questions": []
}
```
Unit ids: `fw1` (workshop), `sNN` / `sNNa`.. (sessions), `extra-kafka`. `light` units come from READMEs; they have no diagrams or questions. `DATA_TODO.md` is generated from these fields.

### Question (from Interview-QnA.md or generated quiz)
```json
{
  "id": "fw1-q08",
  "unit": "fw1",
  "kind": "interview | scenario | mcq",
  "title": "What is Terraform State?",
  "prompt": "question text",
  "reference_answer": "answer text from the source",
  "concept_ids": ["fw1-state-file-terraform-tfstate"],
  "choices": ["..."],
  "answer_index": 0
}
```

### Progress (local, one record per user action)
```json
{
  "item_id": "fw1-provider  (concept or question id)",
  "status": "concepts: not_started | read | lab_done | mastered; questions: not_started | known | review",
  "updated_at": "ISO-8601"
}
```

### InterviewTurn (Ollama session log)
```json
{
  "session_id": "uuid",
  "question_id": "S30-Q01",
  "user_answer": "...",
  "llm_feedback": "...",
  "settings": { "tone": "strict | friendly", "hints": true },
  "followups": [{ "q": "...", "a": "...", "feedback": "..." }],
  "coverage": { "expected_concepts": ["S30-C01"], "hit": ["S30-C01"] },
  "score": 0,
  "score_max": 10,
  "study_suggestions": ["concept_id or session to review"],
  "model": "ollama model tag"
}
```

### Settings (local, per user)
```json
{
  "ollama_url": "http://localhost:11434",
  "interviewer_model": "llama3.2:latest",
  "code_model": "codellama:latest",
  "tone": "friendly",
  "hints": true,
  "followups": 3
}
```

## Maintenance log
- 2026-10-23: Protocol 0 initialised.
- 2026-10-23: Discovery answers recorded (models, interviewer toggles, scoring /10, build order, Mermaid, submodule skills).
- 2026-10-23: Web app architecture added (architecture/webapp.md); schema ids switched to slug ids with a unit field.
- 2026-10-26: Unit record schema added; all sessions ingested (74 units).
- 2026-10-26: Phase 1 added tables `notes(item_id, text, updated_at)` and `bookmarks(item_id, created_at)` to data/progress.sqlite; unit titles now `<session topic> · Day N`.
