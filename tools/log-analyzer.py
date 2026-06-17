#!/usr/bin/env python3
import sys, json, re, os
from collections import Counter
from datetime import datetime

def analyze_access_log(path):
    attacks = {"sqli": 0, "xss": 0, "path_traversal": 0, "scanning": 0, "brute_force": 0}
    status_counts = Counter()
    ip_counts = Counter()
    paths = Counter()
    total = 0

    sqli_pattern = re.compile(r"(\%27|\%22|union.*select|select.*from|drop\s+table|--\s)", re.I)
    xss_pattern = re.compile(r"(<script|<iframe|onerror=|alert\(|%3Cscript)", re.I)
    path_trav_pattern = re.compile(r"(\.\./|\.\.\\|%2e%2e|etc/passwd)", re.I)
    scan_pattern = re.compile(r"(/(admin|wp-admin|backup|config|\.git|\.env|phpmyadmin))", re.I)
    brute_pattern = re.compile(r"(/wp-login|/login|/admin/login|POST.*login)", re.I)

    try:
        with open(path) as f:
            for line in f:
                total += 1
                m = re.search(r'(\d+\.\d+\.\d+\.\d+)\s', line)
                if m: ip_counts[m.group(1)] += 1

                m2 = re.search(r'"\w+\s([^\s]+)\s', line)
                if m2: paths[m2.group(1)] += 1

                m3 = re.search(r'"\s(\d{3})\s', line)
                if m3: status_counts[m3.group(1)] += 1

                if sqli_pattern.search(line): attacks["sqli"] += 1
                if xss_pattern.search(line): attacks["xss"] += 1
                if path_trav_pattern.search(line): attacks["path_traversal"] += 1
                if scan_pattern.search(line): attacks["scanning"] += 1
                if brute_pattern.search(line): attacks["brute_force"] += 1

        return {
            "file": path,
            "total_requests": total,
            "attack_detection": attacks,
            "unique_ips": len(ip_counts),
            "top_ips": ip_counts.most_common(10),
            "status_codes": dict(status_counts),
            "top_paths": paths.most_common(10)
        }
    except FileNotFoundError:
        return {"error": f"File not found: {path}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log-analyzer.py <access_log>")
        sys.exit(1)
    print(json.dumps(analyze_access_log(sys.argv[1]), indent=2))
