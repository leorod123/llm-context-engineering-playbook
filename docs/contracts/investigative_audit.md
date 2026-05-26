# Investigative Audit Contract

## Core Rule

An investigative audit tests a suspicion. It does not make the system look
finished.

## Required Fields

Every investigative audit records:

- exact question
- hypothesis under test
- evidence that would confirm it
- evidence that would refute it
- direct evidence
- indirect evidence
- contrary evidence
- negative results
- alternative hypotheses
- limitations
- confidence
- safe next step

## Finding Status

Allowed values:

- `confirmed`
- `likely`
- `possible`
- `refuted`
- `blocked_by_missing_evidence`

## Evidence Strength

Allowed values:

- `direct`
- `indirect`
- `mixed`
- `missing`

## Forbidden Moves

Do not patch, promote, or close a project inside the same investigative audit.

Open a separate action mode for the next step.
