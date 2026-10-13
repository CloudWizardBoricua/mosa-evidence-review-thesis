"""Generate thesis PNG/SVG figures and exact data tables from verified exports."""
from pathlib import Path
import argparse
import csv
import hashlib
import html
import json
import os
import re
import statistics
import sys
import textwrap

ROOT=Path(__file__).resolve().parents[1]
MODES=('baseline','adaptive','openrouter')
LABELS=('Fixed','Adaptive rules','Model agent')
COLORS=('#1F5B99','#187E89','#744398')
OUTCOMES={'ready':('#237A52','R','Ready'),'not_ready':('#841617','B','Blocking problem'),
          'needs_review':('#A86406','V','Further review'),'failed':('#5C626C','Error','Failed request'),
          'unattempted':('#E9ECF0','N/A','Not attempted')}
CAPTIONS={
    'accuracy':'Twenty unique additional cases, first scheduled repetition. Guarded error bars show the Wilson 95 percent interval. Model accuracy is not estimated.',
    'effort':'Actual validator invocations across all three repetitions on 20 additional cases. Only full method schedules are comparable. A failed model request is not a zero-effort successful review.',
    'latency':'Median elapsed milliseconds among completed reviews of additional cases. Whiskers show the middle half of observed times, not a confidence interval. Failed requests are excluded from successful-review timing.',
    'cost':'Provider charges for completed additional-case reviews. Offline methods make no provider requests. An unresolved model charge is unknown, even when the ledger reports no billed amount.',
    'case_outcomes':'Outcome table for the first scheduled repetition on each additional case. R means ready, B means a blocking problem, V means further review. Error marks the failed request; N/A marks an unattempted review. Colors supplement text.',
    'benchmark_split':'Forty synthetic cases. Expected categories stay outside model inputs. Independent label review is pending.',
    'effort_latency_cost':'Three repetitions on 20 additional cases. The failed model request provides no comparable effort, review time, or provider charge estimate.'}


def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checked_inputs(root):
    summary_path=root/'docs/assets/study_summary.json'
    rows_path=root/'evidence/study40/rows.json'
    labels_path=root/'evidence/study40/labels.json'
    manifest_path=root/'evidence/study40/record_manifest.json'
    summary,rows,labels,manifest=map(read,(summary_path,rows_path,labels_path,manifest_path))
    if summary['schema_version']!=1 or sha(root/'evidence/study40/freeze.json')!=summary['freeze_sha256']:
        raise ValueError('Figure source is not tied to the frozen study')
    if manifest.get('public_rows_sha256') and sha(rows_path)!=manifest['public_rows_sha256']:
        raise ValueError('Canonical rows differ from the validated source export')
    if {r['run_id'] for r in rows}!={r['run_id'] for r in manifest['records']}:
        raise ValueError('Canonical row identities differ from the validated trace manifest')
    if len(rows)!=len(manifest['records']) or len({(r['case_id'],r['mode'],r['repeat']) for r in rows})!=len(rows):
        raise ValueError('Missing or duplicate run records')
    for record in manifest['records']:
        trace=root/'evidence/study40/traces'/(record['run_id']+'.json')
        if sha(trace)!=record['public_trace_sha256']:
            raise ValueError('Public trace changed after validation')
    datasets={d['id']:d for d in summary['datasets']}
    primary={m['mode']:m for m in datasets['study40-heldout']['methods']}
    for mode in MODES:
        selected=[r for r in rows if r['mode']==mode and r['split']=='heldout']
        if primary[mode]['runs']!=len(selected) or primary[mode]['tool_invocations']!=sum(r['tool_invocations'] for r in selected):
            raise ValueError('Figure summary disagrees with recorded events')
    return summary,rows,labels['cases'],primary,{
        'summary_sha256':sha(summary_path),'rows_sha256':sha(rows_path),
        'labels_sha256':sha(labels_path),'freeze_sha256':summary['freeze_sha256']}


def table(path,rows):
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def configure(dependency_path,output):
    if dependency_path:sys.path.insert(0,str(dependency_path.resolve()))
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':16,'axes.titlesize':20,
        'axes.labelsize':16,'xtick.labelsize':16,'ytick.labelsize':16,'axes.spines.top':False,'axes.spines.right':False,
        'axes.titleweight':'bold','axes.titlecolor':'#841617','axes.labelcolor':'#253040',
        'text.color':'#253040','xtick.color':'#253040','ytick.color':'#253040',
        'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white',
        'svg.fonttype':'none','axes.unicode_minus':False})
    output.mkdir(parents=True,exist_ok=True)
    return plt


def frame(ax,title,ylabel):
    ax.set_title(title,pad=17,loc='left');ax.set_ylabel(ylabel)
    ax.set_axisbelow(True);ax.grid(axis='y',color='#E2E6EB',linewidth=.7)
    ax.set_xticks(range(3),LABELS)


def unavailable(ax,index,text='Not estimated'):
    ax.axvspan(index-.34,index+.34,color='#EDF0F4',zorder=0)
    ax.text(index,.44,text,ha='center',va='center',fontsize=16,color='#5C626C',
            transform=ax.get_xaxis_transform())


def save(plt,fig,output,name,title,caption):
    large=name in ('accuracy','benchmark_split')
    fig.subplots_adjust(bottom=.34 if large else .22,top=.86)
    caption_size=16 if large else 12
    width=int(fig.get_figwidth()*(8.5 if large else 10.3))
    fig.text(.03,.035,textwrap.fill(caption,width=width),fontsize=caption_size,ha='left',va='bottom')
    paths=[]
    for extension in ('png','svg'):
        path=output/(name+'.'+extension)
        fig.savefig(path,dpi=240,bbox_inches='tight')
        if extension=='svg':
            text=path.read_text(encoding='utf-8')
            match=re.search(r'<svg\b[^>]*>',text)
            opening=match.group(0)[:-1]+' role="img" aria-labelledby="figure-title figure-description">'
            text=text[:match.start()]+opening+'\n<title id="figure-title">'+html.escape(title)+'</title>\n<desc id="figure-description">'+html.escape(caption)+'</desc>'+text[match.end():]
            path.write_text(text,encoding='utf-8',newline='\n')
        paths.append({'path':path.name,'sha256':sha(path)})
    plt.close(fig)
    return {'id':name,'title':title,'caption':caption,'files':paths,'table':name+'.csv'}


def accuracy(plt,output,primary):
    fig,ax=plt.subplots(figsize=(8.2,5.8));frame(ax,'Recommendation match on additional cases','Correct cases, percent')
    rows=[]
    for index,mode in enumerate(MODES):
        method=primary[mode]
        if method['first_runs_attempted']!=20:
            unavailable(ax,index,'Comparison\nincomplete')
        else:
            raw=100*method['raw_correct']/20;guarded=100*method['guarded_correct']/20
            ax.bar(index-.18,raw,.32,color=COLORS[index],alpha=.50,hatch='//',edgecolor=COLORS[index])
            ax.bar(index+.18,guarded,.32,color=COLORS[index])
            low,high=method['wilson95']
            ax.errorbar(index+.18,guarded,yerr=[[guarded-100*low],[100*high-guarded]],color='#202631',capsize=4,fmt='none')
            for x,value,count in ((index-.18,raw,method['raw_correct']),(index+.18,guarded,method['guarded_correct'])):
                ax.text(x,value+2,str(count)+'/20',ha='center',fontsize=16)
        rows.append({'method':LABELS[index],'attempted_first_runs':method['first_runs_attempted'],
                     'raw_correct':method['raw_correct'],'guarded_correct':method['guarded_correct'],
                     'planned_unique_cases':20,'status':method['status']})
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor='#78808C',alpha=.5,hatch='//',label='Raw draft'),Patch(facecolor='#78808C',label='After guard')],loc='upper left',bbox_to_anchor=(0,1.05),frameon=False,ncol=2,fontsize=16)
    ax.set_ylim(0,135);ax.set_yticks((0,20,40,60,80,100));table(output/'accuracy.csv',rows)
    return save(plt,fig,output,'accuracy','Recommendation match',CAPTIONS['accuracy'])


def performance(plt,output,rows,primary,name,ax=None):
    own=ax is None
    if own:fig,ax=plt.subplots(figsize=(8.2,5.8))
    else:fig=ax.figure
    titles={'effort':('Validation effort','Actual validator invocations'),
            'latency':('Completed review time','Median elapsed milliseconds'),
            'cost':('Completed review provider charges','Reported US dollars')}
    frame(ax,*titles[name]);data=[];values=[]
    for index,mode in enumerate(MODES):
        method=primary[mode];completed=[r for r in rows if r['mode']==mode and r['split']=='heldout' and r['status']=='completed']
        eligible=method['runs']==60 and len(completed)==60
        value=(method['tool_invocations'] if name=='effort' else statistics.median(r['elapsed_ms'] for r in completed) if name=='latency' else sum(r['cost_usd'] for r in completed) if all(r['cost_usd'] is not None for r in completed) else None) if eligible else None
        values.append(value)
        if value is not None:
            ax.bar(index,value,.56,color=COLORS[index]);ax.plot(index,value,'o',color=COLORS[index])
            label=str(value) if name=='effort' else '$'+f'{value:.6f}'.rstrip('0').rstrip('.') if name=='cost' else f'{value:.3f}'
            label_y=value
            if name=='latency':
                observed=sorted(r['elapsed_ms'] for r in completed)
                low=observed[(len(observed)-1)//4];high=observed[3*(len(observed)-1)//4]
                ax.errorbar(index,value,yerr=[[value-low],[high-value]],fmt='none',color='#243142',capsize=4)
                label_y=high;values.append(high)
            ax.annotate(label,(index,label_y),xytext=(0,8),textcoords='offset points',ha='center',fontsize=10)
        else:unavailable(ax,index,'Charge\nunknown' if name=='cost' and method['runs'] else 'Unavailable')
        data.append({'method':LABELS[index],'value':value,'unit':titles[name][1],
                     'completed_runs':len(completed),'planned_runs':60,'recorded_runs':method['runs'],
                     'failed_runs':method['failed_runs'],'eligible_for_comparison':eligible})
    maximum=max([v for v in values if v is not None]+[.01 if name=='cost' else 1])
    ax.set_ylim(0,maximum*1.34)
    if name=='cost':
        ax.ticklabel_format(axis='y',style='plain',useOffset=False)
    if own:
        table(output/(name+'.csv'),data)
        return save(plt,fig,output,name,titles[name][0],CAPTIONS[name])
    return data


def outcomes(plt,output,rows,cases):
    fig,ax=plt.subplots(figsize=(8.5,9.5))
    selected=sorted([c for c in cases if c['split']=='heldout'],key=lambda c:c['case_id'])
    first={(r['case_id'],r['mode']):r for r in rows if r['split']=='heldout' and r['repeat']==1}
    from matplotlib.patches import Rectangle,Patch
    table_rows=[]
    for y,case in enumerate(selected):
        values=[case['disposition']]
        for mode in MODES:
            row=first.get((case['case_id'],mode))
            values.extend(['unattempted','unattempted'] if row is None else ['failed','failed'] if row['status']=='failed' else [row['raw_disposition'],row['guarded_disposition']])
        record={'case_id':case['case_id'],'expected':values[0]}
        for x,value in enumerate(values):
            color,label,_=OUTCOMES[value]
            ax.add_patch(Rectangle((x-.48,y-.48),.96,.96,facecolor=color,edgecolor='white'))
            ax.text(x,y,label,ha='center',va='center',color='#253040' if value=='unattempted' else 'white',fontsize=11,fontweight='bold')
            if x:record[(('fixed_raw','fixed_guarded','adaptive_raw','adaptive_guarded','model_raw','model_guarded'))[x-1]]=value
        table_rows.append(record)
    ax.set_xlim(-.5,6.5);ax.set_ylim(19.5,-.5)
    ax.set_xticks(range(7),('Expected','Fixed\nraw','Fixed\nguarded','Rules\nraw','Rules\nguarded','Model\nraw','Model\nguarded'))
    ax.xaxis.tick_top();ax.tick_params(length=0,pad=7)
    ax.set_yticks(range(20),[c['case_id'] for c in selected]);ax.set_title('First-run outcome table',loc='left',pad=46)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.legend(handles=[Patch(facecolor=color,label=label+' = '+meaning) for color,label,meaning in OUTCOMES.values()],loc='upper center',bbox_to_anchor=(.5,-.02),ncol=3,frameon=False,fontsize=9)
    table(output/'case_outcomes.csv',table_rows)
    return save(plt,fig,output,'case_outcomes','First-run outcome table',CAPTIONS['case_outcomes'])


def split(plt,output,cases):
    fig,ax=plt.subplots(figsize=(8.2,5.3));data=[]
    for y,split in enumerate(('development','heldout')):
        left=0;row={'split':'Development' if split=='development' else 'Additional'}
        for category in ('ready','not_ready','needs_review'):
            count=sum(c['split']==split and c['disposition']==category for c in cases)
            color,_,label=OUTCOMES[category]
            ax.barh(y,count,.5,left=left,color=color,label=label if y==0 else None)
            ax.text(left+count/2,y,str(count),ha='center',va='center',color='white',fontweight='bold',fontsize=18)
            left+=count;row[category]=count
        row['total']=left;data.append(row)
    ax.set_yticks((0,1),('Development','Additional'));ax.invert_yaxis();ax.set_xlim(0,20)
    ax.set_xticks((0,5,10,15,20))
    ax.set_xlabel('Unique synthetic cases');ax.set_title('Benchmark case categories',loc='left',pad=82)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=3,frameon=False,fontsize=16)
    ax.set_axisbelow(True);ax.grid(axis='x',color='#E2E6EB');table(output/'benchmark_split.csv',data)
    return save(plt,fig,output,'benchmark_split','Benchmark case categories',CAPTIONS['benchmark_split'])


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--dependency-path',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();root=args.root.resolve();output=(args.output or root/'docs/assets/figures').resolve()
    summary,rows,cases,primary,hashes=checked_inputs(root);plt=configure(args.dependency_path,output)
    manifest=[accuracy(plt,output,primary)]
    for name in ('effort','latency','cost'):manifest.append(performance(plt,output,rows,primary,name))
    manifest.extend([outcomes(plt,output,rows,cases),split(plt,output,cases)])
    fig=plt.figure(figsize=(6.5,3.6));ax=fig.add_axes((.015,.25,.97,.66));ax.set_axis_off();combined=[]
    from matplotlib.patches import FancyBboxPatch
    headings=('Effort','Time','Cost');units=('Validator calls','Median milliseconds','Provider dollars')
    for index,name in enumerate(('effort','latency','cost')):
        x=index/3+.008
        ax.add_patch(FancyBboxPatch((x,.025),.312,.925,boxstyle='round,pad=0.008,rounding_size=0.025',facecolor='white',edgecolor='#D6DCE3'))
        ax.text(x+.018,.835,headings[index],fontsize=16,fontweight='bold',color='#841617')
        ax.text(x+.018,.72,units[index],fontsize=12,color='#526678')
        entries=list(csv.DictReader((output/(name+'.csv')).open(encoding='utf-8')))
        combined.extend(dict(item,metric=name) for item in entries)
        for row_index,entry in enumerate(entries):
            y=.535-row_index*.19;label=('Fixed','Rules','Model')[row_index]
            raw=entry['value'];value=('Unknown' if name=='cost' else 'Unavailable') if not raw else '$'+f'{float(raw):.6f}'.rstrip('0').rstrip('.') if name=='cost' else f'{float(raw):.3f}'.rstrip('0').rstrip('.') if name=='latency' else str(int(float(raw)))
            ax.text(x+.018,y,label,fontsize=12,color=COLORS[row_index])
            ax.text(x+.287,y,value,fontsize=12,fontweight='bold',ha='right',color='#253040')
    fig.text(.028,.955,'Additional-case comparison',fontsize=16,fontweight='bold',color='#841617')
    table(output/'effort_latency_cost.csv',combined)
    manifest.append(save(plt,fig,output,'effort_latency_cost','Effort time and cost',CAPTIONS['effort_latency_cost']))
    for alias,original in (('accuracy-chart','accuracy'),('effort-latency-cost','effort_latency_cost')):
        for extension in ('png','svg'):
            (output/(alias+'.'+extension)).write_bytes((output/(original+'.'+extension)).read_bytes())
    (output/'figure_manifest.json').write_text(json.dumps({'schema_version':1,'source_hashes':hashes,'figures':manifest,
        'model_status':'Comparison incomplete. Failed attempts are retained in records and excluded from successful-review performance estimates.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'figures':len(manifest),'formats':['PNG','SVG'],'data_tables':len(manifest),'output':str(output)}))


if __name__=='__main__':main()
