# Troubleshooting

Find your problem below. If it is not here, see [Getting help](#getting-help).

- [Installing and setup](#installing-and-setup)
- [Pulling a sprint](#pulling-a-sprint)
- [Working on a task](#working-on-a-task)
- [Integration](#integration)
- [Push and CI](#push-and-ci)
- [Getting help](#getting-help)

## Installing and setup

**The `/rabbit:...` commands do not appear.** Start a new session after
installing. Check that `claude plugin list` shows `rabbit@mayoz` as enabled.

**"only works in the Claude Desktop app".** `pull`, `task` and `dev` open
sessions; run them in Desktop's **Code** tab, not in the terminal.

**A hook error mentions `python3` or `python`.** Python 3 is not on your `PATH`.
Install it (see [Installation](installation.md#your-operating-system)) and start
a new session. On Windows, tick "Add python.exe to PATH" in the installer.

**Setup says it can't find a Jira connection.** Add an MCP server for Jira (see
[Installation](installation.md#1-connect-jira)), start a new session and run
`/rabbit:setup` again.

**Setup can't find the sprint field.** None of your issues is in an active
sprint yet. Run setup again once one is. `/rabbit:task <KEY>` works without it.

**"I can't read" a workflow file.** Check the path; `~` is fine. The file must
be UTF-8 text. If it lives in a team repository, that repository must be cloned
on this machine.

**"Won't apply" a workflow heading.** Only the stage names in
[Your workflow file](workflow.md#stages) are read. Rename the heading or remove
it.

**Messages are in the wrong language.** Set `Chat language` in your profile to a
language instead of `auto`.

## Pulling a sprint

**"already has a main session".** You ran `/rabbit:pull` in a new session, but
the sprint already has one. Open the linked session and run it there.

**A task has no session.** Finished tasks get none. A task that was added later
appears when you run `/rabbit:pull` again in the sprint session.

## Working on a task

**Desktop asks to allow access to a folder.** Rabbit asks for access to each
repository you name. Allow it; without access it can't read the code.

**"I can't find `<name>`".** Rabbit looks for a repository by name in your
repositories folder and one folder below it. Clone it there, or fix the folder
with `/rabbit:setup`.

**"Branch checked out elsewhere".** The task's branch is checked out in another
folder, for example your main checkout. Switch that folder to another branch,
then tell the task session to continue.

**Rabbit "forgot" its rules after a compaction.** The session-start hook reloads
the skill in task and dev sessions. If it did not, type `/rabbit:task` in the
task session, or `/rabbit:dev` in a dev session; it resumes from `jira.md`.

**Rabbit repeats or skips a step.** Check the status lines at the end of the
task's `jira.md`. They record each step; an edited or deleted line confuses the
resume. See [How it works](how-it-works.md#the-status-lines-in-jiramd).

**A fact is marked "not verified locally".** A repository was read through a
code search tool because it isn't cloned. Clone it into your repositories folder
to have it checked.

## Integration

**A scenario is `unverified` because an address "is not local".** Integration
only runs against services on your machine. Start the service locally (for
example with `docker compose up`), or test that scenario in a test environment.

**"Port in use".** An app from your main checkout is running on the same port.
Rabbit tries another port; if the app can't take one, stop the other app and
tell Rabbit to continue.

**The full test suite takes too long.** Turn it off in your workflow file; see
[Customizing
Rabbit](customizing.md#run-only-the-affected-tests-instead-of-the-full-suite).

## Push and CI

**No pull request on GitLab or Bitbucket, or a `gh` error.** Opening pull
requests and following CI need a GitHub `origin` and a signed-in [GitHub
CLI](https://cli.github.com) (check with `gh auth status`). On another host,
Rabbit pushes the branch and you open the merge request yourself; Rabbit says so
when you confirm the repositories.

**CI is `waiting`.** Rabbit has not started following CI yet: either you have
not answered whether to follow it, or the pull requests are drafts. Tell the
task session when drafts should be ready for review.

## Getting help

Search the [issues](https://github.com/mayoz/rabbit/issues) first. If yours is
new, open one with the command you ran, what you expected, what happened and
your Claude Code version (`claude --version`). Leave out your tracker site and
any private names.
