## Environment

- Before running the app, check that the cloud credentials work (for example
  `aws sts get-caller-identity`); when they don't, ask me to refresh them as a
  blocker, then check again.
- Create new test data for each scenario, named with the task key, and list it
  in the environment log.

## Brief

If an error tracker is connected, check every error the task mentions in it; if
a monitoring tool is connected, check the related metrics and logs too.

## Plan:After

- Move the issue to `In Progress` using a transition the issue's
  own workflow offers.
- Add a comment to the issue with the spec's goal and acceptance criteria.

## Review

- Spec, plan and code: every acceptance criterion is met by a change and proven
  by a test.
- Spec, plan and code: nothing outside the criteria changes.
- No security regression: input validation, authorization, no secrets or
  personal data in logs.
- Existing callers keep working: response shapes, events, database schema and
  config stay backward compatible, or the break is in the spec.

## Execute

Use superpowers (`superpowers:executing-plans`).

## Integration

If an impact analysis or code search tool is connected, use it on each changing
repository's branch to check who uses the changed contracts.

## Push:Before

Ask each dev session to run the linter on the changed files. Never format the
whole project.

## Push

Start each pull request title with `<KEY>`.

## Push:After

- Move the issue to `In Review`.
- Ask whether to test the `unverified` rows of `<TASK_DIR>/integration.md` on
  <environment>.
