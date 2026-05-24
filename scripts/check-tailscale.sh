#!/usr/bin/env bash
set -u

json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

emit_json() {
  local key="$1"
  local value="$2"
  printf '"%s": %s' "$key" "$value"
}

CLI_PATH="$(command -v tailscale || true)"

printf '{\n'
if [ -z "$CLI_PATH" ]; then
  printf '  "cli_present": false,\n'
  printf '  "cli_path": null,\n'
  printf '  "version": null,\n'
  printf '  "status_available": false,\n'
  printf '  "authenticated_or_daemon_available": false,\n'
  printf '  "message": "tailscale CLI not found"\n'
  printf '}\n'
  exit 0
fi

VERSION_OUTPUT="$(tailscale version 2>&1 || true)"
STATUS_OUTPUT="$(tailscale status --json 2>&1 || true)"
STATUS_RC=0
tailscale status --json >/dev/null 2>&1 || STATUS_RC=$?

printf '  "cli_present": true,\n'
printf '  "cli_path": %s,\n' "$(printf '%s' "$CLI_PATH" | json_escape)"
printf '  "version": %s,\n' "$(printf '%s' "$VERSION_OUTPUT" | json_escape)"
if [ "$STATUS_RC" -eq 0 ]; then
  printf '  "status_available": true,\n'
  printf '  "authenticated_or_daemon_available": true,\n'
  printf '  "status_error": null,\n'
  printf '  "message": "tailscale CLI available and status returned JSON"\n'
else
  printf '  "status_available": false,\n'
  printf '  "authenticated_or_daemon_available": false,\n'
  printf '  "status_error": %s,\n' "$(printf '%s' "$STATUS_OUTPUT" | json_escape)"
  printf '  "message": "tailscale CLI exists, but status JSON was unavailable"\n'
fi
printf '}\n'
