"""Prepare method-blinded synthetic rating packs; never creates relevance judgements."""
from pathlib import Path
import csv,hashlib,json,random
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/final-submission/research-evaluation/independent-ranking'
SNAPSHOT=ROOT/'docs/evidence/wp5/comparison.json'

def rows(name):
 with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 comparison=json.loads(SNAPSHOT.read_text())
 programmes={p['programme_id']:p for p in rows('data/reference/programmes.csv')}
 qualifications={q['qualification_id']:q for q in rows('data/reference/qualifications.csv')}
 catalogue={pid:{'text':'. '.join(v for v in (p['programme_name'],p['field_of_study'],p['domain'],qualifications[p['qualification_id']]['qualification_type']) if v),'source_id':p['source_id'],'source_url':p['application_url'],'programme_name':p['programme_name']} for pid,p in programmes.items() if p['programme_status']=='Active'}
 assert hashlib.sha256(json.dumps(catalogue,sort_keys=True).encode()).hexdigest()==comparison['catalogue_hash'],'Catalogue differs from saved comparison'
 mapping=[];expected=[];cases=[]
 for index,case in enumerate(comparison['scenarios'],1):
  ids=sorted(case['academic_status'])
  for method in ('deterministic','tfidf','semantic'):
   assert set(case['orders'][method])==set(ids),'Different candidate pools'
  cards=[]
  for n,pid in enumerate(ids,1):
   p=programmes[pid];qual=qualifications[p['qualification_id']]
   code=f'C{index:02d}-{n:02d}'
   facts='. '.join(v for v in (p['programme_name'],p['field_of_study'],p['domain'],qual['qualification_type']) if v)
   cards.append({'case_id':case['scenario'],'candidate_code':code,'programme_title':p['programme_name'],'facts':facts,'official_url':p['application_url']})
   mapping.append({'case_id':case['scenario'],'candidate_code':code,'programme_id':pid,'academic_group':case['academic_status'][pid]})
   expected.append((case['scenario'],code))
  cases.append({'case_id':case['scenario'],'profile':case['synthetic_profile'],'cards':cards})
 for packet,seed in [('A',20261103),('B',20261104)]:
  rng=random.Random(seed);text='# Blinded synthetic relevance cards — packet '+packet+'\n\nNo method names, scores or predicted ranks are shown. Cards are randomised within each case. Rate interest relevance only, not admission/competence. No judgement is supplied by this pack. Empty/uninterpretable goals may be UNJUDGEABLE; missing ratings are not zero. Official links allow fact checking; use the frozen card text as common evidence and note any live-source contradiction rather than silently changing it. Do not view researcher-key.json or comparison.json before independent ratings are frozen.\n'
  ordered=[]
  for case in cases:
   text+='\n## Case '+case['case_id']+'\n\nFictional profile:\n\n```json\n'+json.dumps(case['profile'],ensure_ascii=False,indent=2)+'\n```\n'
   shuffled=list(case['cards']);rng.shuffle(shuffled)
   for card in shuffled:
    text+='\n### '+card['candidate_code']+' — '+card['programme_title']+'\n\n'+card['facts']+'\n\nOfficial source: '+card['official_url']+'\n'
    ordered.append(card)
  (OUT/f'rater-cards-{packet}.md').write_text(text)
  with (OUT/f'ratings-{packet}-blank.csv').open('w') as f:
   wr=csv.writer(f,lineterminator='\n');wr.writerow(['case_id','candidate_code','reviewer_id','relevance_0_to_3_or_UNJUDGEABLE','reason','source_contradiction_or_unavailable','missing_reason'])
   for c in ordered:wr.writerow([c['case_id'],c['candidate_code'],'','','','',''])
 (OUT/'researcher-key.json').write_text(json.dumps({'researcher_only':'Do not give to blinded judges until ratings locked','candidate_mapping':mapping,'frozen_orders':{s['scenario']:s['orders'] for s in comparison['scenarios']}},indent=2)+'\n')
 manifest={'snapshot':'docs/evidence/wp5/comparison.json','comparison_sha256':hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),'catalogue_hash_in_comparison':comparison['catalogue_hash'],'model_revision':json.loads((ROOT/'backend/app/relevance/model-lock.json').read_text())['revision'],'case_count':len(cases),'unique_case_candidate_pairs':len(expected),'packet_seeds':{'A':20261103,'B':20261104},'judgements_created':0,'independent_labels_available':False,'ndcg_computed':False,'source_inputs_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['data/reference/programmes.csv','data/reference/qualifications.csv']}}
 (OUT/'preparation-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
