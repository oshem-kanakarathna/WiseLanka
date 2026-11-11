import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (
    Path(__file__).resolve().parents[1]
    / "pages" / "learner-profile.html"
)


class ProgressionRenderingTests(unittest.TestCase):

    def test_progression_card_displays_correctly(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(PAGE.as_uri())

                page.evaluate("""() => renderRecommendations({
                    recommendations: [{
                        programme_name: "TEST Foundation",
                        category: "ELIGIBLE",
                        academic_match_score: 100,
                        progression: {
                            pathways: [{
                                qualification_name: "TEST Engineering Degree",
                                conditions: "Complete the foundation",
                                guaranteed: false,
                                programmes: [{
                                    provider_name: "TEST Institution"
                                }]
                            }]
                        }
                    }]
                })""")

                card = page.locator(".progression-item")

                self.assertEqual(card.count(), 1)
                self.assertIn("TEST Engineering Degree", card.inner_text())
                self.assertIn("TEST Institution", card.inner_text())
                self.assertIn("Complete the foundation", card.inner_text())
                self.assertIn("Progression not guaranteed", card.inner_text())
            finally:
                browser.close()



    def test_no_progression_pathways(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(PAGE.as_uri())

                page.evaluate("""() => renderRecommendations({
                    recommendations: [{
                        programme_name: "TEST Programme",
                        category: "ELIGIBLE",
                        academic_match_score: 100,
                        progression: {
                            count: 0,
                            pathways: []
                        }
                    }]
                })""")

                self.assertEqual(
                    page.locator(".recommendation-card").count(), 1
                )
                self.assertEqual(
                    page.locator(".academic-progression").count(), 0
                )
            finally:
                browser.close()

if __name__ == "__main__":
    unittest.main()
