"""Harvest Google Autocomplete (free, no key) to build the compact keyword candidate set."""
import json, time, urllib.parse, urllib.request
from pathlib import Path

SERVICES = [
    "waterproofing", "roof waterproofing", "damp proofing", "damp proofing walls",
    "painting contractors", "house painting", "plastering", "kitchen renovations",
    "bathroom renovations", "home renovations", "home extensions", "building contractor",
    "tiling", "ceiling repairs", "boundary wall", "paving", "renovations",
]
AREAS = [
    "cape town", "goodwood", "parow", "bellville", "durbanville", "brackenfell",
    "kuils river", "milnerton", "table view", "montague gardens", "century city",
    "edgemead", "bothasig", "plattekloof", "vasco", "richmond estate", "kraaifontein",
    "somerset west", "strand", "stellenbosch", "observatory", "woodstock", "sea point",
    "claremont", "rondebosch", "muizenberg", "southern suburbs", "northern suburbs",
]
MODS = ["", " near me", " cost", " price", " company", " contractors", " specialists", " services"]

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"}


def suggest(q):
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "firefox", "hl": "en", "gl": "za", "q": q})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
        return [s.lower().strip() for s in data[1]]
    except Exception as e:
        return []


def main():
    found = {}
    seeds = []
    for s in SERVICES:
        for a in AREAS:
            for m in MODS:
                seed = f"{s} {a}{m}".strip()
                if len(seed) < 55:
                    seeds.append(seed)
    print("seeds:", len(seeds))
    for i, seed in enumerate(seeds):
        for sug in suggest(seed):
            if sug not in found:
                found[sug] = seed
        if i % 40 == 0:
            print(f"  {i}/{len(seeds)} unique so far {len(found)}", flush=True)
        time.sleep(0.15)
    out = Path("../research/suggest-candidates.json")
    out.write_text(json.dumps(found, indent=1, ensure_ascii=False), encoding="utf-8")
    Path("../research/suggest-candidates.txt").write_text("\n".join(sorted(found)), encoding="utf-8")
    print("unique suggestions:", len(found), "->", out)


if __name__ == "__main__":
    main()
