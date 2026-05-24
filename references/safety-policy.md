# Safety Policy

## Scope

This skill is for authorized workflow replication on computers that the user owns or is explicitly authorized to administer.

It must not be used for unauthorized access, covert access, credential collection, stealth, persistence, access-control bypass, lateral movement, or disabling security controls.

## Command classes

### GREEN

Read-only, low-side-effect commands.

Examples:

```bash
command -v tailscale
tailscale version
tailscale status --json
hostname
uname -a
pwd
id -un
ls
git status --short
python --version
node --version
```

GREEN commands may run after target confirmation.

### YELLOW

Commands that may change files inside an approved project/work directory or consume moderate resources.

Examples:

```bash
mkdir -p ./workdir
git clone <approved-repo-url>
npm install
pip install -r requirements.txt
cargo test
npm test
python script.py --dry-run
```

Ask before running if the command writes files, installs dependencies, or triggers long-running work.

### RED

Commands with system-level effects, broad deletion, service changes, permission changes, long-running listeners, or package manager changes.

Examples:

```bash
sudo apt install <package>
brew upgrade <package>
systemctl restart <service>
chmod -R ...
chown -R ...
rm -rf <path>
nohup <command> &
```

Always ask before RED commands. Explain impact and rollback if possible.

### FORBIDDEN

Refuse commands or workflows that involve:

- unauthorized access
- covert control
- stealth persistence
- privilege escalation outside normal approved administration
- credential extraction or transfer
- reading private keys, cookies, password stores, browser profiles, token caches, or raw `.env`
- disabling logs or security tools
- bypassing access control
- scanning unrelated machines
- destructive actions outside the approved work directory
- public exposure of services without explicit legitimate deployment context

## Approval language

Use precise confirmations:

```text
I am about to run this on <target> as <user>:

<command>

Class: RED
Expected effect: installs package X system-wide.
Rollback: remove package X with <rollback command> if needed.

Please confirm before I proceed.
```

Do not bundle unrelated mutating commands into one approval.

## Audit minimum

For every remote execution, capture:

- timestamp
- Claude session ID if available
- target
- remote user
- command class
- command purpose
- command string, with secrets redacted
- result summary

Never log secrets.
