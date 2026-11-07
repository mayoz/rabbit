# plan.md (built-in method)

Write `plan.md` in `DOC_LANG` from the approved spec, following the writing
rules 1–5 of `spec-guide.md`. Do not repeat the spec: point to its section.
Tasks grouped by repository; note the order between repositories where one
depends on another (ask when the merge or deploy order is not stated anywhere).

Each task:
- **Files:** exact paths to create or change.
- **Steps:** one action each with a checkable result: write the failing test
  (its name and assertions), run it (command, expected failure), implement
  (exact signature and the values the spec pins), run it again (expected pass),
  commit (message).
  The commit message follows the repository's `CLAUDE.md` or `.claude/rules/`,
  else the style of `git log -20 --format=%s origin/<base>`.
- **Done when:** the command and the output that prove it.

Every row of the spec's `## Scenarios` gets the test that proves it, as a line
`S<n> → <path>::<test>` in the task that writes the test.

For every producer → consumer pair between changing repositories, add a
contract-test task in the consumer repository: a fixture taken from the
producer's real output (serialized from its code or its test), fed to the
consumer's real code, with a positive case and negative cases (missing field,
unexpected value) from the acceptance criteria. Record the task in `impact.md`'s
`Contract test` column. For a consumer that does not change, add a test in the
producer repository: the consumer's current input still works with the new
output.

No test setup for the code a task touches: say so in the plan as an open
question with your recommendation (the framework's default test setup); never
add one silently.

A step is done when the implementer can write exactly one reasonable thing from
it. No "handle edge cases", "add validation" or "TBD".
