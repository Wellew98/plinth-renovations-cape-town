import re, subprocess

BASE = "https://plinthrenovations.co.za"
UA = ["-A", "Mozilla/5.0"]

def get(path):
    r = subprocess.run(["curl", "-s", "-w", "\n%{http_code}"] + UA + [BASE + path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    body, _, code = r.stdout.rpartition("\n")
    return code, body

code, html = get("/painters-cape-town")
print("page", code, "| illustrative credit:", "Illustrative photograph" in html)
imgs = re.findall(r'src="(images/[^"]+)"', html)
print("images on page:", imgs)
for i in imgs[:4]:
    c, _ = get("/" + i)
    print(f"  {c}  {i}")

# spot-check the pages that used to carry stock
for p in ["/waterproofing-cape-town", "/roof-waterproofing-cape-town", "/roof-repairs-cape-town",
          "/leaking-ceiling-repair", "/waterproofing-durbanville"]:
    c, h = get(p)
    print(f"{p:40s} {c}  stock-credit={'Illustrative photograph' in h}")
