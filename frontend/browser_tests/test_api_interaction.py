import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (
    Path(__file__).resolve().parents[1]
    / "pages" / "learner-profile.html"
)


class ApiInteractionTests(unittest.TestCase):

    def test_valid_profile_renders_mocked_recommendation(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(PAGE.as_uri())

                page.evaluate("""() => {
                    window.__apiCalls = [];

                    window.fetch = async (url, options) => {
                        window.__apiCalls.push({
                            url,
                            method: options.method,
                            payload: JSON.parse(options.body)
                        });

                        return {
                            ok: true,
                            json: async () => ({
                                recommendations: [{
                                    programme_name: "TEST Computing Foundation",
                                    category: "ELIGIBLE",
                                    academic_match_score: 100,
                                    progression: {
                                        pathways: [{
                                            qualification_name: "TEST Computing Degree",
                                            conditions: "Complete the foundation",
                                            guaranteed: false,
                                            programmes: [{
                                                provider_name: "TEST University"
                                            }]
                                        }]
                                    }
                                }]
                            })
                        };
                    };
                }""")

                page.locator("#educationLevel").select_option("O_LEVEL")

                for field in (
                    "olMathematics", "olEnglish",
                    "olGrade3", "olGrade4",
                    "olGrade5", "olGrade6"
                ):
                    page.locator("#" + field).select_option("C")

                page.locator("#learnerProfileForm").evaluate(
                    "(form) => form.requestSubmit()"
                )

                page.locator(".recommendation-card").wait_for()

                calls = page.evaluate("window.__apiCalls")

                self.assertEqual(len(calls), 1)
                self.assertEqual(calls[0]["method"], "POST")
                self.assertTrue(
                    calls[0]["url"].endswith(
                        "/personalised-recommendations"
                    )
                )

                education = calls[0]["payload"]["learner_profile"]["education"]
                self.assertEqual(education["O_LEVEL"]["Mathematics"], "C")
                self.assertEqual(education["O_LEVEL"]["English"], "C")

                self.assertIn(
                    "TEST Computing Foundation",
                    page.locator(".recommendation-card").inner_text()
                )

                self.assertIn(
                    "TEST Computing Degree",
                    page.locator(".progression-item").inner_text()
                )

            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
