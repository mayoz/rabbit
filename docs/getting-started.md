# Getting started

This guide takes you from a fresh install to your sprint in Claude Desktop. It
takes about ten minutes. If Rabbit is not installed yet, start with
[Installation](installation.md).

- [1. Run setup](#1-run-setup)
- [2. Pull your sprint](#2-pull-your-sprint)
- [3. Open a task](#3-open-a-task)
- [4. Pull again later](#4-pull-again-later)
- [Work on a task without pulling](#work-on-a-task-without-pulling)

## 1. Run setup

Open a new session in Claude Desktop's **Code** tab, in any folder, and type:

```
/rabbit:setup
```

Setup asks five short questions, one at a time. Each shows a few choices with
the default first; pick one, or type your own answer.

| Question | What it means | Default |
| --- | --- | --- |
| Do you have a Rabbit workflow file? | A file with your team's own instructions. Most people start without one. See [Customizing Rabbit](customizing.md). | `No` |
| Where should Rabbit keep your sprint folders? | Your workspace. Rabbit writes its documents here, never in your repositories. Any empty or new folder is fine. | `~/rabbit/sprints` |
| Which folder holds your git clones? | The folder you clone repositories into. Rabbit finds a repository by name here or one folder deeper. | `~/code` |
| Which language should I talk to you in? | The language of Rabbit's messages. Type `auto` to follow the language you write in. | `English` |
| Which language should briefs, specs and plans be written in? | The language your team reads. | `English` |

Setup then finds your Jira tools, your site and the field that holds sprints,
without asking. If you have more than one Jira connection or site, it asks which
one. It saves everything to `~/.config/rabbit/profile.md` and runs one test
search: you should see your sprint's name and how many tasks are assigned to
you.

Run `/rabbit:setup` again any time to check your profile or change an answer.
See [Your profile](profile.md) for every setting.

## 2. Pull your sprint

Open a new Desktop session. Its folder does not matter; your workspace, for
example `~/rabbit/sprints`, is a good choice.
Type:

```
/rabbit:pull
```

Rabbit reads the issues assigned to you in the active sprint and:

1. moves this session into a sidebar section called **Sprints** and names it
   after the sprint's Jira id, for example `SP_1234`, and makes the sprint
   folder its working folder;
2. creates a folder per unfinished task, for example
   `~/rabbit/sprints/SP_1234/ABC-1/`;
3. opens one session per unfinished task, nested under the sprint session;
4. writes `summary.md` in the sprint folder: every task, its status and its
   session.

If you are in more than one active sprint, Rabbit asks which one to pull.
Finished tasks get no folder and no session.

```
Sprints
└── SP_1234             ← the sprint session, where you ran /rabbit:pull
    ├── ABC-1 Fix login ← one task session per unfinished task
    └── ABC-2 Add export
```

## 3. Open a task

Click a task session in the sidebar. It has already read the issue and written a
one-page `brief.md`, checked by a reviewer that never saw your conversation. It
asks two questions (the first is skipped when the issue names its repositories
in a `Repo:` line):

1. **Which repositories do we need to work in?** Type their names, for example
   `web-app, api`. Rabbit finds them in your repositories folder.
2. **Is there anything you'd like to add?** Type `continue`, or add hints such
   as other repositories to read or decisions already made.

Claude Desktop may ask you to allow access to each repository folder. Allow it;
Rabbit only reads there until you approve a plan.

From here on, Rabbit writes a spec and a plan and asks you to approve each.
Follow [Your first task](first-task.md) for the whole journey, from brief to
pull request.

## 4. Pull again later

When tasks are added to the sprint, go back to the sprint session and run
`/rabbit:pull` again. It adds folders and sessions only for the new tasks and
updates `summary.md`. It never touches existing task folders or sessions.

Run it in the same sprint session. If you run it in another session, Rabbit
points you back to the sprint session and creates nothing.

## Work on a task without pulling

You can start any single task in a new Desktop session:

```
/rabbit:task ABC-123
```

You can also paste the issue's link instead of the key. Rabbit works the same
way. The task's folder goes into its sprint's folder (`SP_1234/ABC-123/`) when
the issue is in an active sprint, and into `tasks/ABC-123/` otherwise. Rabbit
moves the session into that folder after its first reply.
