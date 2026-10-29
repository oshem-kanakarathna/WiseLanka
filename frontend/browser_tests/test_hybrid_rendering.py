import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

class HybridRenderingTests(unittest.TestCase):
    def test_relevance_and_uncertainty_remain_separate(self):
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                page=browser.new_page()
                page.route('**/profile-options',lambda route:route.fulfill(json={'skills':[],'qualifications':[]}))
                page.goto((Path(__file__).resolve().parents[1]/'pages/learner-profile.html').as_uri())
                page.evaluate("""renderRecommendations({ranking:{method:'SEMANTIC',status:'AVAILABLE'},recommendations:[{
                    programme_id:'SYNTHETIC',programme_name:'Synthetic engineering programme',category:'ELIGIBLE',academic_match_score:100,
                    academic_gap_insights:{status:'NOT_MET',groups:[],next_step:'Physics requirement not met'},
                    relevance:{method:'SEMANTIC',score:0.99,explanation:'Similarity is not an admission probability',preference_summary:'Design machines',catalogue_fact:'Engineering programme'}
                }]})""")
                card=page.locator('.recommendation-card').inner_text()
                self.assertIn('Academic eligibility: Not Met',card)
                self.assertNotIn('Academic eligibility: Eligible',card)
                self.assertIn('Relevance method: SEMANTIC',card)
                self.assertIn('Design machines',card)
                self.assertIn('not a probability',card)
            finally:browser.close()

    def test_explicit_offline_fallback_message(self):
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                page=browser.new_page()
                page.route('**/profile-options',lambda route:route.fulfill(json={'skills':[],'qualifications':[]}))
                page.goto((Path(__file__).resolve().parents[1]/'pages/learner-profile.html').as_uri())
                page.evaluate("""renderRecommendations({ranking:{method:'RULE_BASED_FALLBACK',status:'UNAVAILABLE',fallback_reason:'LOCAL_MODEL_UNAVAILABLE'},recommendations:[]})""")
                self.assertIn('LOCAL_MODEL_UNAVAILABLE',page.locator('#learnerInsights').inner_text())
            finally:browser.close()
