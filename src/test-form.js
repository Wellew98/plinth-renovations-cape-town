// Proves the estimate form builds a correct WhatsApp handoff.
const p = require('puppeteer-core');
(async () => {
  const b = await p.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    args: ['--no-sandbox'],
  });
  const page = await b.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.evaluateOnNewDocument(() => {
    window.__opened = [];
    window.open = (u) => { window.__opened.push(u); return null; };
  });
  await page.goto('http://127.0.0.1:8100/estimate', { waitUntil: 'networkidle2' });

  await page.type('#name', 'Thandi Mokoena');
  await page.type('#phone', '082 555 0143');
  await page.type('#email', 'thandi@example.co.za');
  await page.type('#suburb', 'Durbanville');
  await page.select('#service', 'Waterproofing');
  await page.type('#details', 'Flat roof leaking above the braai room after the winter rain.');
  await page.click('button[type=submit]');
  await new Promise((r) => setTimeout(r, 400));

  const out = await page.evaluate(() => ({
    opened: window.__opened,
    button: document.querySelector('button[type=submit]').textContent,
    note: document.querySelector('.wa-note').textContent.slice(0, 90),
  }));

  const url = out.opened[0] || '';
  const text = decodeURIComponent((url.split('text=')[1] || '').replace(/\+/g, ' '));
  console.log('opened     :', url.split('?')[0]);
  console.log('button     :', out.button);
  console.log('note       :', out.note.replace(/\s+/g, ' ').trim());
  console.log('--- message ---');
  console.log(text);
  await b.close();
})();
