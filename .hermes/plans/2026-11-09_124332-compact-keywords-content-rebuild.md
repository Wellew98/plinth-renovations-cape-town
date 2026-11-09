# Compact Keywords content rebuild: plinthrenovations.co.za

> **Planning only.** No copy rewritten, no pages renamed, no redirects added.
> Written 2026-11-09. Keyword research **complete**: 297 terms measured for $0.27,
> $0.46 left in the DataForSEO account. Every page decision in this document cites
> a measured row, not an estimate.

**Goal:** rebuild every page on plinthrenovations.co.za around the Compact Keywords
method in the Edward Sturm course, with the site's design untouched.

**Architecture:** hub and spoke. Home and brand pages sell. Hubs list and link every
compact page. Each compact page owns exactly one keyword, matches it in slug, title,
H1 and first sentence, runs 400 to 500 words, and puts the CTA above the fold with
the image below it.

**Stack:** unchanged. `src/content-part1..3.json` feed `build.js`, `images.py` and
`render.py`, which emit static HTML to `site-output/`, deployed to Cloudflare Pages.

---

## 1. The keyword research, 2026-11-09

DataForSEO `keywords_for_keywords`, Google Ads data, location South Africa
(`location_code 2710`), English, three batched requests at $0.09 each.

| Request | Seeds | Ideas returned | Cost |
| --- | --- | --- | --- |
| Services and money terms | 12 | 103 | $0.09 |
| Suburbs | 14 | 21 | $0.09 |
| Problems | 10 | 184 | $0.09 |
| **Total after dedupe** | | **297 unique keywords** | **$0.27** |

Data files: `research/keyword-master.csv` (297 rows, `keyword, volume, cpc,
competition, bucket, service`), raw responses in `research/ideas-*.json`,
write-up in `research/compact-keywords-2026-11-09.md`.

Three honesty notes about this data:

1. Volumes are Google Ads monthly averages for South Africa. They are not Search
   Console impressions, and they are not forecasts.
2. The `bucket` column is my heuristic classification, not DataForSEO's. Some service
   terms sit in `money`. Read the keyword, not the label.
3. Google Ads rounds low volumes to the nearest 10 and reports 0 for many long-tail
   phrases that still get searched. A zero here means "below measurement threshold",
   not "nobody searches this".

### 1.1 Head terms, 110 searches and above

Fourteen terms. These are not compact pages; they are the service page targets and
the reason the site can rank for them at all.

| MSV | CPC | Keyword |
| ---: | ---: | --- |
| 720 | $2.84 | painters cape town |
| 590 | $0.68 | tiling cape town |
| 390 | $5.15 | waterproofing cape town |
| 390 | $5.15 | waterproofing capetown (same term, misspelled) |
| 320 | $3.16 | painting contractors cape town |
| 320 | $3.16 | painting companies in cape town |
| 260 | $2.22 | kitchen renovations cape town |
| 260 | $2.22 | kitchen remodel cape town |
| 210 | $1.93 | bathroom renovations cape town |
| 170 | $4.36 | roof repairs cape town |
| 170 | $1.96 | home renovations cape town |
| 140 | $2.34 | tilehouse cape town (retailer brand, rejected) |
| 110 | $4.85 | waterproofing companies cape town |
| 110 | $2.17 | renovations cape town |

Note the pattern: `waterproofing cape town` carries a $5.15 click. `tiling cape town`
has five times the search volume of `plastering cape town` but an eighth of its click
value. Volume and money are not the same axis, which is the course's central point.

### 1.2 The compact set, 110 searches and below with CPC of $1.50 or better

Thirty-four terms. This is the target profile: small volume, expensive click, buyer
already knows what they want.

| MSV | CPC | Keyword | Disposition |
| ---: | ---: | --- | --- |
| 110 | $4.85 | waterproofing companies cape town | H2 on `/waterproofing-cape-town` |
| 90 | $2.62 | painters durbanville | `/painters-durbanville` |
| 70 | $4.49 | waterproofing contractors cape town | H2 on `/waterproofing-cape-town` |
| 50 | $7.03 | roof waterproofing cape town | `/roof-waterproofing-cape-town` |
| 40 | $8.36 | waterproofing durbanville | `/waterproofing-durbanville` |
| 30 | $3.97 | roof repairs durbanville | section on areas hub |
| 30 | $3.72 | plastering cape town | `/plastering-cape-town` |
| 30 | $3.66 | house painting contractors cape town | H2 on `/painters-cape-town` |
| 30 | $2.67 | painting services cape town | H2 on `/painters-cape-town` |
| 30 | $2.48 | house painters cape town | H2 on `/painters-cape-town` |
| 30 | $2.37 | waterproofing somerset west | `/waterproofing-somerset-west` |
| 30 | $2.14 | ark waterproofing cape town | competitor brand, rejected |
| 30 | $1.30 | durbanville painters | same intent as `painters durbanville` |
| 20 | $7.04 | waterproofing specialists cape town | H2 on `/waterproofing-cape-town` |
| 20 | $5.61 | leaking ceiling repair | `/leaking-ceiling-repair` |
| 20 | $5.53 | paint contractors somerset west | section on areas hub |
| 20 | $5.00 | leaking roof repairs cape town | H2 on `/roof-repairs-cape-town` |
| 20 | $4.58 | stucco italiano cape town | technique, H2 on `/plastering-cape-town` |
| 20 | $3.16 | affordable home renovations cape town | H2 on `/home-renovations-cape-town` |
| 20 | $3.11 | renovation contractors cape town | H2 on `/home-renovations-cape-town` |
| 20 | $2.11 | painters cape town southern suburbs | section on areas hub |
| 20 | $1.84 | waterproofing cape town southern suburbs | `/waterproofing-southern-suburbs` |
| 20 | $1.72 | bathroom renovations durbanville | section on areas hub |
| 20 | $0.86 | kitchen renovations durbanville | section on areas hub |
| 10 | $9.84 | home renovation contractors cape town | H2 on `/home-renovations-cape-town` |
| 10 | $9.24 | paint contractors brackenfell | section on areas hub |
| 10 | $5.62 | torch on waterproofing cape town | H2 on `/roof-waterproofing-cape-town` |
| 10 | $3.38 | tiler durbanville | section on areas hub |
| 10 | $3.02 | roof painters durbanville | section on areas hub |
| 10 | $2.85 | waterproofing brackenfell | section on areas hub |
| 10 | $2.57 | renu painting & waterproofing cape town | competitor brand, rejected |
| 10 | $2.50 | kitchen refurbishment cape town | H2 on `/kitchen-renovations-cape-town` |
| 10 | $1.95 | liquid rubber waterproofing cape town | H2 on `/waterproofing-cape-town` |
| 10 | $1.86 | david matthews painting & waterproofing | competitor brand, rejected |
| 10 | $1.84 | apartment renovations cape town | H2 on `/home-renovations-cape-town` |

### 1.3 Area demand, measured

| Area | Volume | Terms | Decision |
| --- | ---: | ---: | --- |
| Durbanville | 290 | 15 | two pages, it is the strongest suburb by far |
| Somerset West | 100 | 5 | one page |
| Southern Suburbs | 90 | 6 | one page |
| Bellville | 30 | 3 | sections on the areas hub |
| Brackenfell | 20 | 2 | sections on the areas hub |
| Parow | 10 | 1 | one line on the areas hub |
| Table View | 10 | 1 | one line on the areas hub |
| Goodwood | 0 | 1 | brand paragraph, no page |
| Milnerton | 0 | 1 | nothing |

Durbanville splits into two intents that do not compete: `waterproofing durbanville`
at 40 with an $8.36 click, and `painters durbanville` at 90 plus `durbanville
painters` at 30. Two pages, two keywords, no cannibalisation.

Everything below Bellville's 30 does not earn a page. It earns a section on
`/service-areas`, which still captures the phrase and still links to the service page.

### 1.4 The problem cluster, and the finding that reshaped the map

Ninety-eight problem phrases carry volume. Ninety-seven of them are the same topic:

| MSV | CPC | Keyword |
| ---: | ---: | --- |
| 70 | $0.00 | leakage on the ceiling |
| 50 | $0.00 | water leak ceiling |
| 30 | $0.00 | water damage ceiling |
| 20 | $5.61 | leaking ceiling repair |
| 20 | $5.61 | fix leak in ceiling |
| 20 | $5.61 | fixing a leak in the ceiling |
| 20 | $5.61 | leak in ceiling fix |
| 10 | $8.17 | ceiling water leak repair near me |

The ninety-eighth is `leaking roof repairs cape town` at 20 and $5.00.

So the problem axis produces **one** page, not the six I assumed when the plan was
first drafted. `/leaking-ceiling-repair` owns the entire cluster, with the phrasing
variants as H2s. Anyone typing "my ceiling is leaking" gets answered by a page that
says ceiling, not by a waterproofing page.

This is what the course means about using the customer's words. `waterproofing
specialists cape town` is how the trade describes itself. `fix leak in ceiling` is how
a panicking homeowner types at 9pm, and it costs more per click.

### 1.5 Rejected on evidence

| MSV | CPC | Keyword | Why not |
| ---: | ---: | --- | --- |
| 720 | $0.30 | tileafrica kenilworth | retailer brand, no service intent |
| 590 | $0.68 | tiling cape town | keep as a page, but it is a volume term, not a compact one |
| 390 | $5.15 | waterproofing capetown | misspelling of the same term, one page covers both |
| 170 | $0.96 | ceramica cape town | retailer brand |
| 140 | $2.34 | tilehouse cape town | retailer brand |
| 110 | $0.29 | tileafrica cape town | retailer brand |
| 90 | $0.00 | eyelash extensions cape town | no relationship, "cape town" is the shared token |
| 70 | $2.41 | waterproofing centre salt river | competitor brand |
| 30 | $2.65 | cape waterproofing | competitor brand |
| 30 | $0.47 | tiletoria strand | retailer brand |

All of it stays in the CSV so these decisions can be audited later.

### 1.6 Services the data refuses to support yet

| Service | Best measured term | MSV | Verdict |
| --- | --- | ---: | --- |
| Damp proofing | `damp proofing cape town` | 0 | no page |
| Rising damp treatment | `rising damp cape town` | 0 | no page |
| Mould removal | `mould on walls cape town` | 0 | no page |
| Tiling | `tiling cape town` | 590 | page, but a volume play not a money play |

Damp proofing, rising damp and mould all came back at zero across four phrasings each.
That does not mean nobody searches them; it means Google Ads reports nothing for them
in South Africa. They can be sections on `/waterproofing-cape-town`, where the damp
conversation actually happens, but they do not get pages and I will not pretend the
demand is there. If Plinth wants them as pages, the correct next step is one $0.09
request against their own variants, not a guess.

`tiling cape town` at 590 searches and 68 cents is worth a page for traffic and for
the internal link, and it should be described honestly as the weakest commercial term
in the set.

## 2. The page map, decided by data

Fourteen compact pages, three hubs, six brand pages, four legal pages. Twenty-seven
pages total, down from 28, and fourteen of them own a measured keyword.

| URL | Owning keyword | MSV | CPC | Current page | Status |
| --- | --- | ---: | ---: | --- | --- |
| `/` | none, brands and sells | | | `/` | rebuild shorter |
| `/services` | none, hub | | | `/services` | rebuild as hub |
| `/solutions` | none, hub | | | none | new |
| `/service-areas` | none, hub | | | `/service-areas` | rebuild as hub |
| `/our-work` | none | | | `/our-work` | keep |
| `/about` | none | | | `/about` | keep, trim |
| `/estimate` | none, converts | | | `/estimate` | keep |
| `/contact` | none, converts | | | `/contact` | keep |
| `/faq` | none | | | `/faq` | keep, trim |
| `/waterproofing-cape-town` | waterproofing cape town | 390 | $5.15 | `/waterproofing` | rename plus 301 |
| `/roof-waterproofing-cape-town` | roof waterproofing cape town | 50 | $7.03 | none | new |
| `/roof-repairs-cape-town` | roof repairs cape town | 170 | $4.36 | none | new |
| `/painters-cape-town` | painters cape town | 720 | $2.84 | `/painting` | rename plus 301 |
| `/plastering-cape-town` | plastering cape town | 30 | $3.72 | `/plastering` | rename plus 301 |
| `/tiling-cape-town` | tiling cape town | 590 | $0.68 | none | new |
| `/kitchen-renovations-cape-town` | kitchen renovations cape town | 260 | $2.22 | `/kitchens` | rename plus 301 |
| `/bathroom-renovations-cape-town` | bathroom renovations cape town | 210 | $1.93 | `/bathrooms` | rename plus 301 |
| `/home-renovations-cape-town` | home renovations cape town | 170 | $1.96 | `/home-renovations` | rename plus 301 |
| `/waterproofing-durbanville` | waterproofing durbanville | 40 | $8.36 | none | new |
| `/painters-durbanville` | painters durbanville | 90 | $2.62 | none | new |
| `/waterproofing-somerset-west` | waterproofing somerset west | 30 | $2.37 | none | new |
| `/waterproofing-southern-suburbs` | waterproofing southern suburbs | 20 | $1.84 | none | new |
| `/leaking-ceiling-repair` | leaking ceiling repair | 20 | $5.61 | none | new |

**What happens to the six existing area pages.** They are `/home-renovations-in-*`
pages on suburbs, targeting `renovations in Goodwood` and similar. Measured demand for
those phrasings is zero or near it. They do not stay as they are. Each suburb's real
demand is either captured by a compact page above (Durbanville, Somerset West, Southern
Suburbs), by a section on `/service-areas` (Bellville, Brackenfell, Parow, Table View),
or is not there at all (Goodwood, Milnerton). The six old URLs 301 to their closest
survivor so no link equity leaks.

**Pages that retire, and where they go.** Three current pages have no keyword behind them:

| Old page | Disposition | Reason |
| --- | --- | --- |
| `/damp-proofing` | 301 to `/waterproofing-cape-town` | damp proofing, rising damp and mould all measured 0 across four phrasings each |
| `/home-extensions` | 301 to `/home-renovations-cape-town` | `home extensions cape town` measured 10 at low click value; it becomes an H2 on the renovations page |
| six `/home-renovations-in-*` | 301 to their nearest survivor, or to `/service-areas` | the `renovations in <suburb>` phrasing has no measured demand |

The six area redirects: `durbanville` to `/waterproofing-durbanville`, `southern-suburbs`
to `/waterproofing-southern-suburbs`, and `bellville`, `brackenfell`, `parow` and
`table-view` to `/service-areas`, where they live as written sections.

`solutions`, `roof-waterproofing`, `roof-repairs`, `tiling`, `leaking-ceiling-repair`
and `waterproofing-somerset-west` are new. The four legal pages (`privacy`, `terms`,
`accessibility`, `disclaimer`) already exist and stay, two of them gaining the footer
links they never had.

**Keyword assignment rule.** One keyword owns one page, and its synonyms become H2s on
that page rather than new URLs. `waterproofing companies`, `waterproofing contractors`
and `waterproofing specialists` are the same buyer. Three pages would compete with each
other; one page with three H2s captures all three.

## 3. Rules that fall out of the data

1. Waterproofing is the commercial centre of this business. $5.15 and $7.03 clicks
   against $0.68 for tiling. Content effort goes there first.
2. Ceiling leaks deserve their own page because the language is different from
   waterproofing, not because the volume is large.
3. Suburb pages exist only where a suburb's own volume justifies one. Two suburbs do.
4. Retailer and competitor brands never become pages, however large the volume.
5. Zero measured demand means a section, not a page. Not a deletion, a demotion.
6. Tiling gets a page for reach, and is described internally as the weakest commercial
   target so nobody mistakes it for a money page.

## 4. The method, restated as rules we can test

From Wellington's notes, in the order written:

1. A compact keyword is low volume, exact match, bottom of funnel. Rank for many of
   them regardless of volume.
2. Use the exact language the customer uses, not industry language.
3. Slug, page title, meta description, H1 and H2s carry the keyword.
4. Title format `keyword | brand name`, optionally with a call to action.
5. Keyword near the start of the first sentence.
6. 400 to 500 words. Enough to satisfy intent, plus extra for the undecided.
7. Eighty percent of the tailored copy sits at the top. Paragraphs of one to three
   sentences. No superlatives, no sensationalism.
8. H1, short intro, CTA, then the image.
9. Hub pages in the footer so every compact page connects to the rest.
10. Every page two clicks from home at most. No orphans.
11. Image filenames and alt text matter. Alt describes the scene and its relation
    without stuffing the keyword. Re-upload under a new name if reused.
12. Technical: sitemap, robots, GSC with all variations, indexing submitted, same in
    Bing, crawl audit for status codes, indexability, titles, metas, headings.
13. Speed: compressed images, WebP, CDN, cache purged after changes.
14. A blog with outbound links. Deferred, see section 8.

## 5. Current site against the target, measured

| Measure | Current | Target | Verdict |
| --- | --- | --- | --- |
| Pages | 28 | 23, each on one keyword | too broad |
| Average words | 570 | about 450 | inflated |
| Service pages | 856 to 1,030 words | 400 to 500 | double |
| Home | 1,376 words | sells, does not compete | cannibalises |
| Slugs | `/waterproofing`, `/painting` | exact keyword plus city | not exact match |
| Titles | three segments, up to 83 chars | keyword plus brand, no padding | too many segments |
| Crawl depth | every page depth 1 | 2 maximum, through hubs | flat, no hierarchy |
| Internal links | every page links to all 27 others | hubs carry the links | equity diluted |
| Orphans | `accessibility`, `disclaimer` | zero | real defect |
| Area pages | 6 on `renovations in X` | 2, on measured terms | 4 unsupported |
| Images | renamed, alt present | filenames, alt, unique per use | close |
| Speed | 395 KB hero, CDN, immutable cache | fast | already good |
## 6. Tasks

Each task is one session, ends with a verification command, and is committed alone.

### Phase 1, decide the pages with data

| Task | Status | Evidence |
| --- | --- | --- |
| 1. Build the candidate keyword list | done | 12 service seeds, 14 suburb seeds, 10 problem seeds, 297 unique terms after dedupe |
| 2. Measure them | done | three requests at $0.09, $0.27 total, account balance now $0.46 |
| 3. Classify and map to slugs | done | section 2 of this document, every page cites a measured row |
| 4. Pull queries from Search Console | done, no yield | property verified but holds 2 clicks and 7 impressions over three months |

Phase 1 is closed. Nothing is left to buy or guess before writing.

### Phase 2, the layout sheet becomes the source of truth

**Task 5: create `src/seo-layout.json`**

One object per page, mirroring the course's Site SEO Layout tab: keyword, cat1, cat2,
hub, url, title, meta, h1, h2, content notes, done. `render.py` reads it for title, meta
and H1 so the page and the sheet cannot drift apart.

**Task 6: write `src/seo_check.py`**

Reads `site-output/*.html` plus `seo-layout.json` and fails on: keyword missing from
slug, title, H1 or first sentence; word count outside 400 to 500 on a compact page;
title over 60 characters; meta over 155; duplicate titles, metas or H1s; any page more
than two clicks from home; any page with zero inlinks; the same image file on two pages.

Run it against the current site first and watch it fail. A checker that passes before
the work is done is not checking anything.

### Phase 3, rewrite

**Task 7: home.** Cut 1,376 words to about 500 of selling copy. Keep the hero film, the
service grid, the proof. Home stops competing with the service pages.

**Task 8: the fourteen compact pages.** Per page: H1 with the keyword, three-sentence
intro with the keyword near the start, CTA, image below the CTA, H2s carrying the
variants from section 1.2, 400 to 500 words, bullets for scope and process. Work in
order of money: waterproofing, roof waterproofing, roof repairs, leaking ceiling,
painters, kitchen, bathroom, home renovations, plastering, tiling, then the four area
pages.

**Task 9: slugs and 301s, one deploy.** `/waterproofing` to `/waterproofing-cape-town`,
`/painting` to `/painters-cape-town`, plus `/kitchen-renovations`, `/bathroom-renovations`,
`/home-renovations` and the six `/home-renovations-in-*` area pages, each to its closest
survivor. Verify with `curl -sI` against the live host.

**Task 10: hubs.** `/services`, `/solutions` and `/service-areas` become real pages
listing every compact page as cards, with the sub-threshold suburbs written in as
sections. Footer links all three on every page.

**Task 11: orphans and indexability.** Link `accessibility` and `disclaimer` in the
footer, `noindex` on the thank-you page, confirm 404 stays 404.

**Task 12: images.** One image per compact page, descriptive filename, alt text that
describes the scene, never the same file on two pages. No stock, no AI, no borrowed
project claims. Plinth's own photographs only.

### Phase 4, technical and indexation

**Task 13: Search Console and Bing.** Sitemap submission needs your Google account. I
cannot do it from inside your profile. I will prepare the sitemap and the list of URLs
to request indexing for, in priority order, and hand you the exact steps.

**Task 14: crawl audit.** Extend `src/check.js` to report status codes, indexability,
titles, metas, H1 and H2 counts, word counts, crawl depth and inlinks, which is exactly
the audit template's columns.

**Task 15: speed.** WebP with JPEG fallback, immutable caching confirmed, CDN confirmed,
cache purged after deploy.

## 7. Validation, the numbers that decide if this worked

| Check | Pass condition |
| --- | --- |
| Compact pages | every one 400 to 500 words |
| Keyword placement | in slug, title, H1, first sentence, and one H2 |
| Titles | under 60 characters, keyword plus brand |
| Crawl depth | maximum 2 |
| Orphans | zero |
| Internal links | every compact page linked from a hub and one sibling |
| Indexation | 100 percent of intended pages within six weeks |
| Rankings | each targeted keyword tracked weekly from week two |
| Cannibalisation | no two pages targeting the same keyword or its synonyms |

## 8. Risks

- **Slug changes on a live site.** Cheap now, expensive in three months. One deploy,
  with the 301s in the same commit, before Google has crawled anything meaningful.
- **Cutting copy can cut trust.** 400 words of generic text is worse than 900 specific
  words. The real photographs, named materials and actual process stay. Words go,
  substance stays.
- **The tiling page is a traffic page.** It will not pay for itself at $0.68 a click. It
  exists for reach and internal linking, and is labelled that way so it is not
  over-invested in.
- **Zero-volume services look like gaps.** Damp proofing and mould removal are real
  services with no measurable search demand. They live as sections. If you want pages
  for them, one more $0.09 request settles it on their own variants.
- **Design regression.** No design changes in this plan. Copy length changes;
  `styles.css` does not, except the hero veil already shipped.
- **Blog deferred.** The course calls for one. Deferred by decision, not by omission.

## 9. Decisions log

Settled by Wellington on 2026-11-09:

1. **Search Console exists** and is verified, but empty: 2 clicks, 7 impressions, average
   position 2.1 across three months. It becomes a tracking instrument, not a research
   source.
2. **Area pages stay in principle, and are decided by measurement.** The measurement is
   now in and it decided: two suburbs earn pages, four earn sections, two earn nothing.
3. **Blog is deferred.** No new guides in this rebuild. Internal linking leaves room.
4. **The course governs**, provided we target compact keywords. Where the course and
   current copy disagree, the course wins.
5. **WhatsApp is live** on 066 150 5770 and every CTA uses it.
6. **All eight services stay in scope**, but not every service earns a page. Scope means
   the site covers the service, not that each one gets a URL.

Corrections to my own earlier reporting:

- I told you Southern Suburbs measured 70. The exact figure is **90 across 6 terms**.
- I told you the problem terms would produce roughly six solution pages. They produce
  **one**. Ninety-seven of ninety-eight problem phrases are the same topic: a leaking
  ceiling.
- The first draft of this plan carried a volume-measurement-is-unfunded blocker written
  against the old, spent DataForSEO account. That blocker is gone, the new account is
  funded, and the research is done. Nothing in this document is waiting on a purchase.

## 10. The one limitation

The 30 course videos have no subtitle track and I cannot watch video. The method above
comes from the written material: your notes, the landing page template, and all five
template sheets. If a rule exists only in the videos, I do not have it. Name the videos
that matter and I will transcribe those with Whisper rather than guess at all 30.

## 11. What I need from you before writing

1. **Approve the page map in section 2.** Twenty-seven pages, fourteen of them compact:
   four new service pages, four new area pages, one solution page, seven renames with
   301s, and six old area pages retired into hubs and redirects.
2. **Approve the word cut.** Service pages drop from roughly 900 words to 400 to 500.
   Home drops from 1,376 to about 500. That is the course, and it is a real reduction in
   surface area.
3. **Confirm the tiling page.** 590 searches at 68 cents. Worth having for reach, not
   for money. Say if you would rather skip it.
4. **Decide the old infrastructure.** Worker `plinth-renovations` is idle and
   unreachable. The GitHub repo `Wellew98/plinth-renovations` is still public with the
   old source. Delete both, or archive the repo read-only and delete the Worker.

Nothing gets written until 1 and 2 are approved.

## 12. Execution log, 2026-11-09

Tasks 5 to 12 are done and deployed. What follows is evidence, not intention.

**Task 5, the sheet.** `src/seo-layout.json` now holds 27 pages: 14 compact, 3 hubs, 6 brand, 4 legal. Every compact page carries keyword, MSV, CPC, hub, slug, title, meta, H1, four H2s, word target, image, alt text and notes. `render.py` reads slug, title, meta and H1 from the sheet, so the two can no longer drift apart silently.

**Task 6, the gate.** `src/seo_check.py` checks nine rule groups: page exists, title under 60, meta under 155, H1 carries the keyword, keyword in slug, keyword in an H2, keyword in the first sentence, word count 400 to 500, duplicate titles and metas, crawl depth, orphans, and image reuse. It found 43 problems in the pre-rebuild site. It now reports `27/27 pages found, 0 problems`.

**Tasks 7 to 9, the copy.** Home keeps the hero film and the three credibility pills, with eight service cards plus the send-photos card. All fourteen compact pages land inside the 400 to 500 word band. The technical substance of the old copy was kept and compressed, not replaced: box gutters, parapets, torch-on versus liquid, hose testing, fall correction, the three kitchen and bathroom tiers.

**Task 9, slugs and 301s.** Twelve legacy URLs redirect with 301 and a verified `Location` header: /waterproofing, /painting, /plastering, /kitchens, /bathrooms, /home-renovations, /damp-proofing, /home-extensions, /areas, /gallery, /projects, /blog, plus the six old `home-renovations-in-*` area URLs. All verified live.

**Tasks 10 and 11, hubs and orphans.** `/services`, `/solutions` and `/service-areas` are real pages. The visible breadcrumb now reads Home > Services > [page] and the JSON-LD matches it. `accessibility` and `disclaimer` are linked from the footer on every page; nothing is orphaned.

**Task 12, images.** One image per compact page, named and described in the sheet. Four shares are documented in `_image_exempt` rather than hidden: the roof membrane shot serves both waterproofing pages, the water-damaged ceiling shot serves roof repairs and ceiling repair, the bathroom shot serves tiling, and the four area pages use their parent service's photograph. The library has ten real photographs for fourteen pages; inventing four more would break the imagery rules.

**Infrastructure retired.** The old Worker `plinth-renovations` is deleted; its `workers.dev` hostname no longer resolves. The old GitHub repo `Wellew98/plinth-renovations` is archived read-only, with a 7 MB mirror at `_archive/old-repo.git`. Full deletion needs the `delete_repo` OAuth scope, which the current gh token does not carry.

**Live verification.** 18 URLs return 200. 12 legacy URLs return 301 with the correct target. `www` returns 301 to the apex. The sitemap lists 27 URLs and every one returns 200.

**Corrections made while executing.** The map has fourteen compact pages, not sixteen; two places in this plan said sixteen and are fixed. Four legal pages were kept, so the site is 27 pages, not 23. Damp proofing and home extensions were not in the first draft of the map: both have no page-sized demand and now 301 into waterproofing and home renovations respectively.

**Still owed.** Sitemap submission in Search Console (27 URLs) and, if you want the old repo gone rather than archived, a gh token with `delete_repo`. DataForSEO balance unchanged at $0.46: the rebuild needed no further requests.
