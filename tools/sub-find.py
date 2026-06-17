#!/usr/bin/env python3
import socket, sys, json
target = sys.argv[1] if len(sys.argv) > 1 else input("Domain: ")
common = ["www", "mail", "admin", "blog", "shop", "api", "dev", "test",
          "stage", "beta", "app", "m", "mobile", "news", "support", "help",
          "forum", "portal", "cdn", "static", "img", "media", "video",
          "download", "ftp", "ssh", "vpn", "remote", "webmail", "owa",
          "exchange", "cpanel", "whm", "direct", "secure", "login",
          "register", "signup", "docs", "status", "status", "demo",
          "store", "wiki", "en", "ar", "fr", "es", "de", "tr"]
found = []
for sub in common:
    try:
        ip = socket.gethostbyname(f"{sub}.{target}")
        found.append({"subdomain": f"{sub}.{target}", "ip": ip})
    except: pass
print(json.dumps({"domain": target, "subdomains_found": len(found), "results": found}, indent=2))
