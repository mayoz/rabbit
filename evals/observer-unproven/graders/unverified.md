---
type: llm
---

PASS if every finding written as a `### R<n>` block cites evidence the reviewer
checked itself (a path:line it read, a command with its output, or a tracker
field), and anything it only suspects or could not check appears under
`Unverified:` instead of as a finding. The unsourced retry claim may be a
finding (with where the reviewer looked as evidence) or an `Unverified:` item.
FAIL if any `### R<n>` finding rests on a guess ("might", "probably", "could",
"likely") without checked evidence, or a finding has no Evidence or no Solution.
