"""Evidence-grounded synthetic scenarios; not educational-effectiveness research."""
import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app
from backend.app.eligibility.engine import assess_academic_gaps
from backend.app.progression.engine import get_progression_pathways

client = TestClient(app)
MATHS = {'A_LEVEL': {'Combined Mathematics': 'B', 'Physics': 'C', 'Chemistry': 'C'}}
BUSINESS = {'A_LEVEL': {'Business Studies': 'B', 'Economics': 'C', 'Accounting': 'C'}}


def post(education, **fields):
    response = client.post('/personalised-recommendations', json={'learner_profile': {'education': education, **fields}})
    assert response.status_code == 200
    return response.json()


def by_id(data, programme):
    return next(p for p in data['recommendations'] if p['programme_id'] == programme)


def test_it_al_legacy_requirements_still_met():
    result=by_id(post(MATHS), 'PRG0001')['academic_gap_insights']
    assert result['groups'][0]['status']=='MET'
    assert result['status']=='NOT_ASSESSED'


def test_business_al_route_met_but_selection_not_inferred():
    item = by_id(post(BUSINESS, interests=['Business']), 'PRG0008')
    insight = item['academic_gap_insights']
    assert insight['groups'][0]['status'] == 'MET'
    assert insight['status'] == 'NOT_ASSESSED'
    assert item['eligible'] is False
    assert 'SRC0016' in {r['source_id'] for g in insight['groups'] for r in g['requirements']}


def test_engineering_al_subjects_met_without_guaranteed_selection():
    insight = by_id(post(MATHS), 'PRG0009')['academic_gap_insights']
    assert insight['groups'][0]['status'] == 'MET'
    assert insight['status'] == 'NOT_ASSESSED'


def test_engineering_documented_subject_requirement_not_met():
    result = assess_academic_gaps('PRG0009', {'A_LEVEL': {**MATHS['A_LEVEL'], 'Physics': 'F'}})
    assert result['status'] == 'NOT_MET'
    assert any(r['status']=='NOT_MET' and 'Physics' in r['description'] for g in result['groups'] for r in g['requirements'])


def test_engineering_missing_subject_is_unknown():
    assert assess_academic_gaps('PRG0009', {'A_LEVEL': {'Combined Mathematics':'B'}})['status'] == 'NOT_ASSESSED'


def test_vocational_qualification_and_conditional_pathway():
    data = post({}, learner_category='VOCATIONAL_LEARNER', existing_qualifications=[{
        'qualification_id': 'QLF0010', 'title': 'Higher National Diploma in Mechatronics Technology',
    }])
    recommendation = next(p for p in data['recommendations'] if p['programme_id']=='PRG0011')
    assert recommendation['eligible'] is False
    assert recommendation['academic_gap_insights']['status'] == 'NOT_ASSESSED'
    result = next(p for p in data['academic_insights'] if p['programme_id']=='PRG0011')
    assert result['groups'][0]['status'] == 'MET'  # Reported category, not verified award.
    assert result['status'] == 'NOT_ASSESSED'
    pathway = data['held_qualification_progression'][0]['pathways'][0]
    assert pathway['to_qualification_id'] == 'QLF0011'
    assert pathway['guaranteed'] is False
    assert pathway['source_url'].startswith('https://uovt.ac.lk/')
    assert pathway['supporting_source_url'].endswith('admission_page')


def test_nvq4_entry_is_reported_category_not_framework_equivalence():
    data = post({}, existing_qualifications=[{'qualification_id':'QLF0012','title':'Electrician (NVQ Level 4 Certificate)'}])
    result = next(p for p in data['academic_insights'] if p['programme_id']=='PRG0010')
    assert result['groups'][0]['status']=='MET'
    assert result['status']=='NOT_ASSESSED'
    assert data['held_qualification_progression'][0]['pathways'][0]['to_qualification_id']=='QLF0010'


def test_unknown_custom_award_does_not_infer_nvq_route():
    data = post({}, existing_qualifications=[{'title':'Synthetic unrelated award','framework':'NVQ','level':'6'}])
    assert all(p['status']=='NOT_ASSESSED' for p in data['academic_insights'])
    assert data['held_qualification_progression']==[]


def test_direct_eligibility_empty_rules_not_rejection_and_sources_reach_response():
    unknown=client.post('/eligibility',json={'programme_id':'PRG9999','student_results':{}})
    assert unknown.json()['assessment_status']=='NOT_ASSESSED'
    result=client.post('/eligibility',json={'programme_id':'PRG0009','student_results':MATHS}).json()
    assert result['assessment_status']=='NOT_ASSESSED'
    assert result['requirement_sources'][0]['source_organisation']=='University of Peradeniya'
    assert result['requirement_sources'][0]['source_accessed']=='2026-10-29'
    assert result['failed']==[]


def test_missing_knowledge_file_returns_503(monkeypatch):
    from backend.app.eligibility import engine
    def missing(path):
        raise FileNotFoundError(path)
    monkeypatch.setattr(engine,'load_csv',missing)
    result=client.post('/eligibility',json={'programme_id':'PRG0001','student_results':MATHS})
    assert result.status_code==503
    assert 'No eligibility decision' in result.json()['detail']


def test_application_startup_validates_real_catalogue():
    with TestClient(app) as running:
        assert running.get('/').status_code==200


def test_iit_progression_rechecked_threshold_and_source():
    pathway=next(p for p in get_progression_pathways('QLF0004')['pathways'] if p['to_qualification_id']=='QLF0007')
    assert '40 percent' in pathway['conditions']
    assert pathway['last_verified_date']=='2026-10-29'
    assert pathway['source_url']=='https://www.iit.ac.lk/foundation/it/'


def test_iit_foundation_ol_requirements_link_to_detailed_entry_source():
    result = client.post('/eligibility', json={
        'programme_id': 'PRG0004',
        'student_results': {'O_LEVEL': {
            'Mathematics': 'A', 'English': 'A', 'Science': 'A',
            'ICT': 'A', 'Sinhala': 'A', 'History': 'A',
        }},
        'education_complete': {'O_LEVEL': True},
    })
    assert result.status_code == 200
    data = result.json()
    assert data['assessment_status'] == 'MET'
    source_by_id = {source['source_id']: source for source in data['requirement_sources']}
    assert source_by_id['SRC0010']['source_url'] == 'https://www.iit.ac.lk/foundation/it/'
    requirement_sources = {
        item['requirement_id']: item['source_id']
        for group in data['academic_gap_insights']['groups']
        for item in group['requirements']
    }
    assert {requirement_sources[f'REQ00{i}'] for i in range(14, 18)} == {'SRC0010'}


@pytest.mark.parametrize('endpoint, extra', [
    ('/eligibility', {'programme_id':'PRG0009'}),
    ('/recommendations', {}),
    ('/alternative-pathways/PRG0006', {}),
])
def test_all_academic_endpoints_reject_invalid_grades(endpoint, extra):
    result=client.post(endpoint,json={**extra,'student_results': {'Physics':'INVALID'}})
    assert result.status_code==422
