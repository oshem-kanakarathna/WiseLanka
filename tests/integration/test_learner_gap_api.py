"""WP1 contracts exercised with synthetic profiles; no participant data."""
import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)
SIX = {"Mathematics": "C", "English": "C", "Science": "S", "ICT": "S", "Sinhala": "S", "History": "S"}


def submit(education=None, **extra):
    return client.post('/personalised-recommendations', json={'learner_profile': {
        'education': {'O_LEVEL': SIX} if education is None else education, **extra,
    }})


def test_six_subject_compatibility():
    result = submit().json()
    assert result['count'] == 1
    assert result['recommendations'][0]['eligible'] is False
    assert result['academic_insights'][0]['status'] == 'NOT_MET'
    credits = next(g for g in result['academic_insights'][0]['groups'] if g['group_id'] == 'GRP008')
    assert credits['status'] == 'NOT_MET'


def test_ninth_subject_credit_changes_real_rule_outcome():
    nine = {**SIX, 'Geography': 'F', 'Commerce': 'F', 'Art': 'C'}
    result = submit({'O_LEVEL': nine}).json()
    assert result['recommendations'][0]['eligible'] is True
    assert result['academic_insights'][0]['status'] == 'MET'


def test_six_subjects_can_already_meet_requirements():
    result = submit({'O_LEVEL': {**SIX, 'Science': 'C'}}).json()
    assert result['recommendations'][0]['eligible'] is True
    assert result['academic_insights'][0]['status'] == 'MET'


@pytest.mark.parametrize('education', [
    {'Physics': 'B', 'Chemistry': 'C', 'Combined Mathematics': 'B'},
    {'A_LEVEL': {'Physics': 'B', 'Chemistry': 'C', 'Combined Mathematics': 'B'}},
])
def test_legacy_al(education):
    response = submit(education)
    assert response.status_code == 200
    assert response.json()['count'] == 5
    assert all(p['academic_gap_insights']['status']=='NOT_ASSESSED' and not p['eligible'] for p in response.json()['recommendations'] if p['programme_id'] in {'PRG0001', 'PRG0002', 'PRG0003'})


@pytest.mark.parametrize('education', [
    {'O_LEVEL': {'English': ''}}, {'O_LEVEL': {'English': 'Z'}},
    {'O_LEVEL': {'English': None}}, {'O_LEVEL': {'English': 'C', ' english ': 'B'}},
    {'O_LEVEL': {' ': 'A'}}, {'NVQ': {'Level': 'C'}},
    {'O_LEVEL': {'English': 'C'}, 'Physics': 'A'},
])
def test_invalid_results_rejected(education):
    assert submit(education).status_code == 422


def test_incomplete_counts_and_missing_subject_not_false_negative():
    result = submit({'O_LEVEL': {'English': 'C'}}, education_complete={'O_LEVEL': False}).json()
    assert result['academic_insights'][0]['status'] == 'NOT_ASSESSED'
    assert all(g['status'] != 'NOT_MET' for g in result['academic_insights'][0]['groups'])


def test_supplied_low_grade_remains_unmet_even_if_profile_incomplete():
    result = submit({'O_LEVEL': {'English': 'S'}}, education_complete={'O_LEVEL': False}).json()
    assert result['academic_insights'][0]['status'] == 'NOT_MET'


def test_qualification_only_does_not_infer_exam_equivalence():
    response = submit({}, learner_category='VOCATIONAL_LEARNER', existing_qualifications=[
        {'title': 'Synthetic vocational award', 'framework': 'NVQ', 'level': '4'},
    ])
    assert response.status_code == 200
    data = response.json()
    assert data['recommendations'] == []
    assert data['existing_qualifications'][0]['framework'] == 'NVQ'
    assert data['academic_insights']
    assert all(item['status'] == 'NOT_ASSESSED' for item in data['academic_insights'])


def test_skills_reported_development_and_unreported_are_distinct():
    result = submit(learner_category='EARLY_CAREER', career_goal_id='CAR0001', self_reported_skills=[
        {'skill_id': 'SKL0001', 'status': 'REPORTED'},
        {'skill_id': 'SKL0002', 'status': 'DEVELOPMENT_OPPORTUNITY'},
    ]).json()
    skills = {s['skill_id']: s for s in result['learner_skill_insights']['career_requirements']}
    assert skills['SKL0001']['status'] == 'SELF_REPORTED'
    assert skills['SKL0002']['status'] == 'DEVELOPMENT_OPPORTUNITY'
    assert skills['SKL0003']['status'] == 'NOT_ASSESSED'
    assert 'not verify competence' in skills['SKL0001']['explanation']


def test_no_skills_is_unassessed_not_incompetent():
    result = submit(career_goal_id='CAR0001').json()['learner_skill_insights']
    assert result['career_requirements']
    assert all(s['status'] == 'NOT_ASSESSED' for s in result['career_requirements'])


def test_unknown_career_preserves_self_reports_without_inventing_requirements():
    result = submit(career_goal_id='CAR9999', self_reported_skills=[{'skill_id': 'SKL0001', 'status': 'REPORTED'}]).json()
    assert result['learner_skill_insights']['status'] == 'NOT_ASSESSED'
    assert result['learner_skill_insights']['career_requirements'] == []
    assert len(result['learner_skill_insights']['reported_skills']) == 1


@pytest.mark.parametrize('extra', [
    {'learner_category': 'OTHER'},
    {'self_reported_skills': [{'skill_id': 'SKL9999', 'status': 'REPORTED'}]},
    {'self_reported_skills': [{'skill_id': 'SKL0001', 'status': 'EXPERT'}]},
    {'self_reported_skills': [{'skill_id': 'SKL0001', 'status': 'REPORTED'}] * 2},
    {'existing_qualifications': [{'title': '   '}]},
])
def test_invalid_structured_context(extra):
    assert submit(**extra).status_code == 422


def test_profile_options_from_existing_csv():
    data = client.get('/profile-options').json()
    assert any(s['skill_id'] == 'SKL0001' for s in data['skills'])
    assert any(q['qualification_id'] == 'QLF0004' for q in data['qualifications'])


def test_structured_context_does_not_change_legacy_recommendation_fields():
    from backend.app.recommendation.engine import recommend_programmes
    education = {'A_LEVEL': {'Physics': 'B', 'Chemistry': 'C', 'Combined Mathematics': 'B'}}
    baseline = {item['programme_id']: item for item in recommend_programmes(education)}
    response = submit(education, learner_category='EARLY_CAREER', existing_qualifications=[
        {'title': 'Synthetic diploma'},
    ], self_reported_skills=[{'skill_id': 'SKL0001', 'status': 'REPORTED'}])
    assert response.status_code == 200
    for item in response.json()['recommendations']:
        assert all(item[key] == value for key, value in baseline[item['programme_id']].items())


def test_qualification_alongside_exams_preserves_exam_rule_failure():
    response = submit(existing_qualifications=[{'title': 'Synthetic additional award'}])
    assert response.status_code == 200
    assert response.json()['academic_insights'][0]['status'] == 'NOT_MET'


@pytest.mark.parametrize('award', [
    {'qualification_id': 'QLF9999', 'title': 'Synthetic award'},
    {'qualification_id': 'QLF0004', 'title': 'Unrelated synthetic award'},
    {'qualification_id': 'QLF0004', 'title': 'Level 3 Diploma', 'framework': 'NVQ'},
    {'qualification_id': 'QLF0004', 'title': 'Level 3 Diploma', 'level': '99'},
])
def test_catalogue_award_rejects_unknown_or_inconsistent_metadata(award):
    assert submit({}, existing_qualifications=[award]).status_code == 422


def test_catalogue_award_fills_omitted_metadata_without_inferred_eligibility():
    response = submit({}, existing_qualifications=[{'qualification_id': 'QLF0004', 'title': ' level 3 diploma '}])
    assert response.status_code == 200
    data = response.json()
    assert data['existing_qualifications'] == [{
        'qualification_id': 'QLF0004', 'title': 'Level 3 Diploma',
        'framework': 'Regulated Qualifications Framework', 'level': '3',
    }]
    assert all(item['status'] == 'NOT_ASSESSED' for item in data['academic_insights'])


def test_custom_award_keeps_self_reported_framework_and_level():
    response = submit({}, existing_qualifications=[{
        'title': 'Synthetic vocational award', 'framework': 'NVQ', 'level': '4', 'qualification_id': '',
    }])
    assert response.status_code == 200
    assert response.json()['existing_qualifications'][0]['level'] == '4'


def test_endpoint_missing_sources_prioritises_unknown_over_legacy_eligible(monkeypatch):
    from backend.app.eligibility import engine
    original = engine.load_csv
    monkeypatch.setattr(engine, 'load_csv', lambda path: [] if path == 'metadata/evidence_sources.csv' else original(path))
    response = submit({'O_LEVEL': {**SIX, 'Science': 'C'}})
    assert response.status_code == 200
    item = response.json()['recommendations'][0]
    assert item['eligible'] is True  # Unchanged legacy rule-only calculation.
    assert item['academic_gap_insights']['status'] == 'NOT_ASSESSED'


def test_endpoint_incomplete_results_do_not_turn_legacy_rejection_into_evidence():
    response = submit({'O_LEVEL': {'English': 'C'}}, education_complete={'O_LEVEL': False})
    assert response.status_code == 200
    item = response.json()['recommendations'][0]
    assert item['eligible'] is False
    assert item['academic_gap_insights']['status'] == 'NOT_ASSESSED'


def test_inactive_catalogue_award_is_rejected(monkeypatch):
    from backend.app.personalisation import models
    original = models.load_csv
    monkeypatch.setattr(models, 'load_csv', lambda path: [
        {**row, 'active_status': 'Inactive'} if row['qualification_id'] == 'QLF0004' else row
        for row in original(path)
    ])
    assert submit({}, existing_qualifications=[{'qualification_id': 'QLF0004', 'title': 'Level 3 Diploma'}]).status_code == 422
