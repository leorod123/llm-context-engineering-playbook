# Failure Modes And Countermeasures

| Failure mode | Symptom | Countermeasure |
| --- | --- | --- |
| Overcontext | Agent blends stale and current docs | Registry excludes `raw/`; discovery returns small ranked context |
| Undercontext | Agent patches a local symptom | Discovery asks for system, component, project, or tag |
| Authority confusion | Draft treated as contract | `authority`, `bot_usage`, and `evidence_status` are required |
| False closure | Files exist, project marked done | Promotion requires validated semantics and evidence |
| Suspicion becomes cause | Audit jumps into patching | Investigative audit requires refuting evidence and limitations |
| Cross-system drift | Local change breaks downstream | Cross-system impact fields and contracts are explicit |

## A Useful Rule

When the registry cannot return safe context, that is not a failure of the
agent.

It is evidence that the project memory is not mature enough yet.
