# FAQ

- [Does Rabbit change anything in Jira?](#does-rabbit-change-anything-in-jira)
- [Does Rabbit push or merge on its own?](#does-rabbit-push-or-merge-on-its-own)
- [Will it touch my uncommitted work?](#will-it-touch-my-uncommitted-work)
- [Where does my data go?](#where-does-my-data-go)
- [Can I use it without Claude Desktop?](#can-i-use-it-without-claude-desktop)
- [Does it work on Windows and Linux?](#does-it-work-on-windows-and-linux)
- [Does it work with Jira Server, GitLab or
  Bitbucket?](#does-it-work-with-jira-server-gitlab-or-bitbucket)
- [Do I need superpowers?](#do-i-need-superpowers)
- [What if I am in more than one sprint?](#what-if-i-am-in-more-than-one-sprint)
- [What about sub-tasks and epics?](#what-about-sub-tasks-and-epics)
- [Can I talk in one language and write documents in
  another?](#can-i-talk-in-one-language-and-write-documents-in-another)
- [Can I edit the brief, spec or plan
  myself?](#can-i-edit-the-brief-spec-or-plan-myself)
- [Can I close the task session while dev sessions
  work?](#can-i-close-the-task-session-while-dev-sessions-work)
- [How do I clean up after a task?](#how-do-i-clean-up-after-a-task)

### Does Rabbit change anything in Jira?

No, unless your [workflow
file](customizing.md#move-the-issue-when-work-starts-and-ends) tells it to. Even
then, it asks you once to approve those instructions, and again when the file
changes.

### Does Rabbit push or merge on its own?

No. It pushes only after you answer the push question, and it never merges. It
never force-pushes or rewrites history.

### Will it touch my uncommitted work?

No. Rabbit reads code from the base branch, not your checkout, and writes code
only in separate worktrees under `<repo>/.claude/worktrees/`. Your main
checkout's branch and files stay as they are.

### Where does my data go?

Rabbit is a set of instructions for Claude Code; it has no server of its own. It
reads Jira through the MCP server you connected and your code on your machine,
and Claude processes them like any other Claude Code session. Its documents stay
in your workspace, and Integration only talks to services on your machine.

### Can I use it without Claude Desktop?

Only `/rabbit:setup` works in a terminal. Pulling, tasks and dev sessions open
new sessions, which only Claude Desktop can do.

### Does it work on Windows and Linux?

Yes. Windows needs Git for Windows and Python 3; Claude Desktop for Linux is in
beta. See [Installation](installation.md#your-operating-system).

### Does it work with Jira Server, GitLab or Bitbucket?

Rabbit is built and tested for **Jira Cloud**. Another Jira works if its MCP
server offers the same operations (search issues and read an issue), and Jira
Server/Data Center sprint fields are recognized, but that is less tested. With
GitLab or Bitbucket, Rabbit pushes the branch and you open the merge request
yourself.

### Do I need superpowers?

No. With superpowers, specs, plans and implementation use its skills, which ask
more questions and go deeper. Without it, Rabbit uses its own guides. You can
choose per stage in your [workflow
file](customizing.md#always-use-superpowers-or-never).

### What if I am in more than one sprint?

`/rabbit:pull` lists the active sprints and asks which one to pull. Pull each in
its own session if you want both.

### What about sub-tasks and epics?

A sub-task assigned to you in the sprint gets its own task like any other issue.
While reading a task, Rabbit reads its parent's summary and description, and
lists linked issues and sub-tasks; it reads one in full only when the task
depends on it.

### Can I talk in one language and write documents in another?

Yes. `Chat language` and `Document language` are separate settings in your
[profile](profile.md). Code, commits and pull requests stay in English unless
the repository says otherwise.

### Can I edit the brief, spec or plan myself?

Better to tell the task session what to change: it keeps the spec and plan in
agreement, runs the review again and asks for approval. If you edit a file by
hand, tell the task session so it reads it again.

### Can I close the task session while dev sessions work?

Keep it open. Dev sessions report to it, and it runs Integration when they are
done. If you closed it, open it again: it resumes from `jira.md`.

### How do I clean up after a task?

Archive the task's sessions, remove its worktrees and delete merged branches.
See [Finish the task](first-task.md#9-finish-the-task).
