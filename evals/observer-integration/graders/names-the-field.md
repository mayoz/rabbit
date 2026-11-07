---
type: llm
---

PASS if the reported review says the producer sends `campaign_id` while the
consumer reads `campaignId`, so the consumer breaks.
FAIL if it misses this mismatch or approves the change.
