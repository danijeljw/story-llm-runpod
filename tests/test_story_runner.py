"""Exercise the real client with isolated multi-series fixtures and a loopback API."""
import json
import os
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / 'tools/StoryRunner/bin/Debug/net10.0/StoryRunner.dll'


class StoryRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(['dotnet', 'build', str(ROOT / 'tools/StoryRunner'), '--nologo'], check=True, capture_output=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.requests = []
        self.status = 200
        self.reply = {'choices': [{'message': {'role': 'assistant', 'content': 'Generated test prose.'}}]}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.headers.get('Transfer-Encoding') == 'chunked':
                    chunks = []
                    while True:
                        size = int(self.rfile.readline().strip().split(b';')[0], 16)
                        if size == 0:
                            self.rfile.readline()
                            break
                        chunks.append(self.rfile.read(size))
                        self.rfile.read(2)
                    payload = b''.join(chunks)
                else:
                    payload = self.rfile.read(int(self.headers['Content-Length']))
                owner.requests.append((self.path, json.loads(payload)))
                self.send_response(owner.status)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(owner.reply).encode())

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.write('llm/config/generation.json', {'temperature': 0.72, 'max_tokens': 1234})
        self.write('llm/prompts/system.md', 'SYSTEM')
        self.write('llm/prompts/scene-generation.md', 'TASK')
        self.write('authoring/guidance.md', 'UNIVERSAL')
        for series in ('alpha', 'beta'):
            self.write(f'series/{series}/series.json', {'id': series})
            self.write(f'series/{series}/bible/timeline.md', series.upper() + ' CANON')
            for book in ('book-01', 'book-02'):
                self.write(f'series/{series}/books/{book}/book.json', {'id': book})
                for story in ('story-01', 'story-02'):
                    base = f'series/{series}/books/{book}/stories/{story}'
                    self.write(base + '/story.json', {'contextFiles': ['bible/timeline.md']})
                    self.write(base + '/scenes/scene-01.md', f'{series}/{book}/{story} SCENE')
        self.base = 'series/alpha/books/book-01/stories/story-01'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def write(self, path, value):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) if isinstance(value, dict) else value)

    def run_client(self, scene=None, cwd=None):
        scene = scene or self.base + '/scenes/scene-01.md'
        env = dict(os.environ, LLM_BASE_URL=f'http://127.0.0.1:{self.server.server_port}', LLM_MODEL='test-model')
        return subprocess.run(['dotnet', str(CLIENT), 'generate', '--scene', str(self.root / scene)],
                              cwd=cwd or self.root, env=env, capture_output=True, text=True, timeout=15)

    def test_request_contract_and_selected_series(self):
        result = self.run_client()
        self.assertEqual(result.returncode, 0, result.stderr)
        path, body = self.requests[0]
        self.assertEqual(path, '/v1/chat/completions')
        self.assertEqual(body['model'], 'test-model')
        self.assertEqual(body['temperature'], 0.72)
        self.assertEqual(body['max_tokens'], 1234)
        self.assertEqual(body['messages'][0], {'role': 'system', 'content': 'SYSTEM'})
        context = body['messages'][1]['content']
        for expected in ('UNIVERSAL', 'ALPHA CANON', 'TASK', 'alpha/book-01/story-01 SCENE'):
            self.assertIn(expected, context)
        self.assertNotIn('BETA CANON', context)
        self.assertNotIn('book-02/story-02 SCENE', context)

    def test_outputs_do_not_collide_across_series_books_stories(self):
        for series, book, story in [('alpha', 'book-01', 'story-01'), ('beta', 'book-01', 'story-01'),
                                    ('alpha', 'book-02', 'story-01'), ('alpha', 'book-01', 'story-02')]:
            base = f'series/{series}/books/{book}/stories/{story}'
            self.assertEqual(self.run_client(base + '/scenes/scene-01.md').returncode, 0)
            outputs = list((self.root / base / 'generated').glob('*.md'))
            self.assertEqual(len(outputs), 1)
            self.assertEqual(outputs[0].read_text(encoding='utf-8-sig'), 'Generated test prose.\n')

    def test_nested_working_directory(self):
        result = self.run_client(cwd=self.root / self.base / 'scenes')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cross_series_context_rejected_before_request(self):
        self.write(self.base + '/story.json', {'contextFiles': ['../beta/bible/timeline.md']})
        result = self.run_client()
        self.assertEqual(result.returncode, 1)
        self.assertIn('escapes selected series', result.stderr)
        self.assertEqual(self.requests, [])

    def test_missing_context_rejected_before_request(self):
        self.write(self.base + '/story.json', {'contextFiles': ['bible/missing.md']})
        self.assertEqual(self.run_client().returncode, 1)
        self.assertEqual(self.requests, [])

    def test_image_context_rejected_before_request(self):
        self.write('series/alpha/bible/photo.png', 'binary placeholder')
        self.write(self.base + '/story.json', {'contextFiles': ['bible/photo.png']})
        self.assertEqual(self.run_client().returncode, 1)
        self.assertEqual(self.requests, [])

    def test_scene_outside_hierarchy_rejected(self):
        self.write('scene.md', 'UNOWNED')
        self.assertEqual(self.run_client('scene.md').returncode, 1)
        self.assertEqual(self.requests, [])

    def test_http_error_does_not_write_prose(self):
        self.status = 503
        self.reply = {'error': 'unavailable'}
        self.assertEqual(self.run_client().returncode, 2)
        self.assertFalse((self.root / self.base / 'generated').exists())

    def test_empty_response_does_not_write_prose(self):
        self.reply = {'choices': []}
        self.assertEqual(self.run_client().returncode, 3)
        self.assertFalse((self.root / self.base / 'generated').exists())

    def test_malformed_metadata_rejected_before_request(self):
        self.write(self.base + '/story.json', '{invalid')
        self.assertEqual(self.run_client().returncode, 1)
        self.assertEqual(self.requests, [])


if __name__ == '__main__':
    unittest.main()
