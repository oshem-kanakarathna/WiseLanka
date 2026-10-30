"""Run current live workflows against a fresh API without changing saved WP evidence."""
import importlib.util,json,os,socket,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
processes=[];handles=[];results=[]
def wait(url):
    for _ in range(100):
        try:
            with urllib.request.urlopen(url,timeout=1) as r:return r.read()
        except Exception:time.sleep(.1)
    raise RuntimeError('Server unavailable: '+url)
try:
    try:page=urllib.request.urlopen('http://127.0.0.1:5500/frontend/pages/learner-profile.html',timeout=1).read()
    except Exception:
        f=(OUT/'raw/static-server.txt').open('w');handles.append(f)
        processes.append(subprocess.Popen([sys.executable,'-m','http.server','5500','--bind','127.0.0.1'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT))
        page=wait('http://127.0.0.1:5500/frontend/pages/learner-profile.html')
    assert b'WiseLanka' in page
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    api='http://127.0.0.1:'+str(port)
    env=dict(os.environ,WISELANKA_MODEL_DIR=str(ROOT/'.models/1110a243fdf4706b3f48f1d95db1a4f5529b4d41'),WISELANKA_API_BASE=api)
    f=(OUT/'raw/api-server.txt').open('w');handles.append(f)
    processes.append(subprocess.Popen([sys.executable,'-m','uvicorn','backend.app.api.main:app','--host','127.0.0.1','--port',str(port)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT))
    wait(api+'/')
    for name,path,attr in [('original','live_integration_check.py',None),('wp1','live_learner_gap_check.py','EVIDENCE'),('wp2','live_wp2_check.py','EVIDENCE'),('wp3','live_wp3_check.py','OUTPUT'),('wp4','live_wp4_check.py','OUT')]:
        folder=OUT/'live'/name;folder.mkdir(parents=True,exist_ok=True)
        # All evidence destinations are overridden before the existing script's main call.
        code="import importlib.util; from pathlib import Path; s=importlib.util.spec_from_file_location('live_check',"+repr(str(ROOT/'frontend/browser_tests'/path))+");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        if attr:code+='m.'+attr+'=Path('+repr(str(folder))+');'
        code+='m.main()'
        with (OUT/'raw'/('live-'+name+'.txt')).open('w') as output:
            p=subprocess.run([sys.executable,'-c',code],cwd=ROOT,env=dict(env,WISELANKA_EVIDENCE_DIR=str(folder)),stdout=output,stderr=subprocess.STDOUT)
        results.append({'workflow':name,'exit_code':p.returncode,'api':api,'output':'raw/live-'+name+'.txt'})
        print(name,p.returncode,flush=True)
    # EC08 also checked over real HTTP, beyond in-process TestClient.
    original=OUT.parent/'educational-correctness'
    import csv
    with (original/'SCENARIO_DEFINITIONS.csv').open(newline='') as f:case=next(r for r in csv.DictReader(f) if r['scenario_id']=='EC08')
    request=urllib.request.Request(api+'/eligibility',data=case['input_json'].encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request) as r:body=json.load(r)
    assert body['assessment_status']=='NOT_ASSESSED' and body['failed']==[]
    (OUT/'raw/live-EC08.json').write_text(json.dumps(body,indent=2)+'\n')
    results.append({'workflow':'EC08-real-HTTP','exit_code':0,'api':api,'output':'raw/live-EC08.json'})
finally:
    for p in processes:
        if p.poll() is None:p.terminate();p.wait(timeout=10)
    for h in handles:h.close()
    (OUT/'LIVE_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
if len(results)!=6 or any(r['exit_code'] for r in results):raise SystemExit(1)
