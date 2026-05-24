# AxonLink Invocation Examples

## Basic

```text
/axonlink devbox "replicate the current project's test workflow"
```

## Explicit user

```text
/axonlink alice@linux-gpu "move the data preprocessing workflow to the GPU node"
```

## Chinese

```text
/axonlink devbox "把本机已经跑通的构建和测试流程复刻到远端机器"
```

## Expected first response

Claude should not immediately run remote commands. It should restate:

- target
- user
- workflow goal
- possible side effects
- local Tailscale checks it wants to run

Then it should ask for confirmation unless confirmation was already explicit.
