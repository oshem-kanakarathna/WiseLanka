from pathlib import Path
import csv,json,statistics,math,random
from collections import Counter
O=Path(__file__).resolve().parent
def read(n):
 with (O/n).open(newline='') as f:return list(csv.DictReader(f))
r=read('COMPARATOR_RESULTS.csv');d=read('raw/method-differences.csv');warm=read('raw/warm-samples.csv');cold=json.loads((O/'raw/cold-workers.json').read_text());sc=read('SCENARIO_REGISTER.csv')
# Reporting annotations only; original numerical comparisons and samples retained.
archive=O/'raw/comparator-before-annotation.csv'
if not archive.exists():archive.write_bytes((O/'COMPARATOR_RESULTS.csv').read_bytes())
for row in r:
 if row['actual_method']=='RULE_BASED_FALLBACK':row['score_interpretation']='No relevance score; rule-based fallback, not semantic inference'
with (O/'COMPARATOR_RESULTS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=r[0],lineterminator='\n');w.writeheader();w.writerows(r)
perf=read('PERFORMANCE_RESULTS.csv');counter={}
for row in perf:
 row.update(worker_repetition='',module_import_ms='',subprocess_wall_ms='',second_rank_ms='')
 if row['phase']=='FRESH_PROCESS':
  method=row['requested_method'];rep=counter.get(method,0);counter[method]=rep+1
  c=next(c for c in cold if c['requested_method']==method and c['repetition']==rep)
  row.update(worker_repetition=rep,module_import_ms=c['module_import_ms'],subprocess_wall_ms=c['subprocess_wall_ms'],second_rank_ms=c['second_rank_ms'])
with (O/'PERFORMANCE_RESULTS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=perf[0],lineterminator='\n');w.writeheader();w.writerows(perf)

summary={'scenarios':21,'development':9,'followup':12,'comparisons':63,'warm_repetitions_per_cell':30,'warm_total':1890,'fresh_process_repetitions_per_method':5,'differences':{},'warm_actual_method_only':{},'cold':{},'candidate_pool_counts':dict(Counter(len(json.loads(x['candidate_ids_json'])) for x in r if x['requested_method']=='deterministic')),'labels':False,'relevance_metrics_computed':False}
for split in ['DEVELOPMENT_REUSED','FROZEN_FOLLOWUP','ALL']:
 summary['differences'][split]={}
 for a,b in [('deterministic','tfidf'),('deterministic','semantic'),('tfidf','semantic')]:
  pairs=[x for x in d if (split=='ALL' or x['split']==split) and (x['method_a'],x['method_b'])==(a,b)]
  summary['differences'][split][a+'_vs_'+b]={'n':len(pairs),**{k:sum(x[k]=='True' for x in pairs) for k in ['full_order_differs','top1_differs','ordered_top3_differs']}}
for method in ['deterministic','tfidf','semantic']:
 vals=[float(x['duration_ms']) for x in warm if x['requested_method']==method and x['actual_method']==method.upper()]
 summary['warm_actual_method_only'][method]={'samples':len(vals),'median_ms':statistics.median(vals),'p95_ms':sorted(vals)[math.ceil(.95*len(vals))-1],'min_ms':min(vals),'max_ms':max(vals)}
 c=[x for x in cold if x['requested_method']==method]
 summary['cold'][method]={k+'_median':statistics.median(x[k] for x in c) for k in ['first_rank_ms','model_load_ms','subprocess_wall_ms','peak_rss_after_MiB']}
(O/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
# Compare frozen literal/task-paraphrase pairs without a ground-truth programme.
pairs=[]
for pair in ['IT','BUSINESS','ENGINEERING','VOCATIONAL']:
 ids=[s['scenario_id'] for s in sc if s['pair_id']==pair]
 for method in ['deterministic','tfidf','semantic']:
  a=next(x for x in r if x['scenario_id']==ids[0] and x['requested_method']==method);b=next(x for x in r if x['scenario_id']==ids[1] and x['requested_method']==method)
  pairs.append({'pair':pair,'method':method,'case_a':ids[0],'case_b':ids[1],'top1_a':a['top1'],'top1_b':b['top1'],'ordered_top3_a':a['top3_json'],'ordered_top3_b':b['top3_json'],'same_top1':a['top1']==b['top1'],'interpretation':'Descriptive paired-query behaviour;neither query supplies a reference ranking'})
with (O/'raw/paired-query-results.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=pairs[0],lineterminator='\n');w.writeheader();w.writerows(pairs)
# Create two method-blinded permutations; all response fields remain genuinely blank.
frozen=json.loads((O/'raw/frozen-candidates.json').read_text());facts=json.loads((O/'raw/catalogue-documents.json').read_text())
key={};pack_dir=O/'blinded-review';pack_dir.mkdir(exist_ok=True)
for label,seed in [('A',20261030),('B',20261031)]:
 rng=random.Random(seed);scenario_ids=list(frozen);rng.shuffle(scenario_ids);cards=[];blanks=[];key[label]={}
 for i,sid in enumerate(scenario_ids,1):
  case='S'+str(i).zfill(3);profile=frozen[sid]['profile'];candidate_ids=[p['programme_id'] for p in frozen[sid]['items']];rng.shuffle(candidate_ids)
  cards+=['## Case '+case,'','Stated interest: '+next(s['query'] for s in sc if s['scenario_id']==sid),'','Fictional profile: '+json.dumps(profile,ensure_ascii=False),'']
  for j,pid in enumerate(candidate_ids,1):
   card='C'+str(j).zfill(3);key[label][case+'-'+card]={'scenario_id':sid,'programme_id':pid}
   cards+=['### Candidate '+card,'',facts[pid]['text'],'','Official catalogue link: '+facts[pid]['source_url'],'']
   blanks.append({'reviewer_code':'','case_card_id':case,'candidate_card_id':card,'relevance_0_to_3_or_UNJUDGEABLE':'','reason':'','source_access_issue':''})
 header='# Blinded content-relevance review pack '+label+'\n\nDRAFT; do not recruit or administer before applicable ethics confirmation. No ratings exist. Methods, ranks and scores are withheld. Rate interest fit, not prestige, formal eligibility or admission probability. Do not treat similarity as the answer.\n\nUse0=unrelated,1=weak/indirect,2=clear related fit,3=strong direct fit; UNJUDGEABLE when evidence/intent is insufficient. Empty/uninterpretable intents may be unjudgeable. Work independently before discussion and preserve reasons. No judgement is prefilled. These are synthetic profiles.\n\n'
 (pack_dir/('CARDS_'+label+'.md')).write_text(header+'\n'.join(cards))
 with (pack_dir/('BLANK_'+label+'.csv')).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=blanks[0],lineterminator='\n');w.writeheader();w.writerows(blanks)
 if label=='A':(O/'BLANK_RELEVANCE_REVIEW.csv').write_bytes((pack_dir/'BLANK_A.csv').read_bytes())
(O/'raw/blinding-researcher-key.json').write_text(json.dumps(key,indent=2)+'\n')
print('Blinded pairs per pack:',len(blanks),'all response fields blank; no participant work.')
