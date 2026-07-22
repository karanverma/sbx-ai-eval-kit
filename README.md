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
- Deterministic evaluation runner (`run_evaluation.py`)
- Machine-readable evaluation artifact generation
- Unit tests
- GitHub Actions CI
- Sample evaluation workflow
- Reproducibility guidance
- `AGENTS.md` contributor guidance
- Roadmap

## Example Use Cases

- Prompt evaluation
- Baseline vs. candidate comparison
- Agent workflow testing
- Safety evaluation experiments
- Reproducibility testing

## Status

This repository is an executable prototype for deterministic evaluation workflows built around Docker Sandbox Kits.

The current implementation includes a structured evaluation configuration, a deterministic evaluation runner, generated evaluation artifact, unit tests, and automated validation through GitHub Actions.

The evaluation is intentionally illustrative. Future work will focus on supporting additional evaluation configurations and integrating with real Sandbox Kit validation workflows.

## Quick Start

```bash
pip install -r requirements.txt
python run_evaluation.py
pytest
```

This generates `evaluation-result.json` and verifies the evaluation runner using the unit tests.
