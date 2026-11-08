# Integration

Runs in the task session after every dev session has sent `rabbit: done`, before
the push question, for one repository or many. It proves the change works end to
end against the spec's `## Scenarios` and that no consumer breaks. Apply the
workflow's `## Integration:Before`, `## Integration` and `## Integration:After`
instructions at their points, and `WF.environment` at every step that runs
something. This session runs the applications under rules.md's **Running the
app or its tests**; it never edits code, and a setting it changes for a test is
restored when the test ends. Only this session writes `integration.md`; it adds
the `Env:` lines the dev sessions send to its environment log.

1. **Refresh the impact list.** Re-run the impact search (discovery.md) against
   each changing repository's branch instead of its base (`git -C <repo> grep
   -l -e <term>
   <branch> -- .`; a **read** repository stays on its base) and update
   `TASK_DIR/impact.md`. A break in a consumer repository that does not change:
   send `ask.add-repo` and wait. A new consumer becomes a row of the
   table below with `Criterion` = `impact`; the approved spec is not changed for
   it.
2. **Blind review.** Run the observer with `Kind: integration` (review.md):
   every changing repository with its base and branch, brief and spec,
   `Impact:` = `impact.md`.
3. **Contract tests.** Ask each consumer repository's dev session to run its
   contract tests (`rabbit: run <test command>`); each answers `rabbit: result`.
   A **read** consumer has no dev session: its contract tests live in the
   producer repository (plan-guide.md). A producer → consumer pair with no
   contract test in the plan: show the plan task to add and ask; on yes add it
   to `plan.md`, send that dev session `rabbit: fix add contract test:
   <plan task>` (it answers `rabbit: done`), and say so in the report. Ask each
   dev session to run the tests the plan links to the Scenarios rows (`rabbit:
   run`). Then, unless an Integration instruction says otherwise, ask
   each changing repository's dev session to run its full test suite once
   (`rabbit: run`), with the command from its `CLAUDE.md`, README or CI config;
   none found: send
   `ask.suite-command`. Its result is a row with `Criterion` = `suite`.
4. **Repository kind.** `frontend`, `backend`, `monolith` or `library` (no app
   to start:
   steps 6 and 7 are skipped and its rows rest on the tests), from the
   repository's own files: its `CLAUDE.md`, package files (for example a
   dev-server script in
   `package.json`, `composer.json` with `artisan`, `manage.py`, a server entry
   point) and compose services. Unclear: ask.
5. **Setup and safety.** For each changing repository, in its worktree, apply
   rules.md's **Running the app or its tests** (setup first, then safety on the
   files the process would load) before starting anything. No sign-in source
   in `WF.environment` or in seed, fixture or example config files: the rows
   that need it are `unverified`.
6. **Run it.**
   - The start command comes from its `CLAUDE.md`, then README, then compose,
     then package scripts. None: send `ask.run-command` once and suggest adding
     the answer to the repository's `CLAUDE.md`. Start servers with Bash in the
     background.
   - A port already in use (an app running from the main checkout): pass another
     port; if the app cannot take one, ask.
7. **Try each scenario.**
   - `backend`: real HTTP requests to the local app; for a queue or job, run the
     job and check its effect (a database row, a published message).
   - `frontend`: open the local dev server with the session's browser tool and
     follow the scenario's steps. With a changing backend, point the frontend at
     its running worktree (by environment variable); if that backend was not
     started, the rows that need it are `unverified` with its Reason and To
     pass. Otherwise the backend the repository's local config names, only if it
     is local. No browser tool: `unverified`.
   - `monolith`: both.
8. **Fix.** A `failed` scenario, a confirmed finding or a failing test goes to
   the dev session of its repository (`rabbit: fix <scenario or finding>`); when
   it reports `rabbit: done`, try the scenario again, run step 3's scenario and
   contract tests again (the full suite once more after the last round) and step
   2's verify round (review.md). At most 2 rounds; what still fails after them
   is reported `failed` with its Reason and To pass, and the stage goes on to
   the report.
9. **Report.** Write each record, file or message this stage creates to
   `TASK_DIR/integration.md` as soon as it exists, so cleanup survives a
   restart. Then complete `integration.md` in `DOC_LANG`: the table, the test
   data this stage created (each record, file or message, with how it was
   created), the review summary and an `## Environment log` section (heading
   in `DOC_LANG`): one line per environment step, saying what was done,
   restored, missing and completed, or could not be completed (for example
   `.env` `RATE_LIMIT_ENABLED=false` → test → restored). Send
   `integration.report` with the counts as its summary (`3 passed, 1 failed,
   1 unverified`) and the table:

```markdown
| # | Scenario | Criterion | Result | Evidence | Reason | To pass |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | A signed-in user saves a campaign | AC1 | passed | `POST /campaigns` → 201, row id=42 | | |
| S2 | Save with an empty name | AC2 | failed | 500, `null` error | no validation | `required` rule in `CampaignRequest` |
| S3 | External service timeout | AC3 | unverified | service not available locally | no sandbox | manual test in a test environment |
```

   `Result` is what step 7's real run showed; the tests of step 3 go in
   `Evidence`.
   Contract rows (`Criterion` = `contract`) take the contract tests' result. A
   `failed` or `unverified` row always has `Reason` and `To pass`. Nothing that
   did not run is reported as passed, and the change is never called working
   unless every row passed.

   **Cleanup.** Settings changed for a test are already restored; they do not
   wait for this question. No test data created: stop every process this stage
   started.
   Otherwise send `ask.cleanup` with the list in the same message, append
   `Cleanup: asked <date>` to `jira.md` and end the turn, leaving the apps
   running. Yes: remove only those items, the way each was created in reverse (a
   `DELETE` request, the app's own command), never a bulk delete or a database
   reset; then mark each in `integration.md` as removed or, with the reason, not
   removed. No: mark them kept. Append `Cleanup: <removed|kept> <date>`, then
   stop every process this stage started (after a restart, start them again
   first for a yes).
10. Add `Integration: <passed|failed|unverified> <date>` to `jira.md`'s status
    lines: the worst result of any row (failed, then unverified, then passed).
    Then go to SKILL.md step 8 (publish.md), whose push question is
    `ask.push-anyway` when not every row passed.
