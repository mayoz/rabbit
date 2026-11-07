"""PreToolUse hook: keep the rabbit:observer agent read-only.

Other agents and sessions pass through untouched. The observer may use only the reading tools,
a Bash command whose every part is a known read-only command, and an MCP tool whose name starts
with a read word and has no write word, or that the profile's Tools line names. Anything
else, and any error while checking, is denied.
"""
import json
import re
import shlex
import sys
from pathlib import Path

OBSERVER = {"rabbit:observer"}
READ_TOOLS = {"Read", "Grep", "Glob", "LS", "ToolSearch", "TodoWrite", "SubagentHandback",
              "StructuredOutput"}
GIT_READ = {"show", "grep", "log", "diff", "ls-files", "ls-tree", "rev-parse", "blame",
            "cat-file", "status", "merge-base", "for-each-ref", "shortlog",
            "describe", "show-ref", "rev-list", "name-rev"}
READ = {"ls", "cat", "head", "tail", "wc", "grep", "find", "cut", "tr", "jq", "pwd", "echo",
        "printf", "stat", "basename", "dirname", "realpath", "cd", "diff", "cmp", "test",
        "true", "which", "type", "nl", "column"}
GIT_OPTS_WITH_VALUE = {"-C", "--git-dir", "--work-tree"}
GIT_BAD_GLOBAL = {"-c", "-p"}
# git accepts unique abbreviations of long options, so --open=x means --open-files-in-pager=x.
GIT_BAD_LONG = ("--output", "--ext-diff", "--textconv", "--filters", "--open-files-in-pager",
                "--exec-path", "--config", "--config-env", "--paginate")
GIT_SAFE_LONG = {"--text", "--filter"}
FIND_BAD = re.compile(r"^(-delete|-exec\S*|-ok\S*|-fprint\S*|-fls)$")
MCP_READ = {"get", "list", "search", "read", "find", "lookup", "describe", "view"}
MCP_WRITE = {"create", "edit", "update", "delete", "transition", "add", "write", "post", "send",
             "upload", "remove", "assign", "merge", "publish", "move", "set", "put", "patch",
             "close", "approve", "start", "stop", "run", "exec", "execute", "kill", "trigger",
             "schedule", "cancel", "archive", "scale", "invoke", "apply", "deploy", "restart",
             "reply", "forward", "share", "trash", "upsert", "restore", "submit", "reset",
             "purge", "insert", "drop", "grant", "revoke", "install", "enable", "disable",
             "replace", "save", "rename", "copy", "import", "export", "link", "lock", "unlock",
             "sync", "clear", "mark", "comment", "attach", "bind", "clean", "or", "and", "then"}
PROFILE = Path.home() / ".config" / "rabbit" / "profile.md"
SEPARATORS = {"&&", "||", ";", "|", "&", ";;", "|&"}
# Brace lists such as -{delete,x}, which shlex cannot see.
BRACES = re.compile(r"\{[^}]*(,|\.\.)[^}]*\}")


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "rabbit:observer is read-only: " + reason}}))
    return 0


def words(name):
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[0-9]+", name)]


def git_arg_bad(arg):
    # -O<cmd> (git grep --open-files-in-pager) may sit anywhere in a short-option cluster.
    if re.match(r"^-[^-]", arg) and "O" in arg.split("=")[0]:
        return True
    name = arg.split("=")[0]
    if not name.startswith("--") or len(name) < 3 or name in GIT_SAFE_LONG:
        return False
    return any(opt.startswith(name) for opt in GIT_BAD_LONG)


def dollar_outside_single_quotes(command):
    single = double = escaped = False
    for ch in command:
        if escaped:
            escaped = False
        elif ch == "\\" and not single:
            escaped = True
        elif ch == "'" and not double:
            single = not single
        elif ch == '"' and not single:
            double = not double
        elif ch == "$" and not single:
            return True
    return False


def segment_ok(words):
    if not words:
        return True
    cmd, args = words[0], words[1:]
    if "/" in cmd or "=" in cmd:
        return False
    if cmd == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            if args[i] in GIT_BAD_GLOBAL or git_arg_bad(args[i]):
                return False
            i += 2 if args[i] in GIT_OPTS_WITH_VALUE else 1
        if i >= len(args):
            return args in (["--version"], ["--help"])
        return args[i] in GIT_READ and not any(git_arg_bad(a) for a in args[i + 1:])
    if cmd not in READ:
        return False
    return not (cmd == "find" and any(FIND_BAD.match(a) for a in args))


def command_ok(command):
    if BRACES.search(command) or dollar_outside_single_quotes(command):
        return False
    lexer = shlex.shlex(command.replace("\n", ";"), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        return False
    words, i = [], 0
    while i < len(tokens):
        t = tokens[i]
        if t in SEPARATORS:
            if not segment_ok(words):
                return False
            words = []
        elif t in (">", ">>", ">|", "&>", "&>>"):
            if i + 1 >= len(tokens) or tokens[i + 1] != "/dev/null":
                return False
            i += 1
        elif t == ">&":
            if i + 1 >= len(tokens) or not tokens[i + 1].isdigit():
                return False
            if words and words[-1].isdigit():
                words.pop()
            i += 1
        elif t in ("<", "<<", "<<<"):
            i += 1
        elif set(t) <= set("();<>|&") or "`" in t or "$(" in t:
            return False
        else:
            words.append(t)
        i += 1
    return segment_ok(words)


def profile_tools():
    try:
        text = PROFILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    m = re.search(r"^- Tools:.*?\((.*)\)\s*$", text, re.M)
    return {t.strip() for t in m.group(1).split(",")} if m else set()


def check(data):
    tool = data.get("tool_name") or ""
    if tool in READ_TOOLS:
        return 0
    if tool == "Bash":
        if command_ok((data.get("tool_input") or {}).get("command") or ""):
            return 0
        return deny("only read-only commands such as git show, git grep, git log, "
                    "git diff, ls and cat may run.")
    if tool.startswith("mcp__"):
        name = tool.rsplit("__", 1)[-1]
        w = words(name)
        if (w and w[0] in MCP_READ and not MCP_WRITE & set(w)) or name in profile_tools():
            return 0
        return deny(f"{tool} does not read like a read.")
    return deny(f"{tool} is not a reading tool.")


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    except Exception:
        return 0
    if not isinstance(data, dict) or data.get("agent_type") not in OBSERVER:
        return 0
    try:
        return check(data)
    except Exception:
        return deny("the check failed, so the tool is blocked.")


if __name__ == "__main__":
    sys.exit(main())
