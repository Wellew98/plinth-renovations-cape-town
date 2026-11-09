import json, time, re, sys
from pathlib import Path
import neo

OUT = Path("../research/course")
OUT.mkdir(parents=True, exist_ok=True)

DOC = "https://docs.google.com/document/d/{}/mobilebasic"
CSV = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}"

ITEMS = [
    ("01-your-notes", DOC.format("1x0hMWqmegmqsgOwVpgB8e_KyHBRLp-VcncsyVm_jzJI")),
    ("02-bofu-landing-page-template", DOC.format("1A1AQFy8cEkaFbLzigKQskDDM3q-fhTGlTjXlPn7dysg")),
    ("03-sheet-information-architecture", CSV.format("1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "131667601")),
    ("04-sheet-keywords", CSV.format("1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "1346315491")),
    ("05-sheet-site-layout", CSV.format("1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "472410651")),
    ("06-sheet-competitors", CSV.format("1DkLXktqCtERznNwbOCKg3naEdayKJjQZhxtm5akHlPQ", "1886959757")),
    ("07-sheet-site-audit", CSV.format("1H79LFAPx1HtPMlarCMGaWi3hE-SFsxvx00CTcluQNuw", "0")),
    ("08-sheet-directories", CSV.format("19lgFNZvZFOmMFFBA-kv71BwF2DDV-6gUIjocAfiDWjI", "0")),
]

def text_of(res):
    try:
        return "\n".join(p.get("text", "") for p in res["result"]["content"] if p.get("type") == "text")
    except Exception:
        return json.dumps(res)[:400]

neo.init()
for name, url in ITEMS:
    try:
        neo.call("navigate", {"page": 9, "url": url})
        time.sleep(3.5)
        txt = text_of(neo.call("read", {"page": 9, "format": "text"}))
        txt = re.sub(r"\[UNTRUSTED_PAGE_CONTENT[^\]]*\]", "", txt).strip()
        (OUT / f"{name}.txt").write_text(txt, encoding="utf-8")
        print(f"{name}: {len(txt)} chars")
    except Exception as e:
        print(f"{name}: FAILED {e}")
