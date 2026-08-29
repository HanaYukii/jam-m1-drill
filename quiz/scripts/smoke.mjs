// Headless smoke test of dist/jam-m1-drill.html: console errors, answer flow, mock flow, screenshots (light/dark).
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';

const file = 'file://' + path.resolve('dist/jam-m1-drill.html');
const browser = await chromium.launch();
const results = { errors: [], steps: [] };
for (const scheme of ['light', 'dark']) {
  const ctx = await browser.newContext({ colorScheme: scheme, viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  page.on('pageerror', e => results.errors.push(scheme + ': pageerror ' + e.message));
  page.on('console', m => { if (m.type() === 'error') results.errors.push(scheme + ': console ' + m.text()); });
  await page.goto(file);
  await page.waitForTimeout(600);
  const stem = await page.locator('.stem').first().textContent();
  results.steps.push(scheme + ': first stem: ' + stem.slice(0, 80));
  // answer via keyboard
  await page.keyboard.press('2');
  await page.waitForTimeout(150);
  const verdict = await page.locator('.verdict').first().textContent().catch(() => null);
  results.steps.push(scheme + ': verdict after key 2: ' + verdict);
  const explLen = (await page.locator('.expl').first().textContent()).length;
  results.steps.push(scheme + ': explanation chars: ' + explLen);
  results.steps.push(scheme + ': per-option notes: ' + await page.locator('.optnotes .on').count()
    + ' | key tagged: ' + await page.locator('.on.ok .on-tag.ok').count()
    + ' | your-pick tagged: ' + await page.locator('.on-tag.you').count());
  await page.screenshot({ path: `dist/shot-${scheme}-answered.png`, fullPage: true });
  await page.keyboard.press('Enter');
  await page.waitForTimeout(150);
  const stem2 = await page.locator('.stem').first().textContent();
  results.steps.push(scheme + ': second stem differs: ' + (stem2 !== stem));
  // chapter filter: Safrole
  await page.locator('.ch[data-ch="6"]').click();
  await page.waitForTimeout(150);
  const tag = await page.locator('.tag.chtag').first().textContent();
  results.steps.push(scheme + ': chapter 6 tag: ' + tag);
  // code question via kind chip
  await page.locator('.chip[data-kind="code"]').click();
  await page.waitForTimeout(150);
  const hasCode = await page.locator('pre.code').count();
  results.steps.push(scheme + ': code block shown for kind=code filter: ' + hasCode);
  await page.screenshot({ path: `dist/shot-${scheme}-code.png`, fullPage: false });
  await page.locator('.chip[data-kind="code"]').click();
  await page.locator('.ch[data-ch=""]').click();
  // mock
  await page.locator('.modes button[data-mode="mock"]').click();
  await page.waitForTimeout(150);
  await page.locator('#mockN button[data-n="10"]').click();
  await page.locator('#mockMode button[data-m="exam"]').click();
  await page.locator('#startMock').click();
  await page.waitForTimeout(150);
  for (let i = 0; i < 10; i++) {
    await page.keyboard.press(String(1 + (i % 4)));
    await page.waitForTimeout(60);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(60);
  }
  const score = await page.locator('.score').first().textContent().catch(() => null);
  results.steps.push(scheme + ': mock score: ' + (score || '').replace(/\s+/g, ' ').trim());
  results.steps.push(scheme + ': mock review items: ' + await page.locator('.review-item').count()
    + ' | with 逐項辨析: ' + await page.locator('.review-item .optnotes').count());
  await page.screenshot({ path: `dist/shot-${scheme}-results.png`, fullPage: false });
  // review mode
  await page.locator('.modes button[data-mode="review"]').click();
  await page.waitForTimeout(150);
  const reviewStatus = await page.locator('#status').textContent();
  results.steps.push(scheme + ': review status: ' + reviewStatus.replace(/\s+/g, ' ').trim().slice(0, 80));
  // localStorage persisted?
  const stored = await page.evaluate(() => Object.keys(JSON.parse(localStorage.getItem('jam-m1-drill-v1')).progress).length);
  results.steps.push(scheme + ': progress entries stored: ' + stored);
  // narrow viewport
  await page.setViewportSize({ width: 420, height: 800 });
  await page.locator('.modes button[data-mode="practice"]').click();
  await page.waitForTimeout(200);
  const bodyScrollW = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  results.steps.push(scheme + ': no horizontal overflow at 420px: ' + bodyScrollW);
  await page.screenshot({ path: `dist/shot-${scheme}-mobile.png`, fullPage: false });
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify(results, null, 1));

// glossary smoke test
{
  const browser2 = await chromium.launch();
  const ctx = await browser2.newContext({ colorScheme: 'light', viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push('gloss pageerror ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL/.test(m.text())) errs.push('gloss console ' + m.text()); });
  await page.goto(file);
  await page.waitForTimeout(400);
  await page.locator('.modes button[data-mode="gloss"]').click();
  await page.waitForTimeout(300);
  console.log('terms rendered:', await page.locator('.gcard').count());
  console.log('status:', (await page.locator('#status').textContent()).replace(/\s+/g,' ').trim());
  await page.locator('.chip[data-gcat="pvm"]').click();
  await page.waitForTimeout(200);
  console.log('pvm cat cards:', await page.locator('.gcard').count());
  await page.locator('.chip[data-gcat=""]').click();
  await page.waitForTimeout(150);
  await page.locator('#gsearch').fill('erasure');
  await page.waitForTimeout(400);
  console.log('search "erasure" cards:', await page.locator('.gcard').count(), 'marks:', await page.locator('mark').count());
  await page.screenshot({ path: 'dist/shot-gloss.png' });
  await page.locator('#gsearch').fill('');
  await page.waitForTimeout(300);
  const first = page.locator('.gcard').first();
  await first.locator('summary').click();
  await page.waitForTimeout(200);
  const relCount = await page.locator('.grel button').count();
  if (relCount) { await page.locator('.grel button').first().click(); await page.waitForTimeout(300); }
  console.log('after rel click, open cards:', await page.locator('.gcard[open]').count());
  await page.setViewportSize({ width: 420, height: 800 });
  await page.waitForTimeout(200);
  console.log('gloss no h-overflow @420:', await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  await page.screenshot({ path: 'dist/shot-gloss-mobile.png' });
  console.log('glossary errors:', JSON.stringify(errs));

  // ---- Q&A mode ----
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.locator('.modes button[data-mode="qa"]').click();
  await page.waitForTimeout(400);
  const cards = page.locator('#content .card.qa');
  console.log('qa cards:', await cards.count());
  console.log('qa answers hidden initially:', await page.locator('#content .qa-a:not([hidden])').count() === 0);
  await cards.first().locator('.qa-q').click();
  await page.waitForTimeout(200);
  console.log('qa after click, open:', await page.locator('#content .qa-a:not([hidden])').count(),
              '| has 標準答案:', await page.locator('#content .qa-ans').first().isVisible());
  await page.locator('#qaToggle').click();
  await page.waitForTimeout(500);
  const allOpen = await page.locator('#content .qa-a:not([hidden])').count();
  console.log('qa expand-all open:', allOpen, '/', await cards.count());
  console.log('qa status:', (await page.locator('#status').textContent()).replace(/\s+/g,' ').trim());
  await page.locator('.ch[data-ch="13"]').click();
  await page.waitForTimeout(400);
  console.log('qa ch13 cards:', await cards.count());
  await page.screenshot({ path: 'dist/shot-qa.png' });
  await page.setViewportSize({ width: 420, height: 800 });
  await page.waitForTimeout(250);
  console.log('qa no h-overflow @420:', await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  console.log('qa errors:', JSON.stringify(errs));

  // ---- cheat sheet ----
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.locator('.modes button[data-mode="sheet"]').click();
  await page.waitForTimeout(300);
  await page.locator('.ch[data-ch=""]').click();
  await page.waitForTimeout(300);
  console.log('sheet picker buttons:', await page.locator('#content [data-go]').count());
  await page.locator('#content [data-go]').first().click();
  await page.waitForTimeout(300);
  console.log('sheet title:', await page.locator('.sheet h2').textContent(),
              '| sections:', await page.locator('.sheet section').count(),
              '| asked:', await page.locator('.sheet .qa').count());
  await page.locator('.ch[data-ch="12"]').click();
  await page.waitForTimeout(300);
  console.log('sheet after ch12:', await page.locator('.sheet h2').textContent());
  await page.screenshot({ path: 'dist/shot-sheet.png', fullPage: true });
  await page.setViewportSize({ width: 420, height: 800 });
  await page.waitForTimeout(250);
  console.log('sheet no h-overflow @420:', await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  console.log('sheet errors:', JSON.stringify(errs));
  await browser2.close();
}
