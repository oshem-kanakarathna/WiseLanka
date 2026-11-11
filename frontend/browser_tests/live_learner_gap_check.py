"""WP1 synthetic browser-to-real-API scenarios and screenshot evidence.

Requires frontend port 5500 and an updated API. No responses are mocked.
"""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE_URL = 'http://127.0.0.1:5500/frontend/pages/learner-profile.html'
API_BASE = os.environ.get('WISELANKA_API_BASE', 'http://127.0.0.1:8000')
EVIDENCE = Path(os.environ.get('WISELANKA_EVIDENCE_DIR', str(Path(__file__).resolve().parents[2] / 'docs' / 'evidence' / 'wp1')))


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.add_init_script('window.WISELANKA_API_BASE = ' + json.dumps(API_BASE))
            page.goto(PAGE_URL)
            page.locator('#skill-SKL0001').wait_for()
            page.locator('#educationLevel').select_option('O_LEVEL')
            for field, value in {'olMathematics': 'C', 'olEnglish': 'C', 'olGrade3': 'S', 'olGrade4': 'S', 'olGrade5': 'S', 'olGrade6': 'S'}.items():
                page.locator('#' + field).select_option(value)
            page.locator('#educationComplete').check()

            def submit():
                with page.expect_response(lambda r: r.url == API_BASE + '/personalised-recommendations') as info:
                    page.locator('#submitProfile').click()
                response = info.value
                assert response.status == 200, response.text()
                data = response.json()
                page.wait_for_function("!document.querySelector('#submitProfile').disabled")
                return data

            six = submit()
            assert six['count'] == 1
            assert six['academic_insights'][0]['status'] == 'NOT_MET'
            assert 'Not Met' in page.locator('.academic-gap-group').all_inner_texts()[1]
            print('PASS: six-subject complete O/L profile identifies unmet credit count')

            for number in range(7, 10):
                page.locator('#addOlSubject').click()
                page.locator(f'#olGrade{number}').select_option('C' if number == 9 else 'F')
            page.locator('#learnerCategory').select_option('EARLY_CAREER')
            page.locator('#careerGoal').select_option('CAR0001')
            page.locator('#skill-SKL0001').select_option('REPORTED')
            page.locator('#skill-SKL0002').select_option('DEVELOPMENT_OPPORTUNITY')
            nine = submit()
            assert nine['academic_insights'][0]['status'] == 'MET'
            assert nine['recommendations'][0]['eligible'] is True
            skills = {s['skill_id']: s for s in nine['learner_skill_insights']['career_requirements']}
            assert skills['SKL0001']['report_status'] == 'REPORTED'
            assert skills['SKL0002']['report_status'] == 'DEVELOPMENT_OPPORTUNITY'
            assert skills['SKL0003']['status'] == 'NOT_ASSESSED'
            text = page.locator('#learnerInsights').inner_text()
            assert 'competence not verified' in text and 'Development opportunity selected by you' in text
            page.locator('.results-panel').screenshot(path=str(EVIDENCE / 'nine-subject-results.png'))
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            page.locator('#learnerInsights').scroll_into_view_if_needed()
            page.screenshot(path=str(EVIDENCE / 'mobile-skill-insights.png'))
            print('PASS: ninth-subject credit changes eligibility; three skill states and mobile reflow rendered')

            page.locator('#educationComplete').uncheck()
            for field in ['olMathematics', 'olGrade3', 'olGrade4', 'olGrade5', 'olGrade6', 'olGrade7', 'olGrade8', 'olGrade9']:
                page.locator('#' + field).select_option('NOT_REPORTED')
            incomplete = submit()
            assert incomplete['academic_insights'][0]['status'] == 'NOT_ASSESSED'
            assert 'Academic eligibility: Not Assessed' in page.locator('.recommendation-meta').inner_text()
            print('PASS: incomplete evidence is displayed as not assessed')

            page.locator('#educationLevel').select_option('NONE')
            page.locator('#learnerCategory').select_option('VOCATIONAL_LEARNER')
            page.locator('#addQualification').click()
            page.locator('#qualification-1-title').fill('Synthetic vocational qualification')
            page.locator('#qualification-1-framework').fill('NVQ')
            page.locator('#qualification-1-level').fill('4')
            page.locator('#skill-SKL0001').select_option('')
            page.locator('#skill-SKL0002').select_option('')
            award = submit()
            assert award['recommendations'] == []
            assert all(a['status'] == 'NOT_ASSESSED' for a in award['academic_insights'])
            assert all(s['status'] == 'NOT_ASSESSED' for s in award['learner_skill_insights']['career_requirements'])
            assert 'Synthetic vocational qualification' in page.locator('#learnerInsights').inner_text()
            page.set_viewport_size({'width': 1440, 'height': 1000})
            page.get_by_text('Your reported qualifications', exact=True).locator('..').screenshot(
                path=str(EVIDENCE / 'qualification-only.png')
            )
            print('PASS: vocational award retained without inferred equivalence; no reported skills remain unassessed')

            page.locator('.qualification-row select').select_option('QLF0004')
            catalogue = submit()
            award = catalogue['existing_qualifications'][0]
            assert award == {
                'qualification_id': 'QLF0004', 'title': 'Level 3 Diploma',
                'framework': 'Regulated Qualifications Framework', 'level': '3',
            }
            assert all(a['status'] == 'NOT_ASSESSED' for a in catalogue['academic_insights'])
            invalid = page.request.post(API_BASE + '/personalised-recommendations', data={
                'learner_profile': {'education': {}, 'existing_qualifications': [{
                    **award, 'framework': 'NVQ',
                }]},
            })
            assert invalid.status == 422
            print('PASS: catalogue choice returns consistent metadata; contradictory metadata rejected without inferred equivalence')
            assert not errors, errors
            print('PASS: no JavaScript page errors in live WP1 scenarios')
        finally:
            browser.close()


if __name__ == '__main__':
    main()
