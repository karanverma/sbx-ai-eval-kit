import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run_evaluation import build_result, validate


def sample():
    return {
        "schema_version": "1",
        "evaluation_id": "demo",
        "objective": "demo",
        "conditions": [],
        "baseline": {},
        "candidate": {},
        "criteria": [],
        "observations": [],
        "decision": "candidate",
    }


def test_validate():
    validate(sample())


def test_build_result():
    result = build_result(sample())
    assert result["evaluation_id"] == "demo"
    assert "provenance" in result