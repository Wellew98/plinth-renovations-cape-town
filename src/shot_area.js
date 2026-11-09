const p = require('puppeteer-core');

(async () => {
  const b = await p.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: 'new',
    args: ['--no-sandbox'],
  });
  const pg = await b.newPage();
  const url = 'https://plinthrenovations.co.za/home-renovations-in-bellville?v=' + Date.now();
  await pg.setViewport({ width: 1440, height: 900 });
  await pg.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  await pg.screenshot({ path: '../shots/area-bellville-desktop.png', fullPage: false });
  await pg.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await pg.reload({ waitUntil: 'networkidle2' });
  await pg.screenshot({ path: '../shots/area-bellville-mobile.png', fullPage: false });
  console.log('ok');
  await b.close();
})();
