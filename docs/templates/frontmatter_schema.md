# Frontmatter Schema

Minimum frontmatter for indexed docs:

```yaml
---
id: <unique_doc_id>
title: <human_title>
doc_type: project | audit | architecture | runbook | decision | validation | maintenance | incident | contract | reference
status: draft | active | implemented | validated | superseded | archived | rejected
created_at: <ISO8601 UTC>
updated_at: <ISO8601 UTC>
systems:
  - <system_slug>
authority: primary_architecture | operational_contract | project_memory | audit_summary | validation_evidence | historical_context | secondary_semantic_context | exploratory
include_in_registry: true
validation_state: unvalidated | structurally_validated | implementation_validated | semantically_validated | runtime_validated
semantic_status: validated | partially_validated | unvalidated | invalid
bot_usage: allowed | restricted | forbidden
evidence_status: none | hypothesis | partial | validated
---
```

Recommended fields:

```yaml
project_id: <project_id>
components:
  - <component_slug>
tags:
  - <tag>
cross_system_impact: none | possible | confirmed
upstream_systems:
  - <system_slug>
downstream_systems:
  - <system_slug>
required_contracts:
  - <contract_id>
known_boundaries:
  - <doc_path_or_rule>
```
