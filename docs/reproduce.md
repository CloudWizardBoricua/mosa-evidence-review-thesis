# Reproduce the Study

Choose the evidence you want to inspect. The public website uses saved data. Building it never calls a paid model or changes a review approval.

## 1. Verify the public reading resource

Clone the thesis repository and enter it:

```bash
git clone https://github.com/CloudWizardBoricua/mosa-evidence-review-thesis.git
cd mosa-evidence-review-thesis
python -m venv .venv
```

Use Python 3.11. Activate the environment with `source .venv/bin/activate` on Linux or macOS, or `.\.venv\Scripts\Activate.ps1` in Windows PowerShell.

```bash
python -m pip install -r requirements-site.txt
python tools/render_public_data.py --check
python -m unittest discover -s tests -p "test_public_site.py" -v
node --test tests/test_reader_interactions.js
python -m mkdocs build --strict
python -m mkdocs serve
```

The checks verify published references, schema requirements, consistency of generated tables, required diagram exports, and publication boundaries. A schema is the required structure of a record. The strict build reports broken documentation references as failures.

The interaction tests use Node.js, a runtime that executes JavaScript. They check saved case filters, corrected recommendations, failed runs, and unavailable records. These tests make no network or model requests.

## 2. Inspect the original harness

The original harness is preserved in `prototypes/legacy-harness/`. Its source and recorded output remain together. First read its experiment protocol and research disclosure.

Run these commands from that folder in a separate virtual environment:

```bash
python -m pip install -r requirements.txt
```

On Linux or macOS:

```bash
PYTHONPATH=src python -m mosa_harness.experiment --root . --repeats 20 --seed 20260623
PYTHONPATH=src python -m mosa_harness.analysis --root .
PYTHONPATH=src pytest -q
```

In Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m mosa_harness.experiment --root . --repeats 20 --seed 20260623
python -m mosa_harness.analysis --root .
pytest -q
```

These commands regenerate result files in the working copy. Keep the committed evidence unchanged and run in a separate checkout if you want to compare a fresh execution with the preserved record. Timing may differ across machines. Compare logical outcomes and source settings before interpreting timing differences.

## 3. Run the current capstone in the class repository

The capstone remains in the existing class Codespace until course submission. A Codespace is a hosted development environment. From the class repository root:

```bash
python3 -m unittest discover -s capstone/tests -v
python3 capstone/mosa_review.py review 03_interface_version --mode baseline
python3 capstone/mosa_review.py review 03_interface_version --mode adaptive
python3 capstone/server.py
```

Keep the prototype's port private. The command line and class interface offer the same review methods. The baseline runs every check. The adaptive method uses explicit rules. OpenRouter is the hosted service for the model method.

The model configuration uses the existing private course credentials. A credential is a secret used to access a service. Public files never contain a service key. Use the frozen settings and $5 budget control for the new benchmark; do not substitute an unbounded pilot command for that controlled evaluation.

Verify the existing frozen study before an offline reproduction:

```bash
python3 capstone/study40.py --verify
python3 capstone/study40.py --run --modes baseline adaptive
python3 capstone/study40.py --export
```

For the paid model comparison, verify the existing private credentials and obtain pricing through the budget control:

```bash
python3 capstone/study40.py --pricing
python3 capstone/study40.py --run --modes openrouter
python3 capstone/study40.py --export
```

The runner resumes completed slots rather than repeating them. Keep its cost ledger and failed runs. A missing or stopped hosted comparison remains incomplete. Do not regenerate or refreeze the published study to conceal changed inputs. Read [the research design](research-design.md) before running the paid study.

## 4. Move the tested capstone later

Follow [the migration guide](migration.md) after course submission. It records a source commit, an export manifest, the exact settings, and a fresh checkout test. The class repository remains available with its course history.

!!! info "Blue: logical reproduction"
    A reproduced result should make the same supported recommendation for the same source evidence and settings. Timing and hosted model text may vary. Compare the facts the study claims, including evidence references, rather than requiring every explanatory sentence to match.
