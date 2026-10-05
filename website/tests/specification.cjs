'use strict';
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
let playwright;
try { playwright = require('playwright'); }
catch { playwright = require('/home/hoskinson/.local/share/mise/installs/npm-playwright/1.63.0/node_modules/playwright'); }
const dist = path.resolve(__dirname, '../dist');

(async () => {
  const server = http.createServer(async (req, res) => {
    try {
      const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).slice(1);
      const file = path.resolve(dist, relative);
      assert.ok(file.startsWith(dist + path.sep));
      const body = await fs.readFile(file);
      const type = file.endsWith('.css') ? 'text/css' : file.endsWith('.html') ? 'text/html' : 'text/plain';
      res.setHeader('Content-Type', type + '; charset=utf-8');
      res.end(body);
    } catch { res.writeHead(404); res.end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || '/home/hoskinson/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome';
    browser = await playwright.chromium.launch({headless: true, executablePath});
    const origin = `http://127.0.0.1:${server.address().port}`;
    const context = await browser.newContext({javaScriptEnabled: false, viewport: {width: 1440, height: 1000}});
    await context.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
    const page = await context.newPage();
    const failures = [];
    page.on('response', response => { if (response.status() >= 400) failures.push(response.url()); });
    await page.goto(`${origin}/specification.html`);
    assert.equal(await page.title(), 'Specification: Midnight Express');
    const nav = page.getByRole('navigation', {name: 'Main navigation'});
    assert.deepEqual(await nav.locator('a').allTextContents(), ['Overview', 'Workflows', 'Architecture', 'Data model', 'Subscriptions', 'Specification', 'Implementation']);
    assert.equal(await nav.locator('[aria-current="page"]').textContent(), 'Specification');
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('script').count(), 0, 'Core specification must remain static');
    const content = await page.locator('main').textContent();
    for (const expected of ['rfq.v0.2', 'invoice.v0.2', 'agent.v0.2', 'executes:false', 'validFrom ≤ now < validUntil', '0 < observedAmount ≤ invoicePayable', 'Pending, Final and Reversed', 'JCS', 'source authentication', 'end-to-end']) {
      assert.ok(content.includes(expected), `Missing scope or rule: ${expected}`);
    }
    assert.doesNotMatch(content, /being aligned|will appear here|will be attached/, 'Publication must not retain draft proof/source placeholders');

    // Navigate with the keyboard while scripts are disabled, including the skip link.
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').getAttribute('href'), '#main-content');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('id'), 'main-content');
    for (const detail of await page.locator('details').all()) {
      await detail.locator('summary').focus();
      await page.keyboard.press('Enter');
      assert.equal(await detail.getAttribute('open'), '');
      assert.ok(await detail.locator('p').first().isVisible());
      await page.keyboard.press('Space');
      assert.equal(await detail.getAttribute('open'), null);
    }

    // Assert reflow both at narrow physical widths and enlarged reader text.
    for (const width of [1440, 720, 390, 320]) {
      await page.setViewportSize({width, height: 1000});
      for (const fontSize of ['100%', '200%']) {
        await page.evaluate(size => { document.documentElement.style.fontSize = size; }, fontSize);
        const overflow = await page.evaluate(() => ({page: document.documentElement.scrollWidth, viewport: innerWidth}));
        assert.ok(overflow.page <= overflow.viewport, `Overflow at ${width}px / ${fontSize}: ${JSON.stringify(overflow)}`);
        for (const equation of await page.locator('.spec-equation').all()) {
          const box = await equation.boundingBox();
          assert.ok(box.x >= 0 && box.x + box.width <= width + 1, 'Equation must stay in the viewport');
        }
      }
    }

    // Exercise the actual local links, including copied Lean sources and all jump targets.
    const hrefs = await page.locator('a[href]').evaluateAll(links => links.map(link => link.getAttribute('href')));
    for (const href of new Set(hrefs.filter(href => !/^[a-z]+:/i.test(href)))) {
      const url = new URL(href, `${origin}/specification.html`);
      const response = await context.request.get(url.href);
      assert.equal(response.status(), 200, `Missing local link: ${href}`);
      if (url.hash) {
        const body = await response.text();
        const id = decodeURIComponent(url.hash.slice(1));
        assert.ok(body.includes(`id="${id}"`), `Missing fragment: ${href}`);
      }
    }
    assert.ok(hrefs.some(href => href.endsWith('/Model.lean')), 'Expose the actual model source');
    assert.ok(hrefs.some(href => href.endsWith('/Validation.lean')), 'Expose the actual validator source');

    assert.deepEqual(failures, []);
    console.log('Specification: static content, proof/source publication guards, keyboard disclosures, local links and narrow/enlarged-text reflow passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
