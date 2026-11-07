---
name: pull
description: Pull your active Jira sprint into Claude Desktop. Use when the user asks to pull, sync or load their sprint. Makes this session the sprint's main session, creates one folder and one task session per unfinished task, and writes summary.md. Read-only on the tracker.
---

# Pull

Never write to the tracker. Run the steps in order; stop and ask when a step
says so.

## 0. Before anything

1. **Desktop.** If no `mcp__ccd_session__start_session` tool exists (loaded or
   deferred), send `error.desktop-only` (in the user's language) and stop.
   Create nothing.
2. **Profile.** Read `~/.config/rabbit/profile.md` (its `Workflow:` line is not
   used here).
   If it is missing or unreadable, or a required value is empty (Basics:
   Workspace, Repositories folder, Chat language, Document language; Tracker:
   Site, Tools, Sprint field), send `setup.needed` naming what is missing, run
   the `rabbit:setup` skill with the Skill tool, and when it finishes continue
   here.
   Site or Tools still empty after setup: stop (setup has said what to connect).
   Sprint field still empty (no sprints on this site): send `error.no-sprint`
   and stop.
3. **Language.** `LANG` = Chat language, or for `auto` the language of the
   user's last message (English if none). `DOC_LANG` = Document language, or
   `LANG` for `auto`. Every message stays in `LANG`, even after text in another
   language. Send fixed messages from `references/messages.md` by id,
   translated; keep Markdown, `{{...}}` values, paths, keys and commands as they
   are.

Constants: `FIELD` = Tracker Sprint field; tracker calls use the profile's Tools
(with `cloudId` = Site when the tool takes one); `WORKSPACE` = Basics Workspace
with `~` expanded; sidebar section `Sprints`.

## 1. Read the sprint

Search with `jql: "assignee = currentUser() AND sprint in openSprints() ORDER BY
key"`, `fields: ["summary", "status", "issuetype", "priority", "labels",
"parent", "description", FIELD]`, `maxResults: 100`. Never ask for an "evidence"
or expanded view. Follow the tool's paging (for example `nextPageToken` until
`isLast`, or `startAt`) until every issue is read.

From each issue's `FIELD` keep the active entries: `state` `active` in any case,
or a string entry such as `…Sprint@x[id=12,…,state=ACTIVE,name=…]` (Jira
Server/Data Center), read the same way. No issue: send `error.no-sprint` and
stop. If they span more than one sprint id, send `ask.which-sprint` with the
list, end the turn, and keep only the chosen sprint's issues.
`SPRINT_ID` = that sprint's `id`; `LABEL` = `SP_<SPRINT_ID>`;
`SPRINT_DIR` = `"<WORKSPACE>/<LABEL>"` (always quote paths).

Unfinished keys: the same JQL with `AND statusCategory != Done` before `ORDER
BY` (`fields: ["summary"]`), kept only when the key is among the chosen sprint's
issues. Do not infer status categories from status names.

## 2. Become the sprint's main session

1. `mcp__ccd_sidebar__list_sections`: take the first section named `Sprints`;
   none: create it with `mcp__ccd_sidebar__create_section`.
2. `mcp__ccd_session_mgmt__list_sessions` with `limit: 500` (this session is
   never in the result).
3. A session titled exactly `LABEL` means another session is this sprint's main
   session:
   send `error.other-main` linking it as `[<title>](#<sessionId>)` and stop.
   Create nothing.
4. Otherwise move this session into the section
   (`mcp__ccd_sidebar__move_sessions`, `session_ids: ["self"]`, `section_id`).
   If refused because this session is nested, run
   `mcp__ccd_session_mgmt__detach_session` with `"self"` and move again. Title
   it `LABEL` (`mcp__ccd_session_mgmt__set_session_title`, `"self"`).
5. `mkdir -p` `SPRINT_DIR` and `mcp__ccd_directory__change_directory` to it (it
   applies after this turn; until then use absolute paths).

## 3. Decide which tasks need a session

`mcp__ccd_session_mgmt__get_session` with `"self"` gives this session's id;
`mcp__ccd_session_mgmt__list_sessions` with `linked: true`, `include_archived:
true`, `limit: 500` lists the sessions it started. A task already has a session
when one of them has `startedBy` equal to that id and a title matching
`(^|[^A-Z0-9-])<KEY>([^0-9]|$)`. A task whose folder `<WORKSPACE>/*/<KEY>/`
exists outside `SPRINT_DIR` (an earlier sprint, or `tasks/`) is **carried
over**: its session
and documents stay there; create no folder or session for it. Missing =
unfinished, not carried over and no session. Finished tasks and tasks that left
the sprint are never touched.

## 4. Prepare folders

`mkdir -p` `SPRINT_DIR/<KEY>` for every unfinished task. Never delete or
overwrite anything in an existing task folder.

## 5. Open the missing task sessions

For each missing task, in key order:
- Title: `<KEY> ` + the summary with leading `[...]` tags and spaces removed;
  over 60 characters: cut to 59 and append `…`.
- Fill `references/task-session-prompt.md` and call
  `mcp__ccd_session__start_session` with `initiation: "user_asked"`, `context:
  "fresh"`, `cwd: <task dir>`, `use_worktree: false`, `title`, `prompt` = filled
  Prompt section, `background` = filled Background section. Do not pass
  `permission_mode` or `model`.
- Do not move task sessions: they nest under this session and follow it.

Before the batch, write a bold title line and one sentence.

## 6. Write summary.md

Write `SPRINT_DIR/summary.md` in `DOC_LANG` following
`references/summary-format.md`.

## 7. Report

Send `report.done`. If sessions were opened, send `report.ready` once when each
has finished its first turn, and stop.
