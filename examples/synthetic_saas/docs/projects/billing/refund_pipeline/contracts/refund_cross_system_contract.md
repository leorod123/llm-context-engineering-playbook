---
id: refund_cross_system_contract
title: Refund Cross-System Contract
doc_type: contract
status: active
created_at: 2026-01-01T00:00:00Z
updated_at: 2026-01-01T00:00:00Z
systems:
  - billing
  - notifications
  - scheduler
authority: operational_contract
include_in_registry: true
validation_state: structurally_validated
semantic_status: partially_validated
bot_usage: restricted
evidence_status: partial
project_id: refund_pipeline
components:
  - refund_worker
  - customer_email
  - retry_job
tags:
  - refunds
  - cross-system
cross_system_impact: confirmed
downstream_systems:
  - notifications
  - scheduler
known_boundaries:
  - refund worker must not send customer emails directly
  - retry scheduling must remain idempotent
---
# Refund Cross-System Contract

Refund behavior crosses three systems:

- billing owns the refund state transition
- notifications owns customer-facing messages
- scheduler owns retry timing

Agents must not patch refund logic as if billing were the only affected system.
