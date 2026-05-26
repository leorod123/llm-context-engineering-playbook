# Manual Evaluation Protocol

The bundled evaluation uses synthetic fixture answers so the repository can be
audited without calling an external model. To test a real model, replace the
fixtures with captured outputs from the same model, same settings, and same
scenario prompts.

## Goal

Measure whether the playbook changes agent behavior on the failure modes it is
designed for:

- selecting the right context
- keeping raw notes out of default authority
- declaring limitations
- avoiding unsafe action
- detecting cross-system impact
- grounding conclusions in evidence

This is not a general LLM benchmark. It is a controlled workflow evaluation.

## Procedure

1. Choose one model, model version, temperature, and tool setting.
2. Record those settings in a short note next to the captured answers.
3. For each scenario in `scenarios.json`, ask the prompt without providing the
   playbook workflow. Save each answer under a new run folder, for example
   `evals/runs/my_baseline/context_retrieval.md`.
4. Build and validate the synthetic example registry:

   ```powershell
   python -m context_governance build --root examples/synthetic_saas
   python -m context_governance validate --root examples/synthetic_saas
   python -m context_governance discover --root examples/synthetic_saas --system billing
   ```

5. Ask the same model the same scenario prompts, this time providing the
   relevant playbook rules and discovery output. Save those answers under a
   second run folder, for example `evals/runs/my_playbook/`.
6. Score both runs:

   ```powershell
   python evals/score_outputs.py --baseline-run my_baseline --playbook-run my_playbook
   ```

7. Report the totals, per-scenario distribution, model/settings, and observed
   limitations.

## Reporting Standard

When publishing results, include:

- the scenario prompts
- raw model answers
- scoring script version
- model and settings used
- any prompt or tool context provided
- limitations and known threats to validity

Do not report the included fixture result as a live model benchmark unless the
answers were actually captured from a live model under this protocol.
