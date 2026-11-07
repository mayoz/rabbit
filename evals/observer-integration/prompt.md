---
tags: [observer]
runs: 1
max_turns: 10
allowed_tools: [Skill, Read, Glob, Grep, ToolSearch, Agent]
---

Run the rabbit:observer agent (Agent tool, subagent_type "rabbit:observer") and
show me its verdict. Use absolute paths for everything below (they are relative
to the current folder).
Kind: integration. Task: ABC-2.
Repositories: ./producer (base main, branch feature/ABC-2); ./consumer (base
main, branch feature/ABC-2).
Builds on: ./brief.md, ./spec.md. Impact: ./impact.md.
Tracker: none available. Workflow review rules: none.
Lens: the acceptance criteria hold across the repositories as a whole; fields,
enum values, endpoints and queue names match between repositories; no consumer
in the impact list breaks.
