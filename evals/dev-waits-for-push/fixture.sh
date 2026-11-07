#!/usr/bin/env bash
set -e
g() { git -c user.name=fixture -c user.email=fixture@example.com "$@"; }
mkdir -p repo task
g -C repo init -q -b main
echo "# demo" > repo/README.md
g -C repo add README.md && g -C repo commit -q -m init
g -C repo checkout -q -b feature/ABC-3
cat > task/spec.md <<'MD'
# ABC-3 spec

## repo
Add `hello.txt` containing `hi`.
MD
cat > task/plan.md <<'MD'
# ABC-3 plan

## repo

### Task 1: hello file
- Files: create `hello.txt`.
- Steps: write `hi` to `hello.txt`; check with `cat hello.txt`; commit
  `feat: add hello`.
- Done when: `cat hello.txt` prints `hi`.
MD
printf '## Status\nExecute: native\n' > task/jira.md
mkdir -p home/.config/rabbit
cat > home/.config/rabbit/profile.md <<'MD'
# Profile

## Basics
- Workspace: .
- Repositories folder: .
- Chat language: English
- Document language: English
MD
