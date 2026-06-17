#!/usr/bin/env python3
import json, sys, os, subprocess, smtplib, datetime

class AutomationPack:
    def __init__(self):
        self.results = {}

    def backup_dir(self, source, dest=None):
        dest = dest or f"/tmp/backup_{datetime.date.today()}"
        try:
            subprocess.run(["cp", "-r", source, dest], check=True)
            self.results["backup"] = {"status": "ok", "source": source, "dest": dest}
        except Exception as e:
            self.results["backup"] = {"status": "error", "error": str(e)}
        return self.results["backup"]

    def check_ssl_expiry(self, domain):
        import ssl, socket
        try:
            cert = ssl.get_server_certificate((domain, 443))
            x509 = ssl.PEM_cert_to_DER_cert(cert)
            self.results["ssl_check"] = {"domain": domain, "status": "valid"}
        except Exception as e:
            self.results["ssl_check"] = {"domain": domain, "status": "error", "error": str(e)}
        return self.results["ssl_check"]

    def disk_usage(self, path="/"):
        try:
            stat = os.statvfs(path)
            total = stat.f_frsize * stat.f_blocks
            free = stat.f_frsize * stat.f_bfree
            used = total - free
            pct = (used / total) * 100
            self.results["disk"] = {"path": path, "total_gb": round(total / 1e9, 2), "used_gb": round(used / 1e9, 2), "free_gb": round(free / 1e9, 2), "usage_pct": round(pct, 1)}
        except Exception as e:
            self.results["disk"] = {"error": str(e)}
        return self.results["disk"]

    def running_services(self):
        services = []
        for p in ["/var/run/*.pid", "/run/*.pid"]:
            import glob
            for f in glob.glob(p):
                services.append(os.path.basename(f).replace(".pid", ""))
        self.results["services"] = services or ["check manually"]
        return self.results["services"]

    def network_check(self, host="8.8.8.8"):
        result = subprocess.run(["ping", "-c", "1", "-W", "2", host], capture_output=True, text=True)
        self.results["network"] = {"host": host, "reachable": result.returncode == 0}
        return self.results["network"]

    def docker_status(self):
        try:
            r = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True, timeout=5)
            containers = r.stdout.strip().split("\n") if r.stdout.strip() else []
            self.results["docker"] = {"running": len(containers), "containers": containers}
        except:
            self.results["docker"] = {"error": "docker not available"}
        return self.results["docker"]

    def run_all(self):
        print(json.dumps({k: v for k, v in [
            ("disk_usage", self.disk_usage()),
            ("network", self.network_check()),
            ("docker", self.docker_status()),
            ("services", self.running_services()),
        ]}, indent=2))

if __name__ == "__main__":
    a = AutomationPack()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "disk": a.disk_usage()
        elif cmd == "network": a.network_check()
        elif cmd == "docker": a.docker_status()
        elif cmd == "backup" and len(sys.argv) > 2: a.backup_dir(sys.argv[2])
        elif cmd == "ssl" and len(sys.argv) > 2: a.check_ssl_expiry(sys.argv[2])
        elif cmd == "all": a.run_all()
        else: print("Commands: disk, network, docker, backup <dir>, ssl <domain>, all")
        print(json.dumps(a.results, indent=2))
    else:
        a.run_all()
