# Writing workflow

1. Choose or create the owning series, book and story using [the templates](../authoring/templates/README.md).
2. Develop the book theme/concept and story outline locally. Set book story order independently of in-world chronology.
3. Update series bible facts and relevant character states. Keep planned ideas distinct from approved canon.
4. Prepare a scene brief and select relevant `contextFiles` in that story's JSON. Include profiles, reference descriptions, location facts, book context and outline only as needed.
5. Start disposable remote compute, load a GGUF with llama.cpp and tunnel its API locally, using the [root instructions](../README.md).
6. Run StoryRunner locally with the full selected scene path. Raw output is saved under that story's ignored `generated/` directory.
7. Review, revise and promote useful text to tracked `drafts/` or `manuscript/`. Put critique/continuity decisions in story `reviews/` when useful.
8. Reconcile approved new facts with the owning series bible. Preserve consequences between stories; do not confuse character belief with objective canon.
9. Validate links/metadata, lint Markdown and commit deliberate sources. Retain important ignored output before cleaning a worktree.
10. Terminate the Pod; persistent remote storage contains operational assets only.

## Publication preparation

When ready, fill book `publication.json` with actual edition/format configuration and confirm story order in `book.json`. Keep cover sources and store descriptions with the book. Build scripts should later assemble accepted manuscripts into `build/<series>/<book>/<edition>/`, stage deliverables in `dist/`, and retain approved release assets in the book's `releases/<edition-id>/`. No publish command exists until a real publisher is implemented.
