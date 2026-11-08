# Dev messages

## setup.needed
Rabbit isn't set up yet ({{missing}}). Let's do that first; it takes about two
minutes.

## error.no-context
This session wasn't started by `/rabbit:task`, so I don't know which plan to
implement. Run `/rabbit:task <KEY>` and approve a plan first.

## error.workflow-missing
Your profile points at the workflow file `{{path}}`, but I can't read it. Fix
the `Workflow:` line in `~/.config/rabbit/profile.md`, or run `/rabbit:setup`.

## start.summary
**{{key}} · {{repo}}** on `{{branch}}`. I'll implement these plan tasks in
order, testing and committing each one locally:
{{tasks}}

## step.done
✓ {{step}} — committed `{{sha}}`.

## step.blocked
I stopped at **{{step}}**: {{problem}}
I ran: `{{command}}`
How should we go on?

## ask.blocker
I can't go on with {{step}} without you: {{problem}}
{{what_to_do}}
Options: Done, try again (Recommended) · Skip it (its checks stay unverified)

## ask.instruction-failed
I couldn't apply this instruction from your workflow file ({{stage}}):
"{{instruction}}"
Reason: {{reason}}. What should I do?

## ask.placeholder
Your workflow file needs a value for `{{placeholder}}` ({{stage}}:
"{{instruction}}").
What should it be?

## ask.execute
How should I implement the plan?
Options: superpowers (`superpowers:executing-plans`) (Recommended) · native
(Rabbit's own loop, one commit per plan step)

## done
All {{repo}} steps are done and I reviewed the diff:
{{commits}}
Tests run: {{tests}}
Review: {{review_summary}}
I told the task session. Nothing is pushed; the task session asks you first.

## pushed
Pushed `{{branch}}` and opened {{pr}} ({{status}}).

## pushed.manual
Pushed `{{branch}}`. This repository is not on GitHub, so open the merge request
from `{{branch}}` yourself.

## push.via-task
Pushes go through the task session, so all repositories are pushed and linked
together.
Answer its push question there.

## ask.workflow-approval
Your workflow file asks me to act outside this machine. It is new or changed
since you last approved it:

{{instructions}}

Shall I run these when their moment comes?
Options: Run them (Recommended) · Skip them for this task
