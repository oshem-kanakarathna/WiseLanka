from backend.app.eligibility import engine


def test_missing_programme_rules_is_not_assessed():
    assert engine.assess_academic_gaps('PRG9999', {'Physics': 'A'})['status'] == 'NOT_ASSESSED'


def test_missing_source_evidence_is_not_assessed(monkeypatch):
    original = engine.load_csv
    monkeypatch.setattr(engine, 'load_csv', lambda path: [] if path == 'metadata/evidence_sources.csv' else original(path))
    data = engine.assess_academic_gaps('PRG0004', {'O_LEVEL': {'English': 'A'}})
    assert data['status'] == 'NOT_ASSESSED'
    assert all(r['status'] == 'NOT_ASSESSED' for g in data['groups'] for r in g['requirements'])


def test_or_group_does_not_require_all_options():
    data = engine.assess_academic_gaps('PRG0001', {'Physics': 'C', 'Chemistry': 'S', 'Art': 'S'})
    assert data['status'] == 'NOT_ASSESSED'
    assert next(g for g in data['groups'] if g['operator']=='OR')['status']=='MET'
    assert any(r['status'] == 'NOT_ASSESSED' for g in data['groups'] for r in g['requirements'])


def test_or_group_unknown_is_not_failed(monkeypatch):
    original = engine.load_csv
    def load(path):
        rows = original(path)
        if path == 'relationships/programme_entry_requirements.csv':
            return [{**r, 'source_id': ''} if r['requirement_id'] == 'REQ0005' else r for r in rows]
        return rows
    monkeypatch.setattr(engine, 'load_csv', load)
    data = engine.assess_academic_gaps('PRG0001', {'Higher Mathematics': 'S', 'Combined Mathematics': 'S', 'Mathematics': 'S'})
    assert data['status'] == 'NOT_ASSESSED'


def test_unsupported_rule_is_not_assessed(monkeypatch):
    original = engine.load_csv
    def load(path):
        rows = original(path)
        if path == 'relationships/programme_entry_requirements.csv':
            return [{**r, 'requirement_type': 'UNSUPPORTED_RULE'} if r['programme_id'] == 'PRG0004' else r for r in rows]
        return rows
    monkeypatch.setattr(engine, 'load_csv', load)
    data = engine.assess_academic_gaps('PRG0004', {'O_LEVEL': {'English': 'C'}})
    assert data['status'] == 'NOT_ASSESSED'
