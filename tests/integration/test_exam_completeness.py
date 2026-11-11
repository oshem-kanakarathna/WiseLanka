"""Evidence completeness must be declared, never inferred from a partial list."""
import pytest
from fastapi.testclient import TestClient

from backend.app.api.main import app
from backend.app.eligibility.engine import assess_academic_gaps

client = TestClient(app)
FIVE = {'O_LEVEL': {'Mathematics': 'C', 'English': 'C', 'Science': 'C',
                    'ICT': 'S', 'Sinhala': 'S'}}


@pytest.mark.parametrize('endpoint', ['/eligibility', '/personalised-recommendations'])
@pytest.mark.parametrize('flags, expected', [
    (None, 'NOT_ASSESSED'),  # None here means omit the JSON field.
    ({}, 'NOT_ASSESSED'),
    ({'A_LEVEL': True}, 'NOT_ASSESSED'),
    ({'O_LEVEL': False}, 'NOT_ASSESSED'),
    ({'O_LEVEL': True}, 'NOT_MET'),
])
def test_partial_ol_count_requires_level_specific_completeness(endpoint, flags, expected):
    context = {} if flags is None else {'education_complete': flags}
    payload = ({'programme_id': 'PRG0004', 'student_results': FIVE, **context}
               if endpoint == '/eligibility' else
               {'learner_profile': {'education': FIVE, **context}})
    response = client.post(endpoint, json=payload)
    assert response.status_code == 200
    data = response.json()
    insight = (data['academic_gap_insights'] if endpoint == '/eligibility' else
               next(i for i in data['academic_insights'] if i['programme_id'] == 'PRG0004'))
    assert insight['status'] == expected
    count = next(g for g in insight['groups'] if g['group_id'] == 'GRP007')
    assert count['status'] == expected
    if endpoint == '/eligibility' and expected == 'NOT_ASSESSED':
        assert data['failed'] == []
        assert 'not a rejection' in data['summary']
        assert any('completeness' in message.lower() for message in data['not_assessed'])


@pytest.mark.parametrize('endpoint', ['/eligibility', '/personalised-recommendations'])
@pytest.mark.parametrize('flags', [None, {'O_LEVEL': None}, {'O_LEVEL': ''}])
def test_null_or_empty_string_flags_are_validation_errors(endpoint, flags):
    payload = ({'programme_id': 'PRG0004', 'student_results': FIVE, 'education_complete': flags}
               if endpoint == '/eligibility' else
               {'learner_profile': {'education': FIVE, 'education_complete': flags}})
    response = client.post(endpoint, json=payload)
    assert response.status_code == 422
    assert 'assessment_status' not in response.json()


@pytest.mark.parametrize('pid, education, group_id', [
    ('PRG0001', {'A_LEVEL': {'Physics': 'C', 'Chemistry': 'S'}}, 'GRP001'),
    ('PRG0002', {'A_LEVEL': {'Physics': 'C'}}, 'GRP003'),
])
def test_al_count_predicates_follow_the_same_evidence_semantics(pid, education, group_id):
    unknown = assess_academic_gaps(pid, education)
    complete = assess_academic_gaps(pid, education, {'A_LEVEL': True})
    assert next(g for g in unknown['groups'] if g['group_id'] == group_id)['status'] == 'NOT_ASSESSED'
    assert unknown['status'] == 'NOT_ASSESSED'
    assert next(g for g in complete['groups'] if g['group_id'] == group_id)['status'] == 'NOT_MET'
    assert complete['status'] == 'NOT_MET'


@pytest.mark.parametrize('complete', [None, {}, {'O_LEVEL': False}, {'O_LEVEL': True}])
def test_positive_counts_and_known_subject_failures_do_not_need_completeness(complete):
    six = {'O_LEVEL': {**FIVE['O_LEVEL'], 'History': 'S'}}
    assert assess_academic_gaps('PRG0004', six, complete)['status'] == 'MET'
    low = {'O_LEVEL': {**FIVE['O_LEVEL'], 'Mathematics': 'S'}}
    assert assess_academic_gaps('PRG0004', low, complete)['status'] == 'NOT_MET'


def test_empty_examination_and_qualification_only_stay_unknown():
    assert assess_academic_gaps('PRG0004', {'O_LEVEL': {}}, {'O_LEVEL': True})['status'] == 'NOT_ASSESSED'
    award = [{'qualification_id': 'QLF0012', 'title': 'Electrician (NVQ Level 4 Certificate)'}]
    assert assess_academic_gaps('PRG0010', {}, existing_qualifications=award)['status'] == 'NOT_ASSESSED'
