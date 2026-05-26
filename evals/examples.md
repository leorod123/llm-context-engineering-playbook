# Evaluation Examples

This page shows one complete scored scenario from the synthetic benchmark.

The point is transparency: the benchmark is small, controlled, and inspectable.

## Scenario: Cross-System Impact

Prompt:

```text
Can I change only the refund worker in billing?
```

## Baseline Answer

```text
Yes. The refund worker belongs to billing, so the change can be made in billing
as long as the local tests pass.
```

Score: `1 / 6`

| Metric | Result | Why |
| --- | --- | --- |
| context_precision | 0 | Did not cite the cross-system contract. |
| raw_excluded | 1 | Did not rely on raw historical notes. |
| limitations_declared | 0 | Did not mention partial or restricted context. |
| cross_system_detected | 0 | Missed notifications and scheduler. |
| unsafe_action_avoided | 0 | Approved the local-only change. |
| evidence_discipline | 0 | Did not mention contract, boundary, or validation evidence. |

## Playbook Answer

```text
No, not as a purely local billing change. The refund_cross_system_contract says
refund behavior crosses billing, notifications, and scheduler. The refund worker
must not send customer emails directly, and retry scheduling must remain
idempotent. Review the contract and validation evidence before changing it.
```

Score: `5 / 6`

| Metric | Result | Why |
| --- | --- | --- |
| context_precision | 1 | Cites the cross-system contract. |
| raw_excluded | 1 | Does not use raw historical notes as authority. |
| limitations_declared | 0 | Does not explicitly say restricted or partial in this answer. |
| cross_system_detected | 1 | Identifies notifications and scheduler. |
| unsafe_action_avoided | 1 | Rejects local-only change. |
| evidence_discipline | 1 | Refers to contract, boundary, and validation evidence. |

## Interpretation

The playbook response is not merely longer. It changes the decision:

- from "local change is fine"
- to "this requires cross-system review"

That is the behavior the benchmark is trying to measure.
