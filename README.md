# Plinth Renovations Cape Town: lead-generation microsite

Static site generated with the **Rank Expand Academy Microsite Builder** engine
(the same code as `Microsite Builder - Rank Expand Academy.html`), then given a
content, schema and photography pass. No framework, no build step at deploy time.

Live: https://plinth-renovations-cape-town.pages.dev

## How it is built

```
src/
  extract-engine.js   pulls the builder's own assembly engine out of the builder HTML
  engine.js           generated: BlueprintEngine + SITE_CSS + SITE_JS (do not edit)
  content-part*.json  the seed content (site, home, 8 services, 6 areas)
  build.js            merges the seed, validates it, runs assemble(), writes site-output/
  images.py           crops and resizes Plinth's own project photos, builds og-cover + favicon
  finish.py           real pages for the builder's stubs, schema, OG, clean URLs, sitemap
  server.py           local server that mimics Cloudflare Pages clean-URL handling
  check.js            headless Edge: overflow measurement + screenshots at 390 / 1440
  make.sh             node build.js && python images.py && python finish.py

site-output/          the deployable site (Pages output directory)
```

Rebuild everything:

```bash
cd src && bash make.sh
```

## Keyword basis

Measured with DataForSEO (Google Ads search volume, South Africa, location 2710)
on 2026-11-02. 76 keywords, 29 with measurable demand. The head terms:

| Keyword | MSV | CPC |
|---|---:|---:|
| waterproofing cape town | 390 | $5.15 |
| painting contractors cape town | 320 | $3.16 |
| kitchen renovations cape town | 260 | $2.22 |
| waterproofing near me | 260 | $3.80 |
| bathroom renovations cape town | 210 | $1.93 |
| home renovations cape town | 170 | $1.96 |
| waterproofing companies cape town | 110 | $4.85 |
| renovation companies cape town | 110 | $1.62 |
| roof waterproofing cape town | 50 | $7.03 |

Area pages exist only for suburbs with measured demand (Durbanville, Bellville,
Parow, Table View, Brackenfell, Southern Suburbs). Goodwood, Milnerton and the
rest are listed on `/service-areas` without their own page, because they measure
zero. This follows the Boksburg audit rule: no suburb page without volume.

## Content rules

- No invented statistics, reviews, guarantees or timelines.
- Price tables describe what moves the cost; the only rand figures are labelled
  as published Cape Town market ranges, never as a Plinth quote.
- All photography is Plinth's own work, self-hosted, no stock.
- No emojis, no em dashes.

## Deploy

Cloudflare Pages, project `plinth-renovations-cape-town`, no build command,
output directory `site-output`. Pushing to `main` redeploys.

## Open items

- Estimate form has no handler yet (needs an inbox or a form service).
- Real starting prices should replace the market ranges when the owner supplies them.
- Custom domain not chosen; canonicals currently point at the pages.dev host.
