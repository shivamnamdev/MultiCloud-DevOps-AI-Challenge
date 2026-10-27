import { render, esc } from './md.js';

const app = document.getElementById('app');
const state = { progress: {}, notes: {}, bookmarks: new Set(), scrollTo: null, mermaid: null, mermaidFailed: false, unit: null, diagramSeq: 0 };

const CONCEPT_STATUSES = [['not_started', 'Not started', ''], ['read', 'Read', ''], ['lab_done', 'Lab done', ''], ['mastered', 'Mastered', 'ok']];
const QUESTION_STATUSES = [['known', 'Got it', 'ok'], ['review', 'Review again', 'warn']];
const KIND_LABEL = { concept: 'concept', practical: 'hands-on', overview: 'overview', method: 'method', interview: 'interview', scenario: 'scenario' };

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error(path + ' -> HTTP ' + r.status);
  return r.json();
}

const status = (id) => state.progress[id] || 'not_started';
const post = (path, body) => api(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });

function extras(id) {
  const note = state.notes[id] || '';
  const on = state.bookmarks.has(id);
  return '<div class="extras"><button class="star' + (on ? ' on' : '') + '" data-bm="' + esc(id) + '" aria-pressed="' + on + '" title="Bookmark">' + (on ? '★' : '☆') + '</button>' +
    '<details class="mynote"' + (note ? ' open' : '') + '><summary>My notes' + (note ? ' ✎' : '') + '</summary>' +
    '<textarea data-note="' + esc(id) + '" rows="3" maxlength="5000" placeholder="Write your own notes…">' + esc(note) + '</textarea>' +
    '<button class="btn" data-savenote="' + esc(id) + '">Save note</button> <span class="note" data-notemsg="' + esc(id) + '"></span></details></div>';
}

function openItem(unit, kind, id) {
  const tab = kind === 'concept' ? 'learn' : 'practice';
  state.scrollTo = (kind === 'concept' ? 'c-' : 'q-') + id;
  const target = '#/u/' + unit + '/' + tab;
  if (location.hash === target) route(); else location.hash = target;
}

async function loadMermaid() {
  if (state.mermaid || state.mermaidFailed) return state.mermaid;
  try {
    const m = (await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs')).default;
    const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    m.initialize({ startOnLoad: false, securityLevel: 'strict', theme: dark ? 'dark' : 'default' });
    state.mermaid = m;
  } catch (e) {
    state.mermaidFailed = true;
  }
  return state.mermaid;
}

async function renderDiagrams(concepts) {
  const mermaid = await loadMermaid();
  for (const c of concepts) {
    if (!c.diagram_src) continue;
    const el = document.getElementById('dg-' + c.id);
    if (!el) continue;
    const fallback = (why) => {
      el.innerHTML = '<pre><code>' + esc(c.diagram_src) + '</code></pre><div class="note">' + esc(why) + '</div>';
    };
    if (!mermaid) { fallback('Diagram renderer could not load (needs internet for the Mermaid library). Showing source.'); continue; }
    const rid = 'mm' + (++state.diagramSeq);
    try {
      const { svg } = await mermaid.render(rid, c.diagram_src);
      el.innerHTML = svg;
    } catch (e) {
      const leftover = document.getElementById('d' + rid);
      if (leftover) leftover.remove();
      fallback('This diagram has a syntax error. Showing source.');
    }
  }
}

function pct(a, b) { return b ? Math.round((100 * a) / b) : 0; }

function statusButtons(id, options) {
  const cur = status(id);
  return '<div class="seg" data-item="' + esc(id) + '">' + options.map(([val, label, cls]) =>
    '<button data-status="' + val + '" class="' + (cur === val ? 'on ' + cls : '') + '">' + esc(label) + '</button>').join('') + '</div>';
}

const STATUS_NOTE = {
  partial: ['partly split', 'Some long sections in this note are still one big block (listed below). They are kept verbatim but not yet split into separate concepts.'],
  light: ['outline only', 'No class notes exist for this session. This unit is built from the session README: topics, key learnings and lab task titles only.'],
  sparse: ['needs data', 'Very little could be extracted automatically from this note. It needs manual preparation.'],
};

async function home() {
  const units = await api('/api/units');
  const modules = [];
  units.forEach((u) => {
    let m = modules.find((x) => x.name === u.module);
    if (!m) { m = { name: u.module, units: [] }; modules.push(m); }
    m.units.push(u);
  });
  app.innerHTML = '<h1>Your courses</h1><p class="muted">' + units.length + ' units. Each concept shows the original notes next to a diagram where one exists.</p>' +
    modules.map((m) => '<h2 class="module">' + esc(m.name) + '</h2><div class="grid">' + m.units.map((u) => {
      const done = u.concepts_studied + u.questions_known;
      const total = u.concepts + u.questions;
      const note = STATUS_NOTE[u.status];
      return '<a class="card unit-card" href="#/u/' + esc(u.id) + '/learn"><h2>' + esc(u.title) +
        (note ? '<span class="badge warn">' + esc(note[0]) + '</span>' : '') + '</h2><div class="muted">' + esc(u.subtitle) +
        '</div><div class="bar"><span style="width:' + pct(done, total) + '%"></span></div><div class="muted">' +
        u.concepts_studied + '/' + u.concepts + ' concepts · ' + u.questions_known + '/' + u.questions + ' questions · ' +
        u.diagrams + ' diagrams</div></a>';
    }).join('') + '</div>').join('');
}

function summaryHtml(u) {
  const cs = u.concepts.filter((c) => status(c.id) !== 'not_started').length;
  const qk = u.questions.filter((q) => status(q.id) === 'known').length;
  return '<div class="bar"><span style="width:' + pct(cs + qk, u.concepts.length + u.questions.length) + '%"></span></div>' +
    '<div class="muted">' + cs + '/' + u.concepts.length + ' concepts studied · ' + qk + '/' + u.questions.length + ' questions known</div>';
}

function unitShell(u, tab) {
  const note = STATUS_NOTE[u.status];
  const flat = (u.needs_authoring || []).map((f) => '<li>' + esc(f.section) + '</li>').join('');
  const banner = note ? '<div class="card notice"><strong>' + esc(note[0]) + '.</strong> ' + esc(note[1]) + (flat ? '<ul>' + flat + '</ul>' : '') + '</div>' : '';
  return '<h1>' + esc(u.title) + '</h1><div class="muted">' + esc(u.subtitle) + ' · source: ' + esc(u.source_file) + '</div>' + banner +
    '<div id="summary">' + summaryHtml(u) + '</div>' +
    '<div class="tabs"><a class="tab ' + (tab === 'learn' ? 'on' : '') + '" href="#/u/' + esc(u.id) + '/learn">Learn</a>' +
    '<a class="tab ' + (tab === 'practice' ? 'on' : '') + '" href="#/u/' + esc(u.id) + '/practice">Practice questions</a>' +
    '<a class="tab" href="#/u/' + esc(u.id) + '/print">Cheat sheet</a></div>';
}

async function learn(unitId) {
  const u = state.unit = await api('/api/units/' + unitId);
  const toc = u.concepts.map((c) => '<a href="#c-' + esc(c.id) + '" data-scroll="' + esc(c.id) + '"><span class="dot s-' + status(c.id) + '" data-dot="' + esc(c.id) + '"></span>' + esc(c.title) + '</a>').join('');
  const cards = u.concepts.map((c) => {
    const diagram = c.diagram_src
      ? '<div class="diagram" id="dg-' + esc(c.id) + '"><span class="muted">Rendering diagram…</span></div><div class="note">Diagram generated by AI from the notes, not yet human-reviewed.</div>'
      : '<div class="diagram"><span class="muted">No diagram for this concept yet.</span></div>';
    return '<section class="card" id="c-' + esc(c.id) + '"><h2>' + esc(c.title) + '<span class="badge">' + esc(KIND_LABEL[c.kind] || c.kind) + '</span></h2>' +
      '<div class="split"><div>' + render(c.text_md) + '</div><div>' + diagram + '</div></div>' + statusButtons(c.id, CONCEPT_STATUSES) + extras(c.id) + '</section>';
  }).join('');
  app.innerHTML = unitShell(u, 'learn') + '<div class="layout"><nav class="toc card">' + toc + '</nav><div>' + cards + '</div></div>';
  renderDiagrams(u.concepts);
}

function questionCard(q, concepts) {
  const links = (q.concept_ids || []).map((id) => {
    const c = concepts.find((x) => x.id === id);
    return c ? '<a href="#/u/' + esc(q.unit) + '/learn" data-goto="' + esc(id) + '">' + esc(c.title) + '</a>' : '';
  }).filter(Boolean).join(', ');
  return '<section class="card" id="q-' + esc(q.id) + '" data-q="' + esc(q.id) + '" data-kind="' + esc(q.kind) + '"><h2><span class="dot s-' + status(q.id) + '" data-dot="' + esc(q.id) + '"></span>' +
    esc(q.title) + '<span class="badge">' + esc(KIND_LABEL[q.kind]) + '</span></h2>' +
    (q.kind === 'scenario' ? '<p>' + esc(q.prompt) + '</p>' : '') +
    '<button class="btn" data-reveal="' + esc(q.id) + '">Show reference answer</button>' +
    '<div class="answer" id="ans-' + esc(q.id) + '" hidden>' + render(q.reference_answer) +
    (links ? '<div class="note">Related concepts: ' + links + '</div>' : '') + '</div>' +
    statusButtons(q.id, QUESTION_STATUSES) + extras(q.id) + '</section>';
}

async function practice(unitId) {
  const u = state.unit = await api('/api/units/' + unitId);
  app.innerHTML = unitShell(u, 'practice') +
    '<p class="muted">Try to answer out loud first (What → Why → How → Example), then reveal the reference answer. Mock interviews with a local LLM come in a later step.</p>' +
    '<div class="filters"><span class="muted">Show:</span>' +
    ['all', 'interview', 'scenario', 'review'].map((f) => '<button class="btn" data-filter="' + f + '">' + f + '</button>').join('') + '</div>' +
    (u.questions.length ? '<div id="qlist">' + u.questions.map((q) => questionCard(q, u.concepts)).join('') + '</div>'
      : '<div class="card muted">No questions with answers could be extracted from this unit yet. See DATA_TODO.md.</div>');
}

async function printView(unitId) {
  const u = state.unit = await api('/api/units/' + unitId);
  app.innerHTML = '<div class="noprint"><a href="#/u/' + esc(u.id) + '/learn">← Back to unit</a> ' +
    '<button class="btn" data-print>Print / Save as PDF</button></div><article class="sheet"><h1>' + esc(u.title) + '</h1><div class="muted">' + esc(u.subtitle) + '</div>' +
    u.concepts.map((c) => '<section class="sheetitem"><h2>' + esc(c.title) + '</h2>' + render(c.text_md) +
      (c.diagram_src ? '<div class="diagram" id="dg-' + esc(c.id) + '"></div>' : '') +
      (state.notes[c.id] ? '<div class="mynoteprint"><strong>My note:</strong> ' + esc(state.notes[c.id]) + '</div>' : '') + '</section>').join('') + '</article>';
  renderDiagrams(u.concepts);
}

async function searchView(q) {
  document.getElementById('q').value = q;
  const hits = q.trim() ? await api('/api/search?q=' + encodeURIComponent(q)) : [];
  app.innerHTML = '<h1>Search</h1><p class="muted">' + (q.trim() ? hits.length + ' result' + (hits.length === 1 ? '' : 's') + ' for "' + esc(q) + '"' : 'Type something in the box above.') + '</p>' +
    hits.map((h) => '<a class="card result" href="#/u/' + esc(h.unit_id) + '/' + (h.kind === 'concept' ? 'learn' : 'practice') + '" data-open="' + esc(h.item_id) + '" data-unit="' + esc(h.unit_id) + '" data-kind="' + esc(h.kind) + '">' +
      '<h2>' + esc(h.title) + '<span class="badge">' + esc(h.kind) + '</span></h2><div class="muted">' + esc(h.unit_title) + '</div>' +
      '<div>' + esc(h.snippet).replace(/\[\[/g, '<mark>').replace(/\]\]/g, '</mark>') + '</div></a>').join('');
}

async function mineView() {
  const rows = await api('/api/mine');
  app.innerHTML = '<h1>My notes and bookmarks</h1><p class="muted">' + rows.length + ' item' + (rows.length === 1 ? '' : 's') + '</p>' +
    (rows.length ? rows.map((r) => '<a class="card result" href="#/u/' + esc(r.unit_id) + '/' + (r.kind === 'concept' ? 'learn' : 'practice') + '" data-open="' + esc(r.item_id) + '" data-unit="' + esc(r.unit_id) + '" data-kind="' + esc(r.kind) + '">' +
      '<h2>' + (r.bookmarked ? '★ ' : '') + esc(r.title) + '<span class="badge">' + esc(r.kind) + '</span></h2><div class="muted">' + esc(r.unit_title) + '</div>' +
      (r.note ? '<div class="mynoteprint">' + esc(r.note) + '</div>' : '') + '</a>').join('')
      : '<div class="card muted">Star a concept or write a note on any card and it will show up here.</div>');
}

function applyFilter(f) {
  document.querySelectorAll('#qlist [data-q]').forEach((el) => {
    const id = el.dataset.q;
    const show = f === 'all' || el.dataset.kind === f || (f === 'review' && status(id) === 'review');
    el.hidden = !show;
  });
}

async function setStatus(id, value) {
  const next = status(id) === value && value !== 'not_started' ? 'not_started' : value;
  const kindIsConcept = state.unit.concepts.some((c) => c.id === id);
  const sendVal = next;
  await api('/api/progress', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ item_id: id, status: sendVal }) });
  state.progress[id] = sendVal;
  const group = document.querySelector('.seg[data-item="' + CSS.escape(id) + '"]');
  if (group) {
    const opts = kindIsConcept ? CONCEPT_STATUSES : QUESTION_STATUSES;
    group.querySelectorAll('button').forEach((b) => {
      const cls = (opts.find((o) => o[0] === b.dataset.status) || [0, 0, ''])[2];
      b.className = b.dataset.status === sendVal ? 'on ' + cls : '';
    });
  }
  document.querySelectorAll('[data-dot="' + CSS.escape(id) + '"]').forEach((d) => { d.className = 'dot s-' + sendVal; });
  const s = document.getElementById('summary');
  if (s) s.innerHTML = summaryHtml(state.unit);
}

app.addEventListener('click', (e) => {
  const t = e.target.closest('button, a');
  if (!t) return;
  if (t.dataset.status && t.parentElement.dataset.item) {
    setStatus(t.parentElement.dataset.item, t.dataset.status).catch((err) => alert('Could not save progress: ' + err.message));
  } else if (t.dataset.reveal) {
    const a = document.getElementById('ans-' + t.dataset.reveal);
    a.hidden = !a.hidden;
    t.textContent = a.hidden ? 'Show reference answer' : 'Hide reference answer';
  } else if (t.dataset.filter) {
    applyFilter(t.dataset.filter);
  } else if (t.dataset.scroll) {
    e.preventDefault();
    document.getElementById('c-' + t.dataset.scroll).scrollIntoView({ behavior: 'smooth' });
  } else if (t.dataset.goto) {
    e.preventDefault();
    openItem(state.unit.id, 'concept', t.dataset.goto);
  } else if (t.dataset.open) {
    e.preventDefault();
    openItem(t.dataset.unit, t.dataset.kind, t.dataset.open);
  } else if (t.dataset.bm) {
    const id = t.dataset.bm;
    const on = !state.bookmarks.has(id);
    post('/api/bookmarks', { item_id: id, on }).then(() => {
      if (on) state.bookmarks.add(id); else state.bookmarks.delete(id);
      t.classList.toggle('on', on); t.textContent = on ? '★' : '☆'; t.setAttribute('aria-pressed', String(on));
    }).catch((err) => alert('Could not save bookmark: ' + err.message));
  } else if (t.dataset.savenote) {
    const id = t.dataset.savenote;
    const box = document.querySelector('textarea[data-note="' + CSS.escape(id) + '"]');
    const msg = document.querySelector('[data-notemsg="' + CSS.escape(id) + '"]');
    post('/api/notes', { item_id: id, text: box.value }).then(() => {
      if (box.value.trim()) state.notes[id] = box.value; else delete state.notes[id];
      msg.textContent = box.value.trim() ? 'Saved' : 'Note removed';
    }).catch((err) => { msg.textContent = 'Could not save: ' + err.message; });
  } else if (t.dataset.print !== undefined) {
    window.print();
  }
});

async function route() {
  try {
    const [progress, notes, marks] = await Promise.all([api('/api/progress'), api('/api/notes'), api('/api/bookmarks')]);
    state.progress = progress; state.notes = notes; state.bookmarks = new Set(marks);
    const [path, query = ''] = location.hash.split('?');
    const m = path.match(/^#\/u\/([\w-]+)\/(learn|practice|print)$/);
    if (m) await (m[2] === 'learn' ? learn(m[1]) : m[2] === 'practice' ? practice(m[1]) : printView(m[1]));
    else if (path === '#/search') await searchView(new URLSearchParams(query).get('q') || '');
    else if (path === '#/mine') await mineView();
    else await home();
    if (state.scrollTo) {
      const el = document.getElementById(state.scrollTo);
      state.scrollTo = null;
      if (el) el.scrollIntoView();
    }
  } catch (err) {
    app.innerHTML = '<div class="card"><h2>Something went wrong</h2><p>' + esc(err.message) + '</p></div>';
  }
}

document.getElementById('searchform').addEventListener('submit', (e) => {
  e.preventDefault();
  location.hash = '#/search?q=' + encodeURIComponent(document.getElementById('q').value);
});

window.addEventListener('hashchange', route);
route();
