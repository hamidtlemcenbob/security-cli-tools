#!/usr/bin/env python3
import sys, json, hashlib, os

def hash_file(path, algo="sha256"):
    h = hashlib.new(algo)
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

def scan_directory(base_path):
    if not os.path.isdir(base_path):
        return {"error": f"Not a directory: {base_path}"}

    results = {}
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for f in files:
            if f.startswith('.'): continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base_path)
            h = hash_file(full)
            if h:
                results[rel] = {
                    "sha256": h,
                    "size": os.path.getsize(full),
                    "modified": os.path.getmtime(full)
                }
    return results

def verify_integrity(baseline, current):
    changes = {"added": [], "removed": [], "modified": [], "unchanged": 0}
    baseline_files = set(baseline.keys())
    current_files = set(current.keys())

    for f in current_files - baseline_files:
        changes["added"].append(f)
    for f in baseline_files - current_files:
        changes["removed"].append(f)
    for f in baseline_files & current_files:
        if baseline[f]["sha256"] != current[f]["sha256"]:
            changes["modified"].append(f)
        else:
            changes["unchanged"] += 1

    return changes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 file-watch.py scan /path/to/dir")
        print("  python3 file-watch.py check /path/to/dir baseline.json")
        sys.exit(1)

    if sys.argv[1] == "scan" and len(sys.argv) >= 3:
        result = scan_directory(sys.argv[2])
        baseline_file = f"baseline_{os.path.basename(sys.argv[2])}.json"
        with open(baseline_file, "w") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({"status": "baseline_created", "file": baseline_file, "files_tracked": len(result)}, indent=2))

    elif sys.argv[1] == "check" and len(sys.argv) >= 4:
        baseline = json.load(open(sys.argv[3]))
        current = scan_directory(sys.argv[2])
        changes = verify_integrity(baseline, current)
        changes["total_baseline"] = len(baseline)
        changes["total_current"] = len(current)
        if any(changes[k] for k in ["added", "removed", "modified"]):
            changes["alert"] = "INTEGRITY_BREACH"
        else:
            changes["alert"] = "CLEAN"
        print(json.dumps(changes, indent=2))
    else:
        print("Invalid arguments")
