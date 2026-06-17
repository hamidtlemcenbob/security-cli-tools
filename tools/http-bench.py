#!/usr/bin/env python3
import sys, json, urllib.request, time, statistics

def benchmark(url, count=5):
    if not url.startswith("http"):
        url = "https://" + url
    times = []
    status = None
    for i in range(count):
        start = time.time()
        try:
            r = urllib.request.urlopen(url, timeout=10)
            elapsed = (time.time() - start) * 1000
            times.append(round(elapsed, 1))
            status = r.getcode()
        except Exception as e:
            times.append(None)
    valid = [t for t in times if t is not None]
    if not valid:
        return {"url": url, "error": "All requests failed"}

    return {
        "url": url,
        "requests": count,
        "successful": len(valid),
        "failed": count - len(valid),
        "status_code": status,
        "response_times_ms": {
            "min": min(valid),
            "max": max(valid),
            "avg": round(statistics.mean(valid), 1),
            "median": round(statistics.median(valid), 1),
            "stddev": round(statistics.stdev(valid), 1) if len(valid) > 1 else 0
        },
        "all_times_ms": valid
    }

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("URL: ")
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(json.dumps(benchmark(url, count), indent=2))
