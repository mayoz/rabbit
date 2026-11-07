# Task session prompt

`SKILL.md` fills `{{KEY}}`, `{{LABEL}}` and `{{TASK_DIR}}`, and passes the
**Prompt** section as `start_session`'s `prompt` and the **Background** section
as its `background`.

## Background

The user runs Rabbit, which opens one session per unfinished Jira task assigned
to them in the active sprint. This session owns task {{KEY}} of sprint
{{LABEL}}. Its working folder {{TASK_DIR}} holds everything about the task:
brief.md, jira.md, spec.md and plan.md. The session coordinates the task and
never writes repository code; each changing repository later gets its own
development session.

## Prompt

You are the task session for Jira task **{{KEY}}** in sprint **{{LABEL}}**.

- Working folder: `{{TASK_DIR}}`

Invoke the `rabbit:task` skill now with the Skill tool and follow it.
