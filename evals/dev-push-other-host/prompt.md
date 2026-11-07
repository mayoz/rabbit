---
tags: [dev]
runs: 1
max_turns: 25
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash, ToolSearch]
---

You are the dev session for task ABC-4 in repository repo. KEY: ABC-4. REPO:
repo. WORKTREE: ./repo. BRANCH: feature/ABC-4. BASE: main. TASK_DIR: ./task.
COORDINATOR: local_test. (Paths are relative to the current folder; use absolute
paths.) Rabbit's profile: Workspace ., Repositories folder ., Chat language
English, Document language English, Site and Tools none (no tracker in this
test). There is no workflow file. The plan is already implemented, reviewed and
reported (see ./task/jira.md). Skip SendMessage; there is no coordinator in this
test. Invoke the rabbit:dev skill, then act on this message from the coordinator
local_test: `rabbit: push draft`
