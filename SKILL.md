---
name: axonlink
description: Manually replicate an existing local workflow on a user-authorized remote computer through Tailscale CLI and Tailscale SSH. Use only when the user explicitly asks for remote execution, remote workflow replication, or moving an agent-owned workflow to another named machine.
when_to_use: Trigger only through direct user invocation such as /axonlink, "远控这台机器", "把这个流程复制到另一台电脑", "在远端机器复刻当前工作流", or "用 Tailscale SSH 到目标机器执行". Never use automatically for ordinary build, test, deploy, debug, file editing, or environment setup.
argument-hint: "<user@target-or-target> <workflow-goal>"
arguments:
  - target
  - workflow_goal
disable-model-invocation: true
---

# AxonLink

## Operating principle

This skill helps the agent owner replicate an already-known workflow on another authorized computer. The backend is Tailscale CLI / Tailscale SSH. Treat this as an authorized remote administration workflow, not as generic remote control.

Only proceed when the user has explicitly requested remote operation and has named or approved the target machine.

## Required supporting files

Load these only when needed:

- `references/safety-policy.md`: command classes, refusal rules, approval thresholds.
- `references/tailscale-ops.md`: Tailscale CLI checks, target resolution, preflight commands.
- `references/memory-condensation.md`: how to turn a successful remote run into a reusable workflow recipe.
- `templates/remote-run-report.md`: final report format.
- `templates/workflow-recipe.md`: reusable recipe format.
- `scripts/check-tailscale.sh`: local read-only Tailscale CLI check.
- `scripts/resolve-target.py`: target lookup against `tailscale status --json`.
- `scripts/classify-command.py`: local command-risk classifier.

## Invocation contract

Arguments:

- `target`: Tailscale MagicDNS name, hostname, Tailscale IP, or `user@host`.
- `workflow_goal`: the workflow to replicate.

If either is missing, ask for only the missing value.

Do not infer a remote target from context unless the user has just named it in the same turn.

## Phase 0: hard stop conditions

Stop if any of the following is true:

1. The user has not explicitly authorized remote operation.
2. The target computer is not named, not in the tailnet, or ambiguous.
3. The user asks for covert access, unauthorized access, credential extraction, stealth persistence, bypassing policy, disabling logs, destructive cleanup outside the approved work directory, or broad scanning.
4. The command would expose new public network access.
5. The command would transfer secrets or private keys between machines.

Explain that this skill supports only authorized workflow replication.

## Phase 1: confirm scope

Before running any local or remote command, state:

- target
- remote OS user, if provided
- workflow goal
- expected side effects
- whether installation, update, login, or remote writes may be needed

Ask for confirmation unless the user's current message already confirms these specifics.

## Phase 2: check local Tailscale CLI

Use the local read-only helper:

```bash
"${CLAUDE_SKILL_DIR}/scripts/check-tailscale.sh"
```

Interpret the result:

- Missing CLI: tell the user Tailscale CLI is not installed; ask whether to install it. Do not install yet.
- CLI present but daemon unavailable: report that the daemon or service is unavailable.
- CLI present but not authenticated: ask whether the user wants to authenticate.
- CLI present and authenticated: continue.
- Version appears old: ask whether to update. Do not update yet.

When proposing install or update, state the detected OS and the intended official installation/update method before doing anything.

## Phase 3: verify target

Prefer machine-readable status:

```bash
tailscale status --json > /tmp/tailscale-status.json
python3 "${CLAUDE_SKILL_DIR}/scripts/resolve-target.py" /tmp/tailscale-status.json "$target"
```

If multiple matches appear, ask the user to choose one.

If no match appears, stop. Do not probe random hosts.

## Phase 4: remote preflight

After target verification and user approval, run the smallest possible remote preflight.

Unix-like default:

```bash
tailscale ssh <user@host> "printf 'remote-ok\n'; hostname; uname -a; pwd; id -un"
```

If the target is Windows, ask before adapting to PowerShell. Do not assume a Windows shell.

Record:

- resolved target
- remote user
- hostname
- OS
- shell
- working directory
- project directory, if known

Do not read secret files, shell histories, private keys, browser data, token stores, or `.env` contents.

## Phase 5: build an execution plan

Create a short plan before any mutating remote command.

Include:

1. local workflow summary
2. files or repositories required
3. remote working directory
4. commands to run
5. expected outputs
6. rollback or cleanup steps
7. commands requiring approval

Classify every proposed command using `scripts/classify-command.py`.

Command approval policy:

- GREEN: read-only checks. May run after target confirmation.
- YELLOW: writes within the approved work directory, test runs, dependency install inside project scope. Ask if it changes files.
- RED: package manager changes, service changes, permission changes, deletion, long-lived processes, system config. Always ask.
- FORBIDDEN: refuse.

## Phase 6: execute in small batches

Use one logical operation per remote command.

Preferred Unix-like pattern:

```bash
tailscale ssh <user@host> "set -euo pipefail; cd <approved-dir>; <one logical operation>"
```

After each major step, summarize:

- command purpose
- success or failure
- important output
- next step

If a command fails:

1. stop
2. explain the failure
3. suggest the smallest diagnostic command
4. ask before making state-changing fixes

## Phase 7: condense memory

After success or a useful stopping point, create a workflow recipe only with user approval.

Default path:

```text
docs/agent-recipes/<workflow-name>.md
```

The recipe must preserve:

- task name
- prerequisites
- environment assumptions
- exact commands that worked
- expected outputs
- failure modes
- cleanup steps
- what not to remember

The recipe must exclude:

- credentials
- tokens
- private keys
- raw `.env` values
- cookies
- browser/session material
- excessive logs
- personal conversational history

## Phase 8: final report

Use `templates/remote-run-report.md`.

Report:

- local Tailscale state
- target
- remote user
- commands executed
- files changed locally
- files changed remotely
- recipe location
- unresolved risks
- next recommended step
