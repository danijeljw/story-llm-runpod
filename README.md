# story-llm-runpod

Local-first long-form fiction workspace using disposable RunPod GPU Pods for GGUF inference.

## Architecture

- **Mac/local machine is the source of truth**
  - manuscript
  - story bible
  - characters
  - outlines
  - prompts
  - generated drafts
  - Git history
- **RunPod is disposable compute**
  - create Pod
  - attach persistent network volume
  - run `llama-server`
  - generate
  - copy/save generated output locally
  - terminate Pod
- **RunPod network volume**
  - GGUF model files
  - optional llama.cpp cache
  - no canonical manuscript data

## Why GGUF + llama.cpp

This repository is built around **GGUF inference with llama.cpp**, not PyTorch.

Use PyTorch/Transformers/vLLM later if you decide to:
- fine-tune/train models;
- use a model not well-supported by llama.cpp/GGUF;
- serve high-throughput concurrent workloads;
- use framework-specific inference features.

For a single writer spinning up a GPU only when required, GGUF + llama.cpp is simpler and cheaper operationally.

## Suggested initial GPU

Start with one 48 GB GPU:
- RTX A6000
- A40
- RTX 6000 Ada
- L40 / L40S

Suggested initial model class:
- 20B–30B fiction-tuned GGUF
- Q6_K or Q8_0 where practical

Later, compare against a 70B model using an 80 GB GPU.

## Local prerequisites

```bash
brew install runpod/runpod/runpodctl
brew install jq
```

Configure RunPod:

```bash
runpodctl config --apiKey "$RUNPOD_API_KEY"
```

Copy configuration:

```bash
cp .env.example .env
```

Edit `.env`.

## First-time RunPod storage setup

Create a RunPod network volume from the console or CLI and put its ID in:

```bash
RUNPOD_NETWORK_VOLUME_ID=
```

The network volume should contain:

```text
/workspace/
├── models/
├── cache/
└── runtime/
```

Do **not** use the network volume as the canonical store for manuscript files.

## Workflow

### 1. Start a disposable Pod

```bash
./scripts/runpod/create.sh
```

The script:
- uses the configured GPU;
- attaches the configured RunPod network volume;
- exposes SSH;
- can automatically terminate after a configured safety period.

### 2. Inspect Pod

```bash
./scripts/runpod/status.sh
```

### 3. Connect

```bash
./scripts/runpod/ssh.sh
```

### 4. Bootstrap llama.cpp server on the Pod

```bash
./scripts/remote/bootstrap-llama.sh
```

This starts `llama-server` against the selected GGUF.

### 5. Tunnel the API back to the Mac

```bash
./scripts/runpod/tunnel.sh
```

The local endpoint becomes:

```text
http://127.0.0.1:8080
```

### 6. Generate locally

```bash
dotnet run --project tools/StoryRunner -- \
  generate \
  --scene scenes/chapter-01/scene-01.md
```

The output is saved into `drafts/`.

### 7. Terminate compute

```bash
./scripts/runpod/terminate.sh
```

The Pod disappears. The model/network volume remains.

## Repository layout

```text
story-llm-runpod/
├── .env.example
├── .gitignore
├── README.md
├── Makefile
├── config/
│   ├── generation.json
│   └── models.json
├── docs/
│   ├── architecture.md
│   ├── model-testing.md
│   └── workflow.md
├── prompts/
│   ├── system.md
│   ├── scene-generation.md
│   ├── rewrite.md
│   └── continuity-check.md
├── story-bible/
│   ├── style-guide.md
│   ├── timeline.md
│   ├── locations.md
│   ├── relationships.md
│   └── characters/
│       └── README.md
├── outline/
│   ├── novel.md
│   └── chapter-01.md
├── scenes/
│   └── chapter-01/
│       └── scene-01.md
├── chapters/
│   └── .gitkeep
├── drafts/
│   └── .gitkeep
├── scripts/
│   ├── local/
│   │   ├── health.sh
│   │   └── test-model.sh
│   ├── remote/
│   │   ├── bootstrap-llama.sh
│   │   └── download-model.sh
│   └── runpod/
│       ├── create.sh
│       ├── status.sh
│       ├── ssh.sh
│       ├── tunnel.sh
│       └── terminate.sh
└── tools/
    └── StoryRunner/
        ├── StoryRunner.csproj
        └── Program.cs
```
