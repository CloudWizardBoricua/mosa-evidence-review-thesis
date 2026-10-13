
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint


def wilson(successes: int, n: int) -> tuple[float, float]:
    lo, hi = proportion_confint(successes, n, alpha=0.05, method='wilson')
    return float(lo), float(hi)


def cliffs_delta(x, y):
    x = np.asarray(x); y = np.asarray(y)
    gt = sum(a > b for a in x for b in y)
    lt = sum(a < b for a in x for b in y)
    return (gt - lt) / (len(x) * len(y))


def run(root: Path) -> dict:
    res = root / 'results'
    df = pd.read_csv(res / 'primary_results.csv')
    rep = pd.read_csv(res / 'repeated_runs.csv')
    faults = df[df.expected_conformant == False]
    controls = df[df.expected_conformant == True]
    summary = {'methods': {}, 'pairwise': {}, 'reliability': {}, 'weight_sensitivity': {}}
    for method in ['baseline','harness']:
        fd = faults[faults.method == method]
        cd = controls[controls.method == method]
        sens_n = int(fd.detected_nonconformance.sum()); sens_d = len(fd)
        spec_n = int(cd.passed.sum()); spec_d = len(cd)
        diag_n = int(fd.diagnosis_correct.sum())
        summary['methods'][method] = {
            'sensitivity': sens_n / sens_d,
            'sensitivity_count': [sens_n, sens_d],
            'sensitivity_wilson_95': wilson(sens_n, sens_d),
            'specificity': spec_n / spec_d,
            'specificity_count': [spec_n, spec_d],
            'specificity_wilson_95': wilson(spec_n, spec_d),
            'diagnostic_accuracy': diag_n / sens_d,
            'diagnostic_accuracy_count': [diag_n, sens_d],
            'mean_evidence_completeness_controls': float(cd.evidence_completeness.mean()),
            'median_duration_ms_primary': float(df[df.method == method].duration_ms.median()),
            'median_checks': float(df[df.method == method].tests_or_checks.median()),
            'control_median_duration_ms': float(rep[(rep.method == method) & (rep.expected_conformant == True)].duration_ms.median()),
            'control_p95_duration_ms': float(rep[(rep.method == method) & (rep.expected_conformant == True)].duration_ms.quantile(0.95)),
        }

    piv = df.pivot(index='candidate', columns='method', values='correct_decision')
    both_correct = int(((piv.baseline == True) & (piv.harness == True)).sum())
    baseline_only = int(((piv.baseline == True) & (piv.harness == False)).sum())
    harness_only = int(((piv.baseline == False) & (piv.harness == True)).sum())
    both_wrong = int(((piv.baseline == False) & (piv.harness == False)).sum())
    mc = mcnemar([[both_correct, baseline_only], [harness_only, both_wrong]], exact=True)
    summary['pairwise']['mcnemar_table'] = [[both_correct, baseline_only], [harness_only, both_wrong]]
    summary['pairwise']['mcnemar_exact_p'] = float(mc.pvalue)

    # Repeat-run reliability and timing.
    for method in ['baseline','harness']:
        rd = rep[rep.method == method]
        stable = rd.groupby('candidate').passed.nunique().eq(1)
        summary['reliability'][method] = {
            'decision_stability': float(stable.mean()),
            'median_duration_ms': float(rd.duration_ms.median()),
            'p95_duration_ms': float(rd.duration_ms.quantile(0.95)),
            'iqr_duration_ms': [float(rd.duration_ms.quantile(0.25)), float(rd.duration_ms.quantile(0.75))],
        }
    hdig = rep[rep.method == 'harness'].groupby('candidate').evidence_digest.nunique()
    control_names = set(df[df.expected_conformant == True].candidate)
    summary['reliability']['harness']['digest_stability_all_candidates'] = float(hdig.eq(1).mean())
    summary['reliability']['harness']['digest_stability_controls'] = float(hdig[hdig.index.isin(control_names)].eq(1).mean())

    # Compare paired median timings per candidate.
    med = rep.groupby(['candidate','method']).duration_ms.median().unstack()
    try:
        w = stats.wilcoxon(med.harness, med.baseline, alternative='greater')
        summary['pairwise']['timing_wilcoxon_statistic'] = float(w.statistic)
        summary['pairwise']['timing_wilcoxon_p'] = float(w.pvalue)
    except ValueError:
        pass
    summary['pairwise']['timing_cliffs_delta'] = float(cliffs_delta(med.harness, med.baseline))
    paired_diff = med.harness - med.baseline
    paired_ratio = med.harness / med.baseline.replace(0, np.nan)
    summary['pairwise']['median_candidate_runtime_difference_ms'] = float(paired_diff.median())
    summary['pairwise']['median_candidate_runtime_ratio'] = float(paired_ratio.median())
    summary['pairwise']['primary_median_runtime_ratio'] = float(
        summary['methods']['harness']['median_duration_ms_primary'] /
        summary['methods']['baseline']['median_duration_ms_primary']
    )

    # Weight sensitivity for the existing four dimensions. Gates remain active.
    hdf = df[df.method == 'harness'].copy()
    rng = np.random.default_rng(20260623)
    weights = rng.dirichlet(np.ones(4), size=10000)
    score_only = {}
    gate_adjusted = {}
    for _, row in hdf.iterrows():
        scores = np.array([row.structural_score, row.operational_score, row.competition_readiness_score, row.security_score], dtype=float)
        raw_passes = (weights @ scores >= 80.0)
        score_only[row.candidate] = float(raw_passes.mean())
        adjusted = raw_passes.copy()
        if bool(row.gate_failure):
            adjusted[:] = False
        gate_adjusted[row.candidate] = float(adjusted.mean())
    summary['weight_sensitivity'] = {
        'draws': 10000,
        'score_only_pass_probability': score_only,
        'gate_adjusted_pass_probability': gate_adjusted,
        'control_min_gate_adjusted_pass_probability': min(v for k,v in gate_adjusted.items() if k.startswith('control_')),
        'fault_max_gate_adjusted_pass_probability': max(v for k,v in gate_adjusted.items() if not k.startswith('control_')),
        'fault_max_score_only_pass_probability': max(v for k,v in score_only.items() if not k.startswith('control_')),
    }

    (res / 'statistical_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

    # Tables used by the thesis.
    method_rows = []
    for method, s in summary['methods'].items():
        method_rows.append({
            'Method': method.title(),
            'Faults detected': f"{s['sensitivity_count'][0]}/{s['sensitivity_count'][1]}",
            'Sensitivity': s['sensitivity'],
            'Sensitivity 95% CI': f"{s['sensitivity_wilson_95'][0]:.3f}-{s['sensitivity_wilson_95'][1]:.3f}",
            'Controls accepted': f"{s['specificity_count'][0]}/{s['specificity_count'][1]}",
            'Diagnostic accuracy': s['diagnostic_accuracy'],
            'Control evidence completeness': s['mean_evidence_completeness_controls'],
            'Median checks/tests': s['median_checks'],
        })
    pd.DataFrame(method_rows).to_csv(res / 'method_summary.csv', index=False)
    return summary

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2]); a=p.parse_args()
    print(json.dumps(run(a.root), indent=2))
