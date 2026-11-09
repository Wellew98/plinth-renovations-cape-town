"""Rebuild the Plinth microsite in the original site's design and copy.

The page shells, section anatomy, class names and brand copy come from the
live plinthrenovations.co.za pages. The keyword architecture, service set and
area targeting come from the measured DataForSEO build.
"""

import json
import re
import shutil
from html import escape
from pathlib import Path

import photos
from library import LIBRARY
import ui
from ui import (
    BUSINESS, CITY, DOMAIN, PHONE, STREET, TEL,
    card, checklist, cta_band, faq, floaters, footer, gallery, grid, head, header,
    hero, page_hero, section, steps, ticks, topbar,
)

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
OUT = ROOT / "site-output"
ORIG = Path(r"C:\Users\DELL\OneDrive\Desktop\_archive\PLINTH")

content = json.loads((SRC / "content.json").read_text(encoding="utf-8"))
LAYOUT = json.loads((SRC / "seo-layout.json").read_text(encoding="utf-8"))
SPEC = {s["key"]: s for s in LAYOUT["pages"]}


def _compact_services():
    out = []
    for name in ("content-compact-1.json", "content-compact-2.json"):
        for svc in json.loads((SRC / name).read_text(encoding="utf-8"))["services"]:
            spec = SPEC[svc["key"]]
            svc["slug"] = spec["url"].strip("/")
            svc["title_tag"] = spec["title"]
            svc["meta_description"] = spec["meta"]
            svc["hub"] = spec.get("hub") or "services"
            out.append(svc)
    return out


SERVICES = _compact_services()

AREA_PAGES = json.loads((SRC / "content-areas.json").read_text(encoding="utf-8"))["areas"]
AREAS = content["areas"]          # legacy area feed, redirects only
HOME = content["home"]
SITE = content["site"]

HUBS = {
    "services": ("Services", "/services"),
    "service-areas": ("Service Areas", "/service-areas"),
    "solutions": ("Solutions", "/solutions"),
}

# photographs were catalogued against the old service slugs
PHOTO_KEY = {
    "waterproofing": "waterproofing",
    "roof-waterproofing": "waterproofing",
    "roof-repairs": "waterproofing",
    "leaking-ceiling-repair": "waterproofing",
    "waterproofing-durbanville": "waterproofing",
    "waterproofing-somerset-west": "waterproofing",
    "waterproofing-southern-suburbs": "waterproofing",
    "painting": "painting",
    "painters-durbanville": "painting",
    "plastering": "plastering",
    "tiling": "plastering",
    "kitchens": "kitchen-renovations",
    "bathrooms": "bathroom-renovations",
    "home-renovations": "home-renovations",
}
AREA_KEYS = [s["key"] for s in SPEC.values() if s.get("hub") == "service-areas"]

TAG_OVERRIDE = {
    "roof-waterproofing": "Weatherproofing",
    "roof-repairs": "Repairs",
    "leaking-ceiling-repair": "Water damage",
    "tiling": "Finishes",
    "waterproofing-durbanville": "Weatherproofing",
    "painters-durbanville": "Finishes",
    "waterproofing-somerset-west": "Weatherproofing",
    "waterproofing-southern-suburbs": "Weatherproofing",
}

ICON_OVERRIDE = {
    "roof-waterproofing": "water",
    "roof-repairs": "water",
    "leaking-ceiling-repair": "damp",
    "tiling": "plaster",
    "waterproofing-durbanville": "water",
    "painters-durbanville": "paint",
    "waterproofing-somerset-west": "water",
    "waterproofing-southern-suburbs": "water",
}

ICON_FOR = {
    "Waterproofing": "water",
    "Damp Proofing": "damp",
    "Painting": "paint",
    "Kitchen Renovations": "kitchen",
    "Bathroom Renovations": "bath",
    "Home Renovations": "home",
    "Plastering": "plaster",
    "Home Extensions": "extend",
}

TAG_FOR = {
    "Waterproofing": "Weatherproofing",
    "Damp Proofing": "Weatherproofing",
    "Painting": "Finishes",
    "Kitchen Renovations": "Kitchen & Bath",
    "Bathroom Renovations": "Kitchen & Bath",
    "Home Renovations": "Remodeling",
    "Plastering": "Finishes",
    "Home Extensions": "Remodeling",
}

for _svc in SERVICES:
    _svc["tag"] = TAG_OVERRIDE.get(_svc["key"]) or TAG_FOR.get(_svc["name"], "Services")
    _svc["icon"] = ICON_OVERRIDE.get(_svc["key"]) or ICON_FOR.get(_svc["name"], "plaster")

# The Plinth Standard and the enquiry flow are the owner's own published words.
STANDARD = [
    "Written scope + fixed price before we start",
    "Photo updates if you're not on site",
    "12-month workmanship warranty on renovations",
    "Goodwood-based, fast response across Cape Town",
]

FLOW = [
    ("You send photos", f"Form or WhatsApp to {PHONE}. We respond within 1 business day."),
    ("Walkthrough", "We visit, measure, check damp, electrics and access, and advise honestly."),
    ("Fixed written quote", "Scope, materials, timeline and total price in writing. No hourly drift."),
    ("Build + tidy handover", "Dust control, daily tidy, photo updates and snag-free handover."),
]

WHY_COPY = (
    "<p>We are <strong>Plinth Renovations and Construction</strong>, based at "
    f"{STREET}, {CITY.split(',')[0]}. After years working on homes across the Northern "
    "Suburbs and the greater city, we build for what most contractors underestimate: this climate.</p>"
    "<p>At the foot of Table Mountain your home takes a unique beating. Atlantic salt air "
    "corrodes fixtures and fasteners. The summer Cape Doctor drives dust and UV into paint and "
    "timber. Winter brings sideways rain that finds every failed seal, flat roof and cracked "
    "parapet. Older Goodwood, Parow and Milnerton stock often hides damp, cracked plaster and "
    "tired electrics.</p>"
    "<p>Our playbook is written for that: stainless or treated fixings near the coast, flexible "
    "waterproofing for parapets and flat roofs, mould-resistant prep, and honest advice on where "
    "to spend and where to save.</p>"
)

PAGE_REGISTRY = []  # (slug, title, description, priority)


def page(slug, title, description, body, schema=None, crumbs=None):
    canonical = f"{DOMAIN}/{slug}" if slug else DOMAIN + "/"
    url_path = f"/{slug}" if slug else "/"
    active = url_path if url_path in [h for h, _ in ui.NAV] else ""
    crumbs = crumbs or []
    bc = ""
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
        for i, (name, path) in enumerate(crumbs, 2):
            items.append({"@type": "ListItem", "position": i, "name": name, "item": DOMAIN + path})
        bc = '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        ) + "</script>"

    ld = ""
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>"

    og_img = f'{DOMAIN}/images/{photos.HERO["file"]}'
    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{escape(BUSINESS)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_ZA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=20261103b">
<link rel="stylesheet" href="extra.css?v=20261103b">
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>
<link rel="icon" href="logo.jpg">
{bc}
{ld}
</head>
<body>
{topbar()}
{header(active)}
<main>
{body}
</main>
{footer()}
{floaters()}
<script src="script.js" defer></script>
</body>
</html>
"""


def business_schema(extra=None):
    s = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": DOMAIN + "/#business",
        "name": BUSINESS,
        "url": DOMAIN + "/",
        "telephone": TEL,
        "image": DOMAIN + "/images/" + photos.HERO["file"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": "Goodwood",
            "addressRegion": "Western Cape",
            "postalCode": "7460",
            "addressCountry": "ZA",
        },
        "areaServed": [{"@type": "City", "name": "Cape Town"}] + [
            {"@type": "Place", "name": a["name"]} for a in AREAS
        ],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "07:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00"},
        ],
    }
    if extra:
        s.update(extra)
    return s


def service_schema(svc):
    slug = svc.get("slug") or re.sub(r"[^a-z0-9]+", "-", svc["name"].lower()).strip("-")
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f'{svc["name"]} in Cape Town',
        "serviceType": svc["name"],
        "provider": {"@type": "HomeAndConstructionBusiness", "name": BUSINESS, "telephone": TEL,
                     "address": {"@type": "PostalAddress", "streetAddress": STREET,
                                 "addressLocality": "Goodwood", "postalCode": "7460", "addressCountry": "ZA"}},
        "areaServed": {"@type": "City", "name": "Cape Town"},
        "url": f"{DOMAIN}/{slug}",
        "description": svc["meta_description"],
    }


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ---------------------------------------------------------------- home

def build_home():
    lead = HOME["leader"]
    picks = ["waterproofing", "roof-repairs", "painting", "kitchens",
             "bathrooms", "home-renovations", "plastering", "tiling"]
    cards = [
        card(s["tag"], s["name"], s["teaser"], f'/{s["slug"]}', icon=s["icon"])
        for s in sorted(SERVICES, key=lambda s: picks.index(s["key"]) if s["key"] in picks else 99)
        if s["key"] in picks
    ]
    # the original grid is 3x3; the ninth cell answers the "which one do I need" question
    cards.append(card("Not sure", "Not sure what it needs?",
                      "Send photos on WhatsApp and we will tell you which of these applies, "
                      "before you commit to anything.", "/estimate",
                      link_label="Send photos", icon="plaster"))
    body = hero(
        "Cape Town",
        "Renovations in Cape Town, Built to Last",
        HOME["leader"]["cta_line"],
        ["Quality Workmanship", "Reliable Service", "Timeless Finishes"],
        '<a class="btn btn-gold" href="/estimate">Get a Free Estimate</a>'
        f'<a class="btn btn-ghost" href="tel:{TEL}">{PHONE}</a>',
        video="hero-video.mp4",
    )
    body += section(
        head("01", "What We Do", "Renovation and Waterproofing Services in Cape Town", HOME["services_intro"])
        + grid(cards),
        cls="ghost",
    )
    body += section(
        head("02", "Why Plinth", "Built for Cape Town. Not a Generic Contractor.", left=True)
        + '<div class="why"><div class="reveal">'
        + WHY_COPY
        + ticks([w["point"] + ": " + w["detail"] for w in HOME["whyus"]])
        + "</div>"
        + checklist("The Plinth Standard", STANDARD)
        + "</div>",
        cls="blueprint",
    )
    body += section(
        head("03", "How It Works", "From first call to final walkthrough",
             "Same flow as our estimate page, clear, written, no pressure.")
        + steps(FLOW)
    )
    home_gallery = [
        photos.by_file("kitchen-renovation-cape-town.jpg"),
        photos.by_file("bathroom-renovation-cape-town.jpg"),
        photos.by_file("glass-roof-patio-extension-cape-town.jpg"),
        photos.by_file("plasterboard-bulkhead-ceiling-cape-town.jpg"),
        photos.by_file("interior-renovation-in-progress-cape-town.jpg"),
        photos.by_file("home-extension-under-construction-cape-town.jpg"),
    ]
    body += section(
        head("04", "Recent Work", "Our own jobs, photographed as we work",
             "Every photograph in this section is a Plinth job, from the stripped-out room "
             "through to the finished kitchen.")
        + gallery(home_gallery)
        + '<div class="center-cta"><a class="btn btn-ghost" href="/our-work">'
          "See all our work &rarr;</a></div>",
    )

    area_cards = [
        card("Service area", a["name"], a["teaser"], f'/{a["slug"]}',
             link_label="See this area", icon=None)
        for a in SERVICES if a["hub"] == "service-areas"
    ]
    body += section(
        head("05", "Where We Work", "Areas we cover across Cape Town", HOME["areas_body"])
        + grid(area_cards[:6])
        + '<div class="center-cta reveal"><a class="btn btn-gold" href="/service-areas">'
          "All service areas &rarr;</a></div>",
        cls="sage",
    )
    body += section(
        head("06", "FAQ", "Cape Town Renovation FAQ") + faq([(f["q"], f["a"]) for f in HOME["faq"]])
        + cta_band("Get a Free Estimate on Your Project", HOME["cta_subtext"]),
        cls="cream",
    )

    return page(
        "", "Renovations Cape Town | Plinth Renovations and Construction",
        HOME["meta_description"], body, schema=business_schema(),
    )


# ---------------------------------------------------------------- services

def build_services():
    cards = [
        card(s["tag"], s["name"], s["teaser"], f'/{s["slug"]}', icon=s["icon"])
        for s in SERVICES
    ]
    cards.append(card("Not sure", "Not sure what it needs?",
                      "Send photos and we will tell you which of these applies, and what it "
                      "should cost, before you commit.", "/estimate",
                      link_label="Send photos", icon=None))
    body = page_hero(
        "Services", "Renovation and Waterproofing Services in Cape Town",
        "Waterproofing, repairs, painting, plastering, tiling and full renovations under one written "
        "scope. Every job includes a free written estimate and a fixed price before work starts.", kicker="No Obligation · Flat-Rate Pricing",
    )
    body += section(
        head("01", "What We Do", "Pick the job, or send photos and we will tell you what it needs",
             HOME["services_intro"])
        + grid(cards)
        + cta_band("Not sure which service you need?", "Send photos and we will tell you honestly.")
    )
    return page(
        "services", "Renovation Services Cape Town | Plinth Renovations",
        "Waterproofing, painting, kitchen and bathroom renovations, damp proofing, plastering and "
        "extensions across Cape Town. Free written estimates, fixed prices.", body,
        crumbs=[("Services", "/services")],
    )


def build_service(svc):
    slug = svc["slug"]
    hub_name, hub_url = HUBS[svc["hub"]]
    lead = svc["leader"]
    sub_cards = [
        card("", it["name"], it["desc"], "/estimate", link_label="Get estimate", icon=None)
        for it in svc["subitems"]
    ]
    cost = svc["cost"]
    rows = "".join(
        "<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in r) + "</tr>" for r in cost["rows"]
    )
    thead = "".join(f"<th>{escape(c)}</th>" for c in cost["columns"])
    cost_html = (
        f'<div class="table-wrap"><table class="cost-table"><thead><tr>{thead}</tr></thead>'
        f"<tbody>{rows}</tbody></table></div>"
        f'<p class="table-note">{escape(cost["note"])}</p>'
    )
    body = page_hero(
        [(HUBS[svc["hub"]][0], HUBS[svc["hub"]][1]), (svc["name"], None)],
        lead["h1"], lead["cta_line"], kicker=lead["eyebrow"], cta=True,
    )
    pkey = PHOTO_KEY.get(svc["key"], "waterproofing")
    spec = SPEC[svc["key"]]
    if spec.get("image"):
        ph = dict(photos.by_file(spec["image"]))
        if spec.get("image_alt"):
            ph["alt"] = spec["image_alt"]
            ph["caption"] = spec["image_alt"]
        svc_photos = [ph]
    else:
        svc_photos = [ph for ph in photos.PHOTOS + photos.STOCK if ph["service"] == pkey]
    body += section(
        head("01", svc["name"], svc["intro_heading"])
        + '<div class="prose reveal">'
        + "".join(f"<p>{escape(x.strip())}</p>" for x in svc["intro_body"].split("\n\n") if x.strip())
        + "</div>"
        + (gallery(svc_photos, layout="single" if len(svc_photos) == 1 else "pair") if svc_photos else "")
    )
    strip = spec.get("gallery") or []
    if strip:
        alts = dict(LIBRARY)
        items = [{"file": n, "alt": alts.get(n, ""), "caption": ""} for n in strip]
        body += section('<div class="reveal" style="padding-top:8px">' + gallery(items) + "</div>", cls="ghost")
    body += section(head("02", "What it covers", svc["detail_heading"], svc["detail_intro"]) + grid(sub_cards),
        cls="ghost")
    body += section(head("03", "Cost", cost["heading"]) + cost_html + cta_band(
        f'Get a written {svc["name"].lower()} estimate', svc["cta_subtext"]), cls="cream")
    body += section(
        head("04", "How It Works", svc["process"]["heading"]) + steps(
            [(s["step"], s["detail"]) for s in svc["process"]["steps"]])
        + '<div class="why" style="margin-top:48px"><div class="reveal">'
        + ticks([f'{w["point"]}: {w["detail"]}' for w in svc["whyus"]])
        + "</div>" + checklist("The Plinth Standard", STANDARD) + "</div>",
        cls="blueprint",
    )
    others = [a for a in SERVICES if a["hub"] == "service-areas" and a["key"] != svc["key"]]
    area_links = "".join(
        f'<a class="btn btn-ghost" style="margin:0 8px 12px 0" href="/{a["slug"]}">'
        f'{escape(a["name"])}</a>' for a in others
    )
    body += section(
        head("05", "Where we work", f'{svc["name"]} across Cape Town',
             "We are based in Goodwood and cover Cape Town within about 25km.")
        + f'<div class="reveal">{area_links}'
        + f'<a class="btn btn-ghost" style="margin:0 8px 12px 0" href="/service-areas">All service areas</a>'
        + f'<a class="btn btn-ghost" style="margin:0 8px 12px 0" href="/solutions">Not sure which service?</a></div>'
    )
    return page(
        slug, svc["title_tag"], svc["meta_description"], body,
        schema=service_schema(svc), crumbs=[(hub_name, hub_url), (svc["name"], f"/{slug}")],
    )


# ---------------------------------------------------------------- solutions

def build_solutions():
    cards = [
        card("Water damage", "A leaking ceiling",
             "Water showing on a ceiling inside the house. The entry point is almost always above, "
             "and usually not directly over the stain.",
             "/leaking-ceiling-repair", link_label="Ceiling leak repair", icon="damp"),
        card("Roof", "A leak after rain",
             "Water appears only when it rains, often on one side of the house or around a chimney.",
             "/roof-repairs-cape-town", link_label="Roof repairs", icon="water"),
        card("Damp", "A wall that comes back wet",
             "Paint or plaster fails in the same place every winter, however often it is redone.",
             "/waterproofing-cape-town", link_label="Waterproofing", icon="water"),
    ]
    body = page_hero(
        "Solutions", "Start With the Problem, Not the Service",
        "Most people cannot name the trade they need, and they should not have to. Describe what "
        "the house is doing and this page points to the right one.", kicker="What is the house doing",
    )
    body += section(
        head("01", "Problems", "Three ways a water problem shows up",
             "Almost every call we get starts with one of these.") + grid(cards)
    )
    body += section(
        head("02", "Not listed", "If none of these fit",
             "Send a photo on WhatsApp and a sentence about when it appears. We will tell you which "
             "service it is, or that it is not ours to do.")
        + cta_band("Describe the problem", "Photos and a sentence are usually enough to point you the right way."),
        cls="ghost",
    )
    return page(
        "solutions", "Solutions | Plinth Renovations",
        "Not sure whether you need waterproofing, a roof repair or a renovation? Start with what the "
        "house is doing and work back to the trade.",
        body, crumbs=[("Solutions", "/solutions")],
    )


# ---------------------------------------------------------------- areas

def build_area(area):
    slug = f'home-renovations-in-{slugify(area["name"])}'
    lead = area["leader"]
    svc_cards = [
        card(TAG_FOR[s["name"]], s["name"], s["teaser"], f'/{slugify(s["name"])}', icon=ICON_FOR[s["name"]])
        for s in SERVICES
    ]
    svc_cards.append(card("All services", "See every service",
                          "The full list, with what each one covers and what moves the price.",
                          "/services", link_label="View services", icon=None))
    body = page_hero(area["name"], lead["h1"], lead["cta_line"], kicker=lead["eyebrow"])
    body += section(
        head("01", "Local work", area["intro_heading"])
        + f'<div class="prose reveal"><p>{escape(area["intro_body"])}</p></div>'
        + '<div class="why" style="margin-top:40px"><div class="reveal">'
        + ticks([f'{w["point"]}: {w["detail"]}' for w in area["whyus"]])
        + "</div>" + checklist("The Plinth Standard", STANDARD) + "</div>",
        cls="blueprint",
    )
    i = [a["name"] for a in AREAS].index(area["name"])
    rot = [photos.PHOTOS[(i * 2) % len(photos.PHOTOS)],
           photos.PHOTOS[(i * 2 + 1) % len(photos.PHOTOS)]]
    body += section(head("02", "Recent work", "Work from around the city") + gallery(rot, layout="pair"))
    body += section(
        head("03", "Services here", f'What we do in {area["name"]}') + grid(svc_cards)
        + cta_band(f'Get a free estimate in {area["name"]}', area["cta_subtext"]),
        cls="ghost",
    )
    return page(
        slug, area["title_tag"], area["meta_description"], body,
        schema=business_schema({"areaServed": area["name"]}),
        crumbs=[("Service Areas", "/service-areas"), (area["name"], f"/{slug}")],
    )


def build_coverage_area(a):
    spec = SPEC[a["key"]]
    paras = "".join(f"<p>{escape(p)}</p>" for p in a["intro"].split("\n\n"))
    items = "".join(
        card("Service", i["name"], i["desc"], i["link"], link_label=i["name"], icon="plaster")
        for i in a["items"]
    )
    probs = "".join(f'<li style="margin-bottom:14px">{escape(p)}</li>' for p in a["problems"])
    near = "".join(
        f'<a class="btn btn-ghost" style="margin:0 8px 12px 0" href="{n[1]}">{escape(n[0])}</a>'
        for n in a["nearby"]
    )
    body = page_hero(
        [("Service Areas", "/service-areas"), (a["area"], None)],
        a["h1"], a["intro"].split("\n\n")[0], kicker=f'{a["area"]} \u00b7 Cape Town', cta=True,
    )
    img = dict(photos.by_file(spec["image"]))
    if spec.get("image_alt"):
        img["alt"] = spec["image_alt"]
        img["caption"] = spec["image_alt"]
    body += section(
        head("01", "The area", f'{a["area"]}, as we find it', "")
        + f'<div class="reveal prose">{paras}</div>'
        + f'<div style="margin-top:26px">{gallery([img], layout="single")}</div>'
    )
    cstrip = spec.get("gallery") or []
    if cstrip:
        calts = dict(LIBRARY)
        citems = [{"file": n, "alt": calts.get(n, ""), "caption": ""} for n in cstrip]
        body += section('<div class="reveal">' + gallery(citems) + "</div>", cls="ghost")
    body += section(
        head("02", "Services", f"What we do in {a['area']}",
             "Every service below has its own page. The work is the same as anywhere else in "
             "Cape Town; the houses it goes into are not.") + grid(items),
        cls="ghost",
    )
    body += section(
        head("03", "What fails here", f"The {a['area']} problems we get called for",
             "These come up more often in this area than in the city as a whole.")
        + f'<div class="reveal"><ul class="checks">{probs}</ul></div>'
    )
    body += section(
        head("04", "Around", "Nearby areas we also cover", "")
        + f'<div class="reveal" style="margin-bottom:18px">{near}</div>'
        + cta_band(f"Get an estimate in {a['area']}",
                   "Free site visit, written scope, fixed price before anything starts."),
        cls="sage",
    )
    return page(
        spec["url"].strip("/"), a["title"], a["meta"], body,
        crumbs=[("Service Areas", "/service-areas"), (a["area"], spec["url"])],
    )


def build_areas_index():
    cards = [
        card("Service area", a["name"], a["teaser"], f'/{a["slug"]}',
             link_label="See this area", icon=None)
        for a in SERVICES if a["hub"] == "service-areas"
    ] + [
        card("Local area", a["area"], a["intro"].split(". ")[0] + ".", f'/{a["slug"]}',
             link_label=f'{a["area"]}', icon=None)
        for a in AREA_PAGES
    ]
    nearby = [
        "Goodwood", "Richmond Estate", "Monte Vista", "Edgemead", "Bothasig",
        "Milnerton", "Century City", "Plattekloof", "Kuils River", "Bloubergstrand",
        "Stellenbosch", "Gordon's Bay", "Strand", "Kuils River",
    ]
    body = page_hero(
        "Service Areas", "Where Plinth Works in Cape Town",
        "Based at 64 Oxford Street, Richmond Estate, Goodwood. We cover Cape Town within about "
        "25km, and Stellenbosch or Somerset West by arrangement for larger renovations.",
        kicker="Goodwood based · Cape Town wide",
    )
    body += section(
        head("01", "Areas", "Suburbs we work in most", "The areas below have their own page because "
             "the work there has its own problems, from coastal salt to 1970s plaster.") + grid(cards)
    )
    body += section(
        head("02", "Coverage", "The rest of our service area",
             "These suburbs have no page of their own yet. We work in them regularly, so ask.")
        + '<div class="reveal"><p class="sub">' + " · ".join(nearby) + "</p></div>"
        + cta_band("Check whether we cover your street", "One call is faster than a form."),
        cls="sage",
    )
    return page(
        "service-areas", "Service Areas Cape Town | Plinth Renovations",
        "Plinth Renovations covers Cape Town within 25km of Goodwood, including Durbanville, "
        "Bellville, Parow, Table View, Brackenfell and the Southern Suburbs.", body,
        crumbs=[("Service Areas", "/service-areas")],
    )


# ---------------------------------------------------------------- info pages

ABOUT_PARAS = (
    "<p>Plinth started with a simple frustration: vague quotes, moving prices and messy sites. "
    "We do the opposite: written scope, fixed price, daily tidy, photo updates, and a handover "
    "you can walk through without a snag list.</p>"
    "<p>Based at 64 Oxford Street, Richmond Estate, Goodwood, we specialise in the homes that make "
    "up most of Cape Town: facebrick and plaster 70s to 90s houses, townhouses and family homes "
    "that need real work done properly, not a patch that fails by the next winter.</p>"
)


def build_about():
    body = page_hero(
        "About", "About Plinth Renovations and Construction",
        "Goodwood-based renovators serving Cape Town with honest scopes, fixed prices and tidy sites.",
        kicker="Built on vision, crafted with precision",
    )
    body += section(
        head("01", "Who we are", "Built on vision, crafted with precision")
        + '<div class="why"><div class="reveal">' + ABOUT_PARAS
        + ticks(["Owner-supervised crews",
                 "Coastal-correct materials (stainless, treated timber, flexible waterproofing)",
                 "12-month workmanship warranty on renovations"])
        + "</div>"
        + checklist("Fast Facts", [f"Based: {STREET}, Goodwood, Cape Town",
                                   f"Phone: {PHONE}",
                                   "Hours: Mon to Fri 7 to 18, Sat 8 to 14",
                                   "Service: Cape Town within about 25km",
                                   "Estimates: Free, written, flat-rate"])
        + "</div>",
        cls="blueprint",
    )
    body += section(
        head("02", "Our work", "What the work actually looks like",
             "Finished rooms and the stages that get you there.")
        + gallery([photos.by_file("kitchen-renovation-cape-town.jpg"),
                   photos.by_file("bathroom-renovation-cape-town.jpg"),
                   photos.by_file("renovated-home-exterior-cape-town.jpg")])
    )
    body += section(
        head("03", "How It Works", "From first call to final walkthrough") + steps(FLOW)
        + cta_band("Meet us on site, free estimate", "No obligation, no hourly surprises.")
    )
    return page(
        "about", "About Plinth Renovations | Goodwood, Cape Town",
        "Plinth Renovations and Construction is based at 64 Oxford Street, Richmond Estate, "
        "Goodwood, serving Cape Town with written scopes and fixed prices.", body,
        schema=business_schema(), crumbs=[("About", "/about")],
    )


def build_work():
    body = page_hero(
        "Our Work", "Our Work: Renovations in Cape Town",
        "Kitchens, bathrooms, ceilings and extensions we have built, plus the stages most "
        "contractors never photograph.", kicker="Our own photographs",
    )
    body += section(
        head("01", "Recent work", "Every photograph in this gallery is a Plinth job",
             "Finished rooms and work in progress, in the order a job actually runs: stripped out, "
             "framed, plastered, finished.")
        + gallery(photos.PHOTOS + [photos.HERO], eager=3)
        + cta_band("Want your home done like this?",
                   "Send photos of the space and you will get a written estimate, free.")
    )
    return page(
        "our-work", "Our Work | Plinth Renovations, Cape Town",
        "Kitchens, bathrooms, ceilings and extensions built by Plinth Renovations in Cape Town, "
        "photographed on site.", body, crumbs=[("Our Work", "/our-work")],
    )


def build_contact():
    body = page_hero(
        "Contact", "Talk to Plinth About Your Project",
        f"Call or WhatsApp {PHONE}. We answer during working hours and reply to messages within "
        "one business day.", kicker="Free written estimates",
    )
    details = (
        '<div class="why"><div class="reveal">'
        f"<p><strong>Phone and WhatsApp</strong><br><a href=\"tel:{TEL}\">{PHONE}</a></p>"
        f"<p><strong>Address</strong><br>{STREET},<br>{CITY}</p>"
        "<p><strong>Hours</strong><br>Monday to Friday, 7am to 6pm<br>Saturday, 8am to 2pm</p>"
        "<p><strong>Service area</strong><br>Cape Town within about 25km of Goodwood. "
        "Stellenbosch and Somerset West by arrangement for larger renovations.</p>"
        "</div>"
        + checklist("Before you call", [
            "Photos of the problem, wide and close",
            "Rough size of the room or roof area",
            "Whether you are living in the house during the work",
            "Any deadline you are working to",
        ], cta_href="/estimate", cta_label="Send project details &rarr;")
        + "</div>"
    )
    body += section(head("01", "Contact", "How to reach us") + details, cls="ghost")
    return page(
        "contact", "Contact Plinth Renovations | Cape Town",
        f"Call Plinth Renovations on {PHONE} or send project details for a free written estimate. "
        "Based in Goodwood, working across Cape Town.", body,
        schema=business_schema(), crumbs=[("Contact", "/contact")],
    )


FORM_FIELDS = """
<div class="form-card reveal">
  <form id="estimate-form" action="https://wa.me/27661505770" method="POST">
    <div class="two">
      <div><label for="name">Your name</label><input id="name" name="name" type="text" required></div>
      <div><label for="phone">Phone or WhatsApp</label><input id="phone" name="phone" type="tel" required></div>
    </div>
    <div><label for="email">Email</label><input id="email" name="email" type="email"></div>
    <div><label for="suburb">Suburb</label><input id="suburb" name="suburb" type="text"></div>
    <div><label for="service">What do you need</label>
      <select id="service" name="service">
        <option>Waterproofing</option><option>Damp proofing</option><option>Painting</option>
        <option>Kitchen renovation</option><option>Bathroom renovation</option>
        <option>Home renovation</option><option>Plastering</option><option>Extension</option>
        <option>Not sure yet</option>
      </select></div>
    <div><label for="details">Tell us about the job</label>
      <textarea id="details" name="details" rows="5" placeholder="What needs doing, how big it is, and when you would like it done."></textarea></div>
    <button class="btn btn-gold" type="submit" style="width:100%">Send on WhatsApp</button>
    <p class="table-note wa-note">This opens WhatsApp with your details written out. Nothing is sent until you press send there. Rather talk? Call 066 150 5770.</p>
  </form>
</div>
<script src="form-whatsapp.js?v=1" defer></script>
"""


def build_estimate():
    body = page_hero(
        "Free Estimate", "Get a Free Written Estimate",
        "Tell us about your project and we will follow up to schedule a walkthrough. Every "
        "estimate is detailed, written and flat-rate.", kicker="No Obligation · Flat-Rate Pricing",
    )
    body += section(
        head("01", "Request", "Project details") + FORM_FIELDS
        + '<div class="why" style="margin-top:48px"><div class="reveal">'
        + ticks(["A walkthrough, not a phone guess",
                 "Scope, materials and total price in writing",
                 "The number on the estimate is the number you pay"])
        + "</div>" + checklist("What happens next", [f["title"] + ": " + f["text"] for f in
                                                     [{"title": t, "text": d} for t, d in FLOW]])
        + "</div>",
        cls="ghost",
    )
    return page(
        "estimate", "Free Renovation Estimate Cape Town | Plinth",
        "Request a free written, flat-rate estimate for renovations, waterproofing or painting in "
        "Cape Town. We reply within one business day.", body,
        crumbs=[("Free Estimate", "/estimate")],
    )


def build_faq():
    items = [(f["q"], f["a"]) for f in HOME["faq"]]
    items += [
        ("Which areas do you cover?",
         "Cape Town within about 25km of Goodwood, including Durbanville, Bellville, Parow, "
         "Table View, Brackenfell and the Southern Suburbs. Stellenbosch and Somerset West by "
         "arrangement for larger renovations."),
        ("Do you do small jobs?",
         "Yes. A leaking parapet, one bathroom or a repaint is normal work for us. Small jobs are "
         "usually quoted flat-rate after photos or a short visit."),
        ("Can you work while we live in the house?",
         "Yes, most renovations are done with the family in place. We seal off work areas, tidy "
         "daily and keep water and power interruptions to agreed windows."),
    ]
    body = page_hero("FAQ", "Cape Town Renovation FAQ",
                     "Straight answers about cost, areas, timelines and how we work.", kicker="Questions")
    body += section(
        head("01", "FAQ", "The questions we get asked most") + faq(items)
        + cta_band("Still unsure?", "Call and describe the problem. We will tell you what it needs."),
    )
    schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }
    return page("faq", "Renovation FAQ Cape Town | Plinth Renovations",
                "Cost, areas, timelines and guarantees: the questions Cape Town homeowners ask "
                "before a renovation.", body, schema=schema, crumbs=[("FAQ", "/faq")])


def build_simple(slug, crumb, title_tag, meta, h1, paras, priority=0.5):
    body = page_hero(crumb, h1, "", kicker=crumb)
    body += section('<div class="prose reveal">' + "".join(f"<p>{escape(p)}</p>" for p in paras) + "</div>")
    return page(slug, title_tag, meta, body, crumbs=[(crumb, f"/{slug}")])


def build_thankyou():
    body = '<section class="hero"><div class="wrap"><div class="kicker reveal">Thank you</div>' \
           '<h1 class="reveal">We have your details</h1>' \
           '<p class="lead reveal">We reply within one business day. If it is urgent, call us and ' \
           'we will pick up during working hours.</p>' \
           f'<div class="hero-actions reveal"><a class="btn btn-gold" href="tel:{TEL}">{PHONE}</a>' \
           '<a class="btn btn-ghost" href="/">Back to home</a></div></div></section>'
    return page("thank-you", "Thank You | Plinth Renovations",
                "Your project details have been received.", body)


def build_404():
    body = '<section class="hero"><div class="wrap"><div class="kicker reveal">404</div>' \
           '<h1 class="reveal">That page is not here</h1>' \
           '<p class="lead reveal">The link may be old, or the page may have moved. The home page ' \
           'and the services list are the best places to restart.</p>' \
           '<div class="hero-actions reveal"><a class="btn btn-gold" href="/">Home</a>' \
           '<a class="btn btn-ghost" href="/services">Services</a></div></div></section>'
    html = page("404", "Page Not Found | Plinth Renovations",
                "That page does not exist.", body)
    return html.replace('<meta name="robots"', '<meta name="robots"') .replace(
        "</head>", '<meta name="robots" content="noindex, follow">\n</head>')


# ---------------------------------------------------------------- main

def copy_assets():
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.html"):
        stale.unlink()
    shutil.rmtree(OUT / "assets", ignore_errors=True)
    shutil.rmtree(OUT / "images", ignore_errors=True)
    (OUT / "images").mkdir()
    shutil.copyfile(ORIG / "styles.css", OUT / "styles.css")
    shutil.copyfile(ORIG / "script.js", OUT / "script.js")
    shutil.copyfile(SRC / "extra.css", OUT / "extra.css")
    shutil.copyfile(SRC / "assets" / "form-whatsapp.js", OUT / "form-whatsapp.js")
    shutil.copyfile(ORIG / "logo.jpg", OUT / "logo.jpg")
    # the source file is 4.2 MB for five seconds; the re-encode is 395 KB at
    # SSIM 0.979, which is visually the same clip over a hero-sized video tag
    # 301s from the old plinthrenovations.co.za URLs, in place for the day this
    # domain moves here: gallery and projects both become /our-work, the stub
    # blog folds into /faq, and the rest keep their meaning.
    (OUT / "_redirects").write_text(
        "\n".join([
            "# old site -> this site (active only once the domain points here)",
            "/index.html            /                301",
            "/about.html            /about           301",
            "/services.html         /services        301",
            "/estimate.html         /estimate        301",
            "/faq.html              /faq             301",
            "/areas.html            /service-areas   301",
            "/gallery.html          /our-work        301",
            "/projects.html         /our-work        301",
            "/blog.html             /faq             301",
            "/areas                 /service-areas   301",
            "/gallery               /our-work        301",
            "/projects              /our-work        301",
            "/blog                  /faq             301",
            "",
            "# compact keyword renames, 2026-11-09",
            "/waterproofing              /waterproofing-cape-town           301",
            "/waterproofing.html         /waterproofing-cape-town           301",
            "/painting                   /painters-cape-town                301",
            "/painting.html              /painters-cape-town                301",
            "/plastering                 /plastering-cape-town              301",
            "/plastering.html            /plastering-cape-town              301",
            "/kitchens                   /kitchen-renovations-cape-town     301",
            "/kitchens.html              /kitchen-renovations-cape-town     301",
            "/kitchen-renovations        /kitchen-renovations-cape-town     301",
            "/kitchen-renovations.html   /kitchen-renovations-cape-town     301",
            "/bathrooms                  /bathroom-renovations-cape-town    301",
            "/bathrooms.html             /bathroom-renovations-cape-town    301",
            "/bathroom-renovations       /bathroom-renovations-cape-town    301",
            "/bathroom-renovations.html  /bathroom-renovations-cape-town    301",
            "/home-renovations           /home-renovations-cape-town        301",
            "/home-renovations.html      /home-renovations-cape-town        301",
            "",
            "# no measured demand: folded into a survivor",
            "/damp-proofing              /waterproofing-cape-town           301",
            "/damp-proofing.html         /waterproofing-cape-town           301",
            "/home-extensions            /home-renovations-cape-town        301",
            "/home-extensions.html       /home-renovations-cape-town        301",
            "",
            "# retired area pages",
            "",
        ]),
        encoding="utf-8",
    )

    vid = SRC / "assets" / "hero-video.mp4"
    shutil.copyfile(vid if vid.exists() else ORIG / "hero-video.mp4", OUT / "hero-video.mp4")
    # only the photos this build actually points at
    img_names = ([photos.HERO["file"]] + [ph["file"] for ph in photos.PHOTOS]
                 + [ph["file"] for ph in photos.STOCK] + [name for name, _ in LIBRARY]
                 + ["IMG-20260902-WA0017.jpg"])
    for name in img_names:
        src = SRC / "_images" / name
        if not src.exists():
            src = ORIG / "images" / name
        if src.exists():
            shutil.copyfile(src, OUT / "images" / name)
        else:
            print("missing image:", name)


def write_sitemap(slugs, images=None):
    """Image entries are declared per URL so the photographs are indexed too."""
    images = images or {}
    rows = []
    for slug, prio in slugs:
        loc = f"{DOMAIN}/{slug}" if slug else DOMAIN + "/"
        inner = "".join(
            f"<image:image><image:loc>{DOMAIN}/images/{f}</image:loc></image:image>"
            for f in images.get(slug, [])
        )
        rows.append(f"  <url><loc>{loc}</loc><priority>{prio}</priority>{inner}</url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


def write_headers():
    (OUT / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  X-Frame-Options: DENY\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
        "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; script-src 'self'; "
        "frame-ancestors 'none'; base-uri 'self'; form-action 'self'\n"
        "\n/images/*\n  Cache-Control: public, max-age=31536000, immutable\n"
        "\n/styles.css\n  Cache-Control: public, max-age=3600\n",
        encoding="utf-8")


def main():
    copy_assets()
    pages = []

    pages.append(("", build_home(), "1.0"))
    pages.append(("services", build_services(), "0.9"))
    for svc in SERVICES:
        pages.append((svc["slug"], build_service(svc), "0.9"))
    pages.append(("solutions", build_solutions(), "0.8"))
    for a in AREA_PAGES:
        pages.append((a["slug"], build_coverage_area(a), "0.6"))
    pages.append(("our-work", build_work(), "0.7"))
    pages.append(("service-areas", build_areas_index(), "0.7"))
    pages.append(("about", build_about(), "0.6"))
    pages.append(("contact", build_contact(), "0.7"))
    pages.append(("estimate", build_estimate(), "0.9"))
    pages.append(("faq", build_faq(), "0.6"))
    pages.append(("thank-you", build_thankyou(), "0.2"))
    pages.append(("privacy", build_simple(
        "privacy", "Privacy", "Privacy Policy | Plinth Renovations",
        "How Plinth Renovations handles your personal information under POPIA.",
        "Privacy Policy",
        ["We collect your name, contact details and the description of the work you ask us to "
         "quote on. We use it to prepare the estimate and to carry out the work, and for nothing else.",
         "We do not sell or rent your information. Quote requests are kept only as long as needed "
         "to answer them and to keep a record of work done.",
         f"You can ask us what we hold about you, or ask us to delete it, by calling {PHONE}.",
         f"Information officer: Plinth Renovations and Construction, {STREET}, {CITY}."]), "0.2"))
    pages.append(("terms", build_simple(
        "terms", "Terms", "Terms of Use | Plinth Renovations",
        "The terms that apply to this website and to estimates issued by Plinth Renovations.",
        "Terms of Use",
        ["This website describes our services and lets you request a free written estimate. It is "
         "not a contract for work.",
         "An estimate becomes binding only when it is issued in writing, accepted by you, and the "
         "scope is agreed by both sides. Site conditions found after work starts may change scope, "
         "and changes are agreed in writing before they are carried out.",
         "All photographs on this site show work by Plinth Renovations and Construction."]), "0.2"))
    pages.append(("disclaimer", build_simple(
        "disclaimer", "Disclaimer", "Disclaimer | Plinth Renovations",
        "Guidance on this site is general information, not a diagnosis of your property.",
        "Disclaimer",
        ["The guidance on this site is general. Damp, structural and waterproofing problems can "
         "look identical on the surface and have different causes underneath.",
         "Nothing here replaces an on-site assessment. We give recommendations only after looking "
         "at the property."]), "0.2"))
    pages.append(("accessibility", build_simple(
        "accessibility", "Accessibility", "Accessibility | Plinth Renovations",
        "How this site is built for keyboard, screen reader and low-bandwidth use.",
        "Accessibility",
        ["This site uses semantic HTML, a visible focus state and text that can be resized to "
         "200% without losing content.",
         "Images carry descriptive alternative text. Video is muted, decorative and does not carry "
         "information you need in order to use the site.",
         f"If something is hard to use, call {PHONE} and we will take the details by phone."]), "0.2"))
    pages.append(("404", build_404(), "0.1"))

    for slug, html, _ in pages:
        (OUT / (f"{slug}.html" if slug else "index.html")).write_text(html, encoding="utf-8")

    img_map = {"our-work": [ph["file"] for ph in photos.PHOTOS] + [photos.HERO["file"]]}
    for svc in SERVICES:
        slug = svc["slug"]
        pics = [ph["file"] for ph in photos.PHOTOS if ph["service"] == PHOTO_KEY.get(svc["key"], "waterproofing")]
        if pics:
            img_map[slug] = pics
    write_sitemap([(s, p) for s, _, p in pages if s not in ("404", "thank-you")], img_map)
    write_headers()
    print(f"built {len(pages)} pages")


if __name__ == "__main__":
    main()
