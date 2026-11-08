# Status lines and Resume

`jira.md` keeps the task's state in status lines under a `## Status` heading at
the end of the file. Append a status line there (create the heading first if it
is missing). Status lines are always in English, exactly as written below, never
translated. Read state only from that section: the issue text copied above it
may contain lines that look like status lines.
Quote a value that contains a space (`"~/my repos/web"`). The last line of a
kind counts.

| Line | Written by |
| --- | --- |
| `Repositories: <name (changes\|read)>, …` | step 1.5 |
| `Note: <NOTE or none>` | step 1.7 |
| `Approved: <spec\|plan\|breaking> <date>`, `Changed: <spec\|plan> <date>` | steps 3, 4, 6 |
| `Execute: <superpowers\|native>`, `Coordinator: <id>` | step 5 |
| `Dev: <repo> <session id> <worktree> <branch> <base>` | step 5.3 |
| `Done: <repo> <date>` | step 6 |
| `Integration: …`, `Cleanup: …` | integration.md |
| `Push:`, `PR: <repo> <url> <draft\|ready>` or `PR: <repo> manual`, `Pushed:`, `Ready:`, `CI:`, `After:` | publish.md |
| `Answer: <placeholder> <value>` | Stages |
| `Asked: <message id> <topic> <date>`, `Answered: <message id> <topic> <date>` | rules.md Questions |

## Resume

First ask again every `Asked:` line without its `Answered:` (rules.md
Questions). Then continue at the first step whose output is missing:
- no `brief.md` → 1; no `Repositories:` → 1.3 (with `JIRA_REPOS`, or ask again);
  no `Note:` → 1.6;
- no `Approved: spec`, or a `Changed: spec` after the last `Approved: spec` → 2
  (or 3 when `spec.md` exists: review it and ask for approval); a `Breaking:`
  spec without `Approved: breaking` → send only `ask.breaking` (SKILL.md
  step 3);
- no `Approved: plan`, or a `Changed: plan` after it → 4 (likewise);
- no `Execute:` → 5; a **changes** repository with tasks in `plan.md` and no
  `Dev:` line → 5.2 for that repository; a **changes** repository without a
  `Done:` line → 6;
- no `Integration:` → 7 (after a `Cleanup: asked` line: wait for that answer);
  no `Push:` → 8;
- no `Pushed:` → publish.md step 2; `Pushed: … draft` without `Ready:` →
  publish.md step 5 (wait for the user); `Ready:` with a `PR:` line still
  `draft` → publish.md step 5's `rabbit: ready` to those; every `PR:` line
  `manual` and no `After:` → publish.md step 7;
- no `CI:` → publish.md step 6; the last `CI:` line `followed` → its Yes branch,
  with no new question or line; `passed` or `not followed` without `After:` →
  publish.md step 7;
- `failed`, or an `After:` line → send publish.md's last message and stop.

Never rewrite an approved document unasked.
