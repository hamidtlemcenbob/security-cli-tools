#!/usr/bin/env python3
import sys, json, hashlib, os

ALGOS = ["md5", "sha1", "sha256", "sha512"]

def compute_hashes(path):
    if not os.path.isfile(path):
        return {"error": f"File not found: {path}"}
    size = os.path.getsize(path)
    hashes = {a: hashlib.new(a) for a in ALGOS}
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                for a in ALGOS:
                    hashes[a].update(chunk)
        return {
            "file": path,
            "size_bytes": size,
            "size_human": f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB",
            "hashes": {a: h.hexdigest() for a, h in hashes.items()}
        }
    except PermissionError:
        return {"error": f"Permission denied: {path}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hash-check.py <file1> [file2 ...]")
        sys.exit(1)
    results = [compute_hashes(f) for f in sys.argv[1:]]
    print(json.dumps(results if len(results) > 1 else results[0], indent=2))
