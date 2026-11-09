const p = require('puppeteer-core');
const path = require('path');

(async () => {
  const b = await p.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--hide-scrollbars'],
  });
  const out = path.resolve(__dirname, '..', 'shots');
  require('fs').mkdirSync(out, { recursive: true });
  const targets = [
    ['/', 'home'],
    ['/waterproofing-cape-town', 'waterproofing'],
    ['/services', 'services'],
    ['/solutions', 'solutions'],
    ['/service-areas', 'areas'],
  ];
  for (const [url, name] of targets) {
    const pg = await b.newPage();
    await pg.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await pg.goto('http://127.0.0.1:8099' + (url === '/' ? '/' : url + '.html'), { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 700));
    await pg.screenshot({ path: path.join(out, `${name}-desktop.png`) });
    await pg.close();

    const m = await b.newPage();
    await m.setViewport({ width: 390, height: 844, deviceScaleFactor: 1, isMobile: true });
    await m.goto('http://127.0.0.1:8099' + (url === '/' ? '/' : url + '.html'), { waitUntil: 'networkidle2' });
    await new Promise(r => setTimeout(r, 500));
    await m.screenshot({ path: path.join(out, `${name}-mobile.png`) });
    await m.close();
    console.log('shot', name);
  }
  await b.close();
})();
