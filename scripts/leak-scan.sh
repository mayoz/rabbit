#!/usr/bin/env bash
# Usage: leak-scan.sh [--denylist <file>] [path...]
# Fails (exit 1) when a file holds a personal or company detail that must not be published.
# Extra patterns, one ERE per line, come from the first of: --denylist, $LEAK_PATTERNS,
# ~/.config/rabbit/denylist. With no path, scans the files git tracks.
set -euo pipefail

deny=""
if [ "${1:-}" = --denylist ]; then deny=$2; shift 2; fi

patterns=(
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}'
  '[a-z0-9-]+\.atlassian\.net'
  'customfield_[0-9]+'
  '/Users/[a-z]'
  '/home/[a-z]'
  '(ghp|gho|github_pat|xox[bp]|sk-ant)[-_][A-Za-z0-9]'
)
# Placeholders the docs may use; they are blanked out before matching.
allow='noreply@|@example\.com|<site>\.atlassian\.net|acme\.atlassian\.net'

if [ -n "$deny" ]; then extra=$(cat "$deny")
elif [ -n "${LEAK_PATTERNS:-}" ]; then extra=$LEAK_PATTERNS
elif [ -f "$HOME/.config/rabbit/denylist" ]; then extra=$(cat "$HOME/.config/rabbit/denylist")
else extra=""
fi
while IFS= read -r p; do [ -n "$p" ] && patterns+=("$p"); done <<<"$extra"

args=(); for p in "${patterns[@]}"; do args+=(-e "$p"); done

if [ $# -eq 0 ]; then
  cd "$(git rev-parse --show-toplevel)"
  # The scanner and its test hold the patterns themselves.
  files=()
  while IFS= read -r f; do files+=("$f"); done \
    < <(git ls-files | grep -vxE 'scripts/leak-scan\.sh|tests/test_leak_scan\.sh')
  set -- "${files[@]}"
fi

found=0
for f in "$@"; do
  if [ ! -f "$f" ] || ! grep -Iq . "$f"; then continue; fi
  while IFS= read -r hit; do
    echo "$f:$hit"; found=1
  done < <(sed -E "s#$allow##g" "$f" | grep -noEi "${args[@]}" || true)
done
exit $found
