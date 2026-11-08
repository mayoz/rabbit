# Setup messages

Send a message by its id, translated into `LANG`. Keep Markdown, `{{...}}`
values, paths, URLs, commands and keys exactly as they are.

## setup.welcome
Hi! I'm `Rabbit`.

I'll ask a few short questions to set things up and save your answers to
`~/.config/rabbit/profile.md`.

You can change any answer later.

## setup.doctor
Your profile is at `{{path}}`:

{{table}}

{{report}}


## setup.workflow-read
I read your workflow file. It has instructions for: {{stages}}. Every other
stage uses Rabbit's default.

## setup.workflow-missing
I can't read `{{path}}`. Check the path, or pick No to continue without a
workflow file.

## setup.workflow-unknown
These headings name no Rabbit stage, so they won't be applied: {{headings}}
The stages are listed here:
https://github.com/mayoz/rabbit/blob/main/docs/workflow.md

## setup.workflow-placeholders
These placeholders aren't filled in: {{placeholders}}. I'll ask for them each
time a task needs them; fill them in the file to stop that.

## setup.folder-create
`{{path}}` doesn't exist yet. Create it?
Options: Create it (Recommended) · Choose another folder

## setup.repos-found
Found {{count}} git repositories in `{{path}}`.

## setup.repos-none
I found no git repositories in `{{path}}`. Is that the right folder?

## setup.no-jira-tools
I can't find a Jira connection. Rabbit reads Jira through an MCP server; the
simplest is Atlassian's own:

```
claude mcp add --scope user --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

`--scope user` makes it available in every folder, which Rabbit's sessions need.
Add it, sign in when Claude asks, start a new session and run `/rabbit:setup`
again. For Jira Server or Data Center, add an MCP server that supports it
instead.

## setup.sprint-field
Your sprint field is `{{field}}` (found on `{{key}}`).

## setup.sprint-field-missing
None of your issues is in an active sprint, so I can't find the sprint field
yet. I saved everything else. `/rabbit:task <KEY>` works already; run
`/rabbit:setup` again before `/rabbit:pull`, once you have a task in a sprint.

## setup.saved
Saved to `{{path}}`. Open it in any editor to change a value, or run
`/rabbit:setup` again.

## setup.try
Test run: your active sprint is **{{sprint}}** with {{count}} tasks assigned to
you.

## setup.done
Congratulations, setup is complete.

To start and pull your sprint, run `/rabbit:pull`:

```
/rabbit:pull
```

## setup.try-failed
Setup is saved, but the test query failed: {{error}}
