#!/usr/bin/env python3
import sys, json, urllib.request, ssl, socket

target = sys.argv[1] if len(sys.argv) > 1 else input("Domain: ")

result = {"domain": target, "checks": {}}

try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    r = urllib.request.urlopen(f"https://{target}", timeout=10, context=ctx)
    result["checks"]["status"] = r.getcode()
    result["checks"]["server"] = r.headers.get("Server", "unknown")
    result["checks"]["tech"] = []
    for h in ["X-Powered-By", "CF-Ray", "x-amz-rid"]:
        if r.headers.get(h): result["checks"]["tech"].append(f"{h}={r.headers[h]}")
except Exception as e:
    result["checks"]["error"] = str(e)

try:
    ip = socket.gethostbyname(target)
    result["checks"]["ip"] = ip
except:
    result["checks"]["ip"] = "unknown"

print(json.dumps(result, indent=2))
