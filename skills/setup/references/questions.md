# Setup questions

Ask one question at a time (SKILL.md). Each shows what the answer is for, an
example and the default; `Options` are the choices offered, the first one the
default. Translate into `LANG`; keep paths, URLs, commands and keys as they are.

## workflow
**Do you have a Rabbit workflow file?**
A workflow file tells Rabbit how you work at each stage.
Reply with its path or `no` (Rabbit then uses its defaults and asks when a
choice is needed). Example: `~/rabbit/rabbit-workflow.md`. Default: `No`.
Header: `Workflow`. Options: `No`; `~/rabbit/rabbit-workflow.md`;
`~/httpdocs/rabbit-workflow.md`.

## workspace
**Where should Rabbit keep your sprint folders?**
Rabbit creates one folder per sprint here (`SP_<sprint-id>/`) and one folder per
task inside it. Briefs, specs and plans are written there, never into your
repositories.
Example and default: `~/rabbit/sprints`.
Header: `Sprints`. Options: `~/rabbit/sprints`; `~/httpdocs/sprints`.

## repositories
**Which folder holds your git clones?**
Rabbit finds a repository here by name, or one folder deeper
(`~/code/acme/web-app`), when a task needs it.
Example and default: `~/code`.
Header: `Repos`. Options: `~/code`; `~/httpdocs`.

## chat-language
**Which language should I talk to you in?**
Example: `English`, `Turkish`, `German`. Default: `English`.
Header: `Chat`. Options: `English`; `Turkish`.

## doc-language
**Which language should briefs, specs and plans be written in?**
Pick the language your team reads. Example and default: `English`.
Header: `Documents`. Options: `English`; `Turkish`.

## tracker-tools
**Which Jira connection should Rabbit use?**
I found more than one. List each set found by its server name. Reply with one of
them.
This question is a pick list. There is no default. Header: `Jira`. Options: each
set found (more than 4: list them in the question instead).

## site
**Which Jira site should Rabbit use?**
Your Jira tools can reach more than one. List each site found. Reply with one of
them.
This question is a pick list. There is no default. Header: `Site`. Options: each
site found (more than 4: list them in the question instead).

## doctor-next
**What should I do with your profile?**
Setting it up again asks every question, with your current values as the first
choices.
Header: `Profile`. Options: `Set up again`; `Cancel`.
