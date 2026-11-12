# Plinth: NAP master

Paste from this file. Never retype a field. A directory that disagrees with this
block damages the entity signal the citation effort exists to build.

## The block

```
Plinth Renovations and Construction
64 Oxford Street, Richmond Estate
Goodwood, Cape Town
Western Cape, 7460
South Africa

Phone: 066 150 5770
International: +27 66 150 5770
WhatsApp: 066 150 5770
Website: https://plinthrenovations.co.za
```

Source: the `HomeAndConstructionBusiness` JSON-LD on the live home page, read 11 Nov 2026.

## Decisions this locks in

**Name.** Use `Plinth Renovations and Construction` everywhere, matching the schema. If the
CIPC registration is a different string (Pty Ltd, different trading name), the CIPC version wins
on Brabys and saYellow, and the schema gets corrected to match. One of the two has to move.

**Address.** `64 Oxford Street, Richmond Estate` is the street address as published. Where a
platform has a separate suburb field, suburb is `Goodwood`, city `Cape Town`, province
`Western Cape`, postal code `7460`.

**Phone.** Local format `066 150 5770` in South African forms, E.164 `+27 66 150 5770` where the
field is international. No spaces, no dashes, no `0027`.

**Hours.** Mon to Fri 07:00 to 18:00. Sat 08:00 to 14:00. Sunday closed. These are the hours in
the schema and in the site header; they must be identical in every listing or the entity reads
two businesses.

**Areas.** Cape Town first, then Durbanville, Bellville, Parow, Table View, Brackenfell,
Southern Suburbs. Seven area pages exist on the site, so seven is the number that can be
defended with a URL.

## Categories, in the platform's own vocabulary

| Platform | Primary | Secondary |
|---|---|---|
| Bing Places | Waterproofing service | General contractor, Roofing contractor, Painter, Remodeler |
| Apple Business | Waterproofing | Contractor, Home improvement |
| Facebook | Waterproofing service | Construction company, Home improvement service |
| LinkedIn | Construction | Building construction |
| saYellow / Brabys / Cylex | Waterproofing contractor | Building contractor, Painting contractor, Plasterer |
| Hotfrog | Waterproofing | Renovation, Roofing |

Where a platform offers a category that does not exist (`Waterproofing` is missing on several),
take the closest parent (`Contractor` or `General contractor`) rather than a wrong trade.

## Description blocks

**120 characters**

> Waterproofing, roofs and renovations in Cape Town. Free written estimates after a site visit
> and moisture check.

**300 characters**

> Plinth Renovations and Construction handles waterproofing, roof repairs, painting, tiling and
> full home renovations across Cape Town. We trace the leak before quoting, work to a written
> scope, and back renovations with a 12-month workmanship warranty. Free written estimates.

**Long form (usable to 1000 words, saYellow allows that)**

> Plinth Renovations and Construction is a building and waterproofing company based at 64 Oxford
> Street, Richmond Estate, Goodwood, working across Cape Town and the northern and southern
> suburbs.
>
> Most of the work is water: roofs, parapets, balconies, box gutters and the ceilings underneath
> them. Cape Town's north-westerly fronts drive rain sideways across roofs and under tiles, so a
> leak usually starts at a junction, a flashing or a neglected upstand rather than in the middle
> of a roof. We read moisture through the plaster, hose test where the source is unclear, and
> specify the system for the substrate in front of us rather than the one that is easiest to
> supply.
>
> The renovation side covers kitchens, bathrooms, full homes, tiling, plastering and painting.
> Work runs to a written scope with the junctions finished before the surface goes on, and
> layers photographed so the client sees what is under the membrane before it is covered.
> Renovations carry a 12-month workmanship warranty.
>
> Estimates are free and written, after a site visit. We do not price waterproofing per square
> metre over the phone, because access, substrate and the number of details decide the cost far
> more than area does.

Facts in that copy come from the live site. Do not add a founding year, a team size, a project
count, a star rating or a guarantee length beyond the 12-month workmanship warranty until
Wellington confirms it in writing. A directory claim that the site cannot back is a trust
liability, and Google reads the site too.

## Assets

Logo: `src/logo-*.svg` in the repo, exported to PNG 512x512 and 1200x630 for platforms that
reject SVG. Photos: the licensed library in `site-output/images/`, pick six real-looking
exteriors and bathrooms. Every listing should use the same logo and the same first photo so the
entity is visually consistent.
