#!/usr/bin/env bash
set -euo pipefail

echo "Running evaluation workflow..."
python run_evaluation.py

echo "Validating generated artifact..."
test -f evaluation-result.json
python -m json.tool evaluation-result.json >/dev/null

echo "Running test suite..."
pytest -q

echo "Smoke test passed."
