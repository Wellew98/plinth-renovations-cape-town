"""The photography set, named for search and described accurately.

Every file here is a real Plinth job. The names carry the service and the city,
which is what a Cape Town search actually looks like; the alts and captions say
what is visible in the frame, including the work-in-progress shots, because a
young company showing its stages is more credible than a wall of finished rooms.
"""

HERO = {
    "src": "IMG-20260903-WA0034.jpg",
    "file": "renovated-home-exterior-cape-town.jpg",
    "alt": "Renovated Cape Town home exterior with new paving, planting and a covered entrance",
    "caption": "Finished exterior, paving and entrance",
}

PHOTOS = [
    {
        "src": "IMG-20260903-WA0033.jpg",
        "file": "kitchen-renovation-cape-town.jpg",
        "alt": "Finished kitchen renovation with a stone island, timber cabinetry and pendant lights",
        "caption": "Kitchen: stone island, timber joinery",
        "service": "kitchen-renovations",
    },
    {
        "src": "svc-bathroom.jpg",
        "file": "bathroom-renovation-cape-town.jpg",
        "alt": "Completed bathroom renovation with a walk-in shower, floating vanity and full-height tiling",
        "caption": "Bathroom: walk-in shower, floating vanity",
        "service": "bathroom-renovations",
    },
    {
        "src": "IMG-20260903-WA0028.jpg",
        "file": "glass-roof-patio-extension-cape-town.jpg",
        "alt": "Timber frame and glass roof extension over a patio, under construction",
        "caption": "Glass roof patio extension, frame going up",
        "service": "home-extensions",
    },
    {
        "src": "IMG-20260902-WA0018.jpg",
        "file": "interior-renovation-in-progress-cape-town.jpg",
        "alt": "Interior renovation in progress with new ceilings, cove lighting and dust sheeting",
        "caption": "Interior fit-out: new ceilings and cove lighting",
        "service": "home-renovations",
    },
    {
        "src": "IMG-20260902-WA0022.jpg",
        "file": "plasterboard-bulkhead-ceiling-cape-town.jpg",
        "alt": "New plasterboard bulkhead meeting an existing wall, taped and ready for skimming",
        "caption": "Bulkhead formed and taped for skim",
        "service": "plastering",
    },
    {
        "src": "IMG-20260902-WA0015.jpg",
        "file": "curved-ceiling-plaster-detail-cape-town.jpg",
        "alt": "Curved plaster ceiling detail marked out in a passage before skimming",
        "caption": "Curved ceiling detail, set out before skim",
        "service": "plastering",
    },
    {
        "src": "IMG-20260902-WA0013.jpg",
        "file": "renovation-strip-out-cape-town.jpg",
        "alt": "Room stripped back to its ceiling and walls before renovation work begins",
        "caption": "Stripped back before the new work",
        "service": "painting",
    },
    {
        "src": "IMG-20260902-WA0005.jpg",
        "file": "home-extension-under-construction-cape-town.jpg",
        "alt": "Double-storey home extension under construction with new slab and openings formed",
        "caption": "Extension shell, slab and openings",
        "service": "home-extensions",
    },
]


def by_file(name):
    if HERO["file"] == name:
        return HERO
    for p in PHOTOS:
        if p["file"] == name:
            return p
    raise KeyError(name)
