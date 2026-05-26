# Workflow

## 1. Create A Canonical Project Home

Use:

```text
docs/projects/<system>/<project_id>/
```

Start with a small numbered spine:

```text
README.md
00_overview.md
01_plan.md
02_audits.md
03_implementation_log.md
04_validation.md
05_final_state.md
```

Put active rules in `contracts/` and raw history in `raw/`.

## 2. Add Frontmatter

Every indexed doc needs the minimum schema from
`docs/templates/frontmatter_schema.md`.

## 3. Build The Registry

```powershell
python -m context_governance build --root .
```

## 4. Validate

```powershell
python -m context_governance validate --root .
```

Validation blocks unsafe promotion and reports diagnostic limitations.

## 5. Discover Context

```powershell
python -m context_governance discover --root . --system billing
```

The output explains:

- which docs were selected
- why they matched
- how mature they are
- what limitations remain

## 6. Record The Work

For meaningful agent work, create an operational record:

- context used
- evidence used
- limitations
- confidence
- gate state

This makes agent behavior inspectable after the fact.
