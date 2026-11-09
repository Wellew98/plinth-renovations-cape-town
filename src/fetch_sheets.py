import time, shutil, os
from pathlib import Path
import neo

DL = Path(os.path.expanduser("~/Downloads"))
OUT = Path("../research/course")
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}"
ITEMS = [
    ("info-architecture", "1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "131667601"),
    ("keywords", "1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "1346315491"),
    ("site-layout", "1RPVEC8g6MM0qywUAd7ddzjR_nCmeDeEhhy3j14VuZlw", "472410651"),
    ("competitors", "1DkLXktqCtERznNwbOCKg3naEdayKJjQZhxtm5akHlPQ", "1886959757"),
    ("site-audit", "1H79LFAPx1HtPMlarCMGaWi3hE-SFsxvx00CTcluQNuw", "0"),
    ("directories", "19lgFNZvZFOmMFFBA-kv71BwF2DDV-6gUIjocAfiDWjI", "0"),
]

def newest(since):
    files = [f for f in DL.glob("*") if f.is_file() and f.stat().st_mtime >= since]
    return max(files, key=lambda f: f.stat().st_mtime) if files else None

neo.init()
for name, sid, gid in ITEMS:
    t0 = time.time()
    neo.call("navigate", {"page": 9, "url": BASE.format(sid, gid)})
    hit = None
    for _ in range(30):
        time.sleep(1)
        hit = newest(t0 - 2)
        if hit:
            break
    if not hit:
        print(f"{name}: nothing downloaded")
        continue
    dest = OUT / f"sheet-{name}.csv"
    shutil.copyfile(hit, dest)
    print(f"{name}: {hit.name} -> {dest.name} ({dest.stat().st_size} B)")
