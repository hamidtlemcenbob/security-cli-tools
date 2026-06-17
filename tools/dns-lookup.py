#!/usr/bin/env python3
import socket, sys, json
target = sys.argv[1] if len(sys.argv) > 1 else input("Domain: ")
records = {}
for t in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
    try:
        if t == 'A': records[t] = socket.gethostbyname(target)
        elif t == 'MX': records[t] = [str(r) for r in socket.getaddrinfo(target, 25)]
        else: records[t] = "use dig for full records"
    except: records[t] = None
records["ip"] = socket.gethostbyname(target)
print(json.dumps(records, indent=2))
