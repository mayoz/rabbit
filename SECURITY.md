# Security policy

Rabbit is instructions for Claude Code; it ships no server and stores no
secrets. Still, a skill could be made to write where it should not, leak a
private detail, or skip an approval. Those are security issues.

Please report them privately through
[GitHub security
advisories](https://github.com/mayoz/rabbit/security/advisories/new), not in a
public issue. Include the command, what Rabbit did and what you expected. You
will get an answer within a week.

## What Rabbit does to stay safe

- It reads your tracker and writes to it only when your workflow file says so,
  after you approve the file.
- It pushes only after you say yes, and never force-pushes or deletes branches.
- It runs applications and tests only against services on your machine.
- Its reviewer, the `rabbit:observer` agent, has no file-writing tools. A hook
  lets it use only reading tools, shell commands made only of known read-only
  commands, MCP tools whose names start with a read word (`get`, `list`,
  `search`…) and hold no write word, and the Jira tools your profile names; it
  blocks everything else, including any call it fails to check. Without Python 3
  it blocks every tool the observer calls. It is a guard, not a sandbox: report
  a way around it as a vulnerability.

## Supported versions

Only the latest release is supported.
