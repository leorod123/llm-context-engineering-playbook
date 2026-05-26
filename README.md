# LLM Context Engineering Playbook

A practical governance layer for LLM-assisted software work.

This project turns scattered project memory into small, explainable,
maturity-aware context for coding agents. It is designed for teams using tools
like Codex, Claude, Copilot-style agents, or internal LLM workflows on real
codebases where "just read the docs" is not enough.

The goal is not to make agents read more. The goal is to make them read the
right context, understand its authority, and stop when the evidence is not good
enough.

## Why I Built This

LLM coding agents are powerful, but they fail in repeatable ways when project
context is unmanaged:

- they read stale notes and treat them as current truth
- they miss important boundaries because the right context is buried
- they over-read and blend old plans, audits, and implementation details
- they patch from a plausible story before evidence confirms the cause
- they mark a project "done" because files exist, not because behavior is proven
- they treat a local change as safe even when another subsystem depends on it

This playbook is a structured answer to those failure modes. It combines
documentation architecture, registry generation, validation gates, discovery,
and audit discipline into one small workflow.

## What Problem Was I Actually Solving?

This project did not start as a documentation exercise.

It emerged from repeated audits of LLM-assisted engineering workflows, where
the same classes of failure appeared across different projects:

- agents reasoning from outdated implementation plans
- agents treating hypotheses as validated facts
- agents missing system boundaries and cross-component dependencies
- agents proposing fixes before establishing causality
- agents declaring work complete based on file presence rather than behavioral evidence
- agents losing critical context across long-running projects

The surprising observation was that many failures were not caused by model
capability limits.

They were caused by missing context governance.

The challenge became:

How do we make an agent understand not only *what information exists*, but also:

- how trustworthy it is
- how recent it is
- whether it was validated
- what system it belongs to
- what limitations still apply

This repository is an attempt to answer that question.

## Failure Modes Observed

The design was driven by recurring failure patterns observed while auditing
LLM-assisted software projects.

Examples:

### Context Drift

An implementation plan remained in project memory long after the code evolved.
The agent continued reasoning from the obsolete plan.

### Authority Collapse

Draft notes, migration plans and validated operational records were treated as
equally trustworthy.

### Semantic Validation Gap

Implementation existed, but no evidence demonstrated that behavior matched
design intent.

### Dependency Blindness

A local change appeared correct in isolation but violated assumptions held by
another subsystem.

### Context Overload

Providing more documentation reduced answer quality because relevant context
became diluted by historical material.

## What This Demonstrates

This repository is meant to show engineering judgment as much as code.

It demonstrates:

- designing failure-aware workflows for LLM-assisted development
- separating raw history from operational knowledge
- building lightweight tooling around documentation contracts
- encoding maturity and evidence into machine-readable metadata
- making context retrieval explainable instead of magical
- preventing unsafe promotion from "indexed" to "trusted"
- testing the workflow with synthetic, non-private examples

## Core Idea

Each project document declares a small frontmatter contract:

```yaml
validation_state: implementation_validated
semantic_status: partially_validated
bot_usage: restricted
evidence_status: partial
```

Those fields let the tooling answer questions like:

- Is this document discoverable?
- Is it safe for an agent to rely on?
- Is the behavior semantically validated?
- Is there evidence, or only a hypothesis?
- Does this change have cross-system impact?

The registry is a selector, not a dump.

## What Is Included

- `context_governance build`: builds a registry from docs with frontmatter
- `context_governance validate`: checks maturity and promotion rules
- `context_governance discover`: returns small, explainable context
- reusable contracts for action modes, audits, promotion, raw handling, and
  cross-system impact
- templates for canonical projects, operational records, semantic validation,
  and investigative audits
- a synthetic SaaS example that demonstrates the workflow without private data

## Quick Demo

From the repository root:

```powershell
python -m pip install -e .
python -m context_governance build --root examples/synthetic_saas
python -m context_governance validate --root examples/synthetic_saas
python -m context_governance discover --root examples/synthetic_saas --system billing
```

Expected behavior:

- build indexes the synthetic project docs
- validation passes but reports that context remains restricted
- discovery returns a small ranked context set with explicit limitations

The limitation is intentional. The example shows that discoverable context is
not automatically trusted context.

## Example Discovery Output

The discovery command returns records shaped like this:

```json
{
  "top_docs": [
    {
      "id": "refund_pipeline_validation",
      "matched_on": ["system"],
      "authority": "validation_evidence",
      "validation_state": "implementation_validated",
      "semantic_status": "partially_validated",
      "bot_usage": "restricted",
      "evidence_status": "partial"
    }
  ],
  "limitations": [
    "selected context is restricted; use it with explicit limitations",
    "selected context is not fully semantically validated"
  ]
}
```

That is the whole point: the agent gets useful context and the warning label at
the same time.

## Repository Layout

```text
docs/
  method/        Method explanation and public case study.
  contracts/     Reusable rules for agent-safe project work.
  templates/     Copyable project, audit, and validation templates.

src/
  context_governance/
    CLI and registry/discovery/validation code.

examples/
  synthetic_saas/
    Fictional project docs used to demonstrate the workflow.

tests/
  Regression tests for parser and example workflow.
```

## Workflow

1. Create canonical project docs under `docs/projects/<system>/<project_id>/`.
2. Keep raw notes and migration history under `raw/`.
3. Add frontmatter with authority, maturity, and evidence fields.
4. Build the registry.
5. Validate the registry before treating context as usable.
6. Run discovery before meaningful agent work.
7. Record context, evidence, limitations, confidence, and gate state.
8. Promote context only after semantic and evidence gates pass.

## Design Tradeoffs

This project intentionally stays small:

- no vector database
- no hosted service
- no LLM dependency
- no hidden background state

That makes the workflow easy to inspect and adapt. Teams can later connect it
to graph tools, embeddings, search indexes, or internal agent platforms, but
the governance layer works as plain files plus deterministic scripts.

## Privacy And Safety

This repository uses only synthetic examples.

## Current Status

This is an early public version of a method extracted from real LLM-assisted
engineering work. The example is deliberately small so the rules are easy to
read, run, and challenge.

Useful next extensions:

- richer schema validation
- more example projects
- CI workflow examples
- adapter prompts for Codex and Claude
- optional graph-navigation integration

