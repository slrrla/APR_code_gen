"""Offline regression tests: fake API client only, no real keys or requests."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import generate_fixes as runner


class FakeResponse:
    def __init__(self, content, finish='stop'):
        self.data = {'id': 'offline-test', 'model': 'fake-returned-model',
                     'usage': {'total_tokens': 10},
                     'choices': [{'finish_reason': finish, 'message': {'content': content}}]}

    def model_dump(self, **kwargs):
        return self.data


class FakeClient:
    def __init__(self, content='```python\nx = 1\n```', error=None):
        self.calls = []
        self.content, self.error = content, error
        self.chat = SimpleNamespace(completions=self)

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return FakeResponse(self.content)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.model = 'gpt-6-luna'
        self.entry = {'case': 'issue_009', 'versions': ['0.45.0'],
                      'input_sha256': {'messages.json': 'test-input-hash'}}
        self.manifest = {'cases': [self.entry]}
        self.folder = self.root / self.model / 'generation' / 'issue_009'
        messages = [{'role': 'system', 'content': 'exact original prompt'},
                    {'role': 'user', 'content': 'only the question and buggy code'}]
        runner.write_json(self.root / '_shared' / 'inputs' / 'issue_009' / 'messages.json', messages)
        self.helper = SimpleNamespace(extract_code=lambda text: text.split('```python\n', 1)[-1].split('```', 1)[0])

    def run_fake(self, client, **kwargs):
        return runner.run_generation(self.root, self.model, self.manifest, self.helper, client, '', **kwargs)

    def test_identical_requests_except_model(self):
        requests = [runner.request_for(self.root, m, self.entry) for m in
                    ('gpt-6-luna', 'gpt-6.1-sol', 'gpt-6-astra', 'gpt-6-sol')]
        for request in requests:
            self.assertEqual(set(request), {'model', 'reasoning_effort', 'messages'})
            self.assertEqual(request['reasoning_effort'], 'medium')
            self.assertEqual(request['messages'], requests[0]['messages'])

    def test_success_and_resume_do_not_regenerate(self):
        client = FakeClient()
        self.assertEqual(self.run_fake(client)['CREATED'], 1)
        before = (self.folder / 'fix_009.py').read_bytes()
        self.run_fake(client)
        self.assertEqual(len(client.calls), 1)
        self.assertEqual((self.folder / 'fix_009.py').read_bytes(), before)

    def test_syntax_errors_retained_without_automatic_retry(self):
        client = FakeClient('```python\ndef invalid(:\n```')
        self.assertEqual(self.run_fake(client)['SYNTAX_ERROR'], 1)
        self.assertTrue((self.folder / 'raw_reply.txt').is_file())
        self.assertTrue((self.folder / 'fix_009.py').is_file())
        self.run_fake(client, retry_api_errors=True)
        self.assertEqual(len(client.calls), 1)

    def test_runtime_error_code_is_not_executed(self):
        client = FakeClient('```python\nraise RuntimeError("must not run")\n```')
        self.assertEqual(self.run_fake(client)['CREATED'], 1)

    def test_recover_saved_response_without_api(self):
        runner.write_json(self.folder / 'response.json', FakeResponse('```python\nx=3\n```').data)
        client = FakeClient()
        self.assertEqual(self.run_fake(client)['CREATED'], 1)
        self.assertEqual(client.calls, [])

    def test_api_error_requires_explicit_retry(self):
        client = FakeClient(error=RuntimeError('temporary API failure'))
        self.assertEqual(self.run_fake(client)['API_ERROR'], 1)
        self.run_fake(client)
        self.assertEqual(len(client.calls), 1)
        client.error = None
        self.assertEqual(self.run_fake(client, retry_api_errors=True)['CREATED'], 1)
        self.assertEqual(len(client.calls), 2)

    def test_interrupted_request_not_silently_repeated(self):
        runner.write_json(self.folder / 'inflight.json', {'started_utc': 'before'})
        client = FakeClient()
        self.run_fake(client)
        self.assertEqual(client.calls, [])

    def test_modified_fix_rejected(self):
        self.run_fake(FakeClient())
        (self.folder / 'fix_009.py').write_text('changed=True', encoding='utf-8')
        with self.assertRaises(RuntimeError):
            runner.check_saved(self.root, self.model, self.manifest)

    def test_key_redaction(self):
        self.assertNotIn('secret-test-key', runner.redact_error(RuntimeError('secret-test-key'), 'secret-test-key'))
        self.assertNotIn('sk-abc123', runner.redact_error(RuntimeError('sk-abc123'), ''))

    def test_truncated_response_not_marked_created_success(self):
        state = runner.finish_response(self.folder, self.entry, self.model,
                                       FakeResponse('```python\nx=1\n```', finish='length').data, self.helper)
        self.assertEqual(state['status'], 'INCOMPLETE_RESPONSE')


if __name__ == '__main__':
    unittest.main()
