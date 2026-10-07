# story-llm-runpod

A local-first source system for multiple fiction series, books and substantial short stories. Each series owns one world or continuity. A book may be a themed collection, a linked-story mosaic or a continuous novel. The repository holds authored sources and curated references; disposable RunPod GPUs run GGUF models through llama.cpp.

## Repository map

```text
authoring/
  guidance.md                 universal authoring and canon conventions
  characters.md               reusable character development guidance
  templates/                  small Markdown and JSON starter files
series/
  working-world/              neutral label for the existing unnamed continuity
    series.json               stable ID, title and book ordering
    bible/
      style-guide.md          this series' fantasy voice
      timeline.md
      relationships.md
      locations.md
      characters/
        marek-ilyan/
          profile.md
          character.json      existing character ID and reference manifest
          references.md       clickable image index
          references/         descriptive PNG filenames
        lucan-serris/         same profile/manifest/reference pattern
    books/
      book-01/
        book.json             title, form, status and story ordering
        concept.md            original mosaic-book outline
        publication.json      disabled until editions are configured
        drafts/unassigned/    existing authored prose, story assignment unknown
        stories/
          story-01/
            story.json        identity, status and explicit context file list
            outline.md
            scenes/scene-01.md
            drafts/           tracked reviewed/edited prose
            generated/        ignored raw LLM output
llm/
  config/generation.json      shared sampler settings
  config/models.json          model profile catalogue (documentation only)
  prompts/                    system, scene, rewrite and continuity prompts
scripts/
  local/                      local endpoint helpers
  runpod/                     disposable compute lifecycle
  remote/                     scripts executed on the GPU Pod
tools/StoryRunner/             .NET 10 client and context assembly
docs/                         architecture, workflow and model testing
```

Create a new series in `series/<slug>/`, a book in its `books/book-NN/`, and a story in the book's `stories/story-NN/`. Start with [the templates](authoring/templates/README.md). Add directories only when they contain actual material. Titles live in JSON; folder names and stable local IDs need not change when titles change. Series IDs are project-unique; book IDs are series-local and story IDs are book-local. Fully qualify a story as `working-world/book-01/story-01`. Existing `CH-MAREK-001` and `CH-LUCA-001` IDs are preserved.

## Bible and references

Universal conventions and templates live in `authoring/`. Actual people, places, organisations, world rules and chronology belong to that series' `bible/`. No series automatically inherits another's fictional facts or fantasy style. Keep one canonical profile per recurring character. Temporary characters may live in a story's `characters/<slug>/`; promote them when they recur and update references rather than duplicate canon.

Character images are durable sources next to their profile, partitioned by character. `character.json` records the profile path, canon status and image paths/roles relative to the character directory. `references.md` is the browsable index. Images have descriptive filenames, visually inspected roles and descriptions. Original filenames remain in the manifests for provenance; canonical priority remains unassigned. A text-only LLM receives selected profiles and JSON reference descriptions, not PNG bytes. Future vision tools can use those same manifests.

## Sources, generation and publication

Markdown holds concepts, outlines, notes, prose, reviews and world facts. JSON holds IDs, ordering, metadata and configuration. Reviewed drafts are tracked under `drafts/`; accepted prose can move to a story's `manuscript/`. Raw outputs go to ignored story `generated/` directories. Promote useful output by editing/copying it into tracked sources and committing it. Git-ignored output is not a backup; retain important work before removing a worktree.

Book metadata lives in `book.json`; edition and format settings belong in `publication.json`. Neither is a publishing implementation. As content develops, keep cover sources in the book's `assets/`, editorial decisions in `reviews/`, and deliberately retained edition packages in `releases/<edition-id>/`. Disposable transformations belong under root `build/<series>/<book>/<edition>/`; local release staging belongs under ignored `dist/`. These directories are created when needed. Publication order is the `stories` array, independent of canonical chronology. Unknown titles, ISBNs and release dates remain unset.

See [architecture and migration](docs/architecture.md) and [writing workflow](docs/workflow.md).

## Local verification and generation

Prerequisites: Node/npm, Python 3, .NET 10 SDK; Bash for infrastructure helpers.

```bash
npm ci
make lint
make validate
make build
make test
```

`validate` checks JSON ownership/order, selected context paths, character manifests and local Markdown links. `test` uses an isolated repository fixture and a loopback mock endpoint; no GPU or credentials are required.

```bash
dotnet run --project tools/StoryRunner -- generate \
  --scene series/working-world/books/book-01/stories/story-01/scenes/scene-01.md
```

The scene must belong to a series/book/story. `story.json` selects text context paths relative to its series; missing context and paths outside that series fail before an API call. Add relevant character profiles, reference manifests and location entries deliberately. No indiscriminate bible scan occurs. Global guidance and shared task prompts are also included. Shared settings come from `llm/config/generation.json`; `LLM_BASE_URL` and `LLM_MODEL` are process environment variables. Output goes to that story's `generated/` directory with a UTC timestamp. Rewrite and continuity prompts remain reusable material rather than implemented commands.

## Disposable RunPod sessions

See [the retained setup guide](docs/runpod.md) for GGUF rationale, initial GPU guidance and step-by-step setup.

Install `runpodctl` and `jq`, configure your RunPod API key locally and copy `.env.example` to `.env`. Keep secrets and GGUF files out of Git. Only `create.sh` sources `.env`; other scripts and StoryRunner require exported environment variables. The `.env.example` GPU name contains spaces: quote it when making a shell-compatible `.env`.

```bash
./scripts/runpod/create.sh
./scripts/runpod/status.sh
./scripts/runpod/ssh.sh <pod-id>
# Execute remote/bootstrap-llama.sh on the Pod after installing llama-server.
./scripts/runpod/tunnel.sh <ssh-host> [ssh-port] [ssh-user]
./scripts/local/health.sh
# Run StoryRunner locally through the tunnel; review the result locally.
./scripts/runpod/terminate.sh <pod-id>
```

The equivalent Make wrappers accept `POD_ID`, `SSH_HOST`, `SSH_PORT` and `SSH_USER`. The persistent remote volume is for `/workspace/models`, `/workspace/cache` and `/workspace/runtime`, never canonical manuscripts. Existing download/bootstrap/lifecycle helpers are retained. Pod creation has a configured termination limit. See [model testing](docs/model-testing.md) for the existing GGUF evaluation guidance.
