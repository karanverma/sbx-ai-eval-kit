# SBX AI Evaluation Kit

A Docker Sandbox (SBX) Mixin Kit for building reproducible AI agent evaluation workflows.

## Motivation

As AI agents become more capable and autonomous, evaluating their behavior consistently becomes increasingly important. Small differences in environment, dependencies, tooling, or local configuration can make evaluation results difficult to reproduce and compare.

This project explores how Docker Sandbox Kits can provide reusable, isolated environments for benchmarking, testing, and evaluating AI agents.

The initial focus is simple: make evaluation workflows more repeatable before tackling more advanced evaluation challenges.

## Goals

- Reproducible AI evaluation environments
- Fixed dependencies for more consistent evaluation runs
- Evaluation-focused agent instructions
- Repeatable baseline vs. candidate workflows
- Clear documentation of observations, failures, and limitations
- Support evaluation workflows informed by AI safety and governance practices

## What This Kit Provides

- Structured evaluation configuration (`evaluation.yaml`)
- Deterministic evaluation artifact generation (`run_evaluation.py`)
- Machine-readable evaluation artifact generation
- Unit tests
- GitHub Actions CI
- Sample evaluation workflow
- Reproducibility guidance
- Roadmap

## Example Use Cases

- Prompt evaluation
- Baseline vs. candidate comparison
- Agent workflow testing
- Safety evaluation experiments
- Reproducibility testing

## Status

This repository is an executable prototype for reproducible AI evaluation workflows built around Docker Sandbox Kits.

The current implementation includes:

- a structured evaluation configuration,
- deterministic evaluation artifact generation,
- pinned dependencies,
- agent-context guidance,
- unit tests,
- a reproducible smoke test,
- and GitHub Actions CI.

The included evaluation is intentionally illustrative. The current workflow validates and converts a human-authored evaluation record into a machine-readable artifact; it does not yet execute models or derive judgments automatically.

## Quick Start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the complete workflow:

```bash
./scripts/smoke-test.sh
```

Or run the steps individually:

```bash
python run_evaluation.py
pytest
```

This regenerates `evaluation-result.json`, validates the generated artifact, and runs the unit tests.
