# Token usage

Rabbit is built to stay light for small tasks and bounded for large ones.

## What is always loaded

Only each skill's and the agent's one-line description: about 500 tokens in
total. A skill's instructions load when you run it, and its reference files load
only in the step that needs them. The hooks cost no tokens.

Check it yourself with `claude plugin details rabbit`.

## What a task costs

Most of a task's cost is reading: the issue, the code, and the documents the
observer checks. Rabbit keeps it bounded:

- Tracker searches ask only for the fields they use.
- Without a code-search tool, the impact search lists file names first (`git
  grep -l`) and reads at most 3 files per consumer and 8 in total.
- Every review, Integration's included, runs at most two rounds; the second only
  checks the fixes.
- Each file is read once and cited, not read again.

## Spending less

- **Name the repositories precisely** in the first question. Rabbit reads only
  those, and searches your other clones by file name only.
- **Skip the full test suite** under `## Integration` when a repository's suite
  is slow; CI still runs it.
- **Skip superpowers for small tasks.** Say so under `## Spec and Plan` in your
  workflow file; superpowers asks more and writes more.
- **Answer open questions in one reply.**
- **Pull once per sprint**, and run `/rabbit:pull` again only when tasks were
  added.
- **Archive task sessions** you are done with.
