#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PYTHONPATH=src python -m mosa_harness.experiment --root . --repeats 20 --seed 20260623
PYTHONPATH=src python -m mosa_harness.analysis --root .
PYTHONPATH=src python -m mosa_harness.figures --root .
PYTHONPATH=src pytest -q
