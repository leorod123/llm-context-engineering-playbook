# Cross-System Impact Contract

## Purpose

Some changes look local but affect another system.

## Required Declarations

Use these frontmatter fields when applicable:

```yaml
cross_system_impact: possible | confirmed
upstream_systems:
  - <system>
downstream_systems:
  - <system>
required_contracts:
  - <contract_id>
known_boundaries:
  - <doc_path_or_rule>
```

## Gate

When impact is confirmed, discovery and validation should expose the downstream
relationship. The agent should not treat the task as a purely local change.
