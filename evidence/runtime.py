from typing import Any


def validate_runtime_evidence(evidence: dict[str, Any]) -> None:
    required = {
        "executor": str,
        "command": list,
        "stdout": str,
        "stderr": str,
        "exit_code": int,
        "duration_ms": (int, float),
    }

    for field, expected_type in required.items():
        if field not in evidence:
            raise ValueError(f"Missing runtime evidence field: {field}")

        if not isinstance(evidence[field], expected_type):
            raise ValueError(
                f"Runtime evidence field '{field}' has invalid type"
            )

    if not evidence["command"]:
        raise ValueError("Runtime evidence command cannot be empty")

    if not all(isinstance(item, str) for item in evidence["command"]):
        raise ValueError("Runtime evidence command items must be strings")

    if evidence["duration_ms"] < 0:
        raise ValueError("Runtime evidence duration cannot be negative")
