#!/usr/bin/env python3
import urllib.request, sys, json
target = sys.argv[1] if len(sys.argv) > 1 else input("URL: ")
if not target.startswith("http"): target = "https://" + target
r = urllib.request.urlopen(target, timeout=10)
headers = dict(r.headers)
print(json.dumps({
    "url": target,
    "status": r.getcode(),
    "headers": {k.lower(): v for k, v in headers.items()},
    "security_flags": {
        "strict_transport_security": "HSTS" if "strict-transport-security" in {k.lower():v for k,v in headers.items()} else "MISSING",
        "x_frame_options": headers.get("X-Frame-Options", "MISSING"),
        "x_content_type_options": headers.get("X-Content-Type-Options", "MISSING"),
        "content_security_policy": "SET" if "content-security-policy" in {k.lower():v for k,v in headers.items()} else "MISSING"
    }
}, indent=2))
