"""Execute frozen synthetic references and bounded local performance checks."""
import hashlib
import json
import sys
import time
import statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.app.api.main import app
from backend.app.data_integrity import validate_catalogue
OUT=Path(__file__).resolve().parents[1]/'docs/evidence/wp5'


def main():
 scenarios=json.loads((OUT/'scenarios.json').read_text())
 results=[];latencies=[]
 with TestClient(app) as client:
  for case in scenarios:
   payload={key:case[key] for key in ('education','education_complete','existing_qualifications')}
   r=client.post('/eligibility',json={'programme_id':case['programme_id'],'student_results':payload['education'],'education_complete':payload['education_complete'],'existing_qualifications':payload['existing_qualifications']})
   assert r.status_code==200,(case['id'],r.text)
   actual=r.json()['assessment_status']
   assert actual==case['expected_academic_status'],(case['id'],actual)
   profile={**payload,'career_intention':'Explore '+case['domain'],'learner_category':'VOCATIONAL_LEARNER' if case['learner_category']=='Vocational' else 'EARLY_CAREER' if case['learner_category']=='Early-career' else 'AL_LEARNER'}
   before=client.post('/personalised-recommendations',json={'learner_profile':profile}).json()
   chat=client.post('/assistant/guidance',json={'intent':'eligibility','programme_id':case['programme_id'],'learner_profile':profile})
   assert chat.status_code==200 and chat.json()['academic_assessment']['status']==actual
   after=client.post('/personalised-recommendations',json={'learner_profile':profile}).json()
   assert before==after
   results.append({'scenario':case['id'],'expected':case['expected_academic_status'],'actual':actual,'passed':True,'assistant_unchanged_ranking':True,'ranking_method':before['ranking']['method']})
  profile={'education':scenarios[4]['education'],'career_intention':'Build software applications'}
  for _ in range(40):
   start=time.perf_counter();r=client.post('/personalised-recommendations',json={'learner_profile':profile});latencies.append(time.perf_counter()-start)
   assert r.status_code==200
  invalid=client.post('/recommendations',json={'student_results':{'Physics':'INVALID'}})
  assert invalid.status_code==422
 records={'synthetic_scenarios':results,'count':len(results),'functional_passes':sum(r['passed'] for r in results),'national_admissions_accuracy_measured':False,'performance':{'environment':'in-process FastAPI TestClient, warm model','requests':40,'median_seconds':statistics.median(latencies),'p95_seconds':sorted(latencies)[37]},'invalid_grade_http_status':invalid.status_code,'integrity':validate_catalogue()}
 (OUT/'scenario-results.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps({'scenario_passes':len(results),'performance':records['performance'],'integrity':'passed'},indent=2))

if __name__=='__main__':main()
