"""Replay the original 45 source-grounded cases into a separate evidence folder."""
import csv,hashlib,importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
ORIGINAL=OUT.parent/'educational-correctness'
REPLAY=OUT/'recheck'
REPLAY.mkdir(exist_ok=True)
(REPLAY/'raw').mkdir(exist_ok=True)
for name in ('SCENARIO_DEFINITIONS.csv','ORACLE_LOCK.json'):
    (REPLAY/name).write_bytes((ORIGINAL/name).read_bytes())
baseline=json.loads((ORIGINAL/'BASELINE.json').read_text())
baseline['preservation_hashes']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                                 for p in baseline['preservation_hashes']}
baseline['working_tree_patch'] = 'See ../application-and-test-changes.patch; HEAD unchanged, source modifications are explicit.'
(REPLAY/'BASELINE.json').write_text(json.dumps(baseline,indent=2)+'\n')
s=importlib.util.spec_from_file_location('frozen_s2_evaluation',ORIGINAL/'run_evaluation.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.OUT=REPLAY;m.ROOT=ROOT
m.main()

def records(path):
    with path.open(newline='') as f:return {r['scenario_id']:r for r in csv.DictReader(f)}
before=records(ORIGINAL/'EXPECTED_VS_ACTUAL.csv');after=records(REPLAY/'EXPECTED_VS_ACTUAL.csv')
changed=[{'scenario_id':k,'before':before[k]['actual_decision'],'after':v['actual_decision'],
          'expected':v['expected_decision']} for k,v in after.items()
         if before[k]['actual_decision']!=v['actual_decision']]
assert changed==[{'scenario_id':'EC08','before':'NOT_MET','after':'NOT_ASSESSED','expected':'NOT_ASSESSED'}],changed
(OUT/'CONTROLLED_COMPARISON.json').write_text(json.dumps({
    'original_cases':45,'before_agreements':sum(r['agreement']=='AGREE' for r in before.values()),
    'after_agreements':sum(r['agreement']=='AGREE' for r in after.values()),
    'after_disagreements':[k for k,v in after.items() if v['agreement']=='DISAGREE'],
    'only_decision_changes':changed,'original_expectations_unchanged':True,
    'limitation':'Controlled regression comparison on existing synthetic cases, not new independent domain validation.'},indent=2)+'\n')
