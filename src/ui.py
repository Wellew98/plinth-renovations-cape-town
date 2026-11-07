"""Components in the original Plinth design vocabulary.

Every function here emits the same markup the live plinthrenovations.co.za
pages use, so the site runs on that stylesheet and script unchanged.
"""

from html import escape

import photos

BUSINESS = "Plinth Renovations and Construction"
PHONE = "066 150 5770"
TEL = "+27661505770"
STREET = "64 Oxford Street, Richmond Estate"
CITY = "Goodwood, Cape Town, 7460"
HOURS_TOP = "Mon to Fri 7AM to 6PM | Sat 8AM to 2PM"
DOMAIN = "https://plinthrenovations.co.za"

# stroke icons, 24x24, matching the weight used in the original cards
ICONS = {
    "water": '<path d="M12 3s6 6.4 6 10a6 6 0 0 1-12 0c0-3.6 6-10 6-10Z"/><path d="M9.5 14a2.5 2.5 0 0 0 2.5 2.5"/>',
    "paint": '<path d="M4 5h11a3 3 0 0 1 3 3v2H7a3 3 0 0 1-3-3V5Z"/><path d="M18 8h1a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-6"/><path d="M12 14v3a2 2 0 0 0 2 2h.5"/><rect x="10" y="19" width="4" height="2.5" rx="1"/>',
    "kitchen": '<path d="M4 4h16v16H4z"/><path d="M4 10h16"/><path d="M8 7h2M14 13h2"/>',
    "bath": '<path d="M4 12h16v2a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-2Z"/><path d="M6 12V6a2 2 0 0 1 4 0"/><path d="M8 19l-1 2M16 19l1 2"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
    "damp": '<path d="M5 5h14v14H5z"/><path d="M8 16c1.5-2 2.5-2 4 0s2.5 2 4 0"/><path d="M8 9h8"/>',
    "plaster": '<path d="M4 20 14 10"/><path d="M12 4h8v8l-6 6H6v-8l6-6Z"/>',
    "extend": '<path d="M3 20V9l9-5 9 5v11"/><path d="M9 20v-6h6v6"/><path d="M16 8h4v4"/>',
}

NAV = [
    ("/", "Home"),
    ("/services", "Services"),
    ("/our-work", "Our Work"),
    ("/service-areas", "Areas"),
    ("/about", "About"),
    ("/faq", "FAQ"),
    ("/contact", "Contact"),
]


def topbar():
    return (
        '<div class="topbar"><div class="wrap">'
        f'<div><a href="tel:{TEL}">{PHONE}</a> &nbsp;·&nbsp; {HOURS_TOP}</div>'
        '<div class="badge">&#10003; Serving Cape Town, Free written estimates</div>'
        "</div></div>"
    )


def header(active=""):
    parts = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    links = "".join(parts)
    return (
        '<header class="site-header"><div class="wrap">'
        '<a class="brand" href="/">'
        '<img src="logo.jpg" alt="Plinth Renovations and Construction logo">'
        '<span class="lockup"><strong>PLINTH <span>RENOVATIONS</span></strong>'
        '<span class="sub">Construction &middot; Cape Town</span>'
        '<span class="rule"></span>'
        '<span class="tag">Built on vision &middot; Crafted with precision</span></span></a>'
        '<button class="mobile-toggle" aria-label="Menu">&#9776;</button>'
        '<div class="head-right"><nav class="main">' + links + "</nav>"
        '<a class="header-cta" href="/estimate">Get an Estimate</a>'
        "</div></div></header>"
    )


def hero(kicker, h1, lead, trust, actions, video=None, poster=None):
    poster = poster or "images/" + photos.HERO["file"]
    media = ""
    if video:
        media = (
            f'<video class="hero-bg" autoplay muted loop playsinline preload="metadata"'
            f' poster="{poster}"><source src="{video}" type="video/mp4"></video>'
        )
    else:
        media = f'<img class="hero-bg" src="{poster}" alt="">'
    pills = "".join(f"<span>{escape(t)}</span>" for t in trust)
    return (
        f'<section class="hero">{media}<div class="wrap">'
        f'<div class="kicker reveal">{escape(kicker)}</div>'
        f'<h1 class="reveal">{escape(h1)}</h1>'
        f'<p class="lead reveal">{escape(lead)}</p>'
        f'<div class="trust reveal">{pills}</div>'
        f'<div class="hero-actions reveal">{actions}</div>'
        "</div></section>"
    )


def page_hero(crumb, h1, lead="", kicker=""):
    kick = f'<div class="eyebrow">{escape(kicker)}</div>' if kicker else ""
    lead_html = f"<p>{escape(lead)}</p>" if lead else ""
    return (
        f'<section class="page-hero"><div class="wrap">'
        f'<div class="crumb"><a href="/" style="color:#c9a86a">Home</a> &rsaquo; {escape(crumb)}</div>'
        f"{kick}<h1>{escape(h1)}</h1>{lead_html}</div></section>"
    )


def gallery(items, eager=0, layout=None):
    """The original .gallery-grid: rounded figures, hover zoom, pill caption."""
    figs = []
    for i, p in enumerate(items):
        load = "eager" if i < eager else "lazy"
        figs.append(
            f'<figure><img src="images/{p["file"]}" alt="{escape(p["alt"])}" '
            f'loading="{load}" decoding="async">'
            f'<figcaption>{escape(p["caption"])}</figcaption></figure>'
        )
    cls = "gallery-grid" + (f" {layout}" if layout else "")
    out = f'<div class="{cls}">' + "".join(figs) + "</div>"

    credits = [p for p in items if p.get("credit")]
    if credits:
        lines = []
        for p in credits:
            lic = p.get("licence", "")
            lic_url = p.get("licence_url", "")
            lic_html = f' <a href="{lic_url}" rel="noopener nofollow">{lic}</a>' if lic_url else (" " + lic if lic else "")
            lines.append(f'{p["credit"]}{lic_html}')
        out += '<p class="img-credit">' + "<br>".join(lines) + "</p>"
    return out


def section(inner, cls="", style=""):
    style_attr = f' style="{style}"' if style else ""
    return f'<section class="section {cls}"{style_attr}><div class="wrap">{inner}</div></section>'


def head(n, label, h2, sub="", left=False):
    cls = "section-head left reveal" if left else "section-head reveal"
    sub_html = f'<p class="sub">{escape(sub)}</p>' if sub else ""
    return (
        f'<div class="{cls}">'
        f'<div class="eyebrow"><span class="n">{n}</span><span class="t">{escape(label)}</span></div>'
        f"<h2>{escape(h2)}</h2>{sub_html}</div>"
    )


def card(tag, title, text, href, link_label="Learn more", icon="home", n=""):
    svg = ""
    if icon:
        svg = (
            '<div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            + ICONS.get(icon, ICONS["home"])
            + "</svg></div>"
        )
    tag_html = f'<div class="tag">{escape(tag)}</div>' if tag else ""
    return (
        f'<div class="card reveal">{svg}{tag_html}<h3>{escape(title)}</h3>'
        f"<p>{escape(text)}</p>"
        f'<a class="more" href="{href}">{link_label} &rarr;</a></div>'
    )


def grid(items, cls="grid9"):
    return f'<div class="{cls}">' + "".join(items) + "</div>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def checklist(title, items, cta_href="/estimate", cta_label="Request Free Estimate &rarr;"):
    rows = "".join(f"<li>{escape(i)}</li>" for i in items)
    return (
        f'<div class="checklist reveal"><h3>{escape(title)}</h3><ul>{rows}</ul>'
        f'<p style="margin-top:20px"><a class="btn btn-gold" href="{cta_href}" '
        f'style="width:100%;text-align:center">{cta_label}</a></p></div>'
    )


def steps(items):
    rows = "".join(
        f'<div class="step reveal"><b class="num">{i}</b><h3>{escape(t)}</h3><p>{escape(d)}</p></div>'
        for i, (t, d) in enumerate(items, 1)
    )
    return f'<div class="steps">{rows}</div>'


def faq(items, open_first=True):
    rows = []
    for i, (q, a) in enumerate(items):
        opened = " open" if (open_first and i == 0) else ""
        rows.append(
            f'<details class="faq-item"{opened}><summary>{escape(q)} '
            f'<span class="plus">+</span></summary><div class="a"><p>{escape(a)}</p></div></details>'
        )
    return '<div class="faq">' + "".join(rows) + "</div>"


def cta_band(title, sub):
    return (
        '<div class="cta-band reveal"><div>'
        f"<h2>{escape(title)}</h2><p>{escape(sub)}</p></div>"
        '<div><a class="btn btn-gold" href="/estimate">Request Free Estimate &rarr;</a> &nbsp; '
        f'<a class="btn btn-ghost" href="tel:{TEL}">{PHONE}</a></div></div>'
    )


def footer():
    services = [
        ("/waterproofing", "Waterproofing"),
        ("/damp-proofing", "Damp Proofing"),
        ("/painting", "Painting"),
        ("/kitchen-renovations", "Kitchen Renovations"),
        ("/bathroom-renovations", "Bathroom Renovations"),
        ("/home-renovations", "Home Renovations"),
        ("/plastering", "Plastering"),
        ("/home-extensions", "Home Extensions"),
    ]
    areas = [
        ("/home-renovations-in-durbanville", "Durbanville"),
        ("/home-renovations-in-bellville", "Bellville"),
        ("/home-renovations-in-parow", "Parow"),
        ("/home-renovations-in-table-view", "Table View"),
        ("/home-renovations-in-brackenfell", "Brackenfell"),
        ("/home-renovations-in-southern-suburbs", "Southern Suburbs"),
    ]
    resources = [
        ("/service-areas", "Service Areas"),
        ("/faq", "FAQ"),
        ("/estimate", "Free Estimate"),
        ("/about", "About"),
        ("/contact", "Contact"),
    ]

    def col(title, items):
        rows = "<br>".join(f'<a href="{h}">{escape(l)}</a>' for h, l in items)
        return f"<div><h4>{title}</h4><p>{rows}</p></div>"

    return (
        "<footer><div class=\"wrap\"><div class=\"foot-grid\">"
        "<div><p><strong style=\"color:#fff\">Plinth Renovations and Construction</strong><br>"
        "Built on vision, crafted with precision.<br>"
        f"{STREET},<br>{CITY}</p>"
        f'<p><a href="tel:{TEL}">{PHONE}</a><br>'
        '<a href="https://web.facebook.com/people/Plinth-Renovations-Construction/61594305267891/" '
        'target="_blank" rel="noopener">Facebook</a></p></div>'
        + col("Services", services)
        + col("Service Areas", areas)
        + col("Resources", resources)
        + "</div>"
        '<div class="foot-bottom"><span>&copy; <span id="yr"></span> '
        "Plinth Renovations and Construction &middot; Cape Town</span>"
        '<span><a href="/privacy">Privacy Policy</a> &middot; <a href="/terms">Terms</a></span>'
        "</div></div></footer>"
    )


def floaters():
    return (
        f'<a class="sticky-call" href="tel:{TEL}" aria-label="Call Plinth on {PHONE}">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" width="22" height="22">'
        '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
        "</svg></a>"
        '<button class="to-top" aria-label="Back to top">&uarr;</button>'
    )
