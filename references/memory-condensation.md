# Memory Condensation Reference

## Goal

Convert a successful or partially successful remote workflow into a compact reusable recipe.

The recipe should preserve technical essence. It should not preserve full conversational history.

## What to keep

- task name
- local project context
- target class, not unnecessary target identity
- prerequisites
- environment assumptions
- exact commands that worked
- expected outputs
- meaningful failure modes
- cleanup steps
- verification steps
- known limitations

## What to exclude

- credentials
- tokens
- private keys
- cookies
- raw `.env` contents
- password manager data
- browser/session state
- personal conversation fragments
- irrelevant logs
- temporary failed commands that taught nothing

## Recipe path

Default:

```text
docs/agent-recipes/<workflow-name>.md
```

If the project has another docs convention, follow it.

## Compression rule

Reduce the workflow to the smallest form that lets another agent repeat it safely.

Prefer:

```text
Prerequisite → Command → Expected result → Failure handling
```

Avoid:

```text
Long story → raw transcript → unfiltered terminal output
```

## Privacy rule

If a path, hostname, username, or machine identity is sensitive but not technically necessary, generalize it.

Example:

```text
Use "GPU Linux workstation with CUDA 12" instead of "alice-personal-gpu-laptop".
```
