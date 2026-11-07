#!/usr/bin/env bash
set -e
g() { git -c user.name=fixture -c user.email=fixture@example.com "$@"; }
mkdir -p repo task origin.git home/.config/rabbit
g -C origin.git init -q --bare
g -C repo init -q -b main
echo "# demo" > repo/README.md
g -C repo add README.md && g -C repo commit -q -m init
g -C repo remote add origin "$PWD/origin.git"
g -C repo push -q origin main
g -C repo checkout -q -b feature/ABC-4
echo hi > repo/hello.txt
g -C repo add hello.txt && g -C repo commit -q -m "feat: add hello"
cat > task/plan.md <<'MD'
# ABC-4 plan

## repo

### Task 1: hello file
- Files: create `hello.txt` containing `hi`. Done.
MD
printf '## Status\nExecute: native\nDone: repo 2026-11-07\n' > task/jira.md
cat > home/.config/rabbit/profile.md <<'MD'
# Profile

## Basics
- Workspace: .
- Repositories folder: .
- Chat language: English
- Document language: English
MD
