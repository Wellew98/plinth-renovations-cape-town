const p = require('puppeteer-core');
(async () => {
  const tag = process.argv[2] || 'before';
  const b = await p.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new' });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await pg.goto('https://plinthrenovations.co.za/?v=' + Date.now(), { waitUntil: 'load' });
  await pg.evaluate(() => { const v = document.querySelector('.hero-bg'); if (v) { try { v.pause(); v.currentTime = 1.4; } catch (e) {} } });
  await new Promise(r => setTimeout(r, 2500));
  const box = await pg.evaluate(() => {
    const e = document.querySelector('.hero p.lead');
    const r = e.getBoundingClientRect();
    return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
  });
  await pg.evaluate(() => { document.querySelector('.hero .wrap').style.visibility = 'hidden'; });
  await new Promise(r => setTimeout(r, 400));
  await pg.screenshot({ path: '../_shots/bg-' + tag + '.png' });
  console.log(JSON.stringify(box));
  await b.close();
})();
