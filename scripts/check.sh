#!/usr/bin/env bash
# Usage: scripts/check.sh
# Runs every check a pull request must pass and prints one line per check.
# A missing optional tool (claude, shellcheck) is skipped; CI still runs it.
set -u
cd "$(dirname "$0")/.." || exit 1
py=$(command -v python3 || command -v python) || { echo "python3 is required"; exit 1; }
log=$(mktemp); trap 'rm -f "$log"' EXIT
failed=0

run() {
  local name=$1; shift
  if "$@" >"$log" 2>&1; then
    echo "passed   $name"
  else
    echo "failed   $name"; sed 's/^/         /' "$log"; failed=1
  fi
}

needs() {
  local tool=$1 name=$2; shift 2
  if command -v "$tool" >/dev/null 2>&1; then run "$name" "$@"
  else echo "skipped  $name ($tool not installed)"; fi
}

run "unit tests" "$py" -I -m unittest discover -s tests
run "check script tests" bash tests/test_checks.sh
run "leak scan tests" bash tests/test_leak_scan.sh
needs claude "plugin validate" claude plugin validate . --strict
run "skill size" scripts/check-skill-size.sh
run "line width" "$py" -I scripts/check-line-width.py
run "leak scan" scripts/leak-scan.sh
# shellcheck disable=SC2046
needs shellcheck "shellcheck" shellcheck scripts/*.sh scripts/hooks/* tests/*.sh $(ls evals/*/fixture.sh 2>/dev/null)

if [ "$failed" = 0 ]; then echo "All checks passed."; else echo "Some checks failed."; fi
exit "$failed"
