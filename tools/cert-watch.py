#!/usr/bin/env python3
import ssl, socket, json, sys, datetime

def check_cert(domain, port=443):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = socket.socket()
        s.settimeout(5)
        ss = ctx.wrap_socket(s, server_hostname=domain)
        ss.connect((domain, port))
        cert = ss.getpeercert()
        ss.close()

        expiry_str = cert.get("notAfter", "")
        valid_from = cert.get("notBefore", "")
        expiry = datetime.datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z") if expiry_str else None
        valid_from_dt = datetime.datetime.strptime(valid_from, "%b %d %H:%M:%S %Y %Z") if valid_from else None
        now = datetime.datetime.now()
        days_left = (expiry - now).days if expiry else None

        return {
            "domain": domain,
            "port": port,
            "valid": True,
            "issuer": dict(cert.get("issuer", [])),
            "subject": dict(cert.get("subject", [])),
            "protocol": ss.version(),
            "cipher": ss.cipher()[0] if ss.cipher() else None,
            "valid_from": valid_from,
            "expires": expiry_str,
            "days_remaining": days_left,
            "status": "EXPIRED" if days_left and days_left < 0 else "CRITICAL" if days_left and days_left < 30 else "WARNING" if days_left and days_left < 60 else "OK"
        }
    except Exception as e:
        return {"domain": domain, "port": port, "valid": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 cert-watch.py domain1 [domain2 domain3 ...]')
        print('       python3 cert-watch.py @domains.txt')
        sys.exit(1)

    domains = []
    for arg in sys.argv[1:]:
        if arg.startswith('@'):
            try:
                with open(arg[1:]) as f:
                    domains.extend([l.strip() for l in f if l.strip()])
            except:
                print(f"Error reading {arg[1:]}")
        else:
            domains.append(arg)

    results = [check_cert(d) for d in domains]
    summary = {"total": len(results), "valid": sum(1 for r in results if r["valid"]), "expiring": [r["domain"] for r in results if r.get("days_remaining") and r["days_remaining"] < 30]}
    print(json.dumps({"results": results, "summary": summary}, indent=2))
