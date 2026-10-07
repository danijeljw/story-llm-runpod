# CLAUDE.md

This file guides Claude Code when it works in this repository.

## What this is

A local-first workspace for writing a long-form fiction manuscript, a **linked-story / mosaic fantasy novel**, with help from a self-hosted GGUF model. The model runs under `llama-server` (llama.cpp) on a disposable RunPod GPU Pod.

- **The local repo is canonical.** It holds the story bible, outlines, scenes, prompts and drafts. Git tracks deliberate human edits.
- **RunPod is disposable compute.** Each Pod is created per session and deleted afterwards. Only model files and caches live on the persistent network volume (`/workspace/models`, `/workspace/cache`, `/workspace/runtime`). Manuscript data never goes there.
- The design deliberately uses GGUF with llama.cpp, not PyTorch, vLLM or Transformers. Don't add those unless asked.

Most of the repo is Markdown content and templates. The only code is the bash scripts and one small .NET console app.

## Commands

```bash
npm run lint:md                     # markdownlint-cli2 over all **/*.md (MD013 line length disabled)
dotnet build tools/StoryRunner      # .NET 10 (net10.0)
dotnet run --project tools/StoryRunner -- generate --scene scenes/chapter-01/scene-01.md
./scripts/local/health.sh           # GET $LLM_BASE_URL/health
./scripts/local/test-model.sh       # one-shot chat completion piped to jq
make create | status | health       # wrappers for the scripts
```

There are no tests.

RunPod lifecycle (needs `runpodctl` and `jq`, plus a `.env` copied from `.env.example`):

1. `scripts/runpod/create.sh` sources `.env`, then runs `runpodctl pod create` with the network volume mounted at `/workspace`, SSH enabled and a `--terminate-after` safety limit (6h by default).
2. `scripts/runpod/status.sh` lists Pods.
3. `scripts/runpod/ssh.sh <pod-id>` prints the Pod details, including RunPod's SSH command.
4. `scripts/remote/*.sh` run **on the Pod**, not locally. `download-model.sh <url> [path]` fetches a GGUF. `bootstrap-llama.sh` execs `llama-server` bound to `127.0.0.1:$LLAMA_PORT`. The base image does not include `llama-server`, so it has to be installed or built on the Pod, or a custom image used.
5. `scripts/runpod/tunnel.sh <ssh-host> [port] [user]` forwards local `:8080` to the Pod's llama-server over SSH.
6. `scripts/runpod/terminate.sh <pod-id>` deletes the Pod. The network volume persists.

## Gotchas

- `make ssh`, `make tunnel` and `make terminate` pass no arguments. The underlying scripts require a pod ID or SSH host, so these targets only print usage. The README's step-by-step examples also leave out these arguments.
- Only `create.sh` sources `.env`. StoryRunner and the other scripts read **process environment variables** (`LLM_BASE_URL`, `LLM_MODEL`, `LLAMA_*`) and otherwise fall back to built-in defaults. Export the variables yourself if you need non-default values.
- `.gitignore` excludes generated drafts (`drafts/*.md`), `*.gguf`, `models/` and `.env`. Never commit model files or secrets.

## StoryRunner (`tools/StoryRunner/Program.cs`)

StoryRunner is a single-file top-level-statements program, and its only command is `generate --scene <file>`. It works as follows:

1. It finds the repo root by walking up from the current working directory until it finds `config/generation.json`.
2. It reads the sampler settings from `config/generation.json`: `temperature`, `top_p`, `min_p`, `repeat_penalty` and `max_tokens`.
3. It sends `prompts/system.md` as the system message.
4. It builds the user message by concatenating these files, each wrapped in `--- BEGIN <name> --- / --- END <name> ---` markers and skipped if missing:
   - `story-bible/style-guide.md`
   - `story-bible/timeline.md`
   - `story-bible/relationships.md`
   - `prompts/scene-generation.md`
   - the scene file
5. It POSTs to the OpenAI-compatible `v1/chat/completions` endpoint with a 30-minute timeout.
6. It writes the reply to `drafts/<scene-name>-<yyyyMMdd-HHmmss>.md`.

Exit codes: 1 for bad arguments or a missing file, 2 for an HTTP error, 3 for an empty reply.

The prompt does **not** include `story-bible/characters/`, `story-bible/locations.md`, `outline/`, `prompts/rewrite.md` or `prompts/continuity-check.md`. Scene-specific character, location and previous-scene context has to go in the scene file itself. This follows the "focused context package" strategy in `docs/workflow.md`: never send the whole novel.

## Content layout and conventions

- `story-bible/` holds canonical world facts. `timeline.md` is authoritative for chronology, even when publication order differs. `relationships.md` tracks directional relationship state (IDs look like `REL-a--b`). `characters/` should contain one file per significant character, following the template in its README. `style-guide.md` sets the voice: grounded, character-led fantasy in close third person, one POV per scene.
- `outline/` contains `novel.md`, the architecture of the mosaic novel, and one file per chapter or story (`chapter-NN.md`).
- `scenes/chapter-NN/scene-NN.md` are scene briefs with these sections: Objective, Characters, Location, Continuity required, Previous-scene tail and Instructions. They are the input to StoryRunner.
- `prompts/` contains the LLM prompt templates. `system.md` and `scene-generation.md` are wired into StoryRunner. `rewrite.md` and `continuity-check.md` are not used by any code yet.
- `drafts/` holds raw model output and is git-ignored. `chapters/` is for finished, edited chapters.
- `config/models.json` documents candidate models. Nothing reads it yet. `docs/model-testing.md` describes how to benchmark fiction models.
- Much of the content is still template placeholders (`TBD`, `[Character]`). Keep the existing heading structure when filling them in, because the files are fed to the model verbatim.
- The manuscript is adult fiction. The prompts deliberately tell the model not to moralise and to treat characters as consenting adults. Don't change that wording unless asked.
- Markdown must pass `npm run lint:md`.
