# Blind review

Before a brief, spec or plan reaches the user, in a dev session on its own diff
before it sends `rabbit: done`, and in the Integration stage, run the
`rabbit:observer` agent (`Agent` tool, `subagent_type: "rabbit:observer"`). Give
it only:

```
Kind: <brief | spec | plan | diff | integration>
Task: <KEY>
Document: <absolute path; none for diff and integration>
Builds on: <absolute paths: none for a brief; the brief for a spec; brief and spec for a
  plan; brief, spec and plan for a diff; brief and spec for integration>
Repositories: <absolute path and base branch of each (for a brief, those it cites; none
  before any is known) and, for diff and integration, the branch of each>
Impact: <absolute path of impact.md, for integration; else none>
Tracker: <Site and Tools from the profile>
Workflow review rules: <the instructions under the workflow file's `## Review`, or none>
Language: <DOC_LANG>
Lens: <below>
```

Never the conversation, your reasoning or an earlier round. Apply the workflow's
`## Review:Before` before each run and `## Review:After` after each verdict.

Lens:
- brief: "every fact is correct and sourced; the brief points the reader to the
  right place"
- spec: "every claim and code fact is true on the base branch; following the
  spec works end to end; the tracker's acceptance criteria and the user's
  directions are met; nothing simpler meets every acceptance criterion; a
  developer who never saw the conversation can implement it from this document
  alone; every change has an example; no text the implementer does not need; no
  consumer that does not change breaks"
- plan: "the plan matches the spec, covers all of it and nothing more; every
  task is implementable as written; every Scenarios row has a test; a developer
  who never saw the conversation can implement it from this document alone; no
  text the implementer does not need"
- diff: "every plan step is implemented correctly; the tests prove the
  behaviour"
- integration: "the acceptance criteria hold across the repositories as a whole;
  fields, enum values, endpoints and queue names match between repositories; no
  consumer in the impact list breaks; no consumer that does not change breaks"

## Findings

The observer returns findings as `### R<n> · <critical|major|minor> · <title>`
blocks with Problem, Evidence, Solution and an optional Before / After, then
`Unverified:`,
`Follow-ups:` and `VERDICT`. For each finding:
1. **Prove it.** Open its Evidence yourself or run its command. A finding you
   cannot reproduce, and everything under `Unverified:`, is not a finding: it
   goes to the review file's `## Not proven` with a one-line reason.
2. **It has a solution.** A `minor` finding without a concrete in-scope Solution
   is rejected. A proven `critical` or `major` one whose Solution is `none in
   scope` is shown to the user with its evidence, and you ask how to go on.
3. **Out of scope** (`Follow-ups:`): before the spec is approved, add it to the
   spec's follow-up tasks; after that, to the review file's `## Follow-ups`. An
   approved spec is not changed for it.
4. **Fix** every `critical` and `major` finding. Fix a `minor` one only when the
   fix is one small change; otherwise it stays `open`. A `minor` finding never
   stops a stage.

## Review file

This session writes every review to `TASK_DIR/reviews/<kind>.md`
(`diff-<repo>.md` for a diff), in `DOC_LANG`: `# <Kind> review`, then `## Round
<n>` with each proven finding as returned plus `**Status:** fixed (<commit or
section>) | open | rejected (<one-line reason>)`, then one summary line (`2
fixed, 1 open, 1 rejected, 2 not proven`), `## Not proven` and `## Follow-ups`
when there are any. A second round is appended to the same file. A dev session
reviews its own diff and sends its proven findings and follow-ups in `rabbit:
done`; write them to `diff-<repo>.md`.

## Rounds

1. One review round.
2. Prove and sort the findings as above.
3. A `critical` or `major` finding fixed: run one short round with the same
   inputs plus `Verify these findings were fixed, and review only what the fixes
   changed:` and the list of those findings only. Fixed `minor` findings open
   no round.
4. No `critical` or `major` finding fixed: the review is done.
5. At most 3 observer rounds per document in all. Findings left after that:
   show them to the user and ask how to go on.

## Changes

A reviewed or approved document changes (a finding's fix after approval, the
user's request, a change after dev sessions started). Sort the change first:

| Change | Example | Review | New approval |
| --- | --- | --- | --- |
| Critical | design, acceptance criterion, contract, repository list, data model | one round on the changed sections (`Review only these changed sections:` and their headings) | yes |
| Not critical | wording, a name, dropping an impossible test case, mechanical fit to the repository's rules | none | no |

- Unsure counts as critical.
- Not critical: append `No review needed: <reason>` (in `DOC_LANG`) to
  `reviews/<kind>.md` and tell the user in one line.
- A change the user asked for is approved by their request, even a critical
  one; ask again only for a critical change Rabbit made itself.
- No new approval needed: append the `Approved:` line right after `Changed:`.

The document never mentions the review. Tell the user in one line how many
rounds ran, the summary line and a link to the review file: that line is
`{{review_line}}`.
