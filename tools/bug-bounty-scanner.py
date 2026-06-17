#!/usr/bin/env python3
import json, sys, socket, urllib.request
from concurrent.futures import ThreadPoolExecutor

def check_endpoint(url, path):
    try:
        req = urllib.request.Request(f"{url}{path}", headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=5)
        return {"path": path, "status": resp.status, "size": len(resp.read())}
    except urllib.error.HTTPError as e:
        return {"path": path, "status": e.code, "size": 0}
    except:
        return {"path": path, "status": 0, "size": 0}

def check_open_redirect(url, path):
    try:
        req = urllib.request.Request(f"{url}{path}", headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.geturl() != f"{url}{path}"
    except:
        return False

def scan(target):
    base = f"https://{target}" if not target.startswith("http") else target
    results = {"target": target, "checks": []}
    paths = [
        "/.git/config", "/.env", "/admin", "/robots.txt", "/sitemap.xml",
        "/wp-admin", "/api", "/swagger.json", "/graphql", "/.well-known/security.txt",
        "/backup", "/config.php", "/phpinfo.php", "/.htaccess", "/.DS_Store"
    ]
    with ThreadPoolExecutor(max_workers=10) as ex:
        for result in ex.map(lambda p: check_endpoint(base, p), paths):
            if result["status"] in [200, 301, 302, 403]:
                r = {"type": "exposed_endpoint", "path": result["path"], "status": result["status"], "severity": "high" if result["status"] == 200 else "medium"}
                results["checks"].append(r)
    redirect_paths = ["//evil.com%2f@", "/%2feval.com", "?url=http://evil.com", "/redirect?url=http://evil.com"]
    for p in redirect_paths:
        if check_open_redirect(base, p):
            results["checks"].append({"type": "open_redirect", "path": p, "severity": "high"})
    results["total_issues"] = len(results["checks"])
    results["risk"] = "HIGH" if any(c["severity"] == "high" for c in results["checks"]) else "MEDIUM" if results["checks"] else "LOW"
    results["bounty_potential"] = results["risk"]
    return results

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else input("Target: ")
    print(json.dumps(scan(t), indent=2))
