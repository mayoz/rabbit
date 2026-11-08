---
name: setup
description: Set up or check Rabbit. Writes your profile (sprint folder, repositories folder, languages, optional workflow file) by asking one short question at a time with examples, and finds your Jira tools, site and sprint field itself. When a profile exists it checks it and fixes what you ask. Use when the user says set up rabbit, configure rabbit, rabbit doctor, or when another Rabbit command finds no profile.
---

# Setup

Writes and checks `~/.config/rabbit/profile.md`. The format is described in
`${CLAUDE_PLUGIN_ROOT}/docs/profile.md`, workflow files in
`${CLAUDE_PLUGIN_ROOT}/docs/workflow.md`; read them only if you need a detail
this file lacks.

## Rules

- `LANG`: the profile's Chat language if set and not `auto`; otherwise the
  language of the user's last message; English if there is none. Send every
  fixed message from
  `references/messages.md` by its id, translated into `LANG`; keep Markdown,
  `{{...}}` values, paths, URLs, commands and keys exactly as they are.
- Ask questions from `references/questions.md` one at a time, with
  `AskUserQuestion` (load it with `ToolSearch` if deferred): one question per
  call, the question, an empty line and its purpose in one line, its `Header`
  and `Options`, the default first with ` (Recommended)`; the user types any
  other answer under Other. A question asked again (its answer did not work)
  uses the same tool and options, the reason first.
  Without that tool: one question per message with its purpose, example and
  default, then end the turn and wait; no list unless the question is a pick
  list.
- If the user already gave answers (in the request or earlier), use them and do
  not ask again. An empty reply or `default` means the default.
- `PY` = `python3`, or `python` when `python3` is missing or is not Python 3
  (the Windows Store alias). Expand `~` before writing with `PY -I -c "import
  os;print(os.path.expanduser('~'))"`, or without Python `$HOME`
  (`%USERPROFILE%` on Windows). Never write a token or password.
- Never write to Jira. Only read: the two searches below.
- Run commands only as written here; do not install anything for the user.

## 1. Existing profile → doctor mode

If `~/.config/rabbit/profile.md` exists, read it.

1. **Check:** Basics has Workspace, Repositories folder, Chat language, Document
   language; Tracker has Site and Tools; the folders exist; the Tracker tools
   are available; the `Workflow:` file, if set, passes the step 2 check. An
   empty Site or Tools: run step 4. An empty Sprint field: run step 4.3.
   A Tracker tool name the server no longer offers: replace it with the server's
   tool for the same job (step 4.1) and say so; Tracker is found, never asked.
   Write what these checks found or replaced at once (step 5, changed lines
   only).
   Send `setup.doctor`: a `| Setting | Value |` table of `Workflow` (or `none`),
   the Basics lines and the Tracker lines, then one line per check (✓ or ✗ and
   why).
2. Ask `doctor-next`. **Cancel:** say in one line that nothing else changed, and
   stop. **Set up again:** run steps 2–6; in each question the current value
   comes first with ` (Recommended)`, then the other options without it. Any
   other answer names what to change: change only that, then go to step 5.

No profile: send `setup.welcome` and start at step 2.

## 2. Workflow file

Ask `workflow`. On a path, run
`PY -I "${CLAUDE_PLUGIN_ROOT}/skills/task/scripts/workflow.py" <path>`. If it
can't run, read the file instead.
- Exit 3 or unreadable: ask `workflow` again with `setup.workflow-missing` as
  its reason. Never write the profile with a path that can't be read.
- Otherwise send `setup.workflow-read` with each part that has instructions,
  named as its heading (`Environment` when `environment` is not empty,
  `Plan:After`).
  If `unknown` is not empty, send `setup.workflow-unknown` with those headings;
  if `placeholders` is not empty, send `setup.workflow-placeholders` with them.

## 3. Basics

Ask `workspace`, `repositories`, `chat-language`, `doc-language` in turn.
- Workspace folder missing: ask `setup.folder-create` with `AskUserQuestion`;
  on Create it, `mkdir -p` it; else ask again.
- Repositories folder: count clones with
  `find "<dir>" -maxdepth 3 -name .git | wc -l`; send `setup.repos-found` and
  continue, or `setup.repos-none` and ask again (unless the user gave this
  folder in the request: then keep it and continue).

## 4. Tracker (found, not asked)

1. **Tools.** A Jira tool set is one server's tools for searching issues (a name
   ending in `searchJiraIssuesUsingJql`, or a Jira search tool) and reading an
   issue, plus its tool for reading remote links when it has one. Use ToolSearch
   if tools are deferred. None: write the profile with Tracker empty (step 5),
   send `setup.no-jira-tools` and stop. More than one set: ask
   `tracker-tools` once, listing the sets found.
2. **Site.** From the tools: `getAccessibleAtlassianResources` (its `url`) when
   the set has it; otherwise the site the server reports, or the host of the
   `self` link of the issue step 3's search returns (run it first). More than
   one site: ask `site`, listing them.
3. **Sprint field.** Search `assignee = currentUser() AND sprint in
   openSprints() ORDER BY key`, `maxResults: 1`, `fields: ["*all"]` (`cloudId` =
   Site when the tool takes one). The sprint field is the `customfield_*` whose
   value is a list of objects with `id`, `name`, `state` and `boardId`, or (Jira
   Server/Data Center) of strings such as
   `…Sprint@x[id=12,rapidViewId=3,state=ACTIVE,name=…]`. Found: send
   `setup.sprint-field`. No issue: send `setup.sprint-field-missing`, leave it
   empty and continue.

## 5. Write the profile

`mkdir -p ~/.config/rabbit`, then write `~/.config/rabbit/profile.md`:

```markdown
# Profile

Workflow: <path, only if given>

## Basics
- Workspace: <path>
- Repositories folder: <path>
- Chat language: <value>
- Document language: <value>

## Tracker
- Site: <url>
- Tools: <server> (<search tool>, <issue tool>[, <remote links tool>])
- Sprint field: <customfield_...>
```

In doctor mode, edit only the lines that change. Send `setup.saved` with the
path.

## 6. Test run

If Site, Tools and Sprint field are set, run the active-sprint search once
(`fields: ["summary", "<sprint field>"]`, `maxResults: 50`) and send `setup.try`
with the active sprint's name and the issue count, then `setup.done`; or
`setup.try-failed` with the error.

Whenever setup ends or stops, if another Rabbit command started it, go back to
that command.
