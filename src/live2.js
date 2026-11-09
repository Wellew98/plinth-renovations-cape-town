// Live-site render check: real browser, real network, console errors captured.
const p = require('puppeteer-core');
const B = 'https://plinthrenovations.co.za';
(async () => {
  const b = await p.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--no-sandbox'] });
  const out = [];
  for (const [path, y, name, w, h] of [['/', 0, 'live-home', 1440, 900], ['/waterproofing', 620, 'live-wp', 1440, 900], ['/estimate', 500, 'live-est', 1440, 900], ['/', 0, 'live-m', 390, 844]]) {
    const page = await b.newPage();
    const errs = [];
    page.on('console', (m) => m.type() === 'error' && errs.push(m.text().slice(0, 120)));
    page.on('pageerror', (e) => errs.push('pageerror: ' + e.message.slice(0, 120)));
    await page.setViewport({ width: w, height: h, deviceScaleFactor: 2 });
    await page.goto(B + path + '?v=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await new Promise((r) => setTimeout(r, 1200));
    await page.screenshot({ path: '../_shots/' + name + '.png' });
    const meta = await page.evaluate(() => ({
      imgs: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.currentSrc || i.src),
      vid: document.querySelector('video') ? document.querySelector('video').readyState : 'none',
      form: !!document.getElementById('estimate-form'),
    }));
    out.push({ path, name, errs, ...meta });
    await page.close();
  }
  await b.close();
  console.log(JSON.stringify(out, null, 1));
})();
