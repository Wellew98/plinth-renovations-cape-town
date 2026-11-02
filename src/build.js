// Runs the Rank Expand Academy builder engine against the Plinth seed content.
// Output is byte-for-byte what the builder's wizard would emit for the same
// inputs, written to ../site-output instead of a ZIP.
const fs = require('fs');
const path = require('path');
const engine = require('./engine.js');

const SRC = __dirname;
const OUT = path.join(SRC, '..', 'site-output');

const part1 = JSON.parse(fs.readFileSync(path.join(SRC, 'content-part1.json'), 'utf8'));
const part2 = JSON.parse(fs.readFileSync(path.join(SRC, 'content-part2.json'), 'utf8'));
const part3 = JSON.parse(fs.readFileSync(path.join(SRC, 'content-part3.json'), 'utf8'));

const content = {
  site: part1.site,
  home: part1.home,
  services: [...part2.services, ...part3.services],
  areas: part1.areas,
};

// --- validation the wizard would do, plus a few we care about ---
const errors = [];
if (!content.home) errors.push('missing home');
if (!Array.isArray(content.services)) errors.push('missing services');
if (!Array.isArray(content.areas)) errors.push('missing areas');
if (content.services.length < 1) errors.push('no services');
if (content.areas.length < 1) errors.push('no areas');

const slugs = new Set();
for (const s of content.services) {
  const sl = engine.slugify(s.name);
  if (slugs.has(sl)) errors.push('duplicate service slug: ' + sl);
  slugs.add(sl);
  for (const f of ['title_tag', 'meta_description', 'leader', 'intro_body']) {
    if (!s[f]) errors.push(`service "${s.name}" missing ${f}`);
  }
  if (s.title_tag && s.title_tag.length > 65) errors.push(`title too long: ${s.title_tag}`);
  if (s.meta_description && s.meta_description.length > 165) errors.push(`meta too long: ${s.name}`);
}
const areaSlugs = new Set();
for (const a of content.areas) {
  const sl = engine.slugify(a.name);
  if (areaSlugs.has(sl)) errors.push('duplicate area slug: ' + sl);
  areaSlugs.add(sl);
  for (const f of ['title_tag', 'meta_description', 'leader', 'intro_body']) {
    if (!a[f]) errors.push(`area "${a.name}" missing ${f}`);
  }
}
if (content.home.title_tag.length > 65) errors.push('home title too long: ' + content.home.title_tag);
if (content.home.meta_description.length > 165) errors.push('home meta too long');

if (errors.length) {
  console.error('CONTENT ERRORS:\n- ' + errors.join('\n- '));
  process.exit(1);
}

const S = {
  businessName: 'Plinth Renovations',
  phoneDisplay: '066 150 5770',
  phoneE164: '+27661505770',
  businessEmail: '',
  siteUrl: 'https://plinth-renovations-cape-town.pages.dev',
  brandColor: '#b8772a',
  logoUrl: '',
  primaryService: 'Home Renovations',
  primaryLocation: 'Cape Town',
  primaryRegion: 'Cape Town',
  services: content.services.map((s) => s.name),
  areas: content.areas.map((a) => a.name),
  formActionUrl: '',
  whatConvertsScript: '',
  heroImage: 'assets/images/hero.jpg',
  contentImages: Array.from({ length: 6 }, (_, i) => `assets/images/img-${i + 1}.jpg`),
};

const result = engine.assemble(S, content);
const files = result.files;

// --- theme ---
// The builder takes one brand colour; the rest of Plinth's palette and type is
// applied to its stylesheet here rather than by rewriting the CSS by hand.
let css = engine.SITE_CSS;
css = css.replace('--brand:        #1a56db', '--brand:        ' + S.brandColor);
css = css.replace('--brand-dark:   #1442ad', '--brand-dark:   #8f5a1f');
css = css.replace('--bg-dark:      #15212e', '--bg-dark:      #0d0d0c');
css = css.replace("--font-head: Georgia, 'Times New Roman', serif;", "--font-head: 'Fraunces', Georgia, 'Times New Roman', serif;");
css = css.replace("--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;", "--font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;");

// --- write ---
// OneDrive keeps a handle on the output directory, so recreate its contents
// rather than removing the directory itself.
fs.mkdirSync(path.join(OUT, 'assets', 'images'), { recursive: true });
for (const f of fs.readdirSync(OUT)) {
  const p = path.join(OUT, f);
  if (f.endsWith('.html') || ['sitemap.xml', 'robots.txt', '_headers', '_redirects'].includes(f)) {
    try { fs.unlinkSync(p); } catch (e) { /* rewritten below */ }
  }
}

for (const [name, html] of Object.entries(files)) {
  fs.writeFileSync(path.join(OUT, name), html, 'utf8');
}
fs.writeFileSync(path.join(OUT, 'assets', 'style.css'), css, 'utf8');
fs.writeFileSync(path.join(OUT, 'assets', 'main.js'), engine.SITE_JS, 'utf8');
fs.writeFileSync(path.join(SRC, 'content.json'), JSON.stringify(content, null, 2), 'utf8');
fs.writeFileSync(path.join(SRC, 'site-inputs.json'), JSON.stringify(S, null, 2), 'utf8');

console.log('pages generated:', Object.keys(files).length);
console.log(Object.keys(files).sort().join('\n'));
