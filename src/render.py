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
import ui
from ui import (
    BUSINESS, CITY, DOMAIN, PHONE, STREET, TEL,
    card, checklist, cta_band, faq, floaters, footer, gallery, grid, head, header,
    hero, page_hero, section, steps, ticks, topbar,
)

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
OUT = ROOT / "site-output"
ORIG = Path(r"C:\Users\DELL\OneDrive\Desktop\PLINTH")

content = json.loads((SRC / "content.json").read_text(encoding="utf-8"))

SERVICES = content["services"]
AREAS = content["areas"]
HOME = content["home"]
SITE = content["site"]

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
    slug = re.sub(r"[^a-z0-9]+", "-", svc["name"].lower()).strip("-")
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
    cards = [
        card(TAG_FOR[s["name"]], s["name"], s["teaser"], f'/{slugify(s["name"])}',
             icon=ICON_FOR[s["name"]])
        for s in SERVICES
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
        card("Service area", a["name"], a["teaser"], f'/home-renovations-in-{slugify(a["name"])}',
             link_label="See this area", icon=None)
        for a in AREAS
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
        card(TAG_FOR[s["name"]], s["name"], s["teaser"], f'/{slugify(s["name"])}',
             icon=ICON_FOR[s["name"]])
        for s in SERVICES
    ]
    cards.append(card("Not sure", "Not sure what it needs?",
                      "Send photos and we will tell you which of these applies, and what it "
                      "should cost, before you commit.", "/estimate",
                      link_label="Send photos", icon=None))
    body = page_hero(
        "Services", "Renovation and Waterproofing Services in Cape Town",
        "Eight services, one crew, one written scope. Every job includes a free written estimate "
        "and a fixed price before work starts.", kicker="No Obligation · Flat-Rate Pricing",
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
    slug = slugify(svc["name"])
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
        svc["name"], lead["h1"], lead["cta_line"], kicker=lead["eyebrow"],
    )
    svc_photos = [ph for ph in photos.PHOTOS + photos.STOCK if ph["service"] == slug]
    body += section(
        head("01", svc["name"], svc["intro_heading"])
        + f'<div class="prose reveal"><p>{escape(svc["intro_body"])}</p></div>'
        + (gallery(svc_photos, layout="single" if len(svc_photos) == 1 else "pair") if svc_photos else "")
    )
    body += section(
        head("02", "What it covers", svc["detail_heading"], svc["detail_intro"]) + grid(sub_cards),
        cls="ghost",
    )
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
    area_links = "".join(
        f'<a class="btn btn-ghost" style="margin:0 8px 12px 0" href="/home-renovations-in-{slugify(a["name"])}">'
        f'{escape(a["name"])}</a>' for a in AREAS
    )
    body += section(
        head("05", "Where we work", f'{svc["name"]} across Cape Town',
             "We are based in Goodwood and cover Cape Town within about 25km.")
        + f'<div class="reveal">{area_links}</div>'
    )
    return page(
        slug, svc["title_tag"], svc["meta_description"], body,
        schema=service_schema(svc), crumbs=[("Services", "/services"), (svc["name"], f"/{slug}")],
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


def build_areas_index():
    cards = [
        card("Service area", a["name"], a["teaser"], f'/home-renovations-in-{slugify(a["name"])}',
             link_label="See this area", icon=None)
        for a in AREAS
    ]
    nearby = [
        "Goodwood", "Richmond Estate", "Monte Vista", "Edgemead", "Bothasig",
        "Milnerton", "Century City", "Plattekloof", "Kuils River", "Bloubergstrand",
        "Bellville", "Durbanville", "Parow", "Table View", "Brackenfell", "Stellenbosch",
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
             "No separate page for these suburbs, but we work there regularly.")
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
            "",
        ]),
        encoding="utf-8",
    )

    vid = SRC / "assets" / "hero-video.mp4"
    shutil.copyfile(vid if vid.exists() else ORIG / "hero-video.mp4", OUT / "hero-video.mp4")
    # only the photos this build actually points at
    img_names = ([photos.HERO["file"]] + [ph["file"] for ph in photos.PHOTOS]
                 + [ph["file"] for ph in photos.STOCK] + ["IMG-20260902-WA0017.jpg"])
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
        pages.append((slugify(svc["name"]), build_service(svc), "0.9"))
    pages.append(("our-work", build_work(), "0.7"))
    pages.append(("service-areas", build_areas_index(), "0.7"))
    for area in AREAS:
        pages.append((f'home-renovations-in-{slugify(area["name"])}', build_area(area), "0.8"))
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
        slug = slugify(svc["name"])
        pics = [ph["file"] for ph in photos.PHOTOS if ph["service"] == slug]
        if pics:
            img_map[slug] = pics
    write_sitemap([(s, p) for s, _, p in pages if s not in ("404", "thank-you")], img_map)
    write_headers()
    print(f"built {len(pages)} pages")


if __name__ == "__main__":
    main()
