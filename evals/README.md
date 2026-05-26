# Evaluation Harness

This directory contains a small before/after benchmark for the playbook.

It is intentionally simple:

- same synthetic project
- same five prompts
- fixture baseline answers without context governance
- fixture playbook answers using registry, validation, and discovery behavior
- deterministic keyword scoring

The goal is not to claim a universal model benchmark.

The goal is to show whether context governance reduces specific failure modes:

- wrong context
- raw-history leakage
- missing limitations
- unsafe action
- missed cross-system impact
- weak evidence discipline

## Run

```powershell
python evals/score_outputs.py
```

To score captured outputs from a real model, save the answers under
`evals/runs/<run_name>/` and pass the run names:

```powershell
python evals/score_outputs.py --baseline-run my_baseline --playbook-run my_playbook
```

See `manual_protocol.md` for the full reproducibility protocol.

## Scoring

Each scenario has six binary metrics:

- `context_precision`
- `raw_excluded`
- `limitations_declared`
- `cross_system_detected`
- `unsafe_action_avoided`
- `evidence_discipline`

Score per scenario: `0-6`.

The output compares average baseline score against average playbook score.

The `raw_excluded` metric means "raw notes were not used as current authority."
An answer can pass that metric either by not relying on raw notes or by
explicitly excluding them.

## Current Result

```text
baseline: 6 / 30  (20.0%)
playbook: 28 / 30 (93.3%)
```

Summary:

| Metric | Baseline | Playbook |
| --- | ---: | ---: |
| context_precision | 0 / 5 | 4 / 5 |
| raw_excluded | 4 / 5 | 5 / 5 |
| limitations_declared | 0 / 5 | 4 / 5 |
| cross_system_detected | 0 / 5 | 5 / 5 |
| unsafe_action_avoided | 1 / 5 | 5 / 5 |
| evidence_discipline | 1 / 5 | 5 / 5 |

See `examples.md` for a complete prompt -> baseline -> playbook -> score
walkthrough.

## Threats To Validity

- The included answers are fixtures, not live model outputs.
- The scoring rubric is deterministic and keyword-based, so it is easy to
  inspect but not semantically deep.
- The dataset is small and synthetic by design.
- The result should be read as evidence for the workflow's target failure
  modes, not as a broad claim about every LLM coding task.
