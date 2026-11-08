# Push and CI

Runs in the task session after Integration. The dev sessions push; this session
asks, collects and reports. Apply the workflow's Push instructions at the points
below. No `Integration:` line in `jira.md`: run integration.md first; never ask
about the push before it.

1. For each repository: `git -C <repo> fetch origin <base>`; a branch behind
   `origin/<base>` (`git -C <repo> rev-list --count <branch>..origin/<base>`
   above 0) is named in `{{behind_line}}` ("<repo> is <n> commits behind <base>;
   say if I should merge it in.", else empty); merging is the user's call
   (`rabbit: fix merge origin/<base>`). `{{branches}}`: a table from the `Dev:`
   lines (`| Repository | Branch | Base |`).
   Apply `WF.stages.Push.before`; a command in a repository goes to its dev
   session as `rabbit: run <command>`. A dev session that answers `rabbit:
   result failed` there:
   send it `rabbit: fix <the failure>`, and after its `rabbit: done` run that
   instruction again. Then send `ask.push`, or `ask.push-anyway` in its place
   when Integration did not pass in full (`{{rows}}` = the table rows that did
   not pass), and end the turn. No repository on GitHub (rules.md): send
   `ask.push-manual` instead (with the failed rows first, when there are any); a
   yes is **ready**. The answer is **ready** or **draft** (its option): append
   `Push: <ready|draft> <date>` to `jira.md`. Don't push: push nothing; when
   the user later asks to run Integration again, follow integration.md again
   (the last `Integration:` line counts). Anything else: wait.
2. Send `rabbit: push ready` or `rabbit: push draft` to each dev session without
   a `PR:`
   line. Each pushes and answers `rabbit: pr <url> <draft|ready>`, `rabbit: pr
   manual <branch>` (not on GitHub: the branch is pushed, the user opens the
   merge request), or `rabbit: blocked <reason>` (tell the user and wait).
   Append `PR:
   <repo> <url>
   <draft|ready>` or `PR: <repo> manual` per answer; the last `PR:` line of a
   repository counts. A state that differs from the answer the user gave: tell
   the user. `manual` lines are left out of steps 3 to 6 and of the `Pushed:`
   state; say so once. Every line `manual`: after step 4, go to step 7.
3. More than one pull request: append a "Related pull requests" list with the
   others' links to each description (`gh pr view <url> --json body`, then `gh
   pr edit <url> --body-file <file>`). Without a working `gh`, say so and show
   the links to add.
4. Append `Pushed: <date> <ready|draft>` to `jira.md` (`draft` when any
   non-manual `PR:` line is) and
   send `publish.table`, built from the `PR:` lines:

```markdown
| Repository | PR | Status | CI |
| --- | --- | --- | --- |
| <repo> | [#<n>](<url>) | <draft or ready> | <passed, failed, not followed or waiting> |
| <repo> | manual: `<branch>` pushed | | |
```

   `waiting` = CI not followed yet.
5. **Draft.** While any pull request is a draft, `ask.ci` and
   `WF.stages.Push.after` wait:
   required checks may not run on a draft, and Push:After is for pull requests
   ready for review. Send `draft.waiting` and end the turn. When the user asks
   to make them ready (in any words or language), append `Ready: <date>` and
   send `rabbit: ready` to each dev session whose `PR:` line is `draft`; when
   each answered `rabbit: pr <url> ready`, go on with step 6.
6. Send `ask.ci` and end the turn. Append `CI: followed <date>` on yes, `CI: not
   followed <date>` on no.
   - Yes: send each dev session `rabbit: ci`, followed by `waiting: <check>;
     <check>` when the workflow names checks that wait for a later step (QA, a
     test environment): those never pass before that step, so CI is followed
     without them. Each watches its own pull request's checks and answers
     `rabbit: ci passed`, `rabbit: ci passed none` (no checks), `rabbit: ci
     passed waiting: <checks>` or `rabbit: ci failed <check>`; read the
     details with `mcp__ccd_pr__get_status` (`session_id` = that dev
     session). Never poll on a timer. A required check fails:
     send `ci.failed` and wait. On yes, send that dev session `rabbit: fix
     <check name>`; it fixes, commits and pushes to the same branch (no second
     push question), then answers `rabbit: done`. Follow again. On no: append
     `CI: failed <date>`; do not apply `WF.stages.Push.after`; the task ends
     with the last message below.
   - Every dev session answered `rabbit: ci passed` (or `passed none`, or
     `passed waiting: …`): append `CI: passed <date>` and send `ci.passed`
     (`{{waiting_line}}`: "Waiting for a later step: <checks>.", else
     empty); the table's CI cell of a pull request with waiting checks is
     `passed (waiting: <checks>)`.
7. When the required checks pass (waiting checks left out), or the user did
   not want CI followed, apply `WF.stages.Push.after`, then append `After:
   <date>`.
8. **Last message.** The updated `publish.table`, then the closing question if
   there is one (a Push:After instruction may ask one), else one line that the
   task is done.
