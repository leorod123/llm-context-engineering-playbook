# Principles

## 1. The Registry Is A Selector

The registry should not be a dump of every document.

It should index only docs that declare metadata and maturity fields. Discovery
should return a small ranked set with reasons.

## 2. Raw History Is Not Default Context

Raw notes are useful for lineage and reconstruction, but they should not compete
with current project docs and contracts.

Keep raw material under `raw/` and exclude it from default discovery.

## 3. Maturity Must Be Explicit

Every indexed doc declares:

- validation state
- semantic status
- bot usage
- evidence status

This lets the agent distinguish usable context from partial context.

## 4. Promotion Is Harder Than Indexing

`include_in_registry: true` means "discoverable."

It does not mean "safe authority."

Strong bot usage requires validated semantics and validated evidence.

## 5. Audits Must Seek Refutation

A good investigative audit records what would confirm the hypothesis and what
would refute it.

Uncertainty is an acceptable outcome. False certainty is not.

## 6. Graphs Navigate; Evidence Proves

Graph tools can reveal hubs and relationships, but graph output should not
override contracts, runtime evidence, or explicit maturity gates.
