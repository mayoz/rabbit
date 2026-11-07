# Pull messages

## setup.needed
Rabbit isn't set up yet ({{missing}}). Let's do that first; it takes about two
minutes.

## error.desktop-only
`/rabbit:pull` opens one session per task, which only works in the Claude
Desktop app. Open Claude Desktop and run `/rabbit:pull` there.

## error.no-sprint
I found no active sprint with tasks assigned to you on `{{site}}`.
`/rabbit:pull` needs one; without a sprint, start a single task with
`/rabbit:task <KEY>`.

## ask.which-sprint
You're in more than one active sprint:
{{sprints}}
Which one should I pull?

## error.other-main
Sprint **{{sprint}}** already has a main session: {{link}}. Continue there; I
created nothing.

## report.done
**{{sprint}}**: {{total}} tasks, {{unfinished}} unfinished.
- Sessions opened now: {{opened}}
- Already had a session: {{existing}}
- Carried over from an earlier folder: {{carried}}
- Skipped as finished: {{finished}}

Summary: {{summary_link}}

## report.ready
All task sessions are ready. Open one to start on its task.
