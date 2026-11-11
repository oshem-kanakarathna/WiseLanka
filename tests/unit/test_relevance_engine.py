"""Functional ranking invariants; fabricated preference labels are not used."""
import copy
import math
import pytest
from backend.app.relevance import engine
from backend.app.relevance.encoder import LocalEncoder


def items():
    return [
        {'programme_id':'PRG0001','academic_gap_insights':{'status':'MET'}},
        {'programme_id':'PRG0008','academic_gap_insights':{'status':'NOT_ASSESSED'}},
        {'programme_id':'PRG0009','academic_gap_insights':{'status':'NOT_MET'}},
    ]


def test_tfidf_exact_match_and_unknown_vocabulary():
    scores=engine.tfidf_scores(['business management','computer engineering'],'business management')
    assert scores[0]==pytest.approx(1)
    assert scores[1]==0
    assert engine.tfidf_scores(['business'],'zzzzxxqq')==[0]


def test_empty_preferences_do_not_load_model(monkeypatch):
    def unexpected():raise AssertionError('No model should be loaded')
    monkeypatch.setattr(engine,'get_encoder',unexpected)
    result,meta=engine.rank_recommendations(items(),{})
    assert meta['fallback_reason']=='NO_PREFERENCE'
    assert all(item['relevance']['score'] is None for item in result)


def test_offline_failure_falls_back_with_status(monkeypatch):
    monkeypatch.setattr(engine,'get_encoder',lambda:(None,'OSError'))
    result,meta=engine.rank_recommendations(items(),{'interests':['Business']})
    assert meta['method']=='RULE_BASED_FALLBACK'
    assert meta['status']=='UNAVAILABLE'
    assert [r['programme_id'] for r in result]==['PRG0001','PRG0008','PRG0009']


def test_similarity_cannot_cross_academic_groups():
    before=items(); snapshot=copy.deepcopy(before)
    result,_=engine.rank_recommendations(before,{'interests':['Engineering']},'tfidf')
    assert [r['programme_id'] for r in result]==['PRG0001','PRG0008','PRG0009']
    assert before==snapshot
    assert [r['academic_gap_insights'] for r in result]==[r['academic_gap_insights'] for r in before]


def test_tie_breaking_is_stable():
    original=[{**item,'academic_gap_insights':{'status':'NOT_ASSESSED'}} for item in items()]
    a,_=engine.rank_recommendations(original,{'interests':['zzxxqq']},'tfidf')
    b,_=engine.rank_recommendations(original,{'interests':['zzxxqq']},'tfidf')
    assert a==b
    assert [r['programme_id'] for r in a]==[r['programme_id'] for r in original]


def test_missing_description_does_not_create_score(monkeypatch):
    original=engine.catalogue_documents
    def sparse():
        docs=original();docs['PRG0008']['text']='';return docs
    monkeypatch.setattr(engine,'catalogue_documents',sparse)
    result,_=engine.rank_recommendations(items(),{'interests':['Business']},'tfidf')
    item=next(r for r in result if r['programme_id']=='PRG0008')
    assert item['relevance']['status']=='NOT_ASSESSED'
    assert item['relevance']['score'] is None


def test_model_inference_failure_is_controlled(monkeypatch):
    class Broken:
        def encode(self,text):raise RuntimeError('synthetic model failure')
    engine.document_embeddings.cache_clear()
    monkeypatch.setattr(engine,'get_encoder',lambda:(Broken(),None))
    _,meta=engine.rank_recommendations(items(),{'interests':['Business']})
    assert meta['fallback_reason']=='LOCAL_MODEL_UNAVAILABLE'


def test_checksum_failure_rejects_model(tmp_path):
    pytest.importorskip('onnxruntime')
    with pytest.raises((OSError,ValueError)):
        LocalEncoder(tmp_path)


def test_query_uses_intention_and_explicit_career():
    text=engine.preference_text({'interests':['Computing'],'career_intention':'Build applications','career_goal_id':'CAR0001'})
    assert 'Computing' in text and 'Build applications' in text and 'Software Engineer' in text


def test_unsupported_method_rejected():
    with pytest.raises(ValueError):engine.rank_recommendations(items(),{},'self_learning')


def test_nonfinite_model_output_is_not_clamped_into_a_valid_score(monkeypatch):
    np=pytest.importorskip('numpy')
    class Nonfinite:
        def encode(self,texts):return np.full((len(texts),384),float('nan'))
    engine.document_embeddings.cache_clear()
    monkeypatch.setattr(engine,'get_encoder',lambda:(Nonfinite(),None))
    results,meta=engine.rank_recommendations(items(),{'interests':['Business']})
    assert meta['method']=='RULE_BASED_FALLBACK'
    assert all(item['relevance']['score'] is None for item in results)
    engine.document_embeddings.cache_clear()
