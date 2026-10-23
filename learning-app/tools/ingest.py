"""Ingest course Markdown into content/<unit>/unit.json. See architecture/ingest.md.

    python3 tools/ingest.py
"""
import json
import os
import re
import sys
from typing import List, Tuple

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(APP)

# terms that appear in many titles and say nothing about a question
STOP = {"terraform", "code", "covered", "language", "history", "setup", "installation",
        "with", "from", "and", "the", "instance", "commands", "via", "aws", "file",
        "essential", "windows", "user", "key"}
EXTRA_TERMS = {
    "cli-commands": ["init", "plan", "apply", "destroy", "validate"],
    "state-file-terraform-tfstate": ["state"],
}


class IngestError(Exception):
    pass


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def clean_title(raw: str) -> str:
    raw = re.sub(r"^[^\w`]+", "", raw.replace("`", "")).strip()
    return raw.rstrip(":").strip()


def clean_lines(lines: List[str]) -> List[str]:
    out = [l.replace("****", "").rstrip() for l in lines]
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    # a trailing horizontal rule is a section separator, not content
    while out and out[-1].strip() == "---":
        out.pop()
        while out and not out[-1].strip():
            out.pop()
    return out


def sections(lines: List[str], level: int) -> List[Tuple[str, List[str]]]:
    prefix = "#" * level + " "
    found = []
    fence = False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if not fence and ln.startswith(prefix):
            found.append((ln[len(prefix):].strip(), []))
        elif found:
            found[-1][1].append(ln)
    return found


def split_bullets(body: List[str]) -> List[List[str]]:
    items = []
    for ln in body:
        if re.match(r"- \*\*", ln.replace("****", "")):
            items.append([ln])
        elif items:
            items[-1].append(ln)
    return items


def parse_fw1(text: str, unit: str) -> Tuple[list, list]:
    lines = text.splitlines()
    concepts, questions = [], []

    def add_concept(title, body, kind):
        body = clean_lines(body)
        if body:
            concepts.append({"id": "%s-%s" % (unit, slug(title)), "unit": unit, "kind": kind,
                             "title": title, "text_md": "\n".join(body)})

    for raw_title, body in sections(lines, 2):
        title = clean_title(raw_title)
        if title == "Quick Revision Map":
            add_concept(title, body, "overview")
        elif title == "Essential Terraform Commands":
            add_concept(title, body, "overview")
        elif title == "Interview Preparation Strategy":
            add_concept(title, body, "method")
        elif title == "Core Concepts Covered":
            for sub_raw, sub_body in sections(body, 3):
                sub = clean_title(sub_raw)
                if sub == "Terraform Key Terminology":
                    for item in split_bullets(sub_body):
                        first = item[0].replace("****", "")
                        m = re.match(r"- \*\*(.+?)\*\*", first.replace("`", ""))
                        add_concept(clean_title(m.group(1)), item, "concept")
                else:
                    add_concept(sub, sub_body, "concept")
        elif title == "Hands-On Practicals":
            for sub_raw, sub_body in sections(body, 3):
                add_concept(clean_title(sub_raw), sub_body, "practical")
        else:
            m = re.match(r"(\d+)\.\s+(.*)", title)
            s = re.match(r"Scenario (\d+):\s+(.*)", title)
            joined = "\n".join(clean_lines(body))
            if m:
                a = re.search(r"\*\*Answer:\*\*\s*(.*)", joined, re.S)
                if not a:
                    raise IngestError("question %s has no answer" % title)
                questions.append({"id": "%s-q%02d" % (unit, int(m.group(1))), "unit": unit,
                                  "kind": "interview", "title": m.group(2).replace("`", ""),
                                  "prompt": m.group(2), "reference_answer": a.group(1).strip()})
            elif s:
                qa = re.search(r"\*\*Question:\*\*\s*(.*?)\s*\*\*Answer:\*\*\s*(.*)", joined, re.S)
                if not qa:
                    raise IngestError("scenario %s malformed" % title)
                questions.append({"id": "%s-s%02d" % (unit, int(s.group(1))), "unit": unit,
                                  "kind": "scenario", "title": s.group(2),
                                  "prompt": qa.group(1).strip(), "reference_answer": qa.group(2).strip()})
    return concepts, questions


def concept_terms(concept: dict) -> List[str]:
    key = concept["id"].split("-", 1)[1]
    if key in EXTRA_TERMS:
        return EXTRA_TERMS[key]
    words = re.findall(r"[a-z0-9]+", concept["title"].lower())
    return [w.rstrip("s") if len(w) > 4 else w for w in words if len(w) >= 3 and w not in STOP]


def link_questions(concepts: list, questions: list) -> None:
    linkable = [c for c in concepts if c["kind"] in ("concept", "practical") or c["id"].endswith("-cli-commands")]
    for q in questions:
        text = q["prompt"].lower()
        scored = []
        for c in linkable:
            hits = sum(1 for t in concept_terms(c) if re.search(r"\b" + re.escape(t), text))
            if hits:
                scored.append((hits, c["id"]))
        scored.sort(key=lambda x: (-x[0], x[1]))
        q["concept_ids"] = [cid for _, cid in scored[:3]]


def check_unique(items: list) -> None:
    seen = set()
    for it in items:
        if it["id"] in seen:
            raise IngestError("duplicate id %s" % it["id"])
        seen.add(it["id"])


UNITS = [
    {"id": "fw1", "title": "Free Workshop: Terraform & IaC", "subtitle": "Workshop of 22 Aug 2026",
     "source": "FREE Workshop's/22Aug2026.md", "parser": parse_fw1},
]


def build_unit(unit: dict, repo: str = REPO, app: str = APP) -> dict:
    src = os.path.join(repo, unit["source"])
    with open(src, encoding="utf-8") as f:
        concepts, questions = unit["parser"](f.read(), unit["id"])
    check_unique(concepts + questions)
    link_questions(concepts, questions)
    for c in concepts:
        rel = "content/%s/diagrams/%s.mmd" % (unit["id"], c["id"])
        has = os.path.exists(os.path.join(app, rel))
        c["diagram"] = {"type": "mermaid", "path": rel, "reviewed": False} if has else None
    return {"id": unit["id"], "title": unit["title"], "subtitle": unit.get("subtitle", ""),
            "source_file": unit["source"], "concepts": concepts, "questions": questions}


def main() -> int:
    for unit in UNITS:
        data = build_unit(unit)
        out_dir = os.path.join(APP, "content", unit["id"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "unit.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        withd = sum(1 for c in data["concepts"] if c["diagram"])
        print("%s: %d concepts (%d with diagrams), %d questions" %
              (unit["id"], len(data["concepts"]), withd, len(data["questions"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
