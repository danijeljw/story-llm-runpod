# Architecture and migration

## Ownership

The project contains independent series/worlds. Each series owns its bible and books; each book owns its metadata, concept and ordered stories. Each story owns scene briefs, drafts and generation output. A book does not imply a single continuous narrative.

Universal authoring conventions and reusable templates live in `authoring/`; actual fictional facts live only in the relevant series. The existing fantasy voice belongs in `working-world/bible/style-guide.md` because it explicitly defines that series' style. Root prompts are shared task instructions, preserved verbatim under `llm/prompts/`.

At five series and fifty books, scripts can enumerate `series.json` and `book.json` without reading all manuscripts. Character directories partition thousands of references by owner. Composite series/book/story IDs distinguish identically numbered entities. IDs remain stable after display-title changes; when renaming directories, update IDs/ordering and every path together. Existing character IDs are retained separately from folder slugs.

## Current metadata contract

- `series.json`: `id`, nullable `title`, development `status`, ordered local `books` IDs.
- `book.json`: `id`, nullable title/subtitle, `status`, `form`, ordered local `stories` IDs and contributors.
- `story.json`: `id`, nullable `title`, `status`, and required `contextFiles` array. Paths are relative to the owning series and list only selected Markdown/JSON files.
- `character.json`: existing character `id`, relative `profile`, `canonStatus`, and references with relative `path`, `role` and `canonStatus`.
- `publication.json`: `enabled` and `editions`. Currently disabled with no invented edition data. Future edition entries can carry format, identifiers and settings without scattering book titles across scripts.

The validator enforces ownership, order, context paths and reference integrity. It does not claim to validate publishing readiness, prose quality or every future edition field. Metadata is deliberately small; JSON schemas or a database are not needed for the current content.

## Context and execution

StoryRunner identifies the selected series/book/story from the scene path. It reads required ownership metadata, then assembles universal guidance, explicitly listed series-relative text context, task instructions and the scene. File markers contain repository-relative paths to distinguish repeated filenames. Missing context is an error rather than a silent omission. Cross-series traversal and binary context are rejected. Per-scene facts and previous-scene tails remain in the scene brief; the context list is story-level and can be narrowed for the current task.

Add character profiles, image manifests and specific location/world fragments to the list when relevant. The current client remains text-only: including reference metadata does not mean the model sees images. Future vision/context tools should consume manifests deliberately. Shared sampler defaults and model catalogue live in `llm/config/`; book-specific overrides can be added alongside book metadata when supported by real tooling. No override resolver exists yet.

The existing HTTP contract remains POST `/v1/chat/completions`, with system/user messages, model and sampler settings. The client consumes `choices[0].message.content`. Error responses and empty replies produce no draft. Local mock tests verify this without remote credentials. Future clients/context builders belong in `tools/`; reusable prompts belong in `llm/prompts/`. Infrastructure helpers remain in `scripts/runpod/` and `scripts/remote/`.

The durable repository remains local. The RunPod network volume stores only models, caches and runtime files. No canonical manuscript data moves there.

## Source and publication lifecycle

Concept → outline → tracked draft → revision/review → manuscript → disposable build → retained edition release. Optional notes, revisions, reviews, assets, manuscript and releases directories are created with actual content, not as empty scaffolding.

Ignored story `generated/` output can become canonical after deliberate review and promotion to tracked drafts/manuscript. `build/`, `cache/`, `tmp/` and release staging `dist/` are ignored. Approved edition archives go under a book's tracked `releases/<edition-id>/`; use normal asset-size judgement before committing large bundles. Removing a worktree discards ignored files unless explicitly retained first.

The reference project `how-to-use-ai.com` was inspected for metadata and publishing patterns. Useful principles retained here are JSON authority for ordering/edition settings, separate authored assets, and ignored `dist/`/`tmp/` outputs. Its nonfiction chapter hierarchy and existing PDF assemblers are not copied into this fiction system.

## Migration record

| Original location | Current location | Treatment |
| --- | --- | --- |
| `story-bible/{timeline,relationships,locations,style-guide}.md` | `series/working-world/bible/` | Existing content preserved; style remains series-scoped |
| `story-bible/characters/README.md` | `authoring/characters.md` | Reusable guidance retained; ownership/naming introduction updated |
| `story-bible/characters/<name>.md` | Series `bible/characters/<name>/profile.md` | Existing prose/IDs/status retained; counterpart links and asset index added |
| Character image directories | Character `references/` directories | All 13 PNGs preserved byte-for-byte and filenames unchanged |
| `outline/novel.md` | Book 1 `concept.md` | Existing mosaic concept preserved |
| `outline/chapter-01.md` | Story 1 `outline.md` | Existing substantial-story outline preserved |
| `scenes/chapter-01/scene-01.md` | Story 1 `scenes/scene-01.md` | Existing scene brief preserved |
| `chapters/draft-01.md` | Book 1 `drafts/unassigned/draft-01.md` | Authored variants preserved, not claimed as approved or assigned to Story 1 |
| `prompts/`, `config/` | `llm/prompts/`, `llm/config/` | Content preserved; client paths updated |

`working-world`, `book-01` and `story-01` are organisational IDs. Real titles remain unset. Character reference roles and canonical priority remain unclassified; the manifests make that uncertainty visible rather than guessing from filenames. The unassigned draft and existing planning placeholders remain editorial decisions, not migration failures.

## Validation notes

Markdown lint has narrow exceptions for pre-existing formatting in the unassigned prose and a repeated character subsection heading, preserving authored bytes. Node dependencies are unchanged; the current npm audit reports nine vulnerabilities (three low, one moderate and five high). Dependency remediation is separate from this layout migration. Local checks do not establish live RunPod availability or publication output correctness.
