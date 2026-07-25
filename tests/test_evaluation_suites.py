import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_evaluation import build_suite_result, validate_suite_config


def valid_evaluation(evaluation_id: str, *, command: list[str] | None = None) -> dict:
    data = {
        "schema_version": "1",
        "evaluation_id": evaluation_id,
        "objective": f"Evaluate {evaluation_id}",
        "conditions": ["Same conditions"],
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

    if command is not None:
        data["execution"] = {
            "executor": "local",
            "command": command,
        }

    return data


def test_suite_result_aggregates_summary_counts() -> None:
    config = {
        "evaluations": [
            valid_evaluation("suite-one", command=[sys.executable, "-c", "print('ok')"]),
            valid_evaluation("suite-two", command=[sys.executable, "-c", "print('ok')"]),
        ]
    }

    artifact = build_suite_result(config)

    assert artifact["summary"] == {
        "total": 2,
        "successful": 2,
        "failed": 0,
    }
    assert len(artifact["results"]) == 2


def test_suite_continues_after_non_zero_exit_code() -> None:
    config = {
        "evaluations": [
            valid_evaluation("suite-fail", command=[sys.executable, "-c", "import sys; sys.exit(3)"]),
            valid_evaluation("suite-pass", command=[sys.executable, "-c", "print('still runs')"]),
        ]
    }

    artifact = build_suite_result(config)

    assert artifact["summary"] == {
        "total": 2,
        "successful": 1,
        "failed": 1,
    }
    assert artifact["results"][0]["runtime_evidence"]["exit_code"] == 3
    assert artifact["results"][1]["runtime_evidence"]["exit_code"] == 0


def test_suite_retains_complete_individual_evaluation_fields() -> None:
    config = {
        "evaluations": [
            valid_evaluation("suite-full", command=[sys.executable, "-c", "print('ok')"]),
        ]
    }

    artifact = build_suite_result(config)

    result = artifact["results"][0]
    assert result["evaluation_id"] == "suite-full"
    assert result["objective"] == "Evaluate suite-full"
    assert result["baseline"] == config["evaluations"][0]["baseline"]
    assert result["candidate"] == config["evaluations"][0]["candidate"]
    assert result["criteria"] == config["evaluations"][0]["criteria"]
    assert result["observations"] == config["evaluations"][0]["observations"]
    assert result["decision"] == config["evaluations"][0]["decision"]
    assert result["provenance"]["source_sha256"]
    assert result["runtime_evidence"]["exit_code"] == 0


def test_invalid_suite_configuration_fails_clearly() -> None:
    with pytest.raises(ValueError, match="evaluations"):
        validate_suite_config({"evaluations": "not-a-list"})


def test_cli_generates_suite_output(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    suite_path = tmp_path / "evaluation-suite.yaml"
    output_path = tmp_path / "evaluation-results.json"

    suite_path.write_text(
        """
schema_version: \"1\"
evaluations:
  - schema_version: \"1\"
    evaluation_id: suite-one
    objective: First suite item
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
    execution:
      executor: local
      command:
        - python
        - -c
        - print('first')
  - schema_version: \"1\"
    evaluation_id: suite-two
    objective: Second suite item
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
    execution:
      executor: local
      command:
        - python
        - -c
        - print('second')
""".strip(),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(repository_root / "run_evaluation.py"),
            str(suite_path),
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
    assert artifact["summary"]["total"] == 2
    assert len(artifact["results"]) == 2
