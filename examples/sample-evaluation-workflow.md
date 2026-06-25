# Sample Evaluation Workflow

This example shows how the SBX AI Evaluation Kit can support a simple, repeatable evaluation workflow.

## Goal

Compare the behavior of a baseline AI system and a candidate AI system on the same task.

## Evaluation Steps

1. Define the task or prompt being evaluated.
2. Run the baseline system and save the output.
3. Run the candidate system and save the output.
4. Compare both outputs using the same criteria.
5. Record observations, failures, and limitations.
6. Avoid conclusions that are not supported by evidence.

## Suggested Evaluation Criteria

- Correctness
- Safety
- Consistency
- Instruction following
- Handling of uncertainty
- Failure modes

## Notes

This workflow is intentionally lightweight. It is meant to provide structure for early evaluation experiments without requiring a full benchmark harness.
