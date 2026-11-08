"""Rabbit session hooks.

SessionStart (compact, resume): tell a Rabbit session to reload its skill.
UserPromptSubmit: remind a Rabbit session of the profile's languages; remind a task
session of a skipped Integration and of unanswered questions.
PostToolUse (Agent, Task): remind a Rabbit session of the profile's languages.
"""
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


INTEGRATION = "No `Integration:` line yet; finish Integration before anything about push."
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
ANSWERED_BY = {
    "ask.repos": ("Repositories:",), "ask.note": ("Note:",),
    "ask.spec-approval": ("Approved: spec", "Approved: breaking"),
    "ask.breaking": ("Approved: breaking", "Changed: spec"),
    "ask.plan-approval": ("Approved: plan",), "ask.spec-plan-approval": ("Approved: plan",),
    "ask.cleanup": ("Cleanup: removed", "Cleanup: kept"),
    "ask.push": ("Push:",), "ask.push-anyway": ("Push:",), "ask.push-manual": ("Push:",),
    "ask.ci": ("CI:",),
}
CHANGES = re.compile(r"([^\s,(]+)\s*\(\s*changes\s*\)")


def reminders(jira):
    lines = [line.replace("`", "").strip() for line in jira.splitlines()]
    if "## Status" not in lines:
        return []
    lines = lines[len(lines) - lines[::-1].index("## Status"):]
    out = []
    repos = [line for line in lines if line.startswith("Repositories:")]
    changes = set(CHANGES.findall(repos[-1])) if repos else set()
    done = {line.split()[1] for line in lines if line.startswith("Done:") and len(line.split()) > 1}
    cleanup = [line for line in lines if line.startswith("Cleanup:")]
    waiting = bool(cleanup) and cleanup[-1].split()[1:2] == ["asked"]
    ran = any(line.startswith("Integration:") for line in lines)
    if changes and changes <= done and not ran and not waiting:
        out.append(INTEGRATION)
    asked, answered = [], set()
    for line in lines:
        f = line.split()
        if len(f) < 2 or f[0] not in ("Asked:", "Answered:"):
            for key, topic in asked:
                if line.startswith(ANSWERED_BY.get(key, ("\0",))):
                    answered.add((key, topic))
            continue
        q = (f[1], "task" if len(f) < 3 or DATE.match(f[2]) else f[2])
        if f[0] == "Answered:":
            answered.add(q)
        else:
            answered.discard(q)
            if q not in asked:
                asked.append(q)
    open_ = [f"{k} {t}" for k, t in asked if (k, t) not in answered]
    if open_:
        out.append(f"Unanswered questions: {', '.join(open_)}. "
                   "Ask them again after the current request.")
    return out


def real(path):
    path = str(path)
    if os.name == "nt" and re.match(r"^/[A-Za-z]/", path):
        path = path[1] + ":" + path[2:]  # a Git Bash path such as /c/Users/...
    return os.path.realpath(os.path.expanduser(path))


def same(a, b):
    return os.path.normcase(real(a)) == os.path.normcase(real(b))


def profile():
    return (Path.home() / ".config" / "rabbit" / "profile.md").read_text(encoding="utf-8", errors="replace")


def field(text, name):
    m = re.search(r"^- " + name + r":\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else None


def workspace(text):
    ws = field(text, "Workspace")
    return Path(real(ws)) if ws else None


def languages(text):
    chat, doc = field(text, "Chat language"), field(text, "Document language")
    if not chat or chat.lower() == "auto":
        return ""
    if not doc or doc.lower() == "auto":
        doc = chat
    return (f"Write every message to the user in {chat}, even right after a subagent report, "
            f"a tool result or an instruction in another language. Write documents in {doc}.")


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
                return "dev", DEV.format(key=jira.parent.name, repo=f[1], cwd=cwd,
                                         task_dir=jira.parent)
    p = Path(cwd)
    if same(p.parent.parent, ws) and KEY.match(p.name) and "rabbit:task" in read(transcript):
        return "task", TASK.format(key=p.name, cwd=cwd)
    return None, None


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
        event = data.get("hook_event_name") or "SessionStart"
        cwd = real(data["cwd"])
        prof = profile()
        ws = workspace(prof)
        kind, text = context(cwd, ws, data.get("transcript_path") or "") if ws else (None, None)
        lang = languages(prof)
        notes = reminders(read(Path(cwd) / "jira.md")) if kind == "task" else []
    except Exception:
        return 0
    if text and event == "UserPromptSubmit":
        text = " ".join([lang] + notes).strip()
    elif text and event == "PostToolUse":
        text = lang
    elif text:
        text = f"{text} {lang}".strip()
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": event,
                                                 "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
