# Action Mode Contract

## Purpose

Before meaningful work, the agent declares what kind of work it is doing.

This prevents an audit from silently becoming a patch, or a corrective patch
from becoming promotion.

## Action Modes

### `read_only_analysis`

Allowed:

- inspect docs, code, registry output, and generated artifacts
- summarize limitations

Forbidden:

- patching
- maturity promotion

### `investigative_audit`

Allowed:

- test a suspicion
- collect confirming and refuting evidence
- stop at uncertainty

Forbidden:

- patching in the same action
- treating plausible narrative as confirmed cause

### `corrective_patch`

Allowed:

- fix metadata
- repair registry structure
- move raw material out of default context

Forbidden:

- promoting `bot_usage`
- declaring project closure

### `canonical_migration`

Allowed:

- create canonical project structure
- preserve historical material under `raw/`
- normalize metadata

Forbidden:

- claiming strong validation without evidence

### `semantic_validation`

Allowed:

- compare stated intent, implementation, and evidence
- update semantic status when supported

Forbidden:

- treating inference as evidence

### `promotion_or_closure`

Allowed:

- mark context as bot-safe only when all gates pass

Required:

- validated semantics
- validated evidence
- readiness record

## Minimum Declaration

```text
action_mode:
reason:
allowed_changes:
forbidden_changes:
required_validation_after_change:
```
