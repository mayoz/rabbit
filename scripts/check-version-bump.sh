#!/usr/bin/env bash
# Usage: check-version-bump.sh <base-ref>
# When skills/, agents/, hooks/, .claude-plugin/ or a doc setup reads changed since <base-ref>, the plugin version must
# be higher than the base and CHANGELOG.md must have a "## [<version>]" heading.
set -euo pipefail
base=$1
git diff --quiet "$base" -- skills agents hooks .claude-plugin docs/profile.md docs/workflow.md && exit 0
version() { python3 -I -c 'import json,sys; print(json.load(sys.stdin)["version"])'; }
new=$(version < .claude-plugin/plugin.json)
old=$(git show "$base:.claude-plugin/plugin.json" 2>/dev/null | version || echo none)
if [ "$new" = "$old" ]; then
  echo "Plugin files changed but version is still $new: bump .claude-plugin/plugin.json"; exit 1
fi
if [ "$old" != none ] && python3 -I -c 'import sys; v=lambda s: tuple(int(x) for x in s.split("-")[0].split(".")); sys.exit(v(sys.argv[1]) > v(sys.argv[2]))' "$new" "$old"; then
  echo "Version $new is lower than $old"; exit 1
fi
if ! grep -qF "## [$new]" CHANGELOG.md; then
  echo "CHANGELOG.md has no '## [$new]' section"; exit 1
fi
