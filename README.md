<p align="center">
  <img src="docs/assets/logo.svg#gh-light-mode-only" width="360" alt="Rabbit">
  <img src="docs/assets/logo-dark.svg#gh-dark-mode-only" width="360" alt="Rabbit">
</p>

<p align="center">
<a href="https://github.com/mayoz/rabbit/actions/workflows/ci.yml"><img src="https://github.com/mayoz/rabbit/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="https://github.com/mayoz/rabbit/releases"><img src="https://img.shields.io/github/v/release/mayoz/rabbit" alt="Latest release"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license"></a>
</p>

## Introduction

Rabbit is a [Claude Code](https://claude.com/claude-code) plugin that takes your
Jira sprint from ticket to pull request in Claude Desktop.

It pulls the tasks assigned to you, gives each one its own session, and walks
every task through the same steps: a one-page brief, a spec and a plan you
approve, code written step by step with a test and a commit for each step, an
end-to-end check of the whole change, and the push. A reviewer that never sees
your conversation checks every document and every diff before you do.

Rabbit reads Jira and writes to it only when your workflow file says so, after
you approve it. It never pushes without your
yes and never changes your main checkout's branch or files.

## Installation

> [!IMPORTANT]
> Rabbit runs only in the Claude Desktop app for now. Its commands open sessions
> and change folders with Desktop tools, so in the Claude Code CLI they stop
> with a message. CLI support is planned for a later release.

You need Claude Desktop and the Claude Code CLI, Jira connected through an MCP
server, git and Python 3; opening pull requests also needs the GitHub CLI. See
[Installation](docs/installation.md) for the details on macOS, Windows and
Linux.

```bash
claude plugin marketplace add mayoz/rabbit
```

```bash
claude plugin install rabbit@mayoz
```

Updates don't install on their own; see
[Update](docs/installation.md#update) to turn on auto-update.

Then start a new session in Claude Desktop's **Code** tab and run setup. It asks
five short questions and finds your Jira settings on its own:

```
/rabbit:setup
```

## Usage

Pull your sprint in a new Desktop session:

```
/rabbit:pull
```

Rabbit opens one session per unfinished task. Open one: it has already written a
brief and asks which repositories to work in. From there it writes a spec and a
plan, opens a dev session per repository once you approve the plan, checks the
whole change end to end and asks before it pushes.

| Command | Where | What it does |
| --- | --- | --- |
| `/rabbit:setup` | anywhere | Writes or checks your profile. |
| `/rabbit:pull` | a new Desktop session | Pulls the active sprint. Run it again to add new tasks. |
| `/rabbit:task [KEY \| URL]` | a task session, or any session with a key | Brief → spec → plan → dev sessions → integration → push. |
| `/rabbit:dev` | started for you | Implements one repository's part of the plan. |

[Getting started](docs/getting-started.md) and [Your first
task](docs/first-task.md) walk you through it.

## Customizing

Rabbit works out of the box. To make it follow your team's way of working, write
a **workflow file**: plain instructions under a heading per stage.

```markdown
## Plan:After

Move the issue to In Progress.

## Integration

Skip the full test suite.

## Push

Start each pull request title with `<KEY>`.
```

[Customizing Rabbit](docs/customizing.md) shows how, with ready-made recipes.

## Documentation

The [documentation](docs/index.md) covers installation, your first task,
customizing, the profile and workflow file references, concepts, how Rabbit
works, token usage, an FAQ and troubleshooting.

## Contributing

Thank you for considering contributing to Rabbit! The contribution guide can be
found in [CONTRIBUTING.md](CONTRIBUTING.md).

## Code of Conduct

To keep Rabbit welcoming to everyone, please review and abide by the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Security Vulnerabilities

Please review [our security policy](SECURITY.md) on how to report security
vulnerabilities.

## License

Rabbit is open-sourced software licensed under the [MIT license](LICENSE).
