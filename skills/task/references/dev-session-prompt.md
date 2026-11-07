# Dev session prompt

`SKILL.md` fills `{{KEY}}`, `{{REPO}}`, `{{WORKTREE}}`, `{{BRANCH}}`,
`{{BASE}}`, `{{TASK_DIR}}`, `{{COORDINATOR}}`, `{{ANSWERS}}` and passes
the **Prompt** section as `start_session`'s `prompt` and the **Background**
section as its `background`.

## Background

The user runs Rabbit. A task coordinator session wrote and got approval for a
spec and a plan for task {{KEY}} in {{TASK_DIR}}. This session implements the
{{REPO}} part of that plan in the git worktree {{WORKTREE}}, on branch
{{BRANCH}} cut from {{BASE}}, and reports back to the coordinator.

## Prompt

You are the dev session for task **{{KEY}}** in repository **{{REPO}}**, working
in `{{WORKTREE}}` on branch `{{BRANCH}}` (base `{{BASE}}`). The task's
coordinator session `{{COORDINATOR}}` started you; it owns
`{{TASK_DIR}}/jira.md`, `spec.md` and `plan.md`. Workflow placeholder answers
the user already gave: {{ANSWERS}}.

Invoke the `rabbit:dev` skill now with the Skill tool and follow it.
