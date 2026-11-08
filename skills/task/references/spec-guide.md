# spec.md (built-in method)

Write `spec.md` in `DOC_LANG` from `brief.md`, `jira.md` and the user's answers.

Writing rules (both methods; `SKILL.md` passes them to superpowers too):
1. Every section answers **what** changes and **how** it changes.
2. Every change has an example: code before and after, a request and its
   response, or a data row before and after.
3. Say each thing once. Leave out background that changes no decision of the
   implementer.
4. Short sentences. Define each term once and always use the same name for it.
5. The document stands alone: a developer who never saw this conversation or
   this machine can implement it. No "as discussed", no absolute paths outside a
   repository; repository `path:line` references stay.
6. A contract that a consumer which does not change in this task reads (a field,
   endpoint, event, table or config key) changes only backward compatibly: add
   the field and keep the old one, give a default, or accept both forms. Show
   how with an example.
7. A break is allowed only when the spec says what breaks and why, under
   `## Impact and contracts`, in a line starting `Breaking:`.

Sections, headings translated:
1. `## Goal`: what is wanted and why, 2–4 sentences with sources.
2. `## Acceptance criteria`: numbered (`AC1`, `AC2`, …), each with its source.
3. `## Design`: the simplest design that meets every criterion; alternatives one
   line each with why they lost.
4. One `## <repo>` section per **changes** repository: each change as a short
   sketch in the repository's own style (signatures, changed lines, payload
   JSON, SQL, route) next to the existing code it follows (`path:line`), plus
   the names and assertions of the tests that prove it. Sketches, not the
   finished code: signatures and changed lines, never a full body.
5. `## Impact and contracts`: every producer → consumer pair from `impact.md`,
   with the exact contract (payload, endpoint, field, table) and whether the
   consumer changes. For a consumer that does not change: how the change stays
   compatible (rule 6), before and after. Only pairs across repositories;
   none: the one line "No cross-repository impact." in `DOC_LANG`.
6. `## Scenarios`: for every acceptance criterion the main flow and each case
   that behaves differently from it. Consider edge cases (empty, null, zero,
   very large, duplicate), invalid input, permissions, data written before the
   change and a failure of every service the change calls; cases with the same
   result share one row:

```markdown
| # | Scenario | Criterion | Expected |
| --- | --- | --- | --- |
| S1 | A signed-in user saves a campaign | AC1 | 201, the row exists |
| S2 | Save with an empty name | AC2 | 422, `name` is required |
```

   Contract pairs get rows with `Criterion` = `contract`.
7. `## Follow-up tasks`: drafts from Discovery, or `None`.

Ask only questions rules.md allows; skip anything `jira.md`, `brief.md` or the
answers settle.
