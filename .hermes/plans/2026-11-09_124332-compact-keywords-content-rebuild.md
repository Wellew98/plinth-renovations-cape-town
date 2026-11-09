# Compact Keywords content rebuild: plinthrenovations.co.za

> **Planning only.** Nothing in this document has been executed. No copy has been
> rewritten, no pages have been renamed, no redirects have been added.
> Written 2026-11-09 against the live site at https://plinthrenovations.co.za

**Goal:** Rebuild every page on plinthrenovations.co.za so it follows the Compact
Keywords method in the Edward Sturm course, using measured search volume to decide
which pages exist and the site's own design untouched.

**Architecture:** Hub and spoke. Home and brand pages sell. Three hub pages list
and link every compact page. Each compact page owns exactly one bottom-of-funnel
keyword, matches it in slug, title, H1 and first sentence, runs 400 to 500 words,
and puts the call to action above the fold with the image directly below it.

**Tech stack:** unchanged. `src/content-part1..3.json` feed `build.js`, `images.py`
and `render.py`, which emit static HTML into `site-output/`, deployed to Cloudflare
Pages by `wrangler`.

---

## 1. What I actually read

| Source | What it gave |
| --- | --- |
| Your Google Doc notes (5,464 chars) | The method in your own words: compact vs top funnel, technical audit, landing page structure, information architecture, image SEO |
| `Bottom-of-Funnel SEO Landing Page Template` (Doc) | The page skeleton: URL, page title, meta, H1, six H2s, CTA slots, and the three questions to answer before writing |
| Internal SEO Template: Keywords tab | `Keyword, Category 1, Category 2, Avg Volume, Difficulty, SERP CTR, Moz Priority, On Site Relevance, Notes, Min Volume, Max Volume, Targeted?` |
| Internal SEO Template: Site SEO Layout tab | `Keyword(s), Cat 1, Cat 2, Hub Page Category, Product, URL, Page Title, OG Title, Meta Description, OG Description, H1, H2-1..H2-4, Content Notes, Done?` |
| Internal SEO Template: Information Architecture tab | `Top Navigation (For Brand & Selling), Footer, Blog` |
| Site Audit template | `URL, Delete?, Purpose, New Slug, Current/New Title + length, Current/New Meta + length, Current/New H1 + length, H2s + lengths, Notes, Crawl Depth, Word Count, Inlinks` |
| Competitor Keywords + filled example sheet | How to enumerate variants including misspellings, tag categories, then mark `Targeted Yes/No` |
| 30 course videos | Titles only. See the limitation in section 8. |

The `.txt` files in the folder are not documents, they are links into Drive. I read
through them via your signed-in browser and saved the content to
`research/course/`.

## 2. The method, restated as rules we can test

From your notes, in the order you wrote them:

1. A compact keyword is low volume, exact match, bottom of funnel. Rank for many
   of them regardless of volume.
2. Use the exact language the customer uses, not industry language.
3. URL slug, page title, meta description, H1 and H2s carry the keyword.
4. Title format: `keyword | brand name`, optionally with a call to action in the
   title because it shows in the SERP.
5. Keyword near the start of the first sentence.
6. 400 to 500 words. Less is more. Enough to satisfy intent, plus extra for people
   still on the fence.
7. 80 percent of the tailored copy sits at the top. Short paragraphs of one to
   three sentences, bullets, neutral tone, no superlatives, no sensationalism.
8. H1, then short intro, then CTA, then the image.
9. Beyond the page: hub pages (`services`, `uses`, `alternatives`, `solutions`)
   in the footer, so every compact page connects to the rest.
10. Every page two clicks from home at most. No orphan pages.
11. Image file names matter. Alt text describes what the image shows and how it
    relates, without stuffing the keyword. If an image is used twice, re-upload it
    under a different name.
12. Technical: sitemap, robots, GSC with all variations, indexing submitted, same
    again in Bing, Screaming Frog audit for status codes, indexability, titles,
    metas, headings.
13. Speed: compressed images, WebP, CDN, cache purged after changes.
14. A blog with outbound links, and space treated as luxury.

## 3. Diagnosis of the current site, measured

| Measure | Current | Course target | Verdict |
| --- | --- | --- | --- |
| Pages | 28 | fewer pages, each on one keyword | too broad, not too thin |
| Average words | 570 | about 450 | inflated |
| Service pages | 856 to 1,030 words | 400 to 500 | 2x over |
| Home | 1,376 words | sells, does not compete with service pages | over-long, cannibalises |
| Slugs | `/waterproofing`, `/painting`, `/plastering` | exact keyword, e.g. `/waterproofing-cape-town` | not exact match |
| Titles | three segments, e.g. `Kitchen Renovations Cape Town \| Design, Cabinets and Tiling \| ...` | `keyword \| brand` | too many segments |
| Crawl depth | every page depth 1 | 2 maximum, through hubs | flat, no hierarchy |
| Internal links | every page links to all 27 others | hubs carry the links | link equity diluted |
| Orphan pages | accessibility, disclaimer not linked anywhere | no orphans | real defect |
| Area pages | 6 pages on `renovations in X` | only measured terms | 4 of 6 unmeasured |
| Blog | none | blog with outbound links | missing |
| Images | renamed, alt text present, one credit line | filenames, alt, unique per use | close, needs per-page discipline |
| Speed | 395 KB hero, immutable image caching, CDN | fast, CDN, compressed | already good |

Measured demand we already own, from `research/volumes-2026-11-02.json` (76 terms
pulled, 29 with volume):

| Keyword | MSV | CPC |
| --- | --- | --- |
| waterproofing cape town | 390 | 5.15 |
| painting contractors cape town | 320 | 3.16 |
| kitchen renovations cape town | 260 | 2.22 |
| waterproofing near me | 260 | 3.80 |
| bathroom renovations cape town | 210 | 1.93 |
| home renovations cape town | 170 | 1.96 |
| waterproofing companies cape town | 110 | 4.85 |
| roof waterproofing cape town | 50 | 7.03 |
| waterproofing durbanville | 40 | 8.36 |

The cheap, high-intent money is waterproofing at every level, and it is the one
service where a suburb page has proven demand.

## 4. Target architecture

```
/                             brand and selling. Not a compact page.
/services                     hub: every service, cards, no keyword ownership
/solutions                    hub: problem first (leaking roof, damp walls, cracked plaster)
/service-areas                hub: every area we have measured demand for
/our-work  /about  /estimate  /contact  /faq
/waterproofing-cape-town                    390 MSV  $5.15
/roof-waterproofing-cape-town                50        $7.03
/damp-proofing-cape-town                     (to be measured)
/painting-contractors-cape-town             320        $3.16
/kitchen-renovations-cape-town              260        $2.22
/bathroom-renovations-cape-town             210        $1.93
/home-renovations-cape-town                 170        $1.96
/plastering-cape-town                        30        $3.72
/waterproofing-durbanville                   40        $8.36
```

Rules that fall out of this:

- One keyword owns one page. `/waterproofing-cape-town` does not also chase
  "roof waterproofing"; that is its own page.
- Home does not target "kitchen renovations cape town". It links to the page that does.
- Area pages are born only from measured suburb demand, never from a map.
- Every compact page is linked from its hub, and every hub is in the footer.

## 5. Tasks

Each task is one focused session, ends with a verification command, and is
committed on its own.

### Phase 1, decide the pages with data

**Task 1: Build the candidate keyword list**

- Create: `research/keywords-seed-2026-11-09.txt`
- Generate from three axes: 9 services x 6 modifiers (`cape town`, `near me`,
  `contractors`, `companies`, `cost`, `repair`) x 14 suburbs inside the 25 km
  radius (Goodwood, Richmond Estate, Bellville, Parow, Durbanville, Brackenfell,
  Table View, Milnerton, Montague Gardens, Century City, Edgemead, Bothasig,
  Plattekloof, Kuils River).
- Add the misspellings and colloquialisms from the course example (`damp proofer`,
  `water proofing`, `roof leak repair`).
- Verify: `wc -l` reports 400 to 900 candidate terms.

**Task 2: Measure them in one paid request**

- Create: `research/volumes-2026-11-09.json`
- One call to `keywords_data/google_ads/search_volume/live`, `location_code 2710`,
  `language_code en`, all candidates in a single request. One request costs 0.09
  USD regardless of keyword count, so batching is the whole point.
- Verify: response row count equals candidate count, and the file parses.

**Task 3: Classify and decide, in writing**

- Create: `research/keyword-map-2026-11-09.md`
- Three tables: compact (bottom funnel, becomes a page), support (top funnel,
  becomes a blog or FAQ entry), rejected (no volume and no intent).
- Each compact keyword gets: MSV, CPC, intended slug, hub, and one line on the
  customer's problem.
- Verify: every row marked `Targeted Yes` has a slug that appears in Task 8.

**Task 4: Pull the queries we already rank for**

- Requires your Google Search Console access.
- Export 3 months of queries, add any compact query with impressions to the map.
- Verify: the map now has a `source` column reading `DataForSEO` or `GSC`.

### Phase 2, the layout sheet becomes the source of truth

**Task 5: Create `src/seo-layout.json`**

- One object per page mirroring the course's Site SEO Layout tab:
  `keyword, cat1, cat2, hub, url, title, meta, h1, h2[4], content_notes, done`.
- This file is the brief for every page. `render.py` reads it for title, meta and
  H1 so the page and the sheet cannot drift apart.

**Task 6: Write `src/seo_check.py`**

- Reads `site-output/*.html` plus `seo-layout.json` and fails on:
  - keyword missing from slug, title, H1 or first sentence
  - word count outside 400 to 500
  - title over 60 chars, meta over 155
  - duplicate titles, metas or H1s
  - any page more than 2 clicks from home
  - any page with zero inlinks
  - the same image file used on two pages
- Verify: run it against the current site and watch it fail on purpose. A checker
  that passes before the work is done is not checking anything.

### Phase 3, rewrite

**Task 7: Home**

- Modify: `src/content-part1.json` (home object), `src/render.py` if section order changes.
- Cut 1,376 words to about 500 of selling copy, keep hero film, keep the service
  grid, keep the proof and the FAQ short. Home stops competing with service pages.
- Verify: `node check.js`, home 400 to 500 words, every service page linked.

**Task 8: The nine compact service pages**

- Modify: `src/content-part*.json`, `src/render.py` (page list and slugs).
- Structure per page: H1 with keyword, three sentence intro with the keyword near
  the start, CTA, image directly below the CTA, four H2s carrying variants, 400 to
  500 words, bullets for scope and process.
- Verify: `python src/seo_check.py` passes for all nine.

**Task 9: Slugs and 301s**

- Modify: `src/render.py` (`_redirects` writer and page map).
- `/waterproofing` to `/waterproofing-cape-town`, `/painting` to
  `/painting-contractors-cape-town`, and so on. Old area pages
  `/home-renovations-in-*` to their measured replacements.
- Verify: `curl -sI` each old URL against the deployed site and see 301 to the new one.

**Task 10: Hubs**

- Modify: `src/render.py` (`build_services`, `build_areas`), footer in `src/ui.py`.
- `/services`, `/solutions`, `/service-areas` become practical pages with cards
  linking every compact page. Footer links all three on every page.
- Verify: crawl depth script reports maximum 2 and zero orphans.

**Task 11: Fix the orphans and the indexability**

- Link accessibility and disclaimer in the footer. `noindex` on thank-you. Confirm
  404 stays 404.
- Verify: depth script shows zero unreachable pages.

**Task 12: Images**

- One image per compact page, already-renamed files, alt text describing the scene
  and its relation to the service, no keyword stuffing. Never reuse a file across
  pages without re-uploading under a new name.
- Verify: `seo_check.py` image rule passes.

**Task 13: Blog with outbound links** (optional, your call)

- 3 to 5 guides, for example "what causes rising damp in Cape Town homes", each
  linking out to a credible external source, each linking in to one compact page.

### Phase 4, technical and indexation

**Task 14: Search Console and Bing**

- Verify the property (a `google-site-verification` TXT record already exists on
  the zone), submit `sitemap.xml`, request indexing for the nine compact pages
  first, then repeat in Bing.

**Task 15: Screaming Frog style audit**

- We already have `src/check.js`. Extend it to report status codes, indexability,
  titles, metas, H1 and H2 counts, word counts, crawl depth and inlinks, which is
  exactly the audit template's columns.

**Task 16: Speed**

- Convert project photographs to WebP with JPEG fallback, confirm immutable
  caching and CDN, purge cache after the deploy.

## 6. Validation, the numbers that decide if this worked

| Check | Pass condition |
| --- | --- |
| Compact pages | every one 400 to 500 words |
| Keyword placement | in slug, title, H1, first sentence, one H2 |
| Titles | under 60 characters, `keyword \| Plinth Renovations` |
| Crawl depth | maximum 2 |
| Orphans | zero |
| Internal links | every compact page linked from a hub and at least one sibling |
| Indexation | 100 percent of intended pages indexed within 6 weeks |
| Rankings | each targeted keyword tracked weekly from week 2 |

## 7. Risks and how we avoid them

- **Slug changes on a live site.** Cheap now, expensive later, because the site is
  days old. Do it in Task 9, in one deploy, with the 301s in the same commit.
- **Cutting copy can cut trust.** 400 words of generic text is worse than 900
  specific words. We keep the real photographs, the named materials, the actual
  process. Words go, substance stays.
- **Cannibalisation.** Home currently competes with every service page. Task 7
  removes the overlap.
- **Thin area pages.** No area page is deleted on a hunch. Each is measured first,
  then kept, merged or reworked. An area page with no measurable demand becomes a
  section on its parent hub rather than a weak page of its own.
- **Design regression.** No design changes in this plan. Copy length changes;
  `styles.css` does not.

## 8. Limitation you should know about

The 30 course videos have no subtitle track, and I cannot watch video. I extracted
the method from the written material: your notes, the landing page template, and
all five template sheets. If any rule in the videos is not written down in those
documents, I do not have it. If you tell me which videos carry the parts you care
about, I can transcribe those specific files with Whisper rather than guessing at
all 30.

## 9. Decisions taken, and the one blocker

**Settled by Wellington, 2026-11-09:**

1. **Search Console exists.** The domain property is verified, but it holds almost
   nothing: 2 clicks and 7 impressions across three months at average position 2.1.
   The old site never accumulated query history, so GSC cannot seed this research.
   It becomes a tracking instrument from week two, not a source.
2. **Area pages stay in principle.** None get deleted on a hunch. Each one is kept,
   reworked or merged according to measured demand, and the measurement decides,
   not the aesthetics of a tidy sitemap.
3. **Blog is deferred.** No new guide or blog pages in this rebuild. The internal
   linking work still leaves room for them later without restructuring.
4. **The course governs, provided we target compact keywords.** Where the course and
   our current copy disagree, the course wins.

**Blocker: volume measurement is unfunded.**

The DataForSEO balance is **$0.00065**, not the $0.73 recorded earlier. One request
costs about $0.09, so Task 2 fails with 402 today. Options, cheapest first:

- Top up DataForSEO. At $0.09 per request a $50 deposit is roughly 500 measurement
  rounds, which is years of use for a single market.
- Google Ads Keyword Planner, if you have an Ads account with spend history. Free,
  but new accounts return ranges rather than exact volumes.
- Bing Webmaster keyword research. Free with a verified site, Bing volumes only.

Until one of those lands, the candidate set can still be built and ranked by demand
signals: autocomplete presence and order, commercial intent in the phrase, and what
competitors actually rank pages for. What cannot be done is stating a monthly volume
we have not measured, and I will not put invented numbers in the layout sheet.


## 10. Measured keyword research, 2026-11-09

Done, not planned. Three DataForSEO requests, 297 unique keywords, $0.27 spent.
Full write-up in `research/compact-keywords-2026-11-09.md`, data in
`research/keyword-master.csv`.

**The compact set is real now.** 34 terms at or below 110 searches a month with a
CPC of at least $1.50, which is the exact profile the course targets:

| Volume | CPC | Keyword | Goes to |
|---:|---:|---|---|
| 40 | $8.36 | waterproofing durbanville | area page |
| 50 | $7.03 | roof waterproofing cape town | service page |
| 20 | $7.04 | waterproofing specialists cape town | service page |
| 110 | $4.85 | waterproofing companies cape town | service page |
| 70 | $4.49 | waterproofing contractors cape town | service page |
| 10 | $9.84 | home renovation contractors cape town | home renovations |
| 10 | $9.24 | paint contractors brackenfell | area section |
| 30 | $3.97 | roof repairs durbanville | area page |
| 30 | $3.72 | plastering cape town | service page |
| 20 | $5.61 | leaking ceiling repair | problem page |

**Area demand, measured.** Durbanville 290 across 15 terms. Somerset West 100 across
5. Southern Suburbs 70 across 5. Bellville 30, Brackenfell 20, Parow and Table View 10
each. Milnerton and Goodwood return zero. So: Durbanville, Somerset West and Southern
Suburbs get pages. Bellville and Brackenfell become sections on the areas hub. Goodwood
gets a brand paragraph, not a page. That answers "keep our pages or research more":
the research decided, and I am not deleting anything without this table in hand.

**Problem demand, measured.** 98 problem phrases carry volume, led by leaking ceiling
repair (20 at $5.61), fix leak in ceiling (20 at $5.61), leaking roof repairs cape town
(20 at $5.00) and ceiling water leak repair near me (10 at $8.17). A home renovations
page cannot answer "my ceiling is leaking", so these get their own `/solutions/` pages,
one keyword each.

**Rejected on evidence.** Tile retailer brands (ceramica, tileafrica, tilehouse) at up
to 720 searches: wrong intent entirely. Eyelash extensions: 90 searches, no relation,
appears only because "cape town" is the shared token. Both are in the CSV so the
decision is auditable.
