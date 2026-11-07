# brief.md

Write `brief.md` from scratch (Write tool) before any question, so the user can
steer from it.
At most about 40 lines, no line over 80 characters (count characters, not
bytes). Exactly these sections, headings translated into `DOC_LANG`, each at
most 2–3 short paragraphs or bullets:

- `## What happened`: the situation; for a bug, its cause.
- `## What is asked`
- `## What is expected`: the gist of the acceptance criteria.
- `## Where to start`: the code places the change starts from, as
  `repo/path:line` verified on the base branch. Before any repository is known,
  skip it; it is added once they are confirmed. If several places fit,
  list them and say what settles it.
- `## Repositories`: only when the issue has a `Repo:` line; the names it lists.
- `## Open points`: only when there are any; always every issue that blocks this
  one, with its status, and each attachment that matters but cannot be read (it
  is asked in `ask.note`).

Sources: the issue (description, every comment, every custom field that has a
value, remote links), and any error or metrics link in it, checked with the
tools the workflow's `## Brief` names, or with the session's own tools. Every
claim carries its source. If the issue gives too little to explain the task,
write one line saying so (in `DOC_LANG`) instead of guessing.

Put the chosen heading translations in `jira.md` as its first line, `Headings:
…` (rewrite the file with the Write tool, everything else unchanged); later
steps reuse them.
