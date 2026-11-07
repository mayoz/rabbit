#!/usr/bin/env bash
set -e
g() { git -c user.name=fixture -c user.email=fixture@example.com "$@"; }
repo() {
  mkdir -p "$1" && g -C "$1" init -q -b main
  echo "# $1" > "$1/README.md"
  g -C "$1" add README.md && g -C "$1" commit -q -m init
  g -C "$1" checkout -q -b feature/ABC-2
}
repo producer
cat > producer/export.py <<'PY'
import json


def campaign_paused(campaign):
    return json.dumps({"campaign_id": campaign.id, "status": "paused"})
PY
g -C producer add export.py && g -C producer commit -q -m "ABC-2 | Publish paused campaigns"
repo consumer
cat > consumer/listener.py <<'PY'
import json


def on_message(body, store):
    event = json.loads(body)
    if event["status"] == "paused":
        store.pause(event["campaignId"])
PY
g -C consumer add listener.py && g -C consumer commit -q -m "ABC-2 | Pause campaigns on event"
cat > brief.md <<'MD'
# ABC-2 brief

When a campaign is paused in the producer, the consumer must pause it too, through a
`campaign.paused` message.
MD
cat > spec.md <<'MD'
# ABC-2 spec

The producer publishes `{"campaign_id": <id>, "status": "paused"}`
(`producer/export.py`). The consumer reads the message in `consumer/listener.py` and
pauses that campaign.

Acceptance: pausing a campaign in the producer pauses the same campaign in the consumer.
MD
cat > impact.md <<'MD'
| Surface | Kind | Producer | Consumers (path:line) | Contract test |
| --- | --- | --- | --- | --- |
| campaign.paused message | payload | producer/export.py:5 | consumer/listener.py:7 | none |
MD
