# Your workflow file

This is the reference for workflow files: every stage, every heading and how
Rabbit applies them. For a gentle introduction and ready-made recipes, read
[Customizing Rabbit](customizing.md) first.

- [What it is](#what-it-is)
- [Stages](#stages)
- [Before and after a stage](#before-and-after-a-stage)
- [Heading rules](#heading-rules)
- [How Rabbit applies instructions](#how-rabbit-applies-instructions)
- [Placeholders](#placeholders)
- [Instructions that act outside your
  machine](#instructions-that-act-outside-your-machine)
- [Execute](#execute)

## What it is

A workflow file tells Rabbit how you, or your team, work at each stage of a
task. It reads like a `CLAUDE.md`: each `##` heading names a stage, and the text
under it is plain instructions.

The file is optional. Without it Rabbit uses the defaults below. Keep it
anywhere and point your profile at it:

```markdown
Workflow: ~/rabbit/rabbit-workflow.md
```

Rabbit reads the file when a task or dev session starts or resumes, so an edit
applies from the next session on. Start from
[examples/workflows/rabbit-workflow.md](../examples/workflows/rabbit-workflow.md).

## Stages

| Heading | When it applies | Default without it |
| --- | --- | --- |
| `## Brief` | while the brief is written | the issue and the tools in the session |
| `## Spec` | while the spec is written | superpowers when installed, else Rabbit's own guide |
| `## Plan` | while the plan is written | superpowers when installed, else Rabbit's own guide |
| `## Execute` | while a dev session implements the plan | superpowers when installed, else native |
| `## Review` | in every blind review (adds criteria) | the blind review only |
| `## Integration` | while the changed repositories are checked together | impact check, joint review, contract tests, each repository's full test suite once, every spec scenario tried in the running apps |
| `## Push` | while branches are pushed, pull requests opened and CI followed; may name checks that wait for a later step (QA, a test environment), which CI following leaves out | push and open pull requests, ready or draft as you answer |

`## Spec and Plan` is a shorthand: its instructions apply to both stages.

## Environment

`## Environment` is not a stage and takes no `:Before` or `:After`. It holds
what Rabbit needs to run your apps and tests: how to set up a worktree, where
sign-in data comes from, how to check and refresh credentials, how to make test
data, and when to stop (for example "the test environment is closed at
weekends"). The task session reads it at every step that runs something, and
every dev session reads it too. A stop condition there is a blocker: Rabbit asks
you with a "Done, try again" button and, if it stays, marks the checks that
needed it `unverified` and goes on.

With it, Rabbit sets up the environment, changes a setting for a test and
restores it, and creates new test data named with the task key without asking.
After Integration it asks once whether to keep or remove that test data. Every
step goes to the environment log in `integration.md`.

## Questions

Every yes/no or choice question comes with buttons, the recommended answer
first, after a short box that says what is needed, why, and what each answer
does. Approvals still come one at a time: no plan before the spec is approved,
no code before the plan is approved. If you answer something else, Rabbit does
that and then asks the open question again; "we won't do it" counts as an
answer.

## Before and after a stage

Every stage also takes `:Before` (before it starts) and `:After` (after it ends
and is approved):

| Heading | Runs |
| --- | --- |
| `## Brief:Before` | before the brief is written |
| `## Plan:After` | when you approve the plan |
| `## Review:Before`, `## Review:After` | before each blind review, and after each verdict |
| `## Push:Before` | before Rabbit asks you to push |
| `## Push:After` | once the pull requests are ready for review and the required checks pass, or right away when you chose not to follow CI |

`## Push:After` never runs for draft pull requests, or after a failing check you
chose not to fix. Checks that only pass after a later step (a QA run, a test
environment) would hold it forever: name them under `## Push`, for example
"These checks wait for the test environment: `e2e/staging`, `Release Gate`."
Rabbit then follows CI without them and runs `## Push:After` when the rest
pass. `## Spec and Plan:After` works too.

`/rabbit:pull` starts every task at once, so a tracker change belongs after an
approval (`## Plan:After`), not in `## Brief:Before`.

## Heading rules

- Headings are case-insensitive: `## push:after` is `## Push:After`.
- Only `##` headings open a section. Text before the first one is ignored.
- A heading written twice keeps both: the instructions are joined in order.
- A heading with nothing under it counts as missing, so the default applies.
- A heading that names no stage, such as `## Deploy`, is not applied. Rabbit
  tells you once when it reads the file, and `/rabbit:setup` lists it.

## How Rabbit applies instructions

- Each bullet or paragraph under a heading is one instruction. Rabbit applies
  every one, in order, and skips none.
- When an instruction can't be applied, Rabbit stops, says why and asks what to
  do.
- An instruction can pick a path ("Use superpowers") or ask you to choose ("Ask
  whether to use superpowers or native").
- Write what to do, not how Rabbit works: name the tool, the command or the
  rule.
- The blind review always runs. `## Review` only adds criteria.
- A command in a repository, for example under `## Push:Before`, runs in that
  repository's dev session.
- The repository's own `CLAUDE.md` and `.claude/rules/` win where they disagree.

## Placeholders

A word in angle brackets is a placeholder. Rabbit fills these itself:

| Placeholder | Becomes |
| --- | --- |
| `<KEY>` | the task key, for example `ABC-123` |
| `<SUMMARY>` | the issue's summary |
| `<REPO>` | the repository's name |
| `<BRANCH>` | the task's branch in that repository |
| `<BASE>` | the base branch |
| `<TASK_DIR>` | the task folder |

Any other, such as `<environment>`, is asked the first time an instruction needs
it. Rabbit writes the answer to the task's `jira.md` and uses it for the rest of
the task, in the dev sessions too. Don't use angle brackets for anything else,
such as `<your tool>`: write plain text instead.

## Instructions that act outside your machine

An instruction that writes to your tracker, uploads a file or sends a message
runs only after you approve the workflow file. Before the first such
instruction, Rabbit shows every one of them and asks once. On `yes` it keeps a
copy at `~/.config/rabbit/approved-workflow.md` and doesn't ask again until the
file changes. On `no` it skips those instructions for this task.

Rabbit never writes to your tracker unless an instruction says so.

## Execute

Two ways to implement a plan are supported:

- `superpowers`: superpowers' `executing-plans` skill;
- `native`: Rabbit's own loop, one test and one commit per plan step.

Name one under `## Execute`, or leave the heading out: Rabbit uses superpowers
when it is installed, else native.
