# Project Placement Contract

## Canonical Layout

```text
docs/projects/<system>/<project_id>/
  README.md
  00_overview.md
  01_plan.md
  02_audits.md
  03_implementation_log.md
  04_validation.md
  05_final_state.md
  contracts/
  raw/
```

## Rules

- keep the numbered spine at the project root
- keep active rules in `contracts/`
- keep historical preservation material in `raw/`
- do not invent new root-level docs unless the project README declares them

The goal is for another bot to understand file placement without guesswork.
