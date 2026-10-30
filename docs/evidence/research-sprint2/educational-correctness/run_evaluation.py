"""Execute frozen synthetic references against unchanged FastAPI, no network calls.

This harness records disagreement; it never changes an expected result to match output.
"""
import csv,hashlib,json,platform,subprocess,sys,time
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT))

def rows(name):
 with (OUT/name).open(newline='') as f:return list(csv.DictReader(f))
def dump_csv(name,data):
 with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)

def main():
 lock=json.loads((OUT/'ORACLE_LOCK.json').read_text())
 assert hashlib.sha256((OUT/'SCENARIO_DEFINITIONS.csv').read_bytes()).hexdigest()==lock['scenarios_sha256']
 baseline=json.loads((OUT/'BASELINE.json').read_text())
 for name,h in baseline['preservation_hashes'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
 from fastapi.testclient import TestClient
 from backend.app.api.main import app
 assert app.version==baseline['declared_application_version']
 definitions=rows('SCENARIO_DEFINITIONS.csv');results=[];started=datetime.now(timezone.utc).isoformat()
 with TestClient(app) as client,(OUT/'raw/api-responses.jsonl').open('w') as raw:
  for s in definitions:
   data=json.loads(s['input_json']);begin=time.perf_counter()
   if s['kind']=='ACADEMIC':r=client.post('/eligibility',json=data)
   else:r=client.get('/progression/'+data['from_qualification_id'])
   elapsed=time.perf_counter()-begin;body=r.json();raw.write(json.dumps({'scenario_id':s['scenario_id'],'http_status':r.status_code,'request':data,'reference_context_not_sent':json.loads(s['reference_context_json']),'response':body,'elapsed_seconds':elapsed})+'\n')
   issue='';shape=[]
   if r.status_code!=200:actual='HTTP_'+str(r.status_code);shape.append('Unexpected HTTP status')
   elif s['kind']=='ACADEMIC':
    actual=body['assessment_status']
    if body.get('academic_gap_insights',{}).get('status')!=actual:shape.append('Response/insight status differs')
    if body['eligible'] and actual!='MET':shape.append('Legacy boolean true outside MET')
    if actual=='MET' and 'not guaranteed' not in body['summary'].lower():shape.append('Missing admission caveat')
    if actual=='NOT_ASSESSED' and 'not a rejection' not in body['summary'].lower():shape.append('Missing uncertainty/rejection distinction')
    if actual=='NOT_ASSESSED' and body.get('failed'):shape.append('Unknown result also contains known failed branches; review OR semantics')
    if not body.get('academic_gap_insights',{}).get('groups'):issue='MISSING_RULE_EVIDENCE'
   else:
    edge=next((x for x in body.get('pathways',[]) if x['progression_id']==data['progression_id']),None)
    if edge is None:actual='ROUTE_MISSING';shape.append('Expected route missing')
    else:
     actual='CONDITIONAL_ROUTE_ONLY' if edge['guaranteed'] is False and edge['conditions'] else 'UNCONDITIONAL_OR_UNSUPPORTED_ROUTE'
     if not edge.get('source_url'):shape.append('Missing route source')
     if data['progression_id']=='PROG0003':
      if not all(term in edge['conditions'] for term in ['40','Mathematics for Computing','Mathematics for Data Science','Introduction to Programming','Computer Programming']):shape.append('Module threshold/text differs')
   agreement='AGREE' if actual==s['expected_decision'] else 'DISAGREE'
   if agreement=='DISAGREE':
    issue='INSUFFICIENT_INPUT_CONTRACT' if s['all_oracle_context_representable_in_API']=='false' and actual=='NOT_ASSESSED' else 'DECISION_OR_UNCERTAINTY_SEMANTICS'
   summary=body.get('summary','') if s['kind']=='ACADEMIC' else next((e.get('conditions','') for e in body.get('pathways',[]) if e['progression_id']==data['progression_id']),'')
   results.append({'scenario_id':s['scenario_id'],'programme_id':s['programme_id'],'programme':s['programme'],'kind':s['kind'],'input_conditions':s['input_json'],'reference_context_not_sent':s['reference_context_json'],'expected_decision':s['expected_decision'],'actual_decision':actual,'agreement':agreement,'oracle_type':s['oracle_type'],'all_oracle_context_representable_in_API':s['all_oracle_context_representable_in_API'],'explanation_structural_check':'PASS' if not shape else 'REVIEW: '+'; '.join(shape),'explanation_source_review':'PENDING_EVALUATOR_REVIEW','actual_explanation':summary,'evidence_url':s['evidence_url'],'limitation_or_defect':issue,'http_status':r.status_code})
 dump_csv('EXPECTED_VS_ACTUAL.csv',results)
 direct=[r for r in results if r['oracle_type']=='OFFICIAL_CONDITION' and r['all_oracle_context_representable_in_API']=='true']
 uncertainty=[r for r in results if r['oracle_type']=='SOURCE_GROUNDED_UNCERTAINTY']
 env={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,'python_executable':sys.executable,'python':sys.version,'platform':platform.platform(),'application_version':app.version,'git_commit':baseline['git_commit'],'dependency_versions':{n:version(n) for n in ['fastapi','pydantic','starlette','httpx']},'oracle_sha256':lock['scenarios_sha256'],'case_count':len(results),'all_agreement_counts':dict(Counter(r['agreement'] for r in results)),'direct_official_condition_subset':{'n':len(direct),'counts':dict(Counter(r['agreement'] for r in direct))},'source_grounded_uncertainty_subset':{'n':len(uncertainty),'counts':dict(Counter(r['agreement'] for r in uncertainty))},'structural_explanation_flags':[r['scenario_id'] for r in results if r['explanation_structural_check']!='PASS'],'http_statuses':dict(Counter(str(r['http_status']) for r in results)),'new_application_regression_suite_run':False}
 (OUT/'RUN_MANIFEST.json').write_text(json.dumps(env,indent=2)+'\n')
 for name,h in baseline['preservation_hashes'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
 for r in results:print(r['scenario_id'],r['programme_id'],r['expected_decision'],r['actual_decision'],r['agreement'],r['explanation_structural_check'])
 print(json.dumps(env,indent=2))
 # Disagreements are data, not a reason to erase results or claim the harness failed.
 return 0
if __name__=='__main__':raise SystemExit(main())
