#!/usr/bin/env python3
import sys, json, os, subprocess, socket, ssl, urllib.request
from datetime import datetime

def run_tool(script, args):
    try:
        r = subprocess.run([sys.executable, script] + args, capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout:
            return json.loads(r.stdout)
        return {"error": r.stderr[:200] if r.stderr else "no output"}
    except json.JSONDecodeError:
        return {"error": "invalid JSON output"}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}

def dns_quick(target):
    records = {}
    for t in ['A']:
        try:
            records[t] = socket.gethostbyname(target)
        except:
            records[t] = None
    return records

def port_quick(target):
    common = [21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,6379,8080,8443,9090,27017]
    open_ports = []
    for p in common:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target, p)) == 0:
            try: sv = socket.getservbyport(p)
            except: sv = "unknown"
            open_ports.append({"port": p, "service": sv})
        s.close()
    return open_ports

def ssl_check(target):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = socket.socket()
        s.settimeout(5)
        ss = ctx.wrap_socket(s, server_hostname=target)
        ss.connect((target, 443))
        cert = ss.getpeercert()
        ss.close()
        return {
            "protocol": ss.version(),
            "cipher": ss.cipher()[0] if ss.cipher() else None,
            "expires": cert.get("notAfter", "unknown"),
            "issuer": dict(cert.get("issuer", []))
        }
    except:
        return {"error": "SSL check failed"}

def header_check(target):
    try:
        r = urllib.request.urlopen(f"https://{target}", timeout=10)
        h = {k.lower(): v for k, v in dict(r.headers).items()}
        security = {
            "hsts": "strict-transport-security" in h,
            "csp": "content-security-policy" in h,
            "xfo": h.get("x-frame-options", "MISSING"),
            "xcto": h.get("x-content-type-options", "MISSING")
        }
        return {"status": r.getcode(), "server": h.get("server", "unknown"), "security_headers": security}
    except Exception as e:
        return {"error": str(e)[:100]}

def generate_report(target):
    print(f"[*] Scanning {target}...")
    results = {
        "target": target,
        "scan_time": datetime.now().isoformat(),
        "dns": dns_quick(target),
        "ports": port_quick(target),
        "ssl": ssl_check(target),
        "http": header_check(target)
    }
    results["summary"] = {
        "open_ports": len(results["ports"]),
        "has_ssl": "error" not in results["ssl"],
        "http_status": results["http"].get("status"),
        "hsts_enabled": results["http"].get("security_headers", {}).get("hsts", False)
    }
    return results

def print_report(data):
    t = data["target"]
    print(f"\n{'='*60}")
    print(f"  RECON REPORT: {t}")
    print(f"  Time: {data['scan_time']}")
    print(f"{'='*60}")

    print(f"\n[+] DNS")
    print(f"    IP: {data['dns'].get('A', 'N/A')}")

    print(f"\n[+] Open Ports ({data['summary']['open_ports']} found)")
    if data["ports"]:
        for p in data["ports"]:
            print(f"    {p['port']:5d}/{p['service']:<15s}")
    else:
        print("    None found")

    if "error" not in data.get("ssl", {}):
        print(f"\n[+] SSL/TLS")
        print(f"    Protocol: {data['ssl'].get('protocol')}")
        print(f"    Cipher: {data['ssl'].get('cipher')}")
        print(f"    Expires: {data['ssl'].get('expires')}")

    if "error" not in data.get("http", {}):
        s = data["http"].get("security_headers", {})
        print(f"\n[+] HTTP Headers")
        print(f"    Status: {data['http'].get('status')}")
        print(f"    Server: {data['http'].get('server')}")
        print(f"    HSTS: {'✓' if s.get('hsts') else '✗ MISSING'}")
        print(f"    CSP: {'✓' if s.get('csp') else '✗ MISSING'}")
        print(f"    XFO: {s.get('xfo')}")
        print(f"    XCTO: {s.get('xcto')}")

    print(f"\n{'='*60}")
    print(f"  Report complete. JSON: recon_{t}.json")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 recon-report.py example.com [--json]")
        sys.exit(1)
    target = sys.argv[1]
    report = generate_report(target)
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    with open(f"recon_{target}.json", "w") as f:
        json.dump(report, f, indent=2)
