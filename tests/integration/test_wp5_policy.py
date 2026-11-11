"""Confirmed policy omissions and missing-evidence semantics from source review."""
import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app
from backend.app.eligibility.engine import assess_academic_gaps

@pytest.mark.parametrize('pid',['PRG0001','PRG0002','PRG0003','PRG0009'])
def test_state_university_subject_passes_do_not_establish_formal_eligibility(pid):
 result=assess_academic_gaps(pid,{'A_LEVEL':{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'}})
 assert result['status']=='NOT_ASSESSED'
 policy=[r for g in result['groups'] for r in g['requirements'] if r['source_id']=='SRC0021']
 assert policy and all(r['status']=='NOT_ASSESSED' for r in policy)
 assert all('30 percent' in r['description'] for r in policy)
 with TestClient(app) as client:
  response=client.post('/eligibility',json={'programme_id':pid,'student_results':{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'}}).json()
 assert response['eligible'] is False
 assert response['assessment_status']=='NOT_ASSESSED'
 assert response['failed']==[]


def test_confirmed_complete_results_can_establish_unmet_or_group():
 results={'A_LEVEL':{'Combined Mathematics':'S','Physics':'S','Chemistry':'S'}}
 unknown=assess_academic_gaps('PRG0001',results,{'A_LEVEL':False})
 complete=assess_academic_gaps('PRG0001',results,{'A_LEVEL':True})
 assert unknown['status']=='NOT_ASSESSED'
 assert complete['status']=='NOT_MET'
