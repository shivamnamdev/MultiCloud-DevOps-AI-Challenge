// Tiny, safe Markdown renderer: everything is HTML-escaped before formatting is applied.
export function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

export function inline(s) {
  return s.split(/(`[^`]+`)/).map((p) => {
    if (p.length > 1 && p[0] === '`' && p.endsWith('`')) return '<code>' + esc(p.slice(1, -1)) + '</code>';
    let t = esc(p);
    t = t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    t = t.replace(/(^|[^*])\*([^*\s][^*]*?)\*(?!\*)/g, '$1<em>$2</em>');
    return t;
  }).join('');
}

export function render(md) {
  const lines = md.split('\n');
  let html = '', i = 0, inList = false, para = [];
  const flushPara = () => { if (para.length) { html += '<p>' + inline(para.join(' ')) + '</p>'; para = []; } };
  const closeList = () => { if (inList) { html += '</ul>'; inList = false; } };
  while (i < lines.length) {
    const ln = lines[i];
    if (ln.startsWith('```')) {
      flushPara(); closeList();
      const buf = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) { buf.push(lines[i]); i++; }
      i++;
      html += '<pre><code>' + esc(buf.join('\n')) + '</code></pre>';
      continue;
    }
    const h = ln.match(/^#{1,4}\s+(.*)/);
    if (h) { flushPara(); closeList(); html += '<h4>' + inline(h[1]) + '</h4>'; i++; continue; }
    const b = ln.match(/^(\s*)[-*]\s+(.*)/);
    if (b) {
      flushPara();
      if (!inList) { html += '<ul>'; inList = true; }
      html += '<li class="l' + Math.min(3, Math.floor(b[1].length / 3)) + '">' + inline(b[2]) + '</li>';
      i++; continue;
    }
    const q = ln.match(/^>\s?(.*)/);
    if (q) { flushPara(); closeList(); html += '<blockquote>' + inline(q[1]) + '</blockquote>'; i++; continue; }
    if (!ln.trim()) { flushPara(); closeList(); i++; continue; }
    closeList();
    para.push(ln.trim());
    i++;
  }
  flushPara(); closeList();
  return html;
}
