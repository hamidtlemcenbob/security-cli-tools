#!/usr/bin/env python3
import sys, json, urllib.request, re
from urllib.parse import urljoin

def extract_urls(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64)")
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        found = set()
        for pattern in [r'href=["\']([^"\']+)["\']', r'src=["\']([^"\']+)["\']', r'action=["\']([^"\']+)["\']']:
            for m in re.finditer(pattern, html, re.I):
                u = m.group(1)
                if u.startswith("http"):
                    found.add(u)
                elif u.startswith("//"):
                    found.add("https:" + u)
                elif u.startswith("/"):
                    found.add(url.rstrip("/") + u)
                elif u.startswith("data:"):
                    continue
                else:
                    found.add(url.rstrip("/") + "/" + u)
        return {
            "source": url,
            "total_urls_found": len(found),
            "urls": sorted(found)[:100],
            "truncated": len(found) > 100
        }
    except Exception as e:
        return {"source": url, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 url-extract.py https://example.com")
        sys.exit(1)
    print(json.dumps(extract_urls(sys.argv[1]), indent=2))
