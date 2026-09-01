# Reproducibility Notes

Agent evaluation becomes difficult when each run uses a different environment, dependency set, tool version, or local configuration.

This project focuses on the first layer of reproducibility: creating a repeatable sandbox environment for AI agent evaluation.

## Why Reproducibility Matters

When evaluating AI agents, small environment differences can affect results. A missing dependency, changed package version, different network access rule, or local configuration difference can make two evaluation runs harder to compare.

A repeatable environment helps make evaluation results easier to inspect, compare, and discuss.

## Initial Reproducibility Goals

The first version focuses on:

- Fixed environment setup
- Lightweight evaluation tooling
- Repeatable workflow templates
- Clear evaluation artifacts
- Documentation of assumptions and limitations

## What This Does Not Solve Yet

This project does not yet provide:

- A full benchmark harness
- Automated LLM-as-a-judge scoring
- Multi-agent evaluation orchestration
- Production-grade experiment tracking

These may be explored later after the basic reproducibility layer becomes more useful.

## Current State

The workflow now supports executable evaluations using either the local
executor or Docker Sandboxes (SBX). Each executed evaluation records structured
runtime evidence including the command, stdout, stderr, exit code, and execution
duration.

Evaluation suites extend the same workflow across multiple evaluation
definitions while producing individual results and an aggregated summary.

## Next Direction

A useful next step is reproducibility verification: rerunning a previous
evaluation under comparable conditions and identifying meaningful execution
drift between runs.
