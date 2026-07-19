# Example: Baseline vs Candidate Evaluation

## Purpose

This example demonstrates a simple, reproducible workflow for comparing two AI-generated solutions to the same engineering task.

The example uses illustrative evaluation fixtures to demonstrate the evaluation process. It is not intended to benchmark any specific model or provider.

---

## Evaluation Objective

Determine whether the candidate implementation satisfies the evaluation requirements more completely than the baseline implementation.

---

## Task

A repository contains the following function:

```python
def normalize_username(value: str) -> str:
    return value.lower()
```

Update the implementation so that it:

1. removes leading and trailing whitespace;
2. converts the value to lowercase;
3. includes automated tests covering both behaviours.

---

## Controlled Evaluation Conditions

| Item | Configuration |
|------|---------------|
| Repository state | Same starting commit |
| Task | Identical |
| Environment | Same dependency-locked execution environment |
| Verification | `pytest -q` |
| Evaluation criteria | Identical |
| Network access | Not required |

---

## Baseline Evaluation

### Implementation

```python
def normalize_username(value: str) -> str:
    return value.lower()
```

### Tests

No additional tests.

### Verification

Not executed.

---

## Candidate Evaluation

### Implementation

```python
def normalize_username(value: str) -> str:
    return value.strip().lower()
```

### Tests Added

```python
def test_normalize_username_lowercases_value():
    assert normalize_username("ALICE") == "alice"


def test_normalize_username_strips_whitespace():
    assert normalize_username("  Alice  ") == "alice"
```

### Verification

```text
$ pytest -q
3 passed
```

---

## Evaluation Results

| Criterion | Baseline | Candidate |
|-----------|----------|-----------|
| Removes surrounding whitespace | ✗ | ✓ |
| Converts to lowercase | ✓ | ✓ |
| Adds automated tests | ✗ | ✓ |
| Verification executed | ✗ | ✓ |
| Unrelated modifications | None observed | None observed |

---

## Decision

**Selected:** Candidate

The candidate satisfies every predefined evaluation criterion.

The baseline preserves the original lowercase behaviour but does not complete the requested task or provide verification evidence.

---

## Evaluation Artifacts

This evaluation records:

- evaluation objective;
- task definition;
- controlled evaluation conditions;
- observed implementation;
- verification results;
- evaluation criteria;
- final decision.

Capturing these artifacts enables evaluations to be reviewed, reproduced, and compared consistently.

---

## Extension Points

The same workflow can be extended to evaluate:

- multiple agent configurations;
- benchmark datasets;
- automated scoring pipelines;
- structured evaluation artifacts;
- reproducible sandboxed execution environments.
