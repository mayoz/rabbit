# Installation

This page lists what Rabbit needs and how to install, update and remove it. It
takes about five minutes.

- [Requirements](#requirements)
- [1. Connect Jira](#1-connect-jira)
- [2. Install Rabbit](#2-install-rabbit)
- [3. Install superpowers (optional)](#3-install-superpowers-optional)
- [4. Check the installation](#4-check-the-installation)
- [Update](#update)
- [Uninstall](#uninstall)

## Requirements

| You need | Why | How to check |
| --- | --- | --- |
| **Claude Desktop** with the **Code** tab | `pull`, `task` and `dev` open new sessions, which only Desktop can do. `setup` also works in the terminal. | Open Desktop and look for the Code tab. |
| **Claude Code** in a terminal | To install the plugin. | `claude --version` |
| **Jira** (Cloud; Server and Data Center are less tested) and an MCP server for it | Rabbit reads your sprint and issues through it. | See [step 1](#1-connect-jira). |
| **git** | Branches, worktrees and commits. | `git --version` |
| **Python 3** | Two small helper scripts and two hooks. | `python3 --version` (or `python --version`) |
| **GitHub** and the [GitHub CLI](https://cli.github.com) | Only to open and link pull requests and follow CI. | `gh auth status` |

Without GitHub (GitLab, Bitbucket), Rabbit still pushes the branch; you open the
merge request yourself.

To check a frontend change in a browser, the task session needs a browser tool,
such as Claude Desktop's built-in browser or the Claude in Chrome extension.
Without one, frontend scenarios are reported as `unverified` with the reason.

### Your operating system

| | What to install |
| --- | --- |
| **macOS** | Python 3 comes with the Xcode command line tools (`xcode-select --install`) or from [python.org](https://www.python.org/downloads/). |
| **Windows** | [Git for Windows](https://git-scm.com/download/win), which gives Claude Code its Bash shell, and Python 3 from [python.org](https://www.python.org/downloads/) with "Add python.exe to PATH" ticked. Rabbit uses `python` when there is no `python3`. |
| **Linux** | `git` and `python3` from your package manager. Claude Desktop for Linux is in beta. |

Rabbit needs Desktop's session tools, so run Desktop on the machine itself, not
in WSL or a cloud session.

## 1. Connect Jira

Rabbit reads Jira through an MCP server. If you have never connected one, add
Atlassian's in a terminal:

```bash
claude mcp add --scope user --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

Open a new session in Claude Desktop. The first time a Jira tool runs, Claude
asks you to sign in to Atlassian in your browser. Any other Jira MCP server
works too, as long as it can search issues and read an issue, including a Jira
connector added in Claude Desktop's settings. Setup finds its tools on its own.

## 2. Install Rabbit

Add the marketplace, then install the plugin:

```bash
claude plugin marketplace add mayoz/rabbit
```

```bash
claude plugin install rabbit@mayoz
```

## 3. Install superpowers (optional)

[superpowers](https://github.com/obra/superpowers) adds deeper skills for
writing specs and plans and for implementing them. Rabbit uses them when they
are installed and asks you which to use when it matters. Rabbit works fine
without them.

```bash
claude plugin install superpowers@claude-plugins-official
```

## 4. Check the installation

Start a **new** Desktop session, so the plugins load, and type `/rabbit`. You
should see `/rabbit:setup`, `/rabbit:pull`, `/rabbit:task` and `/rabbit:dev`. If
you don't, see [Troubleshooting](troubleshooting.md).

Next: [Getting started](getting-started.md).

## Update

Plugins from a third-party marketplace do not update on their own. To get the
latest version:

```bash
claude plugin update rabbit@mayoz
```

Start a new session afterwards. Your profile, workflow file and sprint folders
are kept. [CHANGELOG.md](../CHANGELOG.md) lists what changed.

## Uninstall

```bash
claude plugin uninstall rabbit@mayoz
```

```bash
claude plugin marketplace remove mayoz
```

Rabbit leaves your own files alone. Delete them yourself if you no longer need
them:

- your profile, `~/.config/rabbit/` (it also holds `approved-workflow.md`);
- your workspace, the folder that holds your sprint folders, for example
  `~/rabbit/sprints`;
- worktrees and branches Rabbit created in your repositories (see
  [Finish a task](first-task.md#9-finish-the-task)).
