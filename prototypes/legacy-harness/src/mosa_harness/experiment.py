
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import random
import statistics
import sys
from pathlib import Path

from .evaluation import evaluate_candidate, baseline_evaluate, harness_evaluate


def run(root: Path, repeats: int = 30, seed: int = 20260623) -> dict:
    candidates_dir = root / 'candidate_modules'
    results_dir = root / 'results'
    evidence_dir = results_dir / 'evidence_packages'
    evidence_dir.mkdir(parents=True, exist_ok=True)
    fixed_vectors = json.loads((root / 'test_vectors' / 'fixed_vectors.json').read_text())
    candidates = sorted([p for p in candidates_dir.iterdir() if p.is_dir()])

    primary_rows = []
    for c in candidates:
        meta = json.loads((c / 'experiment_metadata.json').read_text())
        b, h = evaluate_candidate(c, fixed_vectors, seed)
        for method, result in [('baseline', b), ('harness', h)]:
            row = {
                'candidate': c.name,
                'fault_class': meta['fault_class'],
                'expected_conformant': meta['expected_conformant'],
                'method': method,
                'passed': result.passed,
                'correct_decision': result.passed == meta['expected_conformant'],
                'detected_nonconformance': (not result.passed) if not meta['expected_conformant'] else False,
                'duration_ms': result.duration_ms,
                'findings_count': len(result.findings),
                'actionable_diagnosis': result.actionable_diagnosis or '',
                'diagnosis_correct': (result.actionable_diagnosis == meta['fault_class']) if not meta['expected_conformant'] else (result.actionable_diagnosis is None),
                'evidence_completeness': result.evidence_completeness,
                'tests_or_checks': getattr(result, 'tests_executed', getattr(result, 'checks_executed', 0)),
                'composite_score': getattr(result, 'composite_score', ''),
                'structural_score': getattr(result, 'structural_score', ''),
                'operational_score': getattr(result, 'operational_score', ''),
                'competition_readiness_score': getattr(result, 'competition_readiness_score', ''),
                'security_score': getattr(result, 'security_score', ''),
                'evidence_confidence': getattr(result, 'evidence_confidence', ''),
                'gate_failure': getattr(result, 'gate_failure', ''),
                'evidence_digest': getattr(result, 'evidence_digest', ''),
            }
            primary_rows.append(row)
        (evidence_dir / f'{c.name}.json').write_text(json.dumps(h.__dict__, indent=2, sort_keys=True), encoding='utf-8')

    with (results_dir / 'primary_results.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(primary_rows[0].keys()))
        w.writeheader(); w.writerows(primary_rows)

    timing_rows = []
    order_rng = random.Random(seed)
    for rep in range(repeats):
        order = candidates[:]
        order_rng.shuffle(order)
        for c in order:
            meta = json.loads((c / 'experiment_metadata.json').read_text())
            rep_seed = seed + rep
            b = baseline_evaluate(c, fixed_vectors[0])
            h = harness_evaluate(c, fixed_vectors, seed)
            for method, result in [('baseline', b), ('harness', h)]:
                timing_rows.append({
                    'repeat': rep + 1,
                    'candidate': c.name,
                    'fault_class': meta['fault_class'],
                    'expected_conformant': meta['expected_conformant'],
                    'method': method,
                    'passed': result.passed,
                    'duration_ms': result.duration_ms,
                    'evidence_digest': getattr(result, 'evidence_digest', ''),
                })
    with (results_dir / 'repeated_runs.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(timing_rows[0].keys()))
        w.writeheader(); w.writerows(timing_rows)

    metadata = {
        'study_type': 'controlled synthetic feasibility evaluation with mutation-based fault injection',
        'seed': seed,
        'repeats': repeats,
        'candidate_count': len(candidates),
        'faulted_candidate_count': sum(1 for c in candidates if not json.loads((c / 'experiment_metadata.json').read_text())['expected_conformant']),
        'control_candidate_count': sum(1 for c in candidates if json.loads((c / 'experiment_metadata.json').read_text())['expected_conformant']),
        'fixed_vectors': len(fixed_vectors),
        'property_vectors_per_harness_run': 48,
        'python': sys.version,
        'platform': platform.platform(),
        'processor': platform.processor(),
    }
    (results_dir / 'experiment_metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--repeats', type=int, default=30)
    parser.add_argument('--seed', type=int, default=20260623)
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.repeats, args.seed), indent=2))

if __name__ == '__main__':
    main()
