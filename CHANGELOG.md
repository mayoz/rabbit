# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-08

### Added
- A workflow `## Environment` heading: how to set up and run apps and tests,
  where sign-in data comes from, how to check and refresh credentials, and
  when to stop. Task and dev sessions read it whenever they run something.
- An environment log in `integration.md`, and a "Done, try again" question for
  the few things only you can do (a browser sign-in, `sudo`, a closed test
  environment).
- Word targets for the brief, the spec and the plan.
- Hook reminders: Integration that has not run yet, and questions still
  waiting for an answer; the language reminder also follows subagent reports.
  A status line an answer writes (`Approved:`, `Cleanup:`, `Push:`, `CI:`)
  counts as that answer.
- The push question shows each repository's branch and base in a table.
- Checks that wait for a later step: name them under `## Push` and CI is
  followed without them, so `## Push:After` (for example a QA hand-off) can
  run. `ci_wait.py` watches the other checks.
- Dev sessions ask for blockers with the same "Done, try again" question.

### Changed
- Every closed question has buttons, the recommended answer first, after a
  short box saying what is needed, why, and what each answer does. A question
  interrupted by another request is asked again.
- Approvals stay one at a time, and reviews are lighter: one round, a second
  only for fixed critical or major findings, at most three per document. A
  later change is sorted first; only a critical change gets a review and a new
  approval.
- Worktree setup, a setting changed for one test, and new test data named with
  the task key no longer ask. After Integration one question asks whether to
  keep or remove the test data.
- Integration always runs after the last repository is done, and there is no
  push question before it.
- A change you ask for after an approval counts as approved; Rabbit asks again
  only for a critical change it makes itself.
- The setup questions use buttons too.
- The observer writes its findings in the document language.
- `impact.md` and the spec list only surfaces that cross repositories; with
  none they say so in one line.
- Shorter Scenarios: cases with the same result share one row.

### Removed
- The `continue` and `yes native` answers, and the question before installing
  a worktree's dependencies.

## [0.0.2] - 2026-11-08

### Changed
- Every spec and plan approval question, including the ones after a change,
  links the document and its review file.
- Each prompt in a Rabbit session reminds it of the profile's chat and document
  languages, and the skills keep every message in the chat language after a
  subagent report or tool result in another language.
- `impact.md` lists only surfaces the change alters that cross a repository
  boundary, defines the producer as the serving side, and no longer counts tests
  as consumers.

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

[0.0.1]: https://github.com/mayoz/rabbit/releases/tag/v0.0.1
