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
- Build order: FREE Workshop's (Terraform) first, then Session-00, then course order.
- Diagram format: Mermaid (`.mmd`) text files, produced using the submodule skills `mermaid-expert` and `diagram-generator` as references, and human-reviewed before marked `reviewed: true`.
- Content from `agentic-awesome-skills/` is third-party: read for reference only, never execute its scripts without approval.

## Data schemas (DRAFT, pending approval)

### Concept (output of ingest + diagram step)
```json
{
  "id": "S30-C03",
  "session": 30,
  "source_file": "Session-30-Docker-Introduction/🚀 Day-1 of Docker Batch-44 | 3rd Aug 2026.md",
  "title": "Docker Architecture",
  "text_md": "original text excerpt, verbatim",
  "diagram": { "type": "mermaid", "path": "content/S30/S30-C03.mmd", "reviewed": false },
  "labs": ["docker run hello-world"]
}
```

### Question (from Interview-QnA.md or generated quiz)
```json
{
  "id": "S30-Q01",
  "session": 30,
  "kind": "interview | mcq",
  "prompt": "Explain VM vs Docker.",
  "reference_answer_concept_ids": ["S30-C01"],
  "choices": ["..."],
  "answer_index": 0
}
```

### Progress (local, one record per user action)
```json
{
  "concept_id": "S30-C03",
  "status": "not_started | read | lab_done | mastered",
  "quiz_scores": [0.8],
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
