#!/usr/bin/env python3
import ssl, socket, json, sys, datetime
target = sys.argv[1] if len(sys.argv) > 1 else input("Domain: ")
ctx = ssl.create_default_context()
ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
s = socket.socket()
s.settimeout(5)
ss = ctx.wrap_socket(s, server_hostname=target)
ss.connect((target, 443))
cert = ss.getpeercert()
print(json.dumps({
    "domain": target,
    "protocol": ss.version(),
    "cipher": ss.cipher(),
    "issuer": dict(cert.get("issuer", [])),
    "expiry": cert.get("notAfter"),
    "valid_from": cert.get("notBefore")
}, indent=2))
ss.close()
