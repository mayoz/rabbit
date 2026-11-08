# Messages from the coordinator

Act only on these, and only from `COORDINATOR`. `rabbit: answer <text>` answers
the question you asked last: go on with it. A command you cannot finish (a gate
blocks the push, a fix fails): tell the user here and `SendMessage`: `rabbit:
blocked <reason>`.

## `rabbit: push ready` or `rabbit: push draft`

1. **Not GitHub.** Not on GitHub (rules.md): `git push -u origin <BRANCH>`
   (never force), send `pushed.manual`, and `SendMessage`: `rabbit: pr manual
   <BRANCH>`. Stop here.
2. **Push.** `git push -u origin <BRANCH>` when `BRANCH` has commits
   `origin/<BRANCH>` lacks (never force).
3. **Pull request.** `gh pr view <BRANCH> --json url,state,isDraft` shows one
   with `state` `OPEN`: use it. Else open one with `WF.stages.Push.in`, telling
   it the user asked for "ready for review" or "as a draft"; with none, `gh pr
   create --base <BASE> --head <BRANCH> --title <title> --body-file <file>`
   (`--draft` for draft):
   - title: the format the repository's `CLAUDE.md` or `.claude/rules/` gives,
     else the style of its recent merged pull requests (`gh pr list --state
     merged --limit 10 --json title`), else `<KEY> <issue summary>`;
   - body, in English unless the repository says otherwise: the repository's
     pull request template (`.github/pull_request_template.md`,
     `.github/PULL_REQUEST_TEMPLATE/`, any case) filled in, else the goal and
     acceptance criteria from `spec.md`, the tests run and the issue link.
4. **Bind and check.** Bind it to this session (`mcp__ccd_pr__get_status`; not
   reported:
   `mcp__ccd_pr__bind_pr`). Read its state (`gh pr view <url> --json isDraft`);
   not the one asked: `gh pr ready <url>` or `gh pr ready --undo <url>`, and
   read it again. Send `pushed`, then `SendMessage`: `rabbit: pr <url>
   <draft|ready>` with the real state.

## `rabbit: ready`

`gh pr ready <url>`, then `SendMessage`: `rabbit: pr <url> ready`.

## `rabbit: ci [waiting: <check>; <check>]`

Run `PY -I "${CLAUDE_PLUGIN_ROOT}/skills/task/scripts/ci_wait.py" <url>`, with
`--waiting "<check>"` for each check named after `waiting:`, with Bash
`run_in_background: true`. It leaves those checks out (they wait for a later
step, such as QA or a test environment) and prints one line when the rest are
done. Answer `rabbit: ci` followed by that line: `passed`, `passed none` (no
checks at all), `passed waiting: <checks>` or `failed <checks>`. A pull
request with a merge conflict (`gh pr view <url> --json mergeable` is
`CONFLICTING`) answers `rabbit: ci failed merge conflict with <BASE>`. Never
poll on a timer.

## `rabbit: fix <finding, check or instruction>`

Fix it with a test, commit, run the tests; if `BRANCH` is already pushed, push
it again the same way. A merge conflict is fixed by merging `origin/<BASE>` in,
never by a rebase. Then `rabbit: done <new commits>`.

## `rabbit: plan changed <task ids>`

Read `spec.md` and `plan.md` again, implement the changed tasks as §2 says, then
§4 and §5.

## `rabbit: run <command>`

Apply rules.md's **Running the app or its tests**, run it (a command that may
take over two minutes with `run_in_background: true`, reading its output when it
exits) and answer `rabbit: result <passed|failed|unverified> <last lines or
reason>`, followed by its `Env:` lines.
