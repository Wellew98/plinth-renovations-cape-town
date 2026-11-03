// Viewport screenshots at a given scroll position, with lazy images settled.
// Usage: node shot.js / our-work 4281 recent-work 1440 900
const p = require('puppeteer-core');
const [, , url = '/', name = 'shot', y = '0', w = '1440', h = '900'] = process.argv;

(async () => {
  const b = await p.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    args: ['--no-sandbox', '--hide-scrollbars'],
  });
  const pg = await b.newPage();
  await pg.setViewport({ width: +w, height: +h, deviceScaleFactor: 2 });
  await pg.goto('http://127.0.0.1:8100' + url, { waitUntil: 'networkidle2' });
  await pg.evaluate((yy) => window.scrollTo(0, yy), +y);
  // let reveals fire, lazy images fetch, transitions finish
  await pg.evaluate(async () => {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
    await new Promise((r) => setTimeout(r, 1200));
  });
  await new Promise((r) => setTimeout(r, 800));
  await pg.screenshot({ path: `../_shots/vp-${name}.png` });
  console.log('shot ->', `_shots/vp-${name}.png`);
  await b.close();
})();
