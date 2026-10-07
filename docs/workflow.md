# Writing workflow

1. Write/update the story bible locally.
2. Write the chapter and scene objective locally.
3. Create a disposable RunPod Pod.
4. Attach persistent model storage.
5. Start `llama-server`.
6. Establish an SSH tunnel.
7. Generate one scene or revision at a time.
8. Save generated output locally.
9. Review and edit locally.
10. Commit deliberate changes to Git.
11. Terminate the Pod.

## Context strategy

Do not send the whole novel on every request.

Build a focused context package containing only:
- system/style rules;
- characters appearing in the scene;
- relevant relationship state;
- relevant timeline facts;
- chapter objective;
- scene objective;
- necessary previous-scene tail.

This reduces drift and wasted context.
