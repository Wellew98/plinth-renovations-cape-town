"""DataForSEO helper: balance readout and one batched search-volume pull."""
import base64, json, sys, urllib.request
from pathlib import Path

CRED = Path(r"C:/Users/DELL/.secrets/dfs-plinth.txt")


def _token() -> str:
    txt = CRED.read_text(encoding="utf-8").strip()
    if txt.count(":") == 1:
        import base64 as _b
        return _b.b64encode(txt.encode()).decode()
    return txt


def auth():
    return {"Authorization": f"Basic {_token()}", "Content-Type": "application/json"}


def call(path, payload=None):
    url = "https://api.dataforseo.com/v3" + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=auth(), method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "balance"
    if cmd == "balance":
        d = call("/appendix/user_data")
        print(json.dumps(d.get("tasks", [{}])[0].get("result", [{}])[0], indent=1)[:600])
    elif cmd == "volume":
        kws = [l.strip() for l in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if l.strip()]
        print("keywords:", len(kws))
        payload = [{"keywords": kws, "location_code": 2710, "language_code": "en", "search_partners": False}]
        d = call("/keywords_data/google_ads/search_volume/live", payload)
        t = d["tasks"][0]
        print("status:", t.get("status_code"), t.get("status_message"), "cost:", t.get("cost"))
        res = t.get("result") or []
        out = Path(sys.argv[3] if len(sys.argv) > 3 else "../research/volumes-pull.json")
        out.write_text(json.dumps(d, indent=1), encoding="utf-8")
        print("rows:", len(res), "->", out)
