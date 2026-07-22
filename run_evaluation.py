import json
import hashlib
from pathlib import Path

import yaml


def load_evaluation(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(data):
    required = [
        "schema_version",
        "evaluation_id",
        "objective",
        "conditions",
        "baseline",
        "candidate",
        "criteria",
        "observations",
        "decision",
    ]

    missing = [k for k in required if k not in data]

    if missing:
        raise ValueError(f"Missing fields: {missing}")


def build_result(data):
    digest = hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

    return {
        "artifact_schema_version": "1",
        "evaluation_id": data["evaluation_id"],
        "objective": data["objective"],
        "decision": data["decision"],
        "criteria": data["criteria"],
        "observations": data["observations"],
        "provenance": {
            "source_sha256": digest
        }
    }


def main():
    config = Path("evaluation.yaml")

    data = load_evaluation(config)

    validate(data)

    result = build_result(data)

    with open("evaluation-result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("evaluation-result.json created")


if __name__ == "__main__":
    main()
