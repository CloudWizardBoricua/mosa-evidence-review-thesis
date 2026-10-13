
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def save(fig, path):
    fig.savefig(path, dpi=220, bbox_inches='tight')
    plt.close(fig)


def run(root: Path):
    res=root/'results'; figdir=res/'figures'; figdir.mkdir(exist_ok=True)
    df=pd.read_csv(res/'primary_results.csv'); rep=pd.read_csv(res/'repeated_runs.csv')
    summary=json.loads((res/'statistical_summary.json').read_text())

    # Experimental workflow diagram.
    fig, ax=plt.subplots(figsize=(11,4.2)); ax.axis('off')
    boxes=[('Interface contract\n+ schemas',0.02),('2 compliant modules\n+ 18 injected faults',0.22),('Conventional\nbaseline',0.45),('Conformance\nharness',0.62),('Paired decisions,\nfindings, timing, evidence',0.82)]
    for text,x in boxes:
        rect=FancyBboxPatch((x,0.32),0.15,0.36,boxstyle='round,pad=0.02',linewidth=1.3,facecolor='white')
        ax.add_patch(rect); ax.text(x+0.075,0.50,text,ha='center',va='center',fontsize=10)
    # split arrows
    ax.add_patch(FancyArrowPatch((0.17,0.5),(0.22,0.5),arrowstyle='->',mutation_scale=14))
    ax.add_patch(FancyArrowPatch((0.37,0.5),(0.45,0.5),arrowstyle='->',mutation_scale=14))
    ax.add_patch(FancyArrowPatch((0.37,0.47),(0.62,0.47),connectionstyle='arc3,rad=.28',arrowstyle='->',mutation_scale=14))
    ax.add_patch(FancyArrowPatch((0.60,0.5),(0.82,0.56),arrowstyle='->',mutation_scale=14))
    ax.add_patch(FancyArrowPatch((0.77,0.5),(0.82,0.44),arrowstyle='->',mutation_scale=14))
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    save(fig, figdir/'experimental_workflow.png')

    # Detection sensitivity.
    methods=['Baseline','Harness']
    vals=[summary['methods']['baseline']['sensitivity']*100,summary['methods']['harness']['sensitivity']*100]
    cis=[summary['methods']['baseline']['sensitivity_wilson_95'],summary['methods']['harness']['sensitivity_wilson_95']]
    yerr=np.array([[vals[i]-cis[i][0]*100 for i in range(2)],[cis[i][1]*100-vals[i] for i in range(2)]])
    fig,ax=plt.subplots(figsize=(7.5,4.8)); ax.bar(methods,vals,yerr=yerr,capsize=6); ax.set_ylim(0,110); ax.set_ylabel('Fault-detection sensitivity (%)'); ax.set_title('Detection of 18 injected nonconformances'); ax.grid(axis='y',alpha=.25)
    for i,v in enumerate(vals): ax.text(i,v+3,f'{v:.1f}%',ha='center',fontweight='bold')
    save(fig,figdir/'fault_detection_sensitivity.png')

    # Fault matrix.
    faults=df[df.expected_conformant==False].pivot(index='fault_class',columns='method',values='detected_nonconformance').astype(int)
    faults=faults[['baseline','harness']]
    fig,ax=plt.subplots(figsize=(7.5,7.2)); im=ax.imshow(faults.values,aspect='auto',vmin=0,vmax=1,cmap='Greys')
    ax.set_xticks([0,1],['Baseline','Harness']); ax.set_yticks(range(len(faults)),[s.replace('_',' ') for s in faults.index]); ax.set_title('Injected faults detected by each method')
    for i in range(len(faults)):
        for j in range(2): ax.text(j,i,'Detected' if faults.iloc[i,j] else 'Missed',ha='center',va='center',fontsize=8,color='white' if faults.iloc[i,j] else 'black')
    fig.tight_layout(); save(fig,figdir/'fault_detection_matrix.png')

    # Diagnostic accuracy and evidence completeness.
    metrics=['Actionable diagnosis','Evidence completeness\n(compliant controls)']
    b=[summary['methods']['baseline']['diagnostic_accuracy']*100,summary['methods']['baseline']['mean_evidence_completeness_controls']*100]
    h=[summary['methods']['harness']['diagnostic_accuracy']*100,summary['methods']['harness']['mean_evidence_completeness_controls']*100]
    x=np.arange(len(metrics)); width=.35
    fig,ax=plt.subplots(figsize=(8.5,4.8)); ax.bar(x-width/2,b,width,label='Baseline'); ax.bar(x+width/2,h,width,label='Harness'); ax.set_xticks(x,metrics); ax.set_ylim(0,110); ax.set_ylabel('Percent'); ax.legend(); ax.grid(axis='y',alpha=.25); ax.set_title('Diagnostic and evidence quality')
    save(fig,figdir/'diagnostic_evidence_quality.png')

    # Runtime distribution.
    data=[rep[rep.method=='baseline'].duration_ms,rep[rep.method=='harness'].duration_ms]
    fig,ax=plt.subplots(figsize=(7.5,4.8)); ax.boxplot(data,labels=['Baseline','Harness'],showfliers=False); ax.set_yscale('log'); ax.set_ylabel('Execution time per candidate (ms, log scale)'); ax.set_title('Automation overhead across repeated runs'); ax.grid(axis='y',alpha=.25)
    save(fig,figdir/'runtime_distribution.png')

    # Conformance scores by candidate.
    hdf=df[df.method=='harness'].sort_values(['expected_conformant','composite_score'])
    fig,ax=plt.subplots(figsize=(9,7)); ax.barh([x.replace('_',' ') for x in hdf.candidate],hdf.composite_score); ax.axvline(80,linestyle='--'); ax.set_xlim(0,105); ax.set_xlabel('Composite conformance score'); ax.set_title('Harness scores with 80-point decision threshold'); ax.grid(axis='x',alpha=.25)
    save(fig,figdir/'candidate_conformance_scores.png')

    # Weight sensitivity: score-only versus gate-adjusted decisions for faulted candidates.
    ws=summary['weight_sensitivity']
    candidates=[c for c in ws['score_only_pass_probability'] if not c.startswith('control_')]
    candidates=sorted(candidates, key=lambda c: ws['score_only_pass_probability'][c])
    raw=[100*ws['score_only_pass_probability'][c] for c in candidates]
    gated=[100*ws['gate_adjusted_pass_probability'][c] for c in candidates]
    y=np.arange(len(candidates)); height=.38
    fig,ax=plt.subplots(figsize=(9.2,7.2))
    ax.barh(y-height/2,raw,height,label='Score only')
    ax.barh(y+height/2,gated,height,label='Critical gates applied')
    ax.set_yticks(y,[c.replace('_',' ') for c in candidates])
    ax.set_xlim(0,105); ax.set_xlabel('Probability of passing across 10,000 random weight sets (%)')
    ax.set_title('Critical gates prevent compensating-score false passes')
    ax.grid(axis='x',alpha=.25); ax.legend(loc='lower right')
    save(fig,figdir/'weight_sensitivity_gates.png')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]); a=p.parse_args(); run(a.root)
