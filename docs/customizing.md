# Customizing Rabbit

Rabbit works out of the box. When you want it to work your team's way, you have
three places to say so:

| Place | What goes there | Who it applies to |
| --- | --- | --- |
| [Your profile](profile.md) | Folders, languages, Jira connection. | You, on this machine. |
| A **workflow file** | How you work at each stage: tools, checks, tracker updates, pull request rules. | You, or your whole team if you share it. |
| A repository's `CLAUDE.md` | Facts about one repository: base branch, branch names, start and test commands. | Everyone working in that repository. |

When they disagree, the repository's `CLAUDE.md` wins, then the workflow file,
then Rabbit's defaults.

- [Your first workflow file](#your-first-workflow-file)
- [Recipes](#recipes)
- [Repository facts in CLAUDE.md](#repository-facts-in-claudemd)
- [Sharing with your team](#sharing-with-your-team)

## Your first workflow file

A workflow file is a Markdown file. Each `##` heading names a stage of a task,
and the lines under it are plain instructions, the way you would tell a
colleague.

1. Create a file, for example `~/rabbit/rabbit-workflow.md`:

   ```markdown
   ## Push

   Start each pull request title with `<KEY>`.
   ```

2. Run `/rabbit:setup`, choose **Set up again**, and give the file's path when
   it asks about a workflow file. Or add this line to the top of
   `~/.config/rabbit/profile.md`:

   ```markdown
   Workflow: ~/rabbit/rabbit-workflow.md
   ```

3. Your next task uses it. `<KEY>` becomes the task's key, for example
   `ABC-123`.

Run `/rabbit:setup` after editing the file: it lists any heading Rabbit does not
recognize. [Your workflow file](workflow.md) lists every stage and rule. A
complete example is in
[examples/workflows/rabbit-workflow.md](../examples/workflows/rabbit-workflow.md).

## Recipes

Copy the parts you need into your workflow file.

### Move the issue when work starts and ends

```markdown
## Plan:After

Move the issue to In Progress, using a transition the issue's own workflow offers.

## Push:After

Move the issue to In Review.
```

Rabbit never writes to Jira unless you say so like this. The first time such an
instruction is about to run, Rabbit shows you every instruction that acts
outside your machine and asks once. It asks again only when the file changes.

### Attach the spec and plan to the issue

This needs a Jira tool that can upload attachments; Atlassian's own MCP server
has none.

```markdown
## Plan:After

Upload `spec.md` and `plan.md` to the issue as attachments.
```

### Check your error tracker while writing the brief

```markdown
## Brief

Check every error the task mentions in the error tracker, and the related logs and metrics
in the monitoring tool.
```

Name the tools as they appear in your Claude session; Rabbit uses the ones
connected there.

### Always use superpowers, or never

```markdown
## Spec and Plan

Use superpowers.

## Execute

Use superpowers.
```

Write `Use native.` under `## Execute` for Rabbit's own step-by-step loop, and
`Write the spec and plan without superpowers.` under `## Spec and Plan` for
small tasks.

### Run only the affected tests instead of the full suite

Integration runs each repository's full test suite once. For large repositories
that is slow; CI runs it anyway.

```markdown
## Integration

Skip the full test suite. Instead, in each changing repository run only the tests the change
affects: the tests of every changed file, and the integration tests that reach the changed
code through its callers, routes, jobs or events. Run the full suite only when I ask for it.
```

### Run the linter before pushing

```markdown
## Push:Before

Ask each dev session to run the linter on the changed files. Never format the whole project.
```

### Add your own review rules

```markdown
## Review

- No secrets or personal data in logs.
- Every acceptance criterion is proven by a test.
```

These are added to every blind review. They can't turn the review off.

### Ask for a value when it is needed

Any word in angle brackets that Rabbit doesn't fill itself is a **placeholder**.
Rabbit asks you for it the first time it is needed and remembers the answer for
the rest of the task.

```markdown
## Push:After

Ask whether to test the `unverified` rows of `<TASK_DIR>/integration.md` on <environment>.
```

Rabbit fills `<KEY>`, `<SUMMARY>`, `<REPO>`, `<BRANCH>`, `<BASE>` and
`<TASK_DIR>` itself.

## Repository facts in CLAUDE.md

Some answers belong to the repository, not to you. Put them in its `CLAUDE.md`
(or a file under `.claude/rules/`) and Rabbit stops asking:

```markdown
## Development

- Base branch: `develop`.
- Branch names: `feature/<KEY>-<short-description>`.
- Start locally: `docker compose up -d && npm run dev`.
- Full test suite: `npm test`.
```

Without a base branch here, Rabbit uses the branch `origin/HEAD` points at,
usually `main`. Without a branch name rule, it follows the style of the
repository's recent branches, or uses the lower-case key, and shows the name
when it asks you to approve the plan.

## Sharing with your team

Keep the workflow file in a private team repository and point everyone's profile
at their clone of it. A `git pull` updates it for everyone; Rabbit reads it
again at the start of every task and dev session.

Keep it out of public repositories if it names internal tools or addresses. The
profile is personal and never goes into a repository.
