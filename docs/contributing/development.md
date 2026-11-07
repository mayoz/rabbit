# Developing Rabbit

## Run your copy

Terminal, for setup and skill triggering:

```bash
claude --plugin-dir <your clone>
```

The copy shadows an installed `rabbit` for that session; `/reload-plugins` picks
up edits.

Claude Desktop, for `pull`, `task` and `dev` end to end: add your checkout as a
local marketplace. Files are read in place, so edits show up in the next new
session.

```bash
claude plugin marketplace add <your clone>
```

```bash
claude plugin install rabbit@mayoz
```

Your checkout's marketplace has the same name, `mayoz`, as the published one. If
you added the published one, remove it first (`claude plugin marketplace remove
mayoz`; this also uninstalls `rabbit`) and add it back from GitHub when you are
done.

## Checks

```bash
scripts/check.sh
```

It runs the CI checks (unit tests, the check script tests, `claude plugin
validate . --strict`, skill size, line width, the leak scan and `shellcheck`)
and prints `passed`, `failed` or `skipped` for each, with the output of a failed
one. It exits with an error when any check fails. A check whose tool is not
installed (`claude`, `shellcheck`) is skipped; CI still runs it.

`scripts/leak-scan.sh` also reads a private pattern list from
`~/.config/rabbit/denylist` (one extended regex per line) so names you must not
publish never enter the repository. Turn it on as a pre-push hook with `git
config core.hooksPath scripts/hooks`.

## Evals

Evals run **only on your machine, never in CI**. They use your normal Claude
Code login and count against your plan's usage; no API key is needed.

```bash
claude plugin eval . --trust-plugin --no-publish --ablation none --tag setup --allow-tools Write
```

- `--ablation none` skips the no-plugin comparison run and halves the cost.
- Run only the cases of the skill you changed: `--tag
  setup|pull|task|observer|dev` or `--case <name>`.
- Prefer free graders (`regex`, `tool_used`, `tool_order`, `file_exists`); use
  `llm` only for language and wording.
- Each case runs in a temporary home without Claude Desktop tools or your
  profile, so evals cover triggering, setup and the stop paths. Desktop flows
  are tested by hand.
- Cases with a `fixture.sh` (the `observer` cases) need `--scaffold`.
- The `dev` cases need `--allow-tools Write,Bash` and a working sandbox; if your
  machine's managed settings exempt commands from the sandbox, evals refuse the
  `Bash` grant.

## Layout

| Path | What it is |
| --- | --- |
| `skills/<name>/SKILL.md` | A command's instructions. Detail lives in `references/`. |
| `skills/task/scripts/` | `workflow.py` parses a workflow file; `find_repo.py` finds a repository by name. |
| `agents/observer.md` | The blind reviewer. |
| `hooks/` | `session_start.py` reloads a skill after a compaction and reminds a Rabbit session of the profile's languages on each prompt; `observer_guard.py` keeps the observer read-only. |
| `tests/` | Unit tests for the scripts and hooks, and shell tests for the checks. |
| `evals/` | Local eval cases, one folder each. |

Helper scripts and hooks are Python 3 with the standard library only, so they
run the same on macOS, Linux and Windows. Avoid shell-only tools in skill text
(`nc`, `sed -i`); CI runs the unit tests on all three systems.

In skill text, `${CLAUDE_SKILL_DIR}` points at the skill's own folder and
`${CLAUDE_PLUGIN_ROOT}` at the plugin's root. Use the first for a skill's own
files and the second for files another skill owns. Claude Code fills both in
when it loads the skill.

## Skill size

`task/SKILL.md` stays at or under 1850 words, the others at or under 1000
(`wc -w`). Detail goes into `references/` and is read only in the step that
needs it.

## Line width

Markdown lines are at most 80 characters. Frontmatter, code blocks, tables,
headings, HTML lines and a line holding a single word (a long URL) are exempt.
`scripts/check-line-width.py` checks every tracked `.md` file.
