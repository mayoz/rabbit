import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "hooks" / "observer_guard.py"


HOME = tempfile.mkdtemp()
(Path(HOME) / ".config" / "rabbit").mkdir(parents=True)
(Path(HOME) / ".config" / "rabbit" / "profile.md").write_text(
    "## Tracker\n- Site: x\n- Tools: Acme (jira, getJiraIssue)\n", encoding="utf-8")


def run(data):
    p = subprocess.run([sys.executable, "-I", str(SCRIPT)], input=json.dumps(data),
                       capture_output=True, text=True, env={**os.environ, "HOME": HOME, "USERPROFILE": HOME})
    assert p.returncode == 0, p.stderr
    return p.stdout


def bash(command, agent="rabbit:observer"):
    return run({"agent_type": agent, "tool_name": "Bash", "tool_input": {"command": command}})


class ObserverGuardTest(unittest.TestCase):
    def denied(self, out):
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"

    def test_reads_pass(self):
        for c in ["git -C /r show origin/main:app/x.php",
                  "git -C /r grep -n 'a->b' origin/main -- app",
                  "git log --oneline -5 && git diff main...feat",
                  "ls -la /r | head -20",
                  "head -40 /r/x.md",
                  "cat x 2>/dev/null || echo none",
                  "git diff a...b 2>&1 | wc -l",
                  "find . -name '*.php' -type f -o -name '*.js'",
                  "cd /r && git status", "git --version",
                  "grep -rn \"x > 1\" src", "grep -n 'end$' x",
                  "git log --oneline --format=%h -3", "git diff --text a b"]:
            self.assertEqual(bash(c), "", c)

    def test_writes_denied(self):
        for c in ["rm -rf /r", "git commit -m x", "git push", "git checkout -b x",
                  "git branch x", "echo x > file", "cat a >> b", "sed -i 's/a/b/' x",
                  "find . -delete", "find . -exec rm {} ;", "sort -o out in",
                  "ls; rm x", "ls\nrm x", "ls && touch x", "echo $(rm x)", "echo `rm x`",
                  "git diff --output=x", "python3 -c 'print(1)'", "curl -X POST http://x",
                  "(rm x)", "git -c core.pager=rm log", "git",
                  "X=1 rm x", "GIT_PAGER=rm git log", "/tmp/evil/ls", "./ls",
                  "sed -n 1p x", "sort -S1 x", "uniq a b", "rg --pre=sh x", "tree -R -H x",
                  "date -s 1", "git grep -Orm x", "git grep --open-files-in-pager=rm x",
                  "git -p log", "git --exec-path=/tmp log", "git cat-file --filters x",
                  "find . -$'delete'", "find . -{delete,name}", "find . -fprint x",
                  "echo a#;touch x", "cat x#; rm -rf y", "echo 'a'#;rm x",
                  "git grep --open=x -e a", "git grep -nO x a", "git log --outp=x",
                  "git symbolic-ref HEAD refs/heads/x", "git symbolic-ref -d HEAD",
                  "echo \"${(e):-${:-\\$}(touch x)}\"", "echo $HOME", "echo \"$(rm x)\"",
                  "git grep -3Orm x", "git grep -1O'sh -c id' x"]:
            self.assertTrue(self.denied(bash(c)), c)

    def test_other_agents_untouched(self):
        self.assertEqual(bash("rm -rf /r", agent="general-purpose"), "")
        self.assertEqual(run({"tool_name": "Bash", "tool_input": {"command": "rm x"}}), "")
        self.assertEqual(bash("rm -rf /r", agent="observer"), "")

    def test_utf8_input_is_checked(self):
        data = {"agent_type": "rabbit:observer", "tool_name": "Bash",
                "tool_input": {"command": "rm -rf x # \U0001f601 \u0101"}}
        p = subprocess.run([sys.executable, "-I", str(SCRIPT)],
                           input=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                           capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1252"})
        self.assertTrue(self.denied(p.stdout.decode()))

    def test_mcp_writes_denied(self):
        w = run({"agent_type": "rabbit:observer", "tool_name":
                 "mcp__atlassian__addCommentToJiraIssue", "tool_input": {}})
        self.assertTrue(self.denied(w))
        r = run({"agent_type": "rabbit:observer", "tool_name":
                 "mcp__atlassian__getJiraIssue", "tool_input": {}})
        self.assertEqual(r, "")
        for name in ["mcp__acme__jira", "mcp__atlassian__searchJiraIssuesUsingJql",
                     "mcp__x__list_pods", "mcp__x__getAsset", "mcp__x__list_datasets"]:
            self.assertEqual(run({"agent_type": "rabbit:observer", "tool_name": name,
                                  "tool_input": {}}), "", name)
        for name in ["mcp__acme__jira_write", "mcp__atlassian__transitionJiraIssue",
                     "mcp__terminal__run_in_terminal", "mcp__ccd_session__start_session",
                     "mcp__kube__exec_pod_command", "mcp__host__clean_up_worktrees",
                     "mcp__chrome__javascript_tool", "mcp__dd__execute_code",
                     "mcp__x__find_and_delete", "mcp__x__get_or_create_x", "mcp__mail__reply",
                     "mcp__env__kill_environment", "mcp__ccd_pr__bind_pr",
                     "mcp__pg__query", "mcp__web__fetch", "mcp__x__find_and_replace",
                     "mcp__x__read_and_save", "mcp__x__get_and_lock_issue"]:
            self.assertTrue(self.denied(run({"agent_type": "rabbit:observer",
                                             "tool_name": name, "tool_input": {}})), name)

    def test_only_reading_tools(self):
        for tool in ["Read", "Grep", "Glob", "ToolSearch", "SubagentHandback"]:
            self.assertEqual(run({"agent_type": "rabbit:observer", "tool_name": tool,
                                  "tool_input": {}}), "", tool)
        for tool in ["PowerShell", "Monitor", "EnterWorktree", "SendMessage", "CronCreate",
                     "WebFetch", "Skill"]:
            self.assertTrue(self.denied(run({"agent_type": "rabbit:observer",
                                             "tool_name": tool, "tool_input": {}})), tool)

    def test_check_error_denies(self):
        out = run({"agent_type": "rabbit:observer", "tool_name": "Bash", "tool_input": "x"})
        self.assertTrue(self.denied(out))

    def test_bad_input_passes(self):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT)], input="not json",
                           capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
