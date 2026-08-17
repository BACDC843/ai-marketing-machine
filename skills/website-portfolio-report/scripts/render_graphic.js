#!/usr/bin/env node
/**
 * render_graphic.js — render an HTML social-graphic card to PNG.
 * Part of the website-portfolio-report skill (ai-marketing-machine plugin).
 *
 * Usage: node render_graphic.js <input.html> <output.png> [width] [height]
 * Defaults: 1080x1350 (4:5 portrait, the feed-safe social card size).
 *
 * Uses the environment's pre-installed Chromium (PLAYWRIGHT_BROWSERS_PATH
 * or /opt/pw-browsers/chromium). Do NOT run `playwright install`.
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [, , input, output, w, h] = process.argv;
  if (!input || !output) {
    console.error('Usage: node render_graphic.js <input.html> <output.png> [width] [height]');
    process.exit(1);
  }
  const width = parseInt(w || '1080', 10);
  const height = parseInt(h || '1350', 10);
  const executablePath = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium';

  let browser;
  try {
    browser = await chromium.launch({ executablePath });
  } catch (e) {
    // Fall back to Playwright's own resolution (PLAYWRIGHT_BROWSERS_PATH)
    browser = await chromium.launch();
  }
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  // Give webfonts (e.g. Google Fonts @import) a moment to paint
  await page.waitForTimeout(1500);
  await page.screenshot({ path: output });
  await browser.close();
  console.log('rendered: ' + output + ' (' + width + 'x' + height + ')');
})();
