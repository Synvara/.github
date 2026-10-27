"""Exercise the exact embedded policy against GitHub-shaped event fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/branch-name.yml'
SOURCE = textwrap.dedent(WORKFLOW.read_text().split("python3 - <<'PY'\n", 1)[1].rsplit('          PY', 1)[0])


def event(branch, login='contributor', kind='User', source=42, target=42):
    return {'pull_request': {
        'head': {'ref': branch, 'repo': {'id': source}},
        'base': {'repo': {'id': target}},
        'user': {'login': login, 'type': kind},
    }}


class BranchPolicyTests(unittest.TestCase):
    def run_policy(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'event.json'
            path.write_text(json.dumps(payload))
            return subprocess.run([sys.executable, '-c', SOURCE],
                                  env={**os.environ, 'GITHUB_EVENT_PATH': str(path)},
                                  capture_output=True, text=True)

    def test_each_supported_type(self):
        for prefix in ('feature', 'fix', 'refactor', 'chore', 'docs'):
            with self.subTest(prefix=prefix):
                self.assertEqual(self.run_policy(event(prefix + '/42-clear-outcome')).returncode, 0)

    def test_slug_boundaries(self):
        self.assertEqual(self.run_policy(event('docs/1-' + 'a' * 80)).returncode, 0)
        self.assertNotEqual(self.run_policy(event('docs/1-' + 'a' * 81)).returncode, 0)

    def test_malformed_branches(self):
        for branch in ('main', 'feature/no-issue', 'feature/0-empty', 'fix/01-leading-zero',
                       'feat/1-short', 'research/1-study', 'epic/1-program', 'docs/1-',
                       'docs/1-UPPER', 'docs/1-under_score', 'docs/1-double--dash',
                       'docs/1-trailing-', 'docs/1-extra/slash', 'docs/1-newline\n'):
            with self.subTest(branch=branch):
                self.assertNotEqual(self.run_policy(event(branch)).returncode, 0)

    def test_genuine_dependabot(self):
        result = self.run_policy(event('dependabot/github_actions/actions/checkout-6', 'dependabot[bot]', 'Bot'))
        self.assertEqual(result.returncode, 0)

    def test_dependabot_lookalikes_and_forks(self):
        for payload in (
            event('dependabot/fake'),
            event('dependabot/fake', 'dependabot[bot]', 'User'),
            event('dependabot/fake', 'other[bot]', 'Bot'),
            event('dependabot/fork', 'dependabot[bot]', 'Bot', source=43),
            event('dependabot/missing', 'dependabot[bot]', 'Bot', source=None, target=None),
            event('arbitrary-name', 'dependabot[bot]', 'Bot'),
        ):
            with self.subTest(payload=payload):
                self.assertNotEqual(self.run_policy(payload).returncode, 0)

    def test_missing_pr_fails_closed(self):
        self.assertNotEqual(self.run_policy({}).returncode, 0)

    def test_branch_text_is_not_executed_or_echoed(self):
        result = self.run_policy(event('docs/1-$(echo secret);`echo other`'))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('secret', result.stdout + result.stderr)
        self.assertNotIn('other', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
