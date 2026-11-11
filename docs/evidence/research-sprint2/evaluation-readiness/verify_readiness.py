"""Read-only structural/integrity audit; never generates human judgements."""
from pathlib import Path
import csv, hashlib, json, math, statistics, subprocess
O = Path(__file__).resolve().parent
A = O.parent / 'ai-ranking'
ROOT = O.parents[3]
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(newline='') as f:
        return list(csv.DictReader(f))
baseline = json.loads((A / 'BASELINE.json').read_text())
summary = json.loads((A / 'SUMMARY.json').read_text())
for p, h in json.loads((A / 'EVIDENCE_SHA256.json').read_text()).items():
    assert digest(A / p) == h, p
for p, h in baseline['dataset_hashes'].items():
    assert digest(ROOT / p) == h, p
for p, h in baseline['actual_model_hashes'].items():
    assert digest(Path(baseline['model_directory']) / p) == h, p
for p, h in baseline['protected_tracked_and_backup_hashes'].items():
    assert digest(ROOT / p) == h, p
warm = read(A / 'raw/warm-samples.csv')
results = read(A / 'COMPARATOR_RESULTS.csv')
assert len(warm) == 1890 and len(results) == 63
for row in results:
    samples = [x for x in warm if (x['scenario_id'], x['requested_method']) == (row['scenario_id'], row['requested_method'])]
    durations = [float(x['duration_ms']) for x in samples]
    assert len(samples) == 30
    assert statistics.median(durations) == float(row['median_rank_ms'])
    assert sorted(durations)[math.ceil(.95 * len(durations))-1] == float(row['p95_rank_ms'])
    order = json.loads(row['ordered_ids_json'])
    scores = json.loads(row['scores_json'])
    signature = hashlib.sha256(json.dumps({'order': order, 'scores': scores}, sort_keys=True).encode()).hexdigest()
    assert all(x['ranking_and_score_signature'] == signature and x['policy_compliant'] == 'True' for x in samples)
for method, report in summary['warm_actual_method_only'].items():
    v = [float(x['duration_ms']) for x in warm if x['requested_method'] == method and x['actual_method'] == method.upper()]
    assert len(v) == report['samples'] and statistics.median(v) == report['median_ms']
    assert sorted(v)[math.ceil(.95*len(v))-1] == report['p95_ms']
key = json.loads((A / 'raw/blinding-researcher-key.json').read_text())
metadata = read(O / 'RESEARCHER_ONLY_PAIR_REGISTER.csv')
frozen = json.loads((A / 'raw/frozen-candidates.json').read_text())
facts = json.loads((A / 'raw/catalogue-documents.json').read_text())
for pack in ['A', 'B']:
    sheet = read(O / 'relevance-review' / pack / 'RATINGS_BLANK.csv')
    assert len(sheet) == 127
    assert len({(x['case_card_id'], x['candidate_card_id']) for x in sheet}) == 127
    cards = (O / 'relevance-review' / pack / 'CARDS.md').read_text()
    assert cards.count('### Candidate ') == 127 and cards.count('## Case ') == 21
    assert all(s not in cards for s in ['MiniLM', 'TF–IDF', 'TF-IDF', 'SEMANTIC', 'NOT_MET', 'NOT_ASSESSED', 'Fictional profile:', 'http'])
    for row in sheet:
        assert all(not row[k] for k in ['reviewer_code', 'relevance_0_to_3_or_UNJUDGEABLE', 'reason_optional', 'missing_information_optional'])
        opaque = row['case_card_id'] + '-' + row['candidate_card_id']
        ref = key[pack][opaque]
        m = next(x for x in metadata if x['pack_id'] == pack and x['case_card_id'] == row['case_card_id'] and x['candidate_card_id'] == row['candidate_card_id'])
        assert (m['scenario_id'], m['programme_id']) == (ref['scenario_id'], ref['programme_id'])
        item = next(i for i in frozen[m['scenario_id']]['items'] if i['programme_id'] == m['programme_id'])
        state = item.get('academic_gap_insights', {}).get('status', item.get('status', 'NOT_ASSESSED'))
        assert state == m['academic_status']
        assert facts[m['programme_id']]['text'] in cards
for p in (O / 'templates').glob('*_BLANK.csv'):
    assert read(p) == [], p
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).strip()
assert not subprocess.check_output(['git', 'diff', '--name-only', '--', 'backend', 'frontend', 'data', 'tests', 'scripts'], cwd=ROOT, text=True).strip()
print(json.dumps({'archive_hashes_unchanged': True, 'protected_files_unchanged': True,
                  'comparator_rows': len(results), 'warm_samples_checked': len(warm),
                  'revised_blank_pairs_per_pack': 127, 'programme_coverage': len(facts),
                  'blank_observation_templates': len(list((O/'templates').glob('*_BLANK.csv'))),
                  'no_human_response_data': True, 'staging_empty': True}, indent=2))
