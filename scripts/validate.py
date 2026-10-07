#!/usr/bin/env python3
"""Validate authored metadata, ownership, context, assets and local Markdown links."""
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate(root):
    errors = []

    def fail(message):
        errors.append(message)

    def load(path):
        try:
            data = json.loads(path.read_text())
            if not isinstance(data, dict):
                raise ValueError('expected a JSON object')
            return data
        except (OSError, ValueError) as exc:
            fail(f'{path.relative_to(root)}: {exc}')
            return {}

    def inside(base, value, file=True):
        if not isinstance(value, str) or not value or Path(value).is_absolute():
            fail(f'{base.relative_to(root)}: invalid relative path {value!r}')
            return None
        target = (base / value).resolve()
        if not target.is_relative_to(base.resolve()):
            fail(f'{base.relative_to(root)}: path escapes scope: {value}')
            return None
        if not (target.is_file() if file else target.is_dir()):
            fail(f'{base.relative_to(root)}: missing path {value}')
        return target

    def identity(path, data):
        if data.get('id') != path.parent.name:
            fail(f'{path.relative_to(root)}: ID must match owning directory')

    def ordering(base, data, field, child_file):
        order = data.get(field)
        if not isinstance(order, list) or any(not isinstance(x, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', x) for x in order):
            fail(f'{base.relative_to(root)}: {field} must be a list of local IDs')
            return
        if len(order) != len(set(order)):
            fail(f'{base.relative_to(root)}: duplicate {field} IDs')
        actual = {p.parent.name for p in (base / field).glob(f'*/{child_file}')}
        if set(order) != actual:
            fail(f'{base.relative_to(root)}: {field} order differs from owned {child_file} directories')
        for value in order:
            inside(base / field, value + '/' + child_file)

    series_root = root / 'series'
    for series in sorted(p for p in series_root.iterdir() if p.is_dir()):
        data = load(series / 'series.json')
        identity(series / 'series.json', data)
        ordering(series, data, 'books', 'book.json')
        for book in sorted((series / 'books').glob('*/')):
            data = load(book / 'book.json')
            identity(book / 'book.json', data)
            ordering(book, data, 'stories', 'story.json')
            publication = load(book / 'publication.json')
            if not isinstance(publication.get('enabled'), bool) or not isinstance(publication.get('editions'), list):
                fail(f'{book.relative_to(root)}: publication requires enabled and editions')
            for story in sorted((book / 'stories').glob('*/')):
                data = load(story / 'story.json')
                identity(story / 'story.json', data)
                context = data.get('contextFiles')
                if not isinstance(context, list):
                    fail(f'{story.relative_to(root)}: contextFiles must be an array')
                    continue
                for item in context:
                    target = inside(series, item)
                    if target and target.suffix not in ('.md', '.json'):
                        fail(f'{story.relative_to(root)}: context must be Markdown or JSON: {item}')
        ids = set()
        for manifest in sorted(series.rglob('character.json')):
            data = load(manifest)
            character_id = data.get('id')
            if not isinstance(character_id, str) or not character_id or character_id in ids:
                fail(f'{manifest.relative_to(root)}: invalid or duplicate character ID')
            else:
                ids.add(character_id)
            inside(manifest.parent, data.get('profile'))
            references = data.get('references')
            if not isinstance(references, list):
                fail(f'{manifest.relative_to(root)}: references must be an array')
                continue
            listed = set()
            for entry in references:
                if not isinstance(entry, dict):
                    fail(f'{manifest.relative_to(root)}: invalid reference entry')
                    continue
                target = inside(manifest.parent, entry.get('path'))
                if target:
                    if target in listed:
                        fail(f'{manifest.relative_to(root)}: duplicate reference path')
                    listed.add(target)
                if not entry.get('role') or not entry.get('canonStatus'):
                    fail(f'{manifest.relative_to(root)}: reference needs role and canonStatus')
            actual = {p.resolve() for p in (manifest.parent / 'references').rglob('*') if p.is_file()}
            if actual != listed:
                fail(f'{manifest.relative_to(root)}: manifest does not match reference files')

    # Inspect tracked source and new non-ignored files, avoiding dependencies and raw outputs.
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root, capture_output=True, check=True)
    for name in set(result.stdout.decode().split('\0')):
        path = root / name
        if not path.is_file() or path.suffix != '.md':
            continue
        text = re.sub(r'^```.*?^```[^\n]*', '', path.read_text(), flags=re.M | re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]*>|[^\s)]+)(?:\s+"[^"]*")?\)', text):
            link = match.group(1).strip('<>')
            if not link or link.startswith('#') or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue
            target = (path.parent / unquote(link.split('#', 1)[0])).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                fail(f'{name}: broken local link {link}')
    return errors


if __name__ == '__main__':
    problems = validate(ROOT)
    for problem in problems:
        print(problem)
    print(f'Validation: {len(problems)} error(s).')
    raise SystemExit(bool(problems))
