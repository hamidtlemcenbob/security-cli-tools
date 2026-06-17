#!/usr/bin/env python3
import sys, json, urllib.request, socket

def whois_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        # Use whois.iana.org for basic info, then RDAP
        req = urllib.request.Request(f"https://rdap.verisign.com/com/v1/domain/{domain}")
        req.add_header("User-Agent", "Mozilla/5.0")
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            return {
                "domain": domain,
                "ip": ip,
                "registrar": data.get("events", [{}])[0].get("eventAction") if data.get("events") else None,
                "name_servers": [e.get("ldhName") for e in data.get("nameservers", [])] if data.get("nameservers") else [],
                "events": [{"action": e.get("eventAction"), "date": e.get("eventDate")} for e in data.get("events", [])],
                "raw_url": f"https://rdap.verisign.com/com/v1/domain/{domain}"
            }
        except:
            return {"domain": domain, "ip": ip, "note": "RDAP lookup failed, try whois command for full details"}
    except Exception as e:
        return {"domain": domain, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 whois-lookup.py example.com")
        sys.exit(1)
    print(json.dumps(whois_lookup(sys.argv[1]), indent=2))
