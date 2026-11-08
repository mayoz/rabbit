# How it works

This page explains what Rabbit does behind the scenes: its sessions, the files
it writes, the checks it runs and the lines it never crosses. For the words used
here, see [Concepts](concepts.md).

- [Sessions](#sessions)
- [Folders and files](#folders-and-files)
- [The status lines in jira.md](#the-status-lines-in-jiramd)
- [A task, step by step](#a-task-step-by-step)
- [Blind reviews](#blind-reviews)
- [Integration](#integration)
- [Surviving a restart](#surviving-a-restart)
- [What Rabbit never does](#what-rabbit-never-does)

## Sessions

```
Sprints (sidebar section)
└── SP_<sprint-id>            ← /rabbit:pull runs here; owns summary.md
    ├── ABC-1 Fix login       ← /rabbit:task; owns the brief, spec and plan
    │   ├── ABC-1 web-app     ← /rabbit:dev, in a git worktree
    │   └── ABC-1 api
    └── ABC-2 Add export
```

- The **sprint session** pulls the sprint and opens task sessions.
- A **task session** talks to you, writes the documents and coordinates. It
  never edits your code.
- A **dev session** writes the code for one repository and reports to its task
  session.

Sessions talk to each other with short messages that start with `rabbit:`, for
example `rabbit: done` from a dev session. You can read them in each session,
but you don't need to.

## Folders and files

```
<Workspace>/
├── SP_<sprint-id>/          one folder per pulled sprint
│   ├── summary.md           every task of the sprint and its session
│   └── ABC-1/               one folder per task
│       ├── jira.md          everything the issue says, plus status lines
│       ├── brief.md         the task on one page
│       ├── impact.md        what the change touches and who uses it
│       ├── spec.md          the design
│       ├── plan.md          the steps
│       ├── integration.md   every scenario tried end to end, with its result
│       └── reviews/         one file per blind review, with every proven finding
└── tasks/
    └── ABC-9/               a task started with /rabbit:task outside an active sprint
```

Documents live in the workspace, never in your repositories. Code changes happen
only in the dev sessions' worktrees, `<repo>/.claude/worktrees/<key in lower
case>`. If the repository does not ignore `.claude/worktrees/`, Rabbit adds it
to `<repo>/.git/info/exclude`, a local ignore list that is never committed.

## The status lines in jira.md

Rabbit records each step's outcome as a line under `## Status` at the end of
`jira.md`, always in English, for example:

```
## Status
Repositories: web-app (changes), api (changes)
Approved: plan 2026-11-07
Dev: web-app local_abc123 /code/web-app/.claude/worktrees/abc-1 feature/ABC-1 main
Integration: passed 2026-11-07
PR: web-app https://github.com/acme/web-app/pull/42 ready
```

When a session restarts, Rabbit reads these lines to see where it was and
continues from there. **Don't edit or delete them**, or Rabbit may repeat or
skip a step.

## A task, step by step

At every stage Rabbit applies the instructions of your [workflow
file](workflow.md), if you have one; the defaults below apply where it says
nothing.

1. **Brief.** The issue, every comment and field, condensed to a page.
2. **Two questions.** Which repositories (skipped when the issue has a `Repo:`
   line), and anything else to know.
3. **Spec, then plan.** Rabbit reads the code on the base branch, not your
   checkout, lists what the change touches and who uses it, and writes the spec,
   then the plan. With superpowers installed it uses superpowers' skills for
   both, else its own guides. Each needs your approval, and the two always
   agree.
4. **Dev sessions.** On plan approval, one per changing repository: superpowers
   or Rabbit's own loop, one commit per step, then a blind review of its own
   diff.
5. **Integration.** The whole change is checked together; see
   [below](#integration).
6. **Push.** Rabbit shows each repository's branch and asks once for all of
   them: ready for review or draft.
   The dev sessions push and open pull requests; Rabbit links them to each
   other.
7. **CI.** Rabbit asks whether to follow CI and asks before fixing a failing
   check. Checks the workflow names as waiting for a later step are left out.

[Your first task](first-task.md) walks through these steps from your side.

## Blind reviews

Before you see a brief, spec or plan, and after each dev session's code, the
`rabbit:observer` agent reviews the work. It never sees your conversation, only
the work and its sources, so it can't be talked into agreeing.

- Each finding is `critical`, `major` or `minor`, with the problem, the evidence
  and a solution.
- Rabbit checks every finding itself. One it cannot prove goes under **Not
  proven** in the review file, with the reason.
- Critical and major findings are fixed; minor ones when the fix is small. A
  critical or major one with no fix in scope comes to you.
- A second round runs only when a critical or major finding was fixed, and
  checks only those fixes. A later change is sorted first: a critical one gets
  one round on what changed, any other none. A document gets at most three
  rounds.

The observer has no tools to write files. A hook also checks every tool it calls
and lets through only reading tools (Read, Grep, Glob), shell commands made only
of known read-only commands such as `git show`, `git grep`, `git log`, `git
diff`, `ls` or `cat`, MCP tools whose names start with a read word (`get…`,
`list…`, `search…`) and hold no write word, and the Jira tools your profile
names. Anything else is blocked, and so is any call the hook fails to check.
Without Python 3 the hook blocks every tool the observer calls, so reviews
cannot run; see [Installation](installation.md).

## Integration

Integration runs in the task session after every dev session is done, before the
push question.

1. **Impact check.** The list of what the change touches is checked again
   against the new branches. A repository that doesn't change but would break is
   reported, and Rabbit asks whether to add it.
2. **Joint review.** One blind review covers every repository together and
   compares what each producer sends with what each consumer reads.
3. **Tests.** Contract tests between producers and consumers, the tests linked
   to each scenario, and each repository's full test suite once. You can turn
   the full suite off in your workflow file.
4. **Running the apps.** Rabbit starts each application from its worktree and
   tries every scenario: HTTP requests and jobs for a backend, the browser for a
   frontend. A library has no app to start, so its rows rest on its tests.
5. **Fixes.** Failures go back to the dev sessions, at most two rounds.
6. **Report.** One table, every row `passed`, `failed` or `unverified`, each
   failed or unverified row with its reason and what would make it pass. Test
   data Integration created is listed, and Rabbit asks whether to remove it.

Before starting an app or a test, Rabbit checks every service address it would
use, such as the database, cache, queue, mail or an external API. Each must be
on your machine (`localhost`, `127.0.0.1` or a compose service) and answering.
Otherwise that run is `unverified`. If a worktree needs dependencies installed
or a `.env` file, Rabbit sets them up without asking, and never commits them.

## Surviving a restart

When a conversation grows long, Claude Code compacts it, and a closed session
can be resumed. Either way, a session-start hook tells a task or dev session to
load its skill again, and the skill continues from `jira.md`'s status lines.

## What Rabbit never does

- Write to your tracker unless your workflow file says so. An instruction that
  acts outside your machine runs only after you approve the file, and again
  after it changes.
- Push or open a pull request before you say yes, force-push or rewrite history.
- Delete a branch, a worktree, a commit or a tracker attachment.
- Run a database migration or seeder without asking, or run anything against a
  service that is not on your machine.
- Change your main checkout's branch or files. Code changes happen only in
  worktrees.
- Store a token or a password.
