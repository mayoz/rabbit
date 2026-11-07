# Discovery and impact

Runs while the spec is written. Find what the change touches beyond the listed
repositories and write the impact list. Keep the token budget small.

## Impact list

1. List every surface the change alters: HTTP endpoint and response shape, queue
   or event payload, database table and column, config or env key, exported
   function or class.
2. Find each surface's consumers (and producers, for what the task reads):
   - If the workflow's `## Brief` or `## Integration` names a code-search tool,
     use it first. Its results are leads, not proof.
   - Search the changing repositories and the other clones under the
     Repositories folder on their base branch: `git -C <repo> grep -l -e <term>
     origin/<base> -- .` (file names only). Read at most **3 files per
     consumer** and **8 files** in total. Never read the same file twice; cite
     each as `path:line`. A consumer left unread by these limits gets its row
     with `unverified (limit reached)` and becomes an open question.
3. Write `TASK_DIR/impact.md` in `DOC_LANG`:

```markdown
| Surface | Kind | Producer | Consumers (path:line) | Contract test |
| --- | --- | --- | --- | --- |
```

`Kind` is one of `endpoint`, `payload`, `db`, `config`, `symbol`. `Contract
test` names the plan task that adds the test, or `none (<reason>)`.

## Findings

Verify each finding (rules.md), then put it under the open questions with its
evidence and these options:
- Local repository: `add as changes` · `add as read` · `follow-up task` · `not
  needed`.
- Not cloned: say so; `follow-up task` · `not needed`.

`follow-up task`: add a tracker-ready draft (title, description, acceptance
criteria) to the spec's follow-up section; the user opens the ticket. `not
needed`: note the user's reason in the spec and do not raise it again. A finding
you could not verify is reported as such, never as a proposal.
