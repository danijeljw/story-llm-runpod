# Architecture

## Principle

The local repository is canonical. RunPod is disposable acceleration.

```text
LOCAL MAC
  |
  | prompts/context
  v
SSH tunnel -> RunPod Pod -> llama.cpp -> GGUF
  ^                              |
  | generated text               |
  +------------------------------+
```

The Pod may be deleted after every writing session.

## Persistent RunPod storage

Only persistent operational assets belong on the network volume:

```text
/workspace/models
/workspace/cache
/workspace/runtime
```

Do not rely on Pod-local storage for anything you care about.

## Manuscript data

Canonical writing data remains local:

```text
story-bible/
outline/
scenes/
chapters/
drafts/
prompts/
```

Git tracks all deliberate human edits and structure.
