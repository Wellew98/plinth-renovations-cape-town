import json, sys, urllib.request
from pathlib import Path

URL = "http://127.0.0.1:9210/mcp"
HDRS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2024-11-05",
}
SID_FILE = Path(__file__).with_name(".neo_sid")
SID = {"v": SID_FILE.read_text().strip() if SID_FILE.exists() else None}


def post(payload):
    data = json.dumps(payload).encode()
    h = dict(HDRS)
    if SID["v"]:
        h["mcp-session-id"] = SID["v"]
    req = urllib.request.Request(URL, data=data, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        sid = r.headers.get("mcp-session-id")
        if sid and sid != SID["v"]:
            SID["v"] = sid
            try:
                SID_FILE.write_text(sid)
            except Exception:
                pass
        body = r.read().decode("utf-8", "replace")
    out = None
    for line in body.splitlines():
        if line.startswith("data:"):
            chunk = line[5:].strip()
            if chunk:
                try:
                    out = json.loads(chunk)
                except Exception:
                    pass
    if out is None:
        try:
            out = json.loads(body)
        except Exception:
            out = {"raw": body[:800]}
    return out


def init():
    post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "hermes", "version": "1"}}})
    try:
        post({"jsonrpc": "2.0", "method": "notifications/initialized"})
    except Exception:
        pass


def call(name, args=None, rid=2):
    return post({"jsonrpc": "2.0", "id": rid, "method": "tools/call",
                 "params": {"name": name, "arguments": args or {}}})


def text_of(res):
    import base64
    from pathlib import Path as _P
    try:
        parts = res["result"].get("content", [])
    except Exception:
        return json.dumps(res)[:2000]
    out = []
    for i, p in enumerate(parts):
        if p.get("type") == "text":
            out.append(p.get("text", ""))
        elif p.get("type") == "image" and p.get("data"):
            fp = _P(__file__).parent.parent / "_shots" / "neo-shot.jpg"
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_bytes(base64.b64decode(p["data"]))
            out.append("[image saved: " + str(fp) + "]")
    return "\n".join(out) or json.dumps(res)[:2000]


if __name__ == "__main__":
    init()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        r = post({"jsonrpc": "2.0", "id": 3, "method": "tools/list"})
        tools = r.get("result", {}).get("tools", [])
        for t in tools:
            print("-", t.get("name"), "|", (t.get("description") or "")[:90].replace("\n", " "))
    else:
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        r = call(cmd, args)
        if "error" in r:
            print("ERROR", json.dumps(r["error"])[:1500])
            sys.exit(1)
        print(text_of(r)[:6000])
