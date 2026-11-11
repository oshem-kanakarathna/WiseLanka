"""Knowledge failures must not be interpreted as absent learner eligibility."""
import pytest
from backend.app import data_loader, data_integrity
from backend.app.data_loader import KnowledgeDataError
from backend.app.eligibility import evaluate_programme, grade_meets_minimum
from backend.app.eligibility.engine import assess_academic_gaps, evaluate_programme as canonical
from backend.app.recommendation.engine import recommend_programmes


def test_public_eligibility_uses_single_implementation():
    assert evaluate_programme is canonical
    assert evaluate_programme('PRG9999', {})['eligible'] is False
    assert grade_meets_minimum('INVALID', 'INVALID') is False


def test_complete_catalogue_integrity():
    counts = data_integrity.validate_catalogue()
    assert counts['programmes'] == 15
    assert counts['qualifications'] == 16
    assert counts['progression'] == 5


def test_stage14_catalogue_records_are_sourced_and_conservative():
    data_integrity.validate_catalogue()
    programmes = {row['programme_id']: row for row in data_loader.load_csv('reference/programmes.csv')}
    requirements = data_loader.load_csv('relationships/programme_entry_requirements.csv')
    sources = {row['source_id']: row for row in data_loader.load_csv('metadata/evidence_sources.csv')}

    assert {programmes[pid]['source_id'] for pid in ('PRG0012', 'PRG0013', 'PRG0014', 'PRG0015')} == {
        'SRC0022', 'SRC0023', 'SRC0024'
    }
    assert programmes['PRG0014']['last_verified_date'] == '2026-11-07'
    assert '2025-10-31' in programmes['PRG0014']['notes']
    assert sources['SRC0025']['publication_date'] == '2025-10-31'
    assert all(sources[sid]['retrieved_date'] == '2026-11-07' for sid in ('SRC0022', 'SRC0023', 'SRC0024', 'SRC0025'))

    for programme_id in ('PRG0012', 'PRG0013', 'PRG0014', 'PRG0015'):
        rows = [row for row in requirements if row['programme_id'] == programme_id]
        assert rows
        assert all(row['source_id'] in sources for row in rows)

    # PRG0005-7 have no direct entry criteria on the reviewed official course
    # pages, so their unsupported direct-entry decisions stay NOT_ASSESSED.
    for programme_id in ('PRG0005', 'PRG0006', 'PRG0007'):
        assert not any(row['programme_id'] == programme_id for row in requirements)
        assert assess_academic_gaps(programme_id, {}, {}, [])['status'] == 'NOT_ASSESSED'

    profile = {
        'O_LEVEL': {'English': 'A', 'Mathematics': 'A', 'Sinhala': 'A'},
        'A_LEVEL': {'Combined Mathematics': 'A', 'Physics': 'A', 'Chemistry': 'A',
                    'Information & Communication Technology': 'A'},
    }
    complete = {'O_LEVEL': True, 'A_LEVEL': True}
    for programme_id in ('PRG0012', 'PRG0013', 'PRG0014', 'PRG0015'):
        assert assess_academic_gaps(
            programme_id, profile, complete, [{'qualification_id': 'QLF0015'}]
        )['status'] == 'NOT_ASSESSED'


def test_iit_foundation_current_requirements_and_progression_are_not_guarantees():
    requirements = [row for row in data_loader.load_csv('relationships/programme_entry_requirements.csv') if row['programme_id'] == 'PRG0004']
    progression = {row['progression_id']: row for row in data_loader.load_csv('relationships/qualification_progression.csv')}
    assert len(requirements) == 4
    assert all(row['source_id'] == 'SRC0010' for row in requirements)
    assert all(progression[f'PROG000{i}']['guaranteed'] == 'false' for i in (1, 2, 3))
    assert '40 percent' in progression['PROG0003']['conditions']


def test_missing_and_header_only_are_different(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, 'DATA_DIR', tmp_path)
    with pytest.raises(FileNotFoundError):
        data_loader.load_csv('missing.csv')
    (tmp_path/'empty.csv').write_text('id,name\n')
    assert data_loader.load_csv('empty.csv') == []


@pytest.mark.parametrize('text', ['', 'id,id\nA,B\n', 'id,name\nA\n', 'id,name\nA,B,C\n'])
def test_malformed_csv_is_rejected(tmp_path, monkeypatch, text):
    monkeypatch.setattr(data_loader, 'DATA_DIR', tmp_path)
    (tmp_path/'bad.csv').write_text(text)
    with pytest.raises(KnowledgeDataError):
        data_loader.load_csv('bad.csv')


def test_csv_loading_independent_of_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert any(p['programme_id'] == 'PRG0008' for p in recommend_programmes({'Economics': 'C','Business Studies':'B','Accounting':'C'}))


@pytest.mark.parametrize('table, mutation', [
    ('reference/programmes.csv', lambda rows: rows + [rows[0]]),
    ('reference/programmes.csv', lambda rows: [{**rows[0], 'qualification_id': 'MISSING'}] + rows[1:]),
    ('relationships/qualification_progression.csv', lambda rows: [{**rows[0], 'source_id': 'MISSING'}] + rows[1:]),
    ('relationships/programme_entry_requirements.csv', lambda rows: [{**rows[0], 'minimum_count': 'invalid'}] + rows[1:]),
    ('relationships/career_skills.csv', lambda rows: rows + [{**rows[0], 'notes': 'different note same relationship'}]),
])
def test_invalid_ids_relationships_and_counts_are_rejected(monkeypatch, table, mutation):
    original = data_integrity.load_csv
    monkeypatch.setattr(data_integrity, 'load_csv', lambda path: mutation(original(path)) if path == table else original(path))
    with pytest.raises(KnowledgeDataError):
        data_integrity.validate_catalogue()
