# The Problem

LLM coding agents are strong at local reasoning and weak at unmanaged project
memory.

In a real codebase, the agent is usually surrounded by:

- old plans
- incomplete audits
- partially true design notes
- stale generated reports
- current contracts
- runtime evidence
- raw chat exports
- migration leftovers

Without governance, the agent has no reliable way to know which material is
current, which material is historical, and which material is safe to act on.

## Common Failure Modes

### Overcontext

The agent reads too much, including stale or low-authority material, and blends
it into a confident but wrong conclusion.

### Undercontext

The agent reads too little, misses a boundary, and applies a local fix that
breaks a downstream behavior.

### Authority Confusion

A note, hypothesis, or migration draft gets treated as if it were a validated
contract.

### False Closure

A project is marked complete because its files exist, not because the behavior
has been validated.

### Suspicion Becomes Cause

An audit finds a plausible explanation and the agent patches immediately,
without testing contrary evidence.

## Goal

The goal is not to make the agent read everything.

The goal is to make the agent retrieve a small, explainable, maturity-aware
context set and know when it must declare limitations.
