#!/usr/bin/env python3
import json, sys, subprocess, platform

def run_tool(tool_name, args):
    try:
        r = subprocess.run([tool_name] + args, capture_output=True, text=True, timeout=30)
        return {"status": "ok", "output": r.stdout[:500], "error": r.stderr[:200]}
    except FileNotFoundError:
        return {"status": "not_found", "error": f"{tool_name} not installed"}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "command timed out"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def security_audit():
    results = {"system": platform.platform(), "tools": {}}
    tools = {
        "nmap": ["--version"],
        "sqlmap": ["--version"],
        "nikto": ["-Version"],
        "gobuster": ["version"],
        "ffuf": ["-V"],
        "hydra": ["-V"],
        "john": ["--version"],
        "whatweb": ["--version"],
        "wpscan": ["--version"],
        "dirb": [""],
        "curl": ["--version"],
        "openssl": ["version"],
        "python3": ["--version"],
    }
    for tool, args in tools.items():
        results["tools"][tool] = run_tool(tool, args)
    results["total_available"] = sum(1 for t in results["tools"].values() if t["status"] == "ok")
    results["total_missing"] = sum(1 for t in results["tools"].values() if t["status"] == "not_found")
    return results

if __name__ == "__main__":
    print(json.dumps(security_audit(), indent=2))
