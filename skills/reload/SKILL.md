---
name: reload
description: Read the workflow file again in a running Rabbit task or dev session, so later steps follow its current instructions. Reports read errors and what changed, and runs no other step. Use when the user says reload, reload the workflow, or read the workflow again.
---

# Reload

Reads the workflow file again and replaces this session's `WF`. Nothing else
happens: no stage starts, moves on or runs again, no tracker write, no message
to another session, no question, no repository change.

1. **Profile.** Read `~/.config/rabbit/profile.md`. Missing or unreadable: send
   `setup.needed` with `{{missing}}` = the profile, and stop. Use only its Chat
   language (`LANG`, as the session already uses it), `Workspace` and
   `Workflow:` lines; other values keep what this session already uses.
2. **Session.** A dev session has a `Dev:` line whose worktree is this folder
   in `<Workspace>/*/*/jira.md`. A task session's folder is
   `<Workspace>/<sprint>/<KEY>` (its name a task key). Neither: this is no
   Rabbit session.
3. **Read.** No `Workflow:` line: `WF` is empty, `{{changes}}` = "no workflow
   file in the profile"; go to step 5. Otherwise run `PY -I
   "${CLAUDE_PLUGIN_ROOT}/skills/task/scripts/workflow.py" <path>` (`PY`:
   `${CLAUDE_PLUGIN_ROOT}/skills/task/references/rules.md`).
   - Exit 3: send `error.workflow-missing` and stop. The old `WF` is not used
     again: the session waits for a fixed file and another `/rabbit:reload`.
   - Its JSON is the new `WF`. `WF.unknown` not empty: send
     `note.unknown-heading`.
4. **Changes.** Compare with the `WF` this session read before: the stages
   whose instructions were added, removed or changed, by heading
   (`Environment`, `Push:After`). Nothing changed: "no changes". No earlier
   `WF` in this session (after a compaction): "loaded" and the stage
   headings. In a dev session only `Environment`, `Execute` and `Push` (in)
   count.
5. **Report.** Send `done.reload`. `{{placeholders}}`: the ones in
   `WF.placeholders` that have no `Answer:` line in `jira.md`; empty when none.
   No Rabbit session: leave out "The next step follows it." and say there is
   no `WF` to use here.

From the next step on, apply the new `WF` exactly as the session's own skill
says: a task session takes every stage, a dev session `Environment`,
`Execute` (before, in, after) and `Push.in`. A question still waiting
(`Asked:`) stays open as it is.

Messages come from `${CLAUDE_PLUGIN_ROOT}/skills/task/references/messages.md`
by id, sent in `LANG`.
