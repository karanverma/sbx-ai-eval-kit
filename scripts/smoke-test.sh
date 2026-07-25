#!/usr/bin/env bash
set -euo pipefail

echo "Running evaluation workflow..."
python run_evaluation.py

echo "Validating generated artifact..."
test -f evaluation-result.json
python -m json.tool evaluation-result.json >/dev/null

echo "Running suite workflow..."
python run_evaluation.py evaluation-suite.yaml

echo "Validating suite artifact..."
test -f evaluation-results.json
python -m json.tool evaluation-results.json >/dev/null
python - <<'PY'
import json
with open("evaluation-results.json", encoding="utf-8") as handle:
    artifact = json.load(handle)
assert artifact["summary"]["total"] == len(artifact["results"])
assert artifact["summary"]["total"] == (
    artifact["summary"]["successful"] + artifact["summary"]["failed"]
)
print("Suite artifact summary validated")
PY

echo "Running test suite..."
pytest -q

echo "Smoke test passed."
