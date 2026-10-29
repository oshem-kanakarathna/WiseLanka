"""Run from repository root with both local servers running; retain exit codes."""
import subprocess,os,json,time,sys
from pathlib import Path
root=Path.cwd();out=root/'docs/evidence/wp5';py=sys.executable
env=dict(os.environ,WISELANKA_MODEL_DIR=os.environ.get('WISELANKA_MODEL_DIR',str(root/'.models/1110a243fdf4706b3f48f1d95db1a4f5529b4d41')),WISELANKA_API_BASE=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8011'),WISELANKA_EVIDENCE_DIR=str(out/'wp1-regression'))
def imported(path,attr=None,folder=None):
 return "import importlib.util; from pathlib import Path; s=importlib.util.spec_from_file_location('evaluation',"+repr(path)+");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"+("m."+attr+"=Path("+repr(str(out/folder))+");m."+attr+".mkdir(parents=True,exist_ok=True);" if attr else '')+"m.main()"
jobs=[('backend',[py,'-m','pytest','tests','-q']),('browser',[py,'-m','unittest','discover','-s','frontend/browser_tests','-p','test_*.py']),('csv-integrity',[py,'-m','backend.app.data_integrity']),('scenario-evaluation',[py,'scripts/evaluate_wp5.py']),('ranker-comparison',[py,'-c',imported('scripts/evaluate_wp3.py','OUTPUT','.')]),('live-original',[py,'frontend/browser_tests/live_integration_check.py']),('live-wp1',[py,'frontend/browser_tests/live_learner_gap_check.py']),('live-wp2',[py,'-c',imported('frontend/browser_tests/live_wp2_check.py','EVIDENCE','wp2-regression')]),('live-wp3',[py,'-c',imported('frontend/browser_tests/live_wp3_check.py','OUTPUT','wp3-regression')]),('live-wp4',[py,'-c',imported('frontend/browser_tests/live_wp4_check.py','OUT','wp4-regression')]),('accessibility',[py,'scripts/audit_accessibility_wp5.py']),('runtime-probe',[py,'scripts/probe_runtime_wp5.py']),('pip-check',[py,'-m','pip','check'])]
results=[]
for name,command in jobs:
 start=time.time()
 with (out/(name+'.log')).open('w') as f:r=subprocess.run(command,env=env,stdout=f,stderr=subprocess.STDOUT)
 result={'check':name,'exit_code':r.returncode,'elapsed_seconds':round(time.time()-start,3),'command':command}
 results.append(result);(out/'verification.json').write_text(json.dumps(results,indent=2)+'\n');print(name,r.returncode,flush=True)

if any(result['exit_code'] for result in results):sys.exit(1)
