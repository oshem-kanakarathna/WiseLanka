"""Content ranking within immutable academic groups, with explicit offline fallback."""
import hashlib
import json
import math
import re
from collections import Counter
from functools import lru_cache
from backend.app.data_loader import load_csv
from backend.app.relevance.encoder import get_encoder, MODEL_ID, REVISION

GROUP_ORDER = {'MET': 0, 'NOT_ASSESSED': 1, 'NOT_MET': 2}


def tokens(text):
    return re.findall(r'[a-z][a-z0-9]+', text.casefold())


def tfidf_scores(documents, query):
    """Smooth IDF, raw term counts, L2 cosine; corpus fitting, no preference training."""
    counts = [Counter(tokens(text)) for text in documents]
    vocabulary = set().union(*(set(c) for c in counts))
    idf = {term: math.log((1+len(counts))/(1+sum(term in c for c in counts)))+1 for term in vocabulary}
    def vector(count):
        values = {term: amount*idf[term] for term,amount in count.items() if term in idf}
        norm = math.sqrt(sum(value*value for value in values.values())) or 1
        return {term:value/norm for term,value in values.items()}
    q = vector(Counter(tokens(query)))
    return [sum(value*q.get(term,0) for term,value in vector(count).items()) for count in counts]


def catalogue_documents():
    """Use source-backed identity/subject fields, never rules or administrative notes."""
    qualifications = {q['qualification_id']:q for q in load_csv('reference/qualifications.csv')}
    return {p['programme_id']: {
        'text': '. '.join(value for value in (
            p.get('programme_name',''), p.get('field_of_study',''), p.get('domain',''),
            qualifications.get(p['qualification_id'],{}).get('qualification_type','')) if value),
        'source_id':p.get('source_id',''), 'source_url':p.get('application_url',''),
        'programme_name':p['programme_name'],
    } for p in load_csv('reference/programmes.csv') if p['programme_status']=='Active'}


def preference_text(profile):
    values = list(profile.get('interests', []))
    intention = profile.get('career_intention','').strip()
    if intention:
        values.append(intention)
    career = next((c for c in load_csv('reference/careers.csv')
                   if c['career_id']==profile.get('career_goal_id') and c['active_status']=='Active'),None)
    if career:
        values.append(career['career_name'])
    return '. '.join(str(value).strip() for value in values if str(value).strip())[:1000]


@lru_cache(maxsize=4)
def document_embeddings(documents):
    encoder, error = get_encoder()
    if encoder is None:
        raise RuntimeError(error or 'Model unavailable')
    return encoder.encode(list(documents))


def academic_status(item):
    return item.get('academic_gap_insights',{}).get('status',item.get('status','NOT_ASSESSED'))


def rank_recommendations(items, profile, method='semantic'):
    if method not in {'semantic','tfidf','deterministic'}:
        raise ValueError('Unsupported relevance method')
    catalogue = catalogue_documents()
    digest = hashlib.sha256(json.dumps(catalogue,sort_keys=True).encode()).hexdigest()
    query = preference_text(profile)
    documents = tuple(catalogue.get(item['programme_id'],{}).get('text','') for item in items)
    catalogue_ids = sorted(catalogue)
    corpus = tuple(catalogue[key]['text'] for key in catalogue_ids)
    lexical_map = dict(zip(catalogue_ids, tfidf_scores(corpus,query))) if corpus and query else {}
    lexical = [lexical_map.get(item['programme_id'],0.0) for item in items]
    semantic = None
    state, used, reason = 'AVAILABLE', method.upper(), None
    if not query:
        state,used,reason = 'NOT_ASSESSED','RULE_BASED_FALLBACK','NO_PREFERENCE'
    elif not items:
        state,used,reason = 'NOT_ASSESSED','RULE_BASED_FALLBACK','NO_CANDIDATES'
    elif method=='semantic':
        try:
            encoder,error = get_encoder()
            if encoder is None:
                raise RuntimeError(error or 'Model unavailable')
            vectors = document_embeddings(corpus)
            query_vector = encoder.encode([query])[0]
            semantic_map = dict(zip(catalogue_ids, vectors@query_vector))
            semantic = [float(semantic_map.get(item['programme_id'],0.0)) for item in items]
            if any(not math.isfinite(value) for value in semantic):
                raise ValueError('Nonfinite score')
            semantic = [max(-1.0,min(1.0,value)) for value in semantic]
        except Exception:
            semantic = None
            document_embeddings.cache_clear()
            state,used,reason = 'UNAVAILABLE','RULE_BASED_FALLBACK','LOCAL_MODEL_UNAVAILABLE'
    results = []
    for index,item in enumerate(items):
        document = catalogue.get(item['programme_id'],{})
        available = bool(documents[index]) and bool(document.get('source_id'))
        score = semantic[index] if semantic is not None and available else lexical[index] if method=='tfidf' and query and available else None
        info = {
            'status':state if available else 'NOT_ASSESSED', 'method':used,
            'score':round(score,6) if score is not None else None,
            'tfidf_score':round(lexical[index],6) if query and available else None,
            'model_revision':REVISION if used=='SEMANTIC' else None,
            'preference_summary':query[:300],
            'catalogue_fact':document.get('text',''), 'source_url':document.get('source_url',''),
            'explanation': (
                'Text similarity compares your stated interests and career intention with the recorded programme title, subject and qualification type. '
                'It does not assess eligibility, competence, admission probability or career success.'
                if score is not None else 'Relevance was not assessed; the existing rule-based order is used. Academic evidence remains separate.'),
        }
        results.append({**item,'relevance':info})
    baseline = {item['programme_id']:i for i,item in enumerate(items)}
    # Eligibility groups are inviolable; similarity can change only within-group order.
    results.sort(key=lambda item: (
        GROUP_ORDER.get(academic_status(item),1),
        -(item['relevance']['score'] if item['relevance']['score'] is not None else -2),
        baseline[item['programme_id']], item['programme_id'],
    ))
    return results, {
        'legacy_order':[item['programme_id'] for item in items],
        'requested_method':method,'method':used,'status':state,'fallback_reason':reason,
        'model_id':MODEL_ID,'model_revision':REVISION,'catalogue_hash':digest,
        'group_order':['MET','NOT_ASSESSED','NOT_MET'],
        'scope':'Relevance within academic groups; not a learned preference model.',
    }
