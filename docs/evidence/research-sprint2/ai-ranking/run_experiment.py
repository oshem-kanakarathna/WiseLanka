"""Frozen descriptive rank comparison, local inference only; no labels/training."""
import argparse,copy,csv,hashlib,json,os,platform,random,resource,statistics,subprocess,sys,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT))
METHODS=('deterministic','tfidf','semantic')

def dump(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def table(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024 if sys.platform=='darwin' else 1024)
def percentile(x):return sorted(x)[max(0,__import__('math').ceil(.95*len(x))-1)]

def worker(method,missing=False):
    started=time.perf_counter()
    from backend.app.relevance.engine import rank_recommendations,document_embeddings,academic_status
    from backend.app.relevance.encoder import get_encoder
    imported=time.perf_counter()-started
    data=json.loads((OUT/'raw/benchmark-input.json').read_text())
    items,profile=data['items'],data['profile'];before=rss();load=0
    if method=='semantic' and not missing:
        t=time.perf_counter();enc,error=get_encoder();load=time.perf_counter()-t
        if enc is None:raise RuntimeError(error)
    t=time.perf_counter();ranked,meta=rank_recommendations(items,profile,method);first=time.perf_counter()-t
    t=time.perf_counter();again,again_meta=rank_recommendations(items,profile,method);second=time.perf_counter()-t
    output={'requested_method':method,'actual_method':meta['method'],'fallback_reason':meta['fallback_reason'],'module_import_ms':imported*1000,'model_load_ms':load*1000,'first_rank_ms':first*1000,'second_rank_ms':second*1000,'rss_before_method_MiB':before,'peak_rss_after_MiB':rss(),'order':[r['programme_id'] for r in ranked],'scores':{r['programme_id']:r['relevance']['score'] for r in ranked},'metadata':meta}
    print(json.dumps(output));return

def main():
    baseline=json.loads((OUT/'BASELINE.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['commit']
    assert hashlib.sha256((OUT/'SCENARIO_REGISTER.csv').read_bytes()).hexdigest()==baseline['scenario_sha256']
    assert hashlib.sha256((OUT/'EXPERIMENT_PROTOCOL.md').read_bytes()).hexdigest()==baseline['protocol_sha256']
    for p,h in baseline['protected_tracked_and_backup_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    for n,h in baseline['actual_model_hashes'].items():assert hashlib.sha256((Path(baseline['model_directory'])/n).read_bytes()).hexdigest()==h
    os.environ['WISELANKA_MODEL_DIR']=baseline['model_directory']
    from backend.app.personalisation.engine import personalise_recommendations
    from backend.app.relevance.engine import rank_recommendations,academic_status,GROUP_ORDER,catalogue_documents
    with (OUT/'SCENARIO_REGISTER.csv').open(newline='') as f:scenarios=list(csv.DictReader(f))
    frozen={};candidate_rows=[]
    for s in scenarios:
        profile=json.loads(s['profile_json']);response=personalise_recommendations(profile)
        pool=response['recommendations'] or response['academic_insights'];by_id={p['programme_id']:p for p in pool}
        assert len(by_id)==len(pool)
        order=response['ranking']['legacy_order'];assert set(order)==set(by_id)
        items=[{k:v for k,v in by_id[pid].items() if k!='relevance'} for pid in order]
        frozen[s['scenario_id']]={'profile':profile,'items':items}
        candidate_rows.append({'scenario_id':s['scenario_id'],'baseline_order':order,'partitions':{k:[p['programme_id'] for p in items if academic_status(p)==k] for k in GROUP_ORDER}})
    dump('raw/frozen-candidates.json',frozen);dump('raw/candidate-partitions.json',candidate_rows)
    dump('raw/catalogue-documents.json',catalogue_documents())
    dump('raw/benchmark-input.json',frozen['F01'])
    # Fixed repeated warm comparisons; no assertions about what should rank as relevant.
    expected={};metadata={};times={};samples=[];policy=[]
    for s in scenarios:
        sid=s['scenario_id'];data=frozen[sid]
        for method in METHODS:
            for _ in range(3):rank_recommendations(copy.deepcopy(data['items']),data['profile'],method)
            times[(sid,method)]=[]
    rng=random.Random(20261030)
    for repetition in range(30):
        jobs=[(s['scenario_id'],method) for s in scenarios for method in METHODS];rng.shuffle(jobs)
        for sid,method in jobs:
            data=frozen[sid];items=copy.deepcopy(data['items']);signature=digest(items)
            t=time.perf_counter();ranked,meta=rank_recommendations(items,data['profile'],method);elapsed=(time.perf_counter()-t)*1000
            assert digest(items)==signature,'Ranker mutated input'
            order=[p['programme_id'] for p in ranked];states=[academic_status(p) for p in ranked]
            original_states={p['programme_id']:academic_status(p) for p in items}
            assert len(set(order))==len(items) and set(order)==set(original_states)
            assert {p['programme_id']:academic_status(p) for p in ranked}==original_states
            assert [GROUP_ORDER[p] for p in states]==sorted(GROUP_ORDER[p] for p in states)
            key=(sid,method);scores={p['programme_id']:p['relevance']['score'] for p in ranked};result_sig=digest({'order':order,'scores':scores})
            if key not in expected:expected[key]=result_sig;metadata[key]=(ranked,meta)
            samples.append({'scenario_id':sid,'requested_method':method,'actual_method':meta['method'],'repetition':repetition,'duration_ms':elapsed,'ranking_and_score_signature':result_sig,'stable_against_first':result_sig==expected[key],'policy_compliant':True})
            times[key].append(elapsed)
    table('raw/warm-samples.csv',samples)
    comparator=[];performance=[]
    for s in scenarios:
        sid=s['scenario_id'];data=frozen[sid]
        for method in METHODS:
            ranked,meta=metadata[(sid,method)];order=[p['programme_id'] for p in ranked];t=times[(sid,method)]
            group={status:[p['programme_id'] for p in ranked if academic_status(p)==status] for status in GROUP_ORDER}
            comparator.append({'scenario_id':sid,'split':s['split'],'domain':s['domain'],'query':s['query'],'profile_json':s['profile_json'],'candidate_ids_json':json.dumps([p['programme_id'] for p in data['items']]),'academic_partitions_json':json.dumps({status:[p['programme_id'] for p in data['items'] if academic_status(p)==status] for status in GROUP_ORDER}),'requested_method':method,'actual_method':meta['method'],'method_status':meta['status'],'fallback_reason':meta['fallback_reason'] or '', 'ordered_ids_json':json.dumps(order),'scores_json':json.dumps({p['programme_id']:p['relevance']['score'] for p in ranked}),'top1':order[0] if order else '', 'top3_json':json.dumps(order[:3]),'group_top3_json':json.dumps({k:v[:3] for k,v in group.items()}),'median_rank_ms':statistics.median(t),'p95_rank_ms':percentile(t),'policy_compliant':True,'stable_order_and_scores':all(x['stable_against_first'] for x in samples if x['scenario_id']==sid and x['requested_method']==method),'score_interpretation':'none:grouped baseline order' if method=='deterministic' else 'lexical cosine;not admission probability' if method=='tfidf' else 'pretrained content cosine;not admission probability','catalogue_hash':meta['catalogue_hash']})
            performance.append({'phase':'WARM_RANK_FUNCTION','scenario_id':sid,'requested_method':method,'actual_method':meta['method'],'samples':len(t),'median_ms':statistics.median(t),'p95_ms':percentile(t),'min_ms':min(t),'max_ms':max(t),'model_load_ms':'','peak_process_rss_MiB':'','scope':'Rank function;academic assessment/candidate generation/browser excluded'})
    table('COMPARATOR_RESULTS.csv',comparator)
    # Fresh process workers, same single benchmark scenario for all methods.
    cold=[]
    for method in METHODS:
        for repetition in range(5):
            t=time.perf_counter();proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',method],cwd=ROOT,env=os.environ.copy(),capture_output=True,text=True);wall=(time.perf_counter()-t)*1000
            (OUT/'raw'/f'cold-{method}-{repetition}-stderr.txt').write_text(proc.stderr)
            if proc.returncode:raise RuntimeError(proc.stderr)
            row=json.loads(proc.stdout);row.update(repetition=repetition,subprocess_wall_ms=wall,exit_code=proc.returncode);cold.append(row)
            performance.append({'phase':'FRESH_PROCESS','scenario_id':'F01','requested_method':method,'actual_method':row['actual_method'],'samples':1,'median_ms':row['first_rank_ms'],'p95_ms':'','min_ms':'','max_ms':'','model_load_ms':row['model_load_ms'],'peak_process_rss_MiB':row['peak_rss_after_MiB'],'scope':'Process replicate'+str(repetition)+';first rank excludes separately measured import/model load;OS file cache not flushed'})
    dump('raw/cold-workers.json',cold);table('PERFORMANCE_RESULTS.csv',performance)
    env=dict(os.environ,WISELANKA_MODEL_DIR=str(OUT/'nonexistent-model-directory'))
    proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker','semantic','--missing-model'],cwd=ROOT,env=env,capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    fallback=json.loads(proc.stdout);baseline_order=[p['programme_id'] for p in metadata[('F01','deterministic')][0]]
    assert fallback['actual_method']=='RULE_BASED_FALLBACK' and fallback['fallback_reason']=='LOCAL_MODEL_UNAVAILABLE'
    assert fallback['order']==baseline_order and all(v is None for v in fallback['scores'].values())
    empty=[]
    for method in METHODS:
        r,m=rank_recommendations([],{'career_intention':'engineering'},method);assert r==[] and m['fallback_reason']=='NO_CANDIDATES';empty.append(m)
    try:rank_recommendations([],{},'invalid')
    except ValueError as e:invalid={'exception':type(e).__name__,'message':str(e),'expected':True}
    else:raise AssertionError('Invalid method accepted')
    dump('raw/failure-probes.json',{'real_missing_model_process':fallback,'empty_candidates':empty,'invalid_method':invalid})
    differences=[]
    for s in scenarios:
        sid=s['scenario_id'];orders={m:[p['programme_id'] for p in metadata[(sid,m)][0]] for m in METHODS}
        for a,b in [('deterministic','tfidf'),('deterministic','semantic'),('tfidf','semantic')]:
            differences.append({'scenario_id':sid,'split':s['split'],'method_a':a,'method_b':b,'full_order_differs':orders[a]!=orders[b],'top1_differs':orders[a][:1]!=orders[b][:1],'ordered_top3_differs':orders[a][:3]!=orders[b][:3],'top3_shared_ids':len(set(orders[a][:3])&set(orders[b][:3]))})
    table('raw/method-differences.csv',differences)
    dump('RUN_STATUS.json',{'scenarios':len(scenarios),'comparator_rows':len(comparator),'warm_calls':len(samples),'cold_workers':len(cold),'policy_assertions_passed':True,'stable_rank_and_scores':all(x['stable_against_first'] for x in samples),'missing_model_fallback_passed':True,'expected_invalid_method_exception':True,'unhandled_exceptions':0,'independent_labels':False,'relevance_metrics_computed':False,'candidate_generation_timing_excluded':True})
    for p,h in baseline['protected_tracked_and_backup_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    print(json.dumps(json.loads((OUT/'RUN_STATUS.json').read_text()),indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--worker',choices=METHODS);ap.add_argument('--missing-model',action='store_true');a=ap.parse_args()
    worker(a.worker,a.missing_model) if a.worker else main()
