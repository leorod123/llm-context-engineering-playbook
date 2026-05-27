# Pre-Publish Adversarial Review

This review lists the objections a rigorous reviewer is likely to raise and how
the repository addresses them.

## Claim Inflation

Risk: the evaluation could be read as a broad claim that the playbook improves
all LLM work by the same amount.

Mitigation:

- `README.md` describes the result as a fixture-based synthetic evaluation.
- `evals/README.md` includes a threats-to-validity section.
- `evals/manual_protocol.md` explains how to replace fixtures with captured
  outputs from a real model.
- The scorer emits `benchmark_scope: synthetic_fixture_answers`.

Residual limitation: the included result is evidence for the target failure
modes, not a universal LLM benchmark.

## Cherry-Picked Evidence

Risk: a reviewer may suspect that only successful examples were shown.

Mitigation:

- All five scenarios are stored in `evals/scenarios.json`.
- Baseline and playbook answers are checked in under `evals/runs/`.
- `evals/examples.md` shows a full prompt -> baseline -> playbook -> score
  walkthrough.
- The scorer reports per-scenario distribution, not only the final total.

Residual limitation: the dataset is deliberately small so it remains readable.

## Weak Scoring Method

Risk: deterministic keyword scoring can be gamed.

Mitigation:

- The scoring method is explicitly named in the JSON output.
- The README calls out that the scorer is auditable but not semantically deep.
- The manual protocol requires publishing raw answers and model settings when
  reporting real-model results.

Residual limitation: a stronger future version could add human review or a
second scoring layer.

## Privacy Leakage

Risk: public examples could accidentally reveal private project details.

Mitigation:

- The example domain is fictional SaaS billing.
- The README privacy section tells users to publish fictional or sanitized
  fixtures only.
- Generated JSON outputs are ignored because they can include local paths.
- The current pre-publish scan found no private-source markers, local absolute
  paths, credentials, or project-specific architecture names in tracked content.

Residual limitation: every future example should be scanned before publication.

## First-Run Reproducibility

Risk: the project may look polished but fail when a reviewer runs it.

Mitigation:

- The quick demo uses plain Python commands.
- CI runs install, registry build, validation, fixture scoring, and tests.
- Local validation passed via `PYTHONPATH=src` when editable install was blocked
  by the local Windows temp directory.

Residual limitation: local Python environments can still vary; CI is the clean
environment check.

## Scope Confusion

Risk: readers may expect a hosted RAG system, vector database, or full agent
platform.

Mitigation:

- The README states that the project is plain files plus deterministic scripts.
- The design tradeoffs section lists what is intentionally excluded.
- The method docs frame graph tools and embeddings as optional future layers,
  not as the governance authority.

Residual limitation: the project should keep this boundary clear as extensions
are added.
