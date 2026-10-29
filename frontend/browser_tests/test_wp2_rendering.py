"""Uncertainty rendering must be consistent across the older application pages."""
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

class WP2RenderingTests(unittest.TestCase):
    def test_legacy_pages_do_not_label_unknown_as_eligible_or_rejected(self):
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                page=browser.new_page()
                base=Path(__file__).resolve().parents[1]/'pages'
                page.goto((base/'eligibility.html').as_uri())
                page.evaluate("""displayResult({programme_name:'Synthetic programme',eligible:true,assessment_status:'NOT_ASSESSED',summary:'Provider review required',passed:[],failed:[],not_assessed:['Missing evidence'],source_url:'https://ou.ac.lk'})""")
                self.assertEqual(page.locator('#statusBadge').inner_text(),'Not assessed')
                page.goto((base/'recommendations.html').as_uri())
                self.assertEqual(page.evaluate("getCategoryLabel('NOT_ASSESSED')"),'Not Assessed')
                text=page.evaluate("""() => createAlternativePathwayCard({pathway_status:'NOT_ASSESSED',alternative_programme_name:'Synthetic route',current_eligibility:{},progression_type:'Conditional',pathway_status_message:'Provider review required'}).innerText""")
                self.assertIn('Not assessed',text)
                self.assertNotIn('Requirements not met',text)
            finally:
                browser.close()
