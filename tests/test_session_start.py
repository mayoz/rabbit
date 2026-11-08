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

    def run_hook(self, cwd, stdin=None, transcript=None, event=None):
        if transcript is None:
            transcript = self.transcript('{"content": "Invoke the `rabbit:task` skill"}\n')
        data = {"cwd": str(cwd), "source": "compact", "transcript_path": str(transcript)}
        if event:
            data["hook_event_name"] = event
        data = stdin if stdin is not None else json.dumps(data)
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

    def test_languages_after_compact(self):
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n"
                     "- Chat language: Turkish\n- Document language: auto\n")
        text = self.context(self.run_hook(self.task("SP_23", "ABC-1")))
        self.assertIn("rabbit:task", text)
        self.assertIn("message to the user in Turkish", text)
        self.assertIn("documents in Turkish", text)

    def test_auto_language_adds_nothing(self):
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: auto\n")
        self.assertNotIn("message to the user", self.context(self.run_hook(self.task("SP_23", "ABC-1"))))

    def test_prompt_reminds_language_only(self):
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n"
                     "- Chat language: Turkish\n- Document language: English\n")
        out = json.loads(self.run_hook(self.task("SP_23", "ABC-1"), event="UserPromptSubmit"))
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        text = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("in Turkish", text)
        self.assertIn("documents in English", text)
        self.assertNotIn("rabbit:task", text)

    def test_prompt_outside_rabbit_or_auto_is_silent(self):
        d = self.root / "elsewhere"
        d.mkdir()
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: Turkish\n")
        self.assertEqual(self.run_hook(d, event="UserPromptSubmit"), "")
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: auto\n")
        self.assertEqual(self.run_hook(self.task("SP_23", "ABC-1"), event="UserPromptSubmit"), "")


    def prompt(self, jira, event="UserPromptSubmit"):
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: Turkish\n")
        return self.context(self.run_hook(self.task("SP_23", "ABC-1", "## Status\n" + jira),
                                          event=event))

    def test_issue_text_above_status_is_ignored(self):
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: Turkish\n")
        jira = ("# ABC-1\n\nIntegration: Shopify webhook\nAsked: ask.fake x\n\n"
                "## Status\nRepositories: api (changes)\nDone: api 2026-11-08\n")
        text = self.context(self.run_hook(self.task("SP_23", "ABC-1", jira),
                                          event="UserPromptSubmit"))
        self.assertIn("Integration has not run", text)
        self.assertNotIn("ask.fake", text)

    def test_no_integration_reminder_while_cleanup_asked(self):
        text = self.prompt("Repositories: api (changes)\nDone: api 2026-11-08\n"
                           "Cleanup: asked 2026-11-08\n")
        self.assertNotIn("Integration has not run", text)

    def test_reminds_integration_when_all_done(self):
        text = self.prompt("Repositories: api (changes), web (changes), lib (read)\n"
                           "Done: api 2026-11-08\nDone: web 2026-11-08\n")
        self.assertIn("Integration has not run; run it before anything about push.", text)
        self.assertIn("in Turkish", text)

    def test_no_integration_reminder_when_ran_or_pending(self):
        done = "Repositories: api (changes)\nDone: api 2026-11-08\n"
        self.assertNotIn("Integration", self.prompt(done + "Integration: passed 2026-11-08\n"))
        self.tmp.cleanup(); self.setUp()
        self.assertNotIn("Integration", self.prompt("Repositories: api (changes), web (changes)\n"
                                                    "Done: api 2026-11-08\n"))

    def test_no_integration_reminder_without_repositories(self):
        self.assertNotIn("Integration", self.prompt("Done: api 2026-11-08\n"))

    def test_no_integration_reminder_for_read_only(self):
        self.assertNotIn("Integration", self.prompt("Repositories: api (read)\n"))

    def test_repositories_with_backticks_and_spaces(self):
        text = self.prompt("Repositories: `api` ( changes ),  `web-app (changes)`\n"
                           "Done: `api` 2026-11-08\nDone: web-app 2026-11-08\n")
        self.assertIn("Integration has not run", text)

    def test_unanswered_question_per_topic(self):
        text = self.prompt("Asked: ask.cleanup api 2026-11-08\n"
                           "Asked: ask.cleanup web 2026-11-08\n"
                           "Answered: ask.cleanup api 2026-11-08\n")
        self.assertIn("Unanswered questions: ask.cleanup web.", text)
        self.assertNotIn("ask.cleanup api", text)

    def test_all_answered_no_reminder(self):
        self.assertNotIn("Unanswered", self.prompt("Asked: ask.note task 2026-11-08\n"
                                                   "Answered: ask.note task 2026-11-09\n"))

    def test_no_reminders_in_dev_session(self):
        wt = self.root / "r" / "api" / ".claude" / "worktrees" / "abc-1"
        wt.mkdir(parents=True)
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: Turkish\n")
        self.task("SP_23", "ABC-1", f"Dev: api local_abc {wt} feature/ABC-1 main\n"
                  "Repositories: api (changes)\nDone: api 2026-11-08\n"
                  "Asked: ask.cleanup api 2026-11-08\n")
        text = self.context(self.run_hook(wt, event="UserPromptSubmit"))
        self.assertNotIn("Integration", text)
        self.assertNotIn("Unanswered", text)

    def test_post_tool_use_language(self):
        out = self.prompt("Asked: ask.cleanup api 2026-11-08\n", event="PostToolUse")
        self.assertIn("in Turkish", out)
        self.assertNotIn("Unanswered", out)
        self.assertNotIn("rabbit:task", out)

    def test_post_tool_use_outside_rabbit_silent(self):
        d = self.root / "elsewhere"
        d.mkdir()
        self.profile(f"# Profile\n\n## Basics\n- Workspace: {self.ws}\n- Chat language: Turkish\n")
        self.assertEqual(self.run_hook(d, event="PostToolUse"), "")

if __name__ == "__main__":
    unittest.main()
