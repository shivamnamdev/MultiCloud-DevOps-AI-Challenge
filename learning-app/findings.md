# findings.md

## Source repo
- 248 Markdown files, ~5.3 MB, no code or images. Sessions S00–S59.
- High value: dated class notes (`🚀 Day-N ... Batch-NN.md`, ~65 files) and project notes S50–S57.
- Low value: `Scenarios.md` (same 10 scenarios per session, topic name swapped, placeholder code); `Interview-QnA.md` answers are generic template text, but the question lists are usable as an interview bank.
- File names contain spaces, emoji, `|` — quote paths.
- Notes are AI summaries of live classes; may contain errors; verify against official docs.
- Course material is paid content: keep the app private/personal.

## Pilot content
- `FREE Workshop's/22Aug2026.md` (~35 KB): Terraform + IaC interview workshop. Sections: IaC, Terraform vs Ansible, terminology, state, CLI workflow, AWS EC2 practical, 25+ interview Qs, 25+ scenarios, roadmap. Marketing/pricing at the end — exclude. Strong diagram candidates: Terraform workflow (init/plan/apply), state/backend, provider/resource dependency graph, Terraform vs Ansible.
- `Session-00-Program-Kickoff/README.md` (~27 KB): mostly motivation, tasks, roadmap, salary map, LinkedIn templates. Little technical content; only the roadmap suits a diagram.

## Submodule `agentic-awesome-skills/` (third-party, ~2650 skills)
- Relevant: `mermaid-expert` (short prompt-style skill), `diagram-generator` (Mermaid default, has `scripts/render_diagram.py` + `references/diagram-patterns.md`), `learn` (adaptive tutoring), `tutorial-engineer`, `ollama-stack` (docs-only setup guidance).
- Use as reference only.

## Environment (this machine)
- Present: node v24, python3. Missing: ollama, mmdc (mermaid-cli).

## Model notes
- llama3.2 (small) and codellama are weak judges; hence the hybrid deterministic scoring rule. codellama suits command/code questions only.

## Constraints
- Diagrams generated once, offline. Ollama only at runtime.

## Research (Blueprint step, 2026-10-23; from web search summaries, not code-reviewed)
- Ollama structured output: `format` parameter on `/api/generate` and `/api/chat` accepts a JSON schema (Ollama >= 0.3.0) and constrains output; `"json"` is looser. Still parse + validate, never trust. -> `ollama_client.generate` needs an optional `format` argument (Architect phase). Docs: https://registry.ollama.ai/blog/structured-outputs
- Mermaid in browser: `securityLevel: 'strict'` recommended for untrusted text; use `mermaid.run()` (`mermaid.init` deprecated). CDN ESM `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`. Exact current version not confirmed — pin the major (11) or vendor the file. Docs: https://mermaid.js.org/config/usage
- No single open-source project found that combines Markdown notes + Mermaid + SRS quizzes + Ollama interviews. Closest, for ideas only (not verified): odosui/mt (notes + Mermaid + spaced repetition), gamosoft/notediscovery (Markdown + Mermaid + Ollama compose), Memoet (self-hosted SM-2 SRS), Interview Prep Buddy (local Ollama question generation, AI + rule-based scoring — matches our hybrid scoring idea).
- Conclusion: build our own small app; reuse ideas, not code. SM-2 is the standard spaced-repetition algorithm and is simple to implement deterministically.

## Corpus structure (2026-10-26)
- 63 class-note files, 878 distinct `##` headings: structure varies. Content lives at `##` or `###` depending on file; some use a noise `##` ("Key Outcomes") as a wrapper around real `###` content; Q&A heading formats vary (`## N. ...?`, `### N. ...`, `### ❓ Qn:`, `### 📌 N. Scenario:`, `### 📌 Scenario N`) and answer markers vary (`**Answer:**`, `**💡 Answer:**`).
- Many notes contain real Q&A with answers; Interview-QnA.md (templated) is not needed for those.
- Some notes list scenario questions without answers (s23, s25): need answers written from the notes.
- Raw transcript-style notes with one heading (s27 "Part 1") cannot be split by rules.
- Sessions with only templated READMEs (light units): s00, s14, s40, s45, s46, s48, s49, s51, s58.
