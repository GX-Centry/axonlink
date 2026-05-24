# Workflow Recipe: <name>

## Purpose

Describe the workflow in one paragraph.

## When to Use

Use when:

- 
- 

Do not use when:

- 
- 

## Prerequisites

- Authorized target:
- OS/runtime assumptions:
- Required repository/files:
- Required tools:
- Required network access:

## Working Directory

```bash
cd <approved-workdir>
```

## Commands

### 1. Preflight

```bash
<command>
```

Expected result:

```text
<expected-output>
```

### 2. Setup

```bash
<command>
```

Expected result:

```text
<expected-output>
```

### 3. Run

```bash
<command>
```

Expected result:

```text
<expected-output>
```

### 4. Verify

```bash
<command>
```

Expected result:

```text
<expected-output>
```

## Failure Modes

| Symptom | Likely Cause | Safe Diagnostic | Fix Requires Approval? |
|---|---|---|---|
|  |  |  |  |

## Cleanup

```bash
<cleanup-command>
```

## What Not to Remember

- No credentials
- No tokens
- No private keys
- No raw `.env`
- No cookies
- No personal conversation history
