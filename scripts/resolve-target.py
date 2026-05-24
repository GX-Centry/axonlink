#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

def normalize_host(value: str) -> str:
    value = value.strip()
    if "@" in value:
        value = value.split("@", 1)[1]
    value = value.rstrip(".")
    return value.lower()

def load_status(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def peer_records(status):
    peers = status.get("Peer", {}) or {}
    for key, peer in peers.items():
        dns = peer.get("DNSName") or ""
        host = peer.get("HostName") or ""
        addrs = peer.get("TailscaleIPs") or []
        os_name = peer.get("OS") or ""
        online = peer.get("Online", None)
        yield {
            "key": key,
            "dns_name": dns,
            "hostname": host,
            "tailscale_ips": addrs,
            "os": os_name,
            "online": online,
            "raw": peer,
        }

def match_score(peer, target):
    t = normalize_host(target)
    candidates = []
    if peer["dns_name"]:
        candidates.append(peer["dns_name"].rstrip(".").lower())
        candidates.append(peer["dns_name"].split(".")[0].lower())
    if peer["hostname"]:
        candidates.append(peer["hostname"].lower())
    candidates += [ip.lower() for ip in peer["tailscale_ips"]]

    if t in candidates:
        return 100
    if any(c.startswith(t + ".") for c in candidates):
        return 90
    if any(t in c for c in candidates if len(t) >= 3):
        return 50
    return 0

def main():
    if len(sys.argv) != 3:
        print("usage: resolve-target.py <tailscale-status.json> <target>", file=sys.stderr)
        sys.exit(2)

    path, target = sys.argv[1], sys.argv[2]
    status = load_status(path)
    matches = []
    for peer in peer_records(status):
        score = match_score(peer, target)
        if score:
            matches.append((score, peer))

    matches.sort(key=lambda x: x[0], reverse=True)

    result = {
        "target": target,
        "match_count": len(matches),
        "matches": [
            {
                "score": score,
                "dns_name": peer["dns_name"],
                "hostname": peer["hostname"],
                "tailscale_ips": peer["tailscale_ips"],
                "os": peer["os"],
                "online": peer["online"],
            }
            for score, peer in matches[:10]
        ],
    }

    if len(matches) == 1 and matches[0][0] >= 90:
        result["resolution"] = "unique"
    elif len(matches) == 0:
        result["resolution"] = "none"
    else:
        result["resolution"] = "ambiguous"

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
