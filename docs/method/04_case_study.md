# Synthetic Case Study

This repository includes a fictional SaaS project with three systems:

- `billing`
- `notifications`
- `scheduler`

The scenario:

> The team wants coding agents to reason about refund processing without reading
> every old incident note and without treating partial audits as validated truth.

The example shows:

- a canonical project home for `refund_pipeline`
- a contract that defines cross-system impact
- an audit that is restricted because evidence is only partial
- registry build and validation
- discovery returning small context with limitations

Run:

```powershell
python -m context_governance build --root examples/synthetic_saas
python -m context_governance validate --root examples/synthetic_saas
python -m context_governance discover --root examples/synthetic_saas --system billing
```

The important part is not the fictional domain. The important part is that the
agent receives context with maturity, limitations, and reasons attached.
