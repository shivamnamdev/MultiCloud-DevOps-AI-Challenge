"""Ingest course Markdown into content/<unit>/unit.json. See architecture/ingest.md.

    python3 tools/ingest.py
"""
import json
import os
import re
import sys
from typing import List, Optional, Tuple

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
    out = [re.sub(r"filecite[\w-]*", "", re.sub("[\ue000-\uf8ff]", "", l)).replace("****", "").rstrip() for l in lines]
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


# ---------------------------------------------------------------- generic parser
SKIP_NAMES = {"README.md", "Interview-QnA.md", "Scenarios.md"}
NOISE_RE = re.compile(
    r"^(key outcomes|action items|next steps|pending|open questions|table of contents|navigation|"
    r"decisions?\b|key decisions|prerequisites|student q|q&a highlights|questions? (&|and) answers? highlights|"
    r"session logistics|interview tips?|participants?|logistics|every wednesday|batch-\d+|session overview|"
    r"summary of session)", re.I)
QA_CONTAINER_RE = re.compile(r"question|scenario|q&a", re.I)
STRICT_QA_RE = re.compile(r"(interview|practice|technical)\s+questions?|q&a|questions?\s+(and|&)\s+answers?", re.I)
Q_RE = re.compile(r"^(?:Q\s*)?(\d+)\s*[.:)\-–]\s*(.+)$", re.I)
SC_RE = re.compile(r"^(?:\d+\s*[.)]\s*)?Scenario\s*(?:(\d+)\s*[:.\-\u2013]?|[:\-\u2013])\s*(.*)$", re.I)
PRACTICAL_RE = re.compile(r"step|hands-on|practical|walkthrough|setup|install|demo|\blab\b|build|deploy|configur|create|launch", re.I)
OVERVIEW_RE = re.compile(r"overview|agenda|introduction|summary|takeaway", re.I)
FLAT_MIN_CHARS = 2500

MODULES = [(0, 4, "M1 Foundation: DevOps, Cloud, AI"), (5, 9, "M2 Linux + GCP"), (10, 21, "M3 AWS"),
           (22, 29, "M4 CI/CD: Git, GitHub, Jenkins"), (30, 37, "M5 Docker, Kubernetes, Monitoring"),
           (38, 44, "M6 IaC + Automation"), (45, 46, "M7 Career"), (47, 49, "M8 Azure + AI"),
           (50, 57, "M9 Live projects"), (58, 58, "M10 Graduation"), (60, 99, "Extras")]


def module_for(n: int) -> str:
    if n == 59:
        return "M9 Live projects"
    for lo, hi, name in MODULES:
        if lo <= n <= hi:
            return name
    return "Other"


def top_sections(lines: List[str]) -> List[list]:
    out, fence = [], False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"(#{1,2}) (.*)", ln)
        if m:
            out.append([len(m.group(1)), m.group(2).strip(), []])
        elif out:
            out[-1][2].append(ln)
    return out


def strip_number(title: str) -> str:
    return re.sub(r"^\d+(\.\d+)*[.):]?\s+", "", title).strip() or title


def is_flat(body: List[str]) -> bool:
    text = "\n".join(body)
    if len(text) < FLAT_MIN_CHARS:
        return False
    lines = [l for l in body if l.strip()]
    bullets = sum(1 for l in lines if re.match(r"\s*[-*]\s", l))
    return bullets >= 0.6 * len(lines)


def question_like(title: str) -> bool:
    t = clean_title(title)
    low = t.lower()
    if not (SC_RE.match(t) or Q_RE.match(t)):
        return False
    return bool(t.rstrip(' "”\'').endswith("?") or re.match(r"Q\s*\d", t, re.I) or "scenario" in low)


ANS = r"\*\*\W*Answer:?\W*\*\*:?"
QUE = r"\*\*\W*Question:?\W*\*\*:?"


def question_from(title: str, body: List[str], container: str = "") -> Optional[dict]:
    t = clean_title(title)
    sc = SC_RE.match(t)
    qm = Q_RE.match(t)
    if not (sc or qm):
        return None
    text = "\n".join(clean_lines(body))
    m = sc or qm
    prompt_title = (m.group(2).strip() if m.lastindex and m.lastindex >= 2 else "") or "Scenario %s" % (m.group(1) or "")
    qa = re.search(QUE + r"\s*(.*?)\s*" + ANS + r"\s*(.*)", text, re.S)
    if qa:
        prompt, answer = qa.group(1).strip(), qa.group(2).strip()
    else:
        a = re.search(ANS + r"\s*(.*)", text, re.S)
        if not a and prompt_title.startswith("Scenario ") and len(prompt_title) < 14:
            return None  # bare "Scenario N" heading whose body is only the question
        prompt, answer = prompt_title, (a.group(1) if a else text).strip()
    if not answer:
        return None
    is_sc = bool(sc) or "scenario" in t.lower()[:40] or "scenario" in container.lower()
    return {"kind": "scenario" if is_sc else "interview", "title": prompt_title.replace("`", ""),
            "prompt": prompt, "reference_answer": answer}


def parse_generic(text: str, unit: str) -> dict:
    lines = text.splitlines()
    secs = top_sections(lines)
    concepts, questions, flat, unparsed, unanswered = [], [], [], [], []
    used = set()
    counters = {"interview": 0, "scenario": 0}

    def add_q(q):
        counters[q["kind"]] += 1
        q.update({"id": "%s-%s%02d" % (unit, "q" if q["kind"] == "interview" else "s", counters[q["kind"]]), "unit": unit})
        questions.append(q)

    def add_c(title, body, kind):
        body = clean_lines(body)
        if len("\n".join(body)) < 40:
            return
        base = "%s-%s" % (unit, slug(title) or "section")
        cid, n = base, 1
        while cid in used:
            n += 1
            cid = "%s-%d" % (base, n)
        used.add(cid)
        concepts.append({"id": cid, "unit": unit, "kind": kind, "title": title, "text_md": "\n".join(body)})

    def handle(level, raw, body):
        title = clean_title(raw)
        if NOISE_RE.match(title):
            return
        if question_like(raw):
            q = question_from(raw, body)
            if q:
                add_q(q)
            else:
                unanswered.append(title)
            return
        child = level + 1
        if QA_CONTAINER_RE.search(title):
            for L in (child, child + 1):
                heads = [(t, b) for t, b in sections(body, L) if question_like(t)]
                found = [question_from(t, b, title) for t, b in heads]
                if heads:
                    unanswered.extend(clean_title(t) for (t, _), q in zip(heads, found) if not q)
                    for q in found:
                        if q:
                            add_q(q)
                    if any(found):
                        return
            if STRICT_QA_RE.search(title):
                if len("\n".join(clean_lines(body))) >= 400:
                    unparsed.append({"section": title, "chars": len("\n".join(body))})
                return
            # not clearly a Q&A section: fall through and treat it as ordinary concept content
        kind = "overview" if OVERVIEW_RE.search(title) else ("practical" if PRACTICAL_RE.search(title) else "concept")
        subs = sections(body, child)
        marker = "#" * child + " "
        if len(subs) >= 2:
            first = body[: next(i for i, l in enumerate(body) if l.startswith(marker))]
            if len("\n".join(clean_lines(first))) >= 120:
                add_c(strip_number(title), first, kind)
            for sub_raw, sub_body in subs:
                st = strip_number(clean_title(sub_raw))
                if NOISE_RE.match(st):
                    continue
                if question_like(sub_raw):
                    q = question_from(sub_raw, sub_body)
                    if q:
                        add_q(q)
                    else:
                        unanswered.append(clean_title(sub_raw))
                    continue
                add_c(st, sub_body, "practical" if PRACTICAL_RE.search(st) and kind == "practical" else kind)
        else:
            cleaned = clean_lines(body)
            if is_flat(cleaned):
                flat.append({"section": strip_number(title), "chars": len("\n".join(cleaned))})
            add_c(strip_number(title), body, kind)

    for idx, (level, raw, body) in enumerate(secs):
        title = clean_title(raw)
        if idx == 0 and level == 1:
            for t, b in sections(body, 3):  # h3 sections directly under the document title
                handle(3, t, b)
            continue
        if level == 2 and NOISE_RE.match(title):
            for t, b in sections(body, 3):  # a noise h2 can wrap real h3 content
                handle(3, t, b)
            continue
        handle(level, raw, body)
    return {"concepts": concepts, "questions": questions, "flat": flat, "unparsed": unparsed, "unanswered": unanswered}


def parse_light(text: str, unit: str) -> dict:
    lines = text.splitlines()
    concepts = []

    def add(title, body, kind):
        concepts.append({"id": "%s-%s" % (unit, slug(title)), "unit": unit, "kind": kind, "title": title, "text_md": body})

    for level, raw, body in top_sections(lines):
        title = clean_title(raw)
        if re.search(r"topics covered", title, re.I):
            add("Topics covered", "\n".join(clean_lines(body)), "overview")
        elif re.search(r"key learnings", title, re.I):
            items = []
            for l in body:
                m = re.match(r">\s*\*\*\d+\.\*\*\s*(.*)", l)
                if m:
                    items.append("- " + m.group(1).strip())
            if items:
                add("Key learnings", "\n".join(items), "concept")
    seen = set()
    for t, b in sections(lines, 3):
        m = re.match(r"^\W*Task-(\d+):\s*(.*)$", t.strip())
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            add("Task %s" % m.group(1), "**Lab task %s:** %s\n\nDo this yourself in a free-tier account and write down the commands you used." % (m.group(1), m.group(2).strip()), "practical")
    return {"concepts": concepts, "questions": [], "flat": [], "unparsed": [], "unanswered": []}


# ---------------------------------------------------------------- discovery
def pretty_session(dirname: str) -> str:
    m = re.match(r"Session-(\d+)-(.*)", dirname)
    return "Session %s · %s" % (m.group(1), re.sub(r"[-_]+", " ", m.group(2)).strip()) if m else dirname


def discover(repo: str = REPO) -> List[dict]:
    """Return unit definitions (without ids resolved to files' content)."""
    found = []  # (order_key, session, kind, source_rel, dirname)
    for name in sorted(os.listdir(repo)):
        full = os.path.join(repo, name)
        m = re.match(r"Session-(\d+)-", name)
        if m and os.path.isdir(full):
            n = int(m.group(1))
            notes = sorted(f for f in os.listdir(full) if f.endswith(".md") and f not in SKIP_NAMES)
            for f in notes:
                found.append((n, "note", "%s/%s" % (name, f), name))
            if not notes and os.path.exists(os.path.join(full, "README.md")):
                found.append((n, "light", "%s/README.md" % name, name))
        elif m and os.path.isfile(full):
            found.append((int(m.group(1)), "note", name, name))
        elif name.startswith("Extra Last Session") and os.path.isfile(full):
            found.append((60, "note", name, name))
    # a session with real notes anywhere never gets a light unit
    with_notes = {n for n, k, _, _ in found if k == "note"}
    found = [f for f in found if not (f[1] == "light" and f[0] in with_notes)]
    per = {}
    for f in found:
        per.setdefault(f[0], []).append(f)
    units = []
    for n in sorted(per):
        group = sorted(per[n], key=lambda f: f[2])
        for i, (_, kind, rel, dirname) in enumerate(group):
            if n == 60:
                uid, sess = "extra-kafka", 60
            else:
                sess = int(n)
                uid = "s%02d" % sess + (chr(ord("a") + i) if len(group) > 1 else "")
            units.append({"id": uid, "session": sess, "order": n * 100 + i, "source": rel, "kind": kind, "dirname": dirname})
    return units


def unit_title(text: str, fallback: str) -> str:
    for ln in text.splitlines():
        if ln.startswith("# "):
            t = re.sub(r"^[^\w`]+", "", ln[2:]).strip()
            return t[:110]
    return fallback


def topic_of(dirname: str) -> str:
    m = re.match(r"Session-(\d+)-(.*)", dirname)
    return re.sub(r"[-_]+", " ", m.group(2)).strip() if m else dirname


def build_generic_unit(u: dict, repo: str = REPO, app: str = APP) -> dict:
    with open(os.path.join(repo, u["source"]), encoding="utf-8", errors="replace") as f:
        text = f.read()
    parsed = (parse_light if u["kind"] == "light" else parse_generic)(text, u["id"])
    batch = re.search(r"Batch[- ]?(\d+)", u["source"])
    heading = unit_title(text, "")
    day = re.search(r"Day[- ]?0*(\d+)", os.path.basename(u["source"]), re.I)
    if u["kind"] == "light":
        title = heading or topic_of(u["dirname"])
    elif u["dirname"].startswith("Session-"):
        title = topic_of(u["dirname"]) + (" \u00b7 Day %s" % day.group(1) if day else "")
    else:
        title = heading or u["dirname"]
    sess = re.match(r"Session-(\d+)", u["dirname"])
    sub = ("Session %s" % sess.group(1)) if sess else u["dirname"][:40]
    if batch:
        sub += " \u00b7 Batch-%s" % batch.group(1)
    short = re.sub(r"^Batch[- ]?\d+\s*[\u2014\u2013|:-]\s*", "", heading).strip()
    if short and short != title and short not in title:
        sub += " \u00b7 " + short[:80]
    if u["kind"] == "light":
        status = "light"
    elif parsed["flat"]:
        status = "partial"
    elif len(parsed["concepts"]) >= 3 or len(parsed["questions"]) >= 10:
        status = "ready"
    else:
        status = "sparse"
    return finish({"id": u["id"], "title": title, "subtitle": sub, "session": u["session"],
                   "module": module_for(u["session"]), "order": u["order"], "status": status,
                   "source_file": u["source"], "needs_authoring": parsed["flat"], "unparsed_qa": parsed["unparsed"],
                   "unanswered_questions": parsed["unanswered"]},
                  parsed["concepts"], parsed["questions"], app)


def finish(meta: dict, concepts: list, questions: list, app: str) -> dict:
    check_unique(concepts + questions)
    link_questions(concepts, questions)
    for c in concepts:
        rel = "content/%s/diagrams/%s.mmd" % (meta["id"], c["id"])
        has = os.path.exists(os.path.join(app, rel))
        c["diagram"] = {"type": "mermaid", "path": rel, "reviewed": False} if has else None
    meta.update({"concepts": concepts, "questions": questions})
    return meta


UNITS = [
    {"id": "fw1", "title": "Free Workshop: Terraform & IaC", "subtitle": "Workshop of 22 Aug 2026",
     "source": "FREE Workshop's/22Aug2026.md", "parser": parse_fw1},
]


def build_unit(unit: dict, repo: str = REPO, app: str = APP) -> dict:
    """Build the hand-configured fw1 unit."""
    with open(os.path.join(repo, unit["source"]), encoding="utf-8") as f:
        concepts, questions = unit["parser"](f.read(), unit["id"])
    meta = {"id": unit["id"], "title": unit["title"], "subtitle": unit.get("subtitle", ""), "session": -1,
            "module": "Free workshop", "order": -100, "status": "ready", "source_file": unit["source"],
            "needs_authoring": [], "unparsed_qa": [], "unanswered_questions": []}
    return finish(meta, concepts, questions, app)


def build_all(repo: str = REPO, app: str = APP) -> List[dict]:
    units = [build_unit(u, repo, app) for u in UNITS]
    units += [build_generic_unit(u, repo, app) for u in discover(repo)]
    seen = {}
    for u in units:
        key = (u["session"], u["title"])
        seen.setdefault(key, []).append(u)
    for group in seen.values():
        if len(group) > 1:
            for u in group:
                u["title"] += " (%s)" % u["id"]
    ids = [u["id"] for u in units]
    if len(ids) != len(set(ids)):
        raise IngestError("duplicate unit ids: %s" % sorted(i for i in ids if ids.count(i) > 1))
    return units


def write_todo(units: List[dict], repo: str = REPO, app: str = APP) -> None:
    """Regenerate DATA_TODO.md: everything that still needs human/Claude data preparation."""
    L = ["# DATA_TODO.md — what is left to prepare", "",
         "Generated by `tools/ingest.py` (do not edit by hand; rerun ingest). Status meanings:",
         "- **ready**: split by the generic parser (3+ concepts or 10+ questions), nothing flagged.",
         "- **partial**: contains flat bullet sections kept as one big concept; they need splitting by hand.",
         "- **sparse**: fewer than 3 concepts and fewer than 10 questions extracted; check the source layout.",
         "- **light**: no class notes exist; unit built from the README (topics, key learnings, task titles only).", ""]
    tot_c = sum(len(u["concepts"]) for u in units)
    tot_d = sum(1 for u in units for c in u["concepts"] if c["diagram"])
    tot_q = sum(len(u["questions"]) for u in units)
    L += ["## Totals", "", "- Units: %d, concepts: %d, questions with answers: %d" % (len(units), tot_c, tot_q),
          "- Concepts with a diagram: %d of %d" % (tot_d, tot_c), ""]
    L += ["## Units", "", "| Unit | Status | Concepts | Diagrams | Questions | Source |", "|---|---|---|---|---|---|"]
    for u in units:
        d = sum(1 for c in u["concepts"] if c["diagram"])
        L.append("| %s | %s | %d | %d | %d | %s |" % (u["id"], u["status"], len(u["concepts"]), d, len(u["questions"]), u["source_file"].replace("|", "\\|")))
    L += ["", "## 1. Flat sections to split by hand (status `partial`)", "",
          "Each is one long bullet list where titles and details are siblings. Split into concepts, then re-run ingest.", ""]
    for u in units:
        for f in u["needs_authoring"]:
            L.append("- `%s` — section **%s** (%d chars) in `%s`" % (u["id"], f["section"], f["chars"], u["source_file"]))
    L += ["", "## 1b. Q&A sections not parsed (no recognisable question headings)", ""]
    for u in units:
        for f in u["unparsed_qa"]:
            L.append("- `%s` — **%s** (%d chars) in `%s`" % (u["id"], f["section"], f["chars"], u["source_file"]))
    L += ["", "## 1c. Questions with no answer in the source (need answers written from the notes)", ""]
    for u in units:
        if u["unanswered_questions"]:
            L.append("- `%s`: %d questions (e.g. %s)" % (u["id"], len(u["unanswered_questions"]), "; ".join(x[:50] for x in u["unanswered_questions"][:2])))
    L += ["", "## 2. Units with no questions", ""]
    L += ["- `%s` (%s)" % (u["id"], u["status"]) for u in units if not u["questions"]]
    L += ["", "## 3. Diagrams", "",
          "Only units with a `content/<unit>/diagrams/<concept-id>.mmd` file have diagrams. Concepts without a diagram are listed per unit in `content/<unit>/unit.json` (`diagram: null`).", ""]
    L += ["## 4. Sources not ingested", "",
          "- `Interview-QnA.md` and `Scenarios.md` in every session: templated generic text, deliberately skipped.",
          "- `Mock-Interview/Mock-01..08`: question lists only (no answers); need grounded answers written from the class notes.",
          "- Session READMEs for sessions that have class notes (tasks, LinkedIn templates, checklists).",
          "- Skipped noise sections inside notes: Key Outcomes, Decisions, Action Items, Pending Confirmation, Student Q&A, etc.", ""]
    with open(os.path.join(app, "DATA_TODO.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main() -> int:
    units = build_all()
    base = os.path.join(APP, "content")
    for u in units:
        out_dir = os.path.join(base, u["id"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "unit.json"), "w", encoding="utf-8") as f:
            json.dump(u, f, ensure_ascii=False, indent=2)
    write_todo(units)
    by = {}
    for u in units:
        by[u["status"]] = by.get(u["status"], 0) + 1
    print("%d units %s | %d concepts | %d questions" % (len(units), by, sum(len(u["concepts"]) for u in units),
                                                          sum(len(u["questions"]) for u in units)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
