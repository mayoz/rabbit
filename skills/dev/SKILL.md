---
name: dev
description: Implement an approved Rabbit plan in one repository. Runs as the first turn of a dev session opened by /rabbit:task; implements the plan steps with superpowers or Rabbit's own loop, one commit per step, reviews its own diff, and pushes only when the task session says so.
---

# Dev

This session implements one repository's part of an approved plan. Its prompt
names `KEY`, `REPO`, `WORKTREE`, `BRANCH`, `BASE`, `TASK_DIR` and `COORDINATOR`;
if any is missing, apply Resume, and if it finds no `Dev:` line, send
`error.no-context` and stop.

## 0. Before anything

1. **Profile.** Read `~/.config/rabbit/profile.md`. If it is missing or
   unreadable, or a required value is empty (Basics: Workspace, Repositories
   folder, Chat language, Document language), send `setup.needed` naming what is
   missing, run the `rabbit:setup` skill with the Skill tool, and when it
   finishes continue here.
2. **Language.** `LANG` = Chat language, or for `auto` the language of the
   user's last message (English if none). Every message stays in `LANG`, even
   after text in another language. Send fixed messages from
   `references/messages.md` by id, translated; keep Markdown, `{{...}}` values,
   paths, keys and commands as they are. Code,
   comments, commits and pull request text are in English unless the repository
   says otherwise.
3. **Workflow.** If the profile has a `Workflow:` line, run
   `PY -I "${CLAUDE_PLUGIN_ROOT}/skills/task/scripts/workflow.py" <path>` (`PY`:
   rules.md); its JSON is `WF`; exit 3: send `error.workflow-missing` and stop.
   Apply `WF.stages.Execute` (before, in, after) and `WF.stages.Push.in`; the
   task session applies the rest (every instruction, in order; fill `<KEY>`,
   `<SUMMARY>`, `<REPO>`, `<BRANCH>`, `<BASE>`, `<TASK_DIR>` yourself; a
   placeholder the prompt's answers do not cover gets
   `ask.placeholder`, and send its answer to `COORDINATOR` as `rabbit:
   placeholder <name>
   <value>`; an instruction you cannot apply, `ask.instruction-failed`).
4. **Rules.** Read `${CLAUDE_PLUGIN_ROOT}/skills/task/references/rules.md` and
   apply it. Read the repository's `CLAUDE.md` and `.claude/rules/`; they win
   where they disagree.
5. **Questions reach the coordinator.** The user usually watches the task
   session. Every question or stop this session sends the user (`step.blocked`,
   `ask.*`) also goes to `COORDINATOR` as `rabbit: blocked <the question>`; take
   the answer from either session.
   One the user answers here: `SendMessage` `rabbit: answered <the question>`.

## Resume

After a compaction or restart, or with any of `KEY`, `REPO`, `TASK_DIR`,
worktree, `BRANCH`, `BASE` or `COORDINATOR` missing: find the `Dev:` line whose
worktree is this folder in `<Workspace>/*/*/jira.md` (several: the most recently
changed file); that file's folder is `TASK_DIR` and its name `KEY`; the line
gives `REPO`, worktree, `BRANCH` and `BASE`, its `Coordinator:` line
`COORDINATOR`. Match the subjects of `git log --format=%s
origin/<BASE>..HEAD` (local `<BASE>` without a remote) to the plan steps' commit
messages and continue at the first step without its commit. Uncommitted work
before a `Done: <REPO>` line belongs to that step: finish it. Every step
committed and no `Done: <REPO>` line: go to §4.
A `Done: <REPO>` line: implement nothing; uncommitted work belongs to the last
fix: finish it, commit and send `rabbit: done <new commits>`; else wait for the
coordinator. A pull request opened earlier: `gh pr view <BRANCH> --json
url,state,isDraft`.

## 1. Read the plan

Read `TASK_DIR/spec.md` (the `REPO` section and every contract it is part of),
`TASK_DIR/plan.md` and the `Execute:` line in `TASK_DIR/jira.md`. Implement only
the `REPO` tasks. Do not edit `spec.md` or `plan.md`. No `Execute:` line: send
`ask.execute` and wait.
Code facts come from `WORKTREE` at `HEAD`, not from the base branch.

Run only the tests of the files you change and of their callers, by path; never
a whole suite unless the plan says so. Before the first one, apply
rules.md's **Running the app or its tests**.

Send `start.summary` listing the plan tasks you will implement, and start at
once: the plan approval was the go-ahead.

## 2. Implement (stage Execute)

Apply `WF.stages.Execute.before`, then implement with `WF.stages.Execute.in` on
top:
- **superpowers:** invoke `superpowers:executing-plans` with args: `Plan:
  <TASK_DIR>/plan.md.
  Implement only the <REPO> tasks, one commit per plan step, staged by path;
  never skip hooks or signing. You are already in the task's worktree
  <WORKTREE>: create no other worktree or workspace. Do not push, do not open a
  pull request and do not finish the branch.`
- **native:** for each plan step, in order:
  1. Write the test the step names; run it; it must fail for the reason the step
     says. A step with no test (configuration, documentation): say so in
     `step.done`.
  2. Make the change; run the test again; it must pass. Run the other tests the
     change could break.
  3. Commit only the files of this step, staged by path (never `git add .` or
     `-A`), with the step's commit message. Never skip hooks or signing; a hook
     that rewrites files:
     stage those same paths again and commit again.
  4. Send `step.done` in one line; then the next step.

A test that will not pass, or a step that cannot be done as written: stop and
send `step.blocked` with what you ran and what happened. The user may say to go
on without it:
then name it under `Unverified:` in the `rabbit: done` report. Then apply
`WF.stages.Execute.after`.

## 3. When the plan is wrong

If the code shows that the spec or a contract is wrong or incomplete, stop. Tell
the user and `SendMessage` to `COORDINATOR`: `rabbit: plan wrong <path:line>
<finding>`. Do not change a contract on your own; wait for `rabbit: plan
changed`.

## 4. Review your own diff

Run `${CLAUDE_PLUGIN_ROOT}/skills/task/references/review.md` with `Kind: diff`
for `REPO` (base `BASE`, branch `BRANCH`), with its Findings rules; write no
review file. Fix each finding to fix with its test and a commit of its own.

## 5. Report and wait

Send `done` with the commit list (`git log --oneline origin/<BASE>..HEAD`, local
`<BASE>` without a remote) and the tests you ran, then `SendMessage` to
`COORDINATOR`: `rabbit: done
<the commit list>`, followed by the proven findings as `### R<n>` blocks with
their `**Status:**`, the summary line, any `Follow-ups:`, `Unverified:` and
`Env:` lines. Wait.

## 6. Messages from the coordinator

Follow `references/commands.md`. Never push, open a pull request or rewrite
history otherwise. If the user asks for a push here, send `push.via-task`.
