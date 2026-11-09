"""One DataForSEO keyword-ideas request: seeds in, related keywords with volume out."""
import json, sys
from pathlib import Path
import dfs

SEEDS = [
    "waterproofing cape town", "damp proofing cape town", "roof waterproofing cape town",
    "kitchen renovations cape town", "bathroom renovations cape town",
    "painting contractors cape town", "home renovations cape town",
    "home extensions cape town", "plastering cape town", "tiling cape town",
]
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
out = Path("../research/ideas-raw.json")
payload = [{
    "keywords": SEEDS,
    "location_code": 2710,
    "language_code": "en",
    "include_adult_keywords": False,
    "limit": LIMIT,
}]
d = dfs.call("/keywords_data/google_ads/keywords_for_keywords/live", payload)
t = d["tasks"][0]
print("status:", t.get("status_code"), t.get("status_message"), "cost:", t.get("cost"))
res = t.get("result") or []
print("ideas:", len(res))
out.write_text(json.dumps(d), encoding="utf-8")
print("saved", out, out.stat().st_size, "bytes")
