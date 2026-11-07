---
name: task
description: Drive one Jira task from a verified brief through spec, plan, per-repository dev sessions, an integration check and the push. Runs as the first turn of a task session opened by /rabbit:pull, or on its own with a Jira key or URL. Use when the user asks to work on, start or resume a Jira task (for example "work on ABC-123").
argument-hint: "[KEY | URL]"
---

# Task

This session is the task's **coordinator**: it owns `brief.md`, `jira.md`,
`spec.md`, `plan.md`, `impact.md` and `integration.md` in the task folder and
never edits repository code. Read `references/rules.md` now and apply it in
every step. Read other references only in the step that names them.

## 0. Before anything

1. **Desktop.** If no `mcp__ccd_session__start_session` tool exists (loaded or
   deferred), send `error.desktop-only` (in the user's language) and stop.
2. **Profile.** Read `~/.config/rabbit/profile.md`. If it is missing or
   unreadable, or a required value is empty (Basics: Workspace, Repositories
   folder, Chat language, Document language; Tracker: Site, Tools), send
   `setup.needed` naming what is missing, run the `rabbit:setup` skill with the
   Skill tool, and when it finishes continue here.
3. **Language.** `LANG` = Chat language, or for `auto` the language of the last
   message the user typed (not a prompt Rabbit generated; English if none).
   `DOC_LANG` = Document language, or `LANG` for `auto`. Send every fixed
   message from `references/messages.md` by its id, translated into `LANG`; keep
   Markdown, `{{...}}` values, paths, keys and commands exactly as they are.
   Approval is language-independent: a clear yes ("yes", "evet", "ja") approves;
   anything else does not.
4. **Workflow.** If the profile has a `Workflow:` line, run `PY -I
   "${CLAUDE_SKILL_DIR}/scripts/workflow.py" <path>` (`PY`: rules.md); its JSON
   is `WF`.
   Exit 3: send `error.workflow-missing` and stop. `WF.unknown` not empty: send
   `note.unknown-heading` once. No `Workflow:` line: `WF` is empty.

Constants: `FIELD` = Sprint field; tracker calls use the profile's Tools
(`cloudId` = Site when the tool takes one); `WORKSPACE` = Workspace, `REPOS` =
Repositories folder, `~` expanded.
Quote every path.

**Stages.** Each step below names its stage. At a stage, apply
`WF.stages.<Stage>.before` first, then the step together with `in`, and after
the stage ends (and is approved, where it needs approval) `after`. Apply every
instruction, in order, and skip none. One you cannot apply: send
`ask.instruction-failed` and wait. A placeholder from `WF.placeholders` gets
`ask.placeholder` the first time an instruction needs it; append `Answer:
<placeholder> <value>` to `jira.md` and use it for the rest of the task. You
fill `<KEY>`, `<SUMMARY>`, `<REPO>`, `<BRANCH>`, `<BASE>` and `<TASK_DIR>`
yourself. An instruction that names its own moment ("when the plan is approved")
runs at that moment, once, however many headings it sits under; before then it
is not a failure. A stage with no instructions follows the step's default. Write
to the tracker only when one says so.

## Find the task

**With an argument** (`KEY` or URL):
1. A URL whose host is not the Site's host: send `error.other-site` and stop.
   Take `KEY` as the first match of `[A-Z][A-Z0-9_]+-[0-9]+` in the argument,
   uppercased.
2. The profile's issue tool with `fields: ["summary", FIELD]`. Not found:
   `error.not-found`, stop.
3. `TASK_DIR` = an existing `WORKSPACE/*/<KEY>` folder; else, with an active
   `FIELD` entry (`state` `active` in any case, or a Server/Data Center string
   with `state=ACTIVE`), `WORKSPACE/SP_<id>/<KEY>`; else
   `WORKSPACE/tasks/<KEY>`. `mkdir -p` it; keep its files.
4. `mcp__ccd_directory__change_directory` to `TASK_DIR` (it applies after this
   turn; until then use absolute paths) and
   `mcp__ccd_session_mgmt__set_session_title` (`"self"`) to `<KEY> <summary>`
   (cut to 60 characters). Do not touch the sidebar.

**Without an argument:** the working folder's name is `KEY` when it matches
`[A-Z][A-Z0-9_]+-[0-9]+` and the folder is inside `WORKSPACE`; then `TASK_DIR` =
it.
Otherwise send `error.no-task` and stop.

**Status and Resume.** `references/status.md` says how `jira.md` keeps status
lines; every "append to `jira.md`" follows it. Files in `TASK_DIR`: read them
and apply its Resume rule.

## 1. Brief and two questions (stage Brief)

1. Read the issue: the profile's issue tool with every field that has a value
   (description, comments, custom fields, links, attachments), and its remote
   links tool when the profile names one. A later comment overrides the
   description where they conflict; say so. A `Repo:`
   line in the description (case-insensitive, comma-separated) gives
   `JIRA_REPOS`. Write all of it to `TASK_DIR/jira.md` (Write tool, never Edit;
   keep any `## Status` section last, unchanged), with acceptance criteria as a
   list and each comment's author and date.
2. Write `TASK_DIR/brief.md` following `references/brief-format.md`, then run
   `references/review.md` on it (Kind `brief`).
3. Send `brief.ready`. With `JIRA_REPOS`, go to 1.4 with those names in the same
   turn; otherwise send `ask.repos` in the same message and end the turn.
   `{{examples}}`: up to two repositories `brief.md` names that `find_repo.py`
   finds, padded to two with unused `user-api`, `order-api`; never assumed
   as the answer.
4. Resolve each name: `PY -I "${CLAUDE_SKILL_DIR}/scripts/find_repo.py" "$REPOS"
   <name>`.
   No result: `ask.repo-missing`; several: `ask.repo-which`; then wait. An
   unclear reply: ask again in one line; never choose. These
   repositories are **changes**; one with no task in the approved plan
   becomes **read**.
5. Send `confirm.repos` (a repository not on GitHub, rules.md, gets "you open
   the merge request yourself"), append `Repositories: <name (changes|read)>, …`
   to `jira.md`, then `mcp__ccd_directory__request_directory` for each
   repository.
6. Send `ask.note` and end the turn. The reply is `NOTE` (`continue` in any
   language or `no` = none). Repositories it asks you to read are **read**
   unless it says they change.
   Add what `NOTE` changes to `brief.md`. If it has no `## Where to start` yet,
   add it now (brief-format.md) and run review.md on it again with these
   repositories.
7. Append `Note: <NOTE or none>` to `jira.md` (update `Repositories:` if `NOTE`
   changed it) and go on to step 2 in the same turn.

## 2. Understand the task

1. Read each repository's `CLAUDE.md` and the `.claude/rules/` files the task
   touches.
2. From the issue copy in `jira.md`: parent/epic: summary and description only.
   Linked issues and sub-tasks: key, summary, status; read one in full only when
   the task depends on it.
3. If `gh` works: `gh pr list --repo <owner>/<repo> --state all --search <KEY>`
   for each listed repository on GitHub.
4. Run `references/discovery.md`: it writes `impact.md`.
5. Add 2.2 and 2.3 to `TASK_DIR/jira.md` (rewrite it with the Write tool;
   `Headings:` stays first, `## Status` last and unchanged).

## 3. Spec (stage Spec)

Method: what `WF.stages.Spec.in` says; else superpowers if a
`superpowers:brainstorming` skill is available; else built-in.
- superpowers: invoke `superpowers:brainstorming` with args:
  `Write the spec to <TASK_DIR>/spec.md in <DOC_LANG>. Context:
  <TASK_DIR>/jira.md,
  <TASK_DIR>/brief.md and <TASK_DIR>/impact.md; the user's note: <NOTE>. Ask
  only questions these do not settle and that change the design or an acceptance
  criterion, in one numbered message with a recommended answer each. One section
  per changing repository, an "Impact and contracts" section with every producer
  → consumer pair from impact.md, sketches with path:line and test names, a
  Scenarios section and a follow-up tasks section, following the writing rules
  and sections of ${CLAUDE_SKILL_DIR}/references/spec-guide.md. Also: <WF Spec
  instructions or none>. Rabbit reviews the spec and asks for approval itself:
  skip your builder check and approval gate. Stop once spec.md is written: do
  not commit it and do not invoke writing-plans.`
- built-in: write `TASK_DIR/spec.md` following `references/spec-guide.md`.

Run Discovery again on the draft (update `## Impact and contracts` if
`impact.md` changed), then `references/review.md` (Kind `spec`), then send
`ask.spec-approval`. On approval append `Approved: spec <date>`; with
`Breaking:` lines, send `ask.breaking` (`{{breaks}}` = those lines) and append
`Approved: breaking <date>` on its yes.

## 4. Plan (stage Plan)

Method as for the spec, with `superpowers:writing-plans`:
- superpowers args: `Spec: <TASK_DIR>/spec.md (approved). Write the plan to
  <TASK_DIR>/plan.md in <DOC_LANG>, tasks grouped by repository, with the order
  between repositories, and for every producer → consumer pair between changing
  repositories a contract-test task in the consumer repository (positive and
  negative cases, fixture from the producer's real output), a test for every
  spec Scenarios row (`S<n> → <path>::<test>`), following
  ${CLAUDE_SKILL_DIR}/references/plan-guide.md. Also: <WF Plan instructions or
  none>. Stop once plan.md is written: do not offer or start execution.`
- built-in: write `TASK_DIR/plan.md` following `references/plan-guide.md`.

Run `references/review.md` (Kind `plan`), then send `ask.plan-approval` and wait
(`{{execute_line}}` from step 5.1; `{{branches}}`: the names step 5.2's rule
gives, with no worktree created yet). A plan change that changes the
spec updates `spec.md` too and asks for both again: spec and plan always agree.
On approval append `Approved: plan <date>` to `jira.md`.

**Approval.** Before appending an `Approved:` line, if the document changed
after its review (its modified time is later), run review.md on it again first.
A change to an approved spec or plan: append `Changed: <spec|plan> <date>`,
update both documents, review and ask again; after the new approval send
`rabbit: plan changed <task ids>` to each dev session whose tasks changed.

## 5. Dev sessions (stage Execute)

Plan approval is the go-ahead; do not wait for "start".
1. Execute method: as `WF.stages.Execute` says; else the one the plan approval
   named (`yes native`); else `superpowers` when a `superpowers:executing-plans`
   skill exists, `native` otherwise. `{{execute_line}}` names that default and
   the other choice, or is empty when the workflow decides. Append `Execute:
   <method>` to `jira.md`. This session reads the Execute instructions only to
   choose the method; the dev sessions apply them.
2. For each **changes** repository with tasks in `plan.md`: base as rules.md
   says; branch from its `CLAUDE.md` or `.claude/rules/`, else one in the style
   of its recent branches (`git -C <repo> for-each-ref
   --sort=-committerdate --count=20 --format='%(refname:short)'
   refs/remotes/origin`) containing `KEY`, else `<key-lowercase>`;
   `{{branches}}` lists them, and the plan approval approves them. Worktree
   `<repo>/.claude/worktrees/<key-lowercase>`:
   already a worktree on `<branch>` (`git -C <repo> worktree list --porcelain`):
   reuse it.
   Else `git -C <repo> fetch origin <base>`, then `git -C <repo> worktree add
   <path> <branch>` if the branch exists, else `git -C <repo> worktree
   add --no-track -b <branch> <path> origin/<base>`. Branch checked out
   elsewhere: stop and ask. If `.claude/worktrees/` is not ignored, add it to
   the file `git -C <repo> rev-parse --git-path info/exclude` prints and say so
   in one line.
3. Fill `references/dev-session-prompt.md` (`{{COORDINATOR}}` = this session's
   id from `mcp__ccd_session_mgmt__get_session` with `"self"`; `{{ANSWERS}}` =
   the placeholder answers so far, or none). Write a bold title line and one
   sentence (several repositories: `mcp__ccd_session__mark_chapter` first), then
   `mcp__ccd_session__start_session` with `initiation: "user_asked"`, `context:
   "fresh"`, `cwd: <worktree>`, `use_worktree: false`, `title: "<KEY> <repo>"`,
   `prompt` = the filled Prompt section, `background` = the filled Background
   section. Append
   `Coordinator: <this session's id>` to `jira.md` once, and for each started
   session `Dev: <repo> <its session id> <worktree> <branch> <base>`. Never
   start a second session for a repository with a `Dev:` line.

A repository added as **changes** later gets these steps once its spec and plan
are approved.

## 6. Coordinate

Answer the dev sessions' messages (`SendMessage` to their `local_…` id). Each
sends `rabbit: done <commits>` when its part is implemented and self-reviewed;
on the first one per repository append `Done: <repo> <date>` to `jira.md`. Write
the findings and follow-ups any `rabbit: done` carries to
`reviews/diff-<repo>.md` (`references/review.md`, Review file).
`rabbit: blocked <reason>` or a question it relays: tell the user, and send the
answer back as `rabbit: answer <text>`; `rabbit: answered <question>`: the user
answered there, drop it.
`rabbit: placeholder <name> <value>`: append `Answer: <name> <value>`. `rabbit:
plan wrong <path:line> <finding>`: change spec and plan as **Approval** says.
All done: go to step 7.

## 7. Integration (stage Integration)

Follow `references/integration.md`.

## 8. Push and CI (stage Push)

Follow `references/publish.md`.
