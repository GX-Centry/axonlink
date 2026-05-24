# Tailscale Operations Reference

## Local checks

Run these before any remote execution:

```bash
command -v tailscale
tailscale version
tailscale status --json
```

The bundled helper performs these checks without installing, updating, logging in, or changing Tailscale state:

```bash
"${CLAUDE_SKILL_DIR}/scripts/check-tailscale.sh"
```

## Target resolution

Use machine-readable status whenever possible:

```bash
tailscale status --json > /tmp/tailscale-status.json
python3 "${CLAUDE_SKILL_DIR}/scripts/resolve-target.py" /tmp/tailscale-status.json "$target"
```

Accept exact matches before fuzzy matches. If multiple peers match, ask the user to choose.

Valid target identifiers may include:

- MagicDNS name
- hostname
- Tailscale IP
- `user@host`

Do not probe unknown hosts. Only use peers returned by `tailscale status --json`.

## Remote preflight

Unix-like target:

```bash
tailscale ssh user@host "printf 'remote-ok\n'; hostname; uname -a; pwd; id -un"
```

If the remote host rejects Tailscale SSH, report the error. Do not attempt policy modification or `tailscale set --ssh` without explicit approval.

## Remote execution pattern

Prefer one operation per command:

```bash
tailscale ssh user@host "set -euo pipefail; cd /approved/path; command"
```

Avoid interactive commands unless the user explicitly wants an interactive session.

Avoid long-running foreground processes. If the workflow needs a server, prefer project-local scripts and a user-approved lifecycle plan.

## File transfer

First version should avoid file transfer unless necessary. Prefer repository clone or reproducible setup commands.

If file transfer is needed:

- ask before upload or download
- transfer only approved files
- do not transfer secrets
- record source and destination
- verify checksums for important files

## Install/update policy

This skill may detect missing or outdated Tailscale CLI, but must not install or update it without user approval.

Before proposing installation or update:

1. detect OS
2. state official method
3. ask for confirmation
4. run only the approved method
5. re-check version and status after completion
