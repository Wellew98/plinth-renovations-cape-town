#!/usr/bin/env python3
"""Compact Keywords gate for site-output.

Reads src/seo-layout.json (the authoritative sheet) and the rendered HTML, then
fails on every rule the course states. Run it before a deploy; exit 1 means do not
ship.

  python src/seo_check.py
"""
import json
import re
import sys
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site-output"
LAYOUT = Path(__file__).resolve().parent / "seo-layout.json"

WORD_MIN, WORD_MAX = 400, 500
TITLE_MAX, META_MAX = 60, 155
DEPTH_MAX = 2


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = ""
        self.h1s, self.h2s = [], []
        self.imgs, self.links = [], []
        self._in = None
        self._buf = []
        self.main_parts = []
        self._main = 0
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self._main += 1
        elif tag in ("script", "style", "noscript"):
            self._skip += 1
        elif tag == "img" and a.get("src"):
            self.imgs.append(a["src"])
        elif tag == "a" and a.get("href", "").startswith("/"):
            self.links.append(a["href"].split("#")[0].split("?")[0])
        elif tag in ("title", "h1", "h2"):
            self._in = tag
            self._buf = []
        elif tag == "meta" and a.get("name") == "description":
            self.meta = (a.get("content") or "").strip()

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1
        elif tag == "main" and self._main:
            self._main -= 1
        if tag == self._in:
            text = " ".join("".join(self._buf).split())
            if tag == "title":
                self.title = text
            elif tag == "h1":
                self.h1s.append(text)
            elif tag == "h2":
                self.h2s.append(text)
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)
        if self._main and not self._skip:
            self.main_parts.append(data)

    @property
    def main_text(self):
        return " ".join(" ".join(self.main_parts).split())


def words(text):
    return [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'&-]*", text)]


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p


def out_path(url):
    return OUT / ("index.html" if url == "/" else f"{url.strip('/')}.html")


def main():
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    pages = layout["pages"]
    fails = defaultdict(list)
    parsed = {}
    fallback_titles = defaultdict(list)
    fallback_metas = defaultdict(list)
    fallback_h1 = defaultdict(list)
    image_use = defaultdict(list)

    for spec in pages:
        url, kw = spec["url"], (spec.get("keyword") or "").lower()
        path = out_path(url)
        if not path.exists():
            fails["missing page"].append(f"{url} not built (expected {path.name})")
            continue
        p = parse(path)
        parsed[url] = p
        text = p.main_text
        wc = len(words(text))
        slug = url.strip("/")

        if len(p.title) > TITLE_MAX:
            fails["title length"].append(f"{url}: {len(p.title)} chars")
        if not p.title:
            fails["title length"].append(f"{url}: no title")
        if len(p.meta) > META_MAX:
            fails["meta length"].append(f"{url}: {len(p.meta)} chars")
        if not p.meta:
            fails["meta length"].append(f"{url}: no meta description")
        if len(p.h1s) != 1:
            fails["h1 count"].append(f"{url}: {len(p.h1s)} h1 elements")

        if kw:
            if kw not in p.title.lower():
                fails["keyword in title"].append(f"{url}: '{kw}' not in title")
            if slug and kw.replace(" ", "-") not in slug:
                fails["keyword in slug"].append(f"{url}: slug '{slug}' != '{kw.replace(' ', '-')}'")
            if p.h1s and kw not in p.h1s[0].lower():
                fails["keyword in h1"].append(f"{url}: h1 '{p.h1s[0]}'")
            first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0].lower()
            if kw not in first:
                fails["keyword in first sentence"].append(f"{url}: opens '{first[:70]}'")
            if not any(kw in h.lower() for h in p.h2s):
                fails["keyword in an h2"].append(f"{url}: h2s carry no variant")
            if spec.get("compact") and not (WORD_MIN <= wc <= WORD_MAX):
                fails["word count"].append(f"{url}: {wc} words")
        elif spec.get("compact"):
            fails["word count"].append(f"{url}: compact page with no keyword")

        fallback_titles[p.title].append(url)
        fallback_metas[p.meta].append(url)
        fallback_h1[tuple(p.h1s)].append(url)
        if spec.get("compact") and spec.get("image"):
            image_use[spec["image"]].append(url)

    for what, bucket in (("duplicate title", fallback_titles), ("duplicate meta", fallback_metas), ("duplicate h1", fallback_h1)):
        for value, urls in bucket.items():
            if len(urls) > 1:
                fails[what].append(f"{', '.join(urls)} share '{str(value)[:60]}'")

    image_exempt = layout.get("_image_exempt") or {}
    for src, urls in image_use.items():
        if len(set(urls)) > 1 and src not in image_exempt:
            fails["image reused across pages"].append(f"{src} on {', '.join(sorted(set(urls)))}")

    # crawl depth from home, using rendered links only
    def norm(href):
        h = href.strip("/")
        if h.endswith(".html"):
            h = h[:-5]
        if h in ("", "index"):
            return "/"
        return "/" + h

    graph = {u: {norm(l) for l in p.links} for u, p in parsed.items()}
    depth = {"/": 0}
    q = deque(["/"])
    while q:
        cur = q.popleft()
        for nxt in graph.get(cur, ()):
            if nxt in graph and nxt not in depth:
                depth[nxt] = depth[cur] + 1
                q.append(nxt)

    inbound = defaultdict(int)
    for src, outs in graph.items():
        for dst in outs:
            if dst in graph and dst != src:
                inbound[dst] += 1

    for url in parsed:
        if url not in depth:
            fails["unreachable"].append(f"{url}: no path from home")
        elif depth[url] > DEPTH_MAX:
            fails["crawl depth"].append(f"{url}: depth {depth[url]}")
        if inbound.get(url, 0) == 0 and url != "/":
            fails["orphan"].append(f"{url}: zero inlinks")

    expected = {spec["url"] for spec in pages}
    exempt_urls = set(layout.get("_exempt") or [])
    built = {"/" if f.name == "index.html" else "/" + f.stem for f in OUT.glob("*.html")}
    for extra in sorted(built - expected - exempt_urls):
        fails["stray page"].append(f"{extra}: built but not in the layout sheet")

    total = sum(len(v) for v in fails.values())
    print(f"seo_check: {len(parsed)}/{len(pages)} pages found, {total} problems\n")
    for kind in sorted(fails, key=lambda k: -len(fails[k])):
        print(f"[{kind}] {len(fails[kind])}")
        for line in fails[kind][:12]:
            print(f"    {line}")
        if len(fails[kind]) > 12:
            print(f"    ... {len(fails[kind]) - 12} more")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
