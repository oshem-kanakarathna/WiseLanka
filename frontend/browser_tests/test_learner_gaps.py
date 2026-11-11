"""Browser contract/interaction checks using synthetic responses."""
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parents[1] / 'pages' / 'learner-profile.html').as_uri()
OPTIONS = {'skills': [{'skill_id': 'SKL0001', 'skill_name': 'Programming'}], 'qualifications': []}


class LearnerGapTests(unittest.TestCase):
    def setUp(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.route('**/profile-options', lambda route: route.fulfill(json=OPTIONS))
        self.payloads = []
        def submit(route):
            self.payloads.append(route.request.post_data_json)
            route.fulfill(json={'recommendations': [], 'academic_insights': [], 'learner_skill_insights': {
                'explanation': 'No competence assessment was performed.', 'career_requirements': [
                    {'skill_id': 'SKL0001', 'skill_name': 'Programming', 'report_status': 'REPORTED', 'expected_level': 'High', 'explanation': 'Self-report only.'},
                    {'skill_id': 'SKL0002', 'skill_name': 'Object-Oriented Programming', 'report_status': 'UNREPORTED', 'explanation': 'Not assessed.'},
                ], 'reported_skills': [],
            }})
        self.page.route('**/personalised-recommendations', submit)
        self.page.goto(PAGE)
        self.page.locator('#skill-SKL0001').wait_for()

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()

    def fill_six(self):
        self.page.locator('#educationLevel').select_option('O_LEVEL')
        for field in ['olMathematics', 'olEnglish', 'olGrade3', 'olGrade4', 'olGrade5', 'olGrade6']:
            self.page.locator('#' + field).select_option('C')

    def submit(self):
        self.page.locator('#submitProfile').click()

    def test_nine_subject_payload_and_skill_states(self):
        self.fill_six()
        for n in range(7, 10):
            self.page.locator('#addOlSubject').click()
            self.page.locator(f'#olGrade{n}').select_option('C')
        self.page.locator('#educationComplete').check()
        self.page.locator('#skill-SKL0001').select_option('REPORTED')
        self.submit()
        self.page.locator('.learner-skill-list').wait_for()
        profile = self.payloads[0]['learner_profile']
        self.assertEqual(len(profile['education']['O_LEVEL']), 9)
        self.assertTrue(profile['education_complete']['O_LEVEL'])
        self.assertEqual(profile['self_reported_skills'][0]['status'], 'REPORTED')
        text = self.page.locator('#learnerInsights').inner_text()
        self.assertIn('competence not verified', text)
        self.assertIn('Not reported; not assessed', text)
        self.assertIn('Recorded career level: High', text)
        self.assertEqual(self.errors, [])

    def test_added_row_requires_grade_and_can_be_removed(self):
        self.fill_six()
        self.page.locator('#addOlSubject').click()
        self.submit()
        self.assertIn('Please select grades for:', self.page.locator('#statusMessage').inner_text())
        self.assertEqual(self.payloads, [])
        self.page.get_by_role('button', name='Remove subject 7', exact=True).click()
        self.submit()
        self.page.locator('.learner-skill-list').wait_for()
        self.assertEqual(len(self.payloads[0]['learner_profile']['education']['O_LEVEL']), 6)

    def test_custom_subject_cannot_duplicate_fixed_mathematics(self):
        self.fill_six()
        self.page.locator('#olSubject3').select_option('Other subject')
        self.page.locator('#olCustom3').fill('Mathematics')
        self.submit()
        self.assertIn('more than once', self.page.locator('#statusMessage').inner_text())
        self.assertEqual(self.payloads, [])

    def test_qualification_only_early_career_payload(self):
        self.page.locator('#learnerCategory').select_option('EARLY_CAREER')
        self.page.locator('#educationLevel').select_option('NONE')
        self.page.locator('#addQualification').click()
        self.page.locator('#qualification-1-title').fill('Synthetic technical diploma')
        self.page.locator('#qualification-1-framework').fill('NVQ')
        self.page.locator('#qualification-1-level').fill('4')
        self.submit()
        self.page.locator('.learner-skill-list').wait_for()
        profile = self.payloads[0]['learner_profile']
        self.assertEqual(profile['education'], {})
        self.assertEqual(profile['existing_qualifications'][0]['level'], '4')
        self.assertEqual(profile['learner_category'], 'EARLY_CAREER')

    def test_complete_confirmation_conflicts_with_unreported_result(self):
        self.fill_six()
        self.page.locator('#olEnglish').select_option('NOT_REPORTED')
        self.page.locator('#educationComplete').check()
        self.submit()
        self.assertIn('Uncheck', self.page.locator('#statusMessage').inner_text())
        self.assertEqual(self.payloads, [])

    def test_empty_qualification_only_profile_is_blocked(self):
        self.page.locator('#educationLevel').select_option('NONE')
        self.submit()
        self.assertIn('Provide examination results', self.page.locator('#statusMessage').inner_text())
        self.assertEqual(self.payloads, [])

    def test_options_failure_keeps_manual_awards_available(self):
        self.page.route('**/profile-options', lambda route: route.abort())
        self.page.reload()
        self.page.locator('#retryProfileOptions').wait_for(state='visible')
        self.page.locator('#addQualification').click()
        self.assertTrue(self.page.locator('#qualification-1-title').is_visible())

    def test_mobile_reflow_and_labels(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.fill_six()
        self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
        self.assertEqual(self.page.locator('label[for="skill-SKL0001"]').inner_text(), 'Programming')
        self.page.locator('#addOlSubject').focus()
        self.page.keyboard.press('Enter')
        self.assertTrue(self.page.locator('#olSubject7').evaluate('(node) => node === document.activeElement'))

    def test_delayed_catalogue_updates_existing_row_without_losing_manual_input(self):
        pending = []
        self.page.route('**/profile-options', lambda route: pending.append(route))
        self.page.reload(wait_until='domcontentloaded')
        self.page.locator('#addQualification').click()
        self.page.locator('#qualification-1-title').fill('Synthetic manual award')
        self.page.locator('#qualification-1-framework').fill('NVQ')
        self.page.wait_for_function("document.querySelector('#profileOptionsStatus').textContent.includes('Loading')")
        self.assertEqual(len(pending), 1)
        pending[0].fulfill(json={**OPTIONS, 'qualifications': [{
            'qualification_id': 'QLF0004', 'qualification_name': 'Level 3 Diploma',
            'framework_name': 'Regulated Qualifications Framework', 'framework_level': '3',
        }]})
        self.page.locator('.qualification-row select option[value="QLF0004"]').wait_for(state='attached')
        self.assertEqual(self.page.locator('#qualification-1-title').input_value(), 'Synthetic manual award')
        self.assertEqual(self.page.locator('#qualification-1-framework').input_value(), 'NVQ')
        self.assertEqual(self.page.locator('.qualification-row select').input_value(), '')

    def test_retry_populates_existing_award_and_catalogue_edit_becomes_custom(self):
        self.page.route('**/profile-options', lambda route: route.abort())
        self.page.reload()
        self.page.locator('#retryProfileOptions').wait_for(state='visible')
        self.page.locator('#addQualification').click()
        self.page.route('**/profile-options', lambda route: route.fulfill(json={**OPTIONS, 'qualifications': [{
            'qualification_id': 'QLF0004', 'qualification_name': 'Level 3 Diploma',
            'framework_name': 'Regulated Qualifications Framework', 'framework_level': '3',
        }]}))
        self.page.locator('#retryProfileOptions').click()
        self.page.locator('.qualification-row select option[value="QLF0004"]').wait_for(state='attached')
        self.page.locator('.qualification-row select').select_option('QLF0004')
        self.assertEqual(self.page.locator('#qualification-1-title').input_value(), 'Level 3 Diploma')
        self.assertEqual(self.page.locator('#qualification-1-level').input_value(), '3')
        self.page.locator('#qualification-1-title').fill('Synthetic custom diploma')
        self.assertEqual(self.page.locator('.qualification-row select').input_value(), '')
        self.page.locator('#educationLevel').select_option('NONE')
        self.submit()
        self.page.locator('.learner-skill-list').wait_for()
        self.assertEqual(self.payloads[0]['learner_profile']['existing_qualifications'][0]['qualification_id'], '')

    def test_qualification_removal_returns_focus_to_add_button(self):
        self.page.locator('#addQualification').click()
        self.page.get_by_role('button', name='Remove qualification 1', exact=True).focus()
        self.page.keyboard.press('Enter')
        self.assertTrue(self.page.locator('#addQualification').evaluate('(node) => node === document.activeElement'))

    def test_qualification_middle_removal_focuses_next_row(self):
        for _ in range(3):
            self.page.locator('#addQualification').click()
        self.page.get_by_role('button', name='Remove qualification 2', exact=True).focus()
        self.page.keyboard.press('Enter')
        self.assertTrue(self.page.locator('.qualification-row').nth(1).locator('select').evaluate('(node) => node === document.activeElement'))

    def test_subject_removal_returns_focus_to_previous_subject(self):
        self.fill_six()
        self.page.locator('#addOlSubject').click()
        self.page.get_by_role('button', name='Remove subject 7', exact=True).focus()
        self.page.keyboard.press('Enter')
        self.assertTrue(self.page.locator('#olSubject6').evaluate('(node) => node === document.activeElement'))
