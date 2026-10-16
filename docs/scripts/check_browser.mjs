/** Actual interaction checks served beneath the GitHub Pages project prefix. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve, extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';

const root = fileURLToPath(new URL('../../_site/', import.meta.url));
const prefix = '/langtons-ant-core/';
const types = {'.html':'text/html', '.mjs':'text/javascript', '.js':'text/javascript',
  '.css':'text/css', '.json':'application/json', '.pdf':'application/pdf',
  '.woff2':'font/woff2', '.ttf':'font/ttf', '.svg':'image/svg+xml'};
const server = createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    assert(pathname.startsWith(prefix));
    const file = resolve(root, pathname.slice(prefix.length) || 'index.html');
    assert(file.startsWith(root));
    res.setHeader('Content-Type', types[extname(file)] || 'application/octet-stream');
    res.end(await readFile(file));
  } catch { res.statusCode = 404; res.end('Not found'); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}${prefix}`;
const browser = await chromium.launch({headless: true});
const errors = [];
const range = async (page, id, value) => page.locator(id).evaluate((el, v) => {
  el.value = v; el.dispatchEvent(new Event('input', {bubbles:true}));
}, String(value));
const text = (page, id) => page.locator(id).innerText();
try {
  for (const width of [1360, 390]) {
    const page = await browser.newPage({viewport:{width, height:1000}, reducedMotion:'reduce'});
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    for (const name of ['index', 'one-black', 'clock', 'wake', 'factors', 'memory', 'ports']) {
      await page.goto(`${base}${name}.html`);
      await page.waitForLoadState('networkidle');
      await page.evaluate(() => document.fonts.ready);
      assert(await page.locator('h1').evaluate(el => el.getBoundingClientRect().height > 20), `${name}: invisible heading`);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${name}: ${width}px overflow`);
      assert.equal(await page.locator('.site-nav a').count(), 7);
      assert(await page.locator('.katex').evaluateAll(nodes => nodes.every(n => !n.getClientRects().length || n.getBoundingClientRect().height > 0)), `${name}: invisible formula`);
      assert.equal(await page.locator('.katex-error').count(), 0, `${name}: malformed formula`);
      if (name === 'index') {
        await page.locator('#hero-step').click();
        assert.match(await text(page, '#hero-caption'), /1 cycles/);
        await page.locator('[data-filter="time"]').click();
        assert((await page.locator('.lab-card:visible').count()) < 6);
        await page.locator('[data-filter="all"]').click();
        assert.equal(await page.locator('.lab-card:visible').count(), 6);
      } else if (name === 'one-black') {
        const stages = page.locator('[data-proof-stage]');
        assert((await stages.count()) > 1);
        const before = await text(page, '#guide-title');
        await stages.nth(1).click();
        assert.notEqual(await text(page, '#guide-title'), before);
      } else if (name === 'clock') {
        await page.locator('#clock-step').click();
        assert.equal(await text(page, '#clock-time'), '1');
        assert.equal(await text(page, '#clock-gain'), '+1');
        await page.locator('#clock-finish').click();
        await page.waitForFunction(() => document.querySelector('#clock-status').textContent.includes('exit'));
        assert.equal(await text(page, '#clock-time'), '36');
      } else if (name === 'wake') {
        await range(page, '#phase', 52);
        await page.locator('#wake-preset').selectOption('excluded');
        assert.match(await text(page, '#screen-result'), /exclud/i);
        await page.locator('#wake-preset').selectOption('standard');
        assert.match(await text(page, '#growth'), /12/);
      } else if (name === 'factors') {
        assert.match(await text(page, '#mass-equation'), /322/);
        const before = await text(page, '#interval-label');
        await page.locator('#interval-step').click();
        assert.notEqual(await text(page, '#interval-label'), before);
        await page.locator('#factor-preset').selectOption('blank');
        await range(page, '#interval-end', 600);
        assert(Number(await text(page, '#bad-windows')) > 0);
      } else if (name === 'memory') {
        const before = await page.locator('#time').inputValue();
        await page.locator('#step-button').click();
        assert.equal(Number(await page.locator('#time').inputValue()), Number(before) + 1);
        await page.locator('#huge-family').click();
        assert((await text(page, '#family-death')).length > 50);
        await range(page, '#scale', 128);
        assert.equal(await text(page, '#scale-output'), '128');
      } else if (name === 'ports') {
        await page.locator('#ports-end').click();
        await page.waitForFunction(() => document.querySelector('#ports-check').textContent.startsWith('PASS:'));
        await page.locator('#ports-mode').selectOption('sharp');
        await page.locator('#ports-end').click();
        await page.waitForFunction(() => document.querySelector('#ports-check').textContent.startsWith('PASS:'));
        assert.equal(await text(page, '#ports-time'), '918');
      }
      console.log(`PASS ${width}px ${name}`);
    }
    for (const name of ['one-black','clock','wake','factors','memory','ports']) {
      const response = await page.request.get(`${base}papers/${name}.pdf`);
      assert.equal(response.status(), 200);
      assert((await response.body()).subarray(0,5).equals(Buffer.from('%PDF-')));
    }
    await page.close();
  }
  assert.deepEqual(errors, []);
  console.log('Browser checks passed at the project prefix: desktop/mobile interactions, formulas, six downloads.');
} finally {
  await browser.close();
  await new Promise(r => server.close(r));
}
