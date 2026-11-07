---
tags: [observer]
runs: 1
max_turns: 10
allowed_tools: [Skill, Read, Glob, Grep, ToolSearch, Agent]
---

Run the rabbit:observer agent (Agent tool, subagent_type "rabbit:observer") on
this document and show me its full answer. Use absolute paths for everything
below (they are relative to the current folder).
Kind: spec. Task: ABC-3. Document: ./spec.md. Builds on: ./brief.md.
Repositories: ./shop (base main). Tracker: none available. Workflow review
rules: none.
Lens: every claim and code fact is true on the base branch; following the spec
works end to end.
