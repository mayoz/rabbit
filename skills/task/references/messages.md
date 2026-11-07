# Task messages

## setup.needed
Rabbit isn't set up yet ({{missing}}). Let's do that first; it takes about two
minutes.

## error.desktop-only
`/rabbit:task` opens dev sessions and moves between folders, which only works in
the Claude Desktop app. Open Claude Desktop and run `/rabbit:task {{arg}}`
there.

## error.no-task
I can't tell which task this is: this session's folder isn't a Rabbit task
folder. Run `/rabbit:task <KEY>` (e.g. `/rabbit:task ABC-123`) or paste the
issue link.

## error.other-site
That link is on `{{site}}`, but your profile reads Jira from `{{profile_site}}`.
Paste a link from your own site or just the key, or change the site with
`/rabbit:setup`.

## error.not-found
I can't find **{{key}}** on `{{site}}`. Check the key, or whether you can open
it in Jira.

## error.workflow-missing
Your profile points at the workflow file `{{path}}`, but I can't read it. Fix
the `Workflow:` line in `~/.config/rabbit/profile.md`, or run `/rabbit:setup`.

## note.unknown-heading
Your workflow file has headings that name no Rabbit stage, so I won't apply
them:
{{headings}}.

## ask.instruction-failed
I couldn't apply this instruction from your workflow file ({{stage}}):
"{{instruction}}"
Reason: {{reason}}. What should I do?

## ask.placeholder
Your workflow file needs a value for `{{placeholder}}` ({{stage}}:
"{{instruction}}").
What should it be?

## brief.ready
> I read Jira for **{{key}}**. I created [brief.md](brief.md) for this ticket.
> Take a look at `brief.md` before we go on to the questions. {{review_line}}

## ask.repos
**Which repositories do we need to work in for {{key}}?** You can write one or
more repository names, for example {{examples}}.

## ask.repo-missing
I can't find {{names}} in `{{folder}}` (I looked there and one folder deeper).
Check the names.

## ask.repo-which
There is more than one `{{name}}`: {{paths}}. Which one?

## confirm.repos
Repositories: {{repos}}.

## ask.note
**Is there anything you'd like to add to the `brief.md` created for {{key}}?**
For example other repositories to read, points to watch, or decisions already
made. If there's nothing, write `continue`.

## ask.spec-approval
The spec is ready. {{review_line}}

Spec: [spec.md](spec.md) · [reviews/spec.md](reviews/spec.md)

Do you approve [spec.md](spec.md)? Tell me what to change otherwise.

## ask.breaking
This spec breaks existing consumers:

{{breaks}}

Do you accept these breaks? If not, tell me and I'll change the spec to avoid
them.

## ask.plan-approval
The plan is ready. {{review_line}}

Branches: {{branches}}. {{execute_line}}

Plan: [plan.md](plan.md) · [reviews/plan.md](reviews/plan.md)

Do you approve [plan.md](plan.md)? When you do, I'll open one dev session per
repository.

## ask.spec-plan-approval
The spec and the plan are updated. {{review_line}}

Branches: {{branches}}. {{execute_line}}

Spec: [spec.md](spec.md) · [reviews/spec.md](reviews/spec.md)
Plan: [plan.md](plan.md) · [reviews/plan.md](reviews/plan.md)

Do you approve [spec.md](spec.md) and [plan.md](plan.md)? When you do, I'll
open one dev session per repository.

## ask.add-repo
`{{repo}}` doesn't change in this task, but it uses {{surface}} and would break:
{{evidence}}. Should I add it to the plan as a changing repository? (`yes` /
`no`)

## integration.report
Integration for **{{key}}**: {{summary}}

{{table}}

Details: [integration.md](integration.md)

## ask.cleanup
Integration created this test data in your local services:

{{items}}

Shall I remove it? I remove only these items, one by one; a no keeps them.

## ask.suite-command
How do I run the full test suite of `{{repo}}`? I couldn't find it in its
`CLAUDE.md`, README or CI config. Reply with the command, or `skip` to leave it
to CI.

## ask.workflow-approval
Your workflow file asks me to act outside this machine. It is new or changed
since you last approved it:

{{instructions}}

Shall I run these when their moment comes? A no skips them for this task.

## ask.run-command
How do I start `{{repo}}` locally? I couldn't find it in its `CLAUDE.md`,
README, compose or package scripts. Adding the answer to its `CLAUDE.md` would
help next time.

## ask.run-setup
To run `{{repo}}` in `{{worktree}}` I need to install its dependencies
(`{{install}}`) and copy `.env` from `{{main_checkout}}`. Shall I? (`yes` /
`no`; with no, those scenarios stay unverified)

## ask.push-anyway
Done: {{repos}}. These scenarios did not pass:

{{rows}}

{{behind_line}}
Push anyway? If yes: open the pull requests as **draft** (recommended, since not
everything passed) or **ready** for review?

## ask.push
Done: {{repos}}. {{behind_line}}
Shall I push and open the pull requests **ready** for review (recommended) or
as **draft**?
Some CI checks skip draft pull requests.

## ask.push-manual
Done: {{repos}}. {{behind_line}}
None of these repositories is on GitHub, so I'll push the branches and you open
the merge requests yourself. Shall I push?

## draft.waiting
The pull requests are drafts, so I'm not following CI or applying the after-push
steps yet.
Tell me when they should be ready for review.

## publish.table
Pull requests for **{{key}}**:

{{table}}

## ask.ci
Shall I follow CI for these pull requests?

## ci.failed
A required check failed on `{{repo}}` ({{pr}}): **{{check}}**. {{reason}}
Shall I fix it and push the fix to the same branch?

## ci.passed
All required checks passed: {{prs}}.
