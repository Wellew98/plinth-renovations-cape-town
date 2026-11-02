"""Local preview server that mimics Cloudflare Pages' clean-URL handling.

/http.server returns 404 for /waterproofing, which Pages serves as
waterproofing.html. Testing locally against the real behaviour avoids
discovering broken links only after deploy.
"""
import http.server
import os
import sys

ROOT = r"C:\Users\DELL\OneDrive\Desktop\Plinth Microsite\site-output"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def translate_path(self, path):
        p = super().translate_path(path)
        if os.path.isdir(p):
            idx = os.path.join(p, "index.html")
            if os.path.exists(idx):
                return idx
        if not os.path.exists(p):
            if os.path.exists(p + ".html"):
                return p + ".html"
        return p

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
