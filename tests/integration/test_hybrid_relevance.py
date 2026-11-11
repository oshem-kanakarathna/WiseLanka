from fastapi.testclient import TestClient
from backend.app.api.main import app
from backend.app.relevance import engine

client=TestClient(app)


def test_api_unavailable_model_preserves_academic_fields(monkeypatch):
    monkeypatch.setattr(engine,'get_encoder',lambda:(None,'missing'))
    result=client.post('/personalised-recommendations',json={'learner_profile':{
        'education':{'Physics':'C','Chemistry':'C','Combined Mathematics':'B'},
        'career_intention':'Create intelligent software',
    }})
    assert result.status_code==200
    data=result.json()
    assert data['ranking']['method']=='RULE_BASED_FALLBACK'
    assert all(not p['eligible'] and p['academic_gap_insights']['status']=='NOT_ASSESSED' for p in data['recommendations'] if p['programme_id'] in {'PRG0001','PRG0002','PRG0003'})
    assert all(p['relevance']['score'] is None for p in data['recommendations'])


def test_vocational_exploration_has_relevance_without_eligibility_promotion():
    result=client.post('/personalised-recommendations',json={'learner_profile':{
        'education':{},'existing_qualifications':[{'qualification_id':'QLF0010','title':'Higher National Diploma in Mechatronics Technology'}],
        'career_intention':'Work with robotics and factory automation',
    }})
    assert result.status_code==200
    data=result.json()
    route=next(p for p in data['recommendations'] if p['programme_id']=='PRG0011')
    assert route['academic_gap_insights']['status']=='NOT_ASSESSED'
    assert route['eligible'] is False
    assert 'relevance' in route
    assert data['academic_insights']
    assert all(p['status']=='NOT_ASSESSED' for p in data['academic_insights'])


def test_intention_length_is_bounded():
    result=client.post('/personalised-recommendations',json={'learner_profile':{'education':{'Physics':'C'},'career_intention':'a'*301}})
    assert result.status_code==422


def test_real_encoder_synonym_and_unknown_input():
    import math
    import pytest
    from backend.app.relevance.encoder import get_encoder
    encoder,error=get_encoder()
    if encoder is None:pytest.skip('Optional local model unavailable: '+str(error))
    values=encoder.encode(['software development','building computer applications','zzqqxxvv'])
    assert values.shape==(3,384)
    assert all(math.isfinite(float(x)) for row in values for x in row)
    assert float(values[0]@values[1]) > float(values[0]@values[2])


def test_real_semantic_business_match_keeps_unknown_status():
    import pytest
    from backend.app.relevance.encoder import get_encoder
    if get_encoder()[0] is None:pytest.skip('Optional local model unavailable')
    result=client.post('/personalised-recommendations',json={'learner_profile':{
        'education':{'Business Studies':'C','Accounting':'C','Economics':'C'},
        'career_intention':'I want to manage a business and lead organisations',
    }}).json()
    assert result['ranking']['method']=='SEMANTIC'
    assert result['recommendations'][0]['programme_id'] in {'PRG0008', 'PRG0013'}
    business = next(item for item in result['recommendations'] if item['programme_id'] in {'PRG0008', 'PRG0013'})
    assert business['academic_gap_insights']['status']=='NOT_ASSESSED'


def test_real_encoder_stability_and_finite_unknown_vocabulary():
    import pytest
    from backend.app.relevance.encoder import get_encoder
    if get_encoder()[0] is None:pytest.skip('Optional model unavailable')
    candidates=[{'programme_id':pid,'academic_gap_insights':{'status':'NOT_ASSESSED'}} for pid in ('PRG0001','PRG0008','PRG0009')]
    for intention in ('Develop computer applications','Manage organisations','Design engineering systems','zzxxqqvv'):
        a,meta=engine.rank_recommendations(candidates,{'career_intention':intention})
        b,_=engine.rank_recommendations(candidates,{'career_intention':intention})
        assert meta['method']=='SEMANTIC'
        assert a==b
        assert all(-1<=item['relevance']['score']<=1 for item in a)
        assert all(item['academic_gap_insights']['status']=='NOT_ASSESSED' for item in a)
