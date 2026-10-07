"""Validate migration integrity failures on minimal authored-content fixtures."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.series = 'series/example'
        self.book = self.series + '/books/book-01'
        self.story = self.book + '/stories/story-01'
        self.write(self.series + '/series.json', {'id': 'example', 'books': ['book-01']})
        self.write(self.book + '/book.json', {'id': 'book-01', 'stories': ['story-01']})
        self.write(self.book + '/publication.json', {'enabled': False, 'editions': []})
        self.write(self.story + '/story.json', {'id': 'story-01', 'contextFiles': []})

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value) if isinstance(value, dict) else value)

    def test_valid_minimal_series(self):
        self.assertEqual(validate(self.root), [])

    def test_unregistered_story(self):
        self.write(self.book + '/book.json', {'id': 'book-01', 'stories': []})
        self.assertTrue(any('order differs' in p for p in validate(self.root)))

    def test_context_cannot_escape_series(self):
        self.write(self.story + '/story.json', {'id': 'story-01', 'contextFiles': ['../other/bible.md']})
        self.assertTrue(any('escapes scope' in p for p in validate(self.root)))

    def test_broken_image_link_with_spaces(self):
        self.write('README.md', '# References\n\n![Portrait](<missing portrait.png>)\n')
        self.assertTrue(any('broken local link' in p for p in validate(self.root)))

    def test_unlisted_reference_image(self):
        base = self.series + '/bible/characters/person'
        self.write(base + '/profile.md', '# Person\n')
        self.write(base + '/references/portrait.png', 'test image')
        self.write(base + '/character.json', {'id': 'CH-PERSON-001', 'profile': 'profile.md', 'references': []})
        self.assertTrue(any('manifest does not match' in p for p in validate(self.root)))

    def test_malformed_metadata_reports_error(self):
        self.write(self.story + '/story.json', '{broken')
        self.assertTrue(any('story.json:' in p for p in validate(self.root)))
