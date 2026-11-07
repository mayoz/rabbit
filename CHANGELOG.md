# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.0.1] - 2026-11-07

### Added
- `/rabbit:setup` writes `~/.config/rabbit/profile.md` one question at a time,
  finds the Jira tools, site and sprint field itself, and checks an existing
  profile.
- `/rabbit:pull` makes one sprint session with one folder and one task session
  per unfinished task, writes `summary.md`, and on a later run adds only what is
  new.
- `/rabbit:task` takes one task from a sourced brief through a spec and a plan,
  each blind reviewed and approved by you, to one dev session per changing
  repository.
- `/rabbit:dev` implements one repository's part, one commit per step, reviews
  its own diff, and pushes only when the task session says so.
- The `rabbit:observer` agent reviews briefs, specs, plans, diffs and
  integrations without the conversation; every finding is `critical`, `major` or
  `minor` with its evidence and solution, and only proven findings are acted on.
  A hook limits it to reading tools, read-only commands and MCP tools whose
  names read like a read; without Python 3 it blocks the observer entirely.
- Integration checks the impact list, runs contract tests and each repository's
  full test suite, starts the applications against local services only and tries
  every spec scenario; each row is `passed`, `failed` or `unverified` with its
  reason and what would make it pass. Test data it created is listed, and
  removed on your yes.
- Push asks once for ready or draft pull requests, links them, follows CI on
  request and ends with a pull request table.
- An optional workflow file adds your own instructions per stage; instructions
  that act outside your machine run only after you approve the file.
- A session-start hook reloads the task or dev skill after a compaction or
  resume.
- Runs on macOS, Windows and Linux; the helper scripts and hooks are Python 3
  with the standard library only.

[0.0.1]: https://github.com/mayoz/rabbit/releases/tag/rabbit--v0.0.1
