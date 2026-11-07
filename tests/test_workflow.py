import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = str(pathlib.Path(__file__).resolve().parent.parent / 'skills/task/scripts/workflow.py')
spec = importlib.util.spec_from_file_location('workflow', SCRIPT)
wf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wf)


class WorkflowTest(unittest.TestCase):
    def test_colon_form(self):
        r = wf.parse('## Push:Before\nb\n\n## Push\n- a\n\n## push : after\n- c\n')
        self.assertEqual(r['stages']['Push'], {'before': ['b'], 'in': ['- a'], 'after': ['- c']})

    def test_colon_spec_and_plan(self):
        r = wf.parse('## Spec and Plan:After\n- y\n')
        self.assertEqual(r['stages']['Spec']['after'], ['- y'])
        self.assertEqual(r['stages']['Plan']['after'], ['- y'])

    def test_unknown_colon_suffix(self):
        self.assertEqual(wf.parse('## Push:Later\n- x\n')['unknown'], ['Push:Later'])

    def test_spec_and_plan_applies_to_both(self):
        r = wf.parse('## Spec and Plan\n- x\n')
        self.assertEqual(r['stages']['Spec']['in'], ['- x'])
        self.assertEqual(r['stages']['Plan']['in'], ['- x'])

    def test_case_insensitive(self):
        self.assertEqual(wf.parse('## push:AFTER\nz\n')['stages']['Push']['after'], ['z'])

    def test_duplicate_heading_concatenates(self):
        r = wf.parse('## Push\n- a\n## Brief\nq\n## Push\n- b\n')
        self.assertEqual(r['stages']['Push']['in'], ['- a', '- b'])

    def test_empty_heading_is_absent(self):
        r = wf.parse('## Execute\n\n## Push\n- a\n')
        self.assertNotIn('Execute', r['stages'])

    def test_unknown_heading(self):
        self.assertEqual(wf.parse('## Deploy\n- x\n')['unknown'], ['Deploy'])

    def test_unknown_before_after(self):
        self.assertEqual(wf.parse('## After Deploy\n- x\n')['unknown'], ['After Deploy'])

    def test_multiline_bullet(self):
        r = wf.parse('## Plan\n- one\n  two\n- three\n')
        self.assertEqual(r['stages']['Plan']['in'], ['- one\n  two', '- three'])

    def test_placeholders_skip_rabbit_vars(self):
        r = wf.parse('## Push:After\nRun `/x <KEY> <environment>`. Use <spec rules>.\n')
        self.assertEqual(r['placeholders'], ['<environment>', '<spec rules>'])

    def test_text_before_first_heading_ignored(self):
        r = wf.parse('# Rabbit workflow\nintro\n## Push\n- a\n')
        self.assertEqual(r['unknown'], [])
        self.assertEqual(r['stages']['Push']['in'], ['- a'])

    def test_missing_file(self):
        p = subprocess.run([sys.executable, '-I', SCRIPT, '/nonexistent.md'],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 3)
        self.assertIn('workflow file not found: /nonexistent.md', p.stderr)

    def test_usage(self):
        p = subprocess.run([sys.executable, '-I', SCRIPT], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)

    def run_file(self, data, name='w f.md'):
        home = tempfile.mkdtemp()
        pathlib.Path(home, name).write_bytes(data)
        return subprocess.run([sys.executable, '-I', SCRIPT, '~/' + name], capture_output=True,
                              text=True, env={**os.environ, 'HOME': home, 'USERPROFILE': home})

    def test_tilde_bom_crlf_and_non_ascii(self):
        p = self.run_file('\ufeff## Push\r\n- ş\r\n'.encode('utf-8'))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(wf.json.loads(p.stdout)['stages']['Push']['in'], ['- ş'])
        self.assertTrue(p.stdout.isascii())

    def test_not_utf8(self):
        p = self.run_file('## Push\n- \xe7\n'.encode('latin-1'))
        self.assertEqual(p.returncode, 3)
        self.assertIn('not UTF-8', p.stderr)

    def test_numbered_and_star_lists(self):
        r = wf.parse('## Plan\n1. one\n2) two\n* three\n')
        self.assertEqual(r['stages']['Plan']['in'], ['1. one', '2) two', '* three'])

    def test_heading_inside_fence(self):
        r = wf.parse('## Push\n- run:\n```\n## Deploy\n```\n')
        self.assertEqual(r['unknown'], [])
        self.assertIn('## Deploy', r['stages']['Push']['in'][0])

    def test_tilde_fence_and_mixed_markers(self):
        r = wf.parse('## Push\n~~~\n## Deploy\n```\n## Other\n~~~\n')
        self.assertEqual(r['unknown'], [])

    def test_generics_not_placeholders(self):
        r = wf.parse('## Push\n- return List<String> or Map<K, V>; ask for <ticket id>\n')
        self.assertEqual(r['placeholders'], ['<ticket id>'])

    def test_autolinks_and_html_not_placeholders(self):
        r = wf.parse('## Push\nSee <https://x.y/z> and <br/> <br>; title <KEY> | <SUMMARY>.\n')
        self.assertEqual(r['placeholders'], [])

    def test_review_stage(self):
        self.assertEqual(wf.parse('## Review\n- x\n')['stages']['Review']['in'], ['- x'])


if __name__ == '__main__':
    unittest.main()
