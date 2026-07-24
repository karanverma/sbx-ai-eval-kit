import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_evaluation import (
    build_result,
    calculate_source_digest,
    load_evaluation,
    validate,
)


def sample():
    return {
        "schema_version": "1",
        "evaluation_id": "demo",
        "objective": "Compare two responses",
        "conditions": ["Same task"],
        "baseline": {
            "name": "baseline",
            "output": "Baseline output",
        },
        "candidate": {
            "name": "candidate",
            "output": "Candidate output",
        },
        "criteria": [
            {
                "name": "correctness",
                "baseline": "Acceptable",
                "candidate": "Better",
                "assessment": "candidate-preferred",
            }
        ],
        "observations": ["Candidate includes validation"],
        "decision": "Prefer candidate",
    }


def test_validate_accepts_valid_evaluation():
    validate(sample())


def test_validate_rejects_missing_field():
    data = sample()
    del data["objective"]

    with pytest.raises(ValueError, match="Missing fields"):
        validate(data)


def test_validate_rejects_unsupported_schema():
    data = sample()
    data["schema_version"] = "2"

    with pytest.raises(ValueError, match="Unsupported schema_version"):
        validate(data)


def test_validate_rejects_invalid_field_type():
    data = sample()
    data["conditions"] = "Same task"

    with pytest.raises(ValueError, match="conditions"):
        validate(data)


def test_validate_rejects_incomplete_participant():
    data = sample()
    del data["baseline"]["output"]

    with pytest.raises(ValueError, match="baseline"):
        validate(data)


def test_validate_rejects_malformed_criterion():
    data = sample()
    del data["criteria"][0]["assessment"]

    with pytest.raises(ValueError, match="missing fields"):
        validate(data)


def test_build_result_preserves_evaluation_context():
    data = sample()
    result = build_result(data)

    assert result["evaluation_id"] == "demo"
    assert result["conditions"] == data["conditions"]
    assert result["baseline"] == data["baseline"]
    assert result["candidate"] == data["candidate"]
    assert result["criteria"] == data["criteria"]
    assert result["observations"] == data["observations"]
    assert "source_sha256" in result["provenance"]


def test_digest_is_deterministic():
    first = sample()
    second = sample()

    assert calculate_source_digest(first) == calculate_source_digest(second)


def test_digest_changes_when_source_changes():
    first = sample()
    second = sample()
    second["decision"] = "Prefer baseline"

    assert calculate_source_digest(first) != calculate_source_digest(second)


def test_load_evaluation_rejects_non_mapping(tmp_path):
    config = tmp_path / "invalid.yaml"
    config.write_text("- item\n- item\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a YAML mapping"):
        load_evaluation(config)


def test_cli_generates_requested_output(tmp_path):
    repository_root = Path(__file__).resolve().parents[1]
    input_path = tmp_path / "evaluation.yaml"
    output_path = tmp_path / "result.json"

    input_path.write_text(
        """
schema_version: "1"
evaluation_id: cli-demo
objective: Test CLI generation
conditions:
  - Same conditions
baseline:
  name: baseline
  output: Baseline output
candidate:
  name: candidate
  output: Candidate output
criteria:
  - name: correctness
    baseline: Acceptable
    candidate: Better
    assessment: candidate-preferred
observations:
  - Candidate is better
decision: Prefer candidate
""".strip(),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(repository_root / "run_evaluation.py"),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert output_path.exists()

    artifact = json.loads(output_path.read_text(encoding="utf-8"))
    assert artifact["evaluation_id"] == "cli-demo"
