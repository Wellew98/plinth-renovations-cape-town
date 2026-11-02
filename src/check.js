// Real layout checks against Edge: measures overflow, then screenshots at the
// two widths the project brief requires (390 mobile, 1440 desktop).
const puppeteer = require('puppeteer-core');
const path = require('path');

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const BASE = 'http://127.0.0.1:8100';
const SHOTS = path.join(__dirname, '..', '_shots');

const PAGES = [
  ['home', '/'],
  ['waterproofing', '/waterproofing'],
  ['damp', '/damp-proofing'],
  ['durbanville', '/home-renovations-in-durbanville'],
  ['services', '/services'],
  ['estimate', '/estimate'],
  ['faq', '/faq'],
  ['contact', '/contact'],
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EDGE,
    headless: 'new',
    args: ['--hide-scrollbars', '--disable-gpu'],
  });

  for (const [width, height, label, isMobile] of [
    [390, 844, '390', true],
    [1440, 900, '1440', false],
  ]) {
    const page = await browser.newPage();
    await page.setViewport({ width, height, isMobile, deviceScaleFactor: 2 });
    for (const [name, url] of PAGES) {
      await page.goto(BASE + url, { waitUntil: 'networkidle0' });
      const report = await page.evaluate(() => {
        const vw = window.innerWidth;
        const wide = [];
        document.querySelectorAll('body *').forEach((el) => {
          const r = el.getBoundingClientRect();
          if (r.width > vw + 1 || r.right > vw + 1) {
            wide.push({
              tag: el.tagName.toLowerCase(),
              cls: (el.className || '').toString().slice(0, 40),
              w: Math.round(r.width),
              right: Math.round(r.right),
            });
          }
        });
        return {
          vw,
          scrollWidth: document.documentElement.scrollWidth,
          bodyWidth: Math.round(document.body.getBoundingClientRect().width),
          wide: wide.slice(0, 8),
        };
      });
      const bad = report.scrollWidth > report.vw + 1 || report.wide.length;
      console.log(
        `${label.padEnd(5)} ${name.padEnd(14)} scrollW=${report.scrollWidth}` +
          ` vw=${report.vw} ${bad ? 'OVERFLOW' : 'ok'}`
      );
      if (bad) for (const w of report.wide) console.log(`        ${w.tag}.${w.cls} w=${w.w} right=${w.right}`);
      await page.screenshot({ path: path.join(SHOTS, `${name}-${label}.png`), fullPage: true });
    }
    await page.close();
  }
  await browser.close();
})();
