#!/usr/bin/env python3
import json
import re
import sys

FORBIDDEN = [
    r"(?i)\b(cookie|cookies|browser\s+profile|login\s+data|keychain|credential\s+store)\b",
    r"(?i)\b(id_rsa|id_ed25519|private\s+key|\.ssh/.*(?:id_|authorized_keys))\b",
    r"(?i)\bcat\s+.*(\.env|token|secret|password|passwd)\b",
    r"(?i)\b(disable|stop).*(audit|logging|defender|firewall|security|edr|av)\b",
    r"(?i)\b(nmap|masscan|zmap)\b.*(/\d+|--top-ports|-p-)",
    r"(?i)\b(persistence|backdoor|reverse\s+shell|keylogger)\b",
]

RED = [
    r"(?i)\bsudo\b",
    r"(?i)\b(systemctl|service|launchctl)\s+(start|stop|restart|enable|disable)\b",
    r"(?i)\b(apt|apt-get|yum|dnf|pacman|zypper|brew)\s+(install|upgrade|remove|autoremove)\b",
    r"(?i)\b(chmod|chown)\s+(-R\s+)?",
    r"(?i)\brm\s+(-rf|-fr)\b",
    r"(?i)\b(nohup|setsid)\b|&\s*$",
    r"(?i)\b(crontab|schtasks)\b",
    r"(?i)\biptables|ufw|firewall-cmd\b",
]

YELLOW = [
    r"(?i)\b(git\s+clone|git\s+pull)\b",
    r"(?i)\b(npm|pnpm|yarn)\s+(install|ci|run|test|build)\b",
    r"(?i)\b(pip|pip3|python\s+-m\s+pip)\s+install\b",
    r"(?i)\b(cargo|go|mvn|gradle)\s+(test|build|install)\b",
    r"(?i)\bmkdir\s+-p\b",
    r"(?i)\btouch\b|\btee\b|>\s*[^&]",
    r"(?i)\bpython\b.*\.py\b",
]

GREEN = [
    r"(?i)^\s*(command\s+-v|which)\s+",
    r"(?i)^\s*tailscale\s+(version|status)(\s+--json)?\s*$",
    r"(?i)^\s*(hostname|uname\s+-a|pwd|id\s+-un|whoami|date)\s*$",
    r"(?i)^\s*(ls|find|du|df)\b",
    r"(?i)^\s*git\s+(status|remote|branch|rev-parse|log)\b",
    r"(?i)^\s*(python3?|node|npm|go|cargo|rustc|java)\s+--version\s*$",
]

def classify(cmd: str):
    for pat in FORBIDDEN:
        if re.search(pat, cmd):
            return "FORBIDDEN", "Matches forbidden remote-operation pattern"
    for pat in RED:
        if re.search(pat, cmd):
            return "RED", "May change system state, security posture, permissions, packages, services, or long-running processes"
    for pat in YELLOW:
        if re.search(pat, cmd):
            return "YELLOW", "May change project/workdir state or consume notable resources"
    for pat in GREEN:
        if re.search(pat, cmd):
            return "GREEN", "Read-only or low-side-effect diagnostic command"
    return "YELLOW", "Unrecognized command; treat conservatively"

def main():
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
    else:
        cmd = sys.stdin.read().strip()

    if not cmd:
        print(json.dumps({"class": "YELLOW", "reason": "empty command"}, ensure_ascii=False))
        return

    klass, reason = classify(cmd)
    print(json.dumps({"command": cmd, "class": klass, "reason": reason}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
