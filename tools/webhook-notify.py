#!/usr/bin/env python3
import sys, json, urllib.request, datetime

def send_discord(webhook_url, title, description, fields=None, color=0xff0000):
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    if fields:
        embed["fields"] = [{"name": k, "value": str(v), "inline": True} for k, v in fields.items()]

    payload = {"embeds": [embed]}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(webhook_url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(req)
    return True

def send_slack(webhook_url, title, description):
    payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": title}},
            {"type": "section", "text": {"type": "mrkdwn", "text": description}}
        ]
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(webhook_url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(req)
    return True

def scan_and_notify(target, webhook_url, webhook_type="discord"):
    import socket, ssl, subprocess
    results = {"target": target, "timestamp": datetime.datetime.now().isoformat(), "alerts": []}

    # Quick port scan
    common_ports = [21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,6379,8080,8443,9090,27017]
    open_ports = []
    for p in common_ports[:5]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((target, p)) == 0:
            open_ports.append(p)
        s.close()

    results["open_ports"] = open_ports

    if open_ports:
        results["alerts"].append(f"Found {len(open_ports)} open ports: {open_ports}")

    # Build notification
    title = f"Scan Complete: {target}"
    desc = f"Open ports: {open_ports if open_ports else 'None found'}"

    try:
        if webhook_type == "discord":
            send_discord(webhook_url, title, desc, {"target": target, "ports": str(open_ports), "time": results["timestamp"]})
        else:
            send_slack(webhook_url, title, desc)
        results["notified"] = True
    except Exception as e:
        results["notified"] = False
        results["error"] = str(e)

    return results

if __name__ == "__main__":
    print("Interactive Security Scanner with Webhook Notifications")
    print("="*55)
    target = input("Target domain/IP: ").strip()
    wtype = input("Webhook type (discord/slack): ").strip().lower() or "discord"
    webhook = input("Webhook URL: ").strip()
    if not target or not webhook:
        print("Target and webhook URL required")
        sys.exit(1)
    result = scan_and_notify(target, webhook, wtype)
    print(json.dumps(result, indent=2))
