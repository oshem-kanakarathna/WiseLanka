"""Real API/domain scenarios and learner-facing vocational progression."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

API=os.environ.get('WISELANKA_API_BASE','http://127.0.0.1:8000')
EVIDENCE=Path(__file__).resolve().parents[2]/'docs/evidence/wp2'

def main():
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            page=browser.new_page(viewport={'width':1440,'height':1000})
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.add_init_script('window.WISELANKA_API_BASE='+json.dumps(API))
            page.goto('http://127.0.0.1:5500/frontend/pages/learner-profile.html')
            page.locator('#skill-SKL0001').wait_for()
            for i,subject in enumerate(['Business Studies','Economics','Accounting'],1):
                page.locator(f'#alSubject{i}').select_option(subject)
                page.locator(f'#alGrade{i}').select_option('C')
            with page.expect_response(lambda r:r.url==API+'/personalised-recommendations') as response:
                page.locator('#submitProfile').click()
            assert response.value.status==200
            page.wait_for_function("!document.querySelector('#submitProfile').disabled")
            card=page.locator('.recommendation-card').filter(has=page.get_by_role('heading',name='Bachelor of Management Studies Honours',exact=True))
            assert 'Academic eligibility: Not Assessed' in card.inner_text()
            assert 'The Open University of Sri Lanka' in card.inner_text()
            card.screenshot(path=str(EVIDENCE/'business-result.png'))
            print('PASS: Business programme, source organisation and unknown admission status rendered')
            page.locator('#educationLevel').select_option('NONE')
            page.locator('#learnerCategory').select_option('VOCATIONAL_LEARNER')
            page.locator('#addQualification').click()
            page.locator('.qualification-row select').select_option('QLF0010')
            with page.expect_response(lambda r:r.url==API+'/personalised-recommendations'):
                page.locator('#submitProfile').click()
            page.wait_for_function("!document.querySelector('#submitProfile').disabled")
            progression=page.locator('#learnerInsights .academic-progression')
            assert 'Bachelor of Engineering Technology in Mechatronics Technology' in progression.inner_text()
            assert 'Progression not guaranteed' in progression.inner_text()
            assert progression.get_by_role('link',name='Progression source').count()==1
            progression.screenshot(path=str(EVIDENCE/'vocational-progression.png'))
            print('PASS: reported vocational award leads to sourced conditional progression without admission guarantee')
            scenarios=[('IT','PRG0001',{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'},'NOT_ASSESSED'),
                       ('Engineering','PRG0009',{'Combined Mathematics':'B','Physics':'C','Chemistry':'C'},'NOT_ASSESSED'),
                       ('Unmet Physics','PRG0009',{'Combined Mathematics':'B','Physics':'F','Chemistry':'C'},'NOT_MET'),
                       ('Missing Physics','PRG0009',{'Combined Mathematics':'B'},'NOT_ASSESSED'),
                       ('Missing rules','PRG9999',{},'NOT_ASSESSED')]
            for name,pid,results,expected in scenarios:
                result=page.request.post(API+'/eligibility',data={'programme_id':pid,'student_results':{'A_LEVEL':results}})
                assert result.status==200
                assert result.json()['assessment_status']==expected
                print('PASS:',name,expected)
            for qid,dest in [('QLF0012','QLF0010'),('QLF0010','QLF0011')]:
                result=page.request.get(API+'/progression/'+qid).json()
                assert result['pathways'][0]['to_qualification_id']==dest
                assert result['pathways'][0]['guaranteed'] is False
            print('PASS: both vocational progression edges sourced and non-guaranteed')
            assert not errors,errors
            print('PASS: no JavaScript page errors')
        finally:
            browser.close()

if __name__=='__main__':main()
