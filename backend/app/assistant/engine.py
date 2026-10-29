import json
from functools import lru_cache
from typing import Literal, Optional
from pydantic import BaseModel, Field
from backend.app.data_loader import PROJECT_ROOT, load_csv
from backend.app.personalisation.models import LearnerProfile
from backend.app.eligibility.engine import assess_academic_gaps
from backend.app.progression.engine import get_progression_pathways
from backend.app.alternative_pathways.engine import find_alternative_pathways
from backend.app.skills.engine import assess_learner_skills
from backend.app.recommendation.engine import get_programme_careers
from backend.app.scholarships.engine import evaluate_scholarship

Intent = Literal['programme','eligibility','progression','alternatives','skills_topic','careers','scholarships','help']


class GuidanceRequest(BaseModel):
    intent: Intent = 'help'
    programme_id: str = Field(default='',max_length=40)
    question: str = Field(default='',max_length=300)
    language: Literal['en','si','ta'] = 'en'
    learner_profile: Optional[LearnerProfile] = None


@lru_cache(maxsize=1)
def translations():
    return json.loads((PROJECT_ROOT/'data/localisation/ui.json').read_text(encoding='utf-8'))


def translate(language,key):
    return translations().get(language,translations()['en']).get(key,translations()['en'][key])


def options():
    return {'programmes':[{'programme_id':row['programme_id'],'programme_name':row['programme_name']}
                          for row in load_csv('reference/programmes.csv') if row['programme_status']=='Active'],
            'intents':['programme','eligibility','progression','alternatives','skills_topic','careers','scholarships','help']}


def answer(request):
    """Read-only engine calls; never updates profile, ranker, rules or conversation history."""
    intent=request.intent
    if request.question.strip():
        text=request.question.strip().casefold().rstrip('?.!')
        aliases={translate(lang,key).casefold():key for lang in ('en','si','ta')
                 for key in ('programme','eligibility','progression','alternatives','skills_topic','careers','scholarships','help')}
        aliases.update({'eligibility':'eligibility','skills':'skills_topic','progression':'progression',
                        'programme':'programme','careers':'careers','scholarships':'scholarships'})
        intent=aliases.get(text)
    response={'intent':intent,'status':'GROUNDED','language':request.language,
              'summary':translate(request.language,'guidance_note'),'blocks':[], 'sources':[],
              'notice':translate(request.language,'review'), 'generated_by':'DETERMINISTIC_GUIDED_ASSISTANT_V1'}
    def stop(status,key):
        response.update(status=status,summary=translate(request.language,key));return response
    def block(key,lines):
        response['blocks'].append({'heading_key':key,'content_language':'en','lines':lines})
    def source(url,title):
        if url and not any(s['url']==url for s in response['sources']):
            response['sources'].append({'url':url,'title':title})
    if intent is None:return stop('UNSUPPORTED','unsupported')
    if intent=='help':
        response['supported_topics']={key:translate(request.language,key) for key in options()['intents']}
        return response
    if intent=='scholarships':
        for scholarship in load_csv('reference/scholarships.csv'):
            block('scholarships',[scholarship['scholarship_name'],f"Application status: {scholarship['status']}; opening: {scholarship['opening_date']}; closing: {scholarship['closing_date']}",
                                  'Application eligibility is separate from current availability and does not guarantee an award.'])
            # Exam-only profile does not contain citizenship, age or reference-year data.
            # Evaluate unknowns honestly rather than inferring scholarship eligibility.
            assessment=evaluate_scholarship(scholarship['scholarship_id'],{})
            block('NOT_ASSESSED',[f"Personal scholarship eligibility: {assessment.get('status','NOT_ASSESSED')}; required personal/context evidence has not been supplied."])
            source(scholarship['application_url'],scholarship['provider_name'])
        if not response['blocks']:return stop('NOT_ASSESSED','no_evidence')
        return response
    programme=next((p for p in load_csv('reference/programmes.csv') if p['programme_id']==request.programme_id and p['programme_status']=='Active'),None)
    if programme is None:return stop('NEEDS_PROGRAMME','need_programme')
    source(programme['application_url'],programme['programme_name'])
    if intent=='programme':
        block('programme',[programme['programme_name'],programme['field_of_study'],programme['programme_type'],programme.get('notes','')])
    elif intent=='careers':
        careers=get_programme_careers(programme['programme_id'])
        if not careers:return stop('NOT_ASSESSED','no_evidence')
        block('careers',['These are curated programme-career relationships; individual relationship source citations are not recorded. Provider programme links do not independently verify these relevance levels.']+[f"{c['career_name']} — recorded relevance: {c['relevance_level']}; not a job guarantee." for c in careers])
    elif intent=='progression':
        result=get_progression_pathways(programme['qualification_id'])
        response['progression']=result
        if not result['pathways']:return stop('NOT_ASSESSED','no_evidence')
        for pathway in result['pathways']:
            block('progression',[pathway['qualification_name'],pathway['conditions'],'Progression not guaranteed'])
            source(pathway['source_url'],'Progression source')
            source(pathway['supporting_source_url'],'Admission process')
    else:
        if request.learner_profile is None:return stop('NEEDS_PROFILE','need_profile')
        profile=request.learner_profile.model_dump()
        if intent=='eligibility':
            result=assess_academic_gaps(programme['programme_id'],profile['education'],profile['education_complete'],profile['existing_qualifications'])
            response['academic_assessment']=result
            block(result['status'],[result['next_step']])
            for group in result['groups']:
                block(group['status'],[f"{group['operator']} group: "+'; '.join(f"{r['status']}: {r['description']}. {r['explanation']}" for r in group['requirements'])])
                for rule in group['requirements']:source(rule['source_url'],rule['source_organisation'])
        elif intent=='alternatives':
            result=find_alternative_pathways(programme['programme_id'],profile['education'])
            response['alternative_pathways']=result
            if not result.get('alternative_pathways'):return stop('NOT_ASSESSED','no_evidence')
            for route in result['alternative_pathways']:
                block('alternatives',[route['alternative_programme_name'],route['pathway_status_message'],route.get('progression_conditions',''),'Progression not guaranteed'])
                alternative=next((p for p in load_csv('reference/programmes.csv') if p['programme_id']==route['alternative_programme_id']),{})
                source(alternative.get('application_url',''),'Alternative programme source')
        elif intent=='skills_topic':
            result=assess_learner_skills(profile['career_goal_id'],profile['self_reported_skills'])
            response['skill_insights']=result
            block('skills_topic',[result['explanation'],result['evidence_note']]+[
                f"{r['skill_name']}: {r['report_status']}. {r['explanation']}" for r in result['career_requirements']])
            if result['status']=='NOT_ASSESSED':response['status']='NOT_ASSESSED'
    return response
