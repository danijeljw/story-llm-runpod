# Content templates

Copy only what you need. JSON files define metadata; Markdown files hold prose. Empty headings are writing prompts, not required fields. Retain established character IDs; choose readable local IDs for new entities.

1. New series: copy `series.json` and `series.md` to `series/<slug>/series.json` and `README.md`; set the ID and book order.
2. New book: copy `book.json`, `publication.json`, and `book.md` to `books/book-NN/` inside that series; name the Markdown file `concept.md`, then register the book ID in `series.json`.
3. New story: copy `story.json`, `story.md`, `outline.md`, and `scene.md` to `stories/story-NN/` inside the book; name the scene `scenes/scene-01.md` and register the story ID in `book.json`.
4. New character: copy `character.json` and `character.md` into `bible/characters/<slug>/` (or a story's `characters/<slug>/`); name the Markdown file `profile.md`. Add actual images under `references/` and list their paths and roles in `character.json`.
5. Locations and relationships: use the corresponding Markdown templates when content warrants them. Keep relationship IDs and established location IDs in the Markdown entries.

Story `contextFiles` are relative to the owning series directory. Select relevant bible fragments, character profiles and reference metadata, book concept and story outline. An empty list sends only global guidance, task instructions and the selected scene. Create optional notes, scenes, assets, manuscript and revision directories as material appears.

Publication `editions` entries can later carry an ID, format, ISBN, publication date, trim settings, cover path and target. Keep unknown values unset rather than inventing publication facts. No publisher reads this configuration yet.
