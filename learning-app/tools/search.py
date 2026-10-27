"""Full-text search over concepts and questions (SQLite FTS5, in memory). See architecture/search_and_notes.md."""
import re
import sqlite3
from typing import Dict, List


def fts5_available() -> bool:
    try:
        c = sqlite3.connect(":memory:")
        c.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        c.close()
        return True
    except sqlite3.Error:
        return False


def plain(md: str) -> str:
    """Strip Markdown/box-drawing noise so snippets read as plain text."""
    t = re.sub(r"```[^\n]*\n?", " ", md)
    t = re.sub(r"[`*#>|]+", " ", t)
    t = re.sub("[\u2500-\u257f\u25b2-\u25bc\u2190-\u21ff]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def fts_query(text: str) -> str:
    """Turn arbitrary user text into a safe FTS5 query: quoted prefix terms, ANDed."""
    tokens = re.findall(r"\w+", text or "", re.U)[:12]
    return " ".join('"%s"*' % t for t in tokens)


class SearchIndex:
    def __init__(self, units: List[dict], use_fts: bool = True):
        self.use_fts = use_fts and fts5_available()
        self.rows = []
        for u in units:
            for c in u["concepts"]:
                self.rows.append((c["id"], u["id"], u["title"], "concept", c["title"], plain(c["text_md"])))
            for q in u["questions"]:
                body = plain(q["reference_answer"])
                if q["prompt"].strip() != q["title"].strip():
                    body = plain(q["prompt"]) + " " + body
                self.rows.append((q["id"], u["id"], u["title"], "question", q["title"], body))
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        if self.use_fts:
            self.conn.execute("CREATE VIRTUAL TABLE docs USING fts5(item_id UNINDEXED, unit_id UNINDEXED, "
                              "unit_title UNINDEXED, kind UNINDEXED, title, body)")
            self.conn.executemany("INSERT INTO docs VALUES (?,?,?,?,?,?)", self.rows)

    def search(self, text: str, limit: int = 25) -> List[Dict]:
        limit = max(1, min(int(limit), 50))
        q = fts_query(text)
        if not q:
            return []
        if self.use_fts:
            cur = self.conn.execute(
                "SELECT item_id, unit_id, unit_title, kind, title, snippet(docs, 5, '[[', ']]', '…', 18) "
                "FROM docs WHERE docs MATCH ? ORDER BY bm25(docs, 0, 0, 0, 0, 10.0, 1.0) LIMIT ?", (q, limit))
            rows = cur.fetchall()
        else:
            terms = [t.lower() for t in re.findall(r"\w+", text, re.U)]
            rows = []
            for r in self.rows:
                hay = (r[4] + " " + r[5]).lower()
                if all(t in hay for t in terms):
                    i = hay.find(terms[0])
                    rows.append((r[0], r[1], r[2], r[3], r[4], r[5][max(0, i - 40):i + 120]))
                    if len(rows) >= limit:
                        break
        return [{"item_id": r[0], "unit_id": r[1], "unit_title": r[2], "kind": r[3], "title": r[4], "snippet": r[5]} for r in rows]
