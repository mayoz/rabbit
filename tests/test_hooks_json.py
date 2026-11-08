import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
GUARD = HOOKS["PreToolUse"][0]["hooks"][0]["command"]
BASH = shutil.which("bash")


def run(data, path=None):
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}
    if path is not None:
        env["PATH"] = path
    p = subprocess.run([BASH, "-c", GUARD], input=json.dumps(data, separators=(",", ":")),
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout


def denied(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


@unittest.skipIf(BASH is None or os.name == "nt", "needs a POSIX bash")
class HooksJsonTest(unittest.TestCase):
    def test_observer_write_denied(self):
        code, out = run({"agent_type": "rabbit:observer", "tool_name": "Bash",
                         "tool_input": {"command": "touch x"}})
        self.assertEqual(code, 0)
        self.assertTrue(denied(out))

    def test_others_pass(self):
        for data in [{"agent_type": "rabbit:observer", "tool_name": "Read"},
                     {"tool_name": "Bash", "tool_input": {"command": "rm x rabbit:observer"}},
                     {"agent_type": "observer", "tool_name": "Bash"}]:
            self.assertEqual(run(data), (0, ""), data)

    def test_no_python(self):
        empty = tempfile.mkdtemp()
        tools = Path(empty, "cat")
        tools.symlink_to(shutil.which("cat"))
        code, out = run({"agent_type": "rabbit:observer", "tool_name": "Read"}, empty)
        self.assertEqual(code, 0)
        self.assertTrue(denied(out))
        self.assertEqual(run({"tool_name": "Bash", "tool_input": {"command": "x"}}, empty),
                         (0, ""))

    def test_post_tool_use_language_hook(self):
        entry = HOOKS["PostToolUse"][0]
        self.assertEqual(entry["matcher"], "Agent|Task")
        self.assertEqual(entry["hooks"][0]["command"],
                         HOOKS["UserPromptSubmit"][0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
