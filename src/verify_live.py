import re, subprocess, sys

BASE = "https://plinthrenovations.co.za"
UA = ["-A", "Mozilla/5.0"]

def code(path, head=False):
    args = ["curl", "-s", "-o", os_devnull(), "-w", "%{http_code}"] + UA
    if head:
        args.append("-I")
    return subprocess.run(args + [BASE + path], capture_output=True, text=True).stdout.strip()

def os_devnull():
    return "NUL" if sys.platform.startswith("win") else "/dev/null"

def location(path):
    out = subprocess.run(["curl", "-s", "-I"] + UA + [BASE + path], capture_output=True, text=True).stdout
    m = re.search(r"(?im)^location:\s*(\S+)", out)
    return m.group(1) if m else "-"

print("== redirects the user asked about ==")
for p in ("/kitchen-renovations", "/bathroom-renovations"):
    print(f"{p:24s} {code(p)} -> {location(p)}")

sm = subprocess.run(["curl", "-s"] + UA + [BASE + "/sitemap.xml"], capture_output=True, text=True).stdout
urls = re.findall(r"<loc>(.*?)</loc>", sm)
bad = []
for u in urls:
    path = u.replace(BASE, "") or "/"
    c = code(path)
    if c != "200":
        bad.append((u, c))
print(f"\nsitemap {len(urls)} urls, non-200: {bad if bad else 'none'}")
