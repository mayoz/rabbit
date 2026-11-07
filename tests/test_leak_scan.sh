#!/usr/bin/env bash
set -u
scan="$(cd "$(dirname "$0")/.." && pwd)/scripts/leak-scan.sh"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0
check() { # name expected-exit text [denylist-line] [expected-output]
  local f="$tmp/$1.md" dl="$tmp/$1.deny" out code
  printf '%s\n' "$3" > "$f"; printf '%s\n' "${4:-}" > "$dl"
  out=$(HOME="$tmp" LEAK_PATTERNS='' "$scan" --denylist "$dl" "$f" 2>&1); code=$?
  if [ "$code" != "$2" ] || { [ -n "${5:-}" ] && ! grep -q -- "$5" <<<"$out"; }; then
    echo "FAIL $1: exit=$code out=$out"; fail=1
  else echo "ok   $1"; fi
}
check custom-field 1 'field customfield_10000' '' 'customfield_'
check custom-field-placeholder 0 'field customfield_<id>'
check example-site 0 'https://acme.atlassian.net/browse/ABC-1'
check placeholder-site 0 'https://<site>.atlassian.net'
check real-site 1 'https://bigco.atlassian.net'
check email 1 'mail jane.doe@bigco.com'
check allowed-email 0 'noreply@anthropic.com and dev@example.com'
check home-path 1 'see /Users/jane/x'
check token 1 'ghp_abcdef123'
check denylist 1 'Built at SecretCorp' 'secretcorp' 'SecretCorp'
check clean 0 'nothing to see'
exit $fail
