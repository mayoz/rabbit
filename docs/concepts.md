# Concepts

This page explains the words the rest of the documentation uses. Read it once;
come back when a word is unclear.

- [Claude and its parts](#claude-and-its-parts)
- [Sprint and task](#sprint-and-task)
- [The two kinds of session](#the-two-kinds-of-session)
- [Documents Rabbit writes](#documents-rabbit-writes)
- [Reviews and checks](#reviews-and-checks)
- [Git](#git)
- [Customizing](#customizing)

## Claude and its parts

**Claude Code.** Anthropic's coding assistant. It runs in a terminal (`claude`)
and in the **Code** tab of the Claude Desktop app.

**Claude Desktop.** The desktop app. Rabbit needs it because only Desktop can
open new sessions and show them in its sidebar.

**Session.** One conversation with Claude, shown as a row in Desktop's sidebar.
Each session has its own working folder and remembers only its own conversation.

**Sidebar section.** A group of sessions in Desktop's sidebar. `/rabbit:pull`
puts your sprint in a section called **Sprints**.

**Nested session.** A session started by another session. It appears under its
parent in the sidebar.

**Plugin.** A package that adds commands and helpers to Claude Code. Rabbit is a
plugin.

**Skill.** One command a plugin adds, such as `/rabbit:pull`. When you run it,
Claude reads the skill's instructions and follows them.

**Agent.** A helper Claude can start for one job. Rabbit has one,
the **observer**, which reviews documents and code.

**Hook.** A small script Claude Code runs on an event. Rabbit has two: one runs
when a session resumes or is compacted, so the session keeps following Rabbit's
rules; the other lets the observer use only tools and commands that read.

**Compaction.** When a conversation grows long, Claude Code shortens its history
to make room. Rabbit's hook makes sure the rules survive this.

**MCP server.** A connector that gives Claude tools for another service. Rabbit
reads Jira through a Jira MCP server, for example Atlassian's.

## Sprint and task

**Sprint.** Your team's active Jira sprint. Rabbit only looks at issues assigned
to you.

**Task.** One Jira issue you work on, such as `ABC-123`. Rabbit gives each task
its own folder and session.

**Workspace.** The folder that holds your sprint folders, for example
`~/rabbit/sprints`. Rabbit's documents live here, never in your repositories.

**Sprint folder.** One folder per sprint inside the workspace, named
`SP_<sprint-id>`. It holds `summary.md` and a task folder per task.

**Task folder.** One folder per task inside its sprint folder, named after the
key, for example `SP_1234/ABC-123/`. It holds the task's brief, spec, plan and
reviews.

**Repositories folder.** The folder that holds your git clones, for example
`~/code`. Rabbit finds a repository here by name, or one folder deeper.

## The two kinds of session

**Task session.** One per task. It talks to you, writes the documents and
coordinates the work. It never edits your code.

**Dev session.** One per repository that changes. It writes the code, one commit
per plan step, in its own worktree. You rarely need to talk to it: it reports to
the task session.

## Documents Rabbit writes

**Brief** (`brief.md`). The task on one page: what happened, what is asked, what
is expected and where in the code the change starts.

**Spec** (`spec.md`). The design: what will change, in which repository, how it
is checked.

**Plan** (`plan.md`). The steps to build the spec, with a test for each.

**Impact list** (`impact.md`). What the change touches and which code uses it.

**Integration report** (`integration.md`). The result of trying the change end
to end.

**Review files** (`reviews/`). What each blind review found and what happened to
it.

**`jira.md`.** Everything the issue says, plus status lines that record your
approvals and progress. Rabbit resumes a task from these lines, so don't edit
them.

## Reviews and checks

**Blind review.** A review by the observer, who never sees your conversation:
only the document or code and its sources. It cannot be talked into agreeing.

**Finding.** One problem a review reports. Each has a severity:
- `critical`: wrong or unsafe; it must be fixed.
- `major`: a real gap a user or developer would hit; it must be fixed.
- `minor`: polish; fixed when the fix is small.

**Scenario.** One thing the change must do, written in the spec, such as "a
signed-in user saves a campaign". Integration tries each scenario in the running
application.

**Producer and consumer.** When one repository sends data (an API response, an
event) and another reads it, the first is the producer and the second the
consumer.

**Contract test.** A test in the consumer that checks it still understands what
the producer sends.

**Result.** Every scenario ends as `passed`, `failed` or `unverified` (it could
not be run safely or at all). A failed or unverified one always says why and
what would make it pass.

## Git

**Base branch.** The branch your change starts from and merges into, usually
`main`.

**Worktree.** A second working copy of a repository in another folder, on its
own branch. Dev sessions work in worktrees, so your main checkout's branch and
files never change.

**Draft pull request.** A pull request marked as not ready for review. Some CI
checks skip drafts.

**Required checks.** The CI checks a pull request must pass before it can merge.

## Customizing

**Profile.** Your personal settings in `~/.config/rabbit/profile.md`: folders,
languages and Jira connection. See [Your profile](profile.md).

**Workflow file.** An optional Markdown file with your own instructions for each
stage of a task. See [Customizing Rabbit](customizing.md).

**Stage.** A part of a task: Brief, Spec, Plan, Execute, Review, Integration and
Push. A workflow file adds instructions to a stage with a heading such as `##
Plan`, and before or after it with `## Plan:Before` or `## Plan:After`.

**Placeholder.** A word in angle brackets in a workflow file, such as
`<environment>`. Rabbit fills in `<KEY>`, `<SUMMARY>`, `<REPO>`, `<BRANCH>`,
`<BASE>` and `<TASK_DIR>` itself and asks you for any other.

**superpowers.** An optional plugin with deeper skills for writing specs and
plans and for implementing them. Rabbit uses it when it is installed.

**native.** Rabbit's own way of implementing a plan: one step, one test, one
commit at a time.
