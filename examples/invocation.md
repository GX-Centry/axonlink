# AxonLink Invocation Examples

## Basic

```text
/axonlink devbox "replicate the current project's test workflow"
```

## Explicit user

```text
/axonlink alice@linux-gpu "move the data preprocessing workflow to the GPU node"
```

## Expected first response

Claude should not immediately run remote commands. It should restate:

- target
- user
- workflow goal
- possible side effects
- local Tailscale checks it wants to run

Then it should ask for confirmation unless confirmation was already explicit.
