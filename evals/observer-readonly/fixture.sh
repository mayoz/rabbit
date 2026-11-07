#!/usr/bin/env bash
cat > brief.md <<'MD'
# ABC-1 brief

## What happened
The login page shows a blank screen after the session expires (description).

## Where to start
`src/login.js:12` renders the form.
MD
