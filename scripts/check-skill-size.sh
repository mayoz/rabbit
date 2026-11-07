#!/usr/bin/env bash
# Usage: check-skill-size.sh [root]
# Fails when a SKILL.md is over its word limit: 1850 for task, 1000 for the others.
set -euo pipefail
root=${1:-$(git rev-parse --show-toplevel)}
fail=0
for f in "$root"/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  limit=1000; [ "$(basename "$(dirname "$f")")" = task ] && limit=1850
  words=$(wc -w < "$f" | tr -d ' ')
  if [ "$words" -gt "$limit" ]; then echo "$f: $words words (limit $limit)"; fail=1; fi
done
exit $fail
