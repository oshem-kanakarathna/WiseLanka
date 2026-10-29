"""Local HTTP timing and isolated missing-model recovery checks; synthetic input."""
import json,os,statistics,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/wp5'
PAYLOAD={'learner_profile':{'education':{'A_LEVEL':{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'}},'career_intention':'Build software applications'}}
def main():
 url=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8011')+'/personalised-recommendations'
 times=[]
 for _ in range(40):
  request=urllib.request.Request(url,data=json.dumps(PAYLOAD).encode(),headers={'Content-Type':'application/json'})
  start=time.perf_counter()
  with urllib.request.urlopen(request,timeout=20) as response:result=json.load(response)
  times.append(time.perf_counter()-start)
  assert result['ranking']['method']=='SEMANTIC'
 code="""from fastapi.testclient import TestClient
from backend.app.api.main import app
import json
with TestClient(app) as client:
 response=client.post('/personalised-recommendations',json=PAYLOAD)
 assert response.status_code==200
 result=response.json()
 assert result['ranking']['method']=='RULE_BASED_FALLBACK'
 assert result['ranking']['fallback_reason']
 print(json.dumps(result['ranking']))
""".replace('json=PAYLOAD','json='+repr(PAYLOAD))
 env=dict(os.environ,WISELANKA_MODEL_DIR=str(ROOT/'.wp5-deliberately-absent-model'))
 fallback=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env=env,capture_output=True,text=True)
 assert fallback.returncode==0,fallback.stderr
 record={'transport':'local HTTP urllib, existing warm server, no browser rendering','requests':40,'median_seconds':statistics.median(times),'p95_seconds':sorted(times)[37],'missing_model_subprocess_exit_code':fallback.returncode,'missing_model_response':json.loads(fallback.stdout),'recovery':'Following isolated failure, real-model server still responds SEMANTIC; failed model setup in a running process requires restart after provisioning.'}
 with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(PAYLOAD).encode(),headers={'Content-Type':'application/json'})) as response:assert json.load(response)['ranking']['method']=='SEMANTIC'
 (OUT/'runtime-network.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record,indent=2))
if __name__=='__main__':main()
