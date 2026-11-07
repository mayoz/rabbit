import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "hooks" / "session_start.py"


class SessionStartTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(os.path.realpath(self.tmp.name))
        self.home = self.root / "home"
        self.ws = self.root / "ws"
        (self.home / ".config" / "rabbit").mkdir(parents=True)
        self.ws.mkdir()
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n")

    def tearDown(self):
        self.tmp.cleanup()

    def profile(self, text):
        (self.home / ".config" / "rabbit" / "profile.md").write_text(text)

    def task(self, sprint, key, jira=None):
        d = self.ws / sprint / key
        d.mkdir(parents=True)
        if jira is not None:
            (d / "jira.md").write_text(jira)
        return d

    def transcript(self, text):
        t = self.root / "transcript.jsonl"
        t.write_text(text)
        return t

    def run_hook(self, cwd, stdin=None, transcript=None):
        if transcript is None:
            transcript = self.transcript('{"content": "Invoke the `rabbit:task` skill"}\n')
        data = stdin if stdin is not None else json.dumps(
            {"cwd": str(cwd), "source": "compact", "transcript_path": str(transcript)})
        env = {"HOME": str(self.home), "USERPROFILE": str(self.home),
               "PATH": os.environ.get("PATH", "")}
        if "SYSTEMROOT" in os.environ:
            env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        p = subprocess.run([sys.executable, "-I", str(SCRIPT)], input=data,
                           capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def context(self, out):
        return json.loads(out)["hookSpecificOutput"]["additionalContext"]

    def test_task_dir_with_jira(self):
        d = self.task("SP_23", "ABC-1", "Repositories: api (changes)\n")
        text = self.context(self.run_hook(d))
        self.assertIn("rabbit:task", text)
        self.assertIn("ABC-1", text)

    def test_task_dir_without_jira(self):
        d = self.task("SP_23", "ABC-1")
        self.assertIn("rabbit:task", self.context(self.run_hook(d)))

    def test_dev_worktree(self):
        wt = self.root / "r" / "api" / ".claude" / "worktrees" / "abc-1"
        wt.mkdir(parents=True)
        self.task("SP_23", "ABC-1", f"Dev: api local_abc {wt} feature/ABC-1 main\n")
        text = self.context(self.run_hook(wt))
        self.assertIn("rabbit:dev", text)
        self.assertIn("api", text)
        self.assertIn("ABC-1", text)
        self.assertNotIn("rabbit:task", text)

    def test_same_key_two_sprints(self):
        old = self.root / "r" / "api" / "old"
        new = self.root / "r" / "web" / "new"
        old.mkdir(parents=True)
        new.mkdir(parents=True)
        self.task("SP_22", "ABC-1", f"Dev: api local_a {old} feature/ABC-1 main\n")
        self.task("SP_23", "ABC-1", f"Dev: web local_b {new} feature/ABC-1 main\n")
        self.assertIn("in api", self.context(self.run_hook(old)))
        self.assertIn("in web", self.context(self.run_hook(new)))

    def test_task_dir_of_another_tool(self):
        d = self.task("SP_23", "ABC-1", "Repositories: api (changes)\n")
        other = self.transcript('{"content": "Invoke the other-skill skill"}\n')
        self.assertEqual(self.run_hook(d, transcript=other), "")

    def test_task_text_has_no_argument(self):
        text = self.context(self.run_hook(self.task("SP_23", "ABC-1")))
        self.assertNotIn("argument `", text)

    def test_same_worktree_two_sprints_takes_newest(self):
        wt = self.root / "r" / "api" / ".claude" / "worktrees" / "abc-1"
        wt.mkdir(parents=True)
        new = self.task("SP_23", "ABC-1", f"Dev: api local_b {wt} feature/ABC-1 main\n")
        old = self.task("SP_9", "ABC-1", f"Dev: api local_a {wt} feature/ABC-1 main\n")
        os.utime(old / "jira.md", (1, 1))
        self.assertIn(str(new), self.context(self.run_hook(wt)))

    def test_unreadable_jira_is_skipped(self):
        bad = self.task("SP_21", "X-1", "Dev: api local_x /nowhere b main\n")
        (bad / "jira.md").chmod(0)
        try:
            self.assertIn("rabbit:task", self.context(self.run_hook(self.task("SP_23", "ABC-1"))))
        finally:
            (bad / "jira.md").chmod(0o644)

    def test_tasks_folder_on_resume(self):
        d = self.task("tasks", "ABC-1")
        t = self.transcript('{"content": "Invoke the `rabbit:task` skill"}\n')
        data = json.dumps({"cwd": str(d), "source": "resume", "transcript_path": str(t)})
        self.assertIn("rabbit:task", self.context(self.run_hook(d, stdin=data)))

    def test_quoted_worktree_with_space(self):
        wt = self.root / "my repos" / "api"
        wt.mkdir(parents=True)
        self.task("SP_23", "ABC-1", f'Dev: api local_abc "{wt}" feature/ABC-1 main\n')
        self.assertIn("rabbit:dev", self.context(self.run_hook(wt)))

    def test_unrelated_dir(self):
        d = self.root / "elsewhere"
        d.mkdir()
        self.assertEqual(self.run_hook(d), "")

    def test_key_shape(self):
        d = self.ws / "SP_23" / "notes"
        d.mkdir(parents=True)
        self.assertEqual(self.run_hook(d), "")

    def test_no_profile(self):
        (self.home / ".config" / "rabbit" / "profile.md").unlink()
        self.assertEqual(self.run_hook(self.task("SP_23", "ABC-1")), "")

    def test_broken_profile(self):
        self.profile("# Profile\n\nnothing here\n")
        self.assertEqual(self.run_hook(self.task("SP_23", "ABC-1")), "")

    def test_bad_stdin(self):
        self.task("SP_23", "ABC-1")
        self.assertEqual(self.run_hook(None, stdin="not json"), "")

    def test_output_json(self):
        out = json.loads(self.run_hook(self.task("SP_23", "ABC-1")))
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")


if __name__ == "__main__":
    unittest.main()
