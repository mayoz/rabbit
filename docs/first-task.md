# Your first task

This page follows one task from the issue to a pull request, so you know what
each step does and what Rabbit asks you. It assumes you ran [Getting
started](getting-started.md).

- [The journey at a glance](#the-journey-at-a-glance)
- [1. Brief](#1-brief)
- [2. Two questions](#2-two-questions)
- [3. Spec](#3-spec)
- [4. Plan](#4-plan)
- [5. Dev sessions](#5-dev-sessions)
- [6. Integration](#6-integration)
- [7. Push](#7-push)
- [8. CI](#8-ci)
- [9. Finish the task](#9-finish-the-task)
- [Changing course](#changing-course)
- [Questions you may see](#questions-you-may-see)

## The journey at a glance

| Step | Who works | What you do |
| --- | --- | --- |
| 1. Brief | task session | Read `brief.md`. |
| 2. Two questions | task session | Pick the repositories, add a note or pick "Nothing to add". |
| 3. Spec | task session | Answer open questions, approve the spec. |
| 4. Plan | task session | Approve the plan. |
| 5. Dev sessions | one dev session per repository | Usually nothing. Answer if one asks. |
| 6. Integration | task session | Read the results table. |
| 7. Push | task session | Say `ready` or `draft`. |
| 8. CI | task session | Say whether Rabbit should follow CI. |

You talk to the **task session** the whole time. Keep it open until the task is
done: the dev sessions report to it.

## 1. Brief

When the task session opens, it reads the whole issue: the description, every
comment, every field with a value, and linked pages, and keeps a copy in
`jira.md`, so later steps don't ask Jira again. It writes `brief.md`, one short
page: what happened, what is asked, what is expected, later where in the code
the change starts, and any open points such as an issue that blocks this one.
Every statement names its source, for example a comment's author and date.

Before you see it, the **observer**, a reviewer that never sees your
conversation, checks the brief against the issue. Rabbit fixes what it finds.
The message tells you the brief is ready.

## 2. Two questions

1. **Which repositories do we need to work in?** Type the names of the
   repositories that will change. The examples in the question are the
   repositories the brief names that Rabbit finds in your repositories folder.
   If the issue's description has a line such as `Repo: web-app, api`, Rabbit
   takes the names from it and skips this question.
2. **Anything you'd like to add?** Pick "Nothing to add" if not. Otherwise add
   what helps: other repositories to read, things to watch, decisions already
   made.

Claude Desktop may ask you to allow access to each repository folder. Allow it.

Rabbit now reads the code on the **base branch** (usually `main`, fetched from
`origin`), not your checkout, so your local changes never confuse it. It lists
everything the change touches and every place that uses it, in other
repositories too, in `impact.md`.

## 3. Spec

The spec says what will change, in which repository, and how each change is
proven. It lists **scenarios**, the things the change must do, which Integration
tries later.

If something can't be settled from the issue or the code, Rabbit asks you in one
message, with a recommended answer for each question. With
[superpowers](installation.md#3-install-superpowers-optional) installed, it uses
superpowers' brainstorming to write the spec.

Rabbit keeps every contract that other code reads backward compatible: response
shapes, events, database columns, config. If the change must break one, the
approval question says so and the break needs its own yes.

Read `spec.md` and pick "Approve", or say what to change.

## 4. Plan

The plan turns the spec into small steps, grouped by repository, each with its
test. When one repository sends data that another reads, the plan adds
a **contract test** in the reader.

Read `plan.md` and pick "Approve". Plan approval is the go-ahead: Rabbit opens
the dev sessions straight away.

## 5. Dev sessions

The dev sessions implement the plan with `superpowers` when it is installed,
else with Rabbit's own loop (`native`); the plan approval message says which.
Your workflow file can decide instead. Then Rabbit opens one dev session per
changing repository, nested under the task session.

Each dev session works in its own **worktree**, a second copy of the repository
in `<repo>/.claude/worktrees/<key in lower case>` (for example `abc-1`), on its
own branch, named in the plan approval message. Your main checkout's branch and
files never change. If `.claude/worktrees/` is not ignored by the repository,
Rabbit adds it to
the repository's `info/exclude` file, a local ignore file that is never
committed.

A dev session implements one step at a time: a test, the code, the test run, one
local commit. When it is done it reviews its own diff with the observer and
reports to the task session. It never pushes on its own.

You rarely need to open a dev session. If one gets stuck, the task session tells
you.

## 6. Integration

When every dev session is done, Rabbit checks the whole change together:

1. It updates the impact list against the new branches.
2. One blind review covers every repository at once.
3. Dev sessions run the contract tests, the tests linked to each scenario, and
   each repository's full test suite once.
4. Rabbit starts the applications from the worktrees and tries every scenario:
   real HTTP requests and jobs for a backend, the browser for a frontend.

Rabbit only runs an application or a test against **local** services. If a
database, queue or API address is not on your machine, that scenario is not run.

You get one table. Each row is `passed`, `failed` or `unverified` (it could not
be run, or not safely). A failed or unverified row always says why and what
would make it pass. Rabbit fixes failures through the dev sessions, at most
twice, and never calls the change working unless every row passed.

If Integration created test data, such as database rows, Rabbit lists it and
asks whether to remove it.

## 7. Push

Rabbit asks once for all repositories: open the pull requests **ready** for
review (recommended) or as **draft**. If some rows did not pass, it shows them,
asks whether to push anyway and recommends **draft**. Repositories not on GitHub
get their branch pushed; you open the merge request yourself.

The dev sessions push their branches and open the pull requests. Rabbit links
them to each other and shows a table:

| Repository | PR | Status | CI |
| --- | --- | --- | --- |
| web-app | #42 | ready | waiting |

Drafts wait: tell Rabbit when they should be ready for review.

## 8. CI

Rabbit asks whether to follow CI. If yes, each dev session watches its own pull
request. When a required check fails, Rabbit tells you which one and asks before
it fixes it; a fix is pushed to the same branch. The last message repeats the
table with CI results.

## 9. Finish the task

Rabbit never deletes a branch, a worktree or a session. When the pull requests
are merged:

- **Archive the sessions** of the task in Desktop's sidebar (right-click a
  session).
- **Remove each worktree**, from the repository's main checkout:

  ```bash
  git worktree remove .claude/worktrees/abc-1
  ```

- **Delete the local branch** if you no longer need it: `git branch -d <branch>`
  (`-D` after a squash merge).
- **Keep or delete the task folder.** It holds the brief, spec, plan and
  reviews, which are useful when someone asks why a change was made.

## Changing course

| You want to | Do this |
| --- | --- |
| Pause | Just stop. Open the task session later; Rabbit resumes from where it was. |
| Change the spec or plan after approving it | Tell the task session what to change. It updates both and asks for approval again. |
| Add a repository | Tell the task session. It reads it and updates the spec and plan with your approval. |
| Run Integration again | Pick "Don't push yet" at the push question, then ask the task session to run Integration again. |
| Restart after a crash or `/compact` | Nothing. A hook reloads Rabbit's rules; if it did not, type `/rabbit:task` in the task session. |
| Stop the task for good | Archive its sessions and remove its worktrees as in [step 9](#9-finish-the-task). |

## Questions you may see

| Question | When | A good answer |
| --- | --- | --- |
| Shall I run these (workflow instructions)? | Your workflow file asks Rabbit to act outside your machine, and it is new or changed. | "Run them" if the list is what you expect. |
| How do I start `<repo>` locally? | Rabbit can't find the start command. | The command, for example `npm run dev`. Add it to the repository's `CLAUDE.md` too. |
| How do I run the full test suite? | Rabbit can't find the command. | The command, or "Leave it to CI". |
| `<repo>` would break; add it? | A repository that doesn't change uses what the change touches. | Usually "Add it". |
| A value for `<environment>`? | Your workflow file has a placeholder. | The value. Rabbit remembers it for this task. |

Claude Code may also ask permission before running a command, depending on your
permission settings. Rabbit's commands are git, `gh`, `mkdir`, `find`, Python
(its two helpers and a port check), `docker compose` when your project uses it,
and your project's test and start commands.
