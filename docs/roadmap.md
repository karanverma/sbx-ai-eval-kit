## Version 0.5 (Current)

Evaluation execution with runtime evidence and evaluation suite support.

### Completed

* Structured evaluation configuration (`evaluation.yaml`)
* Deterministic evaluation runner (`run_evaluation.py`)
* Local command execution
* Docker Sandboxes (SBX) command execution
* Machine-readable evaluation artifacts with runtime evidence
* Evaluation suites with aggregated results
* Unit tests
* GitHub Actions CI
* Reproducible smoke-test workflow

### Success Criteria

* ✅ Repeatable evaluation execution
* ✅ Machine-readable evaluation artifacts
* ✅ Clear distinction between illustrative and executed results
* ✅ Runtime evidence captured for executed evaluations
* ✅ Multiple evaluations supported through suites
* ✅ Automated validation through GitHub Actions

### Current Scope

The implementation executes configured evaluation commands using either the
local executor or Docker Sandboxes (SBX) and records structured runtime evidence.

The included evaluations remain intentionally illustrative. The project does
not yet execute AI models or automatically derive evaluation judgments.

### Next Direction

* Reproducibility verification and replay
* Detection of meaningful execution drift
* Richer evaluation workloads
* Additional artifact and failure-handling support
