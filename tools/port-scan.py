#!/usr/bin/env python3
import socket, sys, concurrent.futures, json

target = sys.argv[1] if len(sys.argv) > 1 else input("IP/Domain: ")
common = [21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,6379,8080,8443,9090,27017]

results = {"target": target, "open_ports": []}
def scan(p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    if s.connect_ex((target, p)) == 0:
        try: sv = socket.getservbyport(p)
        except: sv = "unknown"
        results["open_ports"].append({"port": p, "service": sv})
    s.close()

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
    ex.map(scan, common)

results["total_open"] = len(results["open_ports"])
print(json.dumps(results, indent=2))
