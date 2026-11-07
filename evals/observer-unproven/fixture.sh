#!/usr/bin/env bash
set -e
g() { git -c user.name=fixture -c user.email=fixture@example.com "$@"; }
mkdir -p shop && g -C shop init -q -b main
cat > shop/checkout.py <<'PY'
def total(items):
    return sum(item.price * item.quantity for item in items)
PY
g -C shop add checkout.py && g -C shop commit -q -m init
cat > brief.md <<'MD'
# ABC-3 brief

The checkout total must include every item's quantity.
MD
cat > spec.md <<'MD'
# ABC-3 spec

`total(items)` in `shop/checkout.py:2` multiplies each item's price by its quantity and sums
them. The payment provider retries a failed charge 3 times before it gives up.

Acceptance: an order of 2 items at 5 costs 10.
MD
