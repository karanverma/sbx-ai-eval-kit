import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


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

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

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


def build_result(data: dict[str, Any]) -> dict[str, Any]:
    return {
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
            "Validate an AI evaluation record and generate a "
            "deterministic JSON artifact."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("evaluation.yaml"),
        help="Path to the evaluation YAML file",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evaluation-result.json"),
        help="Path for the generated JSON artifact",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data = load_evaluation(args.input)
    validate(data)

    result = build_result(data)
    write_result(result, args.output)

    print(f"{args.output} created")


if __name__ == "__main__":
    main()
