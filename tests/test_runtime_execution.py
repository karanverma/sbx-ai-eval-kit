import sys

import pytest

from evidence.runtime import validate_runtime_evidence
from executors.local import LocalExecutor
from run_evaluation import build_result, validate


def valid_evaluation() -> dict:
    return {
        "schema_version": "1",
        "evaluation_id": "runtime-evaluation",
        "objective": "Verify runtime evidence capture",
        "conditions": [],
        "baseline": {
            "name": "baseline",
            "output": "baseline output",
        },
        "candidate": {
            "name": "candidate",
            "output": "candidate output",
        },
        "criteria": [],
        "observations": [],
        "decision": "candidate accepted",
    }


def test_local_executor_captures_success() -> None:
    evidence = LocalExecutor().execute(
        [sys.executable, "-c", "print('runtime works')"]
    )

    validate_runtime_evidence(evidence)

    assert evidence["executor"] == "local"
    assert evidence["exit_code"] == 0
    assert evidence["stdout"] == "runtime works\n"
    assert evidence["stderr"] == ""
    assert evidence["duration_ms"] >= 0


def test_local_executor_captures_failure() -> None:
    evidence = LocalExecutor().execute(
        [
            sys.executable,
            "-c",
            "import sys; print('failure', file=sys.stderr); sys.exit(3)",
        ]
    )

    validate_runtime_evidence(evidence)

    assert evidence["exit_code"] == 3
    assert evidence["stdout"] == ""
    assert evidence["stderr"] == "failure\n"


def test_result_contains_runtime_evidence() -> None:
    evaluation = valid_evaluation()
    evaluation["execution"] = {
        "executor": "local",
        "command": [
            sys.executable,
            "-c",
            "print('artifact evidence')",
        ],
    }

    validate(evaluation)
    result = build_result(evaluation)

    assert result["runtime_evidence"]["exit_code"] == 0
    assert (
        result["runtime_evidence"]["stdout"]
        == "artifact evidence\n"
    )


def test_result_without_execution_remains_backward_compatible() -> None:
    evaluation = valid_evaluation()

    validate(evaluation)
    result = build_result(evaluation)

    assert "runtime_evidence" not in result


def test_invalid_execution_command_is_rejected() -> None:
    evaluation = valid_evaluation()
    evaluation["execution"] = {
        "executor": "local",
        "command": "python script.py",
    }

    with pytest.raises(
        ValueError,
        match="execution.command must be a non-empty list",
    ):
        validate(evaluation)


def test_unsupported_executor_is_rejected() -> None:
    evaluation = valid_evaluation()
    evaluation["execution"] = {
        "executor": "sbx",
        "command": ["echo", "test"],
    }

    with pytest.raises(ValueError, match="Unsupported executor"):
        validate(evaluation)
