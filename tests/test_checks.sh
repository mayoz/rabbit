#!/usr/bin/env bash
set -u
root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0
expect() { if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1: exit=$3, want $2"; fail=1; fi; }

mkdir -p "$tmp/size/skills/task" "$tmp/size/skills/pull"
seq 1850 > "$tmp/size/skills/task/SKILL.md"; seq 1000 > "$tmp/size/skills/pull/SKILL.md"
"$root/scripts/check-skill-size.sh" "$tmp/size" >/dev/null; expect size-at-limit 0 $?
seq 1851 > "$tmp/size/skills/task/SKILL.md"
"$root/scripts/check-skill-size.sh" "$tmp/size" >/dev/null; expect size-over 1 $?
seq 1850 > "$tmp/size/skills/task/SKILL.md"; seq 1001 > "$tmp/size/skills/pull/SKILL.md"
"$root/scripts/check-skill-size.sh" "$tmp/size" >/dev/null; expect size-other-over 1 $?

r="$tmp/repo"; mkdir -p "$r/skills/x" "$r/.claude-plugin" "$r/hooks"
git -C "$r" init -q -b main
git -C "$r" -c user.name=t -c user.email=t@example.com commit -q --allow-empty -m init
echo '{"version": "0.1.0"}' > "$r/.claude-plugin/plugin.json"; echo '# Changelog' > "$r/CHANGELOG.md"
echo a > "$r/skills/x/SKILL.md"; echo a > "$r/hooks/h.py"
git -C "$r" add -A; git -C "$r" -c user.name=t -c user.email=t@example.com commit -q -m base
echo b > "$r/skills/x/SKILL.md"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect bump-missing 1 $?
echo '{"version": "0.1.1"}' > "$r/.claude-plugin/plugin.json"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect changelog-missing 1 $?
printf '# Changelog\n\n## [0.1.1] - 2026-01-01\n' > "$r/CHANGELOG.md"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect bump-ok 0 $?
echo '{"version": "0.0.9"}' > "$r/.claude-plugin/plugin.json"; printf '## [0.0.9]\n' > "$r/CHANGELOG.md"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect downgrade 1 $?
git -C "$r" checkout -q -- . ; echo doc > "$r/README.md"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect docs-only 0 $?
git -C "$r" checkout -q -- . ; echo b > "$r/hooks/h.py"
(cd "$r" && "$root/scripts/check-version-bump.sh" HEAD >/dev/null); expect hooks-bump-missing 1 $?
exit $fail
