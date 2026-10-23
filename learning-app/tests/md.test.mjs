import assert from 'node:assert/strict';
import { render, inline } from '../web/md.js';

assert.equal(inline('**bold** and `code`'), '<strong>bold</strong> and <code>code</code>');
assert.equal(inline('Python *can* do'), 'Python <em>can</em> do');
// HTML in the notes must never become markup
assert.ok(!render('<script>alert(1)</script>').includes('<script>'));
assert.ok(!inline('`<img src=x onerror=1>`').includes('<img'));
assert.ok(!inline('**<b>x</b>**').includes('<b>'));
// bold markers inside code stay literal
assert.equal(inline('`**x**`'), '<code>**x**</code>');
// lists with nesting
const html = render('- **A:** one\n    - nested\n- B');
assert.equal((html.match(/<ul>/g) || []).length, 1);
assert.ok(html.includes('<li class="l1">nested</li>'));
// code fence
assert.ok(render('```bash\nterraform init\n```').includes('<pre><code>terraform init</code></pre>'));
// quote + heading
assert.ok(render('### Typical Workflow').includes('<h4>Typical Workflow</h4>'));
assert.ok(render('> **Why?**').includes('<blockquote><strong>Why?</strong></blockquote>'));
console.log('md.test.mjs ok');
