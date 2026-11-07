"""SessionStart hook: after a compact or resume, tell a Rabbit session to reload its skill."""
import json
import os
import re
import shlex
import sys
from pathlib import Path

KEY = re.compile(r"^[A-Z][A-Z0-9_]+-[0-9]+$")
TASK = ("This is the Rabbit task session for {key} ({cwd}). Invoke the `rabbit:task` skill now "
        "with the Skill tool, with no arguments, and continue with its Resume rule; every rule "
        "applies as written.")
DEV = ("This is the Rabbit dev session for {key} in {repo} ({cwd}), task folder {task_dir}. "
       "Invoke the `rabbit:dev` "
       "skill now with the Skill tool and continue with its Resume rule; every rule applies "
       "as written.")


def real(path):
    path = str(path)
    if os.name == "nt" and re.match(r"^/[A-Za-z]/", path):
        path = path[1] + ":" + path[2:]  # a Git Bash path such as /c/Users/...
    return os.path.realpath(os.path.expanduser(path))


def same(a, b):
    return os.path.normcase(real(a)) == os.path.normcase(real(b))


def workspace():
    text = (Path.home() / ".config" / "rabbit" / "profile.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^- Workspace:\s*(.+?)\s*$", text, re.M)
    return Path(real(m.group(1))) if m else None


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def context(cwd, ws, transcript):
    jiras = sorted(ws.glob("*/*/jira.md"), key=lambda j: j.stat().st_mtime, reverse=True)
    for jira in jiras:
        for line in read(jira).splitlines():
            try:
                f = (shlex.split(line.replace("`", "").replace("\\", "/"))
                     if line.startswith("Dev:") else [])
            except ValueError:
                continue
            if len(f) >= 4 and same(f[3], cwd):
                return DEV.format(key=jira.parent.name, repo=f[1], cwd=cwd, task_dir=jira.parent)
    p = Path(cwd)
    if same(p.parent.parent, ws) and KEY.match(p.name) and "rabbit:task" in read(transcript):
        return TASK.format(key=p.name, cwd=cwd)
    return None


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
        cwd = real(data["cwd"])
        ws = workspace()
        text = context(cwd, ws, data.get("transcript_path") or "") if ws else None
    except Exception:
        return 0
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                 "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
