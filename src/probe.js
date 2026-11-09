const p = require('puppeteer-core');
(async () => {
  const b = await p.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new' });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await pg.goto('https://plinthrenovations.co.za/?v=probe' + Date.now(), { waitUntil: 'load' });
  await new Promise(r => setTimeout(r, 2500));
  const out = await pg.evaluate(() => {
    const lead = document.querySelector('.hero p.lead');
    const cs = getComputedStyle(lead);
    const chain = [];
    let el = lead;
    while (el && el !== document.documentElement) {
      const s = getComputedStyle(el);
      chain.push({
        tag: el.tagName + (el.className ? '.' + String(el.className).trim().replace(/\s+/g, '.') : ''),
        z: s.zIndex, pos: s.position, opacity: s.opacity,
        mask: s.maskImage || s.webkitMaskImage || 'none',
        bg: s.backgroundImage === 'none' ? s.backgroundColor : 'IMG',
        filter: s.filter, mix: s.mixBlendMode
      });
      el = el.parentElement;
    }
    const r = lead.getBoundingClientRect();
    return {
      lead: { color: cs.color, shadow: cs.textShadow, opacity: cs.opacity, mask: cs.maskImage || cs.webkitMaskImage, w: r.width, right: r.right },
      chain
    };
  });
  console.log(JSON.stringify(out, null, 1));
  await b.close();
})();
