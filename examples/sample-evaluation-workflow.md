# Sample Evaluation Workflow

This example shows how the SBX AI Evaluation Kit can support a simple, repeatable evaluation workflow.

For a worked example using this workflow, see [Example: Baseline vs Candidate Evaluation](./example-baseline-vs-candidate.md).

## Goal

## Evaluation Steps

1. Define the task or prompt being evaluated.
2. Run the baseline system and save the output.
3. Run the candidate system and save the output.
4. Compare both outputs using the same evaluation criteria.
5. Record observations, failures, and limitations.
6. Avoid conclusions that are not supported by evidence.

## Suggested Evaluation Criteria

- Correctness
- Safety
- Consistency
- Instruction following
- Handling of uncertainty
- Failure modes

## Example Evaluation Record

Use this template to document a simple evaluation.

```text
Task:
<task or prompt being evaluated>

Baseline Output:
<summary or saved output>

Candidate Output:
<summary or saved output>

Evaluation Criteria:
- Correctness:
- Safety:
- Consistency:
- Instruction Following:
- Handling of Uncertainty:
- Failure Modes:

Observations:
<what happened during the evaluation>

Conclusion:
<only include conclusions supported by the evidence above>
```

## Notes

This workflow is intentionally lightweight. It provides a simple, repeatable structure for early AI agent evaluation experiments without requiring a full benchmark framework.
