"""Knowledge failures must not be interpreted as absent learner eligibility."""
import pytest
from backend.app import data_loader, data_integrity
from backend.app.data_loader import KnowledgeDataError
from backend.app.eligibility import evaluate_programme, grade_meets_minimum
from backend.app.eligibility.engine import evaluate_programme as canonical
from backend.app.recommendation.engine import recommend_programmes


def test_public_eligibility_uses_single_implementation():
    assert evaluate_programme is canonical
    assert evaluate_programme('PRG9999', {})['eligible'] is False
    assert grade_meets_minimum('INVALID', 'INVALID') is False


def test_complete_catalogue_integrity():
    counts = data_integrity.validate_catalogue()
    assert counts['programmes'] == 11
    assert counts['progression'] == 5


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
