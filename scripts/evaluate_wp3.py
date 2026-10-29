"""Frozen synthetic comparisons and measured runtime; no independent relevance labels."""
import json
import platform
import resource
import statistics
import sys
import time
from importlib.metadata import version
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.app.api.main import app
from backend.app.relevance.encoder import get_encoder, REVISION
from backend.app.relevance.engine import rank_recommendations
from backend.app.personalisation.engine import personalise_recommendations

OUTPUT=Path(__file__).resolve().parents[1]/'docs/evidence/wp3'
MATHS={'A_LEVEL':{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'}}
SCENARIOS=[
 ('empty',MATHS,''),
 ('it_literal',MATHS,'Software engineering and computer science'),
 ('it_paraphrase',MATHS,'Build reliable applications and computer systems'),
 ('business',{'A_LEVEL':{'Business Studies':'C','Accounting':'C','Economics':'C'}},'Manage a business and lead organisations'),
 ('engineering',MATHS,'Design mechanical and electrical engineering systems'),
 ('unmet_engineering',{'A_LEVEL':{'Combined Mathematics':'C','Physics':'F','Chemistry':'C'}},'Design engineering systems'),
 ('missing_evidence',{'A_LEVEL':{'Physics':'C'}},'Engineering'),
 ('unfamiliar',MATHS,'zzqqxxvv unknownword'),
 ('vocational',{},'Robotics and factory automation'),
]


def main():
 OUTPUT.mkdir(parents=True,exist_ok=True)
 scale=1024*1024 if sys.platform=='darwin' else 1024
 before=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/scale
 start=time.perf_counter();encoder,error=get_encoder();startup=time.perf_counter()-start
 if encoder is None:raise RuntimeError('Real model required for WP3 evaluation: '+str(error))
 comparisons=[]
 for name,education,intention in SCENARIOS:
  profile={'education':education,'career_intention':intention}
  if name=='vocational':profile['existing_qualifications']=[{'qualification_id':'QLF0010','title':'Higher National Diploma in Mechatronics Technology'}]
  result=personalise_recommendations(profile)
  pool=result['recommendations'] or result['academic_insights']
  by_id={item['programme_id']:item for item in pool}
  baseline=[{k:v for k,v in by_id[pid].items() if k!='relevance'} for pid in result['ranking']['legacy_order']]
  orders={'legacy_original':[item['programme_id'] for item in baseline]}
  scores={}
  for method in ('deterministic','tfidf','semantic'):
   ranked,meta=rank_recommendations(baseline,profile,method)
   orders[method]=[item['programme_id'] for item in ranked]
   scores[method]={item['programme_id']:item['relevance']['score'] for item in ranked}
   for item in ranked:
    original=by_id[item['programme_id']]
    assert item.get('academic_gap_insights',item.get('status'))==original.get('academic_gap_insights',original.get('status'))
   if name!='empty':assert meta['method']==method.upper()
  comparisons.append({'scenario':name,'synthetic_profile':profile,'orders':orders,'scores':scores,'academic_status':{item['programme_id']:item.get('academic_gap_insights',{}).get('status',item.get('status')) for item in pool}})
 (OUTPUT/'comparison.json').write_text(json.dumps({'purpose':'Functional/qualitative comparison only; scenario authors are implementers, not independent relevance judges.','independent_labels':False,'ndcg_at_3':None,'catalogue_hash':result['ranking']['catalogue_hash'],'scenarios':comparisons},indent=2)+'\n')
 client=TestClient(app)
 payload={'learner_profile':{'education':MATHS,'career_intention':'Build software applications'}}
 begin=time.perf_counter(); response=client.post('/personalised-recommendations',json=payload); first=time.perf_counter()-begin
 assert response.status_code==200 and response.json()['ranking']['method']=='SEMANTIC'
 times=[]
 for _ in range(40):
  begin=time.perf_counter();r=client.post('/personalised-recommendations',json=payload);times.append(time.perf_counter()-begin)
  assert r.status_code==200
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/scale
 metrics={'python':sys.version,'platform':platform.platform(),'processor':platform.machine(),'revision':REVISION,'versions':{package:version(package) for package in ('numpy','onnxruntime','tokenizers','fastapi','pydantic')},'model_load_seconds':startup,'first_ASGI_request_seconds_after_scenarios':first,'warm_ASGI_requests':40,'warm_median_seconds':statistics.median(times),'warm_p95_seconds':sorted(times)[37],'process_peak_before_model_MiB':before,'process_peak_after_requests_MiB':peak,'memory_note':'Process high-water RSS, not isolated model allocations. Latency uses in-process FastAPI TestClient, not network/browser latency.'}
 (OUTPUT/'performance.json').write_text(json.dumps(metrics,indent=2)+'\n')
 print(json.dumps(metrics,indent=2))
 print('Compared',len(comparisons),'synthetic scenarios; nDCG not computed without independent labels.')

if __name__=='__main__':main()
