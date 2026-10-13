
from pathlib import Path
import json
from mosa_harness.evaluation import baseline_evaluate, harness_evaluate

ROOT=Path(__file__).resolve().parents[1]
VECTORS=json.loads((ROOT/'test_vectors'/'fixed_vectors.json').read_text())

def test_controls_pass_harness():
    for name in ['control_vendor_a','control_vendor_b']:
        result=harness_evaluate(ROOT/'candidate_modules'/name,VECTORS)
        assert result.passed, result.findings

def test_all_mutants_fail_harness():
    for d in (ROOT/'candidate_modules').iterdir():
        if not d.is_dir() or d.name.startswith('control_'):
            continue
        result=harness_evaluate(d,VECTORS)
        assert not result.passed, (d.name,result.composite_score,result.findings)

def test_evidence_digest_is_reproducible():
    d=ROOT/'candidate_modules'/'control_vendor_a'
    a=harness_evaluate(d,VECTORS,seed=7)
    b=harness_evaluate(d,VECTORS,seed=7)
    assert a.evidence_digest==b.evidence_digest
