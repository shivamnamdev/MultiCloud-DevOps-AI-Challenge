# SOP: Ingest (Markdown -> unit JSON)

## Goal
Turn one course source file into `content/<unit>/unit.json` (concepts + questions). Deterministic, no LLM. Source files are never modified.

## Inputs
- A unit definition in `tools/ingest.py` (`UNITS`): id, title, source path, parser.
- Optional diagrams at `content/<unit>/diagrams/<concept-id>.mmd` (hand/Claude-authored, generated once; ingest only attaches them).

## Parser for unit `fw1` (FREE Workshop, Terraform)
Include as concepts:
- `## Quick Revision Map`, `## Essential Terraform Commands` (incl. `### Typical Workflow`), `## Interview Preparation Strategy`.
- Every `###` under `## Core Concepts Covered` (kind `concept`). The `Terraform Key Terminology` section is split into one concept per top-level `- **Term**` bullet.
- Every `###` under `## Hands-On Practicals` (kind `practical`).
Include as questions:
- `## N. Title` + `**Answer:**` (kind `interview`)
- `## Scenario N: Title` + `**Question:**` / `**Answer:**` (kind `scenario`)
Exclude: badges, logistics, participants, roadmap, pricing, Q&A chatter, action items, "Interview Questions Highlighted" (no answers), practice challenge.

## Rules
- Headings inside code fences are ignored.
- Clean artefacts: `****` bold-marker leftovers, trailing spaces.
- Concept id = `<unit>-<slug(title)>` (stable under reordering); question ids `<unit>-q01`, `<unit>-s01`.
- `concept_ids` on a question = up to 3 concepts whose title terms appear in the question prompt (not the answer). Overview/method concepts are never linked.
- IDs must be unique; fail loudly otherwise.

## Edge cases / learnings
(append when something fails)
- Link terms must match on word boundaries ("source" matched "resource"). Found in test_word_boundary_linking.
