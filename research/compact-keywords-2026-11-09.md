# Compact keyword research, Plinth Renovations, 2026-11-09

Method: DataForSEO `keywords_for_keywords` (Google Ads data), location South Africa
(`location_code 2710`), English. Three batched requests, $0.27 total.

- Seeds: 10 core services, 14 suburb phrases, 10 problem phrases.
- Returned: 297 unique keywords, deduplicated by highest volume.
- Buckets: 107 money, 180 problem, 10 other.
- Raw: `ideas-raw.json`, `ideas-suburbs.json`, `ideas-problems.json`.
- Classified: `keyword-master.csv` (keyword, volume, cpc, competition, bucket, service).

## What a compact keyword looks like here

Low volume, high cost per click, exact match, and a buyer on the other end. This is
the profile the course is built around, and it is where the money is:

| Volume | CPC | Keyword |
|---:|---:|---|
| 10 | $9.84 | home renovation contractors cape town |
| 10 | $9.24 | paint contractors brackenfell |
| 40 | $8.36 | waterproofing durbanville |
| 20 | $7.04 | waterproofing specialists cape town |
| 50 | $7.03 | roof waterproofing cape town |
| 10 | $5.62 | torch on waterproofing cape town |
| 20 | $5.53 | paint contractors somerset west |
| 110 | $4.85 | waterproofing companies cape town |
| 70 | $4.49 | waterproofing contractors cape town |
| 30 | $3.97 | roof repairs durbanville |
| 30 | $3.72 | plastering cape town |
| 30 | $3.66 | house painting contractors cape town |

34 such terms sit at or below 110 searches a month with a CPC of at least $1.50.
Nine dollars a click tells you exactly what a click is worth to a competitor.

## Area demand, measured

| Area | Total volume | Terms |
|---|---:|---:|
| Durbanville | 290 | 15 |
| Somerset West | 100 | 5 |
| Southern Suburbs | 70 | 5 |
| Bellville | 30 | 3 |
| Brackenfell | 20 | 2 |
| Parow | 10 | 1 |
| Table View | 10 | 1 |
| Milnerton | 0 | 1 |
| Goodwood | 0 | 1 |

Durbanville earns its own page several times over: 290 searches a month across 15
terms, with waterproofing alone at 40 searches and $8.36 a click. Somerset West and
Southern Suburbs earn pages. Bellville and Brackenfell earn sections on the areas hub.
Milnerton and Goodwood return nothing measurable, and Goodwood is where the business
physically is, which is worth a paragraph for local relevance and nothing more.

## Problem demand, measured

| Volume | CPC | Keyword |
|---:|---:|---|
| 20 | $5.61 | leaking ceiling repair |
| 20 | $5.61 | fix leak in ceiling |
| 20 | $5.00 | leaking roof repairs cape town |
| 10 | $8.17 | ceiling water leak repair near me |
| 10 | $2.15 | leaking ceiling repair cost |

Near a hundred problem phrases returned data. These are the highest-intent searches
on the list: someone with water coming through the ceiling is not researching, they
are buying. They do not fit the service pages, because a service page about
waterproofing does not answer "my ceiling is leaking". They need their own pages.

## What the data rejects

- `ceramica cape town`, `tileafrica kenilworth`, `tilehouse cape town`: tile retailer
  brands, 140 to 720 searches, and useless to a renovation contractor.
- `eyelash extensions cape town`: 90 searches and no relationship to anything here.
  It appears because "cape town" is the only shared token. This is why classifying
  by hand matters more than trusting a volume column.
- Broad head terms like `painters cape town` at 720 are worth having, but they are
  hub and home page territory, not compact pages.
