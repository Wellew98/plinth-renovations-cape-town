import json, sys
from pathlib import Path
import dfs

seeds_file, out_file = sys.argv[1], sys.argv[2]
SEEDS = [l.strip() for l in Path(seeds_file).read_text(encoding="utf-8").splitlines() if l.strip()]
payload = [{
    "keywords": SEEDS[:200], "location_code": 2710, "language_code": "en",
    "include_adult_keywords": False, "limit": 1000,
}]
d = dfs.call("/keywords_data/google_ads/keywords_for_keywords/live", payload)
t = d["tasks"][0]
res = t.get("result") or []
print("seeds:", len(SEEDS), "status:", t.get("status_code"), "cost:", t.get("cost"), "ideas:", len(res))
Path(out_file).write_text(json.dumps(d), encoding="utf-8")
