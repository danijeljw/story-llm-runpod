# Repository agent guidance

This is a multi-series, multi-book, multi-story fiction source repository. Read [README](README.md), [architecture](docs/architecture.md) and [workflow](docs/workflow.md) before changing layout or generation behaviour.

- Local sources and curated references are canonical. RunPod is disposable GGUF/llama.cpp compute. Do not add PyTorch, Transformers or vLLM without a request.
- Universal guidance/templates belong in `authoring/`; fictional canon and series style belong in `series/<slug>/bible/`. Never blend unrelated continuities.
- Recurring profiles live in `bible/characters/<slug>/profile.md`, with `character.json` and `references/`. Preserve filenames, image bytes, existing IDs and profile status. Update every dependency when moving assets.
- Books contain `book.json`, `concept.md`, `publication.json` and `stories/`. Each story owns its `story.json`, outline, scenes and tracked drafts. Only raw `generated/` output is ignored.
- `working-world` is an organisational label. Titles are unset. Do not invent canon, titles, ISBNs or publication claims. Preserve existing non-canonical examples and proposed character status.
- Existing unassigned authored prose is in Book 1's `drafts/unassigned/`; it is not an approved manuscript.
- StoryRunner takes `generate --scene <path>` and selects ownership from that path. Story `contextFiles` are relative to the series; missing files and cross-series traversal fail. Reference PNGs are not transmitted by this text client.
- Global prompts and sampler defaults live in `llm/`. `models.json` is not read by code. Rewrite and continuity prompts are not implemented commands.
- Adult-fiction prompt wording must remain unchanged unless requested. Preserve content heading structure where practical because context is sent verbatim.
- `make lint`, `make validate`, `make build`, `make test` are local checks. Never create GPU resources during validation.
- Lifecycle scripts stay in `scripts/runpod`, Pod-side helpers in `scripts/remote`, endpoint helpers in `scripts/local`. Only create.sh sources `.env`; export other settings explicitly.
- Keep secrets, model files, caches and disposable builds out of Git. Retain reviewed source and intentionally archived release packages.
