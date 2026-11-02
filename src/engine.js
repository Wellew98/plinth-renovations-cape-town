/* ====== embedded assembly engine ====== */
/* ===========================================================================
   One-Click Blueprint — Assembly Engine
   Pure functions: inputs + GPT content JSON -> { "path.html": "<html>...", ... }
   No DOM here so it can be unit-tested in node and reused in the browser wizard.
   =========================================================================== */

(function (root) {
  'use strict';

  // ---------- helpers ----------
  function slugify(s) {
    return String(s).toLowerCase().trim()
      .replace(/['".,/\\()]/g, '')
      .replace(/&/g, ' and ')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function esc(s) { return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function digits(s) { return String(s || '').replace(/[^0-9+]/g, ''); }

  // Minimal, safe markdown -> HTML (headings, bold, lists, paragraphs).
  // The GPT emits simple Markdown; we keep this dependency-free for the engine.
  function md(text) {
    if (text == null) return '';
    if (Array.isArray(text)) text = text.join('\n\n');
    var lines = String(text).split('\n');
    var out = [], i = 0;
    function inline(t) {
      return esc(t)
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>');
    }
    while (i < lines.length) {
      var ln = lines[i];
      if (/^\s*###\s+/.test(ln)) { out.push('<h3>' + inline(ln.replace(/^\s*###\s+/, '')) + '</h3>'); i++; continue; }
      if (/^\s*##\s+/.test(ln))  { out.push('<h2>' + inline(ln.replace(/^\s*##\s+/, '')) + '</h2>'); i++; continue; }
      if (/^\s*[-*]\s+/.test(ln)) {
        var items = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          items.push('<li>' + inline(lines[i].replace(/^\s*[-*]\s+/, '')) + '</li>'); i++;
        }
        out.push('<ul>' + items.join('') + '</ul>'); continue;
      }
      if (/^\s*$/.test(ln)) { i++; continue; }
      // gather paragraph
      var para = [ln]; i++;
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^\s*(#{2,3}|[-*])\s+/.test(lines[i])) { para.push(lines[i]); i++; }
      out.push('<p>' + inline(para.join(' ')) + '</p>');
    }
    return out.join('\n');
  }

  // ---------- marker conversion ----------
  // [PHONE] [LOCATION] [CTA:estimate] [CTA:call] [CTA:book]
  function markers(html, ctx, locationName) {
    var phoneLink = '<a class="wc-phone" href="tel:' + esc(ctx.phoneE164) + '">' + esc(ctx.phoneDisplay) + '</a>';
    return html
      .replace(/\[PHONE\]/g, phoneLink)
      .replace(/\[LOCATION\]/g, esc(locationName || ctx.primaryLocation))
      .replace(/\[CTA:estimate\]/g, '<p><a class="btn" href="estimate.html">Get a Free Estimate</a></p>')
      .replace(/\[CTA:call\]/g, '<p><a class="btn wc-phone" href="tel:' + esc(ctx.phoneE164) + '">Call ' + esc(ctx.phoneDisplay) + '</a></p>')
      .replace(/\[CTA:book\]/g, '<p><a class="btn" href="estimate.html">Book Now</a></p>');
  }

  function prose(text, ctx, locationName) { return markers(md(text), ctx, locationName); }

  // ---------- shared chrome ----------
  function header(ctx) {
    var svcItems = ctx.services.map(function (s) {
      return '<li><a href="' + s.slug + '.html">' + esc(s.name) + '</a></li>';
    }).join('');
    return [
'<header class="site-header"><nav class="nav">',
'<a class="nav__logo" href="index.html">' + (ctx.logoUrl ? '<img src="' + esc(ctx.logoUrl) + '" alt="' + esc(ctx.businessName) + ' logo">' : '<strong>' + esc(ctx.businessName) + '</strong>') + '</a>',
'<button class="nav__toggle" aria-label="Menu" onclick="document.getElementById(\'navlinks\').classList.toggle(\'open\')">&#9776;</button>',
'<ul class="nav__links" id="navlinks">',
'<li class="has-dropdown"><a href="services.html">Our Services</a><ul class="dropdown">' + svcItems + '</ul></li>',
'<li><a href="service-areas.html">Service Areas</a></li>',
'<li><a href="about.html">About Us</a></li>',
'<li><a href="contact.html">Contact</a></li>',
'<li><a href="estimate.html">Get an Estimate</a></li>',
'<li><a class="nav__call wc-phone" href="tel:' + esc(ctx.phoneE164) + '">' + esc(ctx.phoneDisplay) + '</a></li>',
'</ul></nav></header>'
    ].join('');
  }

  function footer(ctx) {
    var quick = ['about|About Us','services|Our Services','service-areas|Service Areas','contact|Contact','estimate|Get an Estimate','faq|FAQ']
      .map(function (p) { var a = p.split('|'); return '<li><a href="' + a[0] + '.html">' + a[1] + '</a></li>'; }).join('');
    var info = ['privacy-policy|Privacy Policy','terms-conditions|Terms & Conditions','referral-marketing-disclosure|Referral Marketing Disclosure','disclaimer|Disclaimer','accessibility|Accessibility','complaints-policy|Complaints Policy','meet-the-team|Meet the Team','careers|Careers']
      .map(function (p) { var a = p.split('|'); return '<li><a href="' + a[0] + '.html">' + a[1] + '</a></li>'; }).join('');
    return [
'<footer class="site-footer"><div class="wrap"><div class="footer-grid">',
'<div><h4>' + esc(ctx.businessName) + '</h4><p style="color:rgba(255,255,255,.8)">' + esc(ctx.site.footer_about_blurb) + '</p>',
'<p class="footer-disclaimer">' + esc(markers(ctx.site.service_area_disclaimer || '', ctx, ctx.primaryLocation).replace(/<[^>]+>/g,'')) + '</p></div>',
'<div><h4>Quick Links</h4><ul>' + quick + '</ul></div>',
'<div><h4>Information</h4><ul>' + info + '</ul></div>',
'<div><h4>Contact</h4><p style="color:rgba(255,255,255,.8)">Call us at <a class="wc-phone" href="tel:' + esc(ctx.phoneE164) + '">' + esc(ctx.phoneDisplay) + '</a>' +
   (ctx.businessEmail ? '<br>Email: <a href="mailto:' + esc(ctx.businessEmail) + '">' + esc(ctx.businessEmail) + '</a>' : '') + '</p>',
'<p class="footer-disclaimer">' + esc(ctx.site.legal_operator_line || '') + '</p></div>',
'</div><div class="footer-bottom">&copy; ' + ctx.year + ' ' + esc(ctx.businessName) + '. All rights reserved.</div></div></footer>'
    ].join('');
  }

  function doc(ctx, opts) {
    return [
'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">',
'<title>' + esc(opts.title) + '</title>',
'<meta name="description" content="' + esc(opts.desc) + '">',
'<link rel="canonical" href="' + esc(ctx.siteUrl) + '/' + (opts.path || '') + '">',
'<meta name="robots" content="all"><meta name="theme-color" content="' + esc(ctx.brandColor) + '">',
'<link rel="stylesheet" href="assets/style.css">',
'<!-- ' + 'HEAD_SCRIPTS' + ' -->' + (ctx.headScripts || ''),
'</head><body>',
header(ctx),
opts.body,
footer(ctx),
'<scr'+'ipt src="assets/main.js"></scr'+'ipt></body></html>'
    ].join('\n');
  }

  // ---------- reusable blocks ----------
  function linklist(items) {
    return '<ul class="linklist">' + items.map(function (it) {
      return '<li><a href="' + it.slug + '.html">' + esc(it.name) + '</a></li>';
    }).join('') + '</ul>';
  }
  function cards(items, kind) {
    return '<div class="grid grid--3">' + items.map(function (it) {
      return '<div class="card"><h3>' + esc(it.name) + '</h3><p>' + esc(it.teaser || '') + '</p><a href="' + it.slug + '.html">Learn more &rarr;</a></div>';
    }).join('') + '</div>';
  }
  function whyus(items) {
    return '<div class="grid grid--2">' + (items || []).map(function (w) {
      return '<div class="card"><h3>' + esc(w.point) + '</h3><p>' + esc(w.detail) + '</p></div>';
    }).join('') + '</div>';
  }
  function faqBlock(items) {
    return '<div class="faq" style="max-width:820px;margin:28px auto 0">' + (items || []).map(function (f) {
      return '<details><summary>' + esc(f.q) + '</summary><p>' + esc(f.a) + '</p></details>';
    }).join('') + '</div>';
  }
  function ctaBand(ctx, heading, sub) {
    return '<section class="cta-band"><div class="wrap"><h2>' + esc(heading) + '</h2>' +
      '<p>' + esc(sub || '') + '</p><p style="margin-top:20px"><a class="btn btn--lg wc-phone" href="tel:' + esc(ctx.phoneE164) + '">Call ' + esc(ctx.phoneDisplay) + '</a></p>' +
      '<p class="muted" style="color:rgba(255,255,255,.8);margin-top:10px">Free &mdash; no obligations</p></div></section>';
  }
  function leader(ctx, l, locationName) {
    if (!l) l = {};
    var media = ctx.heroImage
      ? '<div class="hero__media"><img src="' + esc(ctx.heroImage) + '" alt="' + esc(ctx.primaryService + ' in ' + (locationName || ctx.primaryLocation)) + '"></div>'
      : '';
    var fallback = ctx.heroImage ? '' : ' style="background:var(--bg-dark)"';
    return '<section class="hero"' + fallback + '>' + media + '<div class="hero__inner">' +
      '<p class="hero__eyebrow">' + esc(markers(l.eyebrow||'', ctx, locationName).replace(/<[^>]+>/g,'')) + '</p>' +
      '<h1>' + esc(markers(l.h1||'', ctx, locationName).replace(/<[^>]+>/g,'')) + '</h1>' +
      '<p>' + esc(markers(l.cta_line||'', ctx, locationName).replace(/<[^>]+>/g,'')) + '</p>' +
      '<div class="hero__cta"><a class="btn btn--lg" href="estimate.html">Get a Free Estimate</a>' +
      '<a class="btn btn--ghost btn--lg wc-phone" href="tel:' + esc(ctx.phoneE164) + '" style="color:#fff;border-color:#fff">' + esc(ctx.phoneDisplay) + '</a></div>' +
      '</div></section>';
  }
  function imageBlock(src, alt) {
    return '<section class="section" style="padding:18px 0"><div class="wrap">' +
      '<img src="' + esc(src) + '" alt="' + esc(alt) + '" loading="lazy" style="width:100%;border-radius:var(--radius)"></div></section>';
  }
  // interleave the shared image pool between content sections (every 2nd), rotating
  // a global index across all main pages so the pool spreads evenly site-wide.
  function withImages(sections, ctx, altBase) {
    var pool = ctx.contentImages || [];
    if (!pool.length) return sections.join('\n');
    var out = [], every = 2;
    for (var i = 0; i < sections.length; i++) {
      out.push(sections[i]);
      if ((i + 1) % every === 0 && i < sections.length - 1) {
        var src = pool[ctx._imgIdx % pool.length]; ctx._imgIdx++;
        out.push(imageBlock(src, altBase || ctx.businessName));
      }
    }
    return out.join('\n');
  }

  // ---------- pages ----------
  function pageHome(ctx) {
    var h = ctx.content.home || {};
    var body = leader(ctx, h.leader) + '\n' + withImages([
      '<section class="section"><div class="wrap"><h2>' + esc(h.intro_heading||'') + '</h2><div class="section__lead">' + prose(h.intro_body, ctx) + '</div></div></section>',
      '<section class="section section--alt"><div class="wrap"><h2>' + esc(h.about_heading||'') + '</h2>' + prose(h.about_body, ctx) + '<a class="btn" href="about.html">More about us</a></div></section>',
      '<section class="section"><div class="wrap"><h2>Our Services</h2><p class="section__lead">' + esc(h.services_intro||'') + '</p><div style="margin-top:28px">' + cards(ctx.services) + '</div><p style="margin-top:24px"><a class="btn btn--ghost" href="services.html">View all services</a></p></div></section>',
      '<section class="section section--alt"><div class="wrap"><h2>Where We Serve You</h2>' + prose(h.areas_body, ctx) + '<a class="btn" href="service-areas.html">See all service areas</a></div></section>',
      '<section class="section"><div class="wrap"><h2>Why Choose ' + esc(ctx.businessName) + '?</h2><div style="margin-top:24px">' + whyus(h.whyus) + '</div></div></section>',
      '<section class="section section--alt"><div class="wrap"><h2 class="center">What People Ask Us</h2>' + faqBlock(h.faq) + '</div></section>',
      ctaBand(ctx, 'Contact Us Today for a Free Estimate', h.cta_subtext)
    ], ctx, ctx.businessName + ' ' + ctx.primaryService);
    return doc(ctx, { title: h.title_tag || ctx.businessName, desc: h.meta_description || '', path: '', body: body });
  }

  function pageService(ctx, s) {
    var subs = (s.subitems||[]).map(function (x){ return '<div class="card"><h3>'+esc(x.name)+'</h3><p>'+esc(x.desc)+'</p></div>'; }).join('');
    var cost = s.cost && s.cost.rows ? ('<section class="section section--alt"><div class="wrap"><h2>'+esc(s.cost.heading||'Pricing')+'</h2><div class="table-wrap" style="margin-top:18px"><table><thead><tr>'+
        (s.cost.columns||[]).map(function(c){return '<th>'+esc(c)+'</th>';}).join('')+'</tr></thead><tbody>'+
        (s.cost.rows||[]).map(function(r){return '<tr>'+r.map(function(c){return '<td>'+esc(c)+'</td>';}).join('')+'</tr>';}).join('')+
        '</tbody></table></div>'+(s.cost.note?'<p style="margin-top:16px">'+esc(s.cost.note)+'</p>':'')+'</div></section>') : '';
    var process = s.process && s.process.steps ? ('<section class="section"><div class="wrap"><h2>'+esc(s.process.heading||'Our Process')+'</h2><div class="grid grid--2" style="margin-top:24px">'+
        s.process.steps.map(function(st){return '<div class="card"><h3>'+esc(st.step)+'</h3><p>'+esc(st.detail)+'</p></div>';}).join('')+'</div></div></section>') : '';
    var body = leader(ctx, s.leader) + '\n' + withImages([
      '<section class="section"><div class="wrap"><h2>' + esc(s.intro_heading||'') + '</h2><div class="section__lead">' + prose(s.intro_body, ctx) + '</div></div></section>',
      '<section class="section section--alt"><div class="wrap"><h2 class="center">' + esc(ctx.businessName) + ' Is Proud to Serve ' + esc(ctx.primaryRegion) + '</h2><div style="margin-top:24px">' + linklist(ctx.areas) + '</div></div></section>',
      (s.detail_heading ? '<section class="section"><div class="wrap"><h2>'+esc(s.detail_heading)+'</h2><p class="section__lead">'+esc(s.detail_intro||'')+'</p><div class="grid grid--2" style="margin-top:24px">'+subs+'</div></div></section>' : ''),
      cost,
      '<section class="section"><div class="wrap"><h2>Why Choose Us for ' + esc(s.name) + '?</h2><div style="margin-top:24px">' + whyus(s.whyus) + '</div></div></section>',
      ctaBand(ctx, 'Contact Us Today for a Free Estimate', s.cta_subtext),
      process,
      '<section class="section section--alt"><div class="wrap"><h2 class="center">Our Services in ' + esc(ctx.primaryLocation) + '</h2><div style="margin-top:24px">' + linklist(ctx.services) + '</div></div></section>'
    ].filter(Boolean), ctx, s.name);
    return doc(ctx, { title: s.title_tag || s.name, desc: s.meta_description || '', path: s.slug, body: body });
  }

  function pageArea(ctx, a) {
    var siblings = ctx.areas.filter(function (x) { return x.slug !== a.slug; });
    var sibBlock = '<ul class="linklist">' + siblings.map(function (x){ return '<li><a href="'+x.slug+'.html">'+esc(x.name)+'</a></li>'; }).join('') +
       '<li><a href="service-areas.html"><strong>View all service areas &rarr;</strong></a></li></ul>';
    var body = leader(ctx, a.leader, a.name) + '\n' + withImages([
      '<section class="section"><div class="wrap"><h2>' + esc(a.intro_heading||'') + '</h2><div class="section__lead">' + prose(a.intro_body, ctx, a.name) + '</div></div></section>',
      '<section class="section section--alt"><div class="wrap"><h2 class="center">Our Services in ' + esc(a.name) + '</h2><div style="margin-top:24px">' + linklist(ctx.services) + '</div></div></section>',
      '<section class="section"><div class="wrap"><h2>Why ' + esc(a.name) + ' Chooses ' + esc(ctx.businessName) + '</h2><div style="margin-top:24px">' + whyus(a.whyus) + '</div></div></section>',
      ctaBand(ctx, 'Get Your Free Estimate in ' + a.name, a.cta_subtext),
      '<section class="section section--alt"><div class="wrap"><h2 class="center">Nearby Areas We Serve</h2><div style="margin-top:24px">' + sibBlock + '</div></div></section>'
    ], ctx, ctx.primaryService + ' in ' + a.name);
    return doc(ctx, { title: a.title_tag || a.name, desc: a.meta_description || '', path: a.slug, body: body });
  }

  function pageEstimate(ctx) {
    var opts = ctx.services.map(function (s){ return '<option>'+esc(s.name)+'</option>'; }).join('') + '<option>Not sure / other</option>';
    var body = '<section class="section"><div class="wrap split"><div><h1>Get Your Free Estimate</h1><p class="section__lead">' + esc((ctx.content.site&&ctx.content.site.contact_copy)||'Request your free, no-obligation estimate today.') + '</p>' +
      '<p style="margin-top:18px">Prefer to talk now? Call <a class="wc-phone" href="tel:'+esc(ctx.phoneE164)+'"><strong>'+esc(ctx.phoneDisplay)+'</strong></a>.</p><p class="muted">Free &mdash; no obligations.</p></div>' +
      '<div class="form-card"><form action="' + esc(ctx.formActionUrl || '#') + '" method="POST">' +
      '<div class="form-row"><div class="field"><label>First Name</label><input type="text" name="first_name" required></div><div class="field"><label>Last Name</label><input type="text" name="last_name"></div></div>' +
      '<div class="form-row"><div class="field"><label>Email</label><input type="email" name="email" required></div><div class="field"><label>Phone</label><input type="tel" name="phone" required></div></div>' +
      '<div class="field"><label>Which service?</label><select name="service">' + opts + '</select></div>' +
      '<div class="field"><label>Message</label><textarea name="message"></textarea></div>' +
      '<button class="btn btn--lg" type="submit" style="width:100%">Request My Free Estimate</button></form></div></div></section>';
    return doc(ctx, { title: 'Get an Estimate | ' + ctx.businessName, desc: 'Request a free estimate from ' + ctx.businessName, path: 'estimate', body: body });
  }

  function pageGeneric(ctx, title, slug, inner) {
    var body = '<section class="section"><div class="wrap"><h1>' + esc(title) + '</h1><div class="section__lead" style="margin-top:18px">' + (inner || '<p>Content coming soon.</p>') + '</div></div></section>';
    return doc(ctx, { title: title + ' | ' + ctx.businessName, desc: title + ' — ' + ctx.businessName, path: slug, body: body });
  }

  // services index + service-areas index
  function pageServicesIndex(ctx) {
    var inner = '<p>' + esc((ctx.content.home&&ctx.content.home.services_intro)||'') + '</p>' + cards(ctx.services);
    return pageGeneric(ctx, 'Our Services', 'services', inner);
  }
  function pageAreasIndex(ctx) {
    var inner = '<p>We proudly serve ' + esc(ctx.primaryRegion) + '.</p>' + linklist(ctx.areas);
    return pageGeneric(ctx, 'Service Areas', 'service-areas', inner);
  }

  // ---------- top-level assemble ----------
  function assemble(inputs, content) {
    var ctx = {
      businessName: inputs.businessName,
      phoneDisplay: inputs.phoneDisplay,
      phoneE164: digits(inputs.phoneE164 || inputs.phoneDisplay),
      siteUrl: (inputs.siteUrl || '').replace(/\/$/, ''),
      logoUrl: inputs.logoUrl || '',
      businessEmail: inputs.businessEmail || '',
      brandColor: inputs.brandColor || '#1a56db',
      primaryService: inputs.primaryService,
      primaryLocation: inputs.primaryLocation,
      primaryRegion: inputs.primaryRegion || inputs.primaryLocation,
      formActionUrl: inputs.formActionUrl || '',
      headScripts: inputs.whatConvertsScript || '',
      heroImage: inputs.heroImage || '',
      contentImages: inputs.contentImages || [],
      _imgIdx: 0,
      year: new Date().getFullYear(),
      content: content,
      site: content.site || {}
    };
    var primarySlug = slugify(inputs.primaryService);
    ctx.services = (content.services || []).map(function (s) { return Object.assign({}, s, { slug: slugify(s.name) }); });
    ctx.areas = (content.areas || []).map(function (a) { return Object.assign({}, a, { slug: primarySlug + '-in-' + slugify(a.name) }); });

    var files = {};
    files['index.html'] = pageHome(ctx);
    files['estimate.html'] = pageEstimate(ctx);
    files['services.html'] = pageServicesIndex(ctx);
    files['service-areas.html'] = pageAreasIndex(ctx);
    ctx.services.forEach(function (s) { files[s.slug + '.html'] = pageService(ctx, s); });
    ctx.areas.forEach(function (a) { files[a.slug + '.html'] = pageArea(ctx, a); });
    // core/legal stubs (kept for trust + footer links)
    [['About Us','about'],['Contact','contact'],['FAQ','faq'],['Meet the Team','meet-the-team'],['Careers','careers'],
     ['Privacy Policy','privacy-policy'],['Terms & Conditions','terms-conditions'],['Referral Marketing Disclosure','referral-marketing-disclosure'],
     ['Disclaimer','disclaimer'],['Accessibility','accessibility'],['Complaints Policy','complaints-policy'],['Thank You','thank-you']]
      .forEach(function (p) { files[p[1] + '.html'] = pageGeneric(ctx, p[0], p[1]); });

    return { files: files, ctx: ctx };
  }

  var API = { slugify: slugify, assemble: assemble, md: md };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  root.BlueprintEngine = API;
})(typeof window !== 'undefined' ? window : this);

/* ====== embedded site CSS (written into the ZIP) ====== */
var SITE_CSS = "/* =========================================================\n   Microsite Base \u2014 shared styles\n   Plain CSS, no build step. Edit freely.\n   Brand color and font are driven by CSS variables below so\n   a single change re-themes the whole site.\n   ========================================================= */\n\n:root {\n  --brand:        #1a56db;   /* {{BRAND_COLOR}} primary brand / links / buttons */\n  --brand-dark:   #1442ad;   /* darker shade for hovers */\n  --ink:          #15212e;   /* body text */\n  --ink-soft:     #4a5a6a;   /* secondary text */\n  --line:         #e3e8ee;   /* hairlines / borders */\n  --bg:           #ffffff;\n  --bg-alt:       #f6f8fa;   /* alternating section background */\n  --bg-dark:      #15212e;   /* footer / dark band */\n  --max:          1160px;    /* content max width */\n  --radius:       10px;\n  --font-head: Georgia, 'Times New Roman', serif;\n  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;\n}\n\n* { box-sizing: border-box; margin: 0; padding: 0; }\n\nhtml { scroll-behavior: smooth; }\n\nbody {\n  font-family: var(--font-body);\n  color: var(--ink);\n  line-height: 1.65;\n  background: var(--bg);\n  -webkit-font-smoothing: antialiased;\n}\n\n.wrap { max-width: var(--max); margin: 0 auto; padding: 0 20px; }\n\nh1, h2, h3, h4 { font-family: var(--font-head); line-height: 1.2; color: var(--ink); }\nh1 { font-size: clamp(2rem, 5vw, 3.1rem); }\nh2 { font-size: clamp(1.6rem, 3.5vw, 2.3rem); margin-bottom: .6em; }\nh3 { font-size: 1.25rem; margin-bottom: .35em; }\np  { margin-bottom: 1rem; color: var(--ink-soft); }\na  { color: var(--brand); text-decoration: none; }\na:hover { text-decoration: underline; }\n\nimg { max-width: 100%; height: auto; display: block; }\n\n/* ---------- buttons ---------- */\n.btn {\n  display: inline-block;\n  background: var(--brand);\n  color: #fff;\n  padding: 14px 28px;\n  border-radius: var(--radius);\n  font-weight: 600;\n  font-family: var(--font-body);\n  border: none;\n  cursor: pointer;\n  transition: background .15s ease;\n}\n.btn:hover { background: var(--brand-dark); text-decoration: none; }\n.btn--ghost { background: transparent; color: var(--brand); border: 2px solid var(--brand); }\n.btn--ghost:hover { background: var(--brand); color: #fff; }\n.btn--lg { padding: 18px 38px; font-size: 1.05rem; }\n\n.muted { color: var(--ink-soft); font-size: .9rem; }\n\n/* ---------- header / nav ---------- */\n.site-header {\n  position: sticky; top: 0; z-index: 50;\n  background: var(--bg);\n  border-bottom: 1px solid var(--line);\n}\n.nav {\n  display: flex; align-items: center; justify-content: space-between;\n  gap: 20px; padding: 12px 20px; max-width: var(--max); margin: 0 auto;\n}\n.nav__logo img { max-height: 46px; width: auto; }\n.nav__links { display: flex; align-items: center; gap: 22px; list-style: none; }\n.nav__links a { color: var(--ink); font-weight: 500; font-size: .97rem; }\n.nav__links a:hover { color: var(--brand); text-decoration: none; }\n\n/* dropdown for services */\n.has-dropdown { position: relative; }\n.dropdown {\n  display: none; position: absolute; top: 100%; left: 0;\n  background: #fff; border: 1px solid var(--line); border-radius: var(--radius);\n  min-width: 250px; padding: 8px 0; box-shadow: 0 12px 30px rgba(0,0,0,.08);\n}\n/* invisible bridge: fills the gap between the menu item and the dropdown\n   so hover isn't lost when the mouse travels down into the submenu */\n.has-dropdown::after {\n  content: \"\"; position: absolute; top: 100%; left: 0; right: 0; height: 14px; display: none;\n}\n.has-dropdown:hover::after { display: block; }\n.has-dropdown:hover .dropdown { display: block; }\n.dropdown li { list-style: none; }\n.dropdown a { display: block; padding: 9px 18px; font-size: .92rem; }\n.dropdown a:hover { background: var(--bg-alt); }\n\n.nav__call {\n  background: var(--brand); color: #fff !important;\n  padding: 10px 18px; border-radius: var(--radius); font-weight: 600;\n}\n.nav__call:hover { background: var(--brand-dark); text-decoration: none; }\n\n/* mobile nav toggle */\n.nav__toggle { display: none; background: none; border: 0; font-size: 1.6rem; cursor: pointer; color: var(--ink); }\n@media (max-width: 900px) {\n  .nav__links { display: none; position: absolute; top: 100%; left: 0; right: 0;\n    flex-direction: column; align-items: flex-start; gap: 0;\n    background: #fff; border-bottom: 1px solid var(--line); padding: 10px 20px; }\n  .nav__links.open { display: flex; }\n  .nav__links li { width: 100%; padding: 8px 0; }\n  .dropdown { position: static; display: block; box-shadow: none; border: 0; padding: 4px 0 4px 14px; min-width: 0; }\n  .nav__toggle { display: block; }\n}\n\n/* ---------- hero ---------- */\n.hero { position: relative; color: #fff; }\n.hero__media { position: absolute; inset: 0; z-index: 0; }\n.hero__media img { width: 100%; height: 100%; object-fit: cover; }\n.hero::after { content: \"\"; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(21,33,46,.55), rgba(21,33,46,.78)); z-index: 1; }\n.hero__inner { position: relative; z-index: 2; max-width: var(--max); margin: 0 auto; padding: 90px 20px; }\n.hero__eyebrow { text-transform: uppercase; letter-spacing: .08em; font-size: .85rem; font-weight: 600; opacity: .9; }\n.hero h1 { color: #fff; margin: 10px 0 16px; max-width: 18ch; }\n.hero p { color: rgba(255,255,255,.9); font-size: 1.15rem; max-width: 46ch; }\n.hero__cta { margin-top: 26px; display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }\n\n/* ---------- sections ---------- */\n.section { padding: 64px 0; }\n.section--alt { background: var(--bg-alt); }\n.section--dark { background: var(--bg-dark); color: #fff; }\n.section--dark h2, .section--dark h3 { color: #fff; }\n.section--dark p { color: rgba(255,255,255,.82); }\n.section__lead { max-width: 65ch; }\n.center { text-align: center; }\n.center .section__lead { margin: 0 auto; }\n\n/* two-column split */\n.split { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }\n@media (max-width: 800px) { .split { grid-template-columns: 1fr; gap: 28px; } }\n\n/* feature / why-us grid */\n.grid { display: grid; gap: 24px; }\n.grid--3 { grid-template-columns: repeat(3, 1fr); }\n.grid--4 { grid-template-columns: repeat(4, 1fr); }\n.grid--2 { grid-template-columns: repeat(2, 1fr); }\n@media (max-width: 900px) { .grid--3, .grid--4 { grid-template-columns: repeat(2, 1fr); } }\n@media (max-width: 600px) { .grid--2, .grid--3, .grid--4 { grid-template-columns: 1fr; } }\n\n.card {\n  background: #fff; border: 1px solid var(--line); border-radius: var(--radius);\n  padding: 26px;\n}\n.section--alt .card { background: #fff; }\n.card h3 { margin-bottom: .4em; }\n.card p:last-child { margin-bottom: 0; }\n\n/* service / area link list */\n.linklist { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; list-style: none; }\n@media (max-width: 800px) { .linklist { grid-template-columns: repeat(2, 1fr); } }\n@media (max-width: 500px) { .linklist { grid-template-columns: 1fr; } }\n.linklist a {\n  display: block; padding: 14px 18px; border: 1px solid var(--line);\n  border-radius: var(--radius); background: #fff; color: var(--ink); font-weight: 600;\n}\n.linklist a:hover { border-color: var(--brand); color: var(--brand); text-decoration: none; }\n\n/* cost table */\n.table-wrap { overflow-x: auto; }\ntable { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }\nth, td { text-align: left; padding: 14px 18px; border-bottom: 1px solid var(--line); font-size: .96rem; }\nth { background: var(--bg-alt); font-family: var(--font-body); font-weight: 700; color: var(--ink); }\ntr:last-child td { border-bottom: 0; }\n\n/* FAQ */\n.faq details { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 4px 20px; margin-bottom: 12px; }\n.faq summary { cursor: pointer; font-weight: 600; font-family: var(--font-head); font-size: 1.1rem; padding: 16px 0; list-style: none; }\n.faq summary::-webkit-details-marker { display: none; }\n.faq summary::after { content: \"+\"; float: right; color: var(--brand); font-size: 1.4rem; line-height: 1; }\n.faq details[open] summary::after { content: \"\u2013\"; }\n.faq details > p { padding-bottom: 16px; margin-bottom: 0; }\n\n/* CTA band */\n.cta-band { background: var(--brand); color: #fff; text-align: center; padding: 56px 20px; }\n.cta-band h2 { color: #fff; }\n.cta-band p { color: rgba(255,255,255,.9); }\n.cta-band .btn { background: #fff; color: var(--brand); }\n.cta-band .btn:hover { background: #f0f3f7; }\n\n/* ---------- estimate / contact form ---------- */\n.form-card { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 30px; }\n.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }\n@media (max-width: 600px) { .form-row { grid-template-columns: 1fr; } }\n.field { margin-bottom: 16px; }\n.field label { display: block; font-weight: 600; font-size: .9rem; margin-bottom: 6px; color: var(--ink); }\n.field input, .field textarea, .field select {\n  width: 100%; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px;\n  font-family: var(--font-body); font-size: 1rem;\n}\n.field textarea { min-height: 130px; resize: vertical; }\n\n/* ---------- footer ---------- */\n.site-footer { background: var(--bg-dark); color: rgba(255,255,255,.8); padding: 56px 0 28px; }\n.site-footer h4 { color: #fff; margin-bottom: 14px; font-family: var(--font-body); font-size: 1rem; letter-spacing: .02em; }\n.footer-grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 36px; }\n@media (max-width: 800px) { .footer-grid { grid-template-columns: 1fr 1fr; gap: 28px; } }\n@media (max-width: 480px) { .footer-grid { grid-template-columns: 1fr; } }\n.site-footer ul { list-style: none; }\n.site-footer li { margin-bottom: 9px; }\n.site-footer a { color: rgba(255,255,255,.8); font-size: .93rem; }\n.site-footer a:hover { color: #fff; }\n.footer-bottom { border-top: 1px solid rgba(255,255,255,.15); margin-top: 40px; padding-top: 20px; font-size: .85rem; color: rgba(255,255,255,.55); }\n.footer-disclaimer { font-size: .82rem; color: rgba(255,255,255,.55); margin-top: 10px; line-height: 1.5; }\n\n/* phone link \u2014 class is a stable hook for WhatConverts dynamic number insertion */\n.wc-phone { font-weight: 700; }\n";
var SITE_JS = "document.addEventListener('DOMContentLoaded',function(){var l=document.getElementById('navlinks');if(l){l.addEventListener('click',function(e){if(e.target.tagName==='A'&&innerWidth<=900)l.classList.remove('open')})}});";


module.exports.SITE_CSS = SITE_CSS;
module.exports.SITE_JS = SITE_JS;
