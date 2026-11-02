"""Finishing pass for the generated Plinth microsite.

The builder emits 12 generic "Content coming soon" stubs and no schema, no social
tags and no security headers. This script keeps the builder's own markup and
chrome, then does exactly what the locksmith build did by hand:

  - writes the real About / Contact / FAQ / legal pages
  - rebuilds the two thin hub pages (services, service-areas)
  - adds JSON-LD, Open Graph, Twitter cards, fonts, favicon
  - moves the inline nav handler into main.js so the CSP can stay strict
  - strips .html from internal links and canonicals
  - emits sitemap.xml, robots.txt, _headers, _redirects and a real 404
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SITE = "https://plinth-renovations-cape-town.pages.dev"
ROOT = Path(r"C:\Users\DELL\OneDrive\Desktop\Plinth Microsite\site-output")
SRC = Path(r"C:\Users\DELL\OneDrive\Desktop\Plinth Microsite\src")
BUILD_TS = datetime.now().strftime("%Y%m%d%H%M")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

content = json.loads((SRC / "content.json").read_text(encoding="utf-8"))
inputs = json.loads((SRC / "site-inputs.json").read_text(encoding="utf-8"))

BUSINESS_NAME = "Plinth Renovations and Construction"
PHONE = "+27661505770"
SERVICE_NAMES = [s["name"] for s in content["services"]]
AREA_NAMES = [a["name"] for a in content["areas"]]

# ---------------------------------------------------------------- shell

home_html = (ROOT / "index.html").read_text(encoding="utf-8")
i_body = home_html.index("<body>") + len("<body>")
i_header_end = home_html.index("</header>") + len("</header>")
i_footer = home_html.index("<footer")
HEAD = home_html[:i_body] + home_html[i_body:i_header_end]
HEAD = HEAD.replace(
    '<button class="nav__toggle" aria-label="Menu" onclick="document.getElementById(\'navlinks\').classList.toggle(\'open\')">&#9776;</button>',
    '<button class="nav__toggle" id="navToggle" aria-label="Menu" aria-controls="navlinks" aria-expanded="false">&#9776;</button>',
)
FOOT = home_html[i_footer:]
FOOT = FOOT.replace('<script src="assets/main.js"></script>', f'<script src="assets/main.js?v={BUILD_TS}"></script>')
# no thin team/careers pages for a company this size: those links go to About
FOOT = FOOT.replace('<li><a href="meet-the-team.html">Meet the Team</a></li>', "")
FOOT = FOOT.replace('<li><a href="careers.html">Careers</a></li>', "")


def page(slug, title, desc, body):
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{desc}">', head, flags=re.S)
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="{SITE}/{slug}">', head, flags=re.S)
    return head + body + FOOT


def section(inner, alt=False):
    cls = "section section--alt" if alt else "section"
    return f'<section class="{cls}"><div class="wrap">{inner}</div></section>'


def cta(heading="Get a free written estimate", text="Tell us what the house is doing and we will tell you what it needs."):
    return (f'<section class="cta-band"><div class="wrap"><h2>{heading}</h2><p>{text}</p>'
            f'<p style="margin-top:20px"><a class="btn btn--lg" href="tel:{PHONE}">Call 066 150 5770</a></p>'
            f'<p class="muted" style="color:rgba(255,255,255,.8);margin-top:10px">Free - no obligations</p></div></section>')


def links(items):
    return '<ul class="linklist">' + "".join(f'<li><a href="{s}">{n}</a></li>' for s, n in items) + "</ul>"


def faq_html(items):
    return ('<div class="faq" style="max-width:820px;margin:28px auto 0">'
            + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
            + "</div>")


SERVICE_LINKS = [(f"/{s.lower().replace(' ', '-')}", s) for s in SERVICE_NAMES]

# ---------------------------------------------------------------- custom pages

ABOUT = page(
    "about",
    "About Plinth Renovations | Cape Town Builders in Goodwood",
    "Plinth Renovations and Construction is a Cape Town renovation company based in Goodwood. One team, written scope, and the water diagnosed first.",
    section(
        "<h1>About Plinth Renovations and Construction</h1>"
        '<div class="section__lead"><p>We are a renovation and construction company based at 64 Oxford Street in Richmond Estate, Goodwood, on the northern side of Cape Town. We work on houses and apartments within about 25 km of that base.</p></div>'
    )
    + section(
        "<h2>Why we start with the water</h2>"
        "<p>A renovation is a finish over a structure, and in Cape Town that structure spends four months a year being rained on sideways. We have seen too many bathrooms retiled over a failed membrane, and too many walls repainted over rising damp, to sell a finish without looking underneath it first.</p>"
        "<p>So the first hour of a job is diagnosis. Where does the water enter? Is the damp rising, penetrating or condensing? Is the wall that is coming out carrying anything? Those answers decide the quote, and they decide whether the job lasts.</p>",
        alt=True,
    )
    + section(
        "<h2>How we work</h2>"
        '<div class="grid grid--2" style="margin-top:24px">'
        '<div class="card"><h3>One point of contact</h3><p>The person who quotes your job is the person on site while it runs, and the person you call with a question.</p></div>'
        '<div class="card"><h3>Written scope and sequence</h3><p>What is included, what is excluded, what order it happens in, and what it will cost, before demolition starts.</p></div>'
        '<div class="card"><h3>Our own trades</h3><p>The people on your job are people we work with every week, not whoever is available on the morning.</p></div>'
        '<div class="card"><h3>Lived-in houses</h3><p>Sheeting, daily clean-up and a plan for the room your family still has to use.</p></div>'
        "</div>"
    )
    + section(
        "<h2>What we do</h2>"
        '<p>Renovations, waterproofing, damp repair, painting, plastering, kitchens, bathrooms and extensions. Most jobs combine two or three of them.</p>'
        f'<div style="margin-top:24px">{links(SERVICE_LINKS)}</div>',
        alt=True,
    )
    + cta(),
)

CONTACT = page(
    "contact",
    "Contact Plinth Renovations | Goodwood, Cape Town",
    "Call 066 150 5770 or send an estimate request. Plinth Renovations and Construction, 64 Oxford Street, Richmond Estate, Goodwood, Cape Town.",
    section(
        "<h1>Contact Plinth Renovations</h1>"
        '<div class="section__lead"><p>The fastest way to reach us is the phone. If we are on a site we will call you back the same day.</p></div>'
        '<div class="grid grid--2" style="margin-top:28px">'
        f'<div class="card"><h3>Call</h3><p><a class="wc-phone" href="tel:{PHONE}"><strong>066 150 5770</strong></a></p><p>Mon to Fri, 7AM to 6PM. Saturday, 8AM to 2PM.</p></div>'
        "<div class=\"card\"><h3>Visit</h3><p>64 Oxford Street<br>Richmond Estate<br>Goodwood<br>Cape Town, 7460</p><p>Please call before coming, as we are often on site.</p></div>"
        '<div class="card"><h3>Estimates</h3><p>Free written estimates after a site visit, anywhere within about 25 km of Goodwood.</p><p><a href="/estimate">Request an estimate</a></p></div>'
        '<div class="card"><h3>Areas</h3><p>Northern Suburbs, City Bowl, Atlantic Seaboard and Southern Suburbs. Stellenbosch and Somerset West by arrangement.</p><p><a href="/service-areas">See service areas</a></p></div>'
        "</div>"
    )
    + section(
        "<h2>What to have ready when you call</h2>"
        "<p>You do not need plans or a specification. It helps if you can tell us the age of the house, what the problem looks like and when it started, and whether the work has been attempted before. If you have photos, send them. If the ceiling is open or the tiles are off, that is the best time for us to see it.</p>"
        "<p>For bigger jobs, we will book a site visit at a time that suits you and walk the whole property rather than only the room you mentioned. Most surprises in a renovation are two rooms away from the symptom.</p>",
        alt=True,
    )
    + cta(),
)

FAQ_ITEMS = [
    ("How much does a renovation cost in Cape Town?",
     "It depends on the scope, and a firm price per square metre before anyone has seen the house is a guess. We visit, measure and open what needs opening, then give you one written estimate with the essential work and the optional work separated."),
    ("Do you charge for a site visit or an estimate?",
     "No. The site visit and the written estimate are free within our normal working area of about 25 km around Goodwood."),
    ("Do you handle waterproofing and damp as part of a renovation?",
     "Yes, and we treat it as the first job rather than a line item at the end. A bathroom or kitchen quote that ignores the roof above it is a quote we would not sign ourselves."),
    ("How long does a bathroom or kitchen take?",
     "We give you a date range in the written quote, based on the actual scope. We do not publish a standard number, because a bathroom that needs a drain moved is a different job from one that does not."),
    ("Can I stay in the house while you work?",
     "Usually yes. We sheet off the work area, plan around the bathroom or kitchen you still need, and clean up at the end of each day."),
    ("Do you take on small jobs?",
     "Yes. A leaking parapet, one room painted, a ceiling patch, one shower that has to be redone. Small jobs are often how we meet the owners we later build for."),
    ("Do I need plans or council approval?",
     "Structural work, alterations and additions usually need approval from the City of Cape Town before work starts. We tell you when it applies, and we can work with your architect or draughtsman."),
    ("How do payments work?",
     "Staged against progress and set out in the quote before we start. We do not ask for the whole job upfront."),
    ("What happens if you find something unexpected once the walls are open?",
     "We stop, show you, and price it as a separate agreed item before continuing. You will never get an invoice for work you did not approve."),
    ("Do you work outside Cape Town?",
     "Stellenbosch and Somerset West by arrangement for larger jobs. Our normal working radius is about 25 km around Goodwood."),
    ("Do you supply materials or do I?",
     "Either, as long as it is agreed in writing before the job starts. If you supply, we will tell you the specification we need and the delivery date the programme depends on."),
    ("Are you insured?",
     "Ask us on the call and we will confirm our current cover in writing. We would rather answer that question directly than put a badge on a website."),
]

FAQ = page(
    "faq",
    "Renovation FAQ | Plinth Renovations Cape Town",
    "Straight answers on renovation costs, timelines, waterproofing, damp, approvals and payments from a Cape Town renovation company.",
    section("<h1>Questions we get asked</h1>"
            '<div class="section__lead"><p>If your question is not here, call 066 150 5770 and ask it directly.</p></div>'
            + faq_html(FAQ_ITEMS))
    + cta(),
)

THANK_YOU = page(
    "thank-you",
    "Thank You | Plinth Renovations Cape Town",
    "Your estimate request has been received. We will call you back to arrange a site visit.",
    section("<h1>Thank you, we have your request</h1>"
            '<div class="section__lead"><p>We will call you back to arrange a site visit. If you would rather not wait, call us on <a class="wc-phone" href="tel:+27661505770">066 150 5770</a>.</p></div>'
            "<h2>What happens next</h2>"
            "<p>We will ask a few questions about the house and the work, then book a time to see it. The visit takes about an hour on a normal renovation and longer on a whole-house job. You get a written estimate afterwards, with the essential work and the optional work separated.</p>"
            "<p>If you have photos, or the ceiling is already open, have them ready. It shortens the diagnosis.</p>")
    + cta("Something urgent?", "A leak that is running right now is worth a phone call rather than a form."),
)

PRIVACY = page(
    "privacy-policy",
    "Privacy Policy | Plinth Renovations Cape Town",
    "How Plinth Renovations and Construction collects, uses and stores your personal information, in line with South Africa's POPIA.",
    section("<h1>Privacy policy</h1>"
            '<div class="section__lead"><p>This policy explains what we do with the information you give us. It follows the Protection of Personal Information Act (POPIA).</p></div>'
            "<h2>What we collect</h2>"
            "<p>Only what you send us: your name, phone number, email address, the address of the property, and what you tell us about the work. If you call, we may keep a note of the conversation so the quote is accurate.</p>"
            "<h2>Why we collect it</h2>"
            "<p>To reply to your enquiry, to quote, to do the work, and to keep a record of what was agreed. We do not sell your information and we do not add you to a mailing list you did not ask for.</p>"
            "<h2>Who sees it</h2>"
            "<p>Us, and the people working on your job. Our website and form provider process the submission on our behalf. We do not pass your details to other contractors or lead buyers.</p>"
            "<h2>How long we keep it</h2>"
            "<p>Enquiries that do not become jobs are kept only as long as needed to answer you. Job records are kept for as long as we may need them for accounting and for standing behind our work.</p>"
            "<h2>Your rights</h2>"
            "<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it where we are not required to keep it. Call <a class=\"wc-phone\" href=\"tel:+27661505770\">066 150 5770</a> and ask.</p>"
            "<h2>Cookies</h2>"
            "<p>This site does not set advertising cookies. If we add call or visit analytics later, this page will say what it does and what it stores.</p>")
)

TERMS = page(
    "terms-conditions",
    "Terms and Conditions | Plinth Renovations Cape Town",
    "The terms that apply to estimates, quotations and building work carried out by Plinth Renovations and Construction in Cape Town.",
    section("<h1>Terms and conditions</h1>"
            '<div class="section__lead"><p>These terms apply to estimates and work carried out by Plinth Renovations and Construction. The written quote for your job sets out the scope, the price and the programme, and takes precedence over anything discussed verbally.</p></div>'
            "<h2>Estimates and quotes</h2>"
            "<p>An estimate is our best view of cost before work starts. A quote is a price for a defined scope. Where the scope changes, the price changes, and we will agree the change with you in writing before carrying it out.</p>"
            "<h2>Scope and variations</h2>"
            "<p>The written scope lists what is included and what is excluded. Work not listed is not included. If we open a wall or a ceiling and find a condition that could not reasonably have been seen before, we will show you, price it separately, and wait for your instruction.</p>"
            "<h2>Payment</h2>"
            "<p>Payments are staged against progress and set out in the quote. Materials ordered specifically for your job may require a deposit. We do not ask for the full job upfront.</p>"
            "<h2>Access and site conditions</h2>"
            "<p>You agree to give us reasonable access to the property, water and power during working hours. Delays caused by access, by other contractors, by material shortages or by weather are not a breach, and the programme is adjusted accordingly.</p>"
            "<h2>Materials</h2>"
            "<p>Where we supply, we supply the specification in the quote. Where you supply, you are responsible for the specification, the quantity and the delivery date the programme depends on. Substitutions require our agreement.</p>"
            "<h2>Workmanship</h2>"
            "<p>The work is carried out with reasonable skill and care by people competent to do it. Defects reported within a reasonable time of completion will be assessed and put right where they are down to our workmanship.</p>"
            "<h2>Cancellation</h2>"
            "<p>Either party may cancel in writing. You remain liable for work done, materials ordered and costs committed up to the date of cancellation.</p>"
            "<h2>Liability</h2>"
            "<p>We are not liable for pre-existing defects in the structure or services that were not part of the agreed scope, or for loss caused by events outside our control.</p>")
)

DISCLAIMER = page(
    "disclaimer",
    "Disclaimer | Plinth Renovations Cape Town",
    "The information on this site is general guidance about renovation work in Cape Town. It is not a substitute for a site-specific assessment.",
    section("<h1>Disclaimer</h1>"
            '<div class="section__lead"><p>The information on this site is general guidance about renovation, waterproofing and damp repair in Cape Town. It is written from our own experience and it is not a substitute for an assessment of your property.</p></div>'
            "<h2>No professional advice</h2>"
            "<p>Nothing here is engineering, architectural, legal or financial advice. Structural work, alterations and additions should be assessed on site and, where required, signed off by a competent person and approved by the City of Cape Town.</p>"
            "<h2>Costs and timelines</h2>"
            "<p>Where we refer to market price ranges, those are ranges published by Cape Town contractors in 2026 for context. They are not a quote from us and they are not a promise of what your job will cost. A written estimate follows a site visit.</p>"
            "<h2>Photographs</h2>"
            "<p>Photographs on this site show work carried out by Plinth Renovations and Construction. They are not stock images and they are not representative of every job.</p>"
            "<h2>External links</h2>"
            "<p>Where we link to another site, we do not control its content and we are not responsible for it.</p>")
)

ACCESSIBILITY = page(
    "accessibility",
    "Accessibility | Plinth Renovations Cape Town",
    "How this website is built for accessibility, what we know is still imperfect, and how to tell us about a barrier.",
    section("<h1>Accessibility</h1>"
            '<div class="section__lead"><p>We want this site to be usable by everyone, including people using a screen reader, a keyboard only, or larger text.</p></div>'
            "<h2>What we have done</h2>"
            "<p>The site uses real headings in order, descriptive alternative text on images, labelled form fields, visible focus states, and colour combinations chosen for contrast rather than fashion. The navigation works with a keyboard and the page does not depend on hover to reveal content.</p>"
            "<h2>What we know is not perfect</h2>"
            "<p>The site has not been through a formal WCAG audit. Some photographs of work in progress are low light and their descriptions are necessarily brief. The phone number is the primary contact and it is available on every page.</p>"
            "<h2>Tell us</h2>"
            "<p>If something on this site is difficult for you to use, call <a class=\"wc-phone\" href=\"tel:+27661505770\">066 150 5770</a> and tell us what happened. We will fix what we can and we will give you the information another way in the meantime.</p>")
)

COMPLAINTS = page(
    "complaints-policy",
    "Complaints Policy | Plinth Renovations Cape Town",
    "How to raise a concern about work carried out by Plinth Renovations and Construction, and what happens after you do.",
    section("<h1>Complaints policy</h1>"
            '<div class="section__lead"><p>If something is not right, tell us early. Almost every complaint we can fix is cheaper and faster to fix while we are still on site.</p></div>'
            "<h2>How to raise it</h2>"
            "<p>Call <a class=\"wc-phone\" href=\"tel:+27661505770\">066 150 5770</a>, or write to us at 64 Oxford Street, Richmond Estate, Goodwood, Cape Town, 7460. Tell us the address, what is wrong and when you first noticed it. Photographs help.</p>"
            "<h2>What happens next</h2>"
            "<p>We will acknowledge your complaint and tell you who is handling it. We will inspect the work, and where the fault is ours we will put it right. Where the cause is outside our scope, we will explain what we found and what the correct repair is.</p>"
            "<h2>If we cannot agree</h2>"
            "<p>We will set out our position in writing, including what we inspected and what we found, so that you have a clear record to take further if you choose to.</p>")
)

REFERRAL = page(
    "referral-marketing-disclosure",
    "Referral Marketing Disclosure | Plinth Renovations Cape Town",
    "How this website is operated, and our position on referral fees and paid recommendations.",
    section("<h1>Referral marketing disclosure</h1>"
            '<div class="section__lead"><p>This website is operated by Plinth Renovations and Construction to describe our own work and to take enquiries for it.</p></div>'
            "<h2>No undisclosed referral fees</h2>"
            "<p>We do not accept payment to recommend another company on this site, and we do not pay other websites to present our work as their own. If that ever changes, it will be disclosed on the page where it appears.</p>"
            "<h2>Recommendations we make</h2>"
            "<p>Where we suggest another trade, an engineer or a supplier, it is because we have worked with them, not because we are paid to. We will tell you if we ever stand to benefit from a recommendation.</p>")
)

# ---------------------------------------------------------------- hub pages

SERVICE_CARDS = "".join(
    f'<div class="card"><h3><a href="/{s["name"].lower().replace(" ", "-")}">{s["name"]}</a></h3>'
    f'<p>{s["meta_description"].split(".")[0]}.</p>'
    f'<a href="/{s["name"].lower().replace(" ", "-")}">Learn more &rarr;</a></div>'
    for s in content["services"]
)

SERVICES_INDEX = page(
    "services",
    "Renovation Services Cape Town | Plinth Renovations",
    "Waterproofing, damp proofing, painting, kitchens, bathrooms, home renovations, plastering and extensions across Cape Town. One team, written scope.",
    section("<h1>Renovation services in Cape Town</h1>"
            '<div class="section__lead"><p>Eight services, one team, one written scope. Most jobs combine two or three of them, and the order they happen in is part of the quote.</p></div>'
            f'<div class="grid grid--3" style="margin-top:28px">{SERVICE_CARDS}</div>')
    + section("<h2>Not sure which one you need?</h2>"
              "<p>That is normal. A damp patch on a bedroom wall can be a roof leak, a failed damp course or a ventilation problem, and each has a different repair. Call us, describe it, and we will tell you what we would check first. The site visit is free.</p>",
              alt=True)
    + cta(),
)

AREA_ROWS = "".join(
    f'<div class="card"><h3><a href="/home-renovations-in-{a["name"].lower().replace(" ", "-")}">{a["name"]}</a></h3>'
    f'<p>{a["meta_description"]}</p></div>'
    for a in content["areas"]
)

OTHER_SUBURBS = [
    "Goodwood", "Richmond Estate", "Monte Vista", "Edgemead", "Bothasig",
    "Plattekloof", "Milnerton", "Kuils River", "Century City", "Bloubergstrand",
    "Rondebosch", "Claremont", "Wynberg", "Tokai", "Constantia", "Stellenbosch", "Somerset West",
]

AREAS_INDEX = page(
    "service-areas",
    "Service Areas | Plinth Renovations Cape Town",
    "Plinth Renovations works across Cape Town from a Goodwood base: Northern Suburbs, City Bowl, Atlantic Seaboard and Southern Suburbs, within about 25 km.",
    section("<h1>Where we work</h1>"
            '<div class="section__lead"><p>We are based in Goodwood and work within roughly 25 km of it. Below are the suburbs we write about in detail, because that is where most of our work is.</p></div>'
            f'<div class="grid grid--3" style="margin-top:28px">{AREA_ROWS}</div>')
    + section("<h2>Other areas we cover</h2>"
              "<p>These are inside our normal working radius, and we take jobs in them regularly. They do not have their own pages yet.</p>"
              "<p>" + ", ".join(OTHER_SUBURBS) + ".</p>"
              "<p>Stellenbosch and Somerset West we take on by arrangement when the job is large enough to justify the travel. If your suburb is not listed, call and ask. The answer is usually yes.</p>",
              alt=True)
    + cta(),
)

CUSTOM = {
    "about": ABOUT, "contact": CONTACT, "faq": FAQ, "thank-you": THANK_YOU,
    "privacy-policy": PRIVACY, "terms-conditions": TERMS, "disclaimer": DISCLAIMER,
    "accessibility": ACCESSIBILITY, "complaints-policy": COMPLAINTS,
    "referral-marketing-disclosure": REFERRAL,
    "services": SERVICES_INDEX, "service-areas": AREAS_INDEX,
}

for slug, html in CUSTOM.items():
    (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")

# drop the two pages we deliberately did not write
for dead in ("meet-the-team.html", "careers.html"):
    p = ROOT / dead
    if p.exists():
        p.unlink()

# ---------------------------------------------------------------- schema

BIZ = {
    "@type": "HomeAndConstructionBusiness",
    "@id": f"{SITE}/#business",
    "name": BUSINESS_NAME,
    "alternateName": "Plinth Renovations",
    "url": SITE,
    "telephone": PHONE,
    "image": f"{SITE}/og-cover.jpg",
    "description": "Renovations, waterproofing, damp repair, painting, kitchens, bathrooms and extensions across Cape Town.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "64 Oxford Street, Richmond Estate",
        "addressLocality": "Goodwood",
        "addressRegion": "Western Cape",
        "postalCode": "7460",
        "addressCountry": "ZA",
    },
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "07:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00"},
    ],
    "areaServed": [{"@type": "City", "name": "Cape Town"}] + [{"@type": "Place", "name": a} for a in AREA_NAMES],
    "knowsAbout": SERVICE_NAMES,
}


def crumbs(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             **({"item": f"{SITE}/{url}"} if url else {})}
            for i, (name, url) in enumerate(items)
        ],
    }


def schema_for(slug):
    graph = []
    if slug == "":
        graph.append({
            "@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE,
            "name": BUSINESS_NAME, "publisher": {"@id": f"{SITE}/#business"},
            "inLanguage": "en-ZA",
        })
        graph.append(BIZ)
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in content["home"]["faq"]
            ],
        })
        return {"@context": "https://schema.org", "@graph": graph}

    graph.append(BIZ)
    service = next((s for s in content["services"] if s["name"].lower().replace(" ", "-") == slug), None)
    area = next((a for a in content["areas"] if f"home-renovations-in-{a['name'].lower().replace(' ', '-')}" == slug), None)

    if service:
        graph.append({
            "@type": "Service",
            "@id": f"{SITE}/{slug}#service",
            "name": f"{service['name']} in Cape Town",
            "serviceType": service["name"],
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "City", "name": "Cape Town"}],
            "url": f"{SITE}/{slug}",
            "description": service["meta_description"],
        })
        graph.append(crumbs([("Home", ""), ("Services", "services"), (service["name"], slug)]))
    elif area:
        graph.append({
            "@type": "Service",
            "@id": f"{SITE}/{slug}#service",
            "name": f"Home renovations in {area['name']}",
            "serviceType": "Home renovations",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": {"@type": "Place", "name": area["name"]},
            "url": f"{SITE}/{slug}",
            "description": area["meta_description"],
        })
        graph.append(crumbs([("Home", ""), ("Service Areas", "service-areas"), (area["name"], slug)]))
    elif slug == "faq":
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ_ITEMS
            ],
        })
        graph.append(crumbs([("Home", ""), ("FAQ", slug)]))
    elif slug == "contact" or slug == "estimate":
        graph.append({"@type": "ContactPage", "@id": f"{SITE}/{slug}#page", "url": f"{SITE}/{slug}"})
        graph.append(crumbs([("Home", ""), ("Contact" if slug == "contact" else "Estimate", slug)]))
    elif slug in ("services", "service-areas"):
        graph.append({
            "@type": "CollectionPage", "@id": f"{SITE}/{slug}#page", "url": f"{SITE}/{slug}",
            "name": "Services" if slug == "services" else "Service areas",
        })
        graph.append(crumbs([("Home", ""), ("Services" if slug == "services" else "Service Areas", slug)]))
    else:
        graph.append({"@type": "WebPage", "@id": f"{SITE}/{slug}#page", "url": f"{SITE}/{slug}"})
        graph.append(crumbs([("Home", ""), (slug.replace("-", " ").title(), slug)]))
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- post-process

# written before the enrichment pass so it gets the same head treatment
not_found = page(
    "404",
    "Page Not Found | Plinth Renovations",
    "That page does not exist. Call 066 150 5770 or go back to the home page.",
    section("<h1>That page is not here</h1>"
            '<div class="section__lead"><p>The link may be old, or the page may have moved. The home page and the services list are the best places to restart.</p>'
            '<p><a class="btn" href="/">Home</a> <a class="btn btn--ghost" href="/services">Services</a></p></div>')
)
(ROOT / "404.html").write_text(not_found, encoding="utf-8")

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600'
    '&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
)

pages = sorted(ROOT.glob("*.html"))
urls = []
problems = []

# Each page gets a hero that matches what the page is about, and an alt that
# describes the actual photo instead of repeating the primary service.
HERO_MAP = {
    "waterproofing": "img-5.jpg",       # exterior wall and window detail
    "damp-proofing": "img-6.jpg",       # room with walls opened up
    "painting": "img-3.jpg",            # finished painted corridor
    "kitchen-renovations": "img-1.jpg", # finished kitchen
    "bathroom-renovations": "img-2.jpg",# finished bathroom
    "home-renovations": "img-4.jpg",    # covered outdoor room
    "plastering": "img-7.jpg",          # fresh plaster and new downlight
    "home-extensions": "img-4.jpg",     # covered outdoor room
    "service-areas": "img-3.jpg",
    "about": "img-8.jpg",
    "contact": "img-8.jpg",
}

for p in pages:
    slug = "" if p.stem == "index" else p.stem
    html = p.read_text(encoding="utf-8")

    # language for a South African audience
    html = html.replace('<html lang="en">', '<html lang="en-ZA">')

    # inline handler out of the markup so script-src can stay strict
    html = html.replace(
        '<button class="nav__toggle" aria-label="Menu" '
        "onclick=\"document.getElementById('navlinks').classList.toggle('open')\">&#9776;</button>",
        '<button class="nav__toggle" id="navToggle" aria-label="Menu" '
        'aria-controls="navlinks" aria-expanded="false">&#9776;</button>',
    )

    # real title/description/canonical for pages the builder only stubbed
    html = html.replace("Content coming soon.", "")

    if slug == "404":
        html = html.replace('<meta name="robots" content="all">',
                            '<meta name="robots" content="noindex, follow">')

    # the engine writes "Plinth Renovations Is Proud to Serve Cape Town"
    html = html.replace(" Is Proud to Serve ", " works across ")

    # page-specific hero, described by what the page is actually about
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    hero_alt = re.sub(r"<[^>]+>", "", h1m.group(1)).strip() if h1m else "Plinth Renovations"
    hero_file = HERO_MAP.get(slug, "hero.jpg")
    html = re.sub(r'<img src="assets/images/hero\.jpg" alt="[^"]*">',
                  f'<img src="assets/images/{hero_file}" alt="{hero_alt}">',
                  html, count=1)

    # social + icons + fonts, inserted before </head>
    canonical = f"{SITE}/{slug}" if slug else f"{SITE}/"
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = desc.group(1) if desc else ""
    head_bits = (
        FONTS
        + f'<link rel="icon" type="image/png" href="{SITE}/assets/images/favicon.png">'
        + '<meta property="og:site_name" content="Plinth Renovations">'
        + '<meta property="og:type" content="website">'
        + f'<meta property="og:title" content="{title}">'
        + f'<meta property="og:description" content="{desc}">'
        + f'<meta property="og:url" content="{canonical}">'
        + f'<meta property="og:image" content="{SITE}/og-cover.jpg">'
        + '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        + '<meta property="og:locale" content="en_ZA">'
        + '<meta name="twitter:card" content="summary_large_image">'
        + f'<meta name="twitter:title" content="{title}">'
        + f'<meta name="twitter:description" content="{desc}">'
        + f'<meta name="twitter:image" content="{SITE}/og-cover.jpg">'
        + '<script type="application/ld+json">'
        + json.dumps(schema_for(slug), ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    html = html.replace("</head>", head_bits + "</head>", 1)

    # cache-bust the stylesheet so a stale edge copy cannot lie to us
    html = html.replace('href="assets/style.css"', f'href="assets/style.css?v={BUILD_TS}"')
    html = html.replace('src="assets/main.js"', f'src="assets/main.js?v={BUILD_TS}"')

    # clean URLs
    html = re.sub(r'href="index\.html"', 'href="/"', html)
    html = re.sub(r'href="([a-z0-9-]+)\.html"', r'href="/\1"', html)

    # inline handler is gone, so keep script-src strict
    if "onclick=" in html:
        problems.append(f"{p.name}: inline onclick still present")

    html = html.replace("\u2014", " - ").replace("\u2013", "-")
    p.write_text(html, encoding="utf-8")
    urls.append((slug or "", title, desc))

# ---------------------------------------------------------------- nav js

NAV_JS = """
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navlinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && window.innerWidth <= 900) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
});
"""
(ROOT / "assets" / "main.js").write_text(NAV_JS.lstrip(), encoding="utf-8")

# header logo sizing (the builder has no img rule for it)
css_path = ROOT / "assets" / "style.css"
css = css_path.read_text(encoding="utf-8")
css += """
/* Plinth: header logo is a square gold-on-ink lockup */
.nav__logo img { height: 54px; width: auto; border-radius: 6px; display: block; }
.nav__logo { display: flex; align-items: center; gap: 12px; }
@media (max-width: 600px) { .nav__logo img { height: 42px; } }

/* Plinth: brand presence in the text lockup */
.nav__logo strong { font-family: var(--font-head); font-size: 1.18rem; letter-spacing: .01em; color: var(--brand); }

/* Plinth: stacked calls to action match on a phone */
@media (max-width: 600px) {
  .hero__cta { flex-direction: column; align-items: stretch; }
  .hero__cta .btn { text-align: center; }
  .hero { min-height: 0; }
  .hero__inner { padding: 64px 20px 56px; }
}
"""
css_path.write_text(css, encoding="utf-8")

# ---------------------------------------------------------------- sitemap, robots, headers

order = [("", 1.0), ("services", 0.9), ("service-areas", 0.8), ("estimate", 0.8),
         ("about", 0.7), ("contact", 0.7), ("faq", 0.7)]
for s in content["services"]:
    order.append((s["name"].lower().replace(" ", "-"), 0.9))
for a in content["areas"]:
    order.append((f"home-renovations-in-{a['name'].lower().replace(' ', '-')}", 0.7))
for extra in ("thank-you", "privacy-policy", "terms-conditions", "disclaimer",
              "accessibility", "complaints-policy", "referral-marketing-disclosure"):
    order.append((extra, 0.3))

seen, entries = set(), []
for slug, prio in order:
    if slug in seen:
        continue
    seen.add(slug)
    entries.append(
        f"  <url><loc>{SITE}/{slug}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'weekly' if slug == '' else 'monthly'}</changefreq>"
        f"<priority>{prio:.1f}</priority></url>"
    )

(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(entries) + "\n</urlset>\n",
    encoding="utf-8",
)

(ROOT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
)

(ROOT / "_headers").write_text(
    "/*\n"
    "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'\n"
    "  X-Frame-Options: DENY\n"
    "  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
    "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
    "\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n",
    encoding="utf-8",
)

(ROOT / "_redirects").write_text(
    "/meet-the-team /about 301\n/careers /about 301\n", encoding="utf-8"
)

print("pages finished:", len(pages) + 1)  # + 404
print("urls in sitemap:", len(seen))
for slug, title, _ in urls:
    print(f"  /{slug:<42} {title[:60]}")
if problems:
    print("\nPROBLEMS:")
    for x in problems:
        print(" -", x)
