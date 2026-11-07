# summary.md format

Write in `DOC_LANG`; translate headings and notes, keep keys, ids and links as
they are.

1. `# <sprint full name>` and a short list: sprint id, board id, goal, pull time
   (local time).
2. `## Tasks`: a table of **every** issue from step 1 with columns key, title,
   type, status, repository (the `Repo:` line, or empty), session
   (`[title](#<sessionId>)` or empty), note.
   Notes: `finished, no session`, `left the sprint`, `new`, `carried over:
   <folder>`.
3. `## Since last pull`: if a previous `summary.md` exists, compare its table:
   new tasks, newly finished tasks, tasks no longer in the sprint (keep their
   rows with the note `left the sprint`). First pull: write `First pull.`
