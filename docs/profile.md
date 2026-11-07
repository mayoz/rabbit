# Your Rabbit profile

Rabbit keeps your personal settings in one Markdown file on your machine:

```
~/.config/rabbit/profile.md
```

`/rabbit:setup` writes it for you. You can also open it in any editor and change
a line; every Rabbit command reads the file again each time it runs, so there is
nothing to reload.

- [How the file is laid out](#how-the-file-is-laid-out)
- [Basics](#basics-required-asked-by-setup)
- [Tracker](#tracker-required-found-by-setup)
- [Checking your profile](#checking-your-profile)
- [Examples](#examples)

> **This file never goes into a repository.** It names your tracker site and
> your folders. Keep it local. How you or your team work (tools, specs, pushes)
> goes in a [workflow file](workflow.md) instead.

## How the file is laid out

```markdown
# Profile

Workflow: ~/rabbit/rabbit-workflow.md

## Basics
- Workspace: ~/rabbit/sprints
- Repositories folder: ~/code
- Chat language: English
- Document language: English

## Tracker
- Site: https://acme.atlassian.net
- Tools: Atlassian MCP (searchJiraIssuesUsingJql, getJiraIssue, getJiraIssueRemoteIssueLinks)
- Sprint field: customfield_<id>
```

- `Workflow:` is optional. It points at your [workflow file](workflow.md).
- Each section is a `##` heading followed by `- Key: value` lines.

## Basics (required, asked by setup)

| Key | What it is for | Example | Default |
| --- | --- | --- | --- |
| `Workspace` | Where Rabbit creates one folder per sprint (`SP_<sprint-id>/`) and one per task inside it. | `~/rabbit/sprints` | `~/rabbit/sprints` |
| `Repositories folder` | The folder that holds your git clones. Rabbit finds a repository by name here or one level deeper (`~/code/acme/web-app`). | `~/code` | `~/code` |
| `Chat language` | The language Rabbit talks to you in. `auto` follows the language you write in. | `English`, `Turkish`, `auto` | `English` |
| `Document language` | The language of the brief, spec, plan and reports Rabbit writes. `auto` uses the chat language. | `English`, `Turkish`, `auto` | `English` |

## Tracker (required, found by setup)

Setup fills this section itself. It asks only when more than one Jira connection
or site is available.

| Key | What it is for | Example |
| --- | --- | --- |
| `Site` | Your Jira Cloud address, read from the Jira tools. | `https://acme.atlassian.net` |
| `Tools` | The MCP tools Rabbit calls to read Jira. Any server that offers the same operations works. | `Atlassian MCP (searchJiraIssuesUsingJql, getJiraIssue, getJiraIssueRemoteIssueLinks)` |
| `Sprint field` | The Jira field that holds an issue's sprints. Needed by `/rabbit:pull`; `/rabbit:task <KEY>` works without it. | `customfield_<id>` |

Rabbit never writes to Jira on its own; it writes only when your workflow file
says so.

## Checking your profile

Run `/rabbit:setup` when a profile already exists. It shows your settings in a
table and checks each one: the folders exist, the Jira tools are available, the
sprint field is set and the workflow file can be read. Then it offers **Set up
again**, which asks every question with your current values as the first
choices, or **Cancel**, which changes nothing.

## Examples

See [examples/profiles](../examples/profiles): `minimal.md` has no workflow file
and `personal.md` points at one. [examples/workflows](../examples/workflows) has
a workflow file.
