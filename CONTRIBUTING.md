# Contributing

Thanks for helping. Issues and pull requests are welcome. New to the code? Start
with [Development](docs/contributing/development.md): it shows how to run your
own copy and how the repository is laid out.

## Workflow

1. Open an issue first for anything larger than a typo, so we agree on the
   change.
2. Branch from `main`; one change per pull request.
3. Use [Conventional Commits](https://www.conventionalcommits.org/):
   `feat(task): …`, `fix(pull): …`, `docs: …`.
4. Run `scripts/check.sh` ([Development](docs/contributing/development.md));
   every check must pass. If you changed a skill, run its evals with `--tag
   <skill>` and say in the pull request that you did.
5. A change under `skills/`, `agents/`, `hooks/` or `.claude-plugin/`, or to
   `docs/profile.md` or `docs/workflow.md` (setup reads them), bumps `version`
   in `.claude-plugin/plugin.json` and adds a `CHANGELOG.md` entry.

## Skill text is code

Reviewers read a skill change the way they read code. Call out in the pull
request:
- a new tool the skill calls, and whether it writes anything;
- a new external address;
- any change to when Rabbit asks before acting.

Keep `task/SKILL.md` within 1850 words and the other skills within 1000; move
detail into `references/`. Wrap Markdown at 80 columns.

## Keep private details out

Rabbit is used inside companies. Examples use placeholders: `acme`, `<site>`,
`customfield_<id>`, `example.com`. `scripts/leak-scan.sh` checks for real
addresses, home paths and tokens, but it can't know your company's names, so
please check your own text for company or customer names before you open a pull
request.

## Code of conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
