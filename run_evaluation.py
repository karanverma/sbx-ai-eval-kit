import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from evidence.runtime import validate_runtime_evidence
from executors.factory import get_executor


REQUIRED_FIELDS = {
    "schema_version": str,
    "evaluation_id": str,
    "objective": str,
    "conditions": list,
    "baseline": dict,
    "candidate": dict,
    "criteria": list,
    "observations": list,
    "decision": str,
}


def load_evaluation(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Evaluation configuration must be a YAML mapping")

    return data


def validate(data: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    for field, expected_type in REQUIRED_FIELDS.items():
        value = data[field]

        if not isinstance(value, expected_type):
            raise ValueError(
                f"Field '{field}' must be of type "
                f"{expected_type.__name__}"
            )

    if data["schema_version"] != "1":
        raise ValueError(
            f"Unsupported schema_version: {data['schema_version']}"
        )

    for field in ("evaluation_id", "objective", "decision"):
        if not data[field].strip():
            raise ValueError(f"Field '{field}' must not be empty")

    for participant in ("baseline", "candidate"):
        record = data[participant]

        for required_field in ("name", "output"):
            if required_field not in record:
                raise ValueError(
                    f"Field '{participant}' must contain "
                    f"'{required_field}'"
                )

            if not isinstance(record[required_field], str):
                raise ValueError(
                    f"Field '{participant}.{required_field}' "
                    "must be a string"
                )

            if not record[required_field].strip():
                raise ValueError(
                    f"Field '{participant}.{required_field}' "
                    "must not be empty"
                )

    for index, criterion in enumerate(data["criteria"]):
        if not isinstance(criterion, dict):
            raise ValueError(
                f"Criterion at index {index} must be a mapping"
            )

        required_criterion_fields = {
            "name",
            "baseline",
            "candidate",
            "assessment",
        }

        missing_criterion_fields = (
            required_criterion_fields - criterion.keys()
        )

        if missing_criterion_fields:
            raise ValueError(
                f"Criterion at index {index} is missing fields: "
                f"{sorted(missing_criterion_fields)}"
            )

    validate_execution_config(data.get("execution"))


def validate_execution_config(execution: Any) -> None:
    if execution is None:
        return

    if not isinstance(execution, dict):
        raise ValueError("Field 'execution' must be a mapping")

    executor_name = execution.get("executor", "local")
    command = execution.get("command")

    if not isinstance(executor_name, str) or not executor_name.strip():
        raise ValueError("execution.executor must be a non-empty string")

    if executor_name not in {"local", "sbx"}:
        raise ValueError(f"Unsupported executor: {executor_name}")

    if not isinstance(command, list) or not command:
        raise ValueError("execution.command must be a non-empty list")

    if not all(isinstance(item, str) and item for item in command):
        raise ValueError(
            "Every execution.command item must be a non-empty string"
        )


def calculate_source_digest(data: dict[str, Any]) -> str:
    canonical_source = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(
        canonical_source.encode("utf-8")
    ).hexdigest()


def validate_suite_config(data: dict[str, Any]) -> None:
    if "evaluations" not in data:
        raise ValueError("Suite configuration must contain 'evaluations'")

    evaluations = data["evaluations"]

    if not isinstance(evaluations, list):
        raise ValueError("Field 'evaluations' must be a list")

    for index, evaluation in enumerate(evaluations):
        if not isinstance(evaluation, dict):
            raise ValueError(
                f"Suite evaluation at index {index} must be a mapping"
            )

        validate(evaluation)


def execute_runtime(data: dict[str, Any]) -> dict[str, Any] | None:
    execution = data.get("execution")

    if execution is None:
        return None

    validate_execution_config(execution)

    evidence = get_executor(execution.get("executor", "local")).execute(
        execution["command"]
    )
    validate_runtime_evidence(evidence)

    return evidence


def build_result(data: dict[str, Any]) -> dict[str, Any]:
    result = {
        "artifact_schema_version": "1",
        "evaluation_id": data["evaluation_id"],
        "objective": data["objective"],
        "conditions": data["conditions"],
        "baseline": data["baseline"],
        "candidate": data["candidate"],
        "criteria": data["criteria"],
        "observations": data["observations"],
        "decision": data["decision"],
        "provenance": {
            "source_sha256": calculate_source_digest(data),
        },
    }

    runtime_evidence = execute_runtime(data)

    if runtime_evidence is not None:
        result["runtime_evidence"] = runtime_evidence

    return result


def build_suite_result(data: dict[str, Any]) -> dict[str, Any]:
    validate_suite_config(data)

    results: list[dict[str, Any]] = []
    successful = 0
    failed = 0

    for evaluation in data["evaluations"]:
        result = build_result(evaluation)
        results.append(result)

        runtime_evidence = result.get("runtime_evidence")

        if runtime_evidence is None:
            successful += 1
        elif runtime_evidence.get("exit_code") == 0:
            successful += 1
        else:
            failed += 1

    return {
        "artifact_schema_version": "1",
        "summary": {
            "total": len(results),
            "successful": successful,
            "failed": failed,
        },
        "results": results,
    }


def write_result(result: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False,
        )
        file.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an AI evaluation record and generate an "
            "execution-backed JSON artifact."
        )
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the evaluation YAML file",
    )

    parser.add_argument(
        "--input",
        dest="input_option",
        type=Path,
        default=None,
        help="Path to the evaluation YAML file",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path for the generated JSON artifact",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = args.input_option or args.input_path or Path("evaluation.yaml")
    output_path = args.output or Path("evaluation-result.json")

    data = load_evaluation(input_path)

    if "evaluations" in data:
        result = build_suite_result(data)
        output_path = args.output or Path("evaluation-results.json")
    else:
        validate(data)
        result = build_result(data)

    write_result(result, output_path)

    print(f"{output_path} created")


if __name__ == "__main__":
    main()
